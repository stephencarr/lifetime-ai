import json
from pathlib import Path

import pytest

from lifetime_ai.evaluation.canonical import read_jsonl
from lifetime_ai.evaluation.validation import CorpusValidationError, RELATIONSHIPS
from scripts.score_g4_development import _prediction, score_development


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "evaluation" / "corpus" / "frozen-g4-v0.1-sealed-v21"


def _prediction_rows(limit: int | None = None):
    rows = []
    for history in read_jsonl(CORPUS / "development.jsonl"):
        for pair in history["pair_inputs"]:
            gold = next(
                item for item in history["evaluator_only"]["pair_gold"]
                if item["pair_id"] == pair["pair_id"]
            )
            probabilities = {name: "0" for name in RELATIONSHIPS}
            probabilities[gold["semantic_relationship"]] = "1"
            rows.append({
                "history_id": history["history_id"],
                "pair_id": pair["pair_id"],
                "candidate_snapshot_id": pair["candidate_snapshot_id"],
                "probabilities": probabilities,
                "decision": gold["semantic_relationship"],
                "confidence": "1",
                "escalate": gold["semantic_relationship"] == "uncertain",
            })
    return rows if limit is None else rows[:limit]


def test_development_scorer_requires_complete_artifact_and_runs_when_authorized(tmp_path):
    predictions = tmp_path / "predictions.jsonl"
    predictions.write_text("\n".join(json.dumps(row) for row in _prediction_rows()), encoding="utf-8")

    result = score_development(CORPUS, predictions)
    assert result["partition"] == "development"
    assert result["status"] == "DEVELOPMENT_DIAGNOSTIC_ONLY"
    assert result["validator_applied"] is False
    assert result["pair_count"] == 1080
    assert result["metrics"]["candidate_accept_precision"] == 1.0
    assert result["metrics"]["candidate_accept_coverage"] == 0.875


def test_development_scorer_rejects_incomplete_artifact(tmp_path):
    predictions = tmp_path / "predictions.jsonl"
    predictions.write_text(
        json.dumps(_prediction_rows(limit=1)[0]) + "\n", encoding="utf-8"
    )
    with pytest.raises(CorpusValidationError, match="incomplete"):
        score_development(CORPUS, predictions, require_authorization=False)


def test_development_scorer_rejects_holdout_pairs(tmp_path):
    # A fabricated non-development identity exercises the boundary without
    # opening the sealed holdout payload.
    probabilities = {name: "0" for name in RELATIONSHIPS}
    probabilities["supports"] = "1"
    row = {
        "history_id": "non-development-history",
        "pair_id": "non-development-pair",
        "candidate_snapshot_id": "non-development-snapshot",
        "probabilities": probabilities,
        "decision": "supports",
        "confidence": "1",
        "escalate": False,
    }
    predictions = tmp_path / "predictions.jsonl"
    predictions.write_text(json.dumps(row) + "\n", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="non-development"):
        score_development(CORPUS, predictions, require_authorization=False)


def test_uncertain_cannot_be_marked_as_candidate_accept():
    probabilities = {name: "0" for name in RELATIONSHIPS}
    probabilities["uncertain"] = "1"
    row = {
        "history_id": "history", "pair_id": "pair", "candidate_snapshot_id": "snapshot",
        "probabilities": probabilities, "decision": "uncertain", "confidence": "1",
        "escalate": False,
    }
    with pytest.raises(CorpusValidationError, match="must escalate"):
        _prediction(row)
