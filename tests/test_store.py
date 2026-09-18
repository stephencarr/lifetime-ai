from datetime import datetime, timezone
import sqlite3
from lifetime_ai.store import Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition

def event(eid="e1"):
    return Event(eid, EventType.USER_MESSAGE, "I prefer concise answers", datetime(2026, 9, 17, tzinfo=timezone.utc))

def item(eid="e1", iid="p1"):
    e = event(eid)
    return StateItem(iid, StateKind.PREFERENCE, e.text, e.event_id, e.event_type, e.occurred_at)

def test_idempotent_ingestion_and_atomic_transition(tmp_path):
    s = Store(tmp_path / "state.sqlite")
    assert s.ingest(event()) and not s.ingest(event())
    assert s.apply(Transition("t1", "e1", item(), reason="explicit user statement"))
    assert not s.apply(Transition("t1", "e1", item(), reason="duplicate"))
    assert len(s.active()) == 1 and s.has_transition_for_event("e1")

def test_missing_source_rejected_without_partial_write(tmp_path):
    s = Store(tmp_path / "state.sqlite")
    try:
        s.apply(Transition("t1", "missing", item(), reason="bad"))
    except ValueError:
        pass
    else: raise AssertionError("expected missing source rejection")
    assert s.active() == [] and s.replay() == []

def test_restart_recovery(tmp_path):
    path = tmp_path / "state.sqlite"
    s = Store(path); s.ingest(event()); s.apply(Transition("t1", "e1", item())); s.close()
    s2 = Store(path)
    assert [r["proposition"] for r in s2.active()] == ["I prefer concise answers"]
    assert len(s2.replay()) == 1

