# G3 v21 evidence-builder remediation

**Recorded:** 2026-09-22T13:51:55Z  
**Base commit:** `a0ec5d0a92aaa738195a4691820a422012c712b3`  
**Working-tree status:** dirty, only for the remediation changes documented below; pre-existing untracked `.g3audit/` and `.remember/` directories were not modified.

## Scope and decision

This record closes three post-v21 evidence-tooling findings without changing
the sealed corpus content or its review provenance:

1. `scripts/build_g3_frozen_evidence.py` now writes the caller-supplied
   `expected_manifest` into `g3-gate-record.json`, rather than the legacy v15
   default constant.
2. `_validate_review_findings()` now rejects an open, malformed, or
   closed-without-rationale review finding. A `resolved` or `rejected`
   finding must carry a non-empty `summary` rationale.
3. **Correction to this document's original wording:** a subsequent review
   found that fix (2) was only ever called from `build_review_artifacts()`.
   `build_evidence()` -- the entry point that actually produces the final
   `g3-gate-record.json` -- copied `review_output`'s raw bytes into the
   evidence packet without validating its contents at all, so a bare `{}`
   or any other malformed stand-in for a review record would have been
   silently accepted. This did not affect the real v20/v21 evidence, which
   was hand-built and independently verified by direct inspection rather
   than generated through this script's `evidence` subcommand -- but the
   script itself was genuinely exploitable. Fixed: `build_evidence()` now
   loads `review_output` through `_load_hashed_artifact()` against the real
   review-record JSON schema (the same validator `seal_staged_corpus()`
   uses) before calling `_validate_review_findings()` on its findings. Three
   new tests prove this: a malformed `{}` review output is rejected, a
   schema-valid record with a genuinely open finding is rejected, and the
   real v20/v21 review record (with 6 real resolved/rejected findings) is
   still accepted.

The v21 payload is unchanged from v20: development data, holdout data, family
specifications, assignment manifest, near-duplicate adjudication, and the
review record have identical bytes. No reviewer identity, finding disposition,
or approval has been fabricated or rewritten. This is a focused tooling
remediation; it is not a replacement for the existing content review.

**G3 decision:** `PASS` for the existing sealed v21 corpus and the remediated
evidence builder, subject to committing these recorded changes. G4 model
execution and holdout evaluation remain separately unauthorized.

## Exact bindings

| Artifact | SHA-256 |
| --- | --- |
| sealed v21 manifest (file) | `1290f62d37f17e9b1734adce9c028fac1629ac3e35726a6a8c9bd8192ac8bf02` |
| sealed v21 manifest (declared) | `9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3` |
| v21 review record | `7598c4e4e9955315fa4e3d481d3525c5e3f933778277b2feff018652c263d557` |
| development payload | `9393b6ee9dbb845f19e2c08a8e4222b7fa427b280ecee7f168d9ef64df05686d` |
| holdout payload | `638ba6a239d578ab93356976692e117e9f424035460704fa4758989f61c64883` |
| family-spec payload | `5cf2eb4765fecfe33446361913189ac56ab9ce3aaec0b638ec4c5553e563c982` |
| assignment payload | `8e6e3680d646dcf6c61abd8f0ad20d57c3c0d6bd634ffd645cb4d13a712c5a3c` |
| near-duplicate adjudication | `99ff30bbaa4085f29fff0795a21f36096f74c0109c9ca17ce7f7c0415b0bc9d9` |
| dependency lock | `bcfd91f05df0650318d5afb550175b2586770de59955449250cb4ddab9cc62cd` |
| remediated evidence builder | `db63daf1616b7e2d724caa5ff483544c1568e74b050740c1a072233549c263a1` |
| regression tests | `fc16a48551d4f2e0c960dd8d27ab26bfe70e2b6de4f2322498dfd7360aa99ea2` |

## Procedure and results

Environment: Python managed by `uv 0.12.17 (Homebrew 2026-09-18 aarch64-apple-darwin)`.

| Command | Result |
| --- | --- |
| `uv run --frozen pytest -q tests/test_build_g3_frozen_evidence.py tests/test_g3_frozen_smoke.py tests/test_g4_evaluation_config.py` | `13 passed` |
| `uv run --frozen pytest -q` | `108 passed in 141.30s` |
| `uv run --frozen python scripts/stage_frozen_g4_corpus.py verify --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v21` | `PASS`; manifest `9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3` |
| `uv run --frozen python scripts/run_g3_frozen_smoke.py --corpus evaluation/corpus/frozen-g4-v0.1-sealed-v21` | `PASS`; 405 histories, 1,620 pairs, zero leakage failures, zero learned calls |

The new regression coverage proves that a v21 invocation of `build_evidence()`
records the supplied v21 staging-manifest hash rather than the historical v15
constant. It also proves that open findings and closed findings lacking a
non-empty rationale are rejected, while substantiated resolved/rejected
findings are accepted.

## Deviations and limits

- No new reviewer report was authored or substituted. The existing sealed-v21
  review record is the authoritative content-review provenance.
- The remediation script and its test are not among v21's sealed corpus source
  dependencies. Accordingly, no corpus restage or reseal was performed.
- This record establishes G3 evidence-tool correctness only. It does not
  authorize G4 predictions, tuning, or holdout evaluation.
