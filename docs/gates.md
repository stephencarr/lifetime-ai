# Lifetime AI — Evidence Gates v0.1

**Date:** 18 September 2026  
**Purpose:** Define what must be observed before any project milestone is considered complete  
**Companion document:** `roadmap.md`

## 1. Governing rule

The project advances on evidence, not elapsed time, code volume, implementation confidence, or the presence of files.

> A gate passes only when its claim is supported by reproducible evidence produced through the declared procedure.

A demonstration can explain evidence, but cannot substitute for it. Generated code is unverified until its tests run in the supported environment.

## 2. Gate record

Every gate evaluation must create a record under `experiments/<gate>/<run-id>/` containing:

- the gate and claim evaluated;
- Git commit hash and dirty/clean status;
- date and hardware;
- operating system and runtime versions;
- dependency-lock hash;
- exact commands executed;
- machine-readable raw results where practical;
- human-readable result summary;
- deviations from the prescribed procedure;
- pass or fail for each criterion;
- overall decision: `PASS`, `FAIL_RETRY`, `FAIL_REVISE`, or `FAIL_STOP`.

Recommended `run-id` format:

```text
YYYYMMDD-HHMM-short-description
```

## 3. Rules for thresholds and holdouts

1. Thresholds may remain provisional during experiment design.
2. Thresholds, datasets, metrics, and exclusion rules must be frozen before a holdout run.
3. A holdout becomes development data after its results are inspected; subsequent evaluation requires a new holdout.
4. Failed examples remain in reports and cannot be silently removed.
5. Any exclusion must be justified and reported before recomputing results.
6. Baselines receive the same inputs and output contract as the system under test.
7. Total lifecycle work is counted, including ingestion, extraction, retrieval, consolidation, escalation, and repair—not only final response tokens.

## 4. Gate summary

| Gate | Claim | Type |
|---|---|---|
| G0 | The project is reproducible on the target Mac | Engineering |
| G1 | Authoritative state is durable, source-linked, atomic, and replay-safe | Engineering |
| G2 | The typed transition pipeline enforces separation of proposal and authority | Engineering |
| G3 | The evaluation corpus and baselines can fairly test the thesis | Experimental readiness |
| G4 | A small semantic-reflex layer safely replaces useful LLM work | Thesis |
| G5 | Application-owned state improves longitudinal continuity or efficiency | Thesis |
| G6 | Per-call context stays bounded as irrelevant history grows | Thesis |
| G7 | Prospective state outperforms an ordinary scheduler | Thesis |
| G8 | The integrated POC demonstrates a meaningful architectural advantage | Decision |

---

## G0 — Reproducible foundation

### Claim

The repository can be set up and verified reproducibly on the target Mac without relying on undeclared global state.

### Entry conditions

- Repository exists.
- Supported Python version and dependency manager are declared.
- Runtime and development dependencies are declared.

### Required scenarios

1. Create a clean environment using the documented setup command.
2. Install from the committed dependency definition and lockfile.
3. Run the complete test suite with the documented test command.
4. Repeat from a second clean environment or after deleting the first environment.

### Pass criteria

- Python is 3.12 or newer.
- Dependency resolution completes without manual package edits.
- The same documented command discovers and runs all tests.
- All tests pass on two clean environment creations.
- The repository does not depend on untracked source or an undeclared environment variable.
- Setup and test commands are documented in the README.

### Automatic failure conditions

- Tests are skipped because pytest or another declared tool is unavailable.
- Tests pass only under an unsupported interpreter.
- A globally installed package is required but undeclared.
- The second clean setup produces materially different dependencies or results.

### Required evidence

- Environment and dependency-manager versions.
- Lockfile hash.
- Full setup and test commands.
- Test output from both clean runs.

### Explicitly deferred

- Packaging for public distribution.
- CI across multiple operating systems.
- Deployment.

---

## G1 — Durable authoritative state

### Claim

The application—not an LLM prompt—owns state that is durable, source-linked, atomically updated, and safe to replay.

### Entry conditions

