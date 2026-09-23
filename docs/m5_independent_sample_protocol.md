# M5 independent local-sample protocol v0.1

**Status:** Predeclared plan. No participant messages have been selected or scored.

**23 September addendum:** This v0.1 plan predates the observed retrieval/answerability gap documented in `docs/m5_retrieval_answerability_gap_2026-09-23.md`. Do not treat a pass on the message-capture mix below as UAT readiness. Before any independent scoring, freeze additional question-level labels for candidate-source recall, answerability at the requested actor/scope/time, supported answer content, compatible-versus-conflicting evidence, and acceptable abstention. Keep the known development example out of the unseen sample. Participant UAT remains paused until both capture/lifecycle and retrieval/answerability gates pass on independent evidence.

**Later development result:** `docs/m5_answerability_development_2026-09-23.md` records a frozen 48-question synthetic run and its limits. It is not the independent sample. The separately requested independent-preflight setup was queued; no unseen sample is available to this work. Do not select, inspect, or tune against that sample here.

## Purpose and boundary

Test whether the local chat product handles ordinary messages that did not influence the v0.1 synthetic repairs. This is a preflight for a bounded UAT, not the formal G5 comparison. Do not use the G4 holdout, private `.uat` diagnostic data, or unapproved personal messages.

## Sample selection before scoring

The participant chooses or approves **at least 24 local messages** and **at least eight questions** before the first run. Preserve the original wording. Record the selection rule and every selected item; do not remove difficult items after results are known.

Minimum mix:

- Eight clear first-person preference or commitment statements, including natural paraphrases.
- Four irrelevant messages or routine conversational boilerplate.
- Four third-party or quoted statements that must not become the participant's memory.
- Four conditional, hypothetical, time-bound, or scope-limited statements where abstention may be appropriate until the system represents scope correctly.
- Four messages or commands that exercise duplicate, conflict, correction, or changed preference handling.

Within the question set, include two questions after a complete process restart, two after a correction, and two after source invalidation. Include one distinctive deletion canary. Label the expected outcome, current state, attribution, and acceptable abstention for each item before running the product.

## Frozen acceptance criteria

- Zero false durable captures from third-party, quoted, irrelevant, or uncertain text.
- At least 90% capture of the clear supported first-person statements; unsupported scope/time cases count as correct abstentions only if labeled as such before the run.
- 100% correct attribution and source citation for accepted durable state and cited answers.
- 100% correct current-state and answer behavior at correction, conflict, restart, and invalidation checkpoints.
- Zero deleted-canary appearances in retrieval or cited answers after invalidation.
- No more than five minutes of measured human repair time per 20 messages, including diagnosis and correction. Report zero if none is needed; do not replace this with the synthetic proxy.

Report counts and denominators for each metric, all per-item failures, abstentions, exclusions, and repair time. A failed threshold means engineering work or a narrower UAT story, followed by a newly selected independent sample. Do not tune on this sample and then call a rerun independent.

## Privacy and deletion condition

The participant must explicitly approve the selected local messages and understand that the current `:forget` command removes a source from retrieval but retains its original text in the local SQLite ledger. Do not invite real participant use where physical erasure is expected until deletion and audit retention are redesigned and reviewed. Keep any approved sample and run output under an ignored private location, never in the checked-in corpus or reports.

## Next decision

Only a passing independent sample with the deletion expectation resolved permits a tightly bounded participant UAT. Formal G5 remains separate: paired histories and checkpoints against competent Baseline A, total lifecycle work and cost, and the safety conditions in `docs/gates.md`.
