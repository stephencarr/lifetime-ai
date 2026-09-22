# Lifetime AI — Engineering Handoff

**Updated:** 22 September 2026
**Audience:** the engineer continuing architecture and evaluation work  
**Current phase:** G3 passed; G4 development underway. Holdout evaluation remains unauthorized; sealed v21 is quarantined for a clean-agent evaluation after an accidental broad text search.
**Gate state:** G0-G3 passed. See `docs/g3_completion_handoff.md` for the full remediation record: the v16/v17 seal was found defective by adversarial content review and superseded by v20, which was itself superseded by v21 for unrelated evaluation-tooling fixes (no corpus content change). Do not cite `experiments/g3/20260921-1207-frozen-g4-v16/` as current evidence.

> **Current continuation note:** This general handoff contains historical pilot context (sections 1-9) that remains accurate. For the current G3 PASS evidence, the v16/v17 defect-and-remediation record, and G4 development/holdout authorization boundaries, read [`docs/g3_completion_handoff.md`](g3_completion_handoff.md) first.

> **Holdout incident and owner disposition (22 September 2026):** A broad `rg` search over `docs evaluation scripts` traversed holdout files and returned holdout content, violating the no-access instruction. No holdout results, predictions, scoring, or threshold tuning were produced. The owner chose a clean-agent quarantine rather than automatic replacement: freeze this development candidate, transfer no incident-thread content or holdout data, and require separate authorization before a single final holdout run. The procedural breach must be disclosed; v21 is not literally never-accessed. See `experiments/g4/20260922-1351-local-encoder-development/holdout-access-incident.md`.

## 1. Read this first

Lifetime AI is testing whether durable, provenance-aware application state can carry operational continuity more safely and efficiently than repeatedly reconstructing state inside an LLM prompt.

The immediate proving ground is engineering knowledge for unfamiliar codebases, especially SDUI-style systems. The intended system should help a coding agent answer questions such as “How do I build this form using the current component conventions?” using compact, source-anchored, temporally reconciled state rather than indiscriminate transcript or document retrieval.

This project values falsifiable evidence over feature accumulation. A failed gate is useful. Do not optimize for a persuasive demo, code volume, or an architecture-friendly benchmark.

The next engineer should be comfortable with:

- event-sourced and transactional state;
- provenance, temporal validity, authority, deletion, and replay semantics;
- evaluation design, leakage prevention, calibration, and strong baselines;
- distinguishing reversible bookkeeping from authoritative mutation;
- resisting premature LLM, embedding, vector-store, framework, and UI work.

The right mindset is a skeptical systems/evaluation engineer, not an agent-framework integrator. Preserve the architectural separations even when collapsing them would make a fixture or demo easier.

## 2. Product thesis and practical claim

The broad thesis is:

> The application—not a transient model invocation—should own durable operational state, provenance, time, permissions, lifecycle, and continuity. Models are replaceable semantic and expressive processors.

The narrow claim worth testing first is:

> For selected engineering questions, a maintained, provenance-aware state layer can produce a smaller and more reliable context packet than a strong hybrid MCP/RAG baseline while preserving or improving task success.

This does **not** claim consciousness, human-equivalent memory, general intelligence, universally lossless bounded context, or that structured data is inherently superior to text.

## 3. Target architecture

```text
source events
→ typed candidate state
→ semantic relationship proposal
→ deterministic authority and transition validation
→ atomic canonical-state update with provenance
→ task-specific bounded context
→ replaceable downstream model or tool
```

The intended non-generative path is:

```text
request or source event
→ local typed routing/classification
→ evidence-aware state query
→ compact recommendation/context object
→ ordinary coding agent
```

A vector index, if later justified, is only a candidate-retrieval mechanism. It cannot determine truth, authority, freshness, permission, or mutation.

## 4. Non-negotiable separations

Every evaluated event–candidate pair has four independent targets:

1. **Semantic relationship:** `supports`, `contradicts`, `narrows_scope`, `supersedes`, `unrelated`, or `uncertain`.
2. **Transition disposition:** `accept`, `reject_unauthorized`, `reject_invalid`, `abstain`, or `no_op`.
3. **Expected state effect:** `reinforce`, `preserve_conflict`, `add_scoped_item`, `close_and_replace`, `invalidate`, `expire`, or `none`.
4. **Expected external action:** `none`, `clarify`, `investigate`, `outreach_candidate`, or `silence`.

