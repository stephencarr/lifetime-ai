"""Inspect explicit G4 development proposals with read-only preflight.

Passing this preliminary check is not autonomous acceptance or write approval.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import read_jsonl, sha256_bytes, sha256_value
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_transition import (
    G4TransitionProposal, preflight_g4_transition, witness_g4_transition,
)
from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection, build_system_history_projection,
)
from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_local_development import _assert_development_authorized


def _rows(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(row, dict) for row in rows):
        raise CorpusValidationError("effect prediction rows must be objects")
    return rows


_CHILD_WORKFLOW = re.compile(r"\bchild workflow '([^'\n]+)'", re.IGNORECASE)
_REPLACEMENT = re.compile(
    r"\bauthorizes (.+?) (primary-recovery|primary|secondary|fallback) configuration "
    r"to replace setting ([0-9]+) with setting ([0-9]+) effective (\S+)\."
)


def _scoped_payload_from_visible_pair(pair_projection: dict[str, Any]) -> dict[str, Any] | None:
    """Extract one narrow development proposal from visible text, never gold.

    This fixture-oriented lexical extractor is not semantic validation and is
    deliberately unable to infer other scope forms.
    """
    event = pair_projection["event"]
    snapshot = pair_projection["candidate_snapshot"]
    content = event.get("content")
    prior_payload = snapshot.get("canonical_payload")
    if not isinstance(content, str) or not isinstance(prior_payload, dict):
        return None
    matches = _CHILD_WORKFLOW.findall(content)
    if len(matches) != 1 or not matches[0].strip():
        return None
    prior_scope = prior_payload.get("scope")
    if not isinstance(prior_scope, dict) or "condition" in prior_scope:
        return None
    payload = deepcopy(prior_payload)
    payload["scope"] = {**prior_scope, "condition": matches[0]}
    payload["proposition"] = content
    payload["valid_from"] = event.get("occurred_at")
    return payload


def _replacement_payload_from_visible_pair(pair_projection: dict[str, Any]) -> dict[str, Any] | None:
    """Build one conservative replacement candidate from visible event text."""
    event = pair_projection["event"]
    prior = pair_projection["candidate_snapshot"].get("canonical_payload")
    content = event.get("content")
    if not isinstance(content, str) or not isinstance(prior, dict):
        return None
    matches = list(_REPLACEMENT.finditer(content))
    if len(matches) != 1:
        return None
    product, workflow, old_setting, new_setting, effective = matches[0].groups()
    if (prior.get("scope") != {"product": product, "workflow": workflow}
            or effective != event.get("occurred_at")
            or old_setting == new_setting):
        return None
    payload = deepcopy(prior)
    payload["proposition"] = f"{product} {workflow} configuration use setting {new_setting}."
    payload["status"] = "active"
    payload["epistemic_basis"] = "asserted"
    payload["valid_from"] = effective
    return payload


def _proposal_from_prediction(
    pair: dict[str, Any], row: dict[str, Any], pair_projection: dict[str, Any],
) -> G4TransitionProposal:
    """Construct a proposal from prediction and visible pair fields only."""
    event = pair_projection["event"]
    source_ids = pair_projection["candidate_snapshot"].get("source_event_ids", [])
    effect = row["effect_decision"]
    scoped_payload = None
    new_item_ids: tuple[str, ...] = ()
    if row["relationship_decision"] == "narrows_scope" and effect == "add_scoped_item":
        scoped_payload = _scoped_payload_from_visible_pair(pair_projection)
        if scoped_payload is not None:
            new_item_ids = ("g4-scoped:" + sha256_value({
                "pair_id": pair["pair_id"],
                "candidate_snapshot_id": pair["candidate_snapshot_id"],
                "event_id": event["event_id"],
            })[:32],)
    if row["relationship_decision"] == "supersedes" and effect == "close_and_replace":
        scoped_payload = _replacement_payload_from_visible_pair(pair_projection)
        if scoped_payload is not None:
            new_item_ids = ("g4-replacement:" + sha256_value({
                "pair_id": pair["pair_id"],
                "candidate_snapshot_id": pair["candidate_snapshot_id"],
                "event_id": event["event_id"],
            })[:32],)
    return G4TransitionProposal(
        event_id=event["event_id"],
        candidate_snapshot_id=pair["candidate_snapshot_id"],
        relationship=row["relationship_decision"],
        effect=effect,
        affected_item_ids=(pair["candidate_item_id"],) if effect != "none" else (),
        new_item_ids=new_item_ids,
        evidence_event_ids=tuple(dict.fromkeys((*source_ids, event["event_id"]))),
        new_item_payload=scoped_payload,
    )


def score_preflight(corpus: Path, effect_predictions: Path, output: Path) -> dict[str, Any]:
    _assert_development_authorized()
    manifest = verify_g4_development_partition(corpus)
    rows = _rows(effect_predictions)
    predictions = {row["pair_id"]: row for row in rows}
    if len(rows) != 1080 or len(predictions) != len(rows):
        raise CorpusValidationError("effect artifact must cover development pairs exactly once")
    seen: set[str] = set()
    gated = passed = joint_correct = scoped_payload_proposed = 0
    scoped_reference_available = scoped_payload_exact_matches = 0
    scoped_reference_mismatch_fields: Counter[str] = Counter()
    state_changing_passed = state_changing_joint_correct = 0
    state_changing_gold_dispositions: Counter[str] = Counter()
    state_changing_wrong_by_pair_severity: Counter[str] = Counter()
    witness_passed = witness_joint_correct = 0
    witness_reasons: Counter[str] = Counter()
    witness_gold_dispositions: Counter[str] = Counter()
    reasons: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    wrong_by_pair_severity: Counter[str] = Counter()
    wrong_by_gold_disposition: Counter[str] = Counter()
    shape_consistent = shape_consistent_joint_correct = 0
    shape_consistent_gold_dispositions: Counter[str] = Counter()
    for history in read_jsonl(corpus / "development.jsonl"):
        if history.get("partition") != "development":
            raise CorpusValidationError("non-development history in development payload")
        events = {event["event_id"]: event for event in history["timeline"]}
        golds = {gold["pair_id"]: gold for gold in history["evaluator_only"]["pair_gold"]}
        for pair in history["pair_inputs"]:
            pair_id = pair["pair_id"]
            row = predictions.get(pair_id)
            if row is None or row.get("history_id") != history["history_id"]:
                raise CorpusValidationError("effect artifact references wrong development pair")
            if (row.get("gold_relationship") != golds[pair_id]["semantic_relationship"]
                    or row.get("gold_effect") != golds[pair_id]["expected_state_effect"]["effect"]
                    or row.get("gold_disposition") != golds[pair_id]["transition_disposition"]):
                raise CorpusValidationError("effect artifact gold binding mismatch")
            seen.add(pair_id)
            if not row.get("relationship_probability_gated"):
                continue
            gated += 1
            event = events[pair["event_id"]]
            effect = row["effect_decision"]
            pair_projection = build_pair_classification_projection(history, pair_id)
            history_projection = build_system_history_projection(
                history, sequence=event["sequence"]
            )
            proposal = _proposal_from_prediction(pair, row, pair_projection)
            scoped_payload = proposal.new_item_payload if effect == "add_scoped_item" else None
            if scoped_payload is not None:
                scoped_payload_proposed += 1
            result = preflight_g4_transition(
                proposal, pair_projection, history_projection,
            )
            reasons[result.reason] += 1
            if result.passed:
                passed += 1
                dispositions[golds[pair_id]["transition_disposition"]] += 1
                if scoped_payload is not None:
                    expected = golds[pair_id]["expected_state_effect"]
                    expected_ids = expected.get("expected_new_item_ids", [])
                    if expected.get("effect") == "add_scoped_item" and len(expected_ids) == 1:
                        reference = next((snapshot for snapshot in history["candidate_snapshots"]
                                          if snapshot["item_id"] == expected_ids[0]
                                          and snapshot["captured_after_sequence"] == event["sequence"]), None)
                        if reference is not None:
                            scoped_reference_available += 1
                            reference_payload = reference["canonical_payload"]
                            if scoped_payload == reference_payload:
                                scoped_payload_exact_matches += 1
                            else:
                                for field in set(scoped_payload) | set(reference_payload):
                                    if scoped_payload.get(field) != reference_payload.get(field):
                                        scoped_reference_mismatch_fields[field] += 1
                correct = bool(row["relationship_correct"] and row["effect_correct"])
                joint_correct += correct
                if effect != "none":
                    state_changing_passed += 1
                    state_changing_joint_correct += correct
                    state_changing_gold_dispositions[golds[pair_id]["transition_disposition"]] += 1
                    if not correct:
                        state_changing_wrong_by_pair_severity[golds[pair_id]["severity_if_wrong"]] += 1
                    witness = witness_g4_transition(proposal, pair_projection, history_projection)
                    witness_reasons[witness.reason] += 1
                    if witness.passed:
                        witness_passed += 1
                        witness_joint_correct += correct
                        witness_gold_dispositions[golds[pair_id]["transition_disposition"]] += 1
                if not correct:
                    wrong_by_pair_severity[golds[pair_id]["severity_if_wrong"]] += 1
                    wrong_by_gold_disposition[golds[pair_id]["transition_disposition"]] += 1
                proposed_disposition = row.get("disposition_decision")
                expected_shape = "no_op" if effect == "none" else "accept"
                if proposed_disposition == expected_shape:
                    shape_consistent += 1
                    shape_consistent_joint_correct += correct
                    shape_consistent_gold_dispositions[golds[pair_id]["transition_disposition"]] += 1
    if seen != set(predictions):
        raise CorpusValidationError("effect artifact contains a non-development pair")
    result = {
        "status": "DEVELOPMENT_PREFLIGHT_DIAGNOSTIC_ONLY",
        "partition": "development_only",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "effect_predictions_sha256": sha256_bytes(effect_predictions.read_bytes()),
        "probability_gated_pairs": gated,
        "scoped_payloads_proposed_from_visible_text": scoped_payload_proposed,
        "scoped_reference_payloads_available_for_diagnostic": scoped_reference_available,
        "scoped_payload_exact_reference_matches": scoped_payload_exact_matches,
        "scoped_reference_mismatch_fields": dict(scoped_reference_mismatch_fields),
        "preflight_passed_pairs": passed,
        "joint_relationship_and_effect_correct_among_preflight": joint_correct,
        "state_changing_preflight_passed_pairs": state_changing_passed,
        "joint_correct_among_state_changing_preflight": state_changing_joint_correct,
        "gold_dispositions_among_state_changing_preflight": dict(state_changing_gold_dispositions),
        "wrong_state_changing_pair_predictions_by_pair_severity": dict(
            state_changing_wrong_by_pair_severity
        ),
        "source_witness_passed_pairs": witness_passed,
        "joint_correct_among_source_witness_pairs": witness_joint_correct,
        "source_witness_reasons": dict(witness_reasons),
        "gold_dispositions_among_source_witness": dict(witness_gold_dispositions),
        "preflight_reasons": dict(reasons),
        "gold_dispositions_among_preflight": dict(dispositions),
        "wrong_preflight_pair_predictions_by_pair_severity": dict(wrong_by_pair_severity),
        "wrong_preflight_pair_predictions_by_gold_disposition": dict(wrong_by_gold_disposition),
        "model_disposition_shape_consistent_preflight_pairs": shape_consistent,
        "joint_correct_among_shape_consistent_preflight_pairs": shape_consistent_joint_correct,
        "gold_dispositions_among_shape_consistent_preflight": dict(shape_consistent_gold_dispositions),
        "model_disposition_is_permission": False,
        "no_op_preflight_is_autonomy_eligible": False,
        "semantic_effect_validation_applied": False,
        "mutation_committed": False,
        "counts_as_autonomous": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--effect-predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = score_preflight(args.corpus, args.effect_predictions, args.output)
    print(json.dumps({key: result[key] for key in (
        "status", "probability_gated_pairs", "preflight_passed_pairs",
        "joint_relationship_and_effect_correct_among_preflight",
    )}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
