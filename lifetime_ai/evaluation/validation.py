from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
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


def review_content_sha256(history: dict[str, Any]) -> str:
    """Hash substantive review material while excluding the review decision itself."""
    material = deepcopy(history)
    material.pop("reviewer_status", None)
    evaluator = material["evaluator_only"]
    evaluator.pop("generation_and_review_provenance", None)
    for gold in evaluator["pair_gold"]:
        gold.pop("adjudication_status", None)
        gold.pop("adjudication_notes", None)
    return sha256_value(material)


def _rfc3339_utc(value: str, label: str) -> datetime:
    if not value.endswith("Z"):
        raise CorpusValidationError(f"{label} must be an RFC3339 UTC timestamp")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise CorpusValidationError(f"{label} must be an RFC3339 UTC timestamp") from error


@lru_cache(maxsize=1)
def _schema_validator() -> Draft202012Validator:
    schema_root = Path(__file__).resolve().parents[2] / "evaluation" / "schema"
    schemas = [json.loads(path.read_text(encoding="utf-8"))
               for path in sorted(schema_root.glob("*.schema.json"))]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas)
    history_schema = next(
        schema for schema in schemas
        if schema["$id"] == "https://lifetime-ai.local/schema/history-v1.json"
    )
    return Draft202012Validator(history_schema, registry=registry)


