"""Actual local-model M5 construction, reconciliation, and answer path.

The language model proposes semantic decisions. This runtime and Store enforce
the source/provenance boundary and fail closed on missing or malformed models.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime
from uuid import uuid4

from .chat import ChatResponse, Citation
from .local_models import LocalChatModel, LocalEmbedder, ModelUnavailable, ModelResult
from .model_retrieval import ModelRetriever
from .model_semantics import ModelSemantics, PROMPT_VERSION
from .pipeline import row_to_item
from .store import Store
from .types import Event, EventType, StateItem, StateKind, StateStatus, Transition


class ModelChatRuntime:
    def __init__(self, store: Store, generator: LocalChatModel, embedder: LocalEmbedder):
        self.store = store
        self.semantics = ModelSemantics(generator)
        self.retriever = ModelRetriever(store, embedder)
        self.generator_id = generator.expected_model_id
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0}
        self.index_healthy = True

    def _used(self, result: ModelResult) -> dict:
        self.usage["prompt_tokens"] += result.prompt_tokens
        self.usage["completion_tokens"] += result.completion_tokens
        self.usage["calls"] += 1
        return result.value

    def _abstain(self, event_id: str, ordinal: int, reason: str) -> None:
        self.store.record_proposal(f"model:{event_id}:{ordinal}", event_id, None,
                                   "model_capture", "{}", "abstained", reason)

    def send(self, text: str, occurred_at: datetime,
             event_id: str | None = None) -> ChatResponse:
        event = Event(event_id or f"model-chat:{uuid4().hex}", EventType.USER_MESSAGE,
                      text, occurred_at, {"channel": "local_model_chat"})
        self.store.ingest(event)
        if not self.index_healthy:
            self._abstain(event.event_id, 0, "candidate index unavailable")
            return ChatResponse("The local candidate index is unavailable; nothing was stored.",
                                outcome="abstained")
        try:
            proposals = self._used(self.semantics.extract(text)).get("claims")
            if not isinstance(proposals, list) or len(proposals) > 3:
                raise ModelUnavailable("extractor returned invalid claim count")
        except ModelUnavailable as error:
            self._abstain(event.event_id, 0, str(error))
            return ChatResponse("The local semantic model is unavailable; nothing was stored.",
                                outcome="abstained")
        if not proposals:
            self._abstain(event.event_id, 0, "model proposed no durable claim")
            return ChatResponse("No durable claim was supported from that message.",
                                outcome="abstained")
        accepted: list[Citation] = []
        rejected: list[str] = []
        for ordinal, claim in enumerate(proposals):
            try:
                citation = self._accept_one(event, ordinal, claim)
            except (ModelUnavailable, ValueError, KeyError, TypeError) as error:
                reason = str(error) or type(error).__name__
                self._abstain(event.event_id, ordinal, reason)
                rejected.append(reason)
                continue
            if citation is None:
                rejected.append("duplicate or unsupported relationship")
            else:
                accepted.append(citation)
        if not accepted:
            return ChatResponse("No proposed claim passed source and state checks.",
                                outcome="abstained")
        refs = " ".join(f"[source:{item.source_event_id}]" for item in accepted)
        return ChatResponse(f"Stored {len(accepted)} source-backed claim(s). {refs}",
                            tuple(accepted), "accepted")

    def _accept_one(self, event: Event, ordinal: int, claim: dict) -> Citation | None:
        if not isinstance(claim, dict):
            raise ValueError("malformed claim proposal")
        required = {"kind", "proposition", "actor", "value", "polarity",
                    "scope_anchor", "durability", "source_quote"}
        if set(claim) != required or claim["actor"] != "user":
            raise ValueError("claim actor or fields invalid")
        if claim["kind"] not in {"preference", "commitment", "fact"}:
            raise ValueError("unsupported claim kind")
        if claim["polarity"] not in {"positive", "negative"}:
            raise ValueError("invalid polarity")
        if not all(isinstance(claim[key], str) and 0 < len(claim[key]) <= 500
                   for key in required - {"scope_anchor"}):
            raise ValueError("empty or oversized claim field")
        if (not isinstance(claim["scope_anchor"], str) or
                len(claim["scope_anchor"]) > 100):
            raise ValueError("invalid scope anchor")
        if claim["durability"] != "ongoing":
            raise ValueError("claim is episodic or uncertain, not durable state")
        quote = claim["source_quote"]
        start = event.text.find(quote)
        if start < 0:
            raise ValueError("source quote is not an exact event span")
        if claim["scope_anchor"] and claim["scope_anchor"] not in quote:
            raise ValueError("scope anchor is not in the cited source span")
        claim = {**claim, "scope": claim["scope_anchor"] or "general"}
        verdict = self._used(self.semantics.verify_claim(event.text, claim))
        if (verdict.get("verdict") != "entailed" or
                not isinstance(verdict.get("supporting_quote"), str) or
                not verdict["supporting_quote"] or
                verdict["supporting_quote"] not in event.text):
            raise ValueError("source does not semantically support proposed claim")
        candidates = [row for row in self.retriever.candidates(
            claim["proposition"], final_k=8) if row["kind"] == claim["kind"]]
        related = {}
        if candidates:
            result = self._used(self.semantics.relate(claim, candidates))
            entries = result.get("relationships")
            if not isinstance(entries, list) or len(entries) != len(candidates):
                raise ModelUnavailable("relationship response incomplete")
            related = {entry.get("item_id"): entry.get("relationship") for entry in entries
                       if isinstance(entry, dict)}
            expected = {row["item_id"] for row in candidates}
            if set(related) != expected or len(related) != len(entries):
                raise ModelUnavailable("relationship identities differ from candidates")
            if any(value not in {"unrelated", "reinforces", "contradicts",
                                 "supersedes", "narrows_scope", "uncertain"}
                   for value in related.values()):
                raise ModelUnavailable("invalid relationship value")
            if "uncertain" in related.values():
                raise ValueError("relationship uncertain")
            if "reinforces" in related.values():
                self._abstain(event.event_id, ordinal, "reinforces current claim")
                return None
        superseded = [row for row in candidates
                      if related.get(row["item_id"]) == "supersedes"]
        if len(superseded) > 1:
            raise ValueError("multiple supersession targets")
        prior_transition = None
        if superseded:
            prior = superseded[0]
            if prior["kind"] != claim["kind"] or prior["actor"] != claim["actor"]:
                raise ValueError("supersession kind or actor differs")
            closed = replace(row_to_item(prior), status=StateStatus.EXPIRED,
                             source_event_id=event.event_id, source_type=event.event_type,
                             occurred_at=event.occurred_at, valid_until=event.occurred_at)
            prior_transition = Transition(f"transition:{event.event_id}:{ordinal}:close",
                                          event.event_id, closed,
                                          reason="model-proposed, source-checked supersession")
        embedding = self.retriever.embedder.embed([claim["proposition"]])[0]
        item_id = f"model:{event.event_id}:{ordinal}"
        item = StateItem(item_id, StateKind(claim["kind"]), claim["proposition"],
                         event.event_id, event.event_type, event.occurred_at,
                         confidence=0.0, valid_from=event.occurred_at)
        transition = Transition(f"transition:{event.event_id}:{ordinal}:capture",
                                event.event_id, item, reason="model-proposed, source-checked claim")
        annotation = {"actor": claim["actor"], "relation": claim["kind"],
                      "value": claim["value"], "polarity": claim["polarity"],
                      "scope": claim["scope"], "source_quote": quote,
                      "source_start": start, "source_end": start + len(quote),
                      "embedding": embedding, "generator_model": self.generator_id,
                      "prompt_version": PROMPT_VERSION,
                      "verifier_result": verdict}
        self.store.commit_model_claim(f"model:{event.event_id}:{ordinal}", event.event_id,
                                      transition, annotation, prior_transition)
        try:
            if superseded:
                self.retriever.remove(superseded[0]["item_id"])
            self.retriever.add(item_id, embedding)
        except Exception:
            self.index_healthy = False
            # The durable commit succeeded. Fail closed on future retrieval
            # until a fresh runtime rebuilds the disposable ANN index.
        return Citation(item_id, event.event_id, event.text)

    def ask(self, question: str) -> ChatResponse:
        if not self.index_healthy:
            return ChatResponse("Candidate index unavailable; I cannot answer safely.",
                                outcome="uncertain")
        try:
            candidates = self.retriever.candidates(question)
            if not candidates:
                return ChatResponse("I found no current evidence that supports an answer.",
                                    outcome="uncertain")
            response = self._used(self.semantics.answer(question, candidates))
            outcome = response.get("outcome")
            answer = response.get("answer")
            ids = response.get("item_ids")
            if (outcome not in {"answered", "uncertain", "conflict", "needs_clarification"}
                    or not isinstance(answer, str) or not isinstance(ids, list)
                    or len(ids) != len(set(ids))):
                raise ModelUnavailable("malformed answer proposal")
            by_id = {row["item_id"]: row for row in candidates}
            if any(item_id not in by_id for item_id in ids):
                raise ModelUnavailable("answer cites a non-candidate item")
            if outcome == "uncertain":
                return ChatResponse(answer or "Current evidence is insufficient.",
                                    outcome="uncertain")
            if not ids:
                raise ModelUnavailable("answer has no supporting citation")
            if outcome == "conflict" and len(ids) < 2:
                raise ModelUnavailable("conflict needs at least two cited claims")
            cited = [by_id[item_id] for item_id in ids]
            verified = self._used(self.semantics.verify_answer(question, answer,
                                                                outcome, cited))
            supporting_quote = verified.get("supporting_quote")
            if (verified.get("verdict") != "entailed" or
                    not isinstance(supporting_quote, str) or not supporting_quote or
                    not any(supporting_quote in row["source_quote"] for row in cited)):
                return ChatResponse("I found related state, but cannot verify that it answers the question.",
                                    outcome="uncertain")
            citations = tuple(Citation(row["item_id"], row["source_event_id"],
                                       row["source_text"]) for row in cited)
            refs = " ".join(f"[source:{row['source_event_id']}]" for row in cited)
            return ChatResponse(f"{answer} {refs}", citations, outcome)
        except (ModelUnavailable, ValueError, KeyError, TypeError):
            return ChatResponse("The local semantic path could not verify an answer.",
                                outcome="uncertain")

    def delete_source(self, event_id: str) -> bool:
        item_ids = self.store.model_active_item_ids_for_source(event_id)
        changed = self.store.delete_event(event_id)
        if changed:
            try:
                for item_id in item_ids:
                    self.retriever.remove(item_id)
            except Exception:
                self.index_healthy = False
        return changed
