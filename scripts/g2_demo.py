from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone

from lifetime_ai.pipeline import ExplicitCandidateSelector, TransitionPipeline, TransitionValidator
from lifetime_ai.semantics import ManualClassifier, Relationship, RelationshipResult
from lifetime_ai.store import Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, Transition


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the model-free G2 pipeline demonstration")
    parser.add_argument("database")
    args = parser.parse_args()
    now = datetime(2026, 9, 18, tzinfo=timezone.utc)
    source = Event("demo-source", EventType.USER_MESSAGE,
                   "I prefer concise answers.", now - timedelta(days=1))
    initial = StateItem("demo-preference", StateKind.PREFERENCE, source.text,
                        source.event_id, source.event_type, source.occurred_at,
                        valid_from=source.occurred_at)
    incoming = Event("demo-scope", EventType.USER_MESSAGE,
                     "For personal research, I prefer detailed answers.", now,
                     {"candidate_item_id": initial.item_id})
    probabilities = {relationship: 0.03 for relationship in Relationship}
    probabilities[Relationship.NARROWS_SCOPE] = 0.85
    semantic_result = RelationshipResult(
        probabilities, Relationship.NARROWS_SCOPE, 0.85)

    with Store(args.database) as store:
        store.ingest_and_apply(
            source, Transition("demo-seed", source.event_id, initial,
                               reason="explicit initial preference"))
        pipeline = TransitionPipeline(
            store, ExplicitCandidateSelector(),
            ManualClassifier({incoming.event_id: semantic_result}),
            TransitionValidator(store))
        outcome = pipeline.process(incoming)
        before = store.canonical_digest()
        print(json.dumps({"stage": "validated", "relationship": "narrows_scope",
                          "outcome": outcome.outcome, "digest": before}, sort_keys=True))

    with Store(args.database) as recovered:
        print(json.dumps({"stage": "recovered", "digest": recovered.canonical_digest(),
                          "state": recovered.inspect(),
                          "proposals": [dict(row) for row in recovered.proposals()]},
                         sort_keys=True))


if __name__ == "__main__":
    main()
