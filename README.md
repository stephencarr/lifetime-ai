# Lifetime AI

A model-free persistent runtime foundation for durable, source-linked operational state.

## Requirements

- macOS on Apple Silicon (current proof-of-concept target)
- [`uv`](https://docs.astral.sh/uv/)
- Python 3.12 or newer (`uv` can provision it when needed)

No globally installed Python package is required.

## Reproducible setup and test

From the repository root:

```sh
uv sync --frozen
uv run --frozen pytest -q
```

`uv sync --frozen` installs the exact dependencies from `uv.lock` and fails if the lockfile is stale. The second command is the single documented command for the complete test suite.

To verify a second clean environment without modifying the project environment:

```sh
UV_PROJECT_ENVIRONMENT=/tmp/lifetime-ai-g0-second uv sync --frozen
UV_PROJECT_ENVIRONMENT=/tmp/lifetime-ai-g0-second uv run --frozen pytest -q
```

## Scope

The core runtime contains typed events and state, SQLite persistence, source-linked atomic transitions, restart recovery, and tests. Separate evaluation code includes a local MiniLM development candidate. There is no active chat interface or integrated product path, and no hosted model dependency.

## Inspecting state provenance

The model-free inspector prints each authoritative item together with the source event and transition that established its current value:

```sh
uv run --frozen python -m lifetime_ai.inspect_db path/to/state.sqlite
```

SQLite schema changes are versioned through `PRAGMA user_version` and the `schema_migrations` table. The current schema version is 2.

## Current handoff

G0–G3 have recorded passes. G4 has a development-only candidate and is paused for review; it has not passed. The diagnostic UAT spike was retired after exposing serious raw-message capture failures. See [the M5 and UAT handoff](docs/m5_uat_handoff_2026-09-23.md) for the current evidence, next product slice, and UAT readiness criteria. The historical G3 pilot is not current gate evidence.
