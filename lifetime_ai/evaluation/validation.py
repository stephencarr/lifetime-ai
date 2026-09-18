from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .canonical import sha256_value


RELATIONSHIPS = {"supports", "contradicts", "narrows_scope", "supersedes", "unrelated", "uncertain"}
DISPOSITIONS = {"accept", "reject_unauthorized", "reject_invalid", "abstain", "no_op"}


class CorpusValidationError(ValueError):
    pass


@lru_cache(maxsize=1)
def _schema_validator() -> Draft202012Validator:
    schema_root = Path(__file__).resolve().parents[2] / "evaluation" / "schema"
    schemas = [json.loads(path.read_text(encoding="utf-8"))
               for path in sorted(schema_root.glob("*.schema.json"))]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas)
    history_schema = next(schema for schema in schemas if schema["$id"].endswith("history-v1.json"))
    return Draft202012Validator(history_schema, registry=registry)


def _unique(records: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record[key]
        if identity in indexed:
            raise CorpusValidationError(f"duplicate {label}: {identity}")
        indexed[identity] = record
    return indexed


def validate_history(history: dict[str, Any]) -> None:
    errors = sorted(_schema_validator().iter_errors(history), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "$"
        raise CorpusValidationError(f"JSON Schema violation at {location}: {first.message}")
    required = {
        "schema_version", "dataset_version", "corpus_stage", "history_id", "family_id",
        "partition", "generation_origin", "reviewer_status", "difficulty_tags", "feature_tags",
        "timeline", "candidate_snapshots", "candidate_pools", "pair_inputs",
        "checkpoint_requests", "downstream_tasks", "evaluator_only",
    }
    missing = required - set(history)
    if missing:
        raise CorpusValidationError(f"missing history fields: {sorted(missing)}")
    if history["corpus_stage"] != "pilot":
        raise CorpusValidationError("pilot validator accepts only corpus_stage=pilot")
    if history["partition"] not in {"pilot_development", "pilot_holdout"}:
        raise CorpusValidationError("invalid pilot partition")

    events = _unique(history["timeline"], "event_id", "event")
    sequences = [event["sequence"] for event in history["timeline"]]
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        raise CorpusValidationError("event sequences must be unique and ordered")
    snapshots = _unique(history["candidate_snapshots"], "snapshot_id", "snapshot")
    pools = _unique(history["candidate_pools"], "candidate_pool_id", "candidate pool")
    pairs = _unique(history["pair_inputs"], "pair_id", "pair")
    pair_gold = _unique(history["evaluator_only"]["pair_gold"], "pair_id", "pair gold")
    if set(pairs) != set(pair_gold):
        raise CorpusValidationError("pair inputs and evaluator gold do not match")

    for snapshot in snapshots.values():
        payload = snapshot["canonical_payload"]
        if snapshot["sha256"] != sha256_value(payload):
            raise CorpusValidationError(f"candidate snapshot hash mismatch: {snapshot['snapshot_id']}")
        if any(source not in events for source in snapshot["source_event_ids"]):
            raise CorpusValidationError("candidate snapshot references an unknown event")
    for pool in pools.values():
        material = {"captured_after_sequence": pool["captured_after_sequence"],
                    "snapshot_ids": pool["snapshot_ids"]}
        if pool["sha256"] != sha256_value(material):
            raise CorpusValidationError(f"candidate pool hash mismatch: {pool['candidate_pool_id']}")
        if any(snapshot_id not in snapshots for snapshot_id in pool["snapshot_ids"]):
            raise CorpusValidationError("candidate pool references an unknown snapshot")
        if any(snapshots[snapshot_id]["captured_after_sequence"] > pool["captured_after_sequence"]
               for snapshot_id in pool["snapshot_ids"]):
            raise CorpusValidationError("candidate pool contains a future snapshot")

    for pair_id, pair in pairs.items():
        if pair["event_id"] not in events or pair["candidate_pool_id"] not in pools:
            raise CorpusValidationError(f"pair {pair_id} references missing input")
        snapshot_id = pair.get("candidate_snapshot_id")
        if snapshot_id and snapshot_id not in pools[pair["candidate_pool_id"]]["snapshot_ids"]:
            raise CorpusValidationError("gold candidate is outside isolated pool")
        gold = pair_gold[pair_id]
        if gold["semantic_relationship"] not in RELATIONSHIPS:
            raise CorpusValidationError("unknown semantic relationship")
        if gold["transition_disposition"] not in DISPOSITIONS:
            raise CorpusValidationError("unknown transition disposition")

        action_tasks = [task for task in history["downstream_tasks"]
                        if task["task_type"] == "action_selection"]
        expected_action = gold["expected_external_action"]
        if expected_action == "none" and action_tasks:
            raise CorpusValidationError(
                "expected_external_action=none requires no action-selection task")
        if expected_action != "none" and not action_tasks:
            raise CorpusValidationError(
                "a non-none external action requires an action-selection task")

        effect = gold["expected_state_effect"]["effect"]
        pair_event = events[pair["event_id"]]
        snapshot = snapshots[pair["candidate_snapshot_id"]]
        if effect == "invalidate":
            if pair_event["event_type"] != "deletion":
                raise CorpusValidationError("invalidate effect must use a deletion pair event")
            if not set(snapshot["source_event_ids"]).intersection(pair_event["deletion_target_ids"]):
                raise CorpusValidationError("deletion must target a candidate source event")
        if effect == "expire":
            valid_until = snapshot["canonical_payload"]["valid_until"]
            if pair_event["event_type"] != "time_advance" or valid_until is None:
                raise CorpusValidationError(
                    "expire effect requires a time-advance pair event and explicit valid_until")
            if valid_until > pair_event["occurred_at"]:
                raise CorpusValidationError("expiry checkpoint precedes candidate valid_until")

    task_ids = {task["task_id"] for task in history["downstream_tasks"]}
    gold_task_ids = {task["task_id"] for task in history["evaluator_only"]["downstream_task_gold"]}
    if task_ids != gold_task_ids:
        raise CorpusValidationError("downstream task inputs and gold do not match")


def validate_corpus(histories: list[dict[str, Any]]) -> None:
    history_ids: set[str] = set()
    family_partitions: dict[str, str] = {}
    for history in histories:
        validate_history(history)
        if history["history_id"] in history_ids:
            raise CorpusValidationError("duplicate history id")
        history_ids.add(history["history_id"])
        previous = family_partitions.setdefault(history["family_id"], history["partition"])
        if previous != history["partition"]:
            raise CorpusValidationError("history family crosses partitions")
