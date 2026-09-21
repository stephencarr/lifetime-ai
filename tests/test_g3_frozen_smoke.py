import pytest

from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts import run_g3_frozen_smoke


def test_frozen_smoke_rejects_unsealed_input(tmp_path):
    (tmp_path / "manifest.json").write_text("{}", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="not a frozen-G4 sealed manifest"):
        run_g3_frozen_smoke.run(tmp_path)


def test_frozen_smoke_rejects_prediction_tainted_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(
        run_g3_frozen_smoke,
        "verify_sealed_corpus",
        lambda _path: {"state": "SEALED", "model_predictions_present": True},
    )
    with pytest.raises(CorpusValidationError, match="model predictions are absent"):
        run_g3_frozen_smoke.run(tmp_path)
