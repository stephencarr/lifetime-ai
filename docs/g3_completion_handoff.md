# Lifetime AI — G3 Completion Handoff

**Updated:** 21 September 2026
**Gate state:** G0–G2 passed; G3 remains open (`NOT_EVALUATED`)
**Immediate objective:** finish review, freeze policy/contracts, seal the frozen-G4 corpus, and record a reproducible G3 decision
**Budget constraint:** do not use Atlas/Astra. Work locally and use the cheapest available peer only where independent review is mandatory.

## Read this first

The final planned corpus now exists and is structurally valid, but it is not sealed and G3 has not passed. Do not run learned models, generate predictions, tune thresholds from model output, or expose the final holdout to a model. G4 execution still requires a separate authorization after G3 passes.

The current accepted working draft is v7:

- Blueprint registry: `evaluation/blueprints/frozen-g4-v0.1/registry-v7/`
- Authoring matrix: `evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json`
- Staging corpus: `evaluation/corpus/frozen-g4-v0.1-staging-v7/`
- Size: 135 families, 405 histories, 1,620 pair opportunities
- Split: 90/45 whole families, producing 270/135 histories and 1,080/540 pairs
- Model predictions: absent
- Near-duplicate candidate set: empty in prior structurally equivalent stages; verify again on the final stage

Staging v7 is not the final seal. Its registry hash is:

```text
af14746be1b8d5c9a5655f264d9bec6f1a468aef17c1cd10054fc656156eee46
```

The production config still contains the earlier v4 registry pin, so v7 correctly reports the registry-pin blocker. Do not update the pin until all remaining source and corpus changes are finished; then restage once and pin that final hash.

## What happened in this work session

The frozen-G4 pipeline, schemas, generator, matrix binding, review contracts, lifecycle validation, deletion-query derivative scope, staging/sealing manifests, and model-free smoke harness were implemented or hardened.

The first complete corpus was not rubber-stamped:

- v4 passed structural validators but independent peer review rejected it for systematic domain drift, invented successor state, incorrect expiry rationales, identifier leakage in deletion prose, unestablished derivatives, false independent-support claims, and commitments without obligations.
- v6 repaired most defects but a low-cost peer rejected it for three remaining issues: derivatives marked asserted rather than inferred, scope conditions that did not match cited event text, and ordinary configuration facts typed as commitments.
- v7 repaired those issues. A low-cost focused peer review passed the full affected sets: 30 derivative candidates, 84 scope-narrowing pairs, and 21 commitment-failure pairs. It also rechecked all 1,620 structural pair references and found no broken contexts or deletion targets.

This v7 review proves the named repairs. It is not a substitute for the final two-reviewer, exact-hash approval record required by the sealing contract.

## Current verification state

Known passing checks:

- All 135 v7 blueprints build and validate.
- The focused authoring/matrix suite passes: 6 tests.
- Staging has previously validated exact family/history/pair counts, target coverage, lifecycle semantics, and whole-family assignment.
- Prior staging manifest verification and 3,645 projection canary checks passed with zero canary matches.
- No learned-model calls, embeddings, vector search, or production connections were used.

The last full suite run before the latest generator repair produced **100 passed, 1 failed**. The sole failure is a stale test, `test_frozen_g4_requires_registry_hash_pin`, which assumes the production pin is null. Rewrite it to use a temporary/unpinned config or replace it with pinned-match and pinned-mismatch tests. After doing so, rerun the entire suite; do not quote 100/101 as the final result.

## Remaining hard blockers

### 1. Complete truthful blind review

Create a final review record only after reviewers inspect the final, restaged content hashes.

Required:

- at least two independent reviewer identities;
- exact coverage of all 405 histories and all 1,620 pair IDs;
- no reviewer may equal the recorded generator;
- every difficult history must have second review; the corpus currently has 45 difficult histories;
- written reasoning for difficult-case second review;
- all findings resolved or rejected with rationale;
- approved histories must use exact `review_content_sha256` values;
- sealing must change pair `adjudication_status` from `pending` to `agreed` or `adjudicated`, not leave reviewed output internally pending.

Do not synthesize peer approvals. The owner waived human signoff only when independent agent review is genuine and recorded truthfully.

### 2. Finish seal and projection hardening

The read-only pipeline audit found these required changes:

- `verify_sealed_corpus()` must reload and schema/hash-validate the review and duplicate-adjudication artifacts, reapply approval equivalence, rerun frozen coverage/assignment validation, and verify top-level assignment/registry fields against payloads.
- `scripts/run_g3_frozen_smoke.py` must call `verify_sealed_corpus()` before loading/scoring payloads.
- Remove `partition` from every scored system/baseline projection. Prefer also excluding dataset/corpus/family bookkeeping not required by the contract.
- Add explicit forbidden-key leakage tests in addition to canary searching.
- Run checkpoints chronologically; do not ingest the full future timeline before earlier checkpoints.
- Add a real positive stage → review → seal → verify integration test. Test identities must never be reused as actual review evidence.

### 3. Freeze the G4 evaluation policy

`evaluation/config/g4-evaluation-v0.1.json` is deliberately provisional and therefore blocks G3. It still contains `UNSET_PENDING_DEVELOPMENT_CORPUS_REVIEW`, a provisional matcher, and a mock price table marked `replacement_required_before_g3_pass`.

Freeze, without using learned predictions:

- autonomous acceptance threshold and escalation rule;
- eligible-decision definition;
- calibration/ECE procedure and probability-sum tolerance;
- severity definitions and zero-tolerance handling;
- acceptable-alternative scoring;
- final deterministic semantic-state matcher;
- timeouts, provider failures, malformed output, and retry limits;
- exclusion policy;
- seeds and confidence intervals;
- token, retry, cache-fill, and cache-hit accounting;
- a non-mock, dated price table or an explicit policy that G4 cost comparison is deferred and cannot pass until a price table is frozen.

The gate may freeze a model-agnostic numeric policy. Threshold tuning from learned predictions remains forbidden before G3 pass unless the owner separately amends the phase rule.

### 4. Make baseline parity honest

The four current baseline mocks exercise interfaces but are not yet distinct baseline contracts. Before G3 passes:

- implement separate rolling-summary, scheduler, general-LLM, and limited-oracle adapters with deterministic fake providers;
- create a limited oracle projection that is distinct from the ordinary system projection;
- assert identical ordered ordinary inputs, simulated clock, checkpoint contract, six-class probability contract, and raw lifecycle usage contract;
- explicitly report unsupported fields rather than silently omitting them;
- run the smoke over the sealed corpus with zero learned calls.

### 5. Add holdout governance and final evidence

Create and hash:

- a truthful, append-only holdout access log covering authoring, review, validation, and sealing access;
- a projection manifest describing ordinary and oracle-visible fields;
- dataset card;
- class, feature, and joint-target summaries by partition;
- friendly/hostile case report;
- final config and price-table hashes;
- model-free baseline smoke result;
- exact command log and environment record;
- final `experiments/g3/<run-id>/` gate record with criterion-by-criterion PASS/FAIL and overall decision.

After sealing, model-development workers must not receive holdout evaluator material. A later G4 run must add a separately authorized access-log entry.

## Safe execution order

1. Fix the stale registry-pin test.
2. Harden projection, sealed verification, smoke ordering, and approval-state handling.
3. Freeze the evaluation policy, price/accounting policy, ordinary projection, and limited-oracle projection.
4. Add access-log and evidence-assembly support.
5. Regenerate the registry only if corpus content changed; otherwise retain v7.
6. Stage to a new path and confirm the only blockers are review and duplicate adjudication.
7. Pin the final registry hash in `evaluation/config/frozen-g4-v0.1.json`.
8. Restage to another new path so the staging manifest binds the final pin and final source dependencies.
9. Conduct two-reviewer blind review against exact final hashes; resolve findings and regenerate if content changes.
10. Create the hashed near-duplicate adjudication artifact. An empty reviewed-pair list is correct only when the staged candidate set is empty.
11. Seal to a new immutable output path and run strengthened verification.
12. Run the full test suite, frozen model-free smoke, checksum verification, matrix regeneration comparison, and `git diff --check`.
13. Write the G3 evidence record and update gate status only if every criterion passes.

Any corpus-content change after review invalidates approvals and requires new hashes and review. Any source dependency change after staging requires a new stage.

## Commands to resume

Run from the repository root. Use `/private/tmp` for the uv cache in the managed sandbox.

```sh
git status --short

UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache \
  uv run --frozen pytest -q

UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache \
  uv run --frozen python scripts/stage_frozen_g4_corpus.py stage \
  --blueprints evaluation/blueprints/frozen-g4-v0.1/registry-v7 \
  --authoring-matrix evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json \
  --output evaluation/corpus/frozen-g4-v0.1-staging-<next>
```

For a deterministic matrix check, generate to a temporary path and compare bytes; the generator refuses to overwrite an existing matrix.

```sh
draft_matrix=/private/tmp/lifetime-ai-authoring-matrix-check.json
rm -f "$draft_matrix"
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache \
  uv run --frozen python scripts/generate_frozen_g4_authoring_matrix.py \
  --output "$draft_matrix"
cmp evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json "$draft_matrix"
```

Do not run `seal` until truthful final review and duplicate-adjudication artifacts exist. Do not run the learned evaluation after sealing without separate G4 authorization.

## Files most relevant to continuation

- `docs/g3_evaluation_design_proposal.md`
- `docs/gates.md`
- `evaluation/config/frozen-g4-v0.1.json`
- `evaluation/config/g4-evaluation-v0.1.json`
- `evaluation/schema/frozen-g4-*.schema.json`
- `lifetime_ai/evaluation/frozen_g4.py`
- `lifetime_ai/evaluation/frozen_g4_pipeline.py`
- `lifetime_ai/evaluation/initial_authoring.py`
- `lifetime_ai/evaluation/projection.py`
- `scripts/generate_frozen_g4_authoring_matrix.py`
- `scripts/render_frozen_g4_blueprints.py`
- `scripts/stage_frozen_g4_corpus.py`
- `scripts/run_g3_frozen_smoke.py`
- `tests/test_frozen_g4.py`
- `tests/test_g3_frozen_smoke.py`
- `tests/test_g4_evaluation_config.py`

## Workspace cautions

The worktree is intentionally dirty and includes owner documentation reorganization plus substantial uncommitted G3 work. Do not reset, checkout, delete, or overwrite unrelated changes. Earlier registries and staging directories are audit history; leave them in place until the final seal is accepted, then archive or remove them only with explicit owner direction.

No commit was created during this work. Before an honest G3 PASS, either commit the accepted state or create a complete, hash-bound source/patch bundle in the G3 experiment record so the evidence is reproducible.

## Definition of done

G3 is complete only when the final corpus is reviewed, pinned, sealed, and independently verifiable; evaluation and baseline policies are frozen; ordinary/oracle projections and holdout access are controlled; the full suite and model-free smoke pass; and a reproducible experiment record declares `PASS` with no unresolved deviations.

Until then, the correct status is `G3 OPEN / NOT_EVALUATED`.
