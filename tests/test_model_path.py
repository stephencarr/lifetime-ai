import json
import sqlite3
from datetime import datetime, timezone

import pytest

from lifetime_ai.local_models import LocalChatModel, ModelResult, ModelUnavailable
from lifetime_ai.model_chat import ModelChatRuntime
from lifetime_ai.model_retrieval import ModelRetriever
from lifetime_ai.store import MIGRATION_1, MIGRATION_2, MIGRATION_3, MIGRATION_4, Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition


NOW = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


class FixedEmbedder:
    def embed(self, texts):
        return [[1.0] + [0.0] * 383 for _ in texts]


def test_model_index_is_rebuilt_from_live_canonical_state(tmp_path):
    path = tmp_path / "model.sqlite"
    with Store(path) as store:
        event = Event("source", EventType.USER_MESSAGE, "I prefer quiet mornings.", NOW)
        store.ingest(event)
        item = StateItem("item", StateKind.PREFERENCE, "I prefer quiet mornings.",
                         event.event_id, event.event_type, NOW)
        annotation = {"actor": "user", "relation": "preference", "value": "quiet mornings",
                      "polarity": "positive", "scope": "general", "source_quote": event.text,
                      "source_start": 0, "source_end": len(event.text),
                      "embedding": [1.0] + [0.0] * 383, "generator_model": "test-model",
                      "verifier_result": {"verdict": "entailed"}}
        store.commit_model_claim("proposal", event.event_id,
                                 Transition("transition", event.event_id, item), annotation)
        stored = store.model_row("item")
        assert stored["embedding_format"] == "f16le-v1"
        assert len(stored["embedding"]) == 768
        assert "embedding_sha256" in store.proposals()[0]["proposal_payload"]
        assert '"embedding":' not in store.proposals()[0]["proposal_payload"]
        assert store.model_lexical_candidates("quiet mornings") == ["item"]
        assert store.model_active_item_ids_for_source("source") == ["item"]
        assert store.model_active_item_ids_for_source("other") == []
        assert [row["item_id"] for row in ModelRetriever(store, FixedEmbedder()).candidates(
            "sunrise")] == ["item"]
        assert store.rebuild_state() == store.canonical_digest()
    with Store(path) as store:
        assert [row["item_id"] for row in ModelRetriever(store, FixedEmbedder()).candidates(
            "sunrise")] == ["item"]
        store.delete_event("source")
        assert store.model_active_item_ids_for_source("source") == []
        assert store.model_lexical_candidates("quiet mornings") == []
        assert ModelRetriever(store, FixedEmbedder()).candidates("sunrise") == []


def test_legacy_json_embedding_rebuilds_after_migration(tmp_path):
    path = tmp_path / "legacy.sqlite"
    with Store(path) as store:
        event = Event("source", EventType.USER_MESSAGE, "I prefer tea.", NOW)
        store.ingest(event)
        item = StateItem("item", StateKind.PREFERENCE, "prefer tea",
                         event.event_id, event.event_type, NOW)
        vector = [1.0] + [0.0] * 383
        annotation = {"actor": "user", "relation": "preference", "value": "tea",
                      "polarity": "positive", "scope": "general", "source_quote": event.text,
                      "source_start": 0, "source_end": len(event.text),
                      "embedding": vector, "generator_model": "test-model",
                      "verifier_result": {"verdict": "entailed"}}
        store.commit_model_claim("proposal", event.event_id,
                                 Transition("transition", event.event_id, item), annotation)
        store.db.execute("UPDATE model_claims SET embedding=?, embedding_format='json-v1'",
                         (json.dumps(vector),))
        store.db.commit()
    with Store(path) as store:
        assert [row["item_id"] for row in ModelRetriever(store, FixedEmbedder()).candidates(
            "drink")] == ["item"]


def test_schema_four_model_claims_upgrade_to_five(tmp_path):
    path = tmp_path / "upgrade.sqlite"
    with sqlite3.connect(path) as db:
        for migration in (MIGRATION_1, MIGRATION_2, MIGRATION_3, MIGRATION_4):
            db.executescript(migration)
        assert db.execute("PRAGMA user_version").fetchone()[0] == 4
    with Store(path) as store:
        assert store.schema_version == 5
        columns = {row[1] for row in store.db.execute("PRAGMA table_info(model_claims)")}
        assert "embedding_format" in columns


def test_model_client_rejects_non_loopback_destination():
    with pytest.raises(ValueError, match="loopback"):
        LocalChatModel("https://example.com", "some-model")


class UnsupportedModel:
    expected_model_id = "fake-model"

    def structured(self, system, user, schema, *, name, max_tokens):
        if name == "m5_claims":
            return ModelResult({"claims": [{"kind": "preference",
                "proposition": "The user prefers tea.", "actor": "user", "value": "tea",
                "polarity": "positive", "scope_anchor": "", "durability": "ongoing",
                "source_quote": "Maya prefers tea."}]}, 1, 1)
        if name == "m5_source_support":
            return ModelResult({"verdict": "not_entailed", "supporting_quote": "Maya prefers tea.",
                                "reason": "third-party actor"}, 1, 1)
        raise AssertionError(name)


def test_model_source_rejection_cannot_mutate_state(tmp_path):
    with Store(tmp_path / "model.sqlite") as store:
        runtime = ModelChatRuntime(store, UnsupportedModel(), FixedEmbedder())
        response = runtime.send("Maya prefers tea.", NOW, "third-party")
        assert response.outcome == "abstained"
        assert store.active() == []
        assert store.proposals()[0]["outcome"] == "abstained"


class UnavailableModel:
    expected_model_id = "missing-model"

    def structured(self, *args, **kwargs):
        raise ModelUnavailable("synthetic model outage")


def test_model_outage_abstains_without_rule_fallback(tmp_path):
    with Store(tmp_path / "model.sqlite") as store:
        runtime = ModelChatRuntime(store, UnavailableModel(), FixedEmbedder())
        response = runtime.send("I prefer tea.", NOW, "outage")
        assert response.outcome == "abstained"
        assert store.active() == []
        assert store.proposals()[0]["outcome"] == "abstained"
        assert runtime.ask("What do I prefer?").outcome == "uncertain"


class EpisodicModel:
    expected_model_id = "fake-model"

    def structured(self, system, user, schema, *, name, max_tokens):
        if name == "m5_claims":
            return ModelResult({"claims": [{"kind": "fact",
                "proposition": "The user enjoyed rock climbing",
                "actor": "user", "value": "rock climbing", "polarity": "positive",
                "scope_anchor": "last Saturday", "durability": "episodic",
                "source_quote": "I enjoyed rock climbing last Saturday."}]}, 1, 1)
        raise AssertionError("episodic state must be rejected before support calls")


def test_episodic_event_does_not_become_durable_state(tmp_path):
    with Store(tmp_path / "model.sqlite") as store:
        runtime = ModelChatRuntime(store, EpisodicModel(), FixedEmbedder())
        response = runtime.send("I enjoyed rock climbing last Saturday.", NOW, "episode")
        assert response.outcome == "abstained"
        assert store.active() == []
        assert "episodic" in store.proposals()[0]["reason"]
