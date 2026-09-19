# G3 pilot co-review revision — 20260918-2136-co-review-revision

## Status

`PILOT_READY_FOR_HUMAN_REVIEW` — G3 is **not complete**. The five affected cases require human re-review.

## Build identity

- Commit: `4fc9e5ab4745a9a31dbdf77506be770412f3e7ee`
- Dependency-lock SHA-256: `1438f893cdae63babf1cf48af8520fcfbe84946f0f5e42c9225904eb16218861`
- Pilot-manifest SHA-256: `23e7cb17250c86a63811d71b6d80b6e3113d734ef9706ef18694d2cb547c6387`

## Co-review corrections

- Pilot-04 and pilot-11 now return both the revoked prior item and active replacement for their broad current-state queries.
- Pilot-08 has an exact `valid_until` and machine-readable `metadata.advance_to`, with validation that the clock timestamp is valid, equals `occurred_at`, and reaches the expiry boundary.
- Pilot-09 is now `supersedes / accept / close_and_replace / investigate`, backed by an explicit current-registry source-of-truth rule and temporal boundary.
- Pilot-10 remains `contradicts / abstain / preserve_conflict / clarify`, backed by an equal-authority/no-precedence adjudication rule.
- Existing candidate snapshot identities and hashes were preserved; pilot-09 retains its original candidate hash while the new event and gold disposition carry the correction. Manifests were deterministically regenerated, and evaluator-only projection boundaries, partitions, and action-task semantics remain enforced.

## Automated validation

- Test suite: `40 passed`.
- Candidate-retrieval, pair-classification, and end-to-end mock tracks: pass for all 13 cases.
- Evaluator-only leakage failures: 0.
- Model calls: 0.
- Embeddings/vector search: absent.
- Production connections: absent.
- Final holdouts inspected or created: no.

## Decision

`NOT_EVALUATED`