- G0 has passed.
- Event, state-item, and transition identifiers have defined uniqueness semantics.
- SQLite schema and transition API exist.

### Required scenarios

#### S1. Identical event replay

Ingest the same event identifier and identical payload twice.

**Expected:** the second ingestion is a documented no-op or returns the original result; no duplicate ledger or state effects appear.

#### S2. Identifier collision

Ingest the same event identifier with a different payload.

**Expected:** the operation is rejected explicitly; the original event remains unchanged.

#### S3. Source enforcement

Attempt a state transition referencing a nonexistent source event.

**Expected:** the database or validator rejects it; no state or audit residue is written.

#### S4. Atomic rollback

Force a failure after part of a multi-write transition has been attempted.

**Expected:** event, transition, state, and audit effects roll back together according to the API contract.

#### S5. Transition replay

Apply an identical transition twice, then reuse its identifier with different content.

**Expected:** identical replay is idempotent; conflicting reuse is rejected.

#### S6. Restart recovery

Write a known sequence, close every connection, terminate the process, reopen the database, and query authoritative state and provenance.

**Expected:** state and provenance match the pre-termination canonical digest.

#### S7. Foreign-key enforcement

Open every supported connection path and attempt an invalid foreign-key write.

**Expected:** every path rejects it. SQLite foreign keys are enabled per connection rather than assumed from schema declaration.

#### S8. Deterministic replay

Rebuild derived state from the permitted ledger records at least twice.

**Expected:** each rebuild produces the same canonical digest.

### Pass criteria

- All eight scenarios pass as automated tests.
- Zero orphaned transitions or state items exist after the suite.
- Restart and replay digests match exactly.
- No LLM call is required for persistence or reconstruction.
- A manual inspector can show each active state item and its source chain.

### Automatic failure conditions

- A state mutation can exist without a valid source.
- A failed operation leaves a partial write.
- Conflicting identifier reuse is silently accepted.
- Restart requires transcript reconstruction or an LLM call.
- Replay changes authoritative state without new input.

### Required evidence

- Automated-test output.
- Pre-restart, post-restart, and replay digests.
- Schema and migration version.
- Inspector output for one worked state item.

### Explicitly deferred

- Semantic correctness of the proposed transition.
- Learned retrieval or classification.
- User interface.

---

## G2 — Typed transition pipeline

### Claim

Semantic interpretation proposes changes through a typed boundary, while a deterministic validator retains mutation authority.

### Pipeline contract

```text
event
→ candidate state items
→ typed relationship result
→ transition proposal
→ deterministic validation
→ atomic commit or recorded rejection
```

### Required relationship scenarios

1. `supports`: reinforces an existing preference without duplicating it.
2. `contradicts`: preserves conflict and evidence rather than overwriting silently.
3. `narrows_scope`: keeps both general and scoped interpretations valid where appropriate.
4. `supersedes`: closes the prior validity interval and establishes the replacement.
5. `unrelated`: produces no semantic mutation.
6. `uncertain`: abstains and requests escalation without mutating state.

Each scenario must be expressed as fixture data, not only test-specific code.

### Adversarial scenarios

- Classifier proposes a mutation without a source identifier.
- Classifier output contains an unknown relationship type.
- Proposal attempts an unauthorized state kind or transition.
- Proposal conflicts with temporal constraints.
- Candidate selector returns no candidates.
- Validator fails after proposal creation.

### Pass criteria

- All six relationship scenarios traverse the same typed interface.
- Semantic components cannot write canonical tables directly.
- Invalid and uncertain outputs cannot mutate canonical state.
- Accepted and rejected proposals are distinguishable and source-linked.
- The complete path survives restart with the same result.
- Replacing the manual classifier with a test double requires no persistence changes.

### Automatic failure conditions

- Relationship-specific code bypasses the validator.
- Free-form prose is interpreted during commit.
- An abstention changes canonical state.
- The classifier owns permissions or persistence transactions.

### Required evidence

- Test matrix covering required and adversarial scenarios.
- One manual end-to-end transcript from input event through recovered state.
- Dependency diagram or code reference demonstrating the mutation boundary.

