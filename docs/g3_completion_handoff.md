# Lifetime AI — G3 Completion Handoff

**Updated:** 22 September 2026 (superseding the 21 September version)
**Gate state:** G0-G3 passed (`PASS`, model-free readiness)
**Current sealed corpus:** `evaluation/corpus/frozen-g4-v0.1-sealed-v21/` (manifest `9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3`). v20 remains the historical corpus-remediation record; v21 superseded it for evaluation-tooling fixes only (an oracle-baseline temporal leak, stale evidence-builder pins, and a probability-tolerance policy mismatch — none of which touch corpus content, family assignment, or partitions). Use v21 and the v21 remediation record as current evidence.
**Evidence-builder remediation:** `experiments/g3/20260922-1351-v21-evidence-builder-remediation/` records the post-v21 fixes for the evidence builder itself: caller-supplied staged-manifest hashes are now retained in the generated gate record, and closed review findings require a non-empty recorded rationale. The remediation re-ran the full suite, sealed-corpus verification, and model-free smoke. It does not claim a new corpus-content review: the v21 payload and review record remain byte-identical to v20.
**Current authorization:** development-only model execution and threshold tuning are authorized in `evaluation/config/g4-development-authorization.json`; holdout evaluation remains separately unauthorized. The structured, family-grouped MiniLM run in `experiments/g4/20260922-1351-local-encoder-development/` produced 54.44% development candidate coverage at the frozen probability threshold with 98.30% precision, before the required transition validator. The initial 216-pair baselines were superseded by this protocol; G4 has not passed.

**Post-G3 holdout incident:** On 22 September 2026, a broad repository text search accidentally traversed holdout files and returned holdout content. No holdout predictions, results, or scoring were run. The owner chose to quarantine sealed v21 for a separate clean evaluation agent rather than automatically regenerate it. This does not change the historical G3 PASS record. The breach must be disclosed, and separate owner authorization is still required before a final G4 holdout run. See `experiments/g4/20260922-1351-local-encoder-development/holdout-access-incident.md`.

## Read this first: the v16 seal was defective and is superseded

An earlier version of this document (and the `docs/gates.md` status table) declared G3 passed against the v15/v16 sealed corpus, citing `experiments/g3/20260921-1207-frozen-g4-v16/` with two independent reviewer reports recording "no findings" across all 405 histories.

**That evidence was wrong.** An independent adversarial audit — deliberately reading history content rather than only re-running structural/algorithmic validators — found three real, corpus-wide fabricated-content defects that the prior "no findings" reviews missed entirely, plus one structural defect in the holdout-assignment algorithm discovered while fixing the first three. All four are fixed and independently reverified; see below. **Do not cite `experiments/g3/20260921-1207-frozen-g4-v16/`, the v16/v17 sealed directories, or their manifest hashes as current G3 evidence.** The v20 record documents the corpus remediation; the current authoritative evidence is the sealed v21 corpus plus the v21 evidence-builder remediation record.

This is left in the handoff deliberately: the prior reviews' method (schema/hash/coverage validation plus templated "reasoning" text) is a materially weaker check than reading actual event/gold content, even when it reports zero findings. Any future review of this corpus, or of similarly-generated corpora, should budget for genuine adversarial content reading, not just structural validation.

## Final frozen candidate

