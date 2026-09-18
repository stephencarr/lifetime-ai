from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import sha256_value


SYSTEM_HISTORY_FIELDS = {
    "schema_version", "dataset_version", "corpus_stage", "history_id", "family_id",
    "partition", "timeline", "checkpoint_requests", "downstream_tasks",
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


def build_system_history_projection(history: dict[str, Any], *, sequence: int | None = None) -> dict[str, Any]:
    maximum = sequence if sequence is not None else max(event["sequence"] for event in history["timeline"])
    projection = {key: deepcopy(history[key]) for key in SYSTEM_HISTORY_FIELDS}
    projection["timeline"] = _timeline_at(history, maximum)
    projection["checkpoint_requests"] = [item for item in projection["checkpoint_requests"]
                                         if item["after_sequence"] <= maximum]
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
        "candidates": [deepcopy(snapshots[identity]) for identity in pool["snapshot_ids"]],
    }
    projection["projection_sha256"] = sha256_value(projection)
    return projection


def build_pair_classification_projection(history: dict[str, Any], pair_id: str) -> dict[str, Any]:
    pair = next(item for item in history["pair_inputs"] if item["pair_id"] == pair_id)
    snapshots = {item["snapshot_id"]: item for item in history["candidate_snapshots"]}
    sequence = _event_sequence(history, pair["event_id"])
    projection = {
        "track": "pair_classification",
        "history": build_system_history_projection(history, sequence=sequence),
        "event_id": pair["event_id"],
        "candidate_snapshot": deepcopy(snapshots[pair["candidate_snapshot_id"]]),
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
