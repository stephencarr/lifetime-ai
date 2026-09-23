from datetime import datetime, timezone

import pytest

from lifetime_ai.chat import ChatRuntime, RuleBasedLocalExtractor
from lifetime_ai.m5_answerability_preflight import load_frozen
from lifetime_ai.store import RetrievalIncompleteError, Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition


NOW = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


def test_frozen_development_instrument_has_declared_labels():
    cases, criteria, freeze = load_frozen()
    questions = [q for scenario in cases["scenarios"] for q in scenario["questions"]]
    assert len(questions) == freeze["question_count"] == criteria["minimum_questions"] == 48
    assert all({"expected_candidate_sources", "expected_outcome", "expected_citations",
                "acceptable_abstention", "family"} <= q.keys() for q in questions)


def test_retrieval_is_complete_within_limit_and_fails_closed_at_capacity(tmp_path):
    with Store(tmp_path / "answer.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        chat.send("I prefer tea.", NOW, "tea")
        chat.send("I prefer dark mode.", NOW, "display")
        assert {r["source_event_id"] for r in store.retrieve("How should my screen look?")} == {
            "tea", "display"}
        with pytest.raises(RetrievalIncompleteError):
            store.retrieve("What do I prefer?", limit=1)


def test_support_check_rejects_related_but_unentailed_question(tmp_path):
    with Store(tmp_path / "answer.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        chat.send("I prefer short answers.", NOW, "short")
        assert chat.ask("Did I prefer short answers last year?").outcome == "uncertain"
        assert chat.ask("What do I prefer for answers?").outcome == "answered"
        assert chat.ask("What programming language do I use?").outcome == "uncertain"


def test_compatible_claims_are_not_called_conflict(tmp_path):
    with Store(tmp_path / "answer.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        chat.send("I prefer tea.", NOW, "tea")
        chat.send("I prefer dark mode.", NOW, "display")
        response = chat.ask("What are my preferences?")
        assert response.outcome == "answered"
        assert {c.source_event_id for c in response.citations} == {"tea", "display"}


def test_contextual_preference_does_not_answer_general_question(tmp_path):
    with Store(tmp_path / "answer.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        chat.send("I prefer coffee after lunch.", NOW, "lunch")
        assert chat.ask("What do I prefer?").outcome == "uncertain"
        response = chat.ask("What do I prefer after lunch?")
        assert response.outcome == "answered"
        assert [c.source_event_id for c in response.citations] == ["lunch"]


def test_manually_derived_observation_is_not_treated_as_direct_user_witness(tmp_path):
    with Store(tmp_path / "answer.sqlite") as store:
        event = Event("reviewed-email", EventType.OBSERVATION,
                      "An email mentions tea in an outing.", NOW)
        item = StateItem("item", StateKind.PREFERENCE, "I prefer tea.",
                         event.event_id, event.event_type, NOW)
        store.ingest_and_apply(event, Transition("transition", event.event_id, item))
        response = ChatRuntime(store, RuleBasedLocalExtractor()).ask("Do I prefer tea?")
        assert response.outcome == "uncertain"
        assert response.citations == ()
