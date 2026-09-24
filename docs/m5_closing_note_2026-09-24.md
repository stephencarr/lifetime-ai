# M5 closing note — 24 September 2026

Work on this branch has stopped. This note records what was attempted, what was
measured, why it stopped, and what a future attempt would need. It supersedes the
forward-looking sections of
[the mid-flight handoff](m5_midflight_handoff_2026-09-23.md); that document's
description of branch state and retained evidence remains accurate.

Nothing here is a passed gate. The branch is not a working POC, and no part of it
authorises participant UAT.

## What was attempted

A source-grounded durable memory system: construct structured claims from ordinary
conversation, verify each against its cited source span, reconcile against existing
state, and answer questions only where current source evidence supports the requested
actor, polarity, scope, and time — abstaining otherwise. The intended deployment target
was local inference on an Apple M4 MacBook Air with 16 GB RAM.

## What was measured

All figures below come from checked-in synthetic development instruments, scored with
frozen hashes and retained per-item records. No independent sample was ever selected or
scored.

- **Unattended durable capture is unreliable with 8B-class local models at this
  bar.** Four scored attempts against the frozen 18-scenario instrument
  (`evaluation/m5_model_poc/v0.1`) went 13/14 → 0/14 → 13/14 → 6/14 clear captures.
  Attempt 02 failed closed on a schema mismatch; attempt 04 regressed after a
  principled typed-field revision. Records: `experiments/m5_model_poc/attempt-0{1..4}.json`.
- **Using one model as both proposer and verifier produces correlated errors.** In
  attempt 04 the same model's source-support check rejected a direct `I prefer tea`
  preference while promoting `Thanks, that helps` as an ongoing fact that the user is
  grateful. A separate synthetic probe reproduced both.
- **The independent entailment candidate did not clear its own gate.** The local
  ModernBERT NLI diagnostic (`evaluation/m5_nli_preflight/v0.1`) accepted 21/24
  positives but falsely supported 1/24 negatives, including an injected storage
  instruction. It was never integrated as a truth authority.
- **Single-index ANN failed a planted-vector recall gate.** At one million 384-dim
  vectors, two frozen configurations recovered 12/32 (p95 2.15 ms) and 31/32
  (p95 17.18 ms) planted queries against a 32/32 gate. Query latency was never the
  problem; startup remains an O(N) index rebuild.
- **Retrieval was not the bottleneck.** Candidate recall was 10/10 on supported
  questions in the best attempts. The failures were semantic, at construction and
  verification.

Verification boundary at stop: the selected M5 test set passes (**32 passed**),
`uv lock --check` passes, `git diff --cached --check` passes. A broad test invocation
during development inadvertently entered legacy G4 tests referencing the quarantined
v21 corpus and was interrupted; no G4 output or holdout content was used to develop or
tune M5. Do not run the broad suite while it can reach that corpus.

## Comparison against shipped systems

Checked against primary vendor documentation on 24 September 2026:

- **Anthropic memory tool** (`memory_20250818`): a client-executed file API
  (`view`/`create`/`str_replace`/`insert`/`delete`/`rename`) over a `/memories`
  directory. No embeddings, no entailment check, no reconciliation engine. Truth
  maintenance is delegated entirely to the model's in-context judgment.
- **Claude Code CLAUDE.md + auto memory**: human-written rules plus model-written notes
  in four fixed categories. Index loaded each session up to a size cap, topic files read
  on demand. No ranking, no typed schema, no conflict detection. Documented explicitly
  as context, "not enforced configuration".
- **OpenAI vector stores / file search**: automatic chunk → embed → index with scored
  results and file-level citations. A generic retriever; no claim extraction, no
  source-to-claim entailment, no supersession or deletion-consistency semantics.

None of the three attempts verified, source-grounded, contradiction-aware durable
memory. The likeliest explanation is not difficulty alone: for a vendor, non-portable
memory is a switching cost, so the incumbents best placed to build a portable verified
memory layer are the ones least incentivised to.

## Two design directions identified but not built

Recorded because they route around the measured failures and would be the starting point
for any future attempt.

1. **Confidence that accrues instead of capture-time correctness.** Every observation
   enters tentative and solidifies only across independent occasions, volunteered rather
   than elicited statements, and beliefs that survived being surfaced without
   correction. Under this design the measured failures become benign: a wrongly promoted
   one-off never recurs and decays, and a missed preference is recoverable when it comes
   up again. This trades a measurable-but-wrong metric (per-message capture precision)
   for a correct-but-harder one (does the knowledge base converge over many sessions),
   which would need a synthetic longitudinal harness to keep honest.
2. **A pluggable, model-agnostic memory layer.** If the knowledge base is portable, any
   model becomes immediately familiar with the user, and memory stops being a vendor
   lock-in. This also dissolves the 16 GB constraint — local inference becomes a privacy
   option rather than the only path. The unresolved risks here are not technical:
   distribution (the layer must be always-on to matter), dependence on a protocol the
   incumbents control, and whether users feel the lock-in strongly enough to adopt
   infrastructure over it.

## Why it stopped

The remaining work is a long tail of tweaking and refinement with no clear finish line,
and the parts that would make it matter are distribution problems rather than
engineering ones. A memory layer is only useful if it is always present, which requires a
client people use or a protocol dependency on the vendors whose lock-in it removes.
Neither is in scope for a solo side project, and without them the likely outcome is an
indefinite proof of concept tied to one laptop with no sticky usage.

Stopping is a decision from measured evidence, not an abandonment mid-iteration.

## State of the branch

`codex/m5-semantic-wip` diverged from `main` before the three G3 v21 commits
(`7fa509f`, `9eb7cce`, `ccfa89f`) and is deliberately left unmerged: merging would touch
sealed corpus artifacts for no benefit now that work has stopped. Every failed attempt,
frozen instrument, and per-item record is retained. Preserve the sealed manifest and
historical artifacts unchanged.

If this is ever picked up again, start from the two design directions above rather than
from a fifth prompt revision against the 18-scenario instrument — that set is
development-contaminated and cannot establish generalisation.
