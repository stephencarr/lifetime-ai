# Lifetime AI — G4 Readiness Handoff

**Updated:** 22 September 2026
**Audience:** whoever picks up work after G3
**Gate state:** G0-G3 passed. G4 has not started. **This document's job is to get you from "G3 is done" to "G4 work can safely begin" — it is not itself a G4 authorization.**

If you haven't already, read `docs/repo_map.md` first — it tells you what's real, what's superseded, and where things live. This document assumes you've read that.

## 1. What just happened (one paragraph)

G3 (frozen evaluation corpus) passed against `evaluation/corpus/frozen-g4-v0.1-sealed-v21/`. Getting there took an unusual amount of remediation: a first "PASS" against a v16/v17 seal turned out to be built on a review that recorded zero findings but had only run structural/schema/hash validation, not genuine reading of event/gold content. A deliberate adversarial re-review found three real, corpus-wide fabricated-content defects (a mislabeled action field, a fabricated sensitivity field, and a feature tag that never had real supporting content implemented) plus a holdout-assignment algorithm that wasn't stable under content correction. All four were fixed and independently reverified. Two further rounds of PR review then found and fixed real bugs in the *evaluation tooling* itself (an oracle-baseline temporal leak in the smoke harness, and gaps in the evidence-builder's review-finding validation) — none of which touched corpus content. The corpus is now at v21; content is byte-identical to v20.

The single most important lesson from this, worth internalizing before you touch anything G4-related: **a review that reports zero findings is not the same as a review that read the content.** If you generate or modify anything that will be graded — corpus, gold labels, model outputs — insist on knowing what the reviewer actually did, not just what it concluded.

## 2. What "G4 authorization" actually means and who decides it

`evaluation/config/g4-evaluation-v0.1.json` currently has:

```json
"status": "FROZEN_AT_G3_MODEL_FREE",
"authorization": {
  "model_predictions_authorized": false,
  "threshold_tuning_authorized": false,
  "holdout_evaluation_authorized": false,
  "separate_g4_run_authorization_required": true
}
```

This is not a technical blocker — it's a policy one. Per `docs/gates.md`'s governing rule, the project advances on evidence, and G4 specifically requires a locked, untouched holdout: once a model has seen holdout data, that holdout is spent (rule in `docs/gates.md` section 1 and repeated throughout `docs/lifetime_ai_handoff.md`). The project owner (Stephen) needs to explicitly authorize a G4 run — this is a deliberate gate, not an oversight, and no amount of code readiness substitutes for that decision. **Do not flip these flags, run a model against the corpus, or generate predictions without that explicit authorization**, even if everything else described below is ready.

## 3. What is NOT yet ready, independent of authorization

Even once authorization is granted, three things need attention before a real G4 run should happen:

### 3a. The price table is empty

`evaluation/config/g4-evaluation-v0.1.json`'s `cost_and_lifecycle_accounting` key is currently an empty object — no price table has been added at all yet. Per the gate record's own recorded deviation, **no G4 cost-comparison claim can be made until a dated, real price table is frozen.** This means: pick the actual model/provider you intend to run G4 against, get its current published per-token pricing, freeze it with a date, and hash it — the same way every other piece of frozen config in this project is hash-recorded. Do this before running anything, not after, so the cost numbers you eventually report aren't retroactively justified.

### 3b. No real baseline adapters exist yet

The four "baselines" currently implemented (`lifetime_ai/evaluation/contracts.py`: `MockRollingSummaryBaseline`, `MockSchedulerBaseline`, `MockGeneralLLMBaseline`, `MockOracleBaseline`) are **contract-only fixtures** — they prove the four systems can consume the same projections and emit the same response shape. They are not real baselines and have never produced a meaningful result. `docs/lifetime_ai_handoff.md` section 13 describes what a *real* strong baseline needs to look like (hybrid lexical/vector/symbol retrieval, source filters, recency weighting, citations, conflict reporting, fixed context budget, same source corpus/downstream model/query set/tool budget as the proposed architecture). Building these is G4/G5 work in its own right — don't assume they exist because the mocks pass their contract tests.

### 3c. The G4 decision rule is frozen but never exercised end-to-end

The provisional thresholds in `docs/gates.md`'s G4 section (95% precision, 30% autonomous coverage, ≥100 autonomous holdout decisions, ECE ≤0.10, etc.) and the matching policy in `evaluation/config/g4-evaluation-v0.1.json` (Wilson-interval precision rule, calibration procedure, severity zero-tolerance rules) have been frozen and reviewed, but **no code has ever computed them against real predictions**, because no predictions have ever been generated. Before a real holdout run, build and dry-run the scoring/decision code against a synthetic or mock prediction set (not the real holdout) to make sure it actually produces the right pass/fail verdict shape. Finding a scoring bug *after* the real holdout run is exactly the "holdout is spent" failure mode this project is designed to avoid.

## 4. Concrete next steps, in order

1. **Get explicit G4 run authorization from the project owner.** Don't proceed past this without it, however ready the rest looks.
2. **Freeze a real, dated price table** for whatever model/provider G4 will actually use. Hash it into the config the same way every other frozen artifact in this project is hashed.
3. **Build at least one real, non-mock baseline** — Baseline A (rolling summary + retrieval) is the cheapest one to stand up for real and is explicitly required before any G5 comparison, so building it now is not wasted work even if G4 itself only needs the semantic-reflex model and Baseline C (general LLM).
4. **Dry-run the G4 scoring/decision logic** against synthetic predictions (never the real holdout) to catch scoring bugs before they'd cost you a holdout.
5. **Only then**, with authorization, price table, at least one real baseline, and a proven scoring path: implement the semantic-reflex model itself, run it against the development partition first (development, not holdout, is fine to iterate against), and only run the true holdout once, per the frozen procedure.
6. **Follow the same evidence discipline that got G3 here**: independent adversarial review of anything a model or generator produces — not just schema/structural validation — before calling any of this done. If you dispatch review agents, tell them explicitly what defect classes to hunt for; a review with no scope tends to report "no findings" whether or not that's true.

## 5. One structural cleanup worth doing before G4 work starts (optional but recommended)

`scripts/build_g3_frozen_evidence.py` took three review rounds to get right because its two entry points (`build_review_artifacts`, `build_evidence`) don't share one validation path. If you're going to build a G4 evidence-generation script, don't repeat that shape — one validation function, called from every path that touches a review record or prediction set, not duplicated per entry point.

## 6. Where to look when you get here

- `docs/gates.md` — the actual G4 rulebook: thresholds, required evidence, automatic failure conditions, failure response (revise vs. simplify).
- `evaluation/config/g4-evaluation-v0.1.json` — the frozen policy config.
- `docs/lifetime_ai_handoff.md` sections 4 and 13 — the four independent gold axes and what a strong baseline actually needs.
- `docs/g3_evaluation_design_proposal.md` — corpus design rationale, if you need to understand why a particular gold label or projection field exists the way it does.
