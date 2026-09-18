# Lifetime AI — Roadmap v0.2

**Date:** 18 September 2026  
**Status:** Implementation started; first persistence skeleton awaiting verification  
**Execution model:** Evidence-gated milestones, not calendar weeks  
**Primary constraint:** A compelling proof of concept on retail hardware

## 1. Project thesis

Large language models are extraordinary semantic processors, but poor canonical substrates for lifetime state. Most assistants repeatedly reconstruct temporary identity, memory, goals, and relationship context from transcripts, summaries, retrieved text, and prompts.

This project tests a different arrangement:

> Build a persistent agent runtime that owns durable operational state independently of any individual LLM call, and uses language models as replaceable semantic and expressive processors.

Conversations are events within one continuing lifetime, not containers that define separate cognitive instances.

The practical objective is not to create consciousness or reproduce a biological brain. It is to reduce context burden while improving continuity, accountability, extensibility, and cost control.

## 2. Permitted claims

The proof of concept may attempt to demonstrate that:

1. Source-linked commitments, preferences, facts, and unresolved work survive process restarts.
2. Canonical state exists independently of a running LLM.
3. An LLM can be replaced without destroying operational continuity.
4. For tasks with bounded relevant dependencies, per-call context remains approximately independent of total lifetime history.
5. A small typed decision layer handles a useful fraction of routine semantic decisions cheaply while escalating ambiguity.
6. Persistent prospective state produces useful follow-up candidates without an externally authored semantic prompt.

## 3. Claims outside scope

The proof of concept will not claim to demonstrate:

- consciousness or subjective experience;
- a human-equivalent mind;
- metaphysical identity across model replacement;
- general intelligence;
- biological plausibility or parity;
- universally lossless bounded context;
- autonomous goal formation in the broad sense;
- a novel foundation-model architecture;
- that unsolicited communication alone constitutes agency;
- that structured data is inherently superior to text.

## 4. Operating constraints

| Dimension | Constraint |
|---|---|
| Primary hardware | MacBook Air with Apple M4 and 16 GB unified memory |
| Memory | 16 GB unified memory |
| Storage | 512 GB internal SSD |
| Monthly spend | Maximum CAD $100 |
| Sustainable human attention | Approximately 4 hours per week, with optional bursts |
| Initial modality | Single-user text |
| Model training | No generative-model pretraining or fine-tuning initially |
| External actions | None without explicit review |
| Initiative | Reviewable outbox only |
| Deployment | Local-first |
| Optimization priority | Insight and demonstrable behaviour |

No new hardware purchase is planned for this phase.

## 5. Architectural inversion

### Transcript-centric assistant

```text
user message
→ retrieve text
→ assemble prompt
→ LLM reconstructs temporary state
→ LLM responds
→ temporary cognition disappears
```

### Proposed persistent runtime

```text
event arrives
→ durable state identifies what may have changed
→ typed decision layer handles routine semantic routing
→ difficult semantic operations escalate to an LLM
→ proposed updates are validated
→ authoritative state changes atomically
→ response or action is rendered
```

The LLM does not own time, authoritative state, permissions, commitment lifecycle, provenance, or operational continuity.

## 6. Initial components

### 6.1 Event ledger

Records user and system events, state-change proposals, accepted and rejected transitions, actions and outcomes, model calls and costs, timestamps, and configuration versions.

The ledger is auditable rather than absolutely immutable. Deletion, redaction, expiry, derived-data invalidation, and recovery semantics must be designed explicitly.

### 6.2 Canonical operational state

The first version contains only:

- facts;
- preferences;
- commitments;
- unresolved threads;
- prospective expectations.

Each item carries a stable identifier, proposition, scope, source evidence, validity interval, status, confidence or decision strength, sensitivity, update history, contradictions, and review or expiry conditions.

Do not split this into elaborate memory subsystems until the simple model demonstrates a concrete limitation.

### 6.3 Typed semantic-reflex layer

Its narrow initial responsibilities are:

1. rank whether a new event is relevant to existing state items;
2. classify the relationship between the event and each candidate.

Allowed relationship outputs:

```text
supports
contradicts
narrows_scope
supersedes
unrelated
uncertain
```

It returns typed probabilities, can abstain, produces no prose, and cannot mutate canonical state.

### 6.4 Generative/deliberative LLM

Used selectively for ambiguous interpretation, novel reasoning, hypothesis comparison, nuanced reconstruction, structured extraction beyond the reflex layer, and user-facing language.

