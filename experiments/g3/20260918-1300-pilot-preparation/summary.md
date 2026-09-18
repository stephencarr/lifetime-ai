# G3 development-pilot preparation — 20260918-1300-pilot-preparation

## Status

`PILOT_READY_FOR_HUMAN_REVIEW` — G3 is **not complete** and no pass/fail gate decision has been made.

## Build identity

- Commit: `beadd415b64b42033a07f320fc79d4e4979a97c0`
- Dependency-lock SHA-256: `1438f893cdae63babf1cf48af8520fcfbe84946f0f5e42c9225904eb16218861`
- Pilot-manifest SHA-256: `940e62c2e2a4496faf3a4a0bbae957fb4b32e8eba859ee440c54694ab9690b30`
- Python: 3.13.11
- uv: 0.12.15
- Hardware: Apple M4 MacBook Air with 16 GB
- OS: macOS 26.5.1 build 25F80

## Commands

```sh
uv run --frozen python scripts/generate_g3_pilot.py
uv run --frozen python scripts/run_g3_pilot_smoke.py --output experiments/g3/20260918-1300-pilot-preparation/smoke-results.json
uv run --frozen pytest -q
```

The managed execution sandbox used `UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache`; this changes cache location only.

## Prepared artifacts

- Machine-readable JSON Schemas for histories, candidate snapshots, tasks, system/evaluator/oracle projections, and baseline outputs.
- Deterministic canonical JSON and JSONL serialization with hash test vectors.
- Immutable candidate snapshots and isolated, history-local retrieval pools.
- Whole-family pilot splitting plus disjoint G4–G7 final-holdout assignment logic.
- Allowlist-based system projections and post-deletion tombstoning.
- Semantic state matching that ignores generated runtime item IDs.
- Separate candidate-retrieval, gold-candidate classification, and end-to-end contracts.
- Harness-owned cost calculation from raw usage and a hashed price table.
- Mock smoke implementations for Baselines A–D; the Baseline C mock makes no LLM call.

## Pilot material

Eight histories and eight initial pairs were generated:

- six in `pilot_development`;
- two in `pilot_review`;
- all eight have `reviewer_status: pending`;
- no partition is a final gate holdout.

The cases cover all six semantic relationships plus an unauthorized contradiction, deletion/invalidation, expiry, independent action labels, and architecture-hostile examples. This is an initial review sample, not the complete 30-history/120-pair pilot.

## Automated validation

- Test suite: `34 passed`.
- Schema validation: pass.
- Candidate-pool isolation: pass.
- Whole-family splitting: pass.
- Disjoint final-gate holdout assignment: pass.
- Evaluator-only canary leakage: zero failures.
- Single deletion-event path: pass.
- Full six-class probability contract: pass.
- Harness cost calculation: pass.
- Mock Baseline A–D interfaces: pass.
- Model calls: 0.
- Embeddings/vector search: absent.
- Production connections: absent.

## Required human action

Review every case in `evaluation/corpus/pilot-v0.1/reviews/pilot_review_packet.md`. Approve, revise, or reject each semantic label, disposition, state effect, action, checkpoint, evidence set, and task. Generation must not expand to the full pilot until this review is complete.

## Why G3 remains open

- Only 8 of the planned 30 pilot histories exist.
- Only 8 of the planned 120 pilot pairs exist.
- Human review is 0 of 8.
- Final corpus sizing has not been recalculated from pilot findings.
- No final G4–G7 holdouts or frozen evaluation configurations exist.
- Baselines are mocks and have not produced comparative results.

## Decision

`NOT_EVALUATED`

The correct next step is human review of these eight cases, not more generation or model work.
