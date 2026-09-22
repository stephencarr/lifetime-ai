from pathlib import Path

import pytest

from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.score_g4_preflight_development import (
    _replacement_payload_from_visible_pair,
    _scoped_payload_from_visible_pair,
    score_preflight,
)


CORPUS = Path(__file__).resolve().parents[1] / "evaluation/corpus/frozen-g4-v0.1-sealed-v21"
EFFECT_PREDICTIONS = (
    Path(__file__).resolve().parents[1]
    / "experiments/g4/20260922-1351-local-encoder-development/effect-development-predictions.jsonl"
)


def test_preflight_scorer_rejects_incomplete_development_artifact(tmp_path):
    predictions = tmp_path / "effect.jsonl"
    predictions.write_text('{"pair_id":"fabricated"}\n', encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="cover development pairs"):
        score_preflight(CORPUS, predictions, tmp_path / "result.json")


def test_scoped_payload_extractor_uses_visible_text_and_preserves_parent():
    prior = {
        "kind": "fact", "proposition": "A general setting applies",
        "scope": {"product": "Widget"}, "status": "active",
        "epistemic_basis": "asserted", "sensitivity": "normal",
        "valid_from": "2026-09-20T08:00:00Z", "valid_until": None,
    }
    pair = {
        "event": {
            "content": "The child workflow 'mobile requests' for Widget uses a different setting until that condition ends.",
            "occurred_at": "2026-09-22T08:00:00Z",
        },
        "candidate_snapshot": {"canonical_payload": prior},
    }
    proposed = _scoped_payload_from_visible_pair(pair)
    assert proposed is not None
    assert proposed["scope"] == {"product": "Widget", "condition": "mobile requests"}
    assert proposed["proposition"] == pair["event"]["content"]
    assert proposed["valid_from"] == pair["event"]["occurred_at"]
    assert prior["scope"] == {"product": "Widget"}
    assert prior["proposition"] == "A general setting applies"


def test_scoped_payload_extractor_abstains_on_ambiguous_or_missing_phrase():
    pair = {
        "event": {"content": "No narrower workflow stated", "occurred_at": "2026-09-22T08:00:00Z"},
        "candidate_snapshot": {"canonical_payload": {"scope": {}}},
    }
    assert _scoped_payload_from_visible_pair(pair) is None
    pair["event"]["content"] = "child workflow 'mobile' and child workflow 'desktop'"
    assert _scoped_payload_from_visible_pair(pair) is None


def test_development_diagnostic_keeps_noops_out_of_state_changing_slice(tmp_path):
    result = score_preflight(CORPUS, EFFECT_PREDICTIONS, tmp_path / "result.json")
    assert result["preflight_passed_pairs"] == 422
    assert result["state_changing_preflight_passed_pairs"] == 368
    assert result["joint_correct_among_state_changing_preflight"] == 368
    assert result["gold_dispositions_among_state_changing_preflight"] == {"accept": 368}
    assert result["source_witness_passed_pairs"] == 363
    assert result["joint_correct_among_source_witness_pairs"] == 363
    assert result["gold_dispositions_among_source_witness"] == {"accept": 363}
    assert result["source_witness_reasons"]["prior setting lacks source witness"] == 5
    assert result["no_op_preflight_is_autonomy_eligible"] is False
    assert result["counts_as_autonomous"] is False


def test_replacement_payload_extractor_requires_identity_and_effective_time():
    prior = {
        "kind": "fact", "proposition": "For Widget 1, the primary configuration records setting 18.",
        "scope": {"product": "Widget 1", "workflow": "primary"}, "status": "active",
        "epistemic_basis": "asserted", "sensitivity": "normal",
        "valid_from": "2026-09-20T08:00:00Z", "valid_until": None,
    }
    content = (
        "The approved configuration audit authorizes Widget 1 primary configuration "
        "to replace setting 18 with setting 19 effective 2026-09-22T12:00:00Z. "
        "The earlier configuration remains the historical record before noon; "
        "this event records activation at noon."
    )
    pair = {
        "event": {"content": content, "occurred_at": "2026-09-22T12:00:00Z"},
        "candidate_snapshot": {"canonical_payload": prior},
    }
    proposed = _replacement_payload_from_visible_pair(pair)
    assert proposed is not None
    assert proposed["proposition"] == "Widget 1 primary configuration use setting 19."
    assert proposed["valid_from"] == pair["event"]["occurred_at"]
    assert prior["proposition"].endswith("setting 18.")
    pair["event"]["occurred_at"] = "2026-09-22T11:00:00Z"
    assert _replacement_payload_from_visible_pair(pair) is None
    pair["event"]["occurred_at"] = "2026-09-22T12:00:00Z"
    pair["candidate_snapshot"]["canonical_payload"]["scope"]["workflow"] = "secondary"
    assert _replacement_payload_from_visible_pair(pair) is None