- **Deliberative calls** help determine meaning or whether action is warranted.
- **Expressive calls** render an already selected communicative intent.

### 6.5 Transition validator

Enforces schema validity, permissions, source attachment, temporal consistency, update authority, sensitivity propagation, atomic writes, idempotency, and reversible operations where possible.

Valid syntax is not sufficient evidence for a justified update.

### 6.6 Context compiler

Produces a bounded, task-specific projection containing stable instructions, the current operation, relevant state and evidence, counterevidence, active commitments, constraints, and the permitted output schema.

It records why each item was included and what was omitted.

### 6.7 Prospective state and outbox

Represents expected events, commitments awaiting action, unanswered questions, deadlines, expiry conditions, and possible follow-up intentions. Candidate outreach enters a reviewable outbox and is never sent automatically in this phase.

## 7. Baselines

Every thesis experiment must compare against the strongest relevant simpler system.

| Baseline | Purpose |
|---|---|
| A. Rolling summary plus retrieval | Competent conventional memory harness |
| B. Structured state plus workflow scheduler | Most threatening practical alternative to generalized persistence and initiative |
| C. General LLM for every semantic decision | Quality, latency, cost, and consistency comparison |
| D. Oracle state | Separates state-construction failures from persistence failures |

All baselines must use the same cases, output contracts, and measurement harness wherever possible.

## 8. Milestone map

Time estimates are planning aids only. A milestone is complete only when its referenced gate passes under `gates.md`.

| Milestone | Deliverable | Required gate |
|---|---|---|
| M0. Reproducible foundation | Declared environment, dependency lock, test command, clean setup | G0 |
| M1. Durable state substrate | Event ledger, canonical state, atomic transition API, replay and restart | G1 |
| M2. Typed transition pipeline | Candidate selection → relationship → proposal → validation → commit | G2 |
| M3. Evaluation corpus and baselines | Synthetic histories, gold checkpoints, common baseline interface | G3 |
| M4. Semantic reflex | Rules, embeddings/classifier, calibrated confidence, abstention | G4 |
| M5. Persistent continuity | Longitudinal comparison against summary plus retrieval | G5 |
| M6. Bounded context | Context compiler and controlled history-growth experiment | G6 |
| M7. Prospective state | Follow-up candidates, suppression rules, scheduler comparison | G7 |
| M8. Integrated POC | Restart, model swap, scale comparison, inspector, final decision | G8 |

## 9. Milestone details

### M0 — Reproducible foundation

- Python 3.12+ managed through `uv` or an equivalently reproducible tool.
- Locked runtime and development dependencies.
- One documented command runs all tests.
- A clean environment can reproduce the test result.

### M1 — Durable state substrate

- SQLite event ledger and canonical-state tables.
- Source-linked atomic transitions.
- Idempotent ingestion and transition application.
- Collision detection rather than silent reuse of identifiers.
- Replay and deterministic restart recovery.
- Readable inspection of state and provenance.

### M2 — Typed transition pipeline

Implement one complete path:

> Ingest an event, select a potentially affected state item, classify their relationship through a typed interface, propose a source-linked transition, validate it, apply it atomically, restart, and recover the same authoritative state.

The relationship may initially be supplied manually. Required scenarios are support, contradiction, scope narrowing, temporal supersession, irrelevance, and uncertainty requiring abstention.

### M3 — Evaluation corpus and baselines

- Scripted longitudinal histories containing correction, expiry, contradiction, ambiguity, deletion, and irrelevant noise.
- Gold state at selected checkpoints.
- Development and locked holdout partitions.
- Baselines A–D behind comparable interfaces.
- Cost, latency, token, and decision logging.

### M4 — Semantic-reflex experiment

Compare:

1. deterministic rules;
2. embedding retrieval;
3. a small entailment or cross-encoder model;
4. frozen embeddings plus a lightweight classifier;
5. a general-purpose LLM with structured output.

The reflex layer must return class probabilities, calibrated confidence, and an escalation decision. Thresholds are selected on development data and frozen before holdout evaluation.

### M5 — Persistent continuity

Compare application-owned canonical state with rolling summary plus retrieval across held-out lifetime histories. Measure current-state accuracy, commitment tracking, temporal scope, provenance, unauthorized updates, deletion behaviour, lifecycle cost, and model-swap continuity.

### M6 — Bounded context

Hold relevant dependency size constant while increasing unrelated lifetime history. Measure compiled prompt size, retrieval work, total lifecycle tokens, accuracy, latency, and cost.

