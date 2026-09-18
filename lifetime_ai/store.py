from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .types import Event, StateItem, StateKind, StateStatus, Transition

SCHEMA_VERSION = 2

MIGRATION_1 = """
CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
CREATE TABLE events (
 event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, text TEXT NOT NULL,
 occurred_at TEXT NOT NULL, metadata TEXT NOT NULL, payload_hash TEXT NOT NULL);
CREATE TABLE transitions (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, transition_id TEXT NOT NULL UNIQUE,
 event_id TEXT NOT NULL REFERENCES events(event_id), item_id TEXT NOT NULL,
 operation TEXT NOT NULL, reason TEXT NOT NULL, item_snapshot TEXT NOT NULL,
 payload_hash TEXT NOT NULL, applied_at TEXT NOT NULL);
CREATE TABLE state_items (
 item_id TEXT PRIMARY KEY, kind TEXT NOT NULL, proposition TEXT NOT NULL,
 source_event_id TEXT NOT NULL REFERENCES events(event_id), source_type TEXT NOT NULL,
 occurred_at TEXT NOT NULL, status TEXT NOT NULL, confidence REAL NOT NULL,
 sensitivity TEXT NOT NULL, valid_from TEXT, valid_until TEXT,
 last_transition_id TEXT NOT NULL REFERENCES transitions(transition_id));
CREATE TABLE audit_entries (
 audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
 transition_id TEXT NOT NULL UNIQUE REFERENCES transitions(transition_id),
 event_id TEXT NOT NULL REFERENCES events(event_id),
 outcome TEXT NOT NULL CHECK(outcome = 'accepted'), detail TEXT NOT NULL);
CREATE INDEX idx_transitions_event ON transitions(event_id);
CREATE INDEX idx_state_source ON state_items(source_event_id);
INSERT INTO schema_migrations(version, applied_at) VALUES (1, datetime('now'));
PRAGMA user_version = 1;
"""

MIGRATION_2 = """
CREATE TABLE proposal_records (
 proposal_id TEXT PRIMARY KEY,
 event_id TEXT NOT NULL REFERENCES events(event_id),
 candidate_item_id TEXT,
 relationship TEXT NOT NULL,
 proposal_payload TEXT NOT NULL,
 outcome TEXT NOT NULL CHECK(outcome IN ('accepted','rejected','abstained','noop')),
 reason TEXT NOT NULL,
 created_at TEXT NOT NULL
);
CREATE INDEX idx_proposals_event ON proposal_records(event_id);
INSERT INTO schema_migrations(version, applied_at) VALUES (2, datetime('now'));
PRAGMA user_version = 2;
"""


class IdentifierCollisionError(ValueError):
    """An identifier was reused for content other than its original payload."""


class SourceError(ValueError):
    """A transition lacks a valid and internally consistent source event."""


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()


def _event_record(event: Event) -> dict[str, object]:
    return {"event_id": event.event_id, "event_type": event.event_type.value,
            "text": event.text, "occurred_at": event.occurred_at.isoformat(),
            "metadata": event.metadata or {}}


def _item_record(item: StateItem) -> dict[str, object]:
    return {"item_id": item.item_id, "kind": item.kind.value,
            "proposition": item.proposition, "source_event_id": item.source_event_id,
            "source_type": item.source_type.value, "occurred_at": item.occurred_at.isoformat(),
            "status": item.status.value, "confidence": item.confidence,
            "sensitivity": item.sensitivity,
            "valid_from": item.valid_from.isoformat() if item.valid_from else None,
            "valid_until": item.valid_until.isoformat() if item.valid_until else None}


