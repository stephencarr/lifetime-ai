from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any


TOKEN = re.compile(r"[\w']+", re.UNICODE)


@dataclass(frozen=True)
class MatchConfiguration:
    kind_weight: int = 20
    proposition_weight: int = 30
    scope_weight: int = 15
    status_weight: int = 10
    validity_weight: int = 10
    epistemic_weight: int = 5
    sensitivity_weight: int = 5
    evidence_weight: int = 5
    threshold: int = 70
    temporal_tolerance_seconds: int = 0


def _tokens(text: str) -> set[str]:
    return {match.group(0).casefold() for match in TOKEN.finditer(text)}


def _jaccard(left: set[str], right: set[str]) -> int:
    if not left and not right:
        return 100
    return round(100 * len(left & right) / len(left | right))


def _time_close(left: str | None, right: str | None, tolerance: int) -> bool:
    if left is None or right is None:
        return left == right
    return abs((datetime.fromisoformat(left.replace("Z", "+00:00")) -
                datetime.fromisoformat(right.replace("Z", "+00:00"))).total_seconds()) <= tolerance


def semantic_state_score(predicted: dict[str, Any], gold: dict[str, Any],
                         config: MatchConfiguration) -> int:
    score = 0
    score += config.kind_weight if predicted.get("kind") == gold.get("kind") else 0
    score += config.proposition_weight * _jaccard(
        _tokens(predicted.get("proposition", "")), _tokens(gold.get("proposition", ""))) // 100
    score += config.scope_weight if predicted.get("scope", {}) == gold.get("scope", {}) else 0
    score += config.status_weight if predicted.get("status") == gold.get("status") else 0
    validity = _time_close(predicted.get("valid_from"), gold.get("valid_from"),
                           config.temporal_tolerance_seconds) and _time_close(
                               predicted.get("valid_until"), gold.get("valid_until"),
                               config.temporal_tolerance_seconds)
    score += config.validity_weight if validity else 0
    score += config.epistemic_weight if predicted.get("epistemic_basis") == gold.get("epistemic_basis") else 0
    score += config.sensitivity_weight if predicted.get("sensitivity") == gold.get("sensitivity") else 0
    predicted_evidence = set(predicted.get("evidence_ids", []))
    gold_evidence = set(gold.get("evidence_ids", []))
    score += config.evidence_weight * _jaccard(predicted_evidence, gold_evidence) // 100
    return score


def greedy_semantic_matches(predicted: list[dict[str, Any]], gold: list[dict[str, Any]],
                            config: MatchConfiguration) -> list[tuple[int, int, int]]:
    """Deterministic pilot matcher; final assignment algorithm must be frozen before G5."""
    candidates = sorted(
        ((semantic_state_score(p, g, config), pi, gi)
         for pi, p in enumerate(predicted) for gi, g in enumerate(gold)),
        key=lambda item: (-item[0], item[1], item[2]),
    )
    used_predicted: set[int] = set()
    used_gold: set[int] = set()
    matches = []
    for score, pi, gi in candidates:
        if score < config.threshold or pi in used_predicted or gi in used_gold:
            continue
        used_predicted.add(pi)
        used_gold.add(gi)
        matches.append((pi, gi, score))
    return matches
