# Lifetime AI — Official Roadmap v0.1

**Date:** 17 September 2026  
**Status:** Approved direction; implementation not yet started  
**Planning horizon:** 8 weeks / approximately 32 focused hours  
**Primary constraint:** compelling proof of concept on retail hardware

## 1. Project thesis

Large language models are extraordinary semantic processors, but poor canonical substrates for lifetime state. Most assistants repeatedly reconstruct temporary identity, memory, goals, and relationship context from transcripts, summaries, retrieved text, and prompts.

This project will test a different arrangement:

> Build a persistent agent runtime that owns durable operational state independently of any individual LLM call, and uses language models as replaceable semantic and expressive processors.

Conversations are events within one continuing lifetime, not containers that define separate cognitive instances.

The practical objective is not to create consciousness or reproduce a biological brain. It is to reduce context burden while improving continuity, accountability, extensibility, and cost control.

## 2. Permitted claims

The POC may attempt to demonstrate that:

1. Source-linked commitments, preferences, facts, and unresolved work can survive process restarts.
2. Canonical state can exist independently of a currently running LLM.
3. An LLM can be replaced without destroying operational continuity.
4. For tasks with bounded relevant dependencies, per-call context can remain approximately independent of total lifetime history.
5. A small typed decision layer can handle routine semantic decisions cheaply, escalating ambiguity to an LLM.
6. Persistent prospective state can generate useful follow-up candidates without an externally authored semantic prompt.

## 3. Claims explicitly outside scope

The POC will not claim to demonstrate:

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

The project may discover useful ideas adjacent to these topics, but they will not be used as success criteria.

## 4. Operating constraints

| Dimension | Constraint |
|---|---|
| Primary hardware | Base 2026 M5 MacBook Air |
| Memory | 16 GB unified memory |
| Storage | 512 GB internal SSD |
| Monthly spend | Maximum CAD $100 |
| Sustainable human time | Approximately 4 hours per week |
| Initial duration | 8 weeks |
| Initial modality | Single-user text |
| Model training | No language-model pretraining or fine-tuning initially |
| External actions | None without explicit review |
| Initiative | Reviewable outbox only |
| Deployment | Local development first |
| Optimization priority | Insight and demonstrable behaviour |

No new hardware purchase is planned for the first roadmap period.

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
→ durable state identifies what changed
→ typed decision layer handles routine semantic routing
→ difficult semantic operations escalate to an LLM
→ proposed updates are validated
→ authoritative state changes atomically
→ response or action is rendered
```

The LLM is important, but it does not own time, authoritative state, permissions, commitment lifecycle, provenance, or operational continuity.

## 6. Initial component model

### 6.1 Auditable event ledger

Records:

- user and system messages;
- observations;
- state-change proposals;
- accepted and rejected updates;
- actions and outcomes;
- model calls and costs;
- timestamps and model/configuration versions.

The ledger is auditable rather than absolutely immutable. It must eventually support deletion, redaction, expiry, derived-data invalidation, and recovery semantics.

### 6.2 Canonical operational state

The first version contains only:

- facts;
- preferences;
- commitments;
- unresolved threads;
- prospective expectations.

Each item includes:

- stable identifier;
- subject and proposition;
- source evidence;
- source type;
- validity interval;
- status;
- confidence or decision strength;
- sensitivity;
- update history;
- contradictions;
- expiry or review conditions.

Do not introduce separate episodic, semantic, relational, and working-memory stores until the simple state model demonstrates an actual limitation.

### 6.3 Typed semantic-reflex layer

Inspired by Jev’s technical philosophy, not its undisclosed implementation.

Responsibilities begin narrowly:

1. Rank whether an event is relevant to existing state items.
2. Classify the relationship between an event and a candidate state item.

Allowed relationship outputs:

```text
supports
contradicts
narrows_scope
supersedes
unrelated
uncertain
```

The layer returns typed probabilities and must be able to abstain. It produces no prose and has no permission to change canonical state directly.

### 6.4 Generative/deliberative LLM

Used for:

- ambiguous interpretation;
- structured extraction that the reflex layer cannot perform;
- novel reasoning;
- hypothesis comparison;
- reconstruction of nuanced context;
- user-facing language.

Two call types remain distinct:

- **Deliberative call:** helps determine what an event means or whether action is warranted.
- **Expressive call:** renders an already selected communicative intent.

### 6.5 State transition validator

Enforces:

- schema validity;
- permissions;
- source attachment;
- temporal consistency;
- update authority;
- sensitivity propagation;
- atomic writes;
- idempotency;
- reversible operations where possible.

A valid JSON object is not necessarily a justified update. Initial automatic updates will therefore be limited to narrow, low-risk transitions.

### 6.6 Context compiler

Produces a bounded task-specific projection containing:

- stable operating instructions;
- current request or operation;
- relevant state items;
- relevant source evidence;
- counterevidence;
- active commitments or constraints;
- permitted output schema.

It must record why each included item was selected and what was omitted.

### 6.7 Prospective state and outbox

Represents:

- expected future events;
- commitments awaiting action;
- unanswered questions;
- deadlines and expiry;
- conditions worth monitoring;
- possible follow-up intentions.

Candidate outreach enters a reviewable outbox. The POC will not send messages autonomously.

## 7. The micro-Jev experiment

### Research question

> Can a small non-generative decision model reliably handle routine memory relationships, reducing generative-model calls while escalating uncertain cases?

### Input

```yaml
existing_state:
  proposition: "The user prefers concise answers for work discussions."
  scope: "work"
  validity: "current"

