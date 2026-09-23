from __future__ import annotations

import json
import hashlib
import re
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable, Protocol


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    excerpt: str
    occurred_at: str
    context: str


@dataclass(frozen=True)
class Suggestion:
    suggestion_id: str
    kind: str
    proposition: str
    source_id: str
    rationale: str
    uncertainty: str


class SuggestionAdapter(Protocol):
    name: str

    def suggest(self, sources: Iterable[Source]) -> list[Suggestion]: ...


class DeterministicDemoAdapter:
    """High-precision, abstaining local rules for the no-weights UAT mode."""

    name = "deterministic demo mode (local; no model weights)"

    _patterns = (
        ("preference", re.compile(r"\b(?:i|we|the project)\s+(?:really\s+)?(?:prefer(?:s|red)?|would rather)\b|\bplease use\b", re.I)),
        ("commitment", re.compile(r"\b(?:i|we|maya|stephen|the team)\s+(?:will|shall)\b|\bcommitted to\b|\bdeadline is\b", re.I)),
        ("fact", re.compile(r"\b(?:we decided|the team decided|we agreed|the team agreed|we chose|the plan is|has been approved|was approved|permit has been issued)\b", re.I)),
    )
    _noise = re.compile(r"\b(?:unsubscribe|view your (?:order|receipt|account)|order (?:receipt|number)|invoice|receipt|this email was sent|privacy policy|limited company registered|do not reply|newsletter|daily digest|no[- ]?reply|mailer-daemon)\b", re.I)
    _quoted = re.compile(r"(?im)^\s*(?:>|on .{0,180}wrote:|[-_]{3,}\s*(?:original message|forwarded message)|from:\s|sent:\s|date:\s)")
    _footer = re.compile(r"(?im)^\s*(?:unsubscribe\b|this email and any attachments|this email was sent|confidentiality (?:notice|and disclaimer)|privacy policy\b)")

    def suggest(self, sources: Iterable[Source]) -> list[Suggestion]:
        results: list[Suggestion] = []
        for source in sources:
            if self._noise.search(source.title) or self._noise.search(source.context):
                continue
            body = self._quoted.split(source.excerpt, maxsplit=1)[0]
            body = self._footer.split(body, maxsplit=1)[0]
            body = re.sub(r"https?://\S+|<[^>]+>", " ", body)
            body = re.sub(r"(?im)^\s*(?:dear\s+[^\n,.]+[,!]?|hi\s+[^\n,.]+[,!]?|hello\s+[^\n,.]+[,!]?)\s*", "", body)
            sentences = [re.sub(r"\s+", " ", s).strip(" \t\r\n>-") for s in re.split(r"(?<=[.!?])\s+|\n+", body)]
            candidate = next(((label, sentence) for sentence in sentences if len(sentence) >= 18
                              and not self._noise.search(sentence)
                              for label, pattern in self._patterns if pattern.search(sentence)), None)
            if candidate is None:
                continue
            kind, sentence = candidate
            results.append(Suggestion(
                suggestion_id=f"suggestion:{source.source_id}",
                kind=kind,
                proposition=sentence,
                source_id=source.source_id,
                rationale="A local rule found an explicit decision, preference, or commitment cue in the main message.",
                uncertainty="Deterministic demo mode can miss context or attribution. Inspect the source and correct or delete captured items.",
            ))
        return results


class MiniLMAdapter:
    name = "MiniLM adapter (weights unavailable; using demo fallback)"

    def suggest(self, sources: Iterable[Source]) -> list[Suggestion]:
        return DeterministicDemoAdapter().suggest(sources)


FIXTURES = [
    Source("fixture:planning", "Synthetic planning note", "The team decided to use a weekly planning review and keep decisions in the project log.", "2026-09-18", "Synthetic project planning conversation"),
    Source("fixture:launch", "Synthetic launch note", "Maya will prepare the launch checklist by 2026-10-02, with a Friday progress check.", "2026-09-20", "Synthetic launch coordination"),
    Source("fixture:preference", "Synthetic style note", "The project prefers concise status updates with links to the supporting source.", "2026-09-21", "Synthetic communication preference"),
]