def _unique(records: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record[key]
        if identity in indexed:
            raise CorpusValidationError(f"duplicate {label}: {identity}")
        indexed[identity] = record
    return indexed


def _project_invalidated_derivatives(
    checkpoint: dict[str, Any], derivative_ids: set[str]
) -> list[dict[str, Any]]:
    return [
        item for item in checkpoint["invalidated_derivatives"]
        if item["derivative_id"] in derivative_ids
    ]


def validate_history(
    history: dict[str, Any],
    *,
    schema_validator: Draft202012Validator | None = None,
    expected_corpus_stage: str = "pilot",
    allowed_partitions: set[str] | None = None,
) -> None:
    validator = schema_validator or _schema_validator()
    errors = sorted(validator.iter_errors(history), key=lambda error: list(error.path))
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
    if history["corpus_stage"] != expected_corpus_stage:
        raise CorpusValidationError(
            f"validator accepts only corpus_stage={expected_corpus_stage}"
        )
    partitions = allowed_partitions or {"pilot_development", "pilot_holdout"}
    if history["partition"] not in partitions:
        raise CorpusValidationError(
            f"invalid partition {history['partition']!r}; expected one of {sorted(partitions)}"
        )

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
        if any(source not in events for source in snapshot["counterevidence_event_ids"]):
            raise CorpusValidationError("candidate snapshot references unknown counterevidence")
        if any(events[source]["sequence"] > snapshot["captured_after_sequence"]
               for source in snapshot["source_event_ids"] + snapshot["counterevidence_event_ids"]):
            raise CorpusValidationError("candidate snapshot references future evidence")
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
        pair_sequence = events[pair["event_id"]]["sequence"]
        if pools[pair["candidate_pool_id"]]["captured_after_sequence"] > pair_sequence:
            raise CorpusValidationError("pair references a future candidate pool")
        if any(context_id not in events for context_id in pair["context_event_ids"]):
            raise CorpusValidationError("pair references unknown context")
        if any(events[context_id]["sequence"] > pair_sequence
               for context_id in pair["context_event_ids"]):
            raise CorpusValidationError("pair context contains a future event")
        gold = pair_gold[pair_id]
        if gold["semantic_relationship"] not in RELATIONSHIPS:
            raise CorpusValidationError("unknown semantic relationship")
        if gold["transition_disposition"] not in DISPOSITIONS:
            raise CorpusValidationError("unknown transition disposition")

        action_tasks = [task for task in history["downstream_tasks"]
                        if task["task_type"] == "action_selection"
                        and task["pair_id"] == pair_id]
        expected_action = gold["expected_external_action"]
        if expected_action == "none" and action_tasks:
            raise CorpusValidationError(
                "expected_external_action=none requires no action-selection task")
        if expected_action != "none" and len(action_tasks) != 1:
            raise CorpusValidationError(
                "a non-none external action requires exactly one action-selection task")

        effect = gold["expected_state_effect"]["effect"]
        pair_event = events[pair["event_id"]]
        if pair["candidate_snapshot_id"] is None:
            raise CorpusValidationError("classification pair requires a candidate snapshot")
        snapshot = snapshots[pair["candidate_snapshot_id"]]
        if pair.get("candidate_item_id") != snapshot["item_id"]:
            raise CorpusValidationError("pair candidate_item_id does not match its snapshot item_id")
        if effect == "invalidate":
            if pair_event["event_type"] not in {"deletion", "redaction"}:
                raise CorpusValidationError(
                    "invalidate effect must use a deletion or redaction pair event")
            if not set(snapshot["source_event_ids"]).intersection(pair_event["deletion_target_ids"]):
                raise CorpusValidationError("deletion must target a candidate source event")
        if pair_event["event_type"] in {"deletion", "redaction"}:
            if gold["semantic_relationship"] != "unrelated":
                raise CorpusValidationError(
                    "lifecycle control events must be semantically unrelated"
                )
            if any(target not in events for target in pair_event["deletion_target_ids"]):
                raise CorpusValidationError("lifecycle event references an unknown deletion target")
            event_time = _rfc3339_utc(pair_event["occurred_at"], "lifecycle occurred_at")
            if any(_rfc3339_utc(events[target]["occurred_at"], "target occurred_at") > event_time
                   for target in pair_event["deletion_target_ids"]):
                raise CorpusValidationError("lifecycle event cannot predate its target source")
        if effect == "expire":
            if gold["semantic_relationship"] != "unrelated":
                raise CorpusValidationError(
                    "time-advance expiry events must be semantically unrelated"
                )
            valid_until = snapshot["canonical_payload"]["valid_until"]
            if pair_event["event_type"] != "time_advance" or valid_until is None:
                raise CorpusValidationError(
                    "expire effect requires a time-advance pair event and explicit valid_until")
            advance_to = pair_event["metadata"].get("advance_to")
            if not isinstance(advance_to, str):
                raise CorpusValidationError(
                    "time-advance expiry event requires RFC3339 metadata.advance_to")
            advance_time = _rfc3339_utc(advance_to, "metadata.advance_to")
            expiry_time = _rfc3339_utc(valid_until, "candidate valid_until")
            if advance_to != pair_event["occurred_at"]:
                raise CorpusValidationError(
                    "time-advance occurred_at must equal metadata.advance_to")
            if expiry_time > advance_time:
                raise CorpusValidationError("expiry checkpoint precedes candidate valid_until")

    checkpoints = _unique(history["checkpoint_requests"], "checkpoint_id", "checkpoint")
    checkpoint_gold = _unique(
        history["evaluator_only"]["checkpoint_gold"], "checkpoint_id", "checkpoint gold")
    if set(checkpoints) != set(checkpoint_gold):
        raise CorpusValidationError("checkpoint requests and checkpoint gold do not match")
    maximum_sequence = max(sequences)
    if any(item["after_sequence"] > maximum_sequence for item in checkpoints.values()):
        raise CorpusValidationError("checkpoint references a future sequence")
    for checkpoint_id, gold_checkpoint in checkpoint_gold.items():
        checkpoint_sequence = checkpoints[checkpoint_id]["after_sequence"]
        # Frozen histories preserve every content-bearing historical event here,
        # including events that lack authority to affect current state.
        expected_assertions = {
            event["event_id"] for event in history["timeline"]
            if event["sequence"] <= checkpoint_sequence
            and event["event_type"] in {"message", "observation", "action_outcome"}
        }
        asserted_events = [
            event_id for assertion in gold_checkpoint["historical_assertions"]
            for event_id in assertion["source_event_ids"]
        ]
        if (history["corpus_stage"] == "frozen_g4"
                and (set(asserted_events) != expected_assertions
                     or len(asserted_events) != len(set(asserted_events)))):
            raise CorpusValidationError(
                "checkpoint historical assertions must cover each eligible source event exactly once")
        evidence_ids: list[str] = []
        for assertion in gold_checkpoint["historical_assertions"]:
            evidence_ids.extend(assertion["source_event_ids"])
        for item in gold_checkpoint["current_state"]:
            evidence_ids.extend(item["evidence_ids"])
            evidence_ids.extend(item["counterevidence_ids"])
        for derivative in gold_checkpoint["invalidated_derivatives"]:
            evidence_ids.append(derivative["invalidated_by_event_id"])
        if any(evidence_id not in events for evidence_id in evidence_ids):
            raise CorpusValidationError("checkpoint gold references unknown evidence")
        if any(events[evidence_id]["sequence"] > checkpoint_sequence
               for evidence_id in evidence_ids):
            raise CorpusValidationError("checkpoint gold references future evidence")
        if history["corpus_stage"] == "frozen_g4":
            assertion_ids = [item["assertion_id"]
                             for item in gold_checkpoint["historical_assertions"]]
            if len(assertion_ids) != len(set(assertion_ids)):
                raise CorpusValidationError("checkpoint contains duplicate assertion IDs")
            derivative_ids = [item["derivative_id"]
                              for item in gold_checkpoint["invalidated_derivatives"]]
            if len(derivative_ids) != len(set(derivative_ids)):
                raise CorpusValidationError("checkpoint contains duplicate derivative IDs")
        semantic_keys: set[tuple[str, str]] = set()
        state_refs: set[str] = set()
        for item in gold_checkpoint["current_state"]:
            if history["corpus_stage"] == "frozen_g4" and item["semantic_item_ref"] in state_refs:
                raise CorpusValidationError("checkpoint contains duplicate semantic item references")
            state_refs.add(item["semantic_item_ref"])
            key = (" ".join(item["proposition"].casefold().split()),
                   sha256_value(item["scope"]))
            if key in semantic_keys:
                raise CorpusValidationError(
                    "checkpoint contains duplicate proposition and scope")
            semantic_keys.add(key)

    if history["corpus_stage"] == "frozen_g4":
        expected_status = {
            "resolve": "resolved",
            "expire": "expired",
            "invalidate": "invalidated",
        }
        for pair_id, pair in pairs.items():
            pair_sequence = events[pair["event_id"]]["sequence"]
            later_checkpoints = [
                checkpoint_id for checkpoint_id, request in checkpoints.items()
                if request["after_sequence"] >= pair_sequence
            ]
            if not later_checkpoints:
                raise CorpusValidationError(
                    f"pair {pair_id} has no checkpoint at or after its event")
            checkpoint_id = min(
                later_checkpoints,
                key=lambda item: checkpoints[item]["after_sequence"],
            )
            if checkpoints[checkpoint_id]["after_sequence"] != pair_sequence:
                raise CorpusValidationError(
                    f"pair {pair_id} requires a checkpoint exactly at its event sequence")
            prior_checkpoints = [
                candidate_id for candidate_id, request in checkpoints.items()
                if request["after_sequence"] < pair_sequence
            ]
            if not prior_checkpoints:
                raise CorpusValidationError(
                    f"pair {pair_id} requires a baseline checkpoint before its event")
            before_checkpoint_id = max(
                prior_checkpoints,
                key=lambda candidate_id: checkpoints[candidate_id]["after_sequence"],
            )
            before_items = {
                item["semantic_item_ref"]: item
                for item in checkpoint_gold[before_checkpoint_id]["current_state"]
            }
            state_items = {
                item["semantic_item_ref"]: item
                for item in checkpoint_gold[checkpoint_id]["current_state"]
            }
            effect_spec = pair_gold[pair_id]["expected_state_effect"]
            effect = effect_spec["effect"]
            disposition = pair_gold[pair_id]["transition_disposition"]
            affected = set(effect_spec["affected_item_ids"])
            expected_new = set(effect_spec["expected_new_item_ids"])
            affected_derivative_ids = set(effect_spec.get("affected_derivative_ids", []))
            if "affected_derivative_ids" not in effect_spec:
                raise CorpusValidationError(
                    f"pair {pair_id} must explicitly declare affected_derivative_ids")
            if effect != "invalidate" and affected_derivative_ids:
                raise CorpusValidationError(
                    f"pair {pair_id} effect {effect} cannot declare affected derivative IDs")
            if disposition in {"reject_unauthorized", "reject_invalid", "no_op"} and effect != "none":
                raise CorpusValidationError(
                    f"pair {pair_id} non-accepting disposition cannot mutate state")
            if disposition == "abstain" and effect not in {"none", "preserve_conflict"}:
                raise CorpusValidationError(
                    f"pair {pair_id} abstention allows only no-op or preserved-conflict state")
            if affected & expected_new:
                raise CorpusValidationError(
                    f"pair {pair_id} affected and expected-new state IDs must be disjoint")
            if effect == "none" and affected:
                raise CorpusValidationError(
                    f"pair {pair_id} no-op effect cannot list affected_item_ids")
            if effect != "none" and not affected:
                raise CorpusValidationError(
                    f"pair {pair_id} effect {effect} requires affected_item_ids")
            if effect not in {"add_scoped_item", "close_and_replace"} and expected_new:
                raise CorpusValidationError(
                    f"pair {pair_id} effect {effect} cannot declare expected_new_item_ids")
            if not expected_new <= set(state_items):
                raise CorpusValidationError(
                    f"pair {pair_id} expected new state items are absent from its checkpoint")
            if not affected <= set(state_items):
                raise CorpusValidationError(
                    f"pair {pair_id} affected state items are absent from its checkpoint")
            affected_items = [state_items[item_ref] for item_ref in affected]
            new_items = [state_items[item_ref] for item_ref in expected_new]
            pair_event_id = pair["event_id"]
            pair_event = events[pair_event_id]
            derivatives = checkpoint_gold[checkpoint_id]["invalidated_derivatives"]
            before_derivatives = {
                item["derivative_id"]: item
                for item in checkpoint_gold[before_checkpoint_id]["invalidated_derivatives"]
            }
            after_derivatives = {item["derivative_id"]: item for item in derivatives}
            changed_derivative_ids = {
                derivative_id
                for derivative_id in set(before_derivatives) | set(after_derivatives)
                if before_derivatives.get(derivative_id) != after_derivatives.get(derivative_id)
            }
            if not changed_derivative_ids <= affected_derivative_ids:
                raise CorpusValidationError(
                    f"pair {pair_id} has undeclared derivative changes: "
                    f"{sorted(changed_derivative_ids - affected_derivative_ids)}")
            if affected_derivative_ids != changed_derivative_ids:
                raise CorpusValidationError(
                    f"pair {pair_id} declared derivative changes do not match checkpoint delta")
            changed_refs = {
                item_ref for item_ref in set(before_items) | set(state_items)
                if before_items.get(item_ref) != state_items.get(item_ref)
            }
            if not changed_refs <= affected | expected_new:
                raise CorpusValidationError(
                    f"pair {pair_id} has undeclared state changes: "
                    f"{sorted(changed_refs - affected - expected_new)}")
            if not expected_new.isdisjoint(before_items):
                raise CorpusValidationError(
                    f"pair {pair_id} expected new state IDs already exist before its event")
            if not affected <= set(before_items):
                raise CorpusValidationError(
                    f"pair {pair_id} affected state items must exist before its event")
            before_affected = [before_items[item_ref] for item_ref in affected]
            if effect in expected_status:
                legal_prior_statuses = {
                    "resolve": {"active", "disputed"},
                    "expire": {"active"},
                    "invalidate": {"active", "disputed"},
                }[effect]
                if any(item["status"] not in legal_prior_statuses for item in before_affected):
                    raise CorpusValidationError(
                        f"pair {pair_id} lifecycle effect {effect} has an illegal prior state")
                if not all(item["status"] == expected_status[effect] for item in affected_items):
                    raise CorpusValidationError(
                        f"pair {pair_id} effect {effect} is not reflected in checkpoint state")
                if effect == "invalidate":
                    if any(
                        pair_event_id not in item["evidence_ids"]
                        and not any(
                            derivative["derivative_id"] == item["semantic_item_ref"]
                            and derivative["invalidated_by_event_id"] == pair_event_id
                            for derivative in derivatives
                        )
                        for item in affected_items
                    ):
                        raise CorpusValidationError(
                            f"pair {pair_id} invalidation is not tied to its lifecycle event")
                    if any(
                        derivative_id not in after_derivatives
                        or after_derivatives[derivative_id]["invalidated_by_event_id"] != pair_event_id
                        for derivative_id in affected_derivative_ids
                    ):
                        raise CorpusValidationError(
                            f"pair {pair_id} derivative invalidation is not tied to its lifecycle event")
                elif effect == "resolve" and not all(
                    pair_event_id in item["evidence_ids"] for item in affected_items
                ):
                    raise CorpusValidationError(
                        f"pair {pair_id} resolution is not supported by its pair event")
                elif effect == "expire" and not all(
                    item["valid_until"] is not None
                    and _rfc3339_utc(item["valid_until"], "state valid_until")
                    <= _rfc3339_utc(pair_event["occurred_at"], "expiry pair occurred_at")
                    for item in affected_items
                ):
                    raise CorpusValidationError(
                        f"pair {pair_id} expiry is not supported by expired state validity")
            elif effect == "reinforce":
                if not all(
                    before["status"] == "active"
                    and
                    after["status"] == "active"
                    and pair_event_id in after["evidence_ids"]
                    and pair_event_id not in before["evidence_ids"]
                    for before, after in zip(before_affected, affected_items)
                ):
                    raise CorpusValidationError(
                        f"pair {pair_id} reinforcement is not reflected in active evidence")
            elif effect == "preserve_conflict":
                if not all(
                    before["status"] in {"active", "disputed"}
                    and
                    after["status"] == "disputed"
                    and pair_event_id in after["counterevidence_ids"]
                    and pair_event_id not in before["counterevidence_ids"]
                    for before, after in zip(before_affected, affected_items)
                ):
                    raise CorpusValidationError(
                        f"pair {pair_id} conflict is not reflected in disputed state")
            elif effect == "add_scoped_item":
                if (not expected_new
                        or not all(item["status"] == "active" for item in before_affected)
                        or not all(item["status"] == "active" for item in affected_items)
                        or not all(
                    item["status"] == "active" and pair_event_id in item["evidence_ids"]
                    for item in new_items
                        )):
                    raise CorpusValidationError(
                        f"pair {pair_id} scoped addition is not reflected in active state")
            elif effect == "close_and_replace":
                if not all(item["status"] == "active" for item in before_affected):
                    raise CorpusValidationError(
                        f"pair {pair_id} close_and_replace requires active prior state")
                if (not expected_new
                        or not all(item["status"] != "active" for item in affected_items)
                        or not all(item["status"] == "active" and pair_event_id in item["evidence_ids"]
                                   for item in new_items)):
                    raise CorpusValidationError(
                        f"pair {pair_id} replacement effect is not reflected in checkpoint state")
            elif effect == "none":
                if changed_refs or expected_new or any(
                    pair_event_id in item["evidence_ids"] + item["counterevidence_ids"]
                    for item in state_items.values()
                ):
                    raise CorpusValidationError(
                        f"pair {pair_id} no-op effect is reflected as a state change")

    tasks = _unique(history["downstream_tasks"], "task_id", "downstream task")
    task_ids = set(tasks)
    task_gold = _unique(
        history["evaluator_only"]["downstream_task_gold"], "task_id", "downstream task gold")
    gold_task_ids = set(task_gold)
    if task_ids != gold_task_ids:
        raise CorpusValidationError("downstream task inputs and gold do not match")
    for task_id, task in tasks.items():
        if task["pair_id"] not in pairs:
            raise CorpusValidationError("downstream task references an unknown pair")
        if task["checkpoint_id"] not in checkpoints:
            raise CorpusValidationError("downstream task references an unknown checkpoint")
        pair_sequence = events[pairs[task["pair_id"]]["event_id"]]["sequence"]
        checkpoint_sequence = checkpoints[task["checkpoint_id"]]["after_sequence"]
        if checkpoint_sequence < pair_sequence:
            raise CorpusValidationError("downstream task checkpoint precedes its pair event")
        scope = task["target_scope"]
        if history["corpus_stage"] == "frozen_g4":
            if task["task_type"] == "action_selection" and scope["mode"] != "pair":
                raise CorpusValidationError("action_selection requires a pair target scope")
            if task["task_type"] != "action_selection" and scope["mode"] != "semantic_items":
                raise CorpusValidationError(
                    f"{task['task_type']} requires an explicit semantic-item target scope")
        if scope["mode"] == "pair" and scope["pair_id"] != task["pair_id"]:
            raise CorpusValidationError("downstream task pair scope does not match pair_id")
        if scope["mode"] == "semantic_items":
            state_refs = {item["semantic_item_ref"]
                          for item in checkpoint_gold[task["checkpoint_id"]]["current_state"]}
            if not set(scope["semantic_item_refs"]) <= state_refs:
                raise CorpusValidationError("downstream task scope references unknown state")
            derivative_scope = set(scope.get("derivative_ids", []))
            checkpoint_derivatives = {
                item["derivative_id"]
                for item in checkpoint_gold[task["checkpoint_id"]]["invalidated_derivatives"]
            }
            if task["task_type"] != "deletion_query" and derivative_scope:
                raise CorpusValidationError(
                    "only deletion_query may request invalidated derivatives"
                )
            if not derivative_scope <= checkpoint_derivatives:
                raise CorpusValidationError(
                    "downstream task scope references unknown invalidated derivatives"
                )
        dependencies = (task_gold[task_id]["relevant_dependency_ids"]
                        + task_gold[task_id]["counterevidence_ids"])
        if any(dependency not in events for dependency in dependencies):
            raise CorpusValidationError("downstream task gold references unknown evidence")
        if any(events[dependency]["sequence"] > checkpoint_sequence
               for dependency in dependencies):
            raise CorpusValidationError("downstream task gold references future evidence")
        if task["task_type"] == "action_selection":
            expected_action = pair_gold[task["pair_id"]]["expected_external_action"]
            response = task_gold[task_id]["gold_response"]
            if (not isinstance(response, dict) or set(response) != {"action"}
                    or response.get("action") != expected_action):
                raise CorpusValidationError(
                    "action-selection task gold must contain only the expected external action")
        if history["corpus_stage"] == "frozen_g4" and task["target_scope"]["mode"] == "semantic_items":
            scoped = set(task["target_scope"]["semantic_item_refs"])
            checkpoint_state = {
                item["semantic_item_ref"]: item
                for item in checkpoint_gold[task["checkpoint_id"]]["current_state"]
            }
            gold_response = task_gold[task_id]["gold_response"]
            expected_response_keys = (
                {"current_state", "invalidated_derivatives"}
                if task["task_type"] == "deletion_query"
                else {"current_state"}
            )
            if (not isinstance(gold_response, dict)
                    or set(gold_response) != expected_response_keys):
                raise CorpusValidationError(
                    f"{task['task_type']} gold must use its declared response fields")
            response_state = gold_response["current_state"]
            if not isinstance(response_state, list) or len(response_state) != len(scoped):
                raise CorpusValidationError(
                    "downstream task gold current_state must exactly match its requested semantic items")
            projected_state = [checkpoint_state[ref] for ref in sorted(scoped)]
            # Frozen downstream current-state answers use a defined five-field
            # response projection; internal-only checkpoint attributes stay local.
            response_fields = {
                "semantic_item_ref", "proposition", "scope", "evidence_ids", "status"
            }
            if any(set(item) != response_fields for item in response_state):
                raise CorpusValidationError(
                    "frozen downstream current_state gold must use the declared five-field projection")
            if {item["semantic_item_ref"] for item in response_state} != scoped:
                raise CorpusValidationError(
                    "downstream task gold current_state refs differ from requested semantic items")
            if len({item["semantic_item_ref"] for item in response_state}) != len(response_state):
                raise CorpusValidationError("downstream task gold repeats a semantic item")
            compared_fields = tuple(sorted(response_fields))
            observed_by_ref = {item["semantic_item_ref"]: item for item in response_state}
            expected_by_ref = {item["semantic_item_ref"]: item for item in projected_state}
            for ref in scoped:
                observed_item = observed_by_ref[ref]
                expected_item = expected_by_ref[ref]
                for field in compared_fields:
                    if observed_item[field] != expected_item.get(field):
                        raise CorpusValidationError(
                            f"downstream task gold current_state {field} differs from checkpoint gold")
            if task["task_type"] == "deletion_query":
                derivative_scope = set(task["target_scope"].get("derivative_ids", []))
                expected_derivatives = _project_invalidated_derivatives(
                    checkpoint_gold[task["checkpoint_id"]], derivative_scope
                )
                if gold_response["invalidated_derivatives"] != expected_derivatives:
                    raise CorpusValidationError(
                        "deletion-query invalidated_derivatives differ from checkpoint gold")
            if not scoped <= set(checkpoint_state):
                raise CorpusValidationError("downstream task gold targets state absent at checkpoint")

    pair_features = {
        tag for gold in pair_gold.values() for tag in gold.get("feature_tags", [])
    }
    if history["corpus_stage"] == "frozen_g4" and pair_features != set(history["feature_tags"]):
        raise CorpusValidationError(
            "frozen history feature_tags must exactly equal the union of pair-gold feature tags")

    all_evidence = set(events)
    for pair_id, gold in pair_gold.items():
        if not set(gold["required_evidence_ids"] + gold["forbidden_evidence_ids"]) <= all_evidence:
            raise CorpusValidationError("pair gold references unknown evidence")
        pair_sequence = events[pairs[pair_id]["event_id"]]["sequence"]
        if any(events[evidence_id]["sequence"] > pair_sequence
               for evidence_id in gold["required_evidence_ids"]):
            raise CorpusValidationError("pair gold requires future evidence")

    provenance = history["evaluator_only"]["generation_and_review_provenance"]
    stored_review_hash = provenance["reviewed_content_sha256"]
    if history["reviewer_status"] in {"reviewed", "adjudicated"}:
        if stored_review_hash != review_content_sha256(history):
            raise CorpusValidationError("review approval hash does not match content")
    elif stored_review_hash is not None:
        raise CorpusValidationError("pending history cannot carry a review approval hash")


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