new_event:
  text: "For open-ended personal research, I prefer detailed exploration."
  occurred_at: "2026-09-17"
```

### Output

```yaml
probabilities:
  supports: 0.02
  contradicts: 0.07
  narrows_scope: 0.82
  supersedes: 0.02
  unrelated: 0.05
  uncertain: 0.02
decision: "narrows_scope"
calibrated_confidence: 0.78
escalate: false
```

### Initial implementations

1. Deterministic rule baseline.
2. Pretrained sentence embeddings for candidate retrieval.
3. Small pretrained entailment or cross-encoder model for pair decisions.
4. Frozen embedding model plus lightweight classifier.
5. General-purpose LLM structured-output baseline.

The project will not attempt to reproduce Jev’s proprietary model architecture, sampler, data, or RLCD training method.

### Escalation policy

Provisional thresholds:

```text
high confidence + reversible update → apply
medium confidence                  → LLM deliberation
low confidence                     → preserve event; no semantic update
```

Thresholds must be selected using held-out examples rather than intuition alone.

## 8. Evaluation design

### 8.1 Decision-layer metrics

- accuracy by relationship class;
- precision and recall;
- calibration curve;
- Brier score;
- autonomous-decision coverage;
- error rate above the action threshold;
- escalation rate;
- median and tail latency;
- total cost and energy proxy where available.

### 8.2 Persistence metrics

- current-fact accuracy after revision;
- commitment precision and recall;
- temporal-scope errors;
- source-support accuracy;
- unauthorized update rate;
- duplicate-event handling;
- restart recovery;
- model-swap continuity;
- deleted-canary leakage.

### 8.3 Context metrics

Measure separately:

- total lifetime history length;
- number of facts relevant to the current task;
- compiled prompt size;
- number of retrieval and deliberation calls;
- total lifecycle tokens, not only response tokens;
- latency and monetary cost.

The bounded-context claim applies only when relevant dependency size remains bounded.

### 8.4 Initiative metrics

- usefulness of surfaced follow-ups;
- precision at a fixed interruption/outbox allowance;
- correct suppression of obsolete prospects;
- correct handling of resolved commitments;
- choice among internal investigation, clarification, outreach, and silence;
- comparison with an ordinary workflow scheduler.

## 9. Required baselines

### Baseline A: rolling summary plus retrieval

Represents a competent conventional memory harness.

### Baseline B: structured state plus ordinary workflow scheduler

Uses the same facts, preferences, commitments, expiry rules, and retrieval infrastructure without generalized consolidation, drives, or inferred initiative.

This is the most threatening practical baseline.

### Baseline C: general LLM for every semantic decision

Measures quality, latency, cost, and consistency when the blunt instrument handles everything.

### Baseline D: oracle-state architecture

Receives perfectly correct gold-standard state updates.

If oracle state succeeds while extracted state fails, the bottleneck is state construction rather than persistence architecture.

## 10. Falsification and simplification gates

### Gate 1 — Representation

**Question:** Can canonical state express the target longitudinal behaviours without relying on transcript reconstruction?

**Pass:** Facts, preferences, commitments, revisions, expiry, and provenance remain operational after restart.

**Fail/simplify:** If most state requires storing prose and asking an LLM to reinterpret it, describe the result as a memory harness and narrow the project.

### Gate 2 — Semantic reflex

**Question:** Can the micro-Jev layer handle a useful fraction of routine decisions safely?

**Pass:** It achieves a predeclared precision threshold while meaningfully reducing generative calls.

**Fail/simplify:** If useful coverage is very low or calibration is unreliable, retain typed interfaces but use LLM deliberation.

### Gate 3 — Persistence

**Question:** Does application-owned state improve continuity over summary plus retrieval?

**Pass:** Better longitudinal accuracy or lower total lifecycle cost on held-out histories.

**Fail/simplify:** If the conventional harness matches it, reduce the architecture to the simpler implementation.

### Gate 4 — Initiative

**Question:** Does prospective state improve useful follow-up beyond an ordinary scheduler?

**Pass:** Higher usefulness at a matched outbox/interruption rate on novel cases.

**Fail/simplify:** Call the feature workflow notifications and avoid agency claims.

## 11. Eight-week implementation plan

### Week 1 — Charter, schemas, and repository

Deliverables:

- approve this roadmap;
- initialize repository and development environment;
- define event and state schemas;
- define authority, expiry, deletion, and sensitivity rules;
- create ten worked lifetime-state examples;
- specify baselines and metrics before implementation.

Exit criterion: an event can be manually converted into a justified state transition with explicit provenance.

### Week 2 — Event ledger and canonical state

Deliverables:

- SQLite event store;
- facts/preferences/commitments/prospects tables;
- atomic transition API;
- idempotent event ingestion;
- restart and replay test;
- minimal command-line inspector.

Exit criterion: state survives a complete process restart and reconstructs deterministically from permitted records.

### Week 3 — Synthetic lifetime generator and gold set

Deliverables:

- scripted histories containing preferences, corrections, promises, expiry, contradictions, gaps, and irrelevant events;
- manually reviewed holdout cases;
- deleted-canary scenarios;
- gold state at selected checkpoints.

Exit criterion: the evaluation data distinguishes current truth from historical assertion and operating assumption.

### Week 4 — Retrieval and relationship baselines

Deliverables:

- deterministic rules;
- embedding retrieval;
- LLM structured-output baseline;
- common typed decision API;
- latency, token, and cost logging.

Exit criterion: all baselines process the same cases through the same interface.

### Week 5 — Micro-Jev decision layer

Deliverables:

- small encoder or embedding-plus-classifier implementation;
- training and held-out data split;
- calibrated probabilities;
- abstention and escalation policy;
- calibration and error report.

Exit criterion: decide whether the reflex layer earns continued use.

### Week 6 — Context compiler and chat loop

Deliverables:

- task-specific state projection;
- source and counterevidence inclusion;
- LLM adapter;
- validated response/update cycle;
- comparison of prompt size against history growth.

Exit criterion: a working chat loop whose canonical state persists independently of its prompts.

### Week 7 — Prospective state and outbox

Deliverables:

- explicit commitments and expected-event maturation;
- candidate follow-up generation;
- suppression of resolved, expired, or unauthorized items;
- ordinary workflow-scheduler baseline;
- reviewable outbox.

Exit criterion: candidate outreach is causally traceable and never sent automatically.

### Week 8 — Demonstration and decision

Deliverables:

- accelerated lifetime run;
- complete restart demonstration;
- model-swap demonstration;
- context-growth comparison;
- micro-Jev vs LLM vs rules report;
- scheduler vs prospective-state comparison;
- concise system inspector;
- go/revise/stop decision for the next phase.

## 12. Demonstration narrative

The final POC should demonstrate, without relying on visual spectacle:

1. The user creates a preference and a commitment.
2. Thousands of unrelated events accumulate.
3. The preference is narrowed or revised.
4. The system preserves the original source and current interpretation.
5. The process is terminated completely.
6. It restarts with commitments and current state intact.
7. A different LLM backend is selected.
8. Operational continuity remains while expression changes.
9. An obsolete follow-up is correctly suppressed.
10. A justified new follow-up enters the outbox.
11. Every transition shows its evidence and decision path.
12. Per-call context remains approximately flat for tasks with fixed relevant dependency size.

## 13. Budget plan

| Category | Monthly target | Hard ceiling |
|---|---:|---:|
| Generative model APIs | CAD $25 | CAD $50 |
| Embedding or specialist APIs | CAD $0 | CAD $10 |
| Cloud compute | CAD $0 | CAD $20 |
| Hosting | CAD $0 | CAD $10 |
| Contingency | CAD $15 | CAD $30 |
| Total | CAD $40 | CAD $100 |

All model calls must record estimated cost. Local computation is preferred when it does not consume disproportionate development time.

## 14. Initial software choices

Provisional rather than binding:

- Python 3.12+
- `uv` for environment and dependency management
- SQLite for events and canonical state
- SQL migrations from the beginning
- Pydantic or typed dataclasses for boundaries
- pytest for state-transition and replay tests
- Sentence Transformers for local embeddings/encoders
- scikit-learn for lightweight classifiers and probability calibration
- one backend-neutral LLM adapter
- a minimal local web inspector only after the command-line loop works

Avoid initially:

- distributed infrastructure;
- vector-database services;
- Kubernetes;
- autonomous external tools;
- multiple agent frameworks;
- elaborate graphical worlds;
- training a generative model;
- premature plugin architecture.

## 15. Security and privacy boundaries

The POC must enforce:

- no autonomous external messages;
- no autonomous spending or account creation;
- explicit separation of assertion, inference, and operating assumption;
- sensitivity inherited by derived state;
- provenance for every durable semantic update;
- deletion tests covering sources and derivatives;
- protection against persisted prompt injection;
- expiry for inferred goals and prospects;
- user-visible inspection and correction;
- no optimization target for engagement or relationship continuation.

## 16. Decision log

### Accepted

- Treat biological cognition as optional inspiration, not a privileged blueprint.
- Define the agent operationally as persistent application-owned state plus its processes.
- Treat LLMs as replaceable semantic processors.
- Eliminate cognitive session boundaries while retaining task, topic, privacy, and UI scopes.
- Begin with a narrow typed semantic-reflex layer.
- Compare against strong practical baselines.
- Measure total lifecycle cost.
- Keep initiative in a reviewable outbox.

### Rejected for initial POC

- Full cognitive-module simulation.
- Literal neuron modelling.
- Claims of consciousness.
- A generalized drive system.
- Relationship maintenance as an intrinsic objective.
- A game or graphical environment.
- Treating spontaneous messaging as sufficient evidence of agency.
- Reproducing Jev’s proprietary architecture.

### Deferred

- Rich episodic and semantic memory separation.
- Background consolidation.
- Procedural learning.
- Adaptive routing.
- Learned initiative policies.
- Local generative-model inference.
- Multiple users and relationship boundaries.
- Audio, vision, embodiment, and external tools.
- Long-term model-weight adaptation.

## 17. Immediate first build slice

The first implementation milestone is intentionally small:

> Ingest an event, retrieve a potentially affected state item, classify their relationship through a typed interface, propose a source-linked transition, apply it atomically, restart the program, and recover the same authoritative state.

The first six example histories should cover:

1. Reinforcement of an existing preference.
2. Direct contradiction.
3. Scope narrowing.
4. Temporal supersession.
5. Irrelevant event rejection.
6. Ambiguity requiring abstention and escalation.

No chat UI is required to complete this slice.

## 18. Roadmap completion criteria

At the end of eight weeks, make one of three explicit decisions:

### Continue

The architecture provides measurable continuity or efficiency beyond the practical baselines, and at least one component warrants deeper investment.

### Revise

The central persistence goal remains valuable, but the typed reflex, state model, context compiler, or initiative mechanism requires replacement.

### Stop or simplify

A conventional summary/retrieval system or structured workflow captures nearly all demonstrated value. Preserve useful components and abandon broader architectural claims.

## 19. North-star statement

> Create an AI assistant whose lived experience is durable, accountable, and independent of any one context window—while using the least expensive form of intelligence appropriate to each decision.
