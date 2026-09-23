# M5 retrieval and answerability gap — development finding

**Date:** 23 September 2026

**Decision:** The local browser UI is a state/citation POC, not a reliable question-answering product. Pause participant UAT. The synthetic M5 capture/lifecycle preflight remains valid only for its frozen cases; it does not establish retrieval generalization or answer support. This finding is development evidence, not an independent score or a G5 result.

**Continuation:** The source-support contract, frozen 48-question synthetic instrument, implementation, all scored attempts, and remaining limitations are in [`m5_answerability_development_2026-09-23.md`](m5_answerability_development_2026-09-23.md). The work improves this limited POC path; it does not lift the participant UAT pause.

## Observed failure

In the local POC, a question using the plural, hyphenated form of a recreational activity returned `UNCERTAIN`; the same question using the singular form returned `ANSWERED` with a dated, outing-specific source. The second answer did not establish the user's general preference. The user identified this as systemic brittleness rather than a suffix-normalization request. Preserve both outcomes as known development failures; do not count either as evidence that the UI understands the question.

The relevant code explains the behavior:

- `Store.retrieve()` in `lifetime_ai/store.py` requires **every** non-stopword query term to be a literal substring of either proposition or source text. There is no morphological, paraphrase, entity, or relevance layer. A missing candidate is indistinguishable from absent knowledge.
- `CitedStateRenderer.render()` in `lifetime_ai/chat.py` labels any single matching proposition `answered`, without checking whether it supports the question at the requested scope or time. Distinct propositions among several matches are labeled a `conflict` without a contradiction check.
- Current `StateItem` carries kind, proposition, source, status, and validity dates, but not explicit subject, predicate, polarity, or contextual scope. The reviewed email import was manual and is not evidence that ordinary email claims can be extracted or reconciled automatically.

These are separate failure surfaces: candidate recall, evidence-to-question support, and synthesis across multiple claims. A pluralization patch could improve this one candidate lookup while leaving the unsupported-answer path intact.

## Engineering plan

1. **Specify the answer contract before changing retrieval.** For each question, distinguish `supported`, `unsupported`, `conflicted`, and `needs clarification`. A source about one dated outing cannot establish a timeless general preference. The answer must cite evidence for the proposition actually asserted, including its scope and date, or abstain with a useful explanation.
2. **Build a development question set across failure families, not one phrase.** Include lexical variants (plural, inflection, punctuation), paraphrases without shared keywords, contextual-versus-general questions, temporal updates/corrections, several related-but-compatible claims, genuine contradictions, irrelevant near-matches, and deleted-source checks. Use at least 48 questions across these families, with expected candidate sources, answerability, answer content, and acceptable abstentions labeled before scoring. Keep every miss and false answer. The observed query pair belongs to this development set, never to an unseen final sample.
3. **Separate retrieval from answerability.** Produce a bounded, source-linked candidate set with a high-recall lexical/symbolic path and, if justified, a local semantic path. Inspect retrieval recall independently of response quality. Then verify support, actor, scope, time, and conflict against those candidates before rendering. A model-based verifier must have explicit version, cost, latency, and failure behavior; no silent fallback to the current keyword result.
4. **Represent what the answer check needs.** Add or derive structured claim attributes only where justified by the development cases: subject/actor, relation, polarity, contextual scope, effective interval, and provenance chain. Keep the original source and later user correction distinguishable. Do not promote a broad preference from a context-specific statement.
5. **Gate the UI and then seek independent evidence.** Until the new path passes a frozen development run, label the UI as a state/citation demo and do not invite participant UAT. After engineering, have the separate agent run a newly selected, participant-approved sample that was not used for tuning. A failed independent run stays a failure; repairs require another fresh sample.

## Proposed go/no-go checks for the development run

Freeze the question set, labels, implementation version, and exact thresholds before execution. The proposed minimum is at least 95% recall of the correct source in the bounded candidate set for supported questions; zero `answered` outcomes for questions labeled unsupported because of actor, scope, time, deletion, or irrelevant near-match; 100% source-backed citations and zero deleted-source leakage; at least 90% correct supported answers; and no false `conflict` on compatible claims. Report denominators and every failure. These are development targets, not achieved results or a substitute for the independent sample.

The independent M5 protocol also needs explicit retrieval and answerability labels before it can be a UAT gate. Formal G5 remains a separate paired comparison against a competent rolling-summary/retrieval baseline, with full lifecycle cost. Do not use the quarantined G4 v21 holdout or private `.uat` diagnostics for this work.
