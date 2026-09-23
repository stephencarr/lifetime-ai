# Human UAT decision handoff — 22 September 2026

**Audience:** the next engineering/product agent
**Purpose:** preserve the owner's current direction and provide a safe, concrete starting point for a small real-world UAT.

## Decision

Pause broad classifier experimentation and formal G4 model comparisons for now. Prioritize learning whether the product helps people in real workflows. Run a small, opt-in, human-supervised UAT. This is product-value evidence; it does not establish autonomous reliability or pass G4.

Build a lightweight candidate-facing interface before recruiting nontechnical UAT participants. Prefer a thin local web UI if participants are ordinary users; use a CLI only if the selected participants are comfortable with command-line tools. Keep the interface disposable and narrow. Do not build a general product shell as part of this experiment.

## Evidence and its limits

- Development comparison: structured, family-grouped MiniLM produced 588 candidate accepts among 1,080 development pairs at the frozen 0.95 probability threshold. 578/588 were correct (98.30% precision; 54.44% candidate coverage), before the transition validator. These are development results, not autonomous decisions or independent user evidence.
- Development rehearsal: a read-only funnel prepared 363/1,080 pairs (33.61%); all 363 had correct joint relationship/effect labels and gold `accept` disposition in that development set. All-eligible relationship ECE was 0.0198. This candidate was development-tuned and made no committed mutations.
- Later authorized final POC: the selected model was `structured_tfidf_logistic`, not MiniLM. At threshold 0.95 it scored 540 eligible pairs across 45 holdout families and made zero autonomous decisions. Coverage was 0%, autonomous precision was undefined, ECE was 0.256264, and Brier score was 0.373343. This does not refute MiniLM.
- The harness reports `full_g4_gate_decision: NOT_EVALUATED` because transition-validator metrics are not integrated.
- The v21 holdout had previously been traversed by a broad repository search that returned holdout content. The later authorized run also used v21. Treat v21 as spent and disclosed; do not use it for tuning or call it untouched. Any future formal final evaluation needs a clean replacement holdout and separate authorization.

The run artifacts are in `/private/tmp/lifetime-ai-g4-final-20260922-clean-4511e548/` for as long as that temporary directory is retained. The machine-readable result is `result.json`; the contemporaneous audit is `audit.md`. The run nonce was `g4-poc-20260922-tfidf-4511e548-1e3b-4d0c-88dd-c3e36256f941`.

## UAT product boundary

Use MiniLM as the leading local suggestion candidate for the first UAT. The final TF-IDF result does not change that choice. Defer a hosted API LLM until UAT or targeted development diagnostics show a specific capability gap that justifies its data-sharing, cost, latency, and calibration trade-offs.

The first UAT should test one concrete workflow, such as capturing and later retrieving source-backed project decisions, commitments, or preferences. Suggestions must show their source and let the participant accept, edit, reject, or skip them. The system must not silently change durable state, contact anyone, or take consequential actions. If there is no tested undo and audit path, keep the system read-only and have participants apply accepted changes manually in a disposable test space.

Use only participant-approved data. Make the test easy to stop and clear; explain what is stored, where it is stored, and how to delete it. Do not use participant content for model training without separate explicit consent. Exclude sensitive or consequential use cases from this first study.

## Minimal interface scope

The candidate should be able to:

1. Add or select a small, bounded set of source material for the chosen workflow.
2. Review a proposed item with the source excerpt, date/context, and a plain-language reason.
3. Accept, edit, reject, or defer it; see the resulting state before confirming.
4. Ask a small set of realistic retrieval questions and inspect the supporting sources and any uncertainty.
5. Correct or delete stored test data and leave structured feedback.

Keep evaluator labels, gold answers, holdout paths, and experiment-only metadata out of the interface and model context. Log product events needed for analysis (suggested, shown, accepted, edited, rejected, skipped, retrieved, corrected), but avoid retaining unnecessary raw content.

## What to learn

For each participant and workflow, record:

- whether a suggestion was useful, correct, and supported by its source;
- accept/edit/reject/skip rates and the reasons for edits or rejection;
- important missed items that the participant identifies;
- retrieval success, time to find the needed information, and whether provenance was clear;
- user effort, trust, willingness to continue, and cases where the tool interrupted or misled them.

Set study success criteria before the first participant. Report product usefulness separately from classifier metrics. A positive UAT supports continued product investment; it does not justify autonomous writes or a G4 pass.

## Recommended next sequence

1. Choose one target participant profile and one frequent, bounded workflow.
2. Prototype the smallest local UI (or CLI for technical participants) around the review-and-feedback loop above; use synthetic fixtures first.
3. Verify the UI never performs an unreviewed state change, leaks evaluator-only fields, or retains data after deletion.
4. Run a short opt-in UAT, review failures with participants, and summarize product outcomes and safety incidents.
5. Use those observations to choose the next engineering investment: UX/workflow changes, MiniLM improvements, transition validation, or a separately scoped API-model comparison.

Do not tune on v21 or change the frozen 0.95 policy based on its outcomes. Full G4 remains unevaluated. Autonomous behavior remains out of scope for this UAT.