The claim is bounded only for tasks whose relevant dependency set remains bounded.

### M7 — Prospective state and outbox

- Mature explicit commitments and expected events over simulated time.
- Choose among internal investigation, clarification, outreach, and silence.
- Suppress resolved, expired, unauthorized, and obsolete prospects.
- Compare against an ordinary workflow scheduler at a matched outbox allowance.
- Never send automatically.

### M8 — Integrated POC

The final demonstration should show:

1. creation of a preference and commitment;
2. accumulation of thousands of irrelevant events;
3. narrowing or revision of the preference;
4. preservation of original evidence and current interpretation;
5. complete process termination and recovery;
6. replacement of the LLM backend without loss of operational state;
7. suppression of an obsolete follow-up;
8. creation of a justified new outbox item;
9. inspection of every transition's evidence and decision path;
10. approximately flat per-call context when relevant dependency size is fixed.

## 10. Evaluation dimensions

### Semantic decisions

- accuracy and per-class precision/recall;
- calibration and Brier score;
- autonomous-decision coverage;
- error rate above the action threshold;
- escalation rate;
- median and tail latency;
- cost and local-compute proxy.

### Persistence

- current-state accuracy after revision;
- commitment precision and recall;
- temporal-scope and provenance errors;
- unauthorized update rate;
- duplicate-event and collision handling;
- restart, replay, deletion, and model-swap behaviour.

### Context

- lifetime event count;
- relevant dependency count;
- compiled prompt size;
- retrieval and deliberation calls;
- total lifecycle tokens;
- latency and monetary cost.

### Initiative

- usefulness at a fixed outbox allowance;
- obsolete-prospect suppression;
- handling of resolved commitments;
- correct selection of investigation, clarification, outreach, or silence;
- performance relative to the scheduler baseline.

## 11. Budget

| Category | Monthly target | Hard ceiling |
|---|---:|---:|
| Generative-model APIs | CAD $25 | CAD $50 |
| Embedding or specialist APIs | CAD $0 | CAD $10 |
| Cloud compute | CAD $0 | CAD $20 |
| Hosting | CAD $0 | CAD $10 |
| Contingency | CAD $15 | CAD $30 |
| **Total** | **CAD $40** | **CAD $100** |

All model calls must record estimated cost. Local computation is preferred when it does not consume disproportionate development time.

## 12. Initial software choices

- Python 3.12+
- `uv` for environments and dependencies
- SQLite with migrations from the beginning
- Pydantic or typed dataclasses at boundaries
- pytest for transition, replay, and recovery tests
- Sentence Transformers for local embeddings/encoders
- scikit-learn for lightweight classification and calibration
- one backend-neutral LLM adapter
- command-line inspection before any graphical interface

Avoid distributed infrastructure, hosted vector databases, autonomous external tools, agent frameworks, elaborate graphical worlds, generative-model training, and premature plugin systems.

## 13. Security and privacy boundaries

- No autonomous external messages, spending, or account creation.
- Separate assertion, inference, and operating assumption.
- Propagate sensitivity to derived state.
- Require provenance for every durable semantic update.
- Test deletion of sources and derivatives.
- Prevent persisted prompt injection from gaining authority.
- Expire inferred goals and prospects.
- Make state inspectable and correctable.
- Never optimize for engagement or relationship continuation.

## 14. Decision discipline

`gates.md` is the authoritative completion specification. Implementation output, file count, code volume, or a plausible demonstration never constitutes a pass by itself.

Thresholds may be marked provisional while designing an experiment, but they must be frozen before evaluating its holdout data. A failed gate produces one of three explicit decisions:

- **Retry:** an implementation or evidence defect can be corrected without changing the claim.
- **Revise:** retain the objective but change the component or narrow the claim.
- **Stop or simplify:** a simpler baseline captures the demonstrated value or the claim is unsupported.

## 15. Current checkpoint

As of 18 September 2026:

- A small model-free persistence skeleton has been generated.
- Python 3.13.11 and locked dependencies reproduce the test result in two clean environments.
- G0 has **passed** with evidence under `experiments/g0/`.
- G1 has **passed** with evidence under `experiments/g1/`.

The next action is M2/G2: implement the typed transition pipeline while preserving the validator as the sole mutation authority.

## 16. North star

> Create an AI assistant whose lived experience is durable, accountable, and independent of any one context window—while using the least expensive form of intelligence appropriate to each decision.
