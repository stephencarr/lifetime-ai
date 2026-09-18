from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Protocol

from .semantics import Relationship, RelationshipClassifier, RelationshipResult
from .store import Store
from .types import Event, EventType, StateItem, StateKind, StateStatus, Transition


@dataclass(frozen=True)
class TransitionProposal:
    proposal_id: str
    event_id: str
    candidate_item_id: str | None
    relationship: Relationship
    result: RelationshipResult
    transitions: tuple[Transition, ...]

    def payload(self) -> str:
        value = {
            "proposal_id": self.proposal_id,
            "event_id": self.event_id,
            "candidate_item_id": self.candidate_item_id,
            "relationship": self.relationship.value,
            "confidence": self.result.confidence,
            "escalate": self.result.escalate,
            "transition_ids": [item.transition_id for item in self.transitions],
        }
        return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    outcome: str
    reason: str


class CandidateSelector(Protocol):
    def select(self, event: Event, items: tuple[StateItem, ...]) -> tuple[StateItem, ...]: ...


class ExplicitCandidateSelector:
    """Model-free selector using a fixture/user-supplied candidate identifier."""

    def select(self, event: Event, items: tuple[StateItem, ...]) -> tuple[StateItem, ...]:
        candidate_id = (event.metadata or {}).get("candidate_item_id")
        return tuple(item for item in items if item.item_id == candidate_id)


def row_to_item(row: object) -> StateItem:
    return StateItem(
        row["item_id"], StateKind(row["kind"]), row["proposition"],
        row["source_event_id"], EventType(row["source_type"]),
        datetime.fromisoformat(row["occurred_at"]),
        StateStatus(row["status"]), row["confidence"], row["sensitivity"],
        datetime.fromisoformat(row["valid_from"]) if row["valid_from"] else None,
        datetime.fromisoformat(row["valid_until"]) if row["valid_until"] else None,
    )


class ProposalBuilder:
    def build(self, event: Event, candidate: StateItem | None,
              result: RelationshipResult) -> TransitionProposal:
        proposal_id = f"proposal:{event.event_id}"
        relationship = result.decision
        mutations: tuple[Transition, ...] = ()
        if relationship is Relationship.SUPPORTS and candidate:
            reinforced = replace(candidate, source_event_id=event.event_id,
                                 source_type=event.event_type, occurred_at=event.occurred_at)
            mutations = (Transition(f"transition:{event.event_id}:support", event.event_id,
                                    reinforced, reason="supports existing state"),)
        elif relationship in (Relationship.CONTRADICTS, Relationship.NARROWS_SCOPE) and candidate:
            suffix = "conflict" if relationship is Relationship.CONTRADICTS else "scope"
            new_item = StateItem(f"{candidate.item_id}:{suffix}:{event.event_id}", candidate.kind,
                                 event.text, event.event_id, event.event_type, event.occurred_at,
                                 sensitivity=candidate.sensitivity, valid_from=event.occurred_at)
            mutations = (Transition(f"transition:{event.event_id}:{suffix}", event.event_id,
                                    new_item, reason=relationship.value),)
        elif relationship is Relationship.SUPERSEDES and candidate:
            closed = replace(candidate, source_event_id=event.event_id,
                             source_type=event.event_type, occurred_at=event.occurred_at,
                             status=StateStatus.REVOKED, valid_until=event.occurred_at)
            replacement = StateItem(f"{candidate.item_id}:replacement:{event.event_id}", candidate.kind,
                                    event.text, event.event_id, event.event_type, event.occurred_at,
                                    sensitivity=candidate.sensitivity, valid_from=event.occurred_at)
            mutations = (
                Transition(f"transition:{event.event_id}:close", event.event_id, closed,
                           reason="superseded prior state"),
                Transition(f"transition:{event.event_id}:replace", event.event_id, replacement,
                           reason="replacement state"),
            )
        return TransitionProposal(proposal_id, event.event_id,
                                  candidate.item_id if candidate else None,
                                  relationship, result, mutations)


class TransitionValidator:
    """The only G2 component with canonical-state mutation authority."""

    def __init__(self, store: Store):
        self.store = store

    def validate_and_commit(self, proposal: TransitionProposal, *,
                            fail_during_commit: bool = False) -> ValidationResult:
        reason = self._invalid_reason(proposal)
        if reason:
            self.store.record_proposal(proposal.proposal_id, proposal.event_id,
                                       proposal.candidate_item_id, proposal.relationship.value,
                                       proposal.payload(), "rejected", reason)
            return ValidationResult(False, "rejected", reason)
        if proposal.relationship is Relationship.UNCERTAIN:
            self.store.record_proposal(proposal.proposal_id, proposal.event_id,
                                       proposal.candidate_item_id, proposal.relationship.value,
                                       proposal.payload(), "abstained", "requires escalation")
            return ValidationResult(False, "abstained", "requires escalation")
        if proposal.relationship is Relationship.UNRELATED:
            self.store.record_proposal(proposal.proposal_id, proposal.event_id,
                                       proposal.candidate_item_id, proposal.relationship.value,
                                       proposal.payload(), "noop", "unrelated event")
            return ValidationResult(False, "noop", "unrelated event")
        try:
            self.store.commit_proposal(
                proposal.proposal_id, proposal.event_id, proposal.candidate_item_id,
                proposal.relationship.value, proposal.payload(), proposal.transitions,
                fail_after_first=fail_during_commit)
        except Exception as error:
            self.store.record_proposal(proposal.proposal_id, proposal.event_id,
                                       proposal.candidate_item_id, proposal.relationship.value,
                                       proposal.payload(), "rejected", type(error).__name__)
            return ValidationResult(False, "rejected", type(error).__name__)
        return ValidationResult(True, "accepted", "validated")

    def _invalid_reason(self, proposal: TransitionProposal) -> str | None:
        if not self.store.event_exists(proposal.event_id):
            return "missing source event"
        if proposal.relationship in (Relationship.UNRELATED, Relationship.UNCERTAIN):
            return "non-mutating relationship included transitions" if proposal.transitions else None
        if proposal.candidate_item_id is None:
            return "no candidate state item"
        expected = {Relationship.SUPPORTS: 1, Relationship.CONTRADICTS: 1,
                    Relationship.NARROWS_SCOPE: 1, Relationship.SUPERSEDES: 2}
        if len(proposal.transitions) != expected[proposal.relationship]:
            return "unexpected transition count"
        for transition in proposal.transitions:
            item = transition.item
            if transition.event_id != proposal.event_id or item.source_event_id != proposal.event_id:
                return "mutation lacks proposal source"
            if not isinstance(item.kind, StateKind):
                return "unauthorized state kind"
            if transition.operation != "upsert":
                return "unauthorized transition operation"
            if item.valid_from and item.valid_until and item.valid_from > item.valid_until:
                return "invalid temporal interval"
        return None


class TransitionPipeline:
    def __init__(self, store: Store, selector: CandidateSelector,
                 classifier: RelationshipClassifier, validator: TransitionValidator):
        self.store = store
        self.selector = selector
        self.classifier = classifier
        self.validator = validator
        self.builder = ProposalBuilder()

    def process(self, event: Event) -> ValidationResult:
        self.store.ingest(event)
        items = tuple(row_to_item(row) for row in self.store.active())
        candidates = self.selector.select(event, items)
        candidate = candidates[0] if candidates else None
        result = self.classifier.classify(event, candidate)
        proposal = self.builder.build(event, candidate, result)
        return self.validator.validate_and_commit(proposal)
