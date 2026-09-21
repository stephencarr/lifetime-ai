# Lifetime AI — G3 Completion Handoff

**Updated:** 21 September 2026
**Gate state:** G0–G3 passed (`PASS`, model-free readiness)
**Next authorization:** G4 model execution and holdout evaluation require a separate explicit authorization.

## Final frozen candidate

The accepted corpus content is the reviewed v15 candidate. Its corrected v16
seal uses the reviewers' actual Codex task identities and is independently verified.

- Blueprint registry: `evaluation/blueprints/frozen-g4-v0.1/registry-v15/`
- Authoring matrix: `evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json`
- Staging corpus: `evaluation/corpus/frozen-g4-v0.1-staging-v15/`
- Sealed corpus: `evaluation/corpus/frozen-g4-v0.1-sealed-v16/`
- Size: 135 families, 405 histories, 1,620 pair opportunities
- Split: 90/45 whole families, producing 270/135 histories and 1,080/540 pairs
- Model predictions: absent
- Near-duplicate candidates: zero; empty adjudication artifact is hashed and sealed

Exact bindings:

```text
staging manifest: 4b5e236f6bc8aff2b61ec597c97cdc5e27d680eda7cc3848c5779f98f674d3e0
sealed manifest:  f6f41c49faab07240b174a1bb7ef9c13838e2caeebbb08101ff75ed81cb25fe6
registry:         2dc3138ae52ae7355fc81ece6cfa0ea286f3e35c5ac0a3e57dbc830e0502b159
assignment:       a4024e6ac5e7fa8cc3b706af40cdabfffbf7dcef41e2478cae7448e403ac5e50
```

## Independent review

Two independent blind reviewer reports passed against the exact v15 candidate. Each report covers all 405 histories and all 1,620 pair opportunities, uses canonical substantive-content hashes, and records no findings. The v16 review record identifies the reviewers by their actual Codex task IDs. All 45 histories tagged `difficult` are assigned both reviewer IDs with written second-review rationale. No human review or approval is claimed; the project-owner waiver applies to the genuine independent agent reviews.

Review and evidence packet:

`experiments/g3/20260921-1207-frozen-g4-v16/`

The packet contains the reviewer reports, review record, difficult-history review, empty near-duplicate adjudication, holdout access log, projection manifest, class/feature/joint-target summaries, friendly/hostile planning report, configuration/source hashes, commands, environment, smoke output, and criterion-level gate record.

## Verification evidence

- Targeted frozen-G4/smoke/config/matrix suite: **47 passed**.
- Complete repository suite: **101 passed**.
- `verify_sealed_corpus()`: **PASS**.
- Model-free smoke: **PASS**, 405 end-to-end cases and 1,620 retrieval/classification cases.
- Four deterministic baseline contracts: **PASS** for rolling summary, scheduler, general-LLM interface, and limited oracle.
- Learned model calls: **0**.
- Embeddings/vector search: **false**.
- Production connections: **false**.
- Ordinary projection leakage failures: **0**.
- Chronological checkpoint visibility, lifecycle handling, forbidden-key checks, and prediction canaries: **PASS**.

The evaluation policy is frozen without learned predictions or threshold tuning. It explicitly defers G4 cost comparison until a dated price table is frozen; no cost-based claim is made by G3.

## Post-G3 constraints

1. Preserve `evaluation/corpus/frozen-g4-v0.1-sealed-v16/` as immutable evidence.
2. Do not run learned evaluation, threshold tuning, or holdout model access until a separate G4 authorization is recorded.
3. If corpus content or source dependencies change, create a new stage and obtain new reviews; v15-content approvals and the v16 seal cannot be reused.
4. Freeze and hash a dated price table before making any G4 cost-comparison claim.

## Workspace cautions

Earlier registries and staging directories are audit history. Do not reset, delete, or overwrite them without explicit owner direction. The accepted state should remain committed, and the final evidence packet should be preserved with it.

G3 is complete: the corpus is reviewed, pinned, sealed, and independently verifiable; evaluation and baseline policies are frozen; ordinary/oracle projections and holdout access are controlled; the full suite and model-free smoke pass; and the reproducible experiment record declares `PASS` with no unresolved blockers.