def sources_from_json_payload(payload: object) -> list[Source]:
    """Parse the deliberately narrow, source-only UAT import format."""
    if not isinstance(payload, dict) or payload.get("format") != "lifetime-ai-uat-sources/v1":
        raise ValueError("JSON must use format lifetime-ai-uat-sources/v1")
    raw_sources = payload.get("sources")
    if not isinstance(raw_sources, list) or not raw_sources or len(raw_sources) > 100:
        raise ValueError("JSON must contain between 1 and 100 sources")
    allowed = {"source_id", "title", "excerpt", "occurred_at", "context"}
    sources: list[Source] = []
    for index, raw in enumerate(raw_sources, 1):
        if not isinstance(raw, dict) or set(raw) - allowed:
            raise ValueError(f"source {index} contains unsupported fields")
        missing = allowed - set(raw)
        if missing:
            raise ValueError(f"source {index} is missing: {', '.join(sorted(missing))}")
        values = {key: raw[key] for key in allowed}
        if any(not isinstance(value, str) or not value.strip() for value in values.values()):
            raise ValueError(f"source {index} fields must be non-empty strings")
        if len(values["excerpt"]) > 5000:
            raise ValueError(f"source {index} excerpt is longer than 5000 characters")
        sources.append(Source(values["source_id"], values["title"], values["excerpt"], values["occurred_at"], values["context"]))
    if len({source.source_id for source in sources}) != len(sources):
        raise ValueError("source_id values must be unique")
    return sources


