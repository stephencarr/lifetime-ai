"""Rehearse the G4 transition policy on development pairs without writes.

Decisions use only system-visible projections and out-of-fold prediction
artifacts. Gold is read only after every decision has been constructed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import read_jsonl, sha256_bytes, sha256_value, strict_json_loads
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics, wilson_interval
from lifetime_ai.evaluation.g4_transition import (
    G4PreparedTransition, G4TransitionProposal, preflight_g4_transition,
    prepare_g4_transition, witness_g4_transition,
)
from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection, build_system_history_projection,
)
from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_local_development import _assert_development_authorized
from scripts.score_g4_development import _prediction
from scripts.score_g4_preflight_development import _proposal_from_prediction


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "evaluation/config/g4-evaluation-v0.1.json"
REHEARSAL_POLICY_PATH = ROOT / "evaluation/config/g4-development-rehearsal-policy.json"
IMPLEMENTATION_PATHS = (
    ROOT / "scripts/run_g4_transition_rehearsal_development.py",
    ROOT / "scripts/score_g4_preflight_development.py",
    ROOT / "lifetime_ai/evaluation/g4_transition.py",
)
EVALUATOR_PREDICTION_FIELDS = {
    "gold_relationship", "gold_effect", "gold_disposition", "acceptable_alternatives",
    "severity_if_wrong", "relationship_correct", "effect_correct", "disposition_correct",
}
VISIBLE_HISTORY_FIELDS = (
    "schema_version", "history_id", "timeline", "checkpoint_requests",
    "downstream_tasks", "candidate_snapshots", "pair_inputs",
)


def _rows_by_pair(path: Path) -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(row, dict) and isinstance(row.get("pair_id"), str) for row in rows):
        raise CorpusValidationError("prediction rows must be objects with pair IDs")
    by_pair = {row["pair_id"]: row for row in rows}
    if len(rows) != 1080 or len(by_pair) != len(rows):
        raise CorpusValidationError("prediction artifact must cover development pairs exactly once")
    return by_pair


def _visible_prediction_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in EVALUATOR_PREDICTION_FIELDS}


def _preparation_invariants(
    proposal: G4TransitionProposal,
    prepared: G4PreparedTransition,
    pair_projection: dict[str, Any],
    sequence: int,
) -> bool:
    """Check expected read-only state shape, not semantic correctness."""
    if not prepared.prepared or prepared.write_authorized:
        return False
    before = pair_projection["candidate_snapshot"]
    expected_sources = list(dict.fromkeys((*before["source_event_ids"], proposal.event_id)))
    if proposal.effect == "reinforce":
        after = prepared.candidate_after
        return bool(
            after is not None and not prepared.new_items
            and after["item_id"] == before["item_id"]
            and after["canonical_payload"] == before["canonical_payload"]
            and after["sha256"] == before["sha256"]
            and after["source_event_ids"] == expected_sources
            and after["counterevidence_event_ids"] == before["counterevidence_event_ids"]
            and after["captured_after_sequence"] == sequence
            and after["snapshot_id"] != before["snapshot_id"]
        )
    if proposal.effect == "add_scoped_item":
        if prepared.candidate_after is not None or len(prepared.new_items) != 1:
            return False
        item = prepared.new_items[0]
        return bool(
            item["item_id"] == proposal.new_item_ids[0]
            and item["item_id"] != before["item_id"]
            and item["canonical_payload"] == proposal.new_item_payload
            and item["sha256"] == sha256_value(item["canonical_payload"])
            and item["source_event_ids"] == expected_sources
            and item["counterevidence_event_ids"] == before["counterevidence_event_ids"]
            and item["captured_after_sequence"] == sequence
            and item["snapshot_id"] != before["snapshot_id"]
        )
    if proposal.effect == "close_and_replace":
        if prepared.candidate_after is None or len(prepared.new_items) != 1:
            return False
        closed, replacement = prepared.candidate_after, prepared.new_items[0]
        effective = proposal.new_item_payload["valid_from"]
        expected_closed_payload = deepcopy(before["canonical_payload"])
        expected_closed_payload["status"] = "expired"
        expected_closed_payload["valid_until"] = effective
        return bool(
            closed["item_id"] == before["item_id"]
            and closed["canonical_payload"] == expected_closed_payload
            and closed["sha256"] == sha256_value(expected_closed_payload)
            and closed["source_event_ids"] == expected_sources
            and closed["counterevidence_event_ids"] == before["counterevidence_event_ids"]
            and closed["captured_after_sequence"] == sequence
            and closed["snapshot_id"] != before["snapshot_id"]
            and replacement["item_id"] == proposal.new_item_ids[0]
            and replacement["item_id"] != before["item_id"]
            and replacement["canonical_payload"] == proposal.new_item_payload
            and replacement["sha256"] == sha256_value(replacement["canonical_payload"])
            and replacement["source_event_ids"] == expected_sources
            and replacement["counterevidence_event_ids"] == before["counterevidence_event_ids"]
            and replacement["captured_after_sequence"] == sequence
            and replacement["snapshot_id"] not in {before["snapshot_id"], closed["snapshot_id"]}
        )
    return False


def _decide_pair(
    history: dict[str, Any], pair: dict[str, Any],
    relationship_row: dict[str, Any], effect_row: dict[str, Any], threshold: Decimal,
) -> dict[str, Any]:
    """Return a read-only decision; this function has no evaluator-only input."""
    pair_id = pair["pair_id"]
    if (relationship_row.get("history_id") != history["history_id"]
            or effect_row.get("history_id") != history["history_id"]
            or relationship_row.get("candidate_snapshot_id") != pair["candidate_snapshot_id"]
            or effect_row.get("relationship_decision") != relationship_row.get("decision")
            or relationship_row.get("model_fold") != effect_row.get("model_fold")
            or relationship_row.get("family_id") != effect_row.get("family_id")):
        raise CorpusValidationError("relationship/effect artifact identity or fold mismatch")
    if (effect_row.get("effect_decision") not in {
            "reinforce", "preserve_conflict", "add_scoped_item", "close_and_replace",
            "resolve", "invalidate", "expire", "none",
    } or effect_row.get("disposition_decision") not in {
            "accept", "reject_unauthorized", "reject_invalid", "abstain", "no_op",
    }):
        raise CorpusValidationError("effect artifact decision vocabulary mismatch")
    prediction, eligible = _prediction(relationship_row)
    if not eligible:
        raise CorpusValidationError("rehearsal artifact marks a development pair ineligible")
    pair_projection = build_pair_classification_projection(history, pair_id)
    if pair_projection["candidate_snapshot"].get("snapshot_id") != prediction.candidate_snapshot_id:
        raise CorpusValidationError("candidate projection mismatch")
    selected = Decimal(prediction.confidence)
    above = [name for name, value in prediction.probabilities.items()
             if Decimal(value) >= threshold]
    gated = prediction.decision != "uncertain" and selected >= threshold and above == [prediction.decision]
    if effect_row.get("relationship_probability_gated") is not gated:
        raise CorpusValidationError("effect artifact probability gate mismatch")
    decision = {
        "history_id": history["history_id"], "pair_id": pair_id,
        "candidate_snapshot_id": pair["candidate_snapshot_id"],
        "relationship_decision": prediction.decision,
        "effect_decision": effect_row.get("effect_decision"),
        "disposition_decision": effect_row.get("disposition_decision"),
        "relationship_confidence": prediction.confidence,
        "eligible": True, "rehearsed_accept": False,
        "stage": "probability_gate", "reason": "relationship below or outside single-class gate",
        "prepared_snapshot_ids": [], "prepared_payload_sha256": [],
        "write_authorized": False, "mutation_committed": False,
    }
    if not gated:
        return decision
    if effect_row.get("effect_decision") == "none":
        decision.update(stage="no_op_exclusion", reason="no-op cannot establish unrelatedness")
        return decision
    if effect_row.get("disposition_decision") != "accept":
        decision.update(stage="disposition_shape", reason="predicted disposition is not accept")
        return decision
    if effect_row["effect_decision"] not in {"reinforce", "add_scoped_item", "close_and_replace"}:
        decision.update(stage="unsupported_effect", reason="effect not in rehearsal policy")
        return decision
    event = next(item for item in history["timeline"] if item["event_id"] == pair["event_id"])
    history_projection = build_system_history_projection(history, sequence=event["sequence"])
    proposal = _proposal_from_prediction(pair, effect_row, pair_projection)
    preflight = preflight_g4_transition(proposal, pair_projection, history_projection)
    if not preflight.passed:
        decision.update(stage="preflight", reason=preflight.reason)
        return decision
    witness = witness_g4_transition(proposal, pair_projection, history_projection)
    if not witness.passed:
        decision.update(stage="source_witness", reason=witness.reason)
        return decision
    pair_before, history_before = deepcopy(pair_projection), deepcopy(history_projection)
    prepared = prepare_g4_transition(proposal, pair_projection, history_projection)
    if pair_projection != pair_before or history_projection != history_before:
        raise CorpusValidationError("read-only transition preparation mutated input projection")
    if not _preparation_invariants(proposal, prepared, pair_projection, event["sequence"]):
        decision.update(stage="prepared_state", reason="prepared state failed invariants")
        return decision
    snapshots = ([prepared.candidate_after] if prepared.candidate_after else []) + list(prepared.new_items)
    decision.update(
        rehearsed_accept=True, stage="rehearsed_accept", reason="prepared without write authority",
        prepared_snapshot_ids=[item["snapshot_id"] for item in snapshots],
        prepared_payload_sha256=[item["sha256"] for item in snapshots],
    )
    return decision


def rehearse_development(
    corpus: Path, relationships: Path, effects: Path, output: Path, audit: Path,
) -> dict[str, Any]:
    _assert_development_authorized()
    corpus_root = corpus.resolve()
    if any(path.resolve().is_relative_to(corpus_root)
           for path in (relationships, effects, output, audit)):
        raise CorpusValidationError("prediction or output path must not enter sealed corpus")
    manifest = verify_g4_development_partition(corpus)
    policy = strict_json_loads(POLICY_PATH.read_text(encoding="utf-8"))
    rehearsal_policy = strict_json_loads(REHEARSAL_POLICY_PATH.read_text(encoding="utf-8"))
    if policy["authorization"]["holdout_evaluation_authorized"] is not False:
        raise CorpusValidationError("rehearsal requires holdout authorization to remain false")
    if (rehearsal_policy.get("status") != "DEVELOPMENT_CANDIDATE_NOT_FROZEN_FOR_HOLDOUT"
            or rehearsal_policy.get("partition") != "development_only"
            or set(rehearsal_policy.get("permitted_effects", [])) != {
                "reinforce", "add_scoped_item", "close_and_replace"
            }
            or rehearsal_policy.get("predicted_disposition_required") != "accept"
            or rehearsal_policy.get("no_op_autonomy_eligible") is not False
            or rehearsal_policy.get("single_class_probability_gate") is not True
            or rehearsal_policy.get("structural_preflight_required") is not True
            or rehearsal_policy.get("positive_source_witness_required") is not True
            or rehearsal_policy.get("prepared_state_invariants_required") is not True
            or rehearsal_policy.get("write_authorized") is not False
            or rehearsal_policy.get("mutation_committed") is not False
            or rehearsal_policy.get("model_disposition_is_permission") is not False):
        raise CorpusValidationError("rehearsal policy is incompatible with fail-closed runner")
    threshold = Decimal(policy["decision_policy"]["autonomous_acceptance_threshold"])
    relationship_rows = _rows_by_pair(relationships)
    effect_rows = _rows_by_pair(effects)
    histories = read_jsonl(corpus / "development.jsonl")
    decisions: list[dict[str, Any]] = []
    for full_history in histories:
        if full_history.get("partition") != "development":
            raise CorpusValidationError("non-development history in development payload")
        visible = {key: full_history[key] for key in VISIBLE_HISTORY_FIELDS}
        for pair in visible["pair_inputs"]:
            pair_id = pair["pair_id"]
            if pair_id not in relationship_rows or pair_id not in effect_rows:
                raise CorpusValidationError("prediction artifact missing development pair")
            decisions.append(_decide_pair(
                visible, pair,
                _visible_prediction_row(relationship_rows[pair_id]),
                _visible_prediction_row(effect_rows[pair_id]),
                threshold,
            ))
    pair_ids = {item["pair_id"] for item in decisions}
    if (len(decisions) != 1080 or len(pair_ids) != len(decisions)
            or pair_ids != set(relationship_rows) or pair_ids != set(effect_rows)):
        raise CorpusValidationError("prediction artifact contains missing or non-development pairs")

    # Evaluation-only stage. No gold labels enter the proposal, gate, witness,
    # preparation, or invariant checks above.
    gold_by_pair = {
        gold["pair_id"]: gold
        for history in histories for gold in history["evaluator_only"]["pair_gold"]
    }
    histories_by_id = {history["history_id"]: history for history in histories}
    evaluations: list[PairEvaluation] = []
    joint_correct = 0
    error_severity: Counter[str] = Counter()
    accepted_effects: Counter[str] = Counter()
    accepted_relationships: Counter[str] = Counter()
    replacement_reference_available = replacement_reference_exact = 0
    for decision in decisions:
        pair_id = decision["pair_id"]
        gold = gold_by_pair[pair_id]
        effect_row = effect_rows[pair_id]
        relation_row = relationship_rows[pair_id]
        if (effect_row.get("gold_relationship") != gold["semantic_relationship"]
                or effect_row.get("gold_effect") != gold["expected_state_effect"]["effect"]
                or effect_row.get("gold_disposition") != gold["transition_disposition"]
                or relation_row.get("gold_relationship") != gold["semantic_relationship"]
                or relation_row.get("acceptable_alternatives") != gold["acceptable_alternatives"]):
            raise CorpusValidationError("prediction artifact gold binding mismatch")
        relation, _ = _prediction(relationship_rows[pair_id])
        evaluations.append(PairEvaluation(
            replace(relation, escalate=not decision["rehearsed_accept"]),
            gold["semantic_relationship"], True,
            tuple(gold["acceptable_alternatives"]),
        ))
        relation_correct = decision["relationship_decision"] in {
            gold["semantic_relationship"], *gold["acceptable_alternatives"]
        }
        effect_correct = decision["effect_decision"] == gold["expected_state_effect"]["effect"]
        disposition_correct = gold["transition_disposition"] == "accept"
        decision.update(
            gold_relationship=gold["semantic_relationship"],
            gold_effect=gold["expected_state_effect"]["effect"],
            gold_disposition=gold["transition_disposition"],
            relationship_correct=relation_correct,
            effect_correct=effect_correct,
        )
        if decision["rehearsed_accept"]:
            accepted_effects[decision["effect_decision"]] += 1
            accepted_relationships[decision["relationship_decision"]] += 1
            joint_correct += relation_correct and effect_correct and disposition_correct
            if not (relation_correct and effect_correct and disposition_correct):
                error_severity[gold["severity_if_wrong"]] += 1
            if decision["effect_decision"] == "close_and_replace" and effect_correct:
                history = histories_by_id[decision["history_id"]]
                pair = next(item for item in history["pair_inputs"] if item["pair_id"] == pair_id)
                event = next(item for item in history["timeline"] if item["event_id"] == pair["event_id"])
                expected = gold["expected_state_effect"]
                identities = (*expected["affected_item_ids"], *expected["expected_new_item_ids"])
                if len(identities) == 2:
                    references = [
                        next((snapshot for snapshot in history["candidate_snapshots"]
                              if snapshot["item_id"] == identity
                              and snapshot["captured_after_sequence"] == event["sequence"]), None)
                        for identity in identities
                    ]
                    if all(reference is not None for reference in references):
                        replacement_reference_available += 1
                        replacement_reference_exact += (
                            [reference["sha256"] for reference in references]
                            == decision["prepared_payload_sha256"]
                        )
    metrics = summarize_g4_metrics(evaluations)
    if metrics.eligible_count != len(decisions) or metrics.autonomous_count != sum(
        decision["rehearsed_accept"] for decision in decisions
    ):
        raise CorpusValidationError("rehearsal metric accounting mismatch")
    interval = metrics.autonomous_precision_wilson_95
    joint_interval = wilson_interval(joint_correct, metrics.autonomous_count)
    result = {
        "status": "DEVELOPMENT_READ_ONLY_REHEARSAL",
        "partition": "development_only",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "policy_sha256": sha256_bytes(POLICY_PATH.read_bytes()),
        "rehearsal_policy_status": rehearsal_policy["status"],
        "rehearsal_policy_sha256": sha256_bytes(REHEARSAL_POLICY_PATH.read_bytes()),
        "implementation_sha256": {
            str(path.relative_to(ROOT)): sha256_bytes(path.read_bytes())
            for path in IMPLEMENTATION_PATHS
        },
        "relationship_predictions_sha256": sha256_bytes(relationships.read_bytes()),
        "effect_predictions_sha256": sha256_bytes(effects.read_bytes()),
        "relationship_threshold": str(threshold),
        "eligible_decision_count": metrics.eligible_count,
        "eligible_definition_applied": policy["decision_policy"]["eligible_decision_definition"],
        "rehearsed_accept_count": metrics.autonomous_count,
        "rehearsed_accept_coverage": metrics.autonomous_coverage,
        "joint_correct_rehearsed_accept_count": joint_correct,
        "joint_rehearsed_accept_precision": (
            joint_correct / metrics.autonomous_count if metrics.autonomous_count else None
        ),
        "joint_rehearsed_accept_precision_wilson_95": (
            {"lower": joint_interval.lower, "upper": joint_interval.upper}
            if joint_interval else None
        ),
        "relationship_precision_among_rehearsed": metrics.autonomous_precision,
        "relationship_precision_wilson_95": (
            {"lower": interval.lower, "upper": interval.upper} if interval else None
        ),
        "relationship_expected_calibration_error_all_eligible": metrics.expected_calibration_error,
        "relationship_multiclass_brier_score_all_eligible": metrics.multiclass_brier_score,
        "accepted_relationships": dict(accepted_relationships),
        "accepted_effects": dict(accepted_effects),
        "replacement_reference_pairs_available": replacement_reference_available,
        "replacement_reference_pairs_exact": replacement_reference_exact,
        "rehearsed_error_severity": dict(error_severity),
        "stage_counts": dict(Counter(decision["stage"] for decision in decisions)),
        "reason_counts": dict(Counter(decision["reason"] for decision in decisions)),
        "all_preparations_without_write_authority": all(
            not decision["write_authorized"] and not decision["mutation_committed"]
            for decision in decisions
        ),
        "model_disposition_is_permission": False,
        "real_model_inference_timed": False,
        "baseline_comparison_run": False,
        "counts_as_autonomous": False,
        "holdout_accessed": False,
        "audit_artifact": str(audit),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    audit.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit.write_text(
        "".join(json.dumps(decision, sort_keys=True) + "\n" for decision in decisions),
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--relationships", type=Path, required=True)
    parser.add_argument("--effects", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    result = rehearse_development(
        args.corpus, args.relationships, args.effects, args.output, args.audit,
    )
    print(json.dumps({key: result[key] for key in (
        "status", "eligible_decision_count", "rehearsed_accept_count",
        "joint_correct_rehearsed_accept_count", "rehearsed_accept_coverage",
    )}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
