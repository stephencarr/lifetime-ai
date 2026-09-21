# G3 development-pilot expansion — 20260919-1206

## Status

`DEVELOPMENT_PILOT_GENERATED_AWAITING_REVIEW` — the authorized 30-history/120-pair development pilot has been generated and passes automated instrument checks. All annotations remain pending human review. G3 is **not complete**.

## Build identity

- Commit at generation time: `24c662263aa773136536083ced7f018386ff24ec`
- Working-tree changes: present; this record describes the regenerated corpus and instrument
- Dependency-lock SHA-256: `1438f893cdae63babf1cf48af8520fcfbe84946f0f5e42c9225904eb16218861`
- Pilot-v0.2 manifest SHA-256: `7c50f6e0bbfa417eecec62817e5d7ee352b6e156325bc477a69f7d48e6b1a128`

## Corpus result

- 30 synthetic whole histories and 120 independently labelled event-candidate pairs generated.
- Deterministic split: 21 `pilot_development`, 9 `pilot_holdout`.
- Ten template families remain whole within one partition.
- Each semantic relationship has 20 pairs.
- The declared disposition, effect, action, feature, lifecycle, hostile-case, and multi-pair coverage checks pass.
- All 120 pair decisions and 30 history/checkpoint decisions are unreviewed.

The `pilot_holdout` partition exercises pilot split and sealing machinery only. It becomes development material after review and is not a final gate holdout.

## Automated validation

- Complete test suite: `50 passed`.
- Candidate-retrieval mock track: 120 pairs.
- Pair-classification mock track: 120 pairs.
- End-to-end mock track: 30 histories.
- Each of four baseline mocks executed all 30 histories.
- Schema validation: pass.
- Evaluator-only leakage failures: 0.
- Model calls: 0.
- Embeddings/vector search: absent.
- Production connections: absent.
- Final G4/G5/G6/G7 holdouts inspected or created: no.

## Review status

The review packet provides a decision for every pair plus a separate history/checkpoint decision. Difficult classes require a second reviewer. A requested GTL reassessment of the corrected build could not run because that agent reached its usage limit; this is recorded as unavailable and is not counted as approval.

## Decision

`NOT_EVALUATED`

The exact next step is complete human review of all 120 pair labels and all 30 history/checkpoint groups. Corpus expansion, model predictions, final holdout work, and G3 completion claims remain out of scope until that review is resolved.
