from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection,
    build_retrieval_projection,
    build_system_history_projection,
    contains_evaluator_only_material,
)


def _canaries(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str) and "EVALUATOR_ONLY_CANARY_" in value:
        found.add(value)
    elif isinstance(value, list):
        for item in value:
            found.update(_canaries(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.update(_canaries(item))
    return found


def check_projection_leakage(histories: list[dict[str, Any]]) -> dict[str, Any]:
    """Hard-check evaluator-only canaries against actual system projections."""
    failures = Counter()
    checked = Counter()
    relationship_dispositions: dict[str, Counter[str]] = defaultdict(Counter)
    disposition_relationships: dict[str, Counter[str]] = defaultdict(Counter)
    for history in histories:
        canaries = _canaries(history["evaluator_only"])
        pair_gold = {item["pair_id"]: item
                     for item in history["evaluator_only"]["pair_gold"]}
        system_projection = build_system_history_projection(history)
        checked["system_history"] += 1
        failures["system_history"] += int(
            contains_evaluator_only_material(system_projection, canaries))
        for pair in history["pair_inputs"]:
            relationship = pair_gold[pair["pair_id"]]["semantic_relationship"]
            disposition = pair_gold[pair["pair_id"]]["transition_disposition"]
            relationship_dispositions[relationship][disposition] += 1
            disposition_relationships[disposition][relationship] += 1
            for name, projection in (
                ("candidate_retrieval", build_retrieval_projection(
                    history, pair["pair_id"])),
                ("pair_classification", build_pair_classification_projection(
                    history, pair["pair_id"])),
            ):
                checked[name] += 1
                failures[name] += int(
                    contains_evaluator_only_material(projection, canaries))

    total_failures = sum(failures.values())
    return {
        "protocol": "g3-system-projection-canary-v1",
        "hard_gate": "no evaluator-only canary may occur in a system-facing projection",
        "checked_projection_counts": dict(sorted(checked.items())),
        "leakage_failures_by_projection": dict(sorted(failures.items())),
        "leakage_failures": total_failures,
        "passed": total_failures == 0,
        "relationship_disposition_counts": {
            relation: dict(sorted(counts.items()))
            for relation, counts in sorted(relationship_dispositions.items())},
        "disposition_relationship_counts": {
            disposition: dict(sorted(counts.items()))
            for disposition, counts in sorted(disposition_relationships.items())},
        "statistical_text_accuracy_gate": "not_applicable",
        "rationale": (
            "Semantic relationship is defined relative to an event and candidate; "
            "disposition is determined from structured authority/validity policy. "
            "Event-text-only accuracy is retained only as an exploratory shortcut "
            "diagnostic and is not a gold-label leakage test."),
    }
