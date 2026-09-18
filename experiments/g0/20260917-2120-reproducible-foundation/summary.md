# Gate evaluation: G0 — 20260917-2120-reproducible-foundation

## Claim

The repository can be set up and verified reproducibly on the target Mac without relying on undeclared global state.

## Build identity

- Commit: `0d45cc6b3c676d1ac1d1369bcbc5cc926b0a95c9`
- Working tree clean during both verified runs: yes
- Dependency-lock SHA-256: `ebd3e13fc2dc3a064e7b0aeb20de5160c53756616db70abf691630914dbbc11b`

## Environment

- Hardware: MacBook Air `Mac16,12`, Apple M4, 16 GB
- OS: macOS 26.5.1, build 25F80
- Architecture: arm64
- Python: 3.13.11
- uv: 0.12.15
- pytest: 8.4.2

## Frozen procedure

Run 1:

```sh
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g0-verified1 uv sync --frozen
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g0-verified1 uv run --frozen pytest -q
```

Run 2:

```sh
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g0-verified2 uv sync --frozen
UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache UV_PROJECT_ENVIRONMENT=/private/tmp/lifetime-ai-g0-verified2 uv run --frozen pytest -q
```

`UV_CACHE_DIR` was redirected because the managed execution sandbox cannot write to the default user cache. This changes cache location only, not resolution or runtime behaviour. `UV_PROJECT_ENVIRONMENT` deliberately creates independent clean environments.

## Results

| Criterion | Required | Observed | Result |
|---|---|---|---|
| Supported Python | 3.12+ | 3.13.11 | PASS |
| Locked resolution | No manual edits | Both syncs used `uv.lock` with `--frozen` | PASS |
| Complete test command | Same documented command | `uv run --frozen pytest -q` | PASS |
| First clean environment | All tests pass | 3 passed in 0.03 s | PASS |
| Second clean environment | All tests pass | 3 passed in 0.02 s | PASS |
| Declared dependencies only | No global Python packages | Isolated environments installed six locked packages | PASS |
| README procedure | Setup and test documented | Present in `README.md` | PASS |
| Target hardware | Declared target Mac | Roadmap says M5; host reports M4 | FAIL |

## Failures and deviations

The first attempted supported-environment run failed during collection because the initial `pyproject.toml` lacked a build backend and the local package was not importable. Hatchling was declared, the lockfile was regenerated, and both verified clean runs then passed. The failed attempt has not been excluded from this record.

The larger unresolved deviation is hardware identity: the roadmap declares a base 2026 M5 MacBook Air, while the available host reports an Apple M4 MacBook Air. No performance claim is involved at G0, but the gate's claim explicitly names the target Mac, so this record does not silently reinterpret the target.

## Decision

`FAIL_RETRY`

## Rationale and next action

All software reproducibility criteria pass. Confirm that the M4 MacBook Air is the actual target and revise the roadmap, or repeat this procedure on the declared M5 target. Once that discrepancy is resolved, G0 can be recorded as `PASS` without implementation changes.