Why this matters:

- Authority must never determine the semantic label. Unauthorized text can genuinely contradict a candidate while still being rejected for mutation.
- `none` means action selection is not in scope and there is no action-selection task.
- `silence` means action selection is explicitly in scope and deliberate non-action is the answer.
- `abstain` can coexist with `preserve_conflict`: recording two claims as disputed is reversible bookkeeping, not selecting either as authoritative truth.
- Historical assertion and current operational truth are different evaluator objects.
- Runtime item IDs are provenance handles, not semantic correctness targets.

## 5. Implemented foundation and accepted gates

### G0 — reproducible foundation: passed

- Python 3.13.11 under `uv`; project requires Python 3.12+.
- Locked dependencies in `uv.lock`.
- Two clean-environment runs passed on an Apple M4 MacBook Air with 16 GB.
- Evidence: `experiments/g0/20260917-2120-reproducible-foundation/`.

### G1 — durable authoritative state: passed

- Typed event ledger and canonical state in SQLite.
- Source-linked atomic transitions.
- Idempotent replay and collision rejection.
- Rollback on injected failure.
- Foreign-key enforcement.
- Deterministic restart recovery and inspectable provenance.
- Evidence: `experiments/g1/20260917-2140-durable-state/`.

### G2 — typed transition boundary: passed

- Candidate selection, relationship classification, proposal, validation, and commit are separated.
- The classifier and proposal builder have no `Store` reference.
- Only `TransitionValidator` invokes the canonical mutation operation.
- Support, contradiction, narrowing, supersession, irrelevance, uncertainty, authorization failures, and rollback are covered.
- Evidence: `experiments/g2/20260917-2200-typed-pipeline/` and `docs/g2_mutation_boundary.md`.

### Current automated state

- Complete suite: **50 passing tests**.
- SQLite schema version: 2.
- No LLM calls, embeddings, vector storage, agent framework, production connector, or UI.

## 6. Why G3 exists

G3 builds an evaluation instrument capable of disproving the architecture before learned semantic components are added. It is not a model-quality gate and should not be declared complete because schemas, mocks, or a large JSON file exist.

The approved design protects against the main ways this project could fool itself:

- whole histories/families are split, never individual pairs;
- candidate-retrieval, gold-candidate pair classification, and end-to-end evaluation are separate tracks;
- retrieval candidate pools are isolated and immutable;
- evaluator-only labels and canaries are removed through allowlist projections and never supplied to systems;
- candidate snapshots are canonical, immutable, and SHA-256 addressed;
- state scoring is semantic rather than based on literal runtime IDs;
- full six-class probability vectors are required from classifiers;
- lifecycle cost is calculated by the harness from raw usage;
- deletion uses one ordered event path rather than a side channel;
- expiry uses explicit validity and simulated clock advancement;
- G4, G5, G6, and G7 will require separate final holdout families;
- cases hostile to the proposed architecture are required.

Design source: `docs/g3_evaluation_design_proposal.md`.

## 7. Development-pilot G3 artifacts (historical; superseded by section 10)

> This section describes the 30-history development pilot that predates the final 405-history frozen-G4 corpus. It remains accurate as history but is not the current G3 evidence — see section 10 and `docs/g3_completion_handoff.md` for the corpus that actually satisfied the G3 gate.

The development pilot was `evaluation/corpus/pilot-v0.7/`: **30 histories, 120 pairs**, split across 21 development and 9 pilot-holdout histories. Two independent agent reviews passed; human signoff was waived by the project owner and is not claimed. The final holdouts for G4–G7 have not been created or accessed. Manifest status is `AGENT_REVIEWED`; G3 remains open.

Review findings and verification are recorded in `evaluation/corpus/pilot-v0.7/agent-review-record.md`. The corpus passes schema and coverage validation, all 50 tests, four mock baseline contract smokes, and 270 projection canary checks with zero leaks. The prior v0.3/v0.4 event-text accuracy tests are preserved as exploratory diagnostics, not leakage gates.

Current artifacts:

- Review packet: `evaluation/corpus/pilot-v0.7/reviews/pilot_review_packet.md`
- Manifest and hash: `evaluation/corpus/pilot-v0.7/manifest.json` and `manifest.sha256`
- Generator and review recorder: `scripts/generate_g3_development_pilot_v07.py` and `scripts/record_g3_agent_review.py`
- Smoke harness: `scripts/run_g3_pilot_smoke.py`
- Evaluation contracts and validation: `lifetime_ai/evaluation/`
- G3 decision: `NOT_EVALUATED`

## 8. Earlier seed-pilot review decisions

The following cases are approved in the packet and have `reviewer_status: reviewed`, pair `adjudication_status: agreed`, and dated review provenance.

### pilot-04 — explicit replacement

- Gold: `supersedes / accept / close_and_replace / none`.
- The broad current-state task returns both the revoked prior preference and active replacement.
- Reason: a temporal replacement must preserve the old assertion historically while exposing the replacement as current truth.

### pilot-08 — deadline expiry

- Gold: `unrelated / accept / expire / none`.
- Commitment expiry: `2026-09-18T11:00:00Z`.
- Clock event: `metadata.advance_to = 2026-09-18T12:00:00Z`, equal to event `occurred_at`.
- Reason: time advancement is lifecycle input, not a semantic assertion about the commitment.

### pilot-09 — stale SDUI documentation

- Gold: `supersedes / accept / close_and_replace / none`.
- The event identifies the current component registry as authoritative and explicitly marks the guide as stale.
- The original immutable candidate snapshot and hash were preserved.
- The initial proposed action was `investigate`; human review found that `none` is more defensible because the fixture already supplies the authoritative registry observation and defines no verification task. The action-selection task was therefore removed.

### pilot-10 — conflicting migration observations

- Gold: `contradicts / abstain / preserve_conflict / clarify`.
- Both observations are authorized, cover the same migration/scope/validity period, and have no precedence metadata.
- Reason: no winner can be selected safely. Both claims remain disputed, and clarification is required before execution.

### pilot-11 — ownership change

- Gold: `supersedes / accept / close_and_replace / none`.
- The broad current-state task returns both revoked Team Atlas ownership and active Team Nova ownership.
- Reason: CODEOWNERS provides an explicit effective replacement while provenance retains the former owner historically.

## 9. Completed final pilot co-review

An independent technical-lead co-review found weaknesses not detected by schema validation. All eight formerly pending cases were corrected and approved:

- broad current-state tasks now require proposition, scope, status, and evidence rather than a status-only answer;
- pilot-03 uses a genuine general-to-specific scope relationship;
- pilot-07 invalidates at the deletion event time and relies on the documented lifecycle-event exception for its independent semantic label;
- pilot-12 asks for a system action and names the source/generated-schema discrepancy to investigate.

Evidence: `experiments/g3/20260919-1121-complete-pilot-human-review/`.

## 10. Exact next step

G3 has passed. The frozen-G4 v0.1 corpus is sealed at `evaluation/corpus/frozen-g4-v0.1-sealed-v21/` (405 histories, 1,620 pair opportunities, 270/135 whole-family split), superseding an earlier v16/v17 seal that adversarial content review found defective (see `docs/g3_completion_handoff.md` for the full defect-and-fix record: three fabricated-content bugs and one holdout-assignment instability, all fixed and independently reverified). The v20 seal that resulted from that remediation was itself superseded one day later by v21: an external PR review found three evaluation-*tooling* bugs (an oracle-baseline temporal leak in the smoke harness, stale v15-pinned evidence-builder constants, and a probability-tolerance policy mismatch) that were fixed and required a reseal, but did not change any corpus content, family assignment, or partition — the existing v20 review record was reused as-is.

The evaluation policy (`evaluation/config/g4-evaluation-v0.1.json`) fixes the provisional G4 decision rule at 95% observed point precision, reported with a Wilson interval, and retains ≥100 autonomous accepts as the later observed holdout sample criterion, per the approved second-freeze plan. It remains sealed at `FROZEN_AT_G3_MODEL_FREE` with holdout authorization false; development-only authorization is recorded separately in `evaluation/config/g4-development-authorization.json`.

Development model execution and threshold tuning are authorized only on the development partition. The next authorization decision is for the untouched holdout; do not run models, generate predictions, or tune thresholds against it. “Untouched” holdout means exactly that; an inspected holdout is spent per the governing rule in `docs/gates.md`, and further evaluation requires a new holdout.

