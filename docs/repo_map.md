# Lifetime AI — Repository Map

**Purpose:** a single reference for what exists on disk and why, so a new agent or engineer doesn't have to rediscover it by grepping. This is a map, not a status report — for current gate status and next steps, read `docs/lifetime_ai_handoff.md`.

## Documentation (`docs/`)

| File | What it is | Trust level |
|---|---|---|
| `lifetime_ai_handoff.md` | The primary engineering handoff. Historical context (sections 1-9) plus current gate status and next steps. **Read this first.** | Current |
| `g3_completion_handoff.md` | The detailed G3 defect-and-remediation narrative: what was wrong with the original v16/v17 seal, what was fixed, in what order. Read once, for context; not needed for day-to-day work once you trust the summary in this file and `lifetime_ai_handoff.md`. | Current, but layered with corrective addenda — read the top-of-file notes before the body |
| `gates.md` | The full Evidence Gates v0.1 specification: entry conditions, required scenarios, pass criteria, and required evidence for every gate G0-G8. This is the actual rulebook the project is held to. | Current, authoritative |
| `g3_evaluation_design_proposal.md` | The design rationale behind the frozen-G4 corpus: why whole-family splitting, why four independent gold axes, the scenario coverage matrix, leakage/ambiguity/benchmark-gaming risk analysis. Read before touching corpus generation or evaluation contracts. | Current, authoritative for corpus design |
| `g2_mutation_boundary.md` | Short note on the G2 typed-transition-pipeline mutation boundary. | Current, narrow scope |
| `lifetime_ai_roadmap_v0.2.md` | Longer-range roadmap prose. | Read for context, not gate-authoritative — `gates.md` and `lifetime_ai_handoff.md` win on any conflict |
| `archive/lifetime_ai_roadmap_v0.1.md` | Superseded roadmap. | Historical only |

## Gate evidence (`experiments/`)

Every gate evaluation lives under `experiments/<gate>/<run-id>/` per the record template in `docs/gates.md` section 6. For G3 specifically, there are many run-id directories reflecting the corpus's iteration history:

- `experiments/g3/20260921-1600-frozen-g4-v20-remediated/g3-gate-record.md` — the criterion-by-criterion G3 PASS record. Has an addendum at the top noting it was superseded by v21 for tooling (not content) reasons.
- `experiments/g3/20260922-1351-v21-evidence-builder-remediation/g3-gate-remediation.md` — the evidence-builder tooling fix record (oracle leak, hash pins, review-finding validation). Has its own corrective addendum from a follow-up fix.
- `experiments/g3/20260921-1207-frozen-g4-v16/` — **superseded, do not cite.** This was the original (defective) G3 PASS claim; adversarial content review found real fabricated-content defects here that a schema/hash-only review had missed.
- Everything else under `experiments/g3/` (dated 20260918-20260919) is the pre-frozen-corpus development-pilot history — real, but superseded by the frozen corpus for G3 purposes.
- `experiments/g0/`, `experiments/g1/`, `experiments/g2/` — accepted, uncontested evidence for the earlier gates.

**Rule of thumb:** the newest `g3-gate-record*.md`/`g3-gate-remediation*.md` file is authoritative. Older ones are audit trail.

## Corpus and blueprint data (`evaluation/`)

This directory has accumulated a lot of versioned intermediate output. All of it is real audit history (each version corresponds to a real defect found and fixed, or a real generation attempt), but only the latest sealed version is current evidence.

