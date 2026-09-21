from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import sha256_value


SYSTEM_HISTORY_FIELDS = {
    "schema_version", "dataset_version", "corpus_stage", "history_id", "family_id",
    "partition", "timeline", "checkpoint_requests", "downstream_tasks",
}
SEMANTIC_EVENT_FIELDS = {
    "event_id", "sequence", "occurred_at", "recorded_at", "event_type", "content",
    "source_status", "deletion_target_ids",
}


def _event_sequence(history: dict[str, Any], event_id: str) -> int:
    return next(event["sequence"] for event in history["timeline"] if event["event_id"] == event_id)


def _timeline_at(history: dict[str, Any], sequence: int) -> list[dict[str, Any]]:
    timeline = [deepcopy(event) for event in history["timeline"] if event["sequence"] <= sequence]
    deleted: set[str] = set()
    redacted: set[str] = set()
    for event in timeline:
        if event["event_type"] == "deletion":
            deleted.update(event.get("deletion_target_ids", []))
        elif event["event_type"] == "redaction":
            redacted.update(event.get("deletion_target_ids", []))
    for event in timeline:
        if event["event_id"] in deleted:
            event["content"] = None
            event["source_status"] = "deleted"
            event["metadata"] = {}
        elif event["event_id"] in redacted:
            event["content"] = None
            event["source_status"] = "redacted"
            event["metadata"] = {}
    return timeline


def _source_statuses_at(history: dict[str, Any], sequence: int) -> dict[str, str]:
    return {event["event_id"]: event["source_status"]
            for event in _timeline_at(history, sequence)}


def _project_snapshot(history: dict[str, Any], snapshot: dict[str, Any],
                      sequence: int) -> dict[str, Any]:
    statuses = _source_statuses_at(history, sequence)
    source_statuses = {statuses.get(source_id, "present")
                       for source_id in snapshot["source_event_ids"]}
    if source_statuses and source_statuses <= {"deleted", "redacted"}:
        status = "deleted" if "deleted" in source_statuses else "redacted"
        return {
            "snapshot_id": snapshot["snapshot_id"],
            "item_id": snapshot["item_id"],
            "captured_after_sequence": snapshot["captured_after_sequence"],
            "source_event_ids": deepcopy(snapshot["source_event_ids"]),
            "source_status": status,
            "tombstoned": True,
        }
    return deepcopy(snapshot)


def _semantic_event(event: dict[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(event[key]) for key in SEMANTIC_EVENT_FIELDS}


def build_system_history_projection(history: dict[str, Any], *, sequence: int | None = None) -> dict[str, Any]:
    maximum = sequence if sequence is not None else max(event["sequence"] for event in history["timeline"])
    projection = {key: deepcopy(history[key]) for key in SYSTEM_HISTORY_FIELDS}
    projection["timeline"] = _timeline_at(history, maximum)
    projection["checkpoint_requests"] = [item for item in projection["checkpoint_requests"]
                                         if item["after_sequence"] <= maximum]
    visible_checkpoints = {item["checkpoint_id"] for item in projection["checkpoint_requests"]}
    projection["downstream_tasks"] = [item for item in projection["downstream_tasks"]
                                      if item["checkpoint_id"] in visible_checkpoints]
    projection["projection_sha256"] = sha256_value(projection)
    return projection


def build_retrieval_projection(history: dict[str, Any], pair_id: str) -> dict[str, Any]:
    pair = next(item for item in history["pair_inputs"] if item["pair_id"] == pair_id)
    pool = next(item for item in history["candidate_pools"]
                if item["candidate_pool_id"] == pair["candidate_pool_id"])
    snapshots = {item["snapshot_id"]: item for item in history["candidate_snapshots"]}
    sequence = _event_sequence(history, pair["event_id"])
    projection = {
        "track": "candidate_retrieval",
        "history": build_system_history_projection(history, sequence=sequence),
        "event_id": pair["event_id"],
        "candidate_pool_id": pool["candidate_pool_id"],
        "candidates": [_project_snapshot(history, snapshots[identity], sequence)
                       for identity in pool["snapshot_ids"]],
    }
    projection["history"]["checkpoint_requests"] = []
    projection["history"]["downstream_tasks"] = []
    projection["history"]["timeline"] = [
        _semantic_event(event) for event in projection["history"]["timeline"]]
    projection["history"].pop("projection_sha256", None)
    projection["history"]["projection_sha256"] = sha256_value(projection["history"])
    projection["projection_sha256"] = sha256_value(projection)
    return projection


def build_pair_classification_projection(history: dict[str, Any], pair_id: str) -> dict[str, Any]:
    pair = next(item for item in history["pair_inputs"] if item["pair_id"] == pair_id)
    snapshots = {item["snapshot_id"]: item for item in history["candidate_snapshots"]}
    sequence = _event_sequence(history, pair["event_id"])
    visible_timeline = {event["event_id"]: event for event in _timeline_at(history, sequence)}
    context = [visible_timeline[event_id] for event_id in pair["context_event_ids"]]
    projection = {
        "track": "pair_classification",
        "history_id": history["history_id"],
        "pair_id": pair_id,
        "event": _semantic_event(visible_timeline[pair["event_id"]]),
        "context_events": [_semantic_event(event) for event in context],
        "candidate_snapshot": _project_snapshot(
            history, snapshots[pair["candidate_snapshot_id"]], sequence),
    }
    projection["projection_sha256"] = sha256_value(projection)
    return projection


def contains_evaluator_only_material(value: Any, canaries: set[str]) -> bool:
    if isinstance(value, str):
        return any(canary in value for canary in canaries)
    if isinstance(value, list):
        return any(contains_evaluator_only_material(item, canaries) for item in value)
    if isinstance(value, dict):
        if "evaluator_only" in value:
            return True
        return any(contains_evaluator_only_material(item, canaries) for item in value.values())
    return False
