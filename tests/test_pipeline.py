from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from lifetime_ai.pipeline import (
    ExplicitCandidateSelector, ProposalBuilder, TransitionPipeline,
    TransitionProposal, TransitionValidator, row_to_item,
)
from lifetime_ai.semantics import ManualClassifier, Relationship, RelationshipResult
from lifetime_ai.store import Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition


NOW = datetime(2026, 9, 18, tzinfo=timezone.utc)
FIXTURES = json.loads((Path(__file__).parent / "fixtures" / "g2_relationships.json").read_text())


def result(relationship: Relationship) -> RelationshipResult:
    probabilities = {item: 0.03 for item in Relationship}
    probabilities[relationship] = 0.85
    return RelationshipResult(probabilities, relationship, 0.85,
                              escalate=relationship is Relationship.UNCERTAIN)


class FixedClassifier:
    """A non-ManualClassifier test double proving persistence is classifier-neutral."""

    def __init__(self, decision: Relationship):
        self.decision = decision

    def classify(self, incoming: Event, candidate: StateItem | None) -> RelationshipResult:
        return result(self.decision)


def seed(store: Store) -> None:
    source = Event("seed-event", EventType.USER_MESSAGE,
                   "I prefer concise work answers.", NOW - timedelta(days=1))
    item = StateItem("preference-work", StateKind.PREFERENCE, source.text,
                     source.event_id, source.event_type, source.occurred_at,
                     valid_from=source.occurred_at)
    store.ingest_and_apply(source, Transition("seed-transition", source.event_id, item,
                                             reason="initial preference"))


def event(case: dict[str, str]) -> Event:
    return Event(case["event_id"], EventType.USER_MESSAGE, case["text"], NOW,
                 {"candidate_item_id": "preference-work"})


@pytest.mark.parametrize("case", FIXTURES, ids=lambda case: case["relationship"])
def test_required_relationship_fixture_matrix(tmp_path, case):
    relationship = Relationship(case["relationship"])
    with Store(tmp_path / f"{case['name']}.sqlite") as store:
        seed(store)
        pipeline = TransitionPipeline(
            store, ExplicitCandidateSelector(),
            ManualClassifier({case["event_id"]: result(relationship)}),
            TransitionValidator(store),
        )
        outcome = pipeline.process(event(case))
        proposal = store.proposals()[-1]
        assert proposal["event_id"] == case["event_id"]
        assert proposal["relationship"] == relationship.value

        if relationship is Relationship.SUPPORTS:
            assert outcome.accepted and len(store.active()) == 1
            assert store.active()[0]["item_id"] == "preference-work"
        elif relationship in (Relationship.CONTRADICTS, Relationship.NARROWS_SCOPE):
            assert outcome.accepted and len(store.active()) == 2
            assert store.state_item("preference-work")["status"] == "active"
        elif relationship is Relationship.SUPERSEDES:
            assert outcome.accepted and len(store.active()) == 1
            prior = store.state_item("preference-work")
            assert prior["status"] == "revoked" and prior["valid_until"] == NOW.isoformat()
        elif relationship is Relationship.UNRELATED:
            assert not outcome.accepted and outcome.outcome == "noop"
            assert len(store.transitions()) == 1 and len(store.active()) == 1
        else:
            assert not outcome.accepted and outcome.outcome == "abstained"
            assert len(store.transitions()) == 1 and len(store.active()) == 1


def test_unknown_relationship_type_is_rejected_at_typed_boundary():
    payload = {"probabilities": {item.value: 1 / 6 for item in Relationship},
               "decision": "invented", "confidence": 0.5}
    with pytest.raises(ValueError, match="invalid typed relationship result"):
        RelationshipResult.from_dict(payload)