## 11. Commands for verification

From the repository root:

```sh
uv run --frozen pytest -q
uv run --frozen python scripts/stage_frozen_g4_corpus.py verify --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v21
uv run --frozen python scripts/run_g3_frozen_smoke.py --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v21
(cd evaluation/corpus/frozen-g4-v0.1-sealed-v21 && shasum -a 256 -c manifest.sha256)
```

In the managed sandbox, redirect the uv cache if needed:

```sh
UV_CACHE_DIR=/tmp/lifetime-ai-uv-cache uv run --frozen pytest -q
```

The last full G3 suite recorded 117 passes; the targeted G4 test set subsequently recorded 44 passes. Earlier full sealed-corpus verification reported manifest hash `9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3`; the model-free smoke reported `status: PASS` with 0 evaluator leakage failures and 0 learned model calls across all four baseline contracts. Do not re-run full corpus verification under the current no-holdout-access instruction. The prior `pilot-v0.7` development pilot remains development-only and was never a final gate holdout; it is superseded for G3 purposes by the frozen-G4 corpus above.

The development scoring path is implemented at `scripts/score_g4_development.py`. It accepts a complete precomputed prediction artifact, scores development pairs, and rejects non-development pairs or unauthorized runs by default. Its output is explicitly `DEVELOPMENT_DIAGNOSTIC_ONLY`: artifact-selected candidate accepts are not autonomous decisions, and it does not enforce the frozen transition policy. It does not generate predictions or authorize model execution. Development runners and scorer authenticate the pinned manifest and development payload without opening the holdout; this is intentionally narrower than full sealed-corpus verification.

The local G4 development comparison is recorded in `experiments/g4/20260922-1351-local-encoder-development/`. The initial 216-pair whole-JSON baseline had only 2 candidate accepts per model. The later structured, family-grouped MiniLM protocol produced 588 potential candidate accepts among 1,080 development pairs at the frozen 0.95 probability threshold (54.44% coverage), 578 correct (98.30% precision), with no high-severity errors. These are not autonomous decisions because the deterministic transition validator was not applied; G4 has not passed. Holdout evaluation remains unauthorized.

Separate development-only state-effect and disposition heads now predict out of fold (988/1,080 and 952/1,080 correct, respectively); 569/588 relationship-probability-gated pairs have all three targets correct. A read-only structural preflight passed 138/588, but eight still had a wrong relationship or effect and four had gold disposition `abstain`. Even matching the predicted disposition to proposal shape leaves six wrong pairs and two gold `abstain` cases. These diagnostics cannot authorize writes or count G4 autonomy. Full deterministic effect/permission validation, persistence, and baseline comparisons remain open.

The G4 transition module can prepare read-only no-op, reinforcement, scoped-item, and narrow close-and-replace state candidates while checking payload hashes and source provenance. All positive paths require explicit proposal shape, source authority, and a constrained source-text witness. The scoped-item extractor uses source-visible `child workflow '…'` phrases; the replacement extractor handles explicit setting changes with an effective time and closes the parent. The earlier 138/588 structural-preflight diagnostic grew to 345/588 after scoped-item support, then 422/588 after replacement support. All eight wrong preflight pairs remain no-op proposals; no-op is excluded from the rehearsal. The current state-changing witness slice is 363, all correct in development. This is development-tuned textual matching, not general semantic entailment or independent validation. Resolution, other lifecycle effects, broader semantic correctness, and persistence still need explicit designs and tests. Autonomous G4 decisions remain zero.

The subsequent end-to-end read-only rehearsal (`scripts/run_g4_transition_rehearsal_development.py`) uses an explicit, unfrozen development policy and strips evaluator fields before decisions. It combines the fixed 0.95 single-class gate, no-op exclusion, predicted disposition shape, preflight, source witness, and prepared-state invariants. The initial v0.1 candidate prepared 286/1,080 pairs (26.48%); v0.2 adds a narrow read-only `close_and_replace` path and prepares 363/1,080 (33.61%), all 363 jointly correct with gold `accept` disposition in development. All-eligible relationship ECE is 0.0198. Both prepared replacement payloads match immediate reference snapshots in 45/45 available cases; 32 accepted replacements lack an immediate reference comparison. The full decision audit and hashes are under `experiments/g4/20260922-1351-local-encoder-development/`. No writes, model inference timing, baseline comparison, or holdout access occurred; cost comparison remains deferred. Clearing provisional numbers on development is not a G4 pass or autonomous operation.

