# Lifetime AI — Engineering Handoff

**Updated:** 21 September 2026
**Audience:** the engineer continuing architecture and evaluation work  
**Current phase:** G3 development pilot v0.7 agent review complete; prepare frozen evaluation corpus
**Gate state:** G0, G1, and G2 passed; G3 remains open

> **Current continuation note:** This general handoff contains historical pilot context. For the exact frozen-corpus v7 state and the remaining path to G3 completion, read [`docs/g3_completion_handoff.md`](g3_completion_handoff.md) first.

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

## 7. Current G3 artifacts

The current development pilot is `evaluation/corpus/pilot-v0.7/`: **30 histories, 120 pairs**, split across 21 development and 9 pilot-holdout histories. Two independent agent reviews passed; human signoff was waived by the project owner and is not claimed. The final holdouts for G4–G7 have not been created or accessed. Manifest status is `AGENT_REVIEWED`; G3 remains open.

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

The second freeze plan passed two independent agent reviews; see `experiments/g3/20260919-second-freeze-plan-review/summary.md`. It fixes the provisional G4 decision rule as 95% observed point precision, reported with a Wilson interval, and retains ≥100 autonomous accepts as the later observed holdout sample criterion. The approved planning size is 405 histories/1,620 pair opportunities, split by 90/45 whole families, conditional on the maximum cluster sizes, 30% planning coverage, 20% ineligibility/exclusion allowance, and family ICC ≤.30 in `docs/g3_evaluation_design_proposal.md`. Final-corpus generation, blinded gold adjudication, structural validation, and sealing may proceed under this plan. Model runs still require a G3 pass and separate G4 run authorization. “Untouched” means no model runs, predictions, threshold tuning, or model-output-informed wording changes; blinded gold adjudication and structural validation before sealing are permitted and must be recorded. Keep the v0.7 `pilot_holdout` development-only; it is not a final G4/G5/G6/G7 holdout. G3 remains `NOT_EVALUATED` until the required artifacts are frozen and hash-recorded and baseline smoke tests pass.

## 11. Commands for verification

From the repository root:

```sh
uv run --frozen pytest -q
uv run --frozen python scripts/run_g3_pilot_smoke.py --corpus evaluation/corpus/pilot-v0.7
shasum -a 256 -c evaluation/corpus/pilot-v0.7/manifest.sha256
```

In the managed sandbox, redirect the uv cache if needed:

```sh
UV_CACHE_DIR=/tmp/lifetime-ai-uv-cache uv run --frozen pytest -q
```

Expected current result: 50 tests pass; agent-reviewed v0.7 validates; all 270 system-facing projection canary checks pass; smoke executes all mock tracks and four baseline contracts with zero model calls. The pilot is agent-reviewed, not a frozen G4 holdout; G3 remains open.

## 12. Phase-gated actions

- **Before the second freeze review passes:** do not create or expose final G4/G5/G6/G7 holdouts.
- **After review passes but before G3 passes:** final-corpus generation, blinded gold adjudication, structural validation, and sealing are allowed under the approved plan. Do not run models or generate predictions.
- **After G3 passes:** model implementation/predictions and holdout evaluation still require a separate G4 run authorization. Do not tune thresholds or revise corpus/configuration in response to holdout outcomes; an inspected holdout is spent, and further evaluation requires a new holdout.
- **At every phase:** never treat the v0.7 `pilot_holdout` as a final gate holdout. Production/proprietary connections, embeddings/vector search, or an agent framework/UI are outside the current authorization and require a separately approved scope. Claim G3 completion only after its evidence and gate record satisfy the pass criteria.

Development-only sizing and freeze-plan work may proceed under the assumptions in `docs/g3_evaluation_design_proposal.md`. Mocks are contract tests only and are not experimental baseline results. The ≥100 observed-accept target and final cluster-aware size must be frozen in the second freeze review. The IID calculation is only a planning reference, not the final size decision.

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

There is an owner-driven documentation reorganization in the working tree. At the time of this handoff it includes modifications to `docs/gates.md` and `docs/lifetime_ai_roadmap_v0.2.md`, deletion/movement of `docs/lifetime_ai_roadmap_v0.1.md`, and additions under `docs/archive/`. Do not discard, overwrite, reset, or casually include those changes in another commit.

Some status prose in the in-progress roadmap/gates edits still describes the pre-G0 state. Until the owner reconciles those documents, the accepted experiment records under `experiments/g0`, `experiments/g1`, and `experiments/g2` are the authoritative evidence that G0–G2 passed. The latest G3 experiment record is authoritative for the completed pilot review count.

Before editing, always run `git status --short`. Stage only task-specific files.

## 16. Suggested first response in the next session

Confirm that you have read:

1. this handoff;
2. `docs/g3_evaluation_design_proposal.md`;
3. the G3 section of `docs/gates.md`;
4. `evaluation/corpus/pilot-v0.7/agent-review-record.md` and its review packet;
5. `evaluation/corpus/pilot-v0.7/projection-leakage.json`.

The second-freeze plan review has passed and is recorded at `experiments/g3/20260919-second-freeze-plan-review/summary.md`. The next authorized step is to generate the final corpus exactly to the approved family/size plan, conduct blinded gold review plus structural validation, and seal/hash it. Do not run models or generate predictions until G3 passes and a separate G4 run is authorized. The owner waived human signoff when independent agent review passes; record agent review truthfully and do not describe it as human review.