def _transition_record(transition: Transition) -> dict[str, object]:
    return {"transition_id": transition.transition_id, "event_id": transition.event_id,
            "operation": transition.operation, "reason": transition.reason,
            "item": _item_record(transition.item)}


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        if self.db.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            raise RuntimeError("SQLite foreign-key enforcement could not be enabled")
        self._migrate()

    def _migrate(self) -> None:
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        if version == 0:
            self.db.executescript(MIGRATION_1)
            version = 1
        if version == 1:
            self.db.executescript(MIGRATION_2)
            version = 2
        if version != SCHEMA_VERSION:
            raise RuntimeError(f"unsupported schema version {version}")

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @contextmanager
    def _transaction(self) -> Iterator[None]:
        try:
            self.db.execute("BEGIN IMMEDIATE")
            yield
        except BaseException:
            self.db.rollback()
            raise
        else:
            self.db.commit()

    def _ingest_uncommitted(self, event: Event) -> bool:
        digest = _hash(_canonical(_event_record(event)))
        existing = self.db.execute("SELECT payload_hash FROM events WHERE event_id=?",
                                   (event.event_id,)).fetchone()
        if existing:
            if existing["payload_hash"] != digest:
                raise IdentifierCollisionError(f"event identifier collision: {event.event_id}")
            return False
        self.db.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
                        (event.event_id, event.event_type.value, event.text,
                         event.occurred_at.isoformat(), _canonical(event.metadata or {}), digest))
        return True

    def ingest(self, event: Event) -> bool:
        with self._transaction():
            return self._ingest_uncommitted(event)

    def _apply_uncommitted(self, transition: Transition, fail_after_state: bool = False) -> bool:
        digest = _hash(_canonical(_transition_record(transition)))
        existing = self.db.execute("SELECT payload_hash FROM transitions WHERE transition_id=?",
                                   (transition.transition_id,)).fetchone()
        if existing:
            if existing["payload_hash"] != digest:
                raise IdentifierCollisionError(
                    f"transition identifier collision: {transition.transition_id}")
            return False
        source = self.db.execute("SELECT event_type FROM events WHERE event_id=?",
                                 (transition.event_id,)).fetchone()
        if not source:
            raise SourceError("transition source event does not exist")
        item = transition.item
        if item.source_event_id != transition.event_id:
            raise SourceError("state item and transition source identifiers differ")
        if item.source_type.value != source["event_type"]:
            raise SourceError("state item source type differs from ledger event")
        if transition.operation != "upsert":
            raise ValueError(f"unsupported operation: {transition.operation}")
        snapshot = _canonical(_item_record(item))
        self.db.execute(
            "INSERT INTO transitions(transition_id,event_id,item_id,operation,reason,item_snapshot,payload_hash,applied_at) "
            "VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (transition.transition_id, transition.event_id, item.item_id, transition.operation,
             transition.reason, snapshot, digest))
        self._write_state(item, transition.transition_id)
        if fail_after_state:
            raise RuntimeError("injected failure after state write")
        self.db.execute(
            "INSERT INTO audit_entries(transition_id,event_id,outcome,detail) VALUES (?,?,?,?)",
            (transition.transition_id, transition.event_id, "accepted", transition.reason))
        return True

    def _write_state(self, item: StateItem, transition_id: str) -> None:
        self.db.execute(
            "INSERT INTO state_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(item_id) DO UPDATE SET "
            "kind=excluded.kind,proposition=excluded.proposition,source_event_id=excluded.source_event_id,"
            "source_type=excluded.source_type,occurred_at=excluded.occurred_at,status=excluded.status,"
            "confidence=excluded.confidence,sensitivity=excluded.sensitivity,valid_from=excluded.valid_from,"
            "valid_until=excluded.valid_until,last_transition_id=excluded.last_transition_id",
            (item.item_id, item.kind.value, item.proposition, item.source_event_id,
             item.source_type.value, item.occurred_at.isoformat(), item.status.value,
             item.confidence, item.sensitivity,
             item.valid_from.isoformat() if item.valid_from else None,
             item.valid_until.isoformat() if item.valid_until else None, transition_id))

    def apply(self, transition: Transition, *, fail_after_state: bool = False) -> bool:
        with self._transaction():
            return self._apply_uncommitted(transition, fail_after_state)

    def record_proposal(self, proposal_id: str, event_id: str,
                        candidate_item_id: str | None, relationship: str,
                        payload: str, outcome: str, reason: str) -> None:
        with self._transaction():
            self._record_proposal_uncommitted(
                proposal_id, event_id, candidate_item_id, relationship,
                payload, outcome, reason)

    def _record_proposal_uncommitted(self, proposal_id: str, event_id: str,
                                     candidate_item_id: str | None, relationship: str,
                                     payload: str, outcome: str, reason: str) -> None:
        existing = self.db.execute(
            "SELECT proposal_payload,outcome,reason FROM proposal_records WHERE proposal_id=?",
            (proposal_id,)).fetchone()
        if existing:
            if (existing["proposal_payload"], existing["outcome"], existing["reason"]) != (
                    payload, outcome, reason):
                raise IdentifierCollisionError(f"proposal identifier collision: {proposal_id}")
            return
        self.db.execute(
            "INSERT INTO proposal_records VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (proposal_id, event_id, candidate_item_id, relationship, payload, outcome, reason))

    def commit_proposal(self, proposal_id: str, event_id: str,
                        candidate_item_id: str | None, relationship: str,
                        payload: str, transitions: tuple[Transition, ...],
                        *, fail_after_first: bool = False) -> None:
        with self._transaction():
            for index, transition in enumerate(transitions):
                self._apply_uncommitted(transition)
                if fail_after_first and index == 0:
                    raise RuntimeError("injected validator commit failure")
            self._record_proposal_uncommitted(
                proposal_id, event_id, candidate_item_id, relationship,
                payload, "accepted", "validated")

    def ingest_and_apply(self, event: Event, transition: Transition, *,
                         fail_after_state: bool = False) -> tuple[bool, bool]:
        if event.event_id != transition.event_id:
            raise SourceError("event and transition identifiers differ")
        with self._transaction():
            ingested = self._ingest_uncommitted(event)
            applied = self._apply_uncommitted(transition, fail_after_state)
            return ingested, applied

    def active(self, kind: StateKind | None = None) -> list[sqlite3.Row]:
        query, args = "SELECT * FROM state_items WHERE status=?", [StateStatus.ACTIVE.value]
        if kind:
            query += " AND kind=?"
            args.append(kind.value)
        return list(self.db.execute(query + " ORDER BY occurred_at,item_id", args))

    def state_item(self, item_id: str) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM state_items WHERE item_id=?", (item_id,)).fetchone()

    def event_exists(self, event_id: str) -> bool:
        return self.db.execute("SELECT 1 FROM events WHERE event_id=?", (event_id,)).fetchone() is not None

    def proposals(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM proposal_records ORDER BY created_at,proposal_id"))

    def transitions(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM transitions ORDER BY sequence"))

    def audit_entries(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM audit_entries ORDER BY audit_id"))

    def has_transition_for_event(self, event_id: str) -> bool:
        return self.db.execute("SELECT 1 FROM transitions WHERE event_id=?",
                               (event_id,)).fetchone() is not None

    def canonical_digest(self) -> str:
        rows = [dict(row) for row in self.db.execute("SELECT * FROM state_items ORDER BY item_id")]
        provenance = [dict(row) for row in self.db.execute(
            "SELECT transition_id,event_id,item_id,operation,reason,item_snapshot,payload_hash "
            "FROM transitions ORDER BY sequence")]
        return _hash(_canonical({"state": rows, "provenance": provenance}))

    def rebuild_state(self) -> str:
        """Deterministically rebuild derived state from accepted transition snapshots."""
        with self._transaction():
            self.db.execute("DELETE FROM state_items")
            records = self.db.execute(
                "SELECT transition_id,item_snapshot FROM transitions ORDER BY sequence").fetchall()
            for row in records:
                data = json.loads(row["item_snapshot"])
                self.db.execute(
                    "INSERT INTO state_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?) "
                    "ON CONFLICT(item_id) DO UPDATE SET "
                    "kind=excluded.kind,proposition=excluded.proposition,source_event_id=excluded.source_event_id,"
                    "source_type=excluded.source_type,occurred_at=excluded.occurred_at,status=excluded.status,"
                    "confidence=excluded.confidence,sensitivity=excluded.sensitivity,valid_from=excluded.valid_from,"
                    "valid_until=excluded.valid_until,last_transition_id=excluded.last_transition_id",
                    (data["item_id"], data["kind"], data["proposition"], data["source_event_id"],
                     data["source_type"], data["occurred_at"], data["status"], data["confidence"],
                     data["sensitivity"], data["valid_from"], data["valid_until"],
                     row["transition_id"]))
        return self.canonical_digest()

    def inspect(self) -> list[dict[str, object]]:
        return [dict(row) for row in self.db.execute(
            "SELECT s.item_id,s.kind,s.proposition,s.status,s.last_transition_id,"
            "e.event_id AS source_event_id,e.event_type AS source_event_type,e.text AS source_text,"
            "t.reason AS transition_reason FROM state_items s "
            "JOIN events e ON e.event_id=s.source_event_id "
            "JOIN transitions t ON t.transition_id=s.last_transition_id ORDER BY s.item_id")]

    @property
    def schema_version(self) -> int:
        return self.db.execute("PRAGMA user_version").fetchone()[0]
