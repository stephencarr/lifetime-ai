import json

import pytest

from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g3_frozen_smoke import run


def test_frozen_smoke_rejects_unsealed_input(tmp_path):
    (tmp_path / "manifest.json").write_text(
        json.dumps({"state": "STAGED_NOT_SEALED", "model_predictions_present": False}),
        encoding="utf-8",
    )
    with pytest.raises(CorpusValidationError, match="requires a sealed corpus"):
        run(tmp_path)


def test_frozen_smoke_rejects_prediction_tainted_manifest(tmp_path):
    (tmp_path / "manifest.json").write_text(
        json.dumps({"state": "SEALED", "model_predictions_present": True}),
        encoding="utf-8",
    )
    with pytest.raises(CorpusValidationError, match="model predictions are absent"):
        run(tmp_path)