def sources_from_mbox_text(raw_text: str, *, limit: int = 200) -> list[Source]:
    """Convert a local Gmail Takeout MBOX slice into previewable source excerpts.

    Attachments are intentionally ignored. This function does not write anything.
    """
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("MBOX file is empty")
    chunks = re.split(r"(?m)(?=^From [^\n]+\n)", raw_text)
    messages = [chunk for chunk in chunks if chunk.lstrip().startswith("From ")]
    if not messages:
        raise ValueError("No MBOX messages found")
    if len(messages) > limit:
        raise ValueError(f"MBOX contains {len(messages)} messages; limit is {limit} for this UAT")
    sources: list[Source] = []
    for index, chunk in enumerate(messages, 1):
        message = BytesParser(policy=policy.default).parsebytes(chunk.encode("utf-8", errors="replace"))
        body_part = message.get_body(preferencelist=("plain",))
        body = body_part.get_content() if body_part else ""
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if not body:
            continue
        message_id = message.get("Message-ID", "")
        digest = hashlib.sha256(f"{message_id}|{index}|{message.get('Subject', '')}".encode()).hexdigest()[:16]
        date_value = message.get("Date", "")
        try:
            occurred_at = parsedate_to_datetime(date_value).date().isoformat()
        except (TypeError, ValueError, OverflowError):
            occurred_at = "unknown-date"
        sender = message.get("From", "unknown sender")
        recipients = message.get("To", "")
        context = f"Email from {sender}" + (f" to {recipients}" if recipients else "")
        sources.append(Source(
            source_id=f"mbox:{digest}",
            title=message.get("Subject", "(no subject)")[:240],
            excerpt=body[:5000],
            occurred_at=occurred_at,
            context=context[:1000],
        ))
    if not sources:
        raise ValueError("MBOX contained no messages with readable plain-text bodies")
    return sources


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class UATStore:
    """Isolated disposable store. It never reads the evaluation corpus or core store."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS sources (
          source_id TEXT PRIMARY KEY, title TEXT NOT NULL, excerpt TEXT NOT NULL,
          occurred_at TEXT NOT NULL, context TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS suggestions (
          suggestion_id TEXT PRIMARY KEY, kind TEXT NOT NULL, proposition TEXT NOT NULL,
          source_id TEXT NOT NULL REFERENCES sources(source_id), rationale TEXT NOT NULL,
          uncertainty TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
          edited_proposition TEXT, decided_at TEXT
        );
        CREATE TABLE IF NOT EXISTS state_items (
          item_id TEXT PRIMARY KEY, kind TEXT NOT NULL, proposition TEXT NOT NULL,
          source_id TEXT NOT NULL REFERENCES sources(source_id), status TEXT NOT NULL,
          created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS interaction_events (
          event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, target_id TEXT,
          occurred_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS uat_findings (
          finding_id TEXT PRIMARY KEY, target_type TEXT NOT NULL,
          target_id TEXT NOT NULL, category TEXT NOT NULL,
          note TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL
        );
        """)
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def _event(self, event_type: str, target_id: str | None = None) -> None:
        self.db.execute("INSERT INTO interaction_events VALUES (?,?,?,?)", (str(uuid.uuid4()), event_type, target_id, now()))

    def load_sources(self, sources: Iterable[Source], adapter: SuggestionAdapter, *, auto_capture: bool = False) -> int:
        count = 0
        self.db.execute("BEGIN")
        try:
            for source in sources:
                inserted = self.db.execute("INSERT OR IGNORE INTO sources VALUES (?,?,?,?,?,?)", (source.source_id, source.title, source.excerpt, source.occurred_at, source.context, now())).rowcount
                if not inserted:
                    continue
                suggestion = next(iter(adapter.suggest([source])), None)
                if suggestion is not None:
                    status = "accepted" if auto_capture else "pending"
                    self.db.execute("""INSERT INTO suggestions
                        (suggestion_id,kind,proposition,source_id,rationale,uncertainty,status)
                        VALUES (?,?,?,?,?,?,?)
                        ON CONFLICT(suggestion_id) DO UPDATE SET kind=excluded.kind,
                        proposition=excluded.proposition, rationale=excluded.rationale,
                        uncertainty=excluded.uncertainty,
                        status=CASE WHEN ? THEN excluded.status ELSE suggestions.status END""", (suggestion.suggestion_id, suggestion.kind, suggestion.proposition, suggestion.source_id, suggestion.rationale, suggestion.uncertainty, status, int(auto_capture)))
                    self._event("shown", suggestion.suggestion_id)
                    if auto_capture:
                        item_id = f"item:{suggestion.suggestion_id}"
                        timestamp = now()
                        self.db.execute("""INSERT INTO state_items VALUES (?,?,?,?,?,?,?)
                            ON CONFLICT(item_id) DO UPDATE SET proposition=excluded.proposition,
                            status='active', updated_at=excluded.updated_at""", (item_id, suggestion.kind, suggestion.proposition, source.source_id, "active", timestamp, timestamp))
                        self._event("accepted", suggestion.suggestion_id)
                count += 1
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return count

    def add_source(self, source: Source, adapter: SuggestionAdapter) -> None:
        self.load_sources([source], adapter)

    def dashboard(self) -> dict[str, object]:
        sources = [dict(row) for row in self.db.execute("SELECT * FROM sources ORDER BY occurred_at, source_id")]
        reviews = [dict(row) for row in self.db.execute("SELECT * FROM suggestions ORDER BY source_id")]
        suggestions = [row for row in reviews if row["status"] == "pending"]
        state = [dict(row) for row in self.db.execute("SELECT * FROM state_items WHERE status='active' ORDER BY updated_at, item_id")]
        for record in reviews + state:
            record["source"] = dict(self.db.execute("SELECT * FROM sources WHERE source_id=?", (record["source_id"],)).fetchone())
        findings = [dict(row) for row in self.db.execute("SELECT * FROM uat_findings ORDER BY created_at DESC, finding_id")]
        return {"sources": sources, "suggestions": suggestions, "reviews": reviews,
                "state": state, "findings": findings}

    def add_finding(self, target_type: str, target_id: str, category: str,
                    note: str = "", *, confirmed: bool) -> str:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        if target_type not in {"source", "suggestion", "state"}:
            raise ValueError("unsupported finding target")
        if category not in {"false_positive", "wrong_type", "bad_extraction",
                            "duplicate", "missing_context", "retrieval_issue", "other"}:
            raise ValueError("unsupported finding category")
        if len(note) > 240:
            raise ValueError("finding note must be 240 characters or less")
        table, key = {"source": ("sources", "source_id"),
                      "suggestion": ("suggestions", "suggestion_id"),
                      "state": ("state_items", "item_id")}[target_type]
        if not self.db.execute(f"SELECT 1 FROM {table} WHERE {key}=?", (target_id,)).fetchone():
            raise ValueError("finding target does not exist")
        finding_id = f"finding:{uuid.uuid4()}"
        self.db.execute("INSERT INTO uat_findings VALUES (?,?,?,?,?,?)",
                        (finding_id, target_type, target_id, category, note.strip(), now()))
        self.db.commit()
        return finding_id

    def delete_finding(self, finding_id: str, *, confirmed: bool) -> None:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        if not self.db.execute("SELECT 1 FROM uat_findings WHERE finding_id=?", (finding_id,)).fetchone():
            raise ValueError("finding does not exist")
        self.db.execute("DELETE FROM uat_findings WHERE finding_id=?", (finding_id,))
        self.db.commit()

    def act(self, suggestion_id: str, action: str, *, confirmed: bool, proposition: str | None = None) -> None:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        row = self.db.execute("SELECT * FROM suggestions WHERE suggestion_id=?", (suggestion_id,)).fetchone()
        if not row:
            raise KeyError(suggestion_id)
        if action not in {"accepted", "edited", "rejected", "deferred"}:
            raise ValueError("unsupported review action")
        value = proposition.strip() if proposition else row["proposition"]
        self._event(action, suggestion_id)
        if action in {"accepted", "edited"}:
            item_id = f"item:{suggestion_id}"
            self.db.execute("""INSERT INTO state_items VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(item_id) DO UPDATE SET proposition=excluded.proposition,
                status='active', updated_at=excluded.updated_at""", (item_id, row["kind"], value, row["source_id"], "active", now(), now()))
        self.db.execute("UPDATE suggestions SET status=?, edited_proposition=?, decided_at=? WHERE suggestion_id=?", (action, value if action == "edited" else None, now(), suggestion_id))
        self.db.commit()

    def bulk_act(self, suggestion_ids: list[str], action: str, *, confirmed: bool) -> int:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        if not suggestion_ids or len(suggestion_ids) > 200:
            raise ValueError("Select between 1 and 200 suggestions")
        if action not in {"accepted", "rejected", "deferred"}:
            raise ValueError("unsupported bulk review action")
        rows = []
        for suggestion_id in dict.fromkeys(suggestion_ids):
            row = self.db.execute("SELECT * FROM suggestions WHERE suggestion_id=? AND status='pending'", (suggestion_id,)).fetchone()
            if not row:
                raise KeyError(suggestion_id)
            rows.append(row)
        try:
            for row in rows:
                self._event(action, row["suggestion_id"])
                if action == "accepted":
                    item_id = f"item:{row['suggestion_id']}"
                    timestamp = now()
                    self.db.execute("""INSERT INTO state_items VALUES (?,?,?,?,?,?,?)
                        ON CONFLICT(item_id) DO UPDATE SET proposition=excluded.proposition,
                        status='active', updated_at=excluded.updated_at""", (item_id, row["kind"], row["proposition"], row["source_id"], "active", timestamp, timestamp))
                self.db.execute("UPDATE suggestions SET status=?, decided_at=? WHERE suggestion_id=?", (action, now(), row["suggestion_id"]))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return len(rows)

    def correct(self, item_id: str, proposition: str, *, confirmed: bool) -> None:
        if not confirmed or not proposition.strip():
            raise ValueError("Explicit confirmation and non-empty text are required")
        self._event("corrected", item_id)
        self.db.execute("UPDATE state_items SET proposition=?, updated_at=? WHERE item_id=? AND status='active'", (proposition.strip(), now(), item_id))
        self.db.commit()

    def delete(self, item_id: str, *, confirmed: bool) -> None:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        self._event("deleted", item_id)
        self.db.execute("UPDATE state_items SET status='deleted', updated_at=? WHERE item_id=?", (now(), item_id))
        self.db.commit()

    def retrieve(self, question: str) -> dict[str, object]:
        terms = {term.lower() for term in re.findall(r"[a-zA-Z0-9]{3,}", question)}
        rows = []
        for row in self.db.execute("SELECT * FROM state_items WHERE status='active' ORDER BY updated_at DESC"):
            source = self.db.execute("SELECT * FROM sources WHERE source_id=?", (row["source_id"],)).fetchone()
            haystack = f"{row['proposition']} {source['excerpt']} {source['context']}".lower()
            score = sum(term in haystack for term in terms)
            if score:
                rows.append({"item": dict(row), "source": dict(source), "score": score})
        rows.sort(key=lambda item: item["score"], reverse=True)
        self._event("retrieved")
        self.db.commit()
        return {"question": question, "matches": rows[:5], "uncertainty": "Local keyword retrieval; absence of a match is not proof that no information exists."}

    def reset(self, *, confirmed: bool) -> None:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        self.db.execute("DELETE FROM uat_findings")
        self.db.execute("DELETE FROM interaction_events")
        self._event("reset")
        self.db.execute("DELETE FROM state_items")
        self.db.execute("DELETE FROM suggestions")
        self.db.execute("DELETE FROM sources")
        self.db.commit()

    def event_types(self) -> list[str]:
        return [row[0] for row in self.db.execute("SELECT event_type FROM interaction_events ORDER BY occurred_at")]
