from __future__ import annotations

import hashlib
from collections import defaultdict
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
