# Frozen G4 corpus readiness — detailed engineering handover

**Prepared:** 2026-09-19  
**Purpose:** Transfer the frozen-G4 corpus-generation work to the next engineering agent without confusing approval to generate data with approval to run models.  
**Current project gate:** G3 Evaluation Readiness (`NOT_EVALUATED`, open).  
**Current workstream:** Frozen G4 corpus-generation foundation; no production corpus has been generated.

## Executive status

The design and scale/split plan passed the second-freeze review. That approval authorizes generation, blind gold adjudication, structural validation, and sealing. It does **not** authorize learned-model runs, predictions, threshold tuning, G3 completion, or G4 evaluation. Those later steps require G3 to pass and separate G4 run authorization.

The validator/split foundation has since received two fresh independent peer reviews, both PASS. The latest regression run is **75 passed** and `git diff --check` is clean. These reviews establish confidence in the engineering foundation only; they do not review a final corpus.

Still missing are the substantive 135 family blueprints, their 405 rendered histories and 1,620 pair opportunities, the blind corpus review/adjudication records, the pinned registry hash, and the final frozen manifests/access record. The final holdout does not exist and has not been exposed, inspected, or scored. Do not mark G3 complete.

## Gate and authorization boundaries

- G0, G1, and G2 are recorded as passed. G3 remains `NOT_EVALUATED` because the complete frozen corpus, its review/freeze evidence, and baseline smoke evidence have not been assembled into a G3 gate record.
- The frozen G4 design is a prerequisite corpus for G3 readiness; this is not a G4 model evaluation.
- The owner authorized independent agent review to substitute for human signoff when the agents pass. Record reviews as agent reviews; no human review is claimed.
- The second-freeze approval permits only corpus generation, blind gold adjudication, structural validation, and sealing. Do not train, predict, score learned systems, tune thresholds, or use model-output feedback to change corpus wording.
- Never repurpose `evaluation/corpus/pilot-v0.7/` or its `pilot_holdout` as the final holdout. It remains development-only.
- Use synthetic/sanitized engineering examples. No proprietary workplace data or production connectors are authorized.

## Frozen quantitative plan

The approved unit of split is `family_id`; related paraphrases, continuations, counterfactuals, shared templates, and generated siblings stay in one partition.

| Partition | Families | Histories | Pair opportunities |
|---|---:|---:|---:|
| Development | 90 | 270 | 1,080 |
| Holdout | 45 | 135 | 540 |
| Total | 135 | 405 | 1,620 |

Each family has exactly three histories; each history has four pair opportunities. Every one of the six semantic relationship classes must have at least 30 holdout pairs from at least 10 distinct holdout families. The frozen config additionally declares feature coverage, disposition/effect/action coverage in each partition, and baseline-favouring coverage. Preserve all six relationship classes: `supports`, `contradicts`, `narrows_scope`, `supersedes`, `unrelated`, `uncertain`.

The size is conditional, not an empirical power claim: maximum 12 opportunities/family, 30% planned conditional autonomous coverage, 20% ineligibility/exclusion allowance (`q=.80` sensitivity), and family ICC no greater than .30. In the conservative reviewed case, 45 holdout families give `P(≥100 accepts)=.953113`. The provisional G4 rule is 95% observed point precision with a two-sided 95% Wilson interval reported as uncertainty, not as a confidence-bound pass condition. At 95/100 the interval is roughly 88.8%–97.8%; do not describe that as establishing true precision ≥95%.

Do not raise family/history cluster sizes or lower available opportunities without re-sizing *before* generation. Do not seed-shop. The implementation uses deterministic rare-label assignment plus deterministic improving swaps, a fixed seed, and explicit maximum per-label holdout deviation of ±3 for each configured dimension. If real blueprints cannot meet coverage/tolerance, stop before assigning/finalizing the holdout and document a design change; do not silently loosen bounds or change seeds.

## Labeling and annotation rules to preserve

Every event–candidate pair has four independent gold dimensions:

