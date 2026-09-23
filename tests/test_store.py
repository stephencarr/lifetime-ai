from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from dataclasses import replace
from datetime import datetime, timezone

import pytest

from lifetime_ai.store import IdentifierCollisionError, SourceError, Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition


NOW = datetime(2026, 9, 17, tzinfo=timezone.utc)


def event(eid: str = "e1", text: str = "I prefer concise answers") -> Event:
    return Event(eid, EventType.USER_MESSAGE, text, NOW, {"channel": "test"})


def item(eid: str = "e1", iid: str = "p1", proposition: str | None = None) -> StateItem:
    source = event(eid)
    return StateItem(iid, StateKind.PREFERENCE, proposition or source.text,
                     source.event_id, source.event_type, source.occurred_at)


def transition(tid: str = "t1", eid: str = "e1", iid: str = "p1",
               proposition: str | None = None) -> Transition:
    return Transition(tid, eid, item(eid, iid, proposition), reason="explicit user statement")


def counts(store: Store) -> tuple[int, int, int, int]:
    tables = ("events", "transitions", "state_items", "audit_entries")
    return tuple(store.db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                 for table in tables)


def orphan_counts(store: Store) -> tuple[int, int]:
    transitions = store.db.execute(
        "SELECT count(*) FROM transitions t LEFT JOIN events e ON e.event_id=t.event_id "
        "WHERE e.event_id IS NULL"
    ).fetchone()[0]
    items = store.db.execute(
        "SELECT count(*) FROM state_items s LEFT JOIN events e ON e.event_id=s.source_event_id "
        "LEFT JOIN transitions t ON t.transition_id=s.last_transition_id "
        "WHERE e.event_id IS NULL OR t.transition_id IS NULL"
    ).fetchone()[0]
    return transitions, items


def test_s1_identical_event_replay_is_noop(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        assert store.ingest(event()) is True
        assert store.ingest(event()) is False
        assert counts(store) == (1, 0, 0, 0)


def test_s2_event_identifier_collision_is_rejected(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        store.ingest(event())
        with pytest.raises(IdentifierCollisionError, match="event identifier collision"):
            store.ingest(event(text="I prefer detailed answers"))
        assert store.db.execute("SELECT text FROM events").fetchone()[0] == event().text


def test_s3_missing_or_inconsistent_source_leaves_no_residue(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        with pytest.raises(SourceError, match="does not exist"):
            store.apply(transition())
        assert counts(store) == (0, 0, 0, 0)
        store.ingest(event())
        bad_item = replace(item(), source_event_id="different")
        with pytest.raises(SourceError, match="identifiers differ"):
            store.apply(Transition("t1", "e1", bad_item))
        assert counts(store) == (1, 0, 0, 0)


def test_s4_atomic_rollback_covers_event_transition_state_and_audit(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        with pytest.raises(RuntimeError, match="injected failure"):
            store.ingest_and_apply(event(), transition(), fail_after_state=True)
        assert counts(store) == (0, 0, 0, 0)


def test_s5_transition_replay_and_collision(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        store.ingest(event())
        original = transition()
        assert store.apply(original) is True
        assert store.apply(original) is False
        with pytest.raises(IdentifierCollisionError, match="transition identifier collision"):
            store.apply(transition(proposition="I now prefer detailed answers"))
        assert counts(store) == (1, 1, 1, 1)
        assert store.active()[0]["proposition"] == event().text


def test_s6_restart_in_fresh_process_preserves_digest_and_provenance(tmp_path):
    path = tmp_path / "state.sqlite"
    with Store(path) as store:
        store.ingest_and_apply(event(), transition())
        before = store.canonical_digest()
    code = (
        "import json,sys; from lifetime_ai.store import Store; "
        "s=Store(sys.argv[1]); print(json.dumps({'digest':s.canonical_digest(),'items':s.inspect()})); s.close()"
    )
    result = subprocess.run([sys.executable, "-c", code, str(path)], check=True,
                            capture_output=True, text=True)
    recovered = json.loads(result.stdout)
    assert recovered["digest"] == before
    assert recovered["items"][0]["source_event_id"] == "e1"
    assert recovered["items"][0]["last_transition_id"] == "t1"


def test_s7_every_store_connection_enforces_foreign_keys(tmp_path):
    path = tmp_path / "state.sqlite"
    for _ in range(2):
        with Store(path) as store:
            assert store.db.execute("PRAGMA foreign_keys").fetchone()[0] == 1
            with pytest.raises(sqlite3.IntegrityError):
                store.db.execute(
                    "INSERT INTO transitions(transition_id,event_id,item_id,operation,reason,item_snapshot,payload_hash,applied_at) "
                    "VALUES ('bad','missing','p1','upsert','','{}','x',datetime('now'))"
                )
            store.db.rollback()


def test_s8_deterministic_replay_matches_digest_repeatedly(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        store.ingest_and_apply(event(), transition())
        revised_event = event("e2", "For research, I prefer detailed answers")
        revised_item = StateItem("p1", StateKind.PREFERENCE, revised_event.text,
                                 revised_event.event_id, revised_event.event_type,
                                 revised_event.occurred_at)
        store.ingest_and_apply(
            revised_event, Transition("t2", "e2", revised_item, reason="scope revision"))
        expected = store.canonical_digest()
        assert store.rebuild_state() == expected
        assert store.rebuild_state() == expected
        assert counts(store) == (2, 2, 1, 2)
        assert orphan_counts(store) == (0, 0)


def test_schema_version_and_inspector_source_chain(tmp_path):
    with Store(tmp_path / "state.sqlite") as store:
        store.ingest_and_apply(event(), transition())
        assert store.schema_version == 5
        assert [row[0] for row in store.db.execute(
            "SELECT version FROM schema_migrations ORDER BY version")] == [1, 2, 3, 4, 5]
        assert store.inspect() == [{
            "item_id": "p1", "kind": "preference", "proposition": event().text,
            "status": "active", "last_transition_id": "t1", "source_event_id": "e1",
            "source_event_type": "user_message", "source_text": event().text,
            "transition_reason": "explicit user statement",
        }]