- **Current, authoritative:** `evaluation/corpus/frozen-g4-v0.1-sealed-v21/` — the sealed corpus. Manifest hash `9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3`. Verify with `uv run --frozen python scripts/stage_frozen_g4_corpus.py verify --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v21`.
- **Superseded, do not use as evidence:** every other `evaluation/corpus/frozen-g4-v0.1-{staging,sealed,review}-v*` directory (v3 through v20b). Each exists because a real bug was found in its predecessor. Do not delete without checking with the project owner — they are the audit trail proving the defect-fix history actually happened — but never treat any of them as current.
- `evaluation/blueprints/frozen-g4-v0.1/registry-v*/` — the per-family blueprint JSON files that get staged into a corpus version. `registry-v20/` is what `sealed-v21` was staged from (v21 only changed evaluation tooling, not corpus content, so the registry didn't need to move to v21).
- `evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json` — the frozen per-family authoring plan (which relationship, features, difficulty each family gets). Regenerating this requires `scripts/generate_frozen_g4_authoring_matrix.py`; it refuses to overwrite an existing file.
- `evaluation/corpus/pilot-v0.*/` — the pre-frozen-corpus development pilots (30 histories each). Real, reviewed, but explicitly **not** a final gate holdout for any gate. Superseded by the frozen corpus for G3 purposes.
- `evaluation/config/frozen-g4-v0.1.json` — the corpus's structural/coverage contract (partition sizes, feature minimums, action/effect/relationship vocabularies). Pins the current registry hash; must be updated whenever the registry changes.
- `evaluation/config/g4-evaluation-v0.1.json` — the frozen G4 evaluation policy (decision thresholds, calibration procedure, severity policy). Status `FROZEN_AT_G3_MODEL_FREE`; `model_predictions_authorized: false`. `cost_and_lifecycle_accounting` is currently an empty object — no price table exists yet — which blocks any G4 cost-comparison claim, independent of the authorization decision.
- `evaluation/schema/*.schema.json` — JSON Schema definitions for every corpus/review/adjudication artifact. `frozen-g4-review-record.schema.json` is the one that actually gates whether a review record is well-formed; `lifetime_ai/evaluation/frozen_g4_pipeline.py`'s `seal_staged_corpus`/`verify_sealed_corpus` enforce it directly.

## Code (`lifetime_ai/`, `scripts/`)

| Path | What it does |
|---|---|
| `lifetime_ai/evaluation/initial_authoring.py` | The actual corpus generator: builds histories, events, candidate snapshots, and gold labels from the authoring matrix. This is where the three fabricated-content defects (outreach_candidate, sensitivity, sensitive_state) were rooted and fixed. |
| `lifetime_ai/evaluation/frozen_g4.py` | Coverage validation and the whole-family development/holdout assignment algorithm (`assign_frozen_g4_families`). The holdout-stability fix (tie-break keyed on declared labels, not opaque content) lives here. |
| `lifetime_ai/evaluation/frozen_g4_pipeline.py` | The stage → seal → verify pipeline (`stage_blueprint_registry`, `seal_staged_corpus`, `verify_sealed_corpus`, `_apply_blind_review`). This is what actually enforces the review-record schema and content-hash binding at seal time. |
| `lifetime_ai/evaluation/projection.py` | Builds the ordinary/oracle/retrieval/classification projections a real or mock system would see. `build_limited_oracle_projection`'s `sequence` parameter is a real temporal-visibility cutoff — see the fixed oracle-leak bug in `run_g3_frozen_smoke.py` for why this matters. |
| `lifetime_ai/evaluation/contracts.py` | The four mock baseline dataclasses (rolling-summary, scheduler, general-LLM, oracle) plus `PredictedRelationship` (the six-class probability contract a real G4 model prediction would need to satisfy). |
| `scripts/generate_frozen_g4_authoring_matrix.py` | Generates `authoring-matrix.json` deterministically from the frozen config. Refuses to overwrite. |
| `scripts/render_frozen_g4_blueprints.py` | Calls `initial_authoring.build_blueprints()` and writes a new `registry-v*/` directory. Refuses to overwrite. |
| `scripts/stage_frozen_g4_corpus.py` | CLI wrapper for `stage` / `seal` / `verify`. This is the actual pipeline entry point — use this, not `build_g3_frozen_evidence.py`, to move a corpus version forward. |
| `scripts/run_g3_frozen_smoke.py` | The model-free smoke test: runs all 405 histories through all four mock baselines and checks for projection leakage. No model calls. |
| `scripts/build_g3_frozen_evidence.py` | Builds the machine-readable evidence packet (class distributions, dataset card, gate record) from an already-sealed corpus. **Caution:** this script has two entry points (`review-artifacts`, `evidence`) that don't fully share validation logic — see "known rough edges" below. The actual v20/v21 evidence for this project was hand-built and independently verified rather than generated by this script's `evidence` subcommand. |
| `lifetime_ai/evaluation/split.py` | **Dead code for this purpose.** Pilot-era whole-family splitting (`split_whole_families`, `split_stratified_families`), used only by the old `scripts/generate_g3_pilot*.py` / `scripts/generate_g3_development_pilot*.py` scripts. Does not share the holdout-instability defect that `frozen_g4.py`'s `assign_frozen_g4_families` had, because it never hashed rendered content. Leave alone; not part of the frozen-G4 pipeline. |

## Known rough edges (non-blocking, worth fixing eventually)

- **`scripts/build_g3_frozen_evidence.py`'s two entry points don't share one validation path.** `build_review_artifacts()` validates review findings; `build_evidence()` didn't for a while, and even after a fix, both still duplicate a good deal of logic (hash checking, staged-candidate assertion) rather than one calling the other. Three review rounds during the G3 remediation each found a real gap here. If you touch this script again, consider making `build_evidence()` always run `build_review_artifacts()`'s validation, or collapsing the two entry points into one.
- **`evaluation/config/g4-evaluation-v0.1.json`'s price table is empty.** A dated, real price table must be frozen before any G4 cost-comparison claim can be made — this is explicit in the gate record's own deviations list, not a surprise.
- **Many superseded corpus directories remain on disk** (`evaluation/corpus/frozen-g4-v0.1-*-v3` through `-v20b`). They're real audit trail; ask the project owner before deleting any of them, but never treat a non-latest one as evidence.
