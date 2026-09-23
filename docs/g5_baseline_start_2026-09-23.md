# G5 Baseline A start — 23 September 2026

**Status:** Comparison design started; no G5 baseline run or gate claim.

The current `MockRollingSummaryBaseline` in `lifetime_ai/evaluation/contracts.py` is a contract test double: it retains only the last four strings and does not answer state questions with retrieval or citations. It is not a competent G5 comparator.

The first implementation task is a real rolling-summary-and-retrieval adapter behind `EvaluationSystem`. It must ingest the same ordered event projection as the proposed architecture; maintain a bounded rolling summary; keep source-linked searchable event records; process correction and deletion/invalidation events; and answer the same checkpoints with current state, evidence links, abstentions, and raw lifecycle usage. Neither system receives gold state, evaluator labels, or privileged candidate identifiers. The limited oracle remains diagnostic only.

Record at least ingestion/extraction, consolidation, retrieval, model calls and tokens, elapsed time, local compute, and human repair for **both** systems. Choose the same swappable local model access and comparable context allowance before scoring. Freeze histories, checkpoints, metric definitions, and exclusion rules before a G5 holdout run; use development histories for engineering. The G5 pass rule and safety conditions remain those in `docs/gates.md`.

Next code step: implement the non-mock Baseline A adapter and paired development runner, then verify equal source access and complete usage accounting before any score comparison. The synthetic M5 chat preflight cannot substitute for this paired experiment.
