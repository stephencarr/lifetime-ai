from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Mapping, Protocol

from .validation import RELATIONSHIPS


@dataclass(frozen=True)
class RawLifecycleUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    model_calls: int = 0
    retrieval_operations: int = 0
    elapsed_ms: int = 0
    local_compute_ms: int = 0
    peak_memory_bytes: int | None = None
    provider_usage_records: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True)
class PredictedRelationship:
    candidate_snapshot_id: str
    probabilities: Mapping[str, str]
    decision: str
    confidence: str
    escalate: bool

    def validate(self) -> None:
        if set(self.probabilities) != RELATIONSHIPS:
            raise ValueError("probability vector must contain exactly six relationship classes")
        values = [Decimal(value) for value in self.probabilities.values()]
        if any(value < 0 or value > 1 for value in values):
            raise ValueError("probabilities must be in [0,1]")
        if sum(values) != Decimal("1"):
            raise ValueError("probabilities must sum exactly to 1")
        if self.decision not in RELATIONSHIPS:
            raise ValueError("unknown relationship decision")
        if Decimal(self.confidence) != Decimal(self.probabilities[self.decision]):
            raise ValueError("confidence must equal selected-class probability")


@dataclass(frozen=True)
class RankedCandidate:
    snapshot_id: str
    score: str


class CandidateRetriever(Protocol):
    retriever_id: str

    def rank(self, projection: Mapping[str, Any], limit: int) -> list[RankedCandidate]: ...
    def raw_usage(self) -> RawLifecycleUsage: ...


class PairClassifier(Protocol):
    classifier_id: str

    def classify(self, projection: Mapping[str, Any]) -> PredictedRelationship: ...
    def raw_usage(self) -> RawLifecycleUsage: ...


class EvaluationSystem(Protocol):
    system_id: str

    def reset(self, history_id: str, configuration: Mapping[str, Any]) -> None: ...
    def ingest(self, event: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def raw_usage(self) -> RawLifecycleUsage: ...


@dataclass
class MockCandidateRetriever:
    retriever_id: str = "mock-retriever"
    _usage: RawLifecycleUsage = field(default_factory=RawLifecycleUsage)

    def rank(self, projection: Mapping[str, Any], limit: int) -> list[RankedCandidate]:
        self._usage = RawLifecycleUsage(retrieval_operations=1, elapsed_ms=1, local_compute_ms=1)
        return [RankedCandidate(item["snapshot_id"], "1")
                for item in projection["candidates"][:limit]]

    def raw_usage(self) -> RawLifecycleUsage:
        return self._usage


@dataclass
class MockPairClassifier:
    classifier_id: str = "mock-pair-classifier"
    decision: str = "uncertain"

    def classify(self, projection: Mapping[str, Any]) -> PredictedRelationship:
        others = [name for name in sorted(RELATIONSHIPS) if name != self.decision]
        probabilities = {name: "0.1" for name in others}
        probabilities[self.decision] = "0.5"
        prediction = PredictedRelationship(
            projection["candidate_snapshot"]["snapshot_id"], probabilities,
            self.decision, "0.5", self.decision == "uncertain")
        prediction.validate()
        return prediction

    def raw_usage(self) -> RawLifecycleUsage:
        return RawLifecycleUsage(elapsed_ms=1, local_compute_ms=1)


@dataclass
class MockEvaluationSystem:
    system_id: str = "mock-end-to-end"
    events_seen: int = 0
    configuration: Mapping[str, Any] = field(default_factory=dict)

    def reset(self, history_id: str, configuration: Mapping[str, Any]) -> None:
        self.events_seen = 0
        self.configuration = dict(configuration)

    def ingest(self, event: Mapping[str, Any]) -> Mapping[str, Any]:
        self.events_seen += 1
        return {"accepted": True}

    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return {"current_state": [], "historical_assertions": [], "relationship_decisions": [],
                "proposed_actions": [], "evidence_links": [], "abstentions": [],
                "decision_trace": []}

    def raw_usage(self) -> RawLifecycleUsage:
        return RawLifecycleUsage(elapsed_ms=self.events_seen, local_compute_ms=self.events_seen)


@dataclass
class MockRollingSummaryBaseline(MockEvaluationSystem):
    system_id: str = "baseline-a-mock-rolling-summary"
    summary: list[str] = field(default_factory=list)

    def reset(self, history_id: str, configuration: Mapping[str, Any]) -> None:
        super().reset(history_id, configuration)
        self.summary = []

    def ingest(self, event: Mapping[str, Any]) -> Mapping[str, Any]:
        super().ingest(event)
        content = event.get("content")
        if isinstance(content, str):
            self.summary = [*self.summary[-3:], content]
        return {"accepted": True, "summary_entries": len(self.summary)}

    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return {**super().checkpoint(request), "rolling_summary": list(self.summary),
                "unsupported_fields": ["relationship_probabilities"]}


@dataclass
class MockSchedulerBaseline(MockEvaluationSystem):
    system_id: str = "baseline-b-mock-scheduler"
    scheduled_events: list[str] = field(default_factory=list)

    def reset(self, history_id: str, configuration: Mapping[str, Any]) -> None:
        super().reset(history_id, configuration)
        self.scheduled_events = []

    def ingest(self, event: Mapping[str, Any]) -> Mapping[str, Any]:
        super().ingest(event)
        if event.get("event_type") == "time_advance" or event.get("metadata", {}).get("valid_until"):
            self.scheduled_events.append(str(event["event_id"]))
        return {"accepted": True, "scheduled_events": len(self.scheduled_events)}

    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return {**super().checkpoint(request), "scheduled_events": list(self.scheduled_events),
                "unsupported_fields": ["semantic_relationship", "current_state"]}


@dataclass
class MockGeneralLLMBaseline(MockEvaluationSystem):
    """Contract test double only; performs no model call."""

    system_id: str = "baseline-c-mock-general-llm"

    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return {**super().checkpoint(request), "fake_provider_response": "abstain",
                "unsupported_fields": []}


@dataclass
class MockOracleBaseline(MockEvaluationSystem):
    system_id: str = "baseline-d-mock-oracle"

    def checkpoint(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        projection = self.configuration.get("limited_oracle_projection", {})
        return {**super().checkpoint(request),
                "gold_transitions": projection.get("gold_transitions", []),
                "gold_invalidations": projection.get("gold_invalidations", []),
                "unsupported_fields": []}


def calculate_cost_cad(usage: RawLifecycleUsage, price_table: Mapping[str, str]) -> Decimal:
    input_cost = Decimal(usage.input_tokens) * Decimal(price_table["input_per_token_cad"])
    output_cost = Decimal(usage.output_tokens) * Decimal(price_table["output_per_token_cad"])
    provider_cost = sum(
        (Decimal(str(record.get("cost_cad", "0"))) for record in usage.provider_usage_records),
        Decimal("0"),
    )
    return input_cost + output_cost + provider_cost
