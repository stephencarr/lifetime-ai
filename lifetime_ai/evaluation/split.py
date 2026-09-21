from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from typing import Any, Iterable


def _rank(seed: str, family_id: str) -> str:
    return hashlib.sha256(f"{seed}\0{family_id}".encode()).hexdigest()


def split_whole_families(histories: list[dict[str, Any]], *, seed: str,
                         holdout_fraction: int = 25) -> dict[str, str]:
    """Assign all members of a family to one pilot partition deterministically."""
    families = sorted({history["family_id"] for history in histories},
                      key=lambda family: _rank(seed, family))
    holdout_count = max(1, (len(families) * holdout_fraction + 99) // 100)
    holdout = set(families[:holdout_count])
    return {family: "pilot_holdout" if family in holdout else "pilot_development"
            for family in families}


def split_stratified_families(histories: list[dict[str, Any]], *, seed: str,
                              holdout_history_count: int = 9) -> dict[str, str]:
    """Greedily preserve family boundaries while maximizing holdout stratum coverage."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for history in histories:
        grouped[history["family_id"]].append(history)
    if holdout_history_count <= 0 or holdout_history_count >= len(histories):
        raise ValueError("holdout_history_count must split the corpus")

    def tokens(records: list[dict[str, Any]]) -> set[str]:
        result = {f"feature:{tag}" for record in records for tag in record["feature_tags"]}
        for record in records:
            result.add(f"favor:{record['evaluator_only']['expected_favors']}")
            if any(event["event_type"] in {"deletion", "redaction"}
                   for event in record["timeline"]):
                result.add("has_deletion")
            for gold in record["evaluator_only"]["pair_gold"]:
                result.add(f"relationship:{gold['semantic_relationship']}")
                result.add(f"disposition:{gold['transition_disposition']}")
                result.add(f"effect:{gold['expected_state_effect']['effect']}")
                result.add(f"action:{gold['expected_external_action']}")
                if gold["semantic_relationship"] == "uncertain":
                    result.add("has_ambiguity")
        return result

    remaining = set(grouped)
    holdout: set[str] = set()
    covered: Counter[str] = Counter()
    selected_histories = 0
    while selected_histories < holdout_history_count:
        candidates = []
        for family in remaining:
            size = len(grouped[family])
            if selected_histories + size > holdout_history_count:
                continue
            novelty = sum(1 for token in tokens(grouped[family]) if covered[token] == 0)
            rarity = sum(1 / (1 + covered[token]) for token in tokens(grouped[family]))
            candidates.append((-novelty, -rarity, _rank(seed, family), family))
        if not candidates:
            raise ValueError("family sizes cannot produce the requested holdout history count")
        family = min(candidates)[-1]
        holdout.add(family)
        remaining.remove(family)
        selected_histories += len(grouped[family])
        covered.update(tokens(grouped[family]))
    return {family: "pilot_holdout" if family in holdout else "pilot_development"
            for family in grouped}


def assign_disjoint_gate_holdouts(family_ids: Iterable[str], *, seed: str) -> dict[str, str]:
    """Assign a family to at most one final gate holdout."""
    gates = ("g4_holdout", "g5_holdout", "g6_holdout", "g7_holdout")
    assignments: dict[str, str] = {}
    buckets: dict[str, list[str]] = defaultdict(list)
    for family in sorted(set(family_ids)):
        gate = gates[int(_rank(seed, family), 16) % len(gates)]
        assignments[family] = gate
        buckets[gate].append(family)
    return assignments