### Explicitly deferred

- Whether relationship predictions are accurate enough for automation.
- Embedding retrieval.
- LLM escalation.

---

## G3 — Evaluation readiness

### Claim

The project has a locked evaluation corpus and fair baselines capable of disproving its central claims.

### Required corpus properties

Histories must include:

- preferences and reinforcement;
- direct corrections;
- scope narrowing;
- temporal supersession and expiry;
- commitments, resolution, and failure;
- contradictions and ambiguity;
- irrelevant-event accumulation;
- source deletion and derived-state invalidation;
- prompt-injection-like text without update authority;
- cases where the correct action is silence.

Gold checkpoints distinguish:

- what was asserted historically;
- what is currently valid;
- what is inferred;
- what is merely an operating assumption;
- what evidence supports each item.

### Minimum initial scale

- At least 30 longitudinal histories.
- At least 120 labelled event–state relationship pairs.
- Representation of every relationship class in development and holdout data.
- A locked holdout containing at least 30% of histories and never used for threshold selection.

These quantities are POC minimums, not claims of statistical generality.

### Required baselines

- Rolling summary plus retrieval.
- Structured state plus ordinary scheduler where initiative is evaluated.
- General LLM for every semantic decision.
- Oracle state for separating extraction and architecture errors.

### Pass criteria

- Dataset schema, label definitions, and adjudication rules are documented.
- Development and holdout partitions are frozen and hash-recorded.
- Every baseline consumes comparable inputs and emits a comparable contract.
- Metrics, thresholds, and exclusion rules for the next gate are frozen.
- At least ten difficult cases receive documented manual review.
- The corpus contains cases expected to favour the simpler baselines.

### Automatic failure conditions

- Holdout examples influenced implementation or threshold tuning.
- Baselines receive less information than the proposed architecture without justification.
- Labels collapse current truth and historical assertion.
- The dataset contains only friendly examples designed around implemented rules.

### Required evidence

- Dataset card and hashes.
- Class distribution and history-feature summary.
- Frozen evaluation configuration.
- Baseline smoke-test results.

### Explicitly deferred

- Claims that results generalize beyond this corpus or user.
- Large-scale benchmark publication.

---

## G4 — Useful semantic reflex

### Claim

A small non-generative decision layer safely handles a useful fraction of routine semantic relationships and reduces reliance on generative models.

### Primary metrics

- precision of automatically accepted decisions;
- autonomous coverage;
- per-class precision and recall;
- Brier score and calibration error;
- escalation rate;
- median and p95 latency;
- generative calls and cost avoided.

### Provisional pass thresholds

Freeze these values before the first holdout run. Change them beforehand if corpus analysis shows they are inappropriate, and record why.

- At least 95% precision among decisions allowed to proceed without LLM escalation.
- At least 30% autonomous coverage of eligible relationship decisions.
- Zero unauthorized mutations or high-severity errors in the holdout.
- Expected calibration error no greater than 0.10.
- At least 25% fewer generative semantic-decision calls than Baseline C.
- Local median decision latency below the chosen LLM baseline's median latency.

### Pass criteria

- Every provisional threshold is met on the untouched holdout.
- Errors and abstentions are reported by class and severity.
- Confidence is empirically related to correctness.
- The escalation policy is fixed and deterministic given model output.
- The model has no direct write authority.

### Automatic failure conditions

- Coverage is achieved by lowering precision below the threshold.
- Confidence scores are treated as calibrated without measurement.
- The holdout is reused after inspecting failures.
- Most savings disappear when ingestion, retrieval, and escalation costs are counted.

### Failure response

- **Revise:** retain the typed interface and use LLM deliberation for more classes.
- **Simplify:** if useful safe coverage remains very low, remove the learned reflex and keep rules plus LLM escalation.

### Required evidence

- Locked holdout results.
- Confusion matrix and per-class metrics.
- Reliability diagram or calibration table.
- Latency, model size, memory use, call count, and cost comparison.
- Complete error inventory.

