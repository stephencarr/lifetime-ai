# Lifetime AI — M5 product and UAT handoff

- Date: 23 September 2026
- Branch: `codex/g4-clean-handoff`
- Decision: Retire the diagnostic UAT spike. Resume with an M5 product slice and a measured capture preflight. G4 remains paused for review.

## What is established

- G0–G3 have recorded passes. G0–G2 establish reproducible setup, durable source-linked state, and a typed proposal/validation boundary on controlled inputs. G3 establishes the reviewed evaluation instrument and baseline contracts; it does not establish baseline performance or raw-message capture quality. See `docs/gates.md` and the accepted records under `experiments/g0/` through `experiments/g3/`.
- G4 has a development-only MiniLM candidate. Its read-only rehearsal prepared 363 of 1,080 eligible pairs, with all 363 jointly correct on that development set. There were no autonomous decisions or committed mutations. No G4 pass, real baseline/cost comparison, or final holdout evaluation is claimed. The holdout is quarantined; do not inspect or use it for M5 work.
- The core `lifetime_ai/store.py` and `lifetime_ai/pipeline.py` still provide the model-free state substrate and mutation boundary. The retired UAT app did not use that path.

## What the UAT spike taught us

The spike provided a local source importer, a review workbench, keyword retrieval with citations, and correction/deletion controls. It was a diagnostic tool with a separate SQLite store and a deterministic cue adapter. The `MiniLMAdapter` in that app fell back to the same rules even when weights were configured. It was not the G4 model or the intended chat product.

A private, read-only review of 157 active stored claims in `.uat/workspace.sqlite3` found **2 usable as stored (both synthetic), 32 requiring rework from source, and 123 to drop as active memory**. None of the 154 email-derived claims was usable as stored. The audit did not score uncaptured messages, so it is not a precision or recall estimate. Repeated failure modes were greetings and boilerplate captured as claims, wrong actor or type, quoted-thread leakage, duplicate or superseded facts, and missing time scope. The later rule changes were not validated against that batch. Do not ask a participant to reimport it as though these failures were fixed.

The spike was committed as a recoverable snapshot in `3dd6fdc` and then removed from the active tree. Its local server on port 8766 was stopped. The `.uat/` ignore rule remains; the private databases and audit were **not** committed or deleted. Do not copy their contents into public artifacts or model inputs without a scoped review. The diagnostic code can be examined from that commit if needed, but it should not be treated as a production starting point.

## Where this work belongs

The product capabilities were already planned. M1–M2 establish ingestion and transitions; the architecture calls for selective extraction and user-facing language; M5/G5 tests persistent continuity; M8/G8 is the final integrated demonstration. The gap was sequencing and an explicit UAT preflight within M5, not a missing new research gate. G4's prepared event–state relationship task does not measure whether an ordinary email should create memory in the first place. M5 implementation can proceed while G4 is paused.

## Next product slice

Build one complete local workflow through the **core** state path:

1. A participant states a preference or commitment in a familiar chat interface. The system stores the conversation as a source event and proposes a narrowly attributed, time-scoped claim or abstains.
2. A deterministic validator decides whether the proposal can change canonical state. The model or extractor has no direct write authority. Every durable claim retains its source and transition trace.
3. After a full process restart, a question retrieves current state and its evidence, and the response cites the supporting source. It reports uncertainty or conflict instead of inventing a stable preference.
4. A correction changes the current interpretation with provenance. Deleting a source or claim invalidates derived state and prevents the old claim from appearing in retrieval. If complete deletion/audit semantics are not yet implemented, the affected path remains read-only.
5. State remains independent of the response model. The interface may use a swappable local model adapter; lack of weights must be explicit and must not silently substitute demo rules for product evidence. No external data transmission or autonomous consequential action is part of this slice.

The desired product should learn from ordinary use without per-item approval. Define the promotion and correction policy before allowing unattended durable capture; the spike's batch-confirmation workflow is not that policy.

## M5 UAT preflight and formal G5

Before inviting a participant to evaluate usefulness, run the entire slice above on synthetic and participant-approved local examples. Predeclare a realistic sample that includes positive, irrelevant, third-party, quoted, conflicting, and time-changing messages. Record false captures, misses, attribution and lifecycle errors, citation correctness, deletion leakage, and repair effort. Establish an acceptable error/abstention boundary *before* looking at trial results. A failure leads to engineering work or a narrower UAT story, not silent example removal.

Passing this preflight authorizes a bounded product UAT; it is **not** a G5 pass. Formal G5 requires the paired longitudinal comparison with a competent rolling-summary-and-retrieval baseline, total lifecycle cost accounting, and the safety invariants in `docs/gates.md`. G6–G8 remain later work. No calendar date for meaningful UAT is defensible until the vertical slice runs and capture errors are measured.

## Operator notes

- Run the repository suite with `uv run --frozen pytest -q` in a provisioned environment. In an offline environment with the existing `.venv`, use `.venv/bin/python -m pytest -q` to avoid dependency fetches.
- Keep `.uat/` out of Git. Its contents are private diagnostic data, not gate evidence.
- Preserve the G4 quarantine. Do not access the v21 holdout, its labels, or holdout-derived content for product implementation or UAT.
- Three archive copies of earlier documents were present before this cleanup and remain uncommitted. The original `docs/g3_evaluation_design_proposal.md` path was restored from its byte-identical archive copy because pilot tests still require it; the other two tracked document moves were left untouched.

## Validation at handoff

- Before retirement, the focused UAT suite passed: `9 passed`.
- After retirement, the full repository suite reported `148 passed, 3 failed`; all three failures were `FileNotFoundError` for the pre-existing move of `docs/g3_evaluation_design_proposal.md` into `docs/archive/`. Restoring the required path made those exact three tests pass (`3 passed`). The full slow suite was not rerun after that mechanical restoration.
- `git diff --check` passed, active code has no references to the retired UAT modules, and nothing is listening on the retired UAT port 8766.
