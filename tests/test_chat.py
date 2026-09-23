from datetime import datetime, timezone

from lifetime_ai.chat import ChatRuntime, RuleBasedLocalExtractor
from lifetime_ai.store import SourceError, Store
from lifetime_ai.types import Transition
import pytest


NOW = datetime(2026, 9, 23, 12, 0, tzinfo=timezone.utc)


def test_local_chat_capture_restart_citation_correction_and_deletion(tmp_path):
    path = tmp_path / "chat.sqlite"
    with Store(path) as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        captured = chat.send("I prefer concise answers", NOW, "chat-1")
        assert captured.outcome == "accepted"
        assert "[source:chat-1]" in captured.text
        item_id = captured.citations[0].item_id

        answered = chat.ask("What do I prefer?")
        assert answered.outcome == "answered"
        assert answered.citations[0].source_event_id == "chat-1"

        corrected = chat.correct(item_id, "I prefer detailed answers", NOW, "chat-2")
        assert corrected.outcome == "accepted"
        assert chat.ask("What do I prefer?").citations[0].source_event_id == "chat-2"

        assert chat.delete_source("chat-2") is True
        assert chat.ask("What do I prefer?").outcome == "uncertain"
        assert store.state_item(item_id)["status"] == "revoked"
        assert store.state_item(item_id)["valid_until"] == store.event("chat-2")["deleted_at"]
        assert store.rebuild_state() == store.canonical_digest()

    with Store(path) as recovered:
        assert recovered.retrieve("What do I prefer?") == []
        assert recovered.event("chat-2")["deleted_at"] is not None


def test_chat_abstains_without_claim_and_does_not_mutate_state(tmp_path):
    with Store(tmp_path / "chat.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        response = chat.send("Thanks, that helps", NOW, "chat-irrelevant")
        assert response.outcome == "abstained"
        assert store.active() == []
        assert store.proposals()[0]["outcome"] == "abstained"


def test_deleted_source_is_not_retrievable_even_if_other_state_exists(tmp_path):
    with Store(tmp_path / "chat.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        first = chat.send("I prefer concise answers", NOW, "chat-1")
        chat.send("I prefer detailed answers", NOW, "chat-2")
        assert chat.delete_source(first.citations[0].source_event_id)
        response = chat.ask("What do I prefer?")
        assert response.outcome == "answered"
        assert {citation.source_event_id for citation in response.citations} == {"chat-2"}


def test_deleted_source_cannot_authorize_a_new_transition(tmp_path):
    with Store(tmp_path / "chat.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        captured = chat.send("I prefer concise answers.", NOW, "e1")
        item = store.state_item(captured.citations[0].item_id)
        chat.delete_source("e1")
        from lifetime_ai.pipeline import row_to_item
        with pytest.raises(SourceError, match="was deleted"):
            store.apply(Transition("late", "e1", row_to_item(item)))
        assert store.rebuild_state() == store.canonical_digest()
