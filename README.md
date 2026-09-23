# Lifetime AI

A model-free persistent runtime foundation for durable, source-linked operational state.

**M5 status:** The current local chat UI is a diagnostic workflow. A separate local-model construction, semantic support, and indexed retrieval path now exists, but its first frozen development scores failed and participant UAT is paused. See [the M5 POC architecture reset](docs/m5_poc_architecture_reset_2026-09-23.md) and [the model development record](docs/m5_model_development_2026-09-23.md).

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

The core runtime contains typed events and state, SQLite persistence, source-linked atomic transitions, restart recovery, and tests. A small local chat workflow now exercises capture, cited retrieval, correction, and source deletion through the same validator. The bundled rule extractor is an explicitly named preflight adapter, not a claim about raw-message capture quality; extractor and response rendering remain swappable and no hosted model dependency is required.

## Inspecting state provenance

The model-free inspector prints each authoritative item together with the source event and transition that established its current value:

```sh
uv run --frozen python -m lifetime_ai.inspect_db path/to/state.sqlite
```

SQLite schema changes are versioned through `PRAGMA user_version` and the `schema_migrations` table. The current schema version is 5.

## Local terminal chat

Run the small terminal-style preflight interface against a local SQLite file:

```sh
uv run --frozen lifetime-chat path/to/state.sqlite
```

Plain messages use the explicit preflight extractor. Prefix a question with `?` to retrieve current state with source citations. `:state`, `:correct ITEM TEXT`, and `:forget SOURCE` expose the lifecycle controls used by the M5 preflight. `:forget` hides the source and its derived state from retrieval but retains the original text in the local ledger; it is not complete erasure. This interface is intentionally local and does not send data anywhere.

For a visible terminal-style browser view, run:

```sh
uv run --frozen lifetime-web path/to/state.sqlite --port 8767
```

Open `http://127.0.0.1:8767/` on the same computer. The server binds to loopback only, uses no external assets or services, and shares the same `ChatRuntime` and SQLite state path as the CLI. Start with a fresh local database for a new preflight; do not use private `.uat` diagnostic data.

The frozen synthetic M5 preflight can be rerun with:

```sh
uv run --frozen python -m lifetime_ai.m5_preflight --output /tmp/m5-preflight.json
```

See [the M5 synthetic capture preflight](docs/m5_synthetic_preflight_2026-09-23.md) for its development history. The later [retrieval and answerability development run](docs/m5_answerability_development_2026-09-23.md) specifies a source-support contract, freezes 48 synthetic questions, and records all three scored attempts. The current answer path scans up to 128 live claims and uses a limited, declared support grammar. It abstains outside that grammar or when the candidate set is incomplete. This does not establish general-language answerability. Participant UAT remains paused.

To rerun the frozen answerability development instrument and retain a new attempt:

```sh
uv run --frozen python -m lifetime_ai.m5_answerability_preflight
```

## Local semantic M5 development route

The first product-shaped route is separate from `lifetime-chat` and `lifetime-web`. It uses local llama.cpp with the pinned Qwen3-8B GGUF for claim proposal, source support, reconciliation, and answer checks; a pinned BGE small embedding model; SQLite FTS5; and a USearch HNSW candidate index. Model identity and cached weight hashes are checked against [the model lock](evaluation/m5_model_poc/model_lock.json). There is no keyword-only fallback. The browser view still uses the diagnostic route.

With `llama.cpp` installed and both pinned weights cached, start the two loopback model servers in separate terminals:

```sh
llama-server -hf Qwen/Qwen3-8B-GGUF:Q4_K_M --host 127.0.0.1 --port 8768 -c 4096 --reasoning off
llama-server -hf ggml-org/bge-small-en-v1.5-Q8_0-GGUF:Q8_0 --host 127.0.0.1 --port 8769 -c 2048 --embeddings
```

Use a new synthetic development database only. The `--create` or `--open-existing` choice is mandatory:

```sh
uv run --frozen --group m5 lifetime-model-chat /tmp/lifetime-model-dev.sqlite --create
uv run --frozen --group m5 python -m lifetime_ai.m5_model_poc
```

The servers shown above have no authentication and are for local synthetic evaluation only. Do not send participant data through them. The model route has a frozen integrated development instrument in [evaluation/m5_model_poc/v0.1](evaluation/m5_model_poc/v0.1) and retains every scored attempt in `experiments/m5_model_poc`. [The development record](docs/m5_model_development_2026-09-23.md) reports failures and remaining gates. It has not passed participant UAT or formal G5.

The HNSW index is rebuilt from canonical SQLite state on startup. A [frozen synthetic index-scale experiment](docs/m5_index_scale_2026-09-23.md) measures vector capacity separately from semantic retrieval. Both million-vector configurations failed their planted-candidate recall gate (12/32 and 31/32). A separate [local NLI development experiment](docs/m5_nli_development_2026-09-23.md) tested an independent support classifier; it failed its frozen false-support gate and is not part of the product decision path. These failures are retained and do not count as POC success. The current WIP handoff is in [docs/m5_midflight_handoff_2026-09-23.md](docs/m5_midflight_handoff_2026-09-23.md).

## Current handoff

G0–G3 have recorded passes. G4 has a development-only candidate and is paused for review; it has not passed. The diagnostic UAT spike was retired after exposing serious raw-message capture failures. See [the M5 and UAT handoff](docs/m5_uat_handoff_2026-09-23.md) for the current evidence, next product slice, and UAT readiness criteria. The historical G3 pilot is not current gate evidence.