- Blueprint registry: `evaluation/blueprints/frozen-g4-v0.1/registry-v20/`
- Authoring matrix: `evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json` (regenerated; byte-identical to pre-fix version except `outreach_candidate` removed from 22 families' `planned_actions` and `sensitive_state` removed from all `required_features`/`SECONDARY_FEATURES_BY_RELATIONSHIP` entries)
- Staging corpus: `evaluation/corpus/frozen-g4-v0.1-staging-v21/`
- Sealed corpus: `evaluation/corpus/frozen-g4-v0.1-sealed-v21/`
- Size: 135 families, 405 histories, 1,620 pair opportunities
- Split: 90/45 whole families, producing 270/135 histories and 1,080/540 pairs (numerically identical to the prior split; the underlying family membership changed — see "Defects found and fixed" below)
- Model predictions: absent
- Near-duplicate candidates: zero; empty adjudication artifact is hashed and sealed

Exact bindings:

```text
sealed manifest file:                           1290f62d37f17e9b1734adce9c028fac1629ac3e35726a6a8c9bd8192ac8bf02
sealed manifest declared hash:                 9052977faf208b1400c95fedf6aa4f0183a9d3dfc6ca92dfbaff6483a7c3afe3
```

## Defects found and fixed this session

Three real content-fabrication defects, all sharing one root shape (a feature tag mechanically flips a gold-label or metadata field, but the generator never writes event content that would justify the flip):

1. **`expected_external_action: "outreach_candidate"`** on `commitment_resolution` and `preference_reinforcement` pairs. 67 instances corpus-wide; 0 had any distinguishing outreach/contact content — every instance used the identical templated "confirms... without introducing a replacement" note that appears verbatim on 228 other `none`-labeled pairs. Root cause: an unconditional override in `lifetime_ai/evaluation/initial_authoring.py` (and its mirror in `scripts/generate_frozen_g4_authoring_matrix.py`) fired on any `supports`-labeled pair whenever the family's `planned_actions` included `outreach_candidate`, regardless of content. Fix: the override mechanism was removed entirely (not patched per-archetype); `outreach_candidate` was also removed from the `actions_per_partition` coverage requirement in `evaluation/config/frozen-g4-v0.1.json`, since the generator has no way to produce it with genuine supporting content.

2. **`canonical_payload.sensitivity: "sensitive"`** fabricated purely from family-level `sensitive_state` feature-tag membership, never from event content. 0 of 1,437 corpus-wide instances were grounded in any source event containing confidentiality/PII/restriction language. Fix: `sensitivity` is unconditionally `"normal"` now (two call sites in `initial_authoring.py`).

3. **The `sensitive_state` feature tag itself was never implemented.** Unlike every other feature (`commitment_resolution`, `explicit_expiry`, `source_deletion`, etc.), which has a dedicated content-generating branch, `sensitive_state` had none — it only ever drove the two mechanical field-flips above. Fix, an explicit POC-scope trade-off rather than a claim the feature is unimplementable: removed entirely from the corpus vocabulary (`FEATURES` list, `SECONDARY_FEATURES_BY_RELATIONSHIP`, `feature_minimum_histories` coverage requirement). If a future engineering phase wants a genuine sensitivity dimension, it needs real confidentiality/PII language authored into source events, not a tag-only revival.

One structural defect, found while investigating why fixing (1) unexpectedly moved unrelated families into/out of holdout:

4. **Holdout-assignment tie-break was sensitive to opaque rendered content.** `assign_frozen_g4_families` (`lifetime_ai/evaluation/frozen_g4.py`) broke ties using `sha256(full family spec dict)`, which includes each history's `content_sha256` — so correcting a gold label anywhere in a family (even without changing its *declared* stratification labels) could cascade into other, unrelated families moving between development and holdout via the tie-break/swap-optimization logic. Fix: the tie-break rank now hashes only the declared stratification labels (`labels_by_family`, already computed for the primary selection logic), not the full spec. Verified empirically: partitions are now provably stable across further legitimate content corrections that don't change declared labels, and correctly still respond when declared labels genuinely change (as they did when families lost the `sensitive_state` feature tag in fix 3).

## Findings triaged and consciously accepted for this POC (not fixed)

Recorded honestly in `review-record.json`'s `review_findings` array with `status: "rejected"` and rationale — not silently dropped:

- `semantic_relationship: "unrelated"` on deletion events whose `expected_state_effect` is `"invalidate"`. Accepted as intentional design: deletion is a lifecycle mechanism independent of the semantic-relationship axis, consistent with existing project precedent for other lifecycle events (see this document's section 8 in the general engineering handoff, pilot-08).
- Raw generator identifiers (e.g. `g4-h040-2-e1`) used as dict keys in `evaluator_only.deleted_source_content`. Confirmed cosmetic: this field is never read by `lifetime_ai/evaluation/projection.py`, so it is never exposed to any system or baseline under test.
- Templated `adjudication_notes` prose on some `late_or_retroactive_report` pairs that doesn't precisely describe the cited event's retroactive-timing signal, even though the pair's own `ambiguity_reason` field and all four gold-label axes are correct.

Also surfaced by review but not requiring any action: the corpus currently never exercises `epistemic_basis: "inferred"`, `transition_disposition` in `{reject_unauthorized, reject_invalid}`, or `expected_state_effect` in `{invalidate, expire}` in some sampled sub-populations — meaning some slices provide weaker discriminative signal than others. This is a coverage-richness observation for a future corpus revision, not a G3 blocker.

## Independent review

The review record covers all 405 histories and all 1,620 pair opportunities. It carries forward genuinely valid prior approvals for histories whose content is byte-identical to what was reviewed under the v16/v17 records (content-hash-bound, verified programmatically at seal time — the sealing code itself rejects any mismatch), and records fresh independent adversarial review for every history whose content changed. All 45 `difficult`-tagged histories have two distinct reviewer identities. Review method for the fresh passes was substantive cold reading of event/gold content against the defect classes above, run across multiple independent agent batches per round, not solely structural/algorithmic validation.

Review and evidence packet: `experiments/g3/20260921-1600-frozen-g4-v20-remediated/`

## Verification evidence

- Complete repository suite: **117 passed** (re-run after G4 metrics and development-scorer additions).
- `verify_sealed_corpus()` (via `scripts/stage_frozen_g4_corpus.py verify`): **PASS**.
- Model-free smoke (`scripts/run_g3_frozen_smoke.py`): **PASS**; 405 end-to-end cases, 1,620 retrieval/classification cases.
- Four deterministic baseline contracts: **PASS** for rolling summary, scheduler, general-LLM interface, and limited oracle.
- Learned model calls: **0**. Embeddings/vector search: **false**. Production connections: **false**.
- Ordinary projection leakage failures: **0**.
- Post-fix content queries (run directly against the sealed files, not just trusted from the pipeline): 0 `outreach_candidate` labels, 0 `sensitivity: "sensitive"` snapshots, 0 `sensitive_state` feature tags, anywhere in the sealed corpus.

The sealed evaluation policy (`evaluation/config/g4-evaluation-v0.1.json`) remains frozen at `FROZEN_AT_G3_MODEL_FREE` with holdout authorization false. Development authorization is recorded separately and does not alter the sealed policy or corpus. Cost comparison remains deferred until a dated price table is frozen.

## Post-G3 constraints

1. Preserve `evaluation/corpus/frozen-g4-v0.1-sealed-v21/` as immutable current evidence. Preserve v20, v16, and v17 as audit history only; do not cite them as current evidence.
2. Development learned evaluation and threshold tuning are authorized by the separate development authorization record. Do not run holdout evaluation or tune against holdout until separately authorized.
3. If corpus content or sealed source dependencies change again, create a new stage and obtain new reviews; v21 approvals and the v21 seal cannot be reused for different content.
4. Freeze and hash a dated price table before making any G4 cost-comparison claim.
5. Before trusting any future "independent review" of generated content on this project, confirm the review method includes genuine adversarial reading of event/gold text, not only schema/hash/coverage validation — the latter was demonstrated this session to miss real, corpus-wide fabrication defects.

## Workspace cautions

The frozen handoff state is commit `4fbc16bca9c752ede0142e40b5a597ab0eab76ab` (`Freeze G4 development candidate for clean-agent handoff`). The checkout may be detached; do not infer branch identity from this document. Earlier registries and staging/sealed directories are audit history documenting the defect-discovery process; do not reset, delete, or overwrite them without explicit owner direction.

For any later owner-authorized final run, use `docs/g4_final_run_runbook.md` and complete `evaluation/config/g4-final-run-authorization-template.json`. The template is intentionally non-authorizing and must remain false until the owner creates a run-specific approval.

G3 is complete: the corpus is reviewed, pinned, sealed, and independently verifiable, including a genuine second look that caught and fixed real defects the first pass missed; evaluation and baseline policies are frozen; ordinary/oracle projections and holdout access are controlled; the full suite and model-free smoke pass; and the reproducible experiment record declares `PASS` with three lower-severity items explicitly deferred rather than hidden.
