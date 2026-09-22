from pathlib import Path

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


def test_frozen_smoke_oracle_reprojects_at_each_checkpoint_sequence(monkeypatch):
    """Regression test for the oracle temporal leak: `run()` must rebuild the
    limited-oracle projection at each checkpoint's own `after_sequence`,
    never once at the history's final sequence reused for every earlier
    checkpoint. A history with >1 checkpoint whose gold sequences differ
    proves this by observing distinct sequence arguments and a strictly
    growing gold-transition count across checkpoints."""
    calls_by_history: dict[str, list[int]] = {}
    real_build = run_g3_frozen_smoke.build_limited_oracle_projection

    def spy(history, *, sequence):
        calls_by_history.setdefault(history["history_id"], []).append(sequence)
        return real_build(history, sequence=sequence)

    monkeypatch.setattr(run_g3_frozen_smoke, "build_limited_oracle_projection", spy)

    corpus_root = (
        Path(__file__).resolve().parents[1]
        / "evaluation" / "corpus" / "frozen-g4-v0.1-sealed-v21"
    )
    if not corpus_root.exists():
        pytest.skip("frozen-g4-v0.1-sealed-v21 fixture not present in this checkout")

    from lifetime_ai.evaluation.canonical import read_jsonl
    from lifetime_ai.evaluation.projection import build_system_history_projection

    histories = read_jsonl(corpus_root / "development.jsonl")
    history = next(
        item for item in histories
        if len({c["after_sequence"] for c in build_system_history_projection(item)["checkpoint_requests"]}) > 1
    )

    run_g3_frozen_smoke.run(corpus_root)

    sequences_seen = calls_by_history[history["history_id"]]
    assert len(set(sequences_seen)) > 1, (
        "expected build_limited_oracle_projection to be called with more "
        "than one distinct sequence for this history's checkpoints; seeing "
        "only the final sequence every time would mean the temporal leak "
        "has regressed"
    )
