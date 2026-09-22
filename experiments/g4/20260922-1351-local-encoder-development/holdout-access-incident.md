# G4 holdout-access incident — 22 September 2026

During development follow-up, a broad text search (`rg -n` over `docs evaluation scripts`)
was run to locate Baseline C references. Because `evaluation/` included corpus
directories, the search traversed holdout files and returned holdout content.
The output was truncated, so the exact set of matching holdout records exposed
cannot be established from that output. This breached the owner's no-access
instruction, but no holdout results were produced or inspected.

No model predictions, scoring, threshold tuning, or state transitions were run
on holdout data. The development rehearsal artifacts were produced before the
incident from `development.jsonl` only. The incident does not turn those
development measurements into holdout evidence and does not authorize any
further holdout access.

Owner disposition: keep the existing v21 holdout quarantined for a separate,
clean evaluation agent rather than automatically regenerating it. This agent
must not tune or revise G4 policy after the incident. Freeze and hash the
development-only candidate before handoff. The new agent must receive only the
frozen repository state and minimal evaluation instructions, not this task's
transcript, search output, or holdout content. It must not open the holdout
until the owner separately authorizes a single final evaluation run. Report
the procedural breach in any eventual G4 evidence; do not describe the data
as literally never accessed. If holdout content or outcomes are passed into
development or the clean agent's pre-evaluation context, replace the holdout.
Future repository searches must explicitly exclude corpus holdout paths.
