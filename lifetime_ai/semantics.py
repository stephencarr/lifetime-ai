from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Protocol

from .types import Event, StateItem


class Relationship(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    NARROWS_SCOPE = "narrows_scope"
    SUPERSEDES = "supersedes"
    UNRELATED = "unrelated"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class RelationshipResult:
    probabilities: Mapping[Relationship, float]
    decision: Relationship
    confidence: float
    escalate: bool = False

    def __post_init__(self) -> None:
        if set(self.probabilities) != set(Relationship):
            raise ValueError("probabilities must contain every relationship class")
        if any(value < 0 or value > 1 for value in self.probabilities.values()):
            raise ValueError("probabilities must be between zero and one")
        if abs(sum(self.probabilities.values()) - 1.0) > 1e-6:
            raise ValueError("probabilities must sum to one")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between zero and one")
        if self.decision is Relationship.UNCERTAIN and not self.escalate:
            raise ValueError("uncertain decisions must escalate")

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> RelationshipResult:
        try:
            probabilities = {
                Relationship(name): float(probability)
                for name, probability in dict(value["probabilities"]).items()
            }
            return cls(probabilities, Relationship(str(value["decision"])),
                       float(value["confidence"]), bool(value.get("escalate", False)))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("invalid typed relationship result") from error


class RelationshipClassifier(Protocol):
    def classify(self, event: Event, candidate: StateItem | None) -> RelationshipResult: ...


class ManualClassifier:
    """Fixture/manual classifier implementing the replaceable semantic boundary."""

    def __init__(self, results: Mapping[str, RelationshipResult]):
        self.results = results

    def classify(self, event: Event, candidate: StateItem | None) -> RelationshipResult:
        return self.results[event.event_id]
