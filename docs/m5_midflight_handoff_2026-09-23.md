# M5 semantic product work — mid-flight handoff, 23 September 2026

> **Superseded, 24 September 2026.** Work on this branch has stopped. See
> [the closing note](m5_closing_note_2026-09-24.md) for why, what was measured, and what
> a future attempt would need. The branch-state and retained-evidence sections below
> remain accurate; the "next engineering decision" section is no longer the plan.

## State of the branch

This is a work-in-progress engineering snapshot on `codex/m5-semantic-wip`. It preserves the diagnostic chat/UI work, the first local-model construction and answer path, all frozen synthetic development instruments, and every scored failure. The local-model path is a terminal route; the browser still runs the diagnostic rule path. Neither route is approved as evidence that the Lifetime AI concept works for ordinary participant use. Participant UAT remains paused. Formal G5 is a separate paired baseline comparison.

The user asked for an actual first iteration of claim construction, correctness checking, and source-grounded retrieval that can become the product, including a credible path beyond 128 claims. The [architecture reset](m5_poc_architecture_reset_2026-09-23.md), [answer contract](m5_answer_contract_2026-09-23.md), and [model development record](m5_model_development_2026-09-23.md) explain the intended path and the measured gap. The 128-claim scan is confined to the diagnostic answer route; it is not a product-scale design.

## Implemented paths and their limits

- The diagnostic `lifetime-chat` and `lifetime-web` route persists source-linked state and exercises capture, retrieval, correction, and source invalidation. Its explicit rule extractor and finite answer grammar are development controls. The repaired 18-case capture preflight and 48-question answerability preflight are synthetic development evidence only. The answer route abstains when its bounded scan is incomplete.
- The separate `lifetime-model-chat` route uses pinned local Qwen3-8B generation and BGE embeddings, structured claim proposals, a source-support check, semantic reconciliation, SQLite canonical state and FTS5, USearch HNSW candidates, and a cited answer verifier. Model outages abstain; there is no keyword-only product fallback. The same generator still proposes and verifies claims, and the frozen integrated instrument has **not passed**.
- SQLite schema 5 stores packed float16 embeddings and streams active rows to rebuild HNSW. Deleting a source uses the existing source-ID index to find affected model claims. Query search uses HNSW, but startup rebuilds the full ANN and Python key map. Persisted checkpoint replay, account partitioning, deletion consistency at scale, and complete broad-inventory queries remain unimplemented.
- The independent local ModernBERT NLI candidate is an offline diagnostic. It failed its own frozen false-support gate and is **not** integrated as the final truth authority.

## Retained measured evidence

- [Integrated model instrument](../evaluation/m5_model_poc/v0.1) has 18 scenarios, 22 messages, and 22 questions. Four attempts are retained in [`experiments/m5_model_poc`](../experiments/m5_model_poc). Best attempt 03 captured 13/14 clear claims, falsely captured 1/8 negatives, and answered 8/10 supported questions, with 10/10 candidate recall on this small set. Attempt 04 regressed to 6/14 clear captures, 1/8 false captures, and 5/10 supported answers; it rejected direct preferences and promoted gratitude as durable state. These are failures, not UAT scores.
- [Independent-model synthetic NLI instrument](../evaluation/m5_nli_preflight/v0.1) has 48 frozen source/hypothesis pairs. [Attempt 01](../experiments/m5_nli_preflight/attempt-01.json) accepted 21/24 positives and falsely supported 1/24 negatives, including an injected storage instruction. [Further diagnostic probes](../experiments/m5_nli_preflight/diagnostic-probes-01.json) show that generic durability hypotheses confuse direct assertions with quotations and miss direct requests and commitments.
- [ANN scale instrument](../evaluation/m5_index_scale/v0.1) has seeded 384-dimensional vectors at 10,000, 100,000, and 1,000,000 entries. [Attempt v0.1](../experiments/m5_index_scale/attempt-01.json) recovered 12/32 planted million-vector queries at top 24 with p95 2.15 ms. A second [frozen configuration](../evaluation/m5_index_scale/v0.2) widened search from 96 to 1024; [attempt v0.2](../experiments/m5_index_scale/v0.2-attempt-01.json) recovered 31/32 with p95 17.18 ms. **Both failed** their frozen 32/32 recall gate. They measure mechanical ANN recovery only, not semantic source retrieval, SQLite population, or full product scaling. See [the scale record](m5_index_scale_2026-09-23.md).

## Verification and evidence boundary

The selected M5 model, store, answerability, chat, web, terminal, and local import tests passed: **32 passed**. `uv lock --check` and `git diff --cached --check` passed after the dev-group adjustment. Model-backed scores above were produced only from checked-in synthetic items; no unseen independent sample has been selected, inspected, or scored. The live local POC database is private and was not used as evaluation data. Manual email import is not extractor evidence. Private `.uat` data and the untracked mailbox in the other checkout must stay out of Git.

A broad test invocation in this work session inadvertently entered legacy G4 tests that reference the quarantined v21 corpus. It was interrupted after four G3 evidence tests failed on a historical `uv.lock` manifest mismatch; the partial run reported 62 passed and 4 failed. The test run may have accessed sealed fixture files before interruption. No G4 test output or holdout content was used to develop or tune M5. Do not repeat the broad suite while it can enter that corpus; run selected M5 tests only. Preserve the sealed manifest and historical artifacts unchanged.

## Next engineering decision

1. Select and validate an independent speech-act, actor, temporal, and scope support component or a more capable local model. Freeze a larger product-shaped development instrument before scoring, including source spans, expected candidate sources, supported answer content, false durable captures, corrections, contradiction, deletion, and abstentions. The 18-scenario set has already been used for development and cannot establish generalization by further prompt tuning.
2. Design a partitioned or sharded ANN and account-filtered candidate path with a durable state-change sequence, verified persisted checkpoints, and crash recovery. Measure realistic semantic queries with distractors, update and deletion visibility, startup time, memory, and answer correctness at 10,000/100,000/1,000,000 claims. Both current single-index million-vector settings failed even the planted-vector gate.
3. Keep broad questions on a complete filtered state enumeration or abstain. Require each reply to be supported by current exact source evidence at the requested actor, scope, polarity, and time; multiple compatible hits do not constitute conflict.
4. Once the integrated development gates pass, run the separately planned [participant-approved independent preflight](m5_independent_sample_protocol.md) without tuning on it. Resolve ledger retention versus physical erasure expectations before participant use. Then run formal G5 separately against the rolling-summary-and-retrieval baseline, including total lifecycle cost.

Do not represent this branch as a successful POC or invite UAT on the strength of the diagnostic UI, the model attempt, or the ANN microbenchmarks.