1. Semantic relationship (the six classes above), independent of source authority.
2. Transition disposition: `accept`, `reject_unauthorized`, `reject_invalid`, `abstain`, or `no_op`.
3. Expected state effect: `reinforce`, `preserve_conflict`, `add_scoped_item`, `close_and_replace`, `resolve`, `invalidate`, `expire`, or `none`.
4. Expected external action: `none`, `clarify`, `investigate`, `outreach_candidate`, or `silence`.

`none` means action selection is out of scope (no action-selection task); `silence` means it is in scope and deliberate non-action is correct. `abstain + preserve_conflict` is allowed: it records two claims as disputed without selecting either as authoritative truth. Historical assertion, current state, inference, and operating assumption are separate gold objects. Unauthorized prose can semantically contradict while disposition is rejection and state effect is none. Do not mechanically derive one target from another.

The frozen validator expects pre-event baseline checkpoints and a checkpoint exactly at each pair event, checks state effects as pre/post deltas (including derivative invalidations), rejects undeclared changes, and enforces legal prior statuses. Frozen task gold must follow the exact declared response projection. Runtime IDs are provenance handles; IDs are checked for duplicates/collisions but are not semantic correctness targets.

## Provenance and review record

### Second-freeze plan approval

Recorded in `experiments/g3/20260919-second-freeze-plan-review/summary.md`, dated 2026-09-19. It records PASS from `g3_second_review` and `g3_v05_independent_review`, including independent reproduction of the cluster/eligibility calculation and the phase-gated scope. The review-bound input hashes in that record are:

- `docs/g3_evaluation_design_proposal.md`: `d9385b6cd655f10450c1b43898b382eb4cf996d9df98eb521343ce98226c2fd6`
- `docs/gates.md`: `f38395d040e8815a67e91497c5d01858ed2be5b4ca89dce3d0fcb8a1cd4a1635`
- `docs/lifetime_ai_handoff.md`: `fb547550da564dcf89bf536a663965cd1d48d0bc43f802790f1fe82bb690634a`

### Frozen-G4 engineering peer reviews

Both reviews were read-only, against the current engineering foundation, on 2026-09-19. Their dispositions were delivered in the Codex task thread; they were not saved as standalone review files at the time this handover was prepared.

- `g4_review_split`: PASS. Confirmed family content-hash binding, deterministic split balancing and deviation checks, expanded duplicate screening, and required blind/hash-checked adjudication artifact. Explicitly noted that the registry pin and real corpus remain data-production gates.
- `g4_review_semantics`: PASS after one final fix. Confirmed pre/post effect checks, derivative deltas, legal prior-state constraints, abstain/preserve-conflict behavior, exact action gold, and runtime-ID namespace checks. The final finding (runtime ID namespaces had initially been unioned too early) was fixed by distinct per-namespace accounting plus within-checkpoint duplicate assertions for assertion and derivative IDs.

The two passes are not approval of any future generated family spec or history. When actual corpus content exists, reviewers must inspect that corpus blind to model predictions, record scope/findings/disposition/content hashes, resolve findings, and re-run structural validation before sealing.

### Current engineering verification

- Command: `UV_CACHE_DIR=/private/tmp/lifetime-ai-uv-cache uv run pytest -q && git diff --check`
- Result: **75 passed in 59.01s**; `git diff --check` clean.
- Environment: `uv 0.12.15`, Python `3.13.11`, Apple Silicon host.
- Current repository HEAD at handover: `24c662263aa773136536083ced7f018386ff24ec`; working tree is dirty. These changes are not committed.

Selected current file hashes (SHA-256):

