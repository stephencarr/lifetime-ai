from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import sqrt
from typing import Iterable, Mapping

from .contracts import PredictedRelationship
from .validation import RELATIONSHIPS


@dataclass(frozen=True)
class PairEvaluation:
    """One eligible pair-classification result and its primary gold label."""

    prediction: PredictedRelationship
    gold_relationship: str
    eligible: bool = True
    acceptable_alternatives: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.gold_relationship not in RELATIONSHIPS:
            raise ValueError(f"unknown gold relationship: {self.gold_relationship}")
        if set(self.acceptable_alternatives) - RELATIONSHIPS:
            raise ValueError("unknown acceptable alternative relationship")


def _correct(item: PairEvaluation) -> bool:
    return (item.prediction.decision == item.gold_relationship
            or item.prediction.decision in item.acceptable_alternatives)


@dataclass(frozen=True)
class WilsonInterval:
    lower: float
    upper: float


@dataclass(frozen=True)
class G4Metrics:
    eligible_count: int
    autonomous_count: int
    correct_autonomous_count: int
    autonomous_precision: float | None
    autonomous_coverage: float
    per_class_precision: Mapping[str, float | None]
    per_class_recall: Mapping[str, float | None]
    multiclass_brier_score: float
    expected_calibration_error: float
    autonomous_precision_wilson_95: WilsonInterval | None


def wilson_interval(
    successes: int,
    trials: int,
    *,
    z: float = 1.959963984540054,
) -> WilsonInterval | None:
    """Return a two-sided Wilson score interval, or None for zero trials."""
    if successes < 0 or trials < 0 or successes > trials:
        raise ValueError("successes and trials must satisfy 0 <= successes <= trials")
    if trials == 0:
        return None
    observed = successes / trials
    denominator = 1 + z * z / trials
    center = (observed + z * z / (2 * trials)) / denominator
    margin = (
        z
        * sqrt((observed * (1 - observed) + z * z / (4 * trials)) / trials)
        / denominator
    )
    return WilsonInterval(max(0.0, center - margin), min(1.0, center + margin))


def _selected_probability(item: PairEvaluation) -> float:
    return float(Decimal(item.prediction.probabilities[item.prediction.decision]))


def _precision_by_class(
    items: Iterable[PairEvaluation],
) -> dict[str, float | None]:
    values = {relationship: [0, 0] for relationship in sorted(RELATIONSHIPS)}
    for item in items:
        if not item.eligible:
            continue
        values[item.prediction.decision][1] += 1
        values[item.prediction.decision][0] += _correct(item)
    return {
        relationship: (correct / selected if selected else None)
        for relationship, (correct, selected) in values.items()
    }


def _recall_by_class(
    items: Iterable[PairEvaluation],
) -> dict[str, float | None]:
    values = {relationship: [0, 0] for relationship in sorted(RELATIONSHIPS)}
    for item in items:
        if not item.eligible:
            continue
        values[item.gold_relationship][1] += 1
        values[item.gold_relationship][0] += _correct(item)
    return {
        relationship: (correct / gold_count if gold_count else None)
        for relationship, (correct, gold_count) in values.items()
    }


def multiclass_brier_score(items: Iterable[PairEvaluation]) -> float:
    eligible = [item for item in items if item.eligible]
    if not eligible:
        return 0.0
    total = 0.0
    for item in eligible:
        total += sum(
            (
                float(Decimal(item.prediction.probabilities[relationship]))
                - (relationship == item.gold_relationship)
            )
            ** 2
            for relationship in RELATIONSHIPS
        )
    return total / len(eligible)


def expected_calibration_error(
    items: Iterable[PairEvaluation],
    *,
    bin_count: int = 15,
) -> float:
    """Compute fixed-width ECE over eligible selected-class predictions."""
    if bin_count <= 0:
        raise ValueError("bin_count must be positive")
    eligible = [item for item in items if item.eligible]
    if not eligible:
        return 0.0
    bins: list[list[tuple[float, bool]]] = [[] for _ in range(bin_count)]
    for item in eligible:
        confidence = min(1.0, max(0.0, _selected_probability(item)))
        index = min(bin_count - 1, int(confidence * bin_count))
        bins[index].append((confidence, item.prediction.decision == item.gold_relationship))
    return sum(
        len(bucket)
        / len(eligible)
        * abs(
            sum(confidence for confidence, _ in bucket) / len(bucket)
            - sum(correct for _, correct in bucket) / len(bucket)
        )
        for bucket in bins
        if bucket
    )


def summarize_g4_metrics(items: Iterable[PairEvaluation]) -> G4Metrics:
    """Calculate the frozen G4 pair-classification metrics."""
    materialized = list(items)
    eligible = [item for item in materialized if item.eligible]
    autonomous = [item for item in eligible if not item.prediction.escalate]
    correct_autonomous = [
        item for item in autonomous if _correct(item)
    ]
    autonomous_count = len(autonomous)
    correct_count = len(correct_autonomous)
    precision = correct_count / autonomous_count if autonomous_count else None
    return G4Metrics(
        eligible_count=len(eligible),
        autonomous_count=autonomous_count,
        correct_autonomous_count=correct_count,
        autonomous_precision=precision,
        autonomous_coverage=(autonomous_count / len(eligible) if eligible else 0.0),
        per_class_precision=_precision_by_class(materialized),
        per_class_recall=_recall_by_class(materialized),
        multiclass_brier_score=multiclass_brier_score(materialized),
        expected_calibration_error=expected_calibration_error(materialized),
        autonomous_precision_wilson_95=wilson_interval(correct_count, autonomous_count),
    )
