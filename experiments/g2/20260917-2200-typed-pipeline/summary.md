# Gate evaluation: G2 — 20260917-2200-typed-pipeline

## Claim

Semantic interpretation proposes changes through a typed boundary, while a deterministic validator retains mutation authority.

## Build identity

- Commit: `a0de5d7525210389da9f450417adb3629d001c62`
- Working tree clean: yes
- Dependency-lock SHA-256: `ebd3e13fc2dc3a064e7b0aeb20de5160c53756616db70abf691630914dbbc11b`
- SQLite schema version: 2

## Frozen procedure

```sh
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g2-evidence uv sync --frozen
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g2-evidence uv run --frozen pytest -q
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g2-evidence uv run --frozen python scripts/g2_demo.py /private/tmp/lifetime-ai-g2-evidence.sqlite
```

## Results

| Case | Expected boundary behaviour | Result |
|---|---|---|
| supports | Reinforce one item without duplication | PASS |
| contradicts | Preserve prior item and conflicting evidence | PASS |
| narrows_scope | Preserve general and scoped items | PASS |
| supersedes | Atomically close prior interval and create replacement | PASS |
| unrelated | Record no-op; no semantic mutation | PASS |
| uncertain | Record abstention and escalation; no mutation | PASS |
| Missing source | Reject and record reason | PASS |
| Unknown relationship | Reject at typed parse boundary | PASS |
| Unauthorized kind/operation | Reject before persistence | PASS |
| Temporal conflict | Reject invalid interval | PASS |
| No candidates | Reject mutation proposal | PASS |
| Validator failure | Roll back all canonical writes; record rejection | PASS |
| Classifier replacement | Test double uses unchanged persistence | PASS |

Complete suite: `20 passed in 0.26s`.

The fixture matrix is `tests/fixtures/g2_relationships.json`. The enforced mutation boundary is documented in `docs/g2_mutation_boundary.md`.

## Manual end-to-end transcript

```text
event: demo-scope
candidate: demo-preference
relationship: narrows_scope (confidence 0.85)
proposal: proposal:demo-scope
validator outcome: accepted
canonical digest before close: 4be99b84055e43dc6227fae7396734b9343a90ab73ae9b8426e688bb9e2fcd23
process closes and database reopens
canonical digest after restart: 4be99b84055e43dc6227fae7396734b9343a90ab73ae9b8426e688bb9e2fcd23
recovered active state:
  - demo-preference: "I prefer concise answers."
  - demo-preference:scope:demo-scope: "For personal research, I prefer detailed answers."
source events and transition reasons are present for both items
```

## Mutation authority

The classifier, selector, and proposal builder are pure components with no `Store` reference. Only `TransitionValidator` invokes `Store.commit_proposal`, which atomically writes accepted transitions, canonical state, audit entries, and the accepted proposal record. Invalid, uncertain, and irrelevant proposals are source-linked and distinguishable as `rejected`, `abstained`, or `noop`.

## Failures and exclusions

No failed example was excluded. The learned accuracy of relationship decisions, embedding retrieval, and LLM escalation remain explicitly deferred by G2.

## Decision

`PASS`

## Rationale and next action

All required and adversarial scenarios use the same typed interface; semantic components have no canonical write authority; and restart preserves the accepted result. Proceed to G3 evaluation readiness before adding learned semantic components.
