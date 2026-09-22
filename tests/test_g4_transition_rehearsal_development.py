import json
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

import pytest

from lifetime_ai.evaluation.canonical import read_jsonl
from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_transition_rehearsal_development import (
    EVALUATOR_PREDICTION_FIELDS, VISIBLE_HISTORY_FIELDS,
    _decide_pair, _rows_by_pair, _visible_prediction_row, rehearse_development,
)


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "evaluation/corpus/frozen-g4-v0.1-sealed-v21"
EXPERIMENT = ROOT / "experiments/g4/20260922-1351-local-encoder-development"
RELATIONSHIPS = (
    EXPERIMENT / "grouped-calibrated-predictions/structured_minilm_pair_logistic-out-of-fold.jsonl"
)
EFFECTS = EXPERIMENT / "effect-development-predictions.jsonl"


def test_rehearsal_is_complete_read_only_and_scored_after_decision(tmp_path):
    output, audit = tmp_path / "result.json", tmp_path / "audit.jsonl"
    result = rehearse_development(CORPUS, RELATIONSHIPS, EFFECTS, output, audit)
    decisions = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    accepted = [decision for decision in decisions if decision["rehearsed_accept"]]
    assert len(decisions) == result["eligible_decision_count"] == 1080
    assert len(accepted) == result["rehearsed_accept_count"] == 363
    assert result["joint_correct_rehearsed_accept_count"] == 363
    assert result["rehearsed_accept_coverage"] == pytest.approx(363 / 1080)
    assert result["relationship_expected_calibration_error_all_eligible"] < 0.10
    assert result["joint_rehearsed_accept_precision_wilson_95"]["lower"] > 0.98
    assert result["accepted_effects"] == {
        "reinforce": 84, "add_scoped_item": 202, "close_and_replace": 77,
    }
    assert result["replacement_reference_pairs_available"] == 45
    assert result["replacement_reference_pairs_exact"] == 45
    assert result["rehearsal_policy_status"] == "DEVELOPMENT_CANDIDATE_NOT_FROZEN_FOR_HOLDOUT"
    assert result["all_preparations_without_write_authority"]
    assert not result["counts_as_autonomous"] and not result["holdout_accessed"]
    assert all(not row["write_authorized"] and not row["mutation_committed"] for row in decisions)
    assert all(row["relationship_correct"] and row["effect_correct"] for row in accepted)
    assert all(row["gold_disposition"] == "accept" for row in accepted)
    assert all(len(row["prepared_snapshot_ids"]) == (
        2 if row["effect_decision"] == "close_and_replace" else 1
    ) for row in accepted)


def test_rehearsal_rejects_cross_artifact_probability_gate_tampering():
    history = read_jsonl(CORPUS / "development.jsonl")[0]
    visible = {key: history[key] for key in VISIBLE_HISTORY_FIELDS}
    pair = visible["pair_inputs"][0]
    relationships = _rows_by_pair(RELATIONSHIPS)
    effects = _rows_by_pair(EFFECTS)
    effect = deepcopy(effects[pair["pair_id"]])
    assert not EVALUATOR_PREDICTION_FIELDS & set(_visible_prediction_row(effect))
    effect["relationship_probability_gated"] = not effect["relationship_probability_gated"]
    with pytest.raises(CorpusValidationError, match="probability gate mismatch"):
        _decide_pair(visible, pair, relationships[pair["pair_id"]], effect, Decimal("0.95"))


def test_rehearsal_rejects_artifact_gold_binding_tampering(tmp_path):
    rows = EFFECTS.read_text(encoding="utf-8").splitlines()
    first = json.loads(rows[0])
    first["gold_disposition"] = "tampered"
    rows[0] = json.dumps(first)
    tampered = tmp_path / "tampered-effect.jsonl"
    tampered.write_text("\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="gold binding mismatch"):
        rehearse_development(CORPUS, RELATIONSHIPS, tampered,
                             tmp_path / "result.json", tmp_path / "audit.jsonl")
    assert not (tmp_path / "result.json").exists()
    assert not (tmp_path / "audit.jsonl").exists()