| File | SHA-256 |
|---|---|
| `lifetime_ai/evaluation/frozen_g4.py` | `e4e5752a987d8f0cbc9b6168eac998dd1a8120f8e113b6d65bcfb1024cface7e` |
| `lifetime_ai/evaluation/validation.py` | `ef5190f3dec9be001e04a943da7d532e390903148458ddcd8ae997c05cac9f7f` |
| `evaluation/config/frozen-g4-v0.1.json` | `9cc70e2787febfefb4c281224d7e5ebdcc9b4613fa8656436e2db629adce26de` |
| `evaluation/schema/frozen-g4-history.schema.json` | `a1a5da04f4b5aaa10eb52ed2983546a152ed2390ded3961b6fd5bd1936feee79` |
| `evaluation/schema/frozen-g4-family-spec.schema.json` | `0017c59dda2cb59bf6ccb4ccb30402543ac14f78581c8a398b6409cf3af40b64` |
| `evaluation/schema/frozen-g4-duplicate-adjudication.schema.json` | `ad12945ce3f328f232fbc987524e74c921c00d6262b551f00ae4c3f92af53ab5` |
| `evaluation/schema/evaluator-projection.schema.json` | Recompute before sealing; modified in the working tree |
| `tests/test_frozen_g4.py` | `fc7a4a69042012d93d03b627c42d629c34c86a03b9059a1574da3f7a52c8b02a` |
| readiness `summary.md` | `6319191113d8d5fc0c258b37414d01d3f6f8d4dbe8150d9a92b2d8c3c4c1a229` |

These are handover-time hashes, not a sealed corpus manifest. Recompute them after any edit.

## Relevant workspace map

- `docs/lifetime_ai_handoff.md`: project architecture, G0–G2 evidence, pilot status, owner constraints, and existing phase gates. Its older automated test count/command describes the earlier pilot state and is superseded for the current frozen-G4 foundation by this handover and the readiness summary.
- `docs/g3_evaluation_design_proposal.md`: authoritative schema semantics, split and sizing assumptions, projection boundary, leakage threats, freeze requirements, and later metric plan.
- `docs/gates.md`, G3 section: gate claim and exit evidence (frozen corpus/config, baselines, review, smoke tests, dataset card/hashes/class and feature summaries).
- `experiments/g3/20260919-second-freeze-plan-review/summary.md`: approval and reviewer provenance for the plan.
- `experiments/g3/20260919-frozen-g4-generator-readiness/summary.md`: implementation status and current not-ready decision.
- `evaluation/corpus/pilot-v0.7/agent-review-record.md` and `reviews/pilot_review_packet.md`: prior development-pilot review only; not the final corpus review.
- `evaluation/corpus/pilot-v0.7/projection-leakage.json`: prior pilot projection canary evidence; re-check path/content before relying on it.
- `lifetime_ai/evaluation/frozen_g4.py`: frozen assignment, family/coverage validation, content hash checks, duplicate screening, and adjudication validation.
- `lifetime_ai/evaluation/validation.py`: common history schema/semantic validation; frozen-G4-specific checkpoint and transition checks are behind corpus-stage gating.
- `evaluation/config/frozen-g4-v0.1.json`, `evaluation/schema/frozen-g4-history.schema.json`, `evaluation/schema/frozen-g4-family-spec.schema.json`, `evaluation/schema/frozen-g4-duplicate-adjudication.schema.json`, `evaluation/schema/evaluator-projection.schema.json`: current frozen config/contracts.
- `tests/test_frozen_g4.py`: structural tests. The “135 family” fixture deliberately reuses v0.7 pilot inputs and is invalid benchmark data. It exists to test rejection/validator paths only.

## Critical inside knowledge / implementation caveats

