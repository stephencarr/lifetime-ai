import pytest

from lifetime_ai.evaluation.contracts import PredictedRelationship
from lifetime_ai.evaluation.g4_metrics import (
    PairEvaluation,
    expected_calibration_error,
    summarize_g4_metrics,
    wilson_interval,
)
from lifetime_ai.evaluation.validation import RELATIONSHIPS


def prediction(decision: str, confidence: str, *, escalate: bool = False):
    remaining = [name for name in sorted(RELATIONSHIPS) if name != decision]
    probabilities = {name: "0" for name in remaining}
    probabilities[decision] = confidence
    return PredictedRelationship(
        candidate_snapshot_id="snapshot-1",
        probabilities=probabilities,
        decision=decision,
        confidence=confidence,
        escalate=escalate,
    )


def test_g4_metrics_separate_autonomous_precision_from_coverage_and_recall():
    items = [
        PairEvaluation(prediction("supports", "0.9"), "supports"),
        PairEvaluation(prediction("contradicts", "0.8"), "supports"),
        PairEvaluation(prediction("uncertain", "0.6", escalate=True), "uncertain"),
        PairEvaluation(prediction("supersedes", "0.7"), "supersedes", eligible=False),
    ]

    metrics = summarize_g4_metrics(items)

    assert metrics.eligible_count == 3
    assert metrics.autonomous_count == 2
    assert metrics.correct_autonomous_count == 1
    assert metrics.autonomous_precision == pytest.approx(0.5)
    assert metrics.autonomous_coverage == pytest.approx(2 / 3)
    assert metrics.per_class_precision["supports"] == pytest.approx(1.0)
    assert metrics.per_class_precision["contradicts"] == pytest.approx(0.0)
    assert metrics.per_class_recall["supports"] == pytest.approx(0.5)
    assert metrics.per_class_recall["uncertain"] == pytest.approx(1.0)
    assert metrics.autonomous_precision_wilson_95 is not None


def test_g4_metrics_use_multiclass_brier_and_fixed_width_ece():
    items = [
        PairEvaluation(prediction("supports", "1"), "supports"),
        PairEvaluation(prediction("contradicts", "1"), "supports"),
    ]

    metrics = summarize_g4_metrics(items)

    assert metrics.multiclass_brier_score == pytest.approx(1.0)
    assert expected_calibration_error(items, bin_count=2) == pytest.approx(0.5)


def test_acceptable_alternative_counts_for_precision_but_primary_drives_calibration():
    item = PairEvaluation(
        prediction("uncertain", "1", escalate=True),
        "contradicts",
        acceptable_alternatives=("uncertain",),
    )
    metrics = summarize_g4_metrics([item])
    assert metrics.per_class_precision["uncertain"] == 1.0
    assert metrics.multiclass_brier_score == 2.0
    assert metrics.expected_calibration_error == 1.0


def test_wilson_interval_handles_empty_and_validates_counts():
    assert wilson_interval(0, 0) is None
    interval = wilson_interval(95, 100)
    assert interval is not None
    assert interval.lower < 0.95 < interval.upper
    with pytest.raises(ValueError):
        wilson_interval(101, 100)
