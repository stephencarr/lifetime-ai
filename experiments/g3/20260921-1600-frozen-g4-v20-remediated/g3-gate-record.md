# Gate evaluation: G3 — 20260921-1600-frozen-g4-v20-remediated

## Claim

The evaluation corpus and baselines can fairly test the thesis.

## Build identity

- Worktree: `/private/tmp/lifetime-ai-g3` (branch `codex/complete-g3`)
- Base commit: `b6e407d5e875c91da527b9dc1d6671adcedc6ae3` ("fix(g3): bind seal to reviewer identities")
- Working tree clean: **no** — see "Uncommitted changes" below; this record documents work not yet committed.
- Dependency-lock hash (`uv.lock` SHA-256): `bcfd91f05df0650318d5afb550175b2586770de59955449250cb4ddab9cc62cd`

## Environment

- Hardware: Apple Silicon (arm64), consistent with prior gate records
- OS: macOS
- Python: 3.13.4
- uv: 0.12.17
- No LLM, embeddings, or vector-store dependency invoked at any point in this evaluation

## Why this record exists

The corpus inherited from commit `b6e407d` (registry v15/v16 seal) was independently audited by three rounds of adversarial cold review during this session, spanning three real defects found and fixed, one structural instability found and fixed, and three lower-severity items triaged and consciously accepted for this POC. This record supersedes the `20260921-1207-frozen-g4-v16` record: that record's `sealed_manifest_sha256` (`f6f41c49...`, corresponding to the `frozen-g4-v0.1-sealed-v16`/`-v17` directories) is **not** valid evidence of a defect-free corpus. Do not cite it as the current G3 evidence.

## Frozen procedure

- Dataset/configuration hash: registry `cc95e911353bf43fdb73e2e409570c77f0638a4fb2f1a9b9c4d5cb96941a7413`, sealed manifest `30310fcd9d36e37d0584f60d640164e9d5ec1b893ebaaad13b16bc8ed2834f12`
- Sealed corpus path: `evaluation/corpus/frozen-g4-v0.1-sealed-v20/`
- Review record: `evaluation/corpus/frozen-g4-v0.1-sealed-v20/review-record.json` (copied into the sealed directory by `seal_staged_corpus`; source built at `evaluation/corpus/frozen-g4-v0.1-review-v20/review-record-v20.json`)
- Near-duplicate adjudication: `evaluation/corpus/frozen-g4-v0.1-sealed-v20/near-duplicate-adjudication.json` (empty candidate set, consistent with all prior versions)
- Commands executed, in order:
  ```sh
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen pytest -q
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen python scripts/render_frozen_g4_blueprints.py \
    --output evaluation/blueprints/frozen-g4-v0.1/registry-v20
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen python scripts/stage_frozen_g4_corpus.py stage \
    --blueprints evaluation/blueprints/frozen-g4-v0.1/registry-v20 \
    --authoring-matrix evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json \
    --output evaluation/corpus/frozen-g4-v0.1-staging-v20b
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen python scripts/stage_frozen_g4_corpus.py seal \
    --staging evaluation/corpus/frozen-g4-v0.1-staging-v20b \
    --review-record evaluation/corpus/frozen-g4-v0.1-review-v20/review-record-v20.json \
    --duplicate-adjudication evaluation/corpus/frozen-g4-v0.1-review-v20/near-duplicate-adjudication-v20.json \
    --output evaluation/corpus/frozen-g4-v0.1-sealed-v20
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen python scripts/stage_frozen_g4_corpus.py verify \
    --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v20
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen python scripts/run_g3_frozen_smoke.py \
    --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v20
  UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run --frozen pytest -q   # rerun after seal, confirms no regression
  ```
- Deviations from the originally-approved second-freeze plan: three corpus-authoring defects were found post-approval and repaired (see "Findings and remediation" below); this is explicitly permitted by the phase rule ("blinded gold adjudication and structural validation before sealing are permitted") since no model predictions were ever generated or consumed.

## Results

