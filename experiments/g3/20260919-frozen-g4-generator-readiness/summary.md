# Frozen G4 Generator Readiness

**Date:** 2026-09-19  
**State:** Freeze plan approved; final corpus generation not yet ready or attempted  
**Holdout state:** No final G4/G5/G6/G7 holdout was generated, exposed, inspected, or scored.

## Approved plan

The second-freeze review passed and is recorded in `experiments/g3/20260919-second-freeze-plan-review/summary.md`. Its approval boundary is limited to corpus generation, blinded gold adjudication, structural validation, and sealing. No model run, prediction, threshold tuning, G3 pass, or G4 evaluation is authorized by that review.

## Implementation feasibility finding

A read-only peer inspection found the pilot implementation cannot safely be scaled into the approved final corpus:

- The pilot schema/validator permits only pilot versions and pilot partitions.
- Pilot coverage checks are fixed at 30 histories and a 21/9 split, and do not require all final lifecycle effects.
- The pilot generator is a chained revision stack over 30 records and 10 repeating template families; renumbering/repeating it would not create 135 distinct family clusters and would increase surface-pattern leakage risk.
- The pilot splitter does not implement the exact 90/45-family final split.
- The pilot manifest does not capture every transitive generator dependency needed for a reproducible frozen corpus.

## Completed separate-path foundation

- Added `evaluation/schema/frozen-g4-history.schema.json`; the existing pilot schema remains intact.
- Added `evaluation/config/frozen-g4-v0.1.json` with the approved scale, split, cluster/exclusion assumptions, and coverage rules.
- Added `lifetime_ai/evaluation/frozen_g4.py` for frozen-schema, semantic/reference, family/split, pair-ID, class/family, disposition/effect/action, and baseline-favoring coverage validation.
- Extended `validate_history` with optional schema/stage/partition arguments while preserving pilot defaults. The pilot schema selector now uses an exact `$id`, avoiding collision with the new frozen schema.
- Added `tests/test_frozen_g4.py`; its repeated pilot-derived data are synthetic validator fixtures only and are explicitly not benchmark data.

## Verification

- Initial foundation tests: **54 passed**.
- Pilot smoke: **PASS** for all four mock baseline contracts, 30 histories/120 pairs, zero model calls, and zero projection leakage failures.
- Existing v0.7 manifest checksum: **verified**.
- No corpus-generation command was run.

## Remaining work before corpus generation

Implement a new standalone frozen-G4 pipeline driven by 135 distinct declarative family specifications. It must freeze an exact deterministic 90/45 whole-family split, render exactly three histories and four pair opportunities per family, reject duplicate/near-duplicate cross-family content, perform the approved coverage checks, and manifest all direct/transitive source, schema, config, and spec hashes. Generate first into a new staging directory; then obtain blind independent review of all histories/pairs, resolve findings before sealing, and create the final immutable hashes/access record. Do not adapt or multiply the v0.7 template families to meet the count.

## Post-review hardening (2026-09-19)

Two independent code reviews returned **REVISE**. The validator foundation was hardened without generating corpus content:

- Candidate item IDs must match snapshot item IDs; lifecycle targets must exist; invalidation accepts deletion or redaction.
- Frozen checkpoint historical assertions are required to preserve content-bearing events, including unauthorized sources; semantic-item task gold is checked against checkpoint propositions/scopes/evidence; frozen feature tags must be declared; neutral cases no longer count as baseline-favoring.
- Frozen corpus coverage rejects exact normalized family-text duplicates and very high token-set Jaccard similarity; the misnamed planned accept count was corrected.
- The former replicated-pilot “positive corpus” test is now a negative test proving that relabeling pilot families is rejected. The latest full regression suite passes **66 tests**; `git diff --check` passes.

The split implementation now derives all size/coverage constants from the frozen config and assigns whole families via deterministic multi-label balancing over dominant relationship, features, difficulty, expected-favor, deletion presence, and ambiguity presence. Seed+spec-hash ordering breaks ties; deterministic improving swaps are followed by explicit per-dimension deviation checks, and the manifest records labels, targets, observations, and deviations. Frozen current-state task gold is constrained to an explicit five-field answer projection and compared with checkpoint gold; feature quotas require the exact union of pair-gold tags.

Further hardening added a closed family-spec schema with hashes for each of the three rendered histories; validation binds complete rendered semantic content to those hashes and still requires a pinned family-registry SHA-256. The pin remains deliberately `null` until substantive specifications exist and are independently reviewed, so final coverage validation remains fail-closed. Frozen state effects now compare pre/post checkpoints, include derivative deltas, reject undeclared changes, enforce prior-state requirements for lifecycle operations, and require exact action-selection gold fields. Runtime assertion, derivative, and semantic-item IDs are checked for within-checkpoint duplication and across-history/namespace collisions. Near-duplicate screening covers rendered textual fields beyond timeline content, and successful validation requires a schema-checked, blind, hashed adjudication artifact for every above-threshold candidate. The latest full regression suite passes **75 tests**; `git diff --check` passes. Both independent peer reviews now PASS the engineering foundation.

This still does **not** clear the generation gate. The 135 substantive family blueprints and their rendered histories do not yet exist; consequently the family-registry hash is unpinned, the real split’s tolerance feasibility is unproven, and no blind adjudication or corpus-wide review artifact exists. Current structural fixtures are deliberately pilot-derived and invalid for benchmark use; they prove validator behavior, not corpus validity or coverage. The two PASS reviews apply to the engineering foundation only, not to absent data or generation outputs. No final family specifications, histories, model predictions, or holdout were generated or accessed.
