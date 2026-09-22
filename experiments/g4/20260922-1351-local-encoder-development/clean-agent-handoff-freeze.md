# G4 development candidate — clean-agent handoff freeze

**Frozen for handoff:** 22 September 2026. This is a development candidate,
not a G4 gate pass or authorization to open the holdout. The final evaluation
policy remains subject to the required baseline, latency, and deferred cost
work. Any change to the decision code or policy requires a new development-only
run and a new freeze before final evaluation.

The v0.2 read-only rehearsal used 1,080 development pairs and prepared 363
transitions (33.61%). All 363 matched the joint relationship/effect labels and
gold `accept` disposition in development; all-eligible relationship ECE was
0.0198. No state was committed. These are development-selected observations,
not independent holdout evidence. The full audit is
`rehearsal-development-audit.jsonl`.

## Exact candidate inputs and implementation

| File | SHA-256 |
| --- | --- |
| `evaluation/config/g4-development-rehearsal-policy.json` | `b0bfe8a64fe606916a30a8a8233e18ab97bcc324ad247213908b8fb8ebf18b95` |
| `evaluation/config/g4-evaluation-v0.1.json` | `a99d9a4b4497241dcf613b477b004507041440694485d454504e1c229e2f4a99` |
| `evaluation/config/g4-development-authorization.json` | `6d9f972a76f1b8514d265c73ac09c78d7b2d17a80cb4f832e20eef4a5aebcb52` |
| `lifetime_ai/evaluation/g4_transition.py` | `f067acac5ef80e077c99df5003727c63fe0e4439af8537e16732bedae2b9229f` |
| `scripts/score_g4_preflight_development.py` | `d6ca7d4c132a35e62c469b36c9a7c1b0ac4c64092001b0e7675ca8081fcd2d06` |
| `scripts/run_g4_transition_rehearsal_development.py` | `6bfb813d6dd2aaa5f74337b0909b27b2071491354e2e52f21eda9b9180543f6e` |
| `experiments/g4/20260922-1351-local-encoder-development/grouped-calibrated-predictions/structured_minilm_pair_logistic-out-of-fold.jsonl` | `8e8c7f08ef50c05d67f3b0ac28619c2908f9c8769262ac1435d46cb22b42e315` |
| `experiments/g4/20260922-1351-local-encoder-development/effect-development-predictions.jsonl` | `461d111e5f2de39d0ce6344c53adff8b6a67e97a374d124b3139f775f3604866` |
| `experiments/g4/20260922-1351-local-encoder-development/rehearsal-development-results.json` | `cdeffb37e1ef6a543958dcee94bac212236fe3a28ad6ebfd589404d0ef6e9686` |

Pinned sealed-v21 corpus manifest SHA-256:
`9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3`.
The manifest identifies the frozen corpus; this handoff did not open the
holdout to verify it. The preceding access incident is documented in
`holdout-access-incident.md` without raw holdout content.

## Clean-agent boundary

The receiving agent should get this frozen repository state and a minimal
prompt only. Do not transfer the prior task transcript, search output, or
holdout content. Do not inspect any holdout file until the owner explicitly
authorizes a single final evaluation. Report the procedural no-access breach
in final evidence and do not claim the corpus was literally never accessed.
The prior agent must not make further G4 policy or threshold changes after
this freeze. Baseline and latency work may proceed on development-only inputs;
if that work changes the candidate, re-freeze before any final evaluation.