| Criterion | Required | Observed | Pass/Fail |
|---|---:|---:|---|
| Final corpus is whole-family split, pinned, sealed, and independently verifiable | — | `verify` command passes; manifest hash matches recomputation | PASS |
| Development/holdout split | 270/135 | 270/135 | PASS |
| Histories / pairs / families | 405 / 1,620 / 135 | 405 / 1,620 / 135 | PASS |
| Two independent reviews cover every history and pair | — | 405/405 history_approvals, all `disposition: approved` | PASS |
| Difficult histories receive second review | >=10 | 45/45 difficult histories have >=2 distinct reviewer_ids | PASS |
| Near-duplicate candidates adjudicated | — | empty candidate set, hashed empty adjudication artifact | PASS |
| Evaluation policy frozen without learned predictions | — | `g4-evaluation-v0.1.json` status `FROZEN_AT_G3_MODEL_FREE`; `model_predictions_authorized: false` | PASS |
| Ordinary/oracle projections and baseline contracts pass model-free smoke | — | 4/4 baseline contract smokes PASS, 0 evaluator leakage failures, 0 learned model calls | PASS |
| Full automated test suite | all pass | 101/101 pass (re-run after seal) | PASS |
| Zero unauthorized/fabricated content in gold labels (this session's specific finding) | 0 | 0 (see remediation below; independently re-verified post-fix) | PASS |

## Findings and remediation (this session)

Three real corpus-authoring defects were found by adversarial cold review (not caught by prior structural/algorithmic review), root-caused in `lifetime_ai/evaluation/initial_authoring.py` and `scripts/generate_frozen_g4_authoring_matrix.py`, fixed, and independently re-verified by both automated queries and fresh adversarial review agents:

1. **`expected_external_action: "outreach_candidate"` fabricated** on `commitment_resolution` and `preference_reinforcement` pairs with no outreach/contact content in any source event (67 instances corpus-wide, 0 with supporting content anywhere). Fix: removed the unconditional label-override mechanism entirely rather than exempting archetypes one at a time; `outreach_candidate` removed from `actions_per_partition` coverage requirement. Verified: 0 occurrences post-fix.
2. **`canonical_payload.sensitivity: "sensitive"` fabricated** on snapshots in `sensitive_state`-tagged families with no confidentiality/PII/restriction language in any source event (0 of 1,437 instances were grounded, corpus-wide). Fix: `sensitivity` is always `"normal"` now.
3. **`sensitive_state` feature tag itself was never implemented with real content** in any special-case branch (unlike every sibling feature). Fix: removed from the corpus vocabulary entirely (`FEATURES`, `SECONDARY_FEATURES_BY_RELATIONSHIP`, `feature_minimum_histories` coverage requirement) rather than authoring new confidentiality content for 78 histories — an explicit POC-scope trade-off, not a claim that the feature couldn't be done properly later.

One structural defect, independent of the above, was also found and fixed: the whole-family development/holdout assignment algorithm (`assign_frozen_g4_families`, `lifetime_ai/evaluation/frozen_g4.py`) broke ties using a hash of each family's *full* spec content, including opaque rendered-history hashes — so correcting any gold-label content (even without changing declared stratification labels) could cascade into unrelated families moving between partitions. Fixed to key the tie-break rank only on declared stratification labels. Verified: identical partitions are now produced across multiple rounds of unrelated content correction; the split changes only when declared labels genuinely change (as it correctly did in step 3 above, when families lost the `sensitive_state` label).

## Findings triaged and accepted for POC (not fixed; recorded in `review-record.json`'s `review_findings` as `rejected` with rationale)

- `semantic_relationship: "unrelated"` on deletion events that cause `expected_state_effect: "invalidate"` — accepted as intentional design (deletion is a lifecycle mechanism independent of the semantic-relationship axis), consistent with existing project precedent (see `docs/lifetime_ai_handoff.md` section 8, pilot-08).
- Raw generator identifiers (e.g. `g4-h040-2-e1`) as dict keys in `evaluator_only.deleted_source_content` — confirmed cosmetic only; the field is never read by `lifetime_ai/evaluation/projection.py`, so it is never exposed to any system or baseline under test.
- Templated `adjudication_notes` text on some `late_or_retroactive_report` pairs that doesn't precisely match the cited event's retroactive-timing signal — the four gold-label axes themselves are correct in every case (the pair's own `ambiguity_reason` field carries the correct rationale); only the redundant prose is imprecise.

All three are explicitly flagged for post-POC content-authoring engineering, not silently dropped.

## Decision

PASS

## Rationale and next action

The corpus, as sealed in `evaluation/corpus/frozen-g4-v0.1-sealed-v20/`, is free of the fabricated-content defect class that this session found and fixed, is partition-stable under further legitimate correction, passes all structural/model-free verification, and has genuine (not rubber-stamped) two-reviewer coverage recorded honestly, including three consciously-accepted lower-severity findings. This satisfies the G3 pass criteria in `docs/gates.md` for a POC-scoped corpus.

Next action: commit the sealed corpus, review record, and generator fixes; update `docs/gates.md`'s gate-status table to G3 PASS with a link to this record; retire `docs/g3_completion_handoff.md` (superseded); update `docs/lifetime_ai_handoff.md` to reflect the new gate state and hand off to G4 planning. G4 model implementation, predictions, and holdout evaluation remain separately unauthorized per `evaluation/config/g4-evaluation-v0.1.json` (`model_predictions_authorized: false`) and require a distinct authorization decision from the project owner before any model call is made against this corpus.
