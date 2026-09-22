import json

import pytest

from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_effect_development import _relationship_rows
from scripts.run_g4_grouped_development import Case


def _case(family: str, pair: str) -> Case:
    return Case(family, "history-" + pair, pair, "snapshot-" + pair, "supports", (),
                "low", "", "", "", "")


def test_effect_runner_requires_aligned_out_of_fold_relationship_artifact(tmp_path):
    cases = [_case("family-a", "pair-a"), _case("family-b", "pair-b")]
    folds = [[0], [1]]
    rows = [{
        "pair_id": case.pair_id, "history_id": case.history_id,
        "family_id": case.family_id, "candidate_snapshot_id": case.snapshot_id,
        "gold_relationship": case.gold, "model_fold": number,
        "decision": "supports", "confidence": "1", "probabilities": {"supports": "1"},
    } for number, case in enumerate(cases)]
    path = tmp_path / "relationships.jsonl"
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    assert len(_relationship_rows(path, cases, folds)) == 2

    rows[0]["model_fold"] = 1
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="fold mismatch"):
        _relationship_rows(path, cases, folds)

    rows[0]["model_fold"] = 0
    rows[0]["confidence"] = "0.5"
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="confidence mismatch"):
        _relationship_rows(path, cases, folds)
