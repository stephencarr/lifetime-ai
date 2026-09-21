# Initial rendered batch

`initial-drafts/` is a pending draft from the six briefs in `initial-authoring-batch.md`. It contains 18 individually validated histories and 72 pair opportunities, with rationales, before/after checkpoint gold, isolated candidate snapshots and explicit downstream questions.

The renderer is `scripts/render_initial_g4_batch.py`; its original narrative source is `lifetime_ai/evaluation/initial_authoring.py`. Reproduction requires a new output directory, for example `python scripts/render_initial_g4_batch.py --output /private/tmp/initial-g4-reproduction`. Existing artifacts are never overwritten by the renderer.

All records remain pending. The provisional `development` field is required by the history schema and is not a final partition assignment. No model predictions, holdout assignment, review approval or sealing claim is produced.

The prototype identifiers expose family ordinals and must not be used as final system-facing identifiers. `remap_blueprint_identifiers` provides a reference-preserving opaque remapping and recomputes candidate-pool hashes; final authoring must use opaque identifiers and independently review the resulting content. These six files are development prototypes, not final-family-ready artifacts.

## Planning differences that require review

The initial prose briefs specify relationship boundaries but do not incorporate all supplemental episodes allocated by the broader matrix. In particular, this batch does not claim the matrix's expiry/outreach in family 001, independent-support survival in 003, additional scope narrowing in 004, contradictory evidence in 005, or derivative invalidation in 006. Only tags actually represented in the draft are emitted. Baseline affinity is neutral pending review instead of asserting the matrix's planned advantages without evidence.

Each history tracks three distinct candidate items within one release context. The first three pair opportunities exercise the family's primary relationship, and the fourth exercises its hostile boundary. Review should assess whether this clustered structure provides enough natural longitudinal variety before expanding the corpus. The three histories in a family vary evidence framing and scope, not just actor names.

Family 004's future-announcement variant records the pair at the announced activation boundary; it does not test a separate pre-activation checkpoint after the announcement. Adding that boundary test is a potential expansion item, not claimed coverage here.