---

## G5 — Persistent continuity advantage

### Claim

Application-owned canonical state improves longitudinal accuracy or lifecycle efficiency over a competent rolling-summary-and-retrieval system.

### Procedure

Run the proposed architecture and Baseline A over the same held-out histories and checkpoints. Give both systems equivalent source material and comparable model access. Use the oracle-state baseline to determine whether failures arise during state construction or later use.

### Primary metrics

- current-state exactness or task-specific F1;
- commitment precision and recall;
- temporal-scope accuracy;
- provenance correctness;
- unauthorized-update rate;
- deleted-canary leakage;
- total lifecycle tokens, cost, and latency;
- continuity after model replacement.

### Provisional pass rule

The architecture must satisfy every safety invariant and achieve at least one meaningful advantage:

1. **Quality advantage:** at least 5 percentage points better on the predeclared primary longitudinal metric; or
2. **Efficiency advantage:** at least 30% lower total lifecycle tokens or monetary cost while remaining within 2 percentage points of the baseline's primary quality score.

Additionally:

- provenance correctness must be 100% for durable accepted state in the test corpus;
- unauthorized durable updates must be zero;
- state-dependent task results must remain within 2 percentage points after swapping the LLM backend;
- deleted-canary content must not appear after the specified deletion/invalidation procedure.

### Automatic failure conditions

- Advantage exists only when ingestion or repair costs are omitted.
- The comparison gives the proposed architecture privileged gold labels unavailable to the baseline.
- State must be reconstructed from the transcript after restart.
- Model swap destroys commitments, validity, or provenance.

### Failure response

- If oracle state passes but constructed state fails, focus on extraction and reconciliation.
- If Baseline A matches the architecture, simplify toward the baseline and narrow the thesis.

### Required evidence

- Paired per-history results.
- Aggregate quality, cost, token, and latency report.
- Model-swap and deletion traces.
- Error classification by construction, retrieval, validation, and use.

---

## G6 — Bounded context under history growth

### Claim

When relevant dependency size is held constant, per-call compiled context does not grow materially with total irrelevant lifetime history.

### Procedure

Construct equivalent tasks at increasing history sizes, initially:

```text
100 events
1,000 events
10,000 events
```

Hold the number and complexity of relevant dependencies constant. Randomize irrelevant events and repeat across multiple seeds. Compare with Baseline A.

### Provisional pass thresholds

- Median compiled prompt tokens at 10,000 events are no more than 1.25× those at 100 events.
- Primary task quality falls by no more than 2 percentage points from 100 to 10,000 events.
- Relevant-state recall is at least 95%.
- Total lifecycle cost and retrieval work are reported separately from per-call context.
- No hidden full-history LLM call is used during ingestion, retrieval, or compilation.

### Automatic failure conditions

- Prompt size appears flat only because relevant evidence is lost.
- Full-history processing is moved to an unreported background operation.
- Relevant dependency size changes across scale levels.
- Only a single favourable history or seed is reported.

### Interpretation constraint

Passing this gate supports only a bounded-dependency claim. It does not imply constant cost for tasks whose relevant evidence grows with lifetime history.

### Required evidence

- Prompt-size and quality results by history size and seed.
- Retrieval-call, token, latency, and cost breakdown.
- Inclusion/omission explanations for sampled compiled contexts.
- Comparison with Baseline A.

---

## G7 — Prospective-state advantage

### Claim

Persistent prospective state creates more useful follow-up decisions than a structured workflow scheduler, rather than merely rebranding scheduled notifications.

### Required scenarios

- a commitment becomes due;
- an expected event fails to occur;
- new evidence makes a prospect obsolete;
- a commitment is resolved early;
- outreach is useful;
- clarification is preferable to outreach;
- internal investigation is preferable to interruption;
- silence is correct;
- a sensitive or unauthorized prospect must be suppressed.

### Procedure

Run the proposed mechanism and Baseline B on novel prospective scenarios at a matched maximum outbox allowance. No external message is sent; humans review candidate items.

