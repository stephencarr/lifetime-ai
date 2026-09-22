# G4 final-run runbook

**Status:** procedural template only; this document does not authorize a run.

## Preconditions

The evaluator owner must complete and approve `evaluation/config/g4-final-run-authorization-template.json` as a separate run-specific record. The record must identify:

- the approving owner and approval timestamp;
- the exact frozen repository commit and candidate artifact digest;
- a unique run nonce;
- the exact evaluator command and output directory;
- confirmation that no holdout-derived content was supplied to development or evaluator context.

The evaluator must start from the frozen repository state named in that record. Any mismatch is an abort condition.

## Single-run procedure

1. Verify the authorization record is present, approved, and still matches the commit and candidate digest.
2. Verify the evaluator environment and dependency lock match the recorded run specification.
3. Run the one authorized evaluator command exactly as recorded.
4. Write raw outputs, machine-readable results, logs, and the complete error inventory only to the recorded output directory.
5. Record the commit, authorization digest, run nonce, commands, environment, timing, failures, exclusions, and final decision.

No exploratory search, interactive inspection, threshold adjustment, retry beyond the frozen retry limit, or second holdout run is permitted.

## Immediate abort conditions

- missing, stale, or ambiguous owner authorization;
- commit, candidate digest, policy, or dependency mismatch;
- any holdout content or outcome appears in evaluator input unexpectedly;
- provider, harness, schema, or environment failure prevents the frozen contract from being applied;
- a post-seal defect, outcome-driven exclusion, or request to change thresholds or policy;
- any attempt to start a second final run.

An abort must preserve the raw evidence and be reported as an incomplete or failed run. It must not be silently retried or converted into a pass.

## Post-run reporting

The report must disclose the 22 September 2026 repository-search incident and must not describe the quarantined v21 holdout as literally never accessed. The report must distinguish development measurements from final holdout evidence and must state whether the run completed, aborted, or failed.
