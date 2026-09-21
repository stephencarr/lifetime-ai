# G3 pre-expansion instrument hardening — 20260919-1136

## Status

`PILOT_INSTRUMENT_HARDENED` — the 13 reviewed seed histories remain approved and the evaluation instrument now enforces the independent GTL's pre-expansion acceptance criteria. G3 is **not complete**.

## Build identity

- Commit at hardening time: `24c662263aa773136536083ced7f018386ff24ec`
- Working-tree changes: present; this record describes the regenerated pilot artifacts
- Dependency-lock SHA-256: `1438f893cdae63babf1cf48af8520fcfbe84946f0f5e42c9225904eb16218861`
- Pilot-manifest SHA-256: `b581094c17fd2f873aa5a027921680a65cc0f4fc0e9360a7595cf3e428e5ac4b`

## Acceptance result

All seven pre-expansion criteria pass:

1. Pair-classification projections exclude authority, actor identity, task wording, future events, and evaluator metadata.
2. Deleted content is absent from system, retrieval, and pair-classification projections; deleted snapshots become tombstones.
3. A synthetic mixed-action, multi-pair history validates, renders every pair, and runs through retrieval, classification, and end-to-end tracks.
4. Schemas and semantic validation enforce pair, pool, snapshot, checkpoint, task, evidence, and temporal references.
5. Review decisions are bound to substantive content hashes; content changes invalidate approval.
6. Deterministic stratified family splitting and a 30-history/120-pair coverage gate enforce the declared split, class, family, feature, hostile-case, disposition, effect, and action requirements.
7. Every downstream task declares its triggering pair and explicit target scope.

The smoke harness now executes every baseline mock across all 13 histories and checkpoints. It no longer awards a pass for construction alone.

## Automated validation

- Complete test suite: `47 passed`.
- Candidate-retrieval, pair-classification, and end-to-end mock tracks: pass for all 13 cases.
- Each of four baseline mocks executed 13 corpus cases.
- Evaluator-only leakage failures: 0.
- Model calls: 0.
- Embeddings/vector search: absent.
- Production connections: absent.
- Final holdouts inspected or created: no.

## Decision

`NOT_EVALUATED`

The evaluation instrument is ready for the separately authorized 30-history/120-pair development-pilot expansion. This record does not authorize that expansion and does not create or inspect any final G4/G5/G6/G7 holdout.
