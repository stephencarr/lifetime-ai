# Gate evaluation: G1 — 20260917-2140-durable-state

## Claim

The application—not an LLM prompt—owns state that is durable, source-linked, atomically updated, and safe to replay.

## Build identity

- Commit: `cde6e894d9b87bae2fac5d6461368ee5928485a0`
- Working tree clean: yes
- Dependency-lock SHA-256: `ebd3e13fc2dc3a064e7b0aeb20de5160c53756616db70abf691630914dbbc11b`

## Environment

- Hardware: MacBook Air `Mac16,12`, Apple M4, 16 GB
- OS: macOS 26.5.1, build 25F80
- Python: 3.13.11
- pytest: 8.4.2
- SQLite schema version: 1

## Commands

```sh
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g1-final uv sync --frozen
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g1-final uv run --frozen pytest -q
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g1-final uv run --frozen python -m lifetime_ai.inspect_db /private/tmp/lifetime-ai-g1-final.sqlite
```

The cache override is required only by the managed execution sandbox. No dependency or runtime behaviour changed.

## Results

| Scenario | Observed | Result |
|---|---|---|
| S1 identical event replay | Exact replay returned a no-op; one ledger row | PASS |
| S2 identifier collision | Conflicting event payload rejected; original retained | PASS |
| S3 source enforcement | Missing and inconsistent sources rejected without residue | PASS |
| S4 atomic rollback | Injected post-state-write failure rolled back event, transition, state, and audit | PASS |
| S5 transition replay | Exact replay was idempotent; conflicting reuse rejected | PASS |
| S6 restart recovery | Fresh process recovered identical state/provenance digest | PASS |
| S7 foreign-key enforcement | Every Store connection enabled FKs and rejected invalid writes | PASS |
| S8 deterministic replay | Two rebuilds produced the original canonical digest | PASS |

Test result: `9 passed in 0.15s`. Orphaned transitions: 0. Orphaned state items: 0. LLM calls: 0.

Pre-restart and replay digest:

```text
4fbfd70cb95735bb96f6d621080b7625b145f28ce1cd9d2e7e6f9121506e319e
```

## Inspector output

```json
[
  {
    "item_id": "preference-1",
    "kind": "preference",
    "last_transition_id": "transition-1",
    "proposition": "I prefer concise work answers.",
    "source_event_id": "event-preference-1",
    "source_event_type": "user_message",
    "source_text": "I prefer concise work answers.",
    "status": "active",
    "transition_reason": "explicit user preference"
  }
]
```

## Failures and deviations

The pre-gate skeleton silently accepted conflicting identifier reuse and did not rebuild state during replay. Those defects were corrected before this frozen run and remain represented by collision and replay regression tests. No result was excluded.

## Decision

`PASS`

## Rationale and next action

All eight required scenarios pass, replay is model-free and deterministic, provenance is inspectable, and no orphaned records remain. Proceed to G2's typed proposal/validation pipeline without granting semantic components direct persistence access.
