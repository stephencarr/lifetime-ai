from __future__ import annotations
import sqlite3
from pathlib import Path
from .types import Event, EventType, StateItem, StateKind, StateStatus, Transition


SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
 event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, text TEXT NOT NULL,
 occurred_at TEXT NOT NULL, metadata TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS state_items (
 item_id TEXT PRIMARY KEY, kind TEXT NOT NULL, proposition TEXT NOT NULL,
 source_event_id TEXT NOT NULL REFERENCES events(event_id), source_type TEXT NOT NULL,
 occurred_at TEXT NOT NULL, status TEXT NOT NULL, confidence REAL NOT NULL,
 sensitivity TEXT NOT NULL, valid_from TEXT, valid_until TEXT);
CREATE TABLE IF NOT EXISTS transitions (
 transition_id TEXT PRIMARY KEY, event_id TEXT NOT NULL REFERENCES events(event_id),
 item_id TEXT NOT NULL REFERENCES state_items(item_id), operation TEXT NOT NULL,
 reason TEXT NOT NULL, applied_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_transitions_event ON transitions(event_id);
"""


class Store:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    def ingest(self, event: Event) -> bool:
        cur = self.db.execute("INSERT OR IGNORE INTO events VALUES (?,?,?,?,?)",
            (event.event_id, event.event_type, event.text, event.occurred_at.isoformat(), event.payload()))
        self.db.commit()
        return cur.rowcount == 1

    def apply(self, transition: Transition) -> bool:
        """Atomically record a source-linked state change and its audit record."""
        with self.db:
            if not self.db.execute("SELECT 1 FROM events WHERE event_id=?", (transition.event_id,)).fetchone():
                raise ValueError("transition source event does not exist")
            if self.db.execute("SELECT 1 FROM transitions WHERE transition_id=?", (transition.transition_id,)).fetchone():
                return False
            i = transition.item
            self.db.execute("INSERT OR REPLACE INTO state_items VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                i.item_id, i.kind, i.proposition, i.source_event_id, i.source_type,
                i.occurred_at.isoformat(), i.status, i.confidence, i.sensitivity,
                i.valid_from.isoformat() if i.valid_from else None,
                i.valid_until.isoformat() if i.valid_until else None))
            self.db.execute("INSERT INTO transitions VALUES (?,?,?,?,?,datetime('now'))",
                (transition.transition_id, transition.event_id, i.item_id, transition.operation, transition.reason))
        return True

    def active(self, kind: StateKind | None = None) -> list[sqlite3.Row]:
        q, args = "SELECT * FROM state_items WHERE status=?", [StateStatus.ACTIVE]
        if kind: q += " AND kind=?"; args.append(kind)
        return list(self.db.execute(q + " ORDER BY occurred_at, item_id", args))

    def has_transition_for_event(self, event_id: str) -> bool:
        return self.db.execute("SELECT 1 FROM transitions WHERE event_id=?", (event_id,)).fetchone() is not None

    def replay(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM transitions ORDER BY applied_at, transition_id"))