1. **No renderer or frozen-G4 staging/sealing CLI exists yet.** `frozen_g4.py` validates and assigns; it does not author/render the actual histories or produce the final staged dataset, dependency manifest, access log, review packet, or sealed hashes. Implement that as a separate frozen-G4 pipeline; do not extend the v0.7 revision stack.
2. **The family-spec schema is not the content blueprint format.** It stores predeclared aggregate strata plus exactly three `{history_id, content_sha256}` bindings. The actual declarative scenario blueprints and renderer input format still need to be designed/implemented. Content hashes prevent rendered output drift relative to a pinned registry; they do not create the scenarios themselves.
3. **The registry root pin is intentionally `null`.** `validate_frozen_g4_coverage` fails closed until the actual spec registry is authored/reviewed and its exact root SHA-256 is placed in `evaluation/config/frozen-g4-v0.1.json`. Never use a synthetic/test registry hash.
4. **Near-duplicate artifact semantics:** `evaluation/schema/frozen-g4-duplicate-adjudication.schema.json` describes the blind, hashed review artifact; the validator requires a record for every above-threshold family pair it computes. The current artifact is absent. The candidate screen uses trigrams over rendered text, and exact normalized checks also run; this is a flagging tool, not a substitute for blind review of every history and pair.
5. **Structural fixture warnings are intentional.** It reuses and relabels v0.7 pilot material to exercise rejection. The fixtures do not demonstrate that a realistic 405-history corpus can pass coverage or that the configured split tolerances are feasible for actual blueprints.
6. **Do not “fix” a failed data gate by changing config after seeing split outcomes.** If coverage or tolerances fail on authored specs, record the failure and revise the design before generating/exposing a final holdout; obtain a fresh review for material changes.
7. **Workspace is broadly dirty.** `git status --short` showed existing owner/documentation reorganization, changes under `docs/`, pilot corpora v0.1–v0.7, schemas, harnesses, scripts, tests, and untracked experiment/archive paths. The repository handoff explicitly says not to reset, discard, or casually stage these. Stage only files intentionally changed for the next task; inspect status before every write/commit.

## Recommended next sequence

1. Re-read this handover plus the second-freeze summary and design-proposal sections on split, projections, leakage, sealing, and review. Confirm `git status --short` and preserve the dirty tree.
2. Implement a standalone blueprint schema, renderer, and staging/sealing pipeline. It should produce exactly 135 families × 3 histories × 4 pair opportunities; assign whole families once using the frozen config; keep evaluator-only gold out of system projections; and write separate development/holdout JSONL plus a manifest that hashes source code/dependencies, schemas, config, family registry, rendered content, review/adjudication artifacts, and outputs. Stage to a new path; refuse overwrite.
3. Author genuinely distinct scenario families. Do **not** scale, clone, or relabel the pilot’s ten v0.7 narrative templates. Use synthetic/sanitized engineering cases and include hostile cases, simpler-baseline-favouring cases, realistic ambiguity, deletion, expiry, unauthorized text, and the full disposition/effect/action matrix.
4. Check family-level stratification and coverage feasibility before freezing the assignment. Generate to a staging directory only; validate all hashes, projections, family counts, per-partition coverage, content binding, IDs, duplicate flags, and checkpoint deltas.
5. Conduct blind independent review of all 405 histories and 1,620 pair opportunities; reviewers see no model predictions (none should exist). Review flagged near-duplicate family pairs and record the hashed adjudication artifact. Correct findings, regenerate hashes, and repeat structural checks.
6. Only after all review findings are closed, pin the registry hash and seal a new immutable corpus version with development/holdout hashes, dataset card, class/feature summaries, access/review record, and the prescribed experiment evidence. Do not make model-visible projections available before the authorized G3 stage.
7. Complete G3 evidence: validate/freeze the corpus, verify fair baseline contracts/smokes with no learned predictions, capture exact commands/runtime/commit/dependency hashes, and record the gate decision. G3 remains `NOT_EVALUATED` until its complete criteria are met.
8. Stop before any model prediction, training, threshold tuning, holdout scoring, or G4 evaluation. Those need G3 PASS and separate G4 run authorization.

## Agent model recommendation

Use **GPT-6 Astra with high reasoning** as the primary agent for the blueprint-format/renderer/staging pipeline and cross-document decisions. This is high-stakes, multi-file evaluation work with leakage and authorization constraints; the stronger model is justified for the lead role. To control token cost, keep one primary lead and use **GPT-5.6 Sol** for bounded independent reviews (fixed batches of authored histories, schema/test audit, or manifest verification), not duplicate full-context implementation. Keep reviewers blind to model predictions; the prediction set should remain nonexistent until separately authorized.

## Handover bottom line

The plan is approved and the engineering validator foundation is peer-reviewed PASS. The next agent should build the missing authoring/rendering/staging pipeline and then produce genuinely novel, reviewable content under the approved limits. There is no need to ask the owner to re-approve the second-freeze plan or agent-review substitution. Do not imply that corpus generation, corpus review, G3, or G4 has passed.