def test_missing_source_and_unauthorized_kind_are_recorded_rejections(tmp_path):
    with Store(tmp_path / "adversarial.sqlite") as store:
        seed(store)
        incoming = Event("bad-source", EventType.USER_MESSAGE, "Change it", NOW)
        store.ingest(incoming)
        candidate = row_to_item(store.state_item("preference-work"))
        proposal = ProposalBuilder().build(incoming, candidate, result(Relationship.SUPPORTS))
        bad_transition = replace(proposal.transitions[0],
                                 item=replace(proposal.transitions[0].item,
                                              source_event_id="missing"))
        bad = replace(proposal, transitions=(bad_transition,))
        outcome = TransitionValidator(store).validate_and_commit(bad)
        assert outcome.outcome == "rejected" and outcome.reason == "mutation lacks proposal source"
        assert store.proposals()[-1]["outcome"] == "rejected"

    with Store(tmp_path / "kind.sqlite") as store:
        seed(store)
        incoming = Event("bad-kind", EventType.USER_MESSAGE, "Change it", NOW)
        store.ingest(incoming)
        candidate = row_to_item(store.state_item("preference-work"))
        proposal = ProposalBuilder().build(incoming, candidate, result(Relationship.SUPPORTS))
        malformed = replace(proposal.transitions[0].item, kind="unauthorized")  # type: ignore[arg-type]
        outcome = TransitionValidator(store).validate_and_commit(
            replace(proposal, transitions=(replace(proposal.transitions[0], item=malformed),)))
        assert outcome.reason == "unauthorized state kind"
        assert len(store.transitions()) == 1


def test_temporal_conflict_and_unauthorized_operation_are_rejected(tmp_path):
    with Store(tmp_path / "temporal.sqlite") as store:
        seed(store)
        incoming = Event("bad-time", EventType.USER_MESSAGE, "Change it", NOW)
        store.ingest(incoming)
        candidate = row_to_item(store.state_item("preference-work"))
        proposal = ProposalBuilder().build(incoming, candidate, result(Relationship.SUPPORTS))
        invalid = replace(proposal.transitions[0].item,
                          valid_from=NOW, valid_until=NOW - timedelta(days=1))
        outcome = TransitionValidator(store).validate_and_commit(
            replace(proposal, transitions=(replace(proposal.transitions[0], item=invalid),)))
        assert outcome.reason == "invalid temporal interval"

    with Store(tmp_path / "operation.sqlite") as store:
        seed(store)
        incoming = Event("bad-op", EventType.USER_MESSAGE, "Change it", NOW)
        store.ingest(incoming)
        candidate = row_to_item(store.state_item("preference-work"))
        proposal = ProposalBuilder().build(incoming, candidate, result(Relationship.SUPPORTS))
        outcome = TransitionValidator(store).validate_and_commit(
            replace(proposal, transitions=(replace(proposal.transitions[0], operation="delete"),)))
        assert outcome.reason == "unauthorized transition operation"


def test_no_candidates_and_validator_commit_failure_do_not_mutate_state(tmp_path):
    with Store(tmp_path / "none.sqlite") as store:
        seed(store)
        incoming = Event("no-candidate", EventType.USER_MESSAGE, "Change it", NOW, {})
        pipeline = TransitionPipeline(
            store, ExplicitCandidateSelector(),
            ManualClassifier({incoming.event_id: result(Relationship.SUPPORTS)}),
            TransitionValidator(store),
        )
        outcome = pipeline.process(incoming)
        assert outcome.reason == "no candidate state item"
        assert len(store.transitions()) == 1

    with Store(tmp_path / "failure.sqlite") as store:
        seed(store)
        incoming = Event("commit-failure", EventType.USER_MESSAGE, "Replace it", NOW)
        store.ingest(incoming)
        candidate = row_to_item(store.state_item("preference-work"))
        proposal = ProposalBuilder().build(incoming, candidate, result(Relationship.SUPERSEDES))
        before = store.canonical_digest()
        outcome = TransitionValidator(store).validate_and_commit(
            proposal, fail_during_commit=True)
        assert outcome.outcome == "rejected" and outcome.reason == "RuntimeError"
        assert store.canonical_digest() == before
        assert store.proposals()[-1]["outcome"] == "rejected"


def test_complete_path_survives_restart_and_classifier_is_replaceable(tmp_path):
    path = tmp_path / "restart.sqlite"
    case = next(case for case in FIXTURES if case["relationship"] == "narrows_scope")
    with Store(path) as store:
        seed(store)
        pipeline = TransitionPipeline(
            store, ExplicitCandidateSelector(),
            FixedClassifier(Relationship.NARROWS_SCOPE),
            TransitionValidator(store),
        )
        assert pipeline.process(event(case)).accepted
        digest = store.canonical_digest()
    with Store(path) as recovered:
        assert recovered.canonical_digest() == digest
        assert len(recovered.active()) == 2
        assert recovered.proposals()[0]["outcome"] == "accepted"
