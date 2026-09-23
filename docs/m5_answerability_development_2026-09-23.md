# M5 retrieval and answerability development run — 23 September 2026

**Decision:** The literal-match/automatic-answer path has been replaced in the local POC. The new path meets the predeclared aggregate thresholds on a frozen 48-question synthetic development instrument, but this is limited development evidence. Participant UAT remains paused. No independent sample was seen or scored, and formal G5 is separate.

## Frozen before scoring

- Contract: [`m5_answer_contract_2026-09-23.md`](m5_answer_contract_2026-09-23.md).
- Instrument: `evaluation/m5_answerability/v0.1/cases.json` (SHA-256 `d0c6aaa3d8d2aa2a63b2bb42588e9d3f509008db652beea1fc8f722f3b58b28a`).
- Criteria: `evaluation/m5_answerability/v0.1/criteria.json` (SHA-256 `4251f2e6c5328d5a44af5be698b9c9e1165f03e71c5f4f7e3fad6082233656b9`).
- Freeze record: `evaluation/m5_answerability/v0.1/freeze.json`. Twelve isolated scenarios contain 48 questions. Every question names expected candidate source IDs, answer outcome, citation IDs, content where applicable, and whether abstention is acceptable. Families include paraphrase without shared words, inflection, dated context versus general scope, actor, temporal questions, corrections, deleted sources, near matches, compatible claims, and contradiction. The observed rock-climbing failure family is development material.

## Implementation

`Store.retrieve()` now returns all live current claims and their exact source text up to 128 candidates. Exceeding the limit raises an incomplete-retrieval error; `ChatRuntime.ask()` abstains. This gives complete candidate recall for a small local state without depending on query terms. It is an O(number of active claims) POC path, not a scalable semantic retriever.

`lifetime_ai/answerability.py` derives actor, relation, topic, polarity, scope, and time from a declared narrow grammar, checks the question against live claims, and distinguishes `answered`, `uncertain`, `needs_clarification`, and `conflict`. It cites only claims used in the answer or in explaining a genuine ambiguity/conflict. Invalidation removes a source from candidates; correction remains a distinct source. Unknown forms abstain. The browser states these limits and UAT status.

The support check currently accepts only direct local user-message witnesses (plus the validator's exact “keep your answers short” normalization). Manually reviewed observation/email claims remain visible in state but are not promoted into an `answered` response by this grammar. That is an intentional abstention until their actor, source span, and contextual entailment can be represented and verified; the manual import is not extractor evidence.

No model is loaded and there is no silent keyword fallback. General paraphrase and robust semantic entailment are not established. A future model-backed path needs pinned local weights/version, calibration on a separate development set, source-level entailment and contradiction checks, measured latency and cost, and explicit failure behavior when weights are unavailable. The current finite aliases are development scaffolding, not general product evidence. The manually curated email import remains outside extractor evidence.

## Recorded results and retained failures

All item-level predictions, candidate IDs, citations, and failures are retained in `experiments/m5_answerability/attempt-01.json` through `attempt-04.json`. Attempt 02 followed a context-scope repair and regressed one supported answer; attempt 03 repaired explicit-scope questions. Attempt 04 required a direct user-message source witness before answering. No cases or criteria changed between attempts.

| Frozen v0.1 check | Attempt 01 | Attempt 02 | Attempt 03 | Attempt 04 | Threshold |
|---|---:|---:|---:|---:|---:|
| Expected source among candidates, supported questions | 20/20 | 20/20 | 20/20 | 20/20 | ≥95% |
| Correct supported outcome, content, and citations | 20/20 | 19/20 | 20/20 | 20/20 | ≥90% |
| False `answered` on unsupported questions | 0/23 | 0/23 | 0/23 | 0/23 | 0 |
| Valid live citations on responses with citations | 24/24 | 23/23 | 24/24 | 24/24 | 100% |
| False `conflict` on compatible questions | 0/5 | 0/5 | 0/5 | 0/5 | 0 |
| Deleted-source citation leaks | 0/48 | 0/48 | 0/48 | 0/48 | 0 |
| Exact item checks, including instrument citation labels | 44/48 | 43/48 | 44/48 | 44/48 | Report all |

The four exact-check failures in attempts 01, 03, and 04 are `compatible-drinks-q1` and `true-contradiction-q1` through `q3`. The frozen labels set expected citations to empty on non-`answered` outcomes, while the contract and implementation cite the live sources used to explain ambiguity or contradiction. These are instrument-label defects, retained as failures. Attempt 02 also missed `compatible-drinks-q2` after a scope guard treated an explicit “after lunch” question as a general one. That code error is retained in the attempt and fixed in attempt 03. A future version of the instrument can repair the citation labels, but v0.1 must remain immutable and its recorded scores must not be rewritten.

The older frozen 18-scenario capture preflight was rerun as `experiments/m5_preflight/20260923-synthetic-v01/attempt-04.json`. It now fails its `conflicting_preference` answer expectation: the older label treats “I prefer tea” and “I prefer coffee” as a conflict solely because the propositions differ. The new contract treats those as compatible claims requiring clarification. Its capture, abstention, active state, restart, citation, and deletion checks still pass. This historical development preflight does not establish UAT readiness and its frozen label was not altered.

## Remaining work before participant UAT

The independent-preflight task was only queued. Do not tune on or claim an unseen sample. The independent protocol must be amended with question-level retrieval/support labels before any approved local sample is run. The broad synthetic set is hand-authored and uses a small, explicit grammar; 100% supported recall partly follows from scanning all state and says little about larger stores. The 128-candidate cap, untested ordinary paraphrases, incomplete structural claim metadata, and unresolved physical-erasure expectation remain product limits. Participant UAT stays paused; formal G5 still requires its paired baseline and lifecycle accounting.
