# Lifetime AI — Engineering Handoff

**Updated:** 19 September 2026  
**Audience:** the engineer continuing architecture and evaluation work  
**Current phase:** G3 development-pilot review  
**Gate state:** G0, G1, and G2 passed; G3 remains open

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

- Complete suite: **40 passing tests**.
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

The current development pilot contains **13 histories and 13 relationship pairs**:

- 9 in `pilot_development`;
- 4 in `pilot_holdout`;
- 5 reviewed and approved;
- 8 pending human review.

`pilot_holdout` is only exercising pilot split/sealing machinery. It is **not** a final G4/G5/G6/G7 holdout and becomes development material after pilot review.

Key artifacts:

- Review packet: `evaluation/corpus/pilot-v0.1/reviews/pilot_review_packet.md`
- Development records: `evaluation/corpus/pilot-v0.1/development.jsonl`
- Pilot holdout records: `evaluation/corpus/pilot-v0.1/holdout.jsonl`
- Manifest: `evaluation/corpus/pilot-v0.1/manifest.json`
- Manifest hash file: `evaluation/corpus/pilot-v0.1/manifest.sha256`
- Generator: `scripts/generate_g3_pilot.py`
- Smoke harness: `scripts/run_g3_pilot_smoke.py`
- Validation: `lifetime_ai/evaluation/validation.py`
- Projection boundary: `lifetime_ai/evaluation/projection.py`
- Baseline contracts: `lifetime_ai/evaluation/contracts.py`
- Evaluation tests: `tests/test_evaluation_harness.py`

Current accepted build identity:

- Pilot build commit: `409a430e2f135cead166b0ada0d0ab54021d00f5`
- Partial-review record commit: `f870bb1`
- Pilot manifest SHA-256: `23380a545bd63165f6642d8ffb794e1fb072650cfb48b2abd506f79e57df9a73`
- Evidence record: `experiments/g3/20260919-1025-partial-human-review/`
- G3 decision: `NOT_EVALUATED`

## 8. Human-review decisions already made

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

## 9. Cases still awaiting human review

Do not silently mark these approved. Present them for review and record any corrections before requesting expansion authorization.

- **pilot-01:** `supports / accept / reinforce / none` — preference reinforcement.
- **pilot-02:** `contradicts / reject_unauthorized / none / silence` — unauthorized imported contradiction; deliberate silence has an action-selection task.
- **pilot-03:** `narrows_scope / accept / add_scoped_item / none` — detailed personal-research exception beneath a general concise preference.
- **pilot-05:** `unrelated / no_op / none / silence` — irrelevant weather with deliberate non-action explicitly evaluated.
- **pilot-06:** `uncertain / abstain / none / clarify` — genuinely underspecified referent and scope.
- **pilot-07:** `unrelated / accept / invalidate / none` — deletion event targets the sole supporting source and invalidates the derivative.
- **pilot-12:** `contradicts / reject_unauthorized / none / investigate` — generated schema conflicts with authoritative source schema; investigation is explicitly evaluated.
- **pilot-13:** `supports / accept / reinforce / none` — ADR confirms intentional duplication across platform boundaries.

Review especially whether the action-selection tasks in pilot-02, pilot-05, pilot-06, and pilot-12 describe a concrete decision rather than smuggling policy into semantic classification.

## 10. Exact next step

The next task is **human review of the remaining eight cases**, not corpus expansion.

**Authorization boundary:** the owner has already authorized the next engineer to inspect all eight pending records, perform the complete read-only co-review, run existing validation commands, and present per-case approval/revision/rejection recommendations. No additional permission is needed for that analysis. The engineer must pause only before changing labels, recording approvals, regenerating corrected records, or expanding the corpus; those writes require the owner's response to the review findings.

Recommended sequence:

1. Read each pending case in `evaluation/corpus/pilot-v0.1/reviews/pilot_review_packet.md` and follow its link to the underlying JSONL record.
2. Review semantic relationship independently of authority.
3. Review disposition against explicit authority, temporal, and safety metadata.
4. Review state effect against checkpoint truth and historical assertions.
5. Review external action only when an action-selection task exists.
6. Verify evidence IDs, source status, snapshot hash, checkpoint, and downstream gold.
7. Present a complete co-review with a proposed `approve`, `revise`, or `reject` disposition for every pending case, including any concrete correction required. Do not stop merely to ask permission to perform this review.
8. After the owner accepts the recommendations, record approved decisions and corrections in generated source plus tests; do not hand-edit only the rendered packet.
9. Rerun generation, the complete test suite, and the mock smoke harness.
10. Record a new non-passing G3 experiment entry with the manifest hash and review count.

Only after all 13 cases pass human review should the owner be asked for explicit authorization to generate the full 30-history/120-pair development pilot. The previous review explicitly did **not** authorize expansion.

## 11. Commands for verification

From the repository root:

```sh
uv run --frozen python scripts/generate_g3_pilot.py
uv run --frozen pytest -q
uv run --frozen python scripts/run_g3_pilot_smoke.py
```

In the managed sandbox, redirect the uv cache if needed:

```sh
UV_CACHE_DIR=/tmp/lifetime-ai-uv-cache uv run --frozen pytest -q
```

Expected current result: 40 tests pass; 13 cases pass schema validation; all three mock tracks run; evaluator leakage failures are zero; model calls are zero.

## 12. Explicitly unauthorized next actions

Until the owner says otherwise, do not:

- generate the 30-history/120-pair corpus;
- create, inspect, score, or tune against any final gate holdout;
- implement or call an LLM;
- add embeddings or vector search;
- implement learned models or generate model predictions;
- connect production or proprietary systems;
- add an agent framework or UI;
- claim G3 completion;
- begin G4 threshold selection.

Mocks are contract tests only and are not experimental baseline results.

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

Some status prose in the in-progress roadmap/gates edits still describes the pre-G0 state. Until the owner reconciles those documents, the accepted experiment records under `experiments/g0`, `experiments/g1`, and `experiments/g2` are the authoritative evidence that G0–G2 passed. The latest G3 experiment record is authoritative for the partial review count.

Before editing, always run `git status --short`. Stage only task-specific files.

## 16. Suggested first response in the next session

Confirm that you have read:

1. this handoff;
2. `docs/g3_evaluation_design_proposal.md`;
3. the G3 section of `docs/gates.md`;
4. `experiments/g3/20260919-1025-partial-human-review/summary.md`;
5. the review packet and the eight pending records.

Then proceed directly through the complete read-only co-review of all eight pending cases and present per-case recommendations. Do not ask for another authorization merely to inspect or evaluate them. Do not modify data until the owner accepts the recommendations, and do not interpret “continue” as permission to expand the corpus or access a final holdout.
