from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .validation import CorpusValidationError, RELATIONSHIPS


FEATURE_MINIMUMS = {
    "preference_reinforcement": 4,
    "direct_correction": 4,
    "scope_narrowing": 4,
    "temporal_supersession": 4,
    "explicit_expiry": 4,
    "commitment_resolution": 4,
    "commitment_failure": 3,
    "contradiction_without_repair": 4,
    "genuine_ambiguity": 4,
    "irrelevant_noise": 6,
    "source_deletion": 3,
    "derivative_invalidation": 3,
    "independent_support_survives": 2,
    "unauthorized_injection_text": 4,
    "silence_is_correct": 4,
    "late_or_retroactive_report": 3,
    "sensitive_state": 3,
}
DISPOSITIONS = {"accept", "reject_unauthorized", "reject_invalid", "abstain", "no_op"}
EFFECTS = {
    "reinforce", "preserve_conflict", "add_scoped_item",
    "close_and_replace", "resolve", "none",
}
ACTIONS = {"none", "clarify", "investigate", "outreach_candidate", "silence"}
PARTITIONS = {"pilot_development", "pilot_holdout"}


def _require_both(values: dict[str, set[str]], names: set[str], label: str,
                  errors: list[str]) -> None:
    for name in sorted(names):
        if values.get(name, set()) != PARTITIONS:
            errors.append(f"{label} {name} must appear in both pilot partitions")


def validate_development_pilot_coverage(histories: list[dict[str, Any]]) -> None:
    """Enforce the approved 30-history/120-pair development-pilot matrix."""
    errors: list[str] = []
    if len(histories) != 30:
        errors.append(f"expected 30 histories, found {len(histories)}")
    pair_count = sum(len(history["pair_inputs"]) for history in histories)
    if pair_count < 120:
        errors.append(f"expected at least 120 pairs, found {pair_count}")
    partition_counts = Counter(history["partition"] for history in histories)
    if partition_counts != Counter({"pilot_development": 21, "pilot_holdout": 9}):
        errors.append(f"expected 21/9 history split, found {dict(partition_counts)}")

    relationship_counts: Counter[str] = Counter()
    relationship_holdout: Counter[str] = Counter()
    relationship_families: dict[tuple[str, str], set[str]] = defaultdict(set)
    feature_counts: Counter[str] = Counter()
    feature_partitions: dict[str, set[str]] = defaultdict(set)
    disposition_partitions: dict[str, set[str]] = defaultdict(set)
    effect_partitions: dict[str, set[str]] = defaultdict(set)
    action_partitions: dict[str, set[str]] = defaultdict(set)
    hostile_count = 0
    hostile_partitions: set[str] = set()

    for history in histories:
        partition = history["partition"]
        family = history["family_id"]
        if history["dataset_version"] == "pilot-v0.2":
            pair_features = {feature for gold in history["evaluator_only"]["pair_gold"]
                             for feature in gold.get("feature_tags", [])}
            if pair_features != set(history["feature_tags"]):
                errors.append(
                    f"history {history['history_id']} feature tags do not match pair tags")
            if not history["evaluator_only"].get("expected_favors_rationale"):
                errors.append(
                    f"history {history['history_id']} lacks expected-favors rationale")
        for feature in history["feature_tags"]:
            feature_counts[feature] += 1
            feature_partitions[feature].add(partition)
        if history["evaluator_only"]["expected_favors"] != "architecture":
            hostile_count += 1
            hostile_partitions.add(partition)
        for gold in history["evaluator_only"]["pair_gold"]:
            relationship = gold["semantic_relationship"]
            relationship_counts[relationship] += 1
            relationship_families[(relationship, partition)].add(family)
            if partition == "pilot_holdout":
                relationship_holdout[relationship] += 1
            disposition_partitions[gold["transition_disposition"]].add(partition)
            effect_partitions[gold["expected_state_effect"]["effect"]].add(partition)
            action_partitions[gold["expected_external_action"]].add(partition)

    for relationship in sorted(RELATIONSHIPS):
        if relationship_counts[relationship] < 12:
            errors.append(f"relationship {relationship} has fewer than 12 pairs")
        if relationship_holdout[relationship] < 3:
            errors.append(f"relationship {relationship} has fewer than 3 holdout pairs")
        for partition in sorted(PARTITIONS):
            if len(relationship_families[(relationship, partition)]) < 2:
                errors.append(
                    f"relationship {relationship} needs multiple families in {partition}")

    for feature, minimum in FEATURE_MINIMUMS.items():
        if feature_counts[feature] < minimum:
            errors.append(f"feature {feature} has fewer than {minimum} histories")
        if feature_partitions[feature] != PARTITIONS:
            errors.append(f"feature {feature} must appear in both pilot partitions")
    if hostile_count < 6 or hostile_partitions != PARTITIONS:
        errors.append("baseline-favoring histories need at least 6 cases across both partitions")

    _require_both(disposition_partitions, DISPOSITIONS, "disposition", errors)
    _require_both(effect_partitions, EFFECTS, "effect", errors)
    _require_both(action_partitions, ACTIONS, "action", errors)
    if errors:
        raise CorpusValidationError("development-pilot coverage failed: " + "; ".join(errors))
