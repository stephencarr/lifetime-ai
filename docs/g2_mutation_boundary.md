# G2 mutation boundary

```text
Event
  │
  ▼
ExplicitCandidateSelector ──► tuple[StateItem, ...]
  │
  ▼
RelationshipClassifier ──► RelationshipResult
  │                         (typed probabilities, decision, confidence, escalation)
  ▼
ProposalBuilder ──► TransitionProposal
  │                 (immutable request; no persistence authority)
  ▼
TransitionValidator
  ├── invalid ──► source-linked rejected proposal record
  ├── uncertain ► source-linked abstention record; no mutation
  ├── unrelated ► source-linked no-op record; no mutation
  └── valid ────► Store.commit_proposal(...)
                    └── one SQLite transaction:
                        transitions + canonical state + audit + accepted proposal
```

The classifier, candidate selector, and proposal builder receive no `Store` reference. `TransitionValidator` is the sole G2 component allowed to call `Store.commit_proposal`, which is the canonical mutation operation. Event ingestion remains a ledger operation performed by the pipeline before semantic interpretation.

The replaceable classifier contract is `RelationshipClassifier` in `lifetime_ai/semantics.py`. `ManualClassifier` is the current model-free implementation. Replacing it requires no change to the persistence or validation layers.
