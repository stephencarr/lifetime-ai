# G3 pilot review revision — 20260918-1337-pilot-review-revision

## Status

`PILOT_READY_FOR_HUMAN_REVIEW` — G3 is **not complete** and no pass/fail gate decision has been made.

## Build identity

- Commit: `a298de58d730a865a1c008bd02c65f478abcd51e`
- Dependency-lock SHA-256: `1438f893cdae63babf1cf48af8520fcfbe84946f0f5e42c9225904eb16218861`
- Pilot-manifest SHA-256: `ae60f1ca5b10d09fbed5ca33ba2c3e5686661b3b1dcaa89026073476b714517c`
- Python: 3.13.11
- uv: 0.12.15
- Hardware: Apple M4 MacBook Air with 16 GB
- OS: macOS 26.5.1 build 25F80

## Revision

- Replaced `pilot_review` with `pilot_holdout` throughout active schemas, split logic, generated data, configuration, and smoke tooling.
- Removed the legacy `review.jsonl`; the corpus now has `development.jsonl`, `holdout.jsonl`, and one review packet.
- Expanded the packet to expose or link event IDs, timestamps, authority, source IDs, immutable snapshot and pool hashes, checkpoints, and downstream task gold.
- Made `none` mean no action-selection task and `silence` a deliberate result only when such a task exists.
- Rebuilt pilot-07 around a sole-source deletion event and pilot-08 around an explicit deadline followed by time advancement.
- Added SDUI/codebase histories for stale documentation, migration conflict, ownership change, generated schema, and intentional duplication.

## Automated validation

- Test suite: `38 passed`.
- Histories/pairs: 13/13; partitions: 9 development and 4 holdout.
- Schema and lifecycle validation: pass.
- Candidate-retrieval, pair-classification, and end-to-end mock tracks: pass for all 13 cases.
- Evaluator-only leakage failures: 0.
- Model calls: 0.
- Embeddings/vector search: absent.
- Production connections: absent.

## Required human action

Review all 13 cases in `evaluation/corpus/pilot-v0.1/reviews/pilot_review_packet.md`. Approve, revise, or reject each independent target, evidence set, checkpoint, and downstream task before any larger pilot corpus is generated.

## Why G3 remains open

- Human review is 0 of 13.
- The development target remains 30 histories and 120 relationship pairs.
- The statistically stronger frozen corpus and separate G4–G7 final holdouts do not exist.
- Baselines remain mocks and no model predictions were generated.

## Decision

`NOT_EVALUATED`