## 12. Phase-gated actions

- **G3 has passed; development G4 is authorized:** model implementation, development predictions, and development threshold tuning are allowed under the separate development authorization artifact. Holdout evaluation still requires separate authorization. Do not tune thresholds or revise corpus/configuration in response to holdout outcomes; an inspected holdout is spent, and further evaluation requires a new holdout.
- **If corpus content changes again for any reason** (further defect found, feature added, etc.): a new stage and fresh review are required; v21-content approvals cannot be reused for different content, per the sealing code's own content-hash binding.
- **At every phase:** never treat the historical `pilot-v0.7` `pilot_holdout` as a final gate holdout. The authorized local MiniLM development embeddings do not authorize production/proprietary connections, hosted vector search, or an agent framework/UI; those require separately approved scope.

Mocks (the four baseline contracts exercised by the model-free smoke) are contract tests only and are not experimental baseline results — they establish that all four baselines consume comparable inputs and emit a comparable contract, not that any of them perform well. Real baseline runs are G4/G5 work, separately authorized.

## 13. Strong-baseline requirement for later work

When authorized, the relevant conventional baseline is not naive vector search. It should include hybrid lexical/vector/symbol retrieval, source filters, recency weighting, citations, conflict reporting, a fixed context budget, and the same source corpus, downstream model, query set, and tool budget.

Useful engineering task families include:

- orientation: “Where does this request flow?”
- implementation: “How do I build this form using current SDUI conventions?”
- impact: “What else must change if I add this field?”

Measure task success, source-anchor correctness, stale and unsupported claims, conflict detection, abstention quality, final-agent tokens, broad searches, latency, update lag, and total lifecycle cost.

## 14. Security, budget, and operating constraints

- Current target machine: Apple M4 MacBook Air, 16 GB unified memory.
- Prototype budget: approximately CAD $100/month.
- Sustainable owner attention: approximately four focused hours/week.
- Local-first, single-user text prototype.
- External actions require explicit human review; future initiative is a reviewable outbox only.
- Do not ingest proprietary workplace data or connect to workplace systems without explicit authorization. Use synthetic or sanitized SDUI fixtures.

## 15. Workspace hygiene at handoff

The v21 remediation is committed on branch `codex/complete-g3`. Earlier registries and staging/sealed directories are audit history; do not reset, delete, or overwrite them without explicit owner direction.

Earlier registries (`registry-v2` through `registry-v19`) and their staging/sealed directories are audit history documenting the defect-discovery and remediation process. Do not reset, delete, or overwrite them without explicit owner direction.

The accepted experiment records under `experiments/g0`, `experiments/g1`, and `experiments/g2` remain the authoritative evidence that G0-G2 passed. The current G3 evidence is `evaluation/corpus/frozen-g4-v0.1-sealed-v21/` plus `experiments/g3/20260922-1351-v21-evidence-builder-remediation/`; the v20 and v16 records are historical and must not be cited as current evidence.

Before editing, always run `git status --short`. Stage only task-specific files.

## 16. Suggested first response in the next session

Confirm that you have read:

1. this handoff;
2. `docs/g3_completion_handoff.md` (the full v16-defect/v20-remediation and v21-tooling record — read this before trusting any prior "G3 passed" claim);
3. the G3 section of `docs/gates.md`;
4. `experiments/g3/20260922-1351-v21-evidence-builder-remediation/g3-gate-remediation.md`;
5. `evaluation/corpus/frozen-g4-v0.1-sealed-v21/review-record.json`'s `review_findings` array (the three consciously-accepted lower-severity items).

G3 has passed against `evaluation/corpus/frozen-g4-v0.1-sealed-v21/`. Development-only model runs are authorized by `evaluation/config/g4-development-authorization.json`; do not access or generate predictions for the holdout until separately authorized. If asked to extend or re-review this corpus, budget for genuine adversarial reading of event/gold content, not only structural/schema/hash validation: that weaker method is what let the original v16/v17 defects through undetected.
