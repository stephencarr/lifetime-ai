# M5 local chat synthetic preflight — 23 September 2026

## Decision

The 18-scenario synthetic development preflight now meets its frozen v0.1 thresholds on the repaired implementation. This is **not** participant UAT readiness or a G5 pass. The rule extractor was repaired after the first scored run on these same cases, so the final pass is development evidence, not independent generalization evidence.

**Later answer-contract regression:** A fourth retained run after the retrieval/answerability repair fails one old answer label: distinct tea and coffee preferences were called `conflict` by v0.1. Under the new support contract they are compatible and need clarification. See `experiments/m5_preflight/20260923-synthetic-v01/attempt-04.json` and `docs/m5_answerability_development_2026-09-23.md`. The historical v0.1 labels and earlier results remain unchanged.

**Later development finding:** The local UI subsequently showed brittle literal retrieval and an `answered` outcome for evidence that did not establish the question's general scope. See `docs/m5_retrieval_answerability_gap_2026-09-23.md`. This does not retroactively change the frozen scores; it adds a blocking answer-quality requirement before participant UAT.

## Frozen instrument

- Cases: `evaluation/m5_preflight/v0.1/cases.json` (SHA-256 `9606c62db2df4fbf4ca264cc30f22b0e1976bfbe2ab403761cdd067ba5ff160d`)
- Criteria: `evaluation/m5_preflight/v0.1/criteria.json` (SHA-256 `ce7d451abce8800b0bff73a62938ce355853e3307fc66e002586163cd8cf5d17`)
- Freeze record: `evaluation/m5_preflight/v0.1/freeze.json`
- All scenarios and per-step failures are retained in `experiments/m5_preflight/20260923-synthetic-v01/attempt-01.json` through `attempt-03.json`.

The corpus includes direct preference and commitment capture, a common paraphrase, irrelevant and third-party messages, quoted and conditional text, unsupported time scope, duplicates, conflicts, explicit correction, ordinary time change, restart, citations, and source invalidation.

## Results

| Metric | First run | Final run | Frozen threshold |
|---|---:|---:|---:|
| Positive captures | 10/12 | 12/12 | ≥90% |
| Safe abstentions | 4/9 | 9/9 | 100% |
| Active state checkpoints | 20/27 | 27/27 | 100% |
| Answer outcomes/content | 9/11 | 11/11 | 100% |
| Citation checks | 8/11 | 11/11 | 100% |
| Fresh-process restart checks | 4/4 | 4/4 | 100% |
| Deleted source leaks | 0 | 0 | 0 |
| Failed-expectation proxy per 20 messages | 20.0 | 0.0 | ≤1 |

The initial failures were the ordinary paraphrase, quoted text, question and conditional capture, a dated commitment, duplicate capture, and an explicit time change. The repairs narrowed unattended promotion, added a deterministic source witness check in the validator, deduplicated current claims, and allowed a specific witnessed replacement. A later review fixed deletion replay to use the recorded deletion timestamp. The frozen files were unchanged for all three attempts.

## Remaining conditions before participant UAT

1. Predeclare and run an **independent participant-approved local sample**. Include ordinary positive, irrelevant, third-party, quoted, conflicting, changing, and deletion cases. Keep every miss and false capture. This development set cannot establish raw-message quality beyond its wording.
2. Agree on the unattended promotion/correction policy and the user's deletion expectation. `:forget` prevents retrieval and invalidates derived state, but the local ledger still retains original text. It is not physical erasure.
3. Measure actual human repair time and task usefulness. The synthetic report's repair metric is only a count-based proxy.
4. Only then consider a bounded participant UAT. Formal G5 separately requires the paired longitudinal Baseline A comparison, full lifecycle cost accounting, and the safety invariants in `docs/gates.md`.

No G4 holdout material, private `.uat` data, or participant messages were used here.