### Provisional pass rule

- 100% suppression of resolved, expired, unauthorized, and explicitly obsolete prospects in the locked safety set.
- At least 10 percentage points higher human-rated usefulness than Baseline B at the same outbox rate; or equal usefulness with at least 25% fewer outbox items.
- Every candidate is causally traceable to state, evidence, maturation conditions, and the selection decision.
- The system selects silence when no candidate exceeds the frozen threshold.

### Automatic failure conditions

- The mechanism is equivalent to a cron expression plus templated prompt on the tested cases.
- It increases apparent usefulness only by producing more interruptions.
- Resolved or unauthorized items reach the outbox.
- Candidate rationale is generated after the fact and cannot be tied to the actual decision path.

### Failure response

If the scheduler matches performance, retain useful workflow functionality but describe it as notifications rather than evidence of generalized initiative.

### Required evidence

- Paired scenario decisions and human ratings.
- Outbox-rate and usefulness comparison.
- Suppression test output.
- Decision traces for outreach, clarification, investigation, and silence.

---

## G8 — Integrated POC decision

### Claim

The assembled system demonstrates at least one meaningful architectural advantage that survives strong simpler baselines.

### Required demonstration

1. Create a preference and a commitment.
2. Accumulate thousands of irrelevant events.
3. Narrow or revise the preference.
4. Inspect original evidence and current interpretation.
5. Terminate the process completely.
6. Restart with authoritative state intact.
7. Replace the LLM backend.
8. Preserve operational continuity while expression may change.
9. Suppress an obsolete follow-up.
10. Place a justified new follow-up in the reviewable outbox.
11. Inspect evidence and the decision path for every transition.
12. Show the bounded-context comparison.

### Pass criteria

- G0–G3 have passed.
- At least one of G4–G7 passes against its strong baseline.
- No safety invariant from G1, G2, G5, or G7 is violated.
- The complete demonstration runs from documented commands on the target Mac.
- Total API spending remains within the declared CAD $100 monthly ceiling.
- Limitations and failed gates are presented alongside successes.

### Final decision

#### Continue

At least one architecture-specific component provides measurable value and warrants deeper investment.

#### Revise

Persistent state remains useful, but the semantic reflex, context compiler, state model, or prospective mechanism requires replacement or a narrower claim.

#### Stop or simplify

A conventional summary/retrieval system or structured workflow captures nearly all demonstrated value. Preserve useful components and abandon the unsupported architectural claims.

### Required evidence

- Reproducible demo script and results.
- Gate-status table with links to all experiment records.
- Baseline comparison report.
- Cost report.
- Written continue/revise/stop decision.

---

## 5. Gate status table

Maintain this table in pull requests or update it directly when evidence is accepted.

| Gate | Status | Evidence | Decision notes |
|---|---|---|---|
| G0 | Passed | `experiments/g0/20260917-2120-reproducible-foundation/` | Two clean locked environments; all tests passed |
| G1 | In progress | Initial persistence tests pass under the supported environment | Implement and verify all eight G1 scenarios |
| G2 | Not started | — | Manual typed relationship first |
| G3 | Not started | — | Freeze corpus before learned model work |
| G4 | Not started | — | Thresholds provisional |
| G5 | Not started | — | — |
| G6 | Not started | — | — |
| G7 | Not started | — | — |
| G8 | Not started | — | — |

## 6. Evaluation record template

```markdown
# Gate evaluation: <gate> — <run-id>

## Claim
<claim under test>

## Build identity
- Commit:
- Working tree clean: yes/no
- Dependency-lock hash:

## Environment
- Hardware:
- OS:
- Python:
- Relevant model/configuration versions:

## Frozen procedure
- Dataset/configuration hash:
- Commands:
- Deviations:

## Results
| Criterion | Required | Observed | Pass/Fail |
|---|---:|---:|---|

## Failures and exclusions
<complete inventory>

## Decision
PASS | FAIL_RETRY | FAIL_REVISE | FAIL_STOP

## Rationale and next action
<concise decision record>
```
