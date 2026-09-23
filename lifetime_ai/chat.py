"""Small local chat workflow layered on the model-independent state core.

The extractor and renderer are explicit seams.  The bundled rule extractor is
only a deterministic preflight adapter; it is not presented as evidence of
capture quality or as a silent substitute for a model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Protocol
from uuid import uuid4

from .answerability import decide
from .pipeline import TransitionValidator
from .store import RetrievalIncompleteError, SourceError, Store
from .types import Event, EventType, StateKind


@dataclass(frozen=True)
class ExtractedClaim:
    proposition: str
    kind: StateKind
    item_id: str | None = None
    confidence: float = 1.0
    sensitivity: str = "normal"
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    replaces_proposition: str | None = None


class ClaimExtractor(Protocol):
    def extract(self, event: Event) -> ExtractedClaim | None: ...


class RuleBasedLocalExtractor:
    """Explicit, narrow preflight adapter for preference/commitment statements."""

    _patterns = (
        (re.compile(r"^I prefer .+[.!]?$", re.IGNORECASE), StateKind.PREFERENCE),
        (re.compile(r"^I will .+[.!]?$", re.IGNORECASE), StateKind.COMMITMENT),
    )
    _change = re.compile(
        r"^I now prefer (?P<new>.+) instead of (?P<old>.+)[.!]$", re.IGNORECASE)
    _short = re.compile(r"^Please keep your answers short[.!]$", re.IGNORECASE)
    _unsafe = re.compile(
        r"\b(if|unless|perhaps|maybe|hypothetically|tomorrow|yesterday|next week)\b"
        r"|\b(?:said|wrote|asked)\b|[\n\r\"“”]|\?",
        re.IGNORECASE,
    )

    def extract(self, event: Event) -> ExtractedClaim | None:
        text = event.text.strip()
        if self._unsafe.search(text):
            return None
        change = self._change.fullmatch(text)
        if change:
            return ExtractedClaim(
                proposition=f"I prefer {change['new']}.", kind=StateKind.PREFERENCE,
                valid_from=event.occurred_at,
                replaces_proposition=f"I prefer {change['old']}.",
            )
        if self._short.fullmatch(text):
            return ExtractedClaim("I prefer short answers.", StateKind.PREFERENCE,
                                  valid_from=event.occurred_at)
        for pattern, kind in self._patterns:
            if pattern.fullmatch(text):
                return ExtractedClaim(
                    proposition=text, kind=kind, valid_from=event.occurred_at
                )
        return None


@dataclass(frozen=True)
class Citation:
    item_id: str
    source_event_id: str
    source_text: str


@dataclass(frozen=True)
class ChatResponse:
    text: str
    citations: tuple[Citation, ...] = ()
    outcome: str = "noop"


class ResponseRenderer(Protocol):
    def render(self, query: str, rows: list[object]) -> ChatResponse: ...


class CitedStateRenderer:
    """Render only propositions supported by the declared development grammar."""

    def render(self, query: str, rows: list[object]) -> ChatResponse:
        decision = decide(query, rows)
        citations = tuple(Citation(row["item_id"], row["source_event_id"], row["source_text"])
                          for row in decision.rows)
        refs = " ".join(f"[source:{row['source_event_id']}]" for row in decision.rows)
        if decision.outcome == "answered":
            propositions = "; ".join(dict.fromkeys(row["proposition"] for row in decision.rows))
            return ChatResponse(f"{propositions} {refs}", citations, "answered")
        if decision.outcome == "conflict":
            return ChatResponse(f"{decision.reason} {refs}", citations, "conflict")
        if decision.outcome == "needs_clarification":
            return ChatResponse(f"{decision.reason} {refs}".strip(), citations,
                                "needs_clarification")
        return ChatResponse(decision.reason or "I cannot support an answer from current sources.",
                            outcome="uncertain")


class ChatRuntime:
    def __init__(self, store: Store, extractor: ClaimExtractor,
                 renderer: ResponseRenderer | None = None):
        self.store = store
        self.extractor = extractor
        self.renderer = renderer or CitedStateRenderer()
        self.validator = TransitionValidator(store)

    def send(self, text: str, occurred_at: datetime, event_id: str | None = None) -> ChatResponse:
        event = Event(event_id or f"chat:{uuid4().hex}", EventType.USER_MESSAGE, text, occurred_at,
                      {"channel": "local_chat"})
        self.store.ingest(event)
        claim = self.extractor.extract(event)
        if claim is None:
            self.store.record_proposal(
                f"capture:{event.event_id}", event.event_id, None, "capture", "{}",
                "abstained", "extractor returned no claim",
            )
            return ChatResponse("I did not capture a durable claim from that message.",
                                outcome="abstained")
        active = self.store.active(claim.kind)
        if any(row["proposition"].casefold() == claim.proposition.casefold() for row in active):
            self.store.record_proposal(
                f"capture:{event.event_id}", event.event_id, None, "capture", "{}",
                "abstained", "duplicate current claim",
            )
            return ChatResponse("That claim is already current; I kept the existing source.",
                                outcome="abstained")
        if claim.replaces_proposition:
            candidates = [row for row in active if row["proposition"].casefold() ==
                          claim.replaces_proposition.casefold()]
            if len(candidates) != 1:
                self.store.record_proposal(
                    f"capture:{event.event_id}", event.event_id, None, "capture", "{}",
                    "abstained", "no unique earlier preference for time change",
                )
                return ChatResponse("I could not identify one earlier preference to replace.",
                                    outcome="abstained")
            claim = replace(claim, item_id=candidates[0]["item_id"])
        outcome = self.validator.validate_capture(event, claim)
        if not outcome.accepted:
            return ChatResponse(f"I did not store that claim: {outcome.reason}.",
                                outcome=outcome.outcome)
        return ChatResponse(
            f"Stored a source-backed {claim.kind.value}: {claim.proposition} "
            f"[source:{event.event_id}]",
            (Citation(claim.item_id or f"claim:{event.event_id}", event.event_id, event.text),),
            "accepted",
        )

    def correct(self, item_id: str, proposition: str, occurred_at: datetime,
                event_id: str | None = None) -> ChatResponse:
        prior = self.store.state_item(item_id)
        if not prior:
            raise SourceError("state item does not exist")
        event = Event(event_id or f"correction:{uuid4().hex}", EventType.USER_MESSAGE,
                      proposition, occurred_at, {"channel": "local_chat", "correction": item_id})
        self.store.ingest(event)
        claim = ExtractedClaim(proposition, StateKind(prior["kind"]), item_id=item_id,
                               valid_from=occurred_at, sensitivity=prior["sensitivity"])
        outcome = self.validator.validate_capture(event, claim)
        if not outcome.accepted:
            return ChatResponse(f"I did not apply that correction: {outcome.reason}.",
                                outcome=outcome.outcome)
        return ChatResponse(f"Updated {item_id}: {proposition} [source:{event.event_id}]",
                            (Citation(item_id, event.event_id, proposition),), "accepted")

    def ask(self, query: str) -> ChatResponse:
        try:
            candidates = self.store.retrieve(query)
        except RetrievalIncompleteError:
            return ChatResponse("Current state exceeds the candidate limit; I cannot give a complete source-backed answer.",
                                outcome="uncertain")
        return self.renderer.render(query, candidates)

    def delete_source(self, event_id: str) -> bool:
        return self.store.delete_event(event_id)
