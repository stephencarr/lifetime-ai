# Initial frozen G4 family briefs

**Status:** authoring briefs only; no histories or holdout assignments exist.

These six briefs establish one example of each primary semantic relationship. Each eventual family must contain three histories and four pair opportunities per history. The variants below alter actors, wording, irrelevant context, and timing without changing the adjudicated relationship boundary.

## g4-family-53356db3137c240a — supports

- Candidate: the mobile client currently targets API v4 for account-management requests.
- New evidence: the authorized API owner independently confirms that the same client and request scope remain on v4 during the same validity period.
- Gold boundary: compatible evidence for the same proposition and scope; no narrowing or replacement cue.
- Default transition: `supports / accept / reinforce / none`.
- Variants: direct owner confirmation; approved release checklist confirmation; signed compatibility report with unrelated release chatter.
- Hostile element: one pair should use strong lexical overlap about a different client so lexical retrieval alone produces an attractive distractor.

## g4-family-bbcc66aecae82161 — contradicts

- Candidate: telemetry records the mobile checkout client calling API v3 in the current rollout.
- New evidence: an equally authorized gateway observation records that same client and rollout calling v4, with no source precedence or change boundary.
- Gold boundary: both cannot describe the same current traffic as stated; recency alone does not establish supersession.
- Default transition: `contradicts / abstain / preserve_conflict / clarify`.
- Variants: gateway versus client telemetry; two region-level observations with overlapping scope; delayed batch telemetry whose occurrence time still overlaps.
- Hostile element: newer timestamps must not be treated as an automatic replacement rule.

## g4-family-0fedd86324f32815 — narrows_scope

- Candidate: mobile account-management requests use API v4.
- New evidence: offline password-reset requests specifically remain on v3 until the queued migration completes.
- Gold boundary: an explicit child workflow and condition make both propositions simultaneously valid.
- Default transition: `narrows_scope / accept / add_scoped_item / none`.
- Variants: offline queue exception; regulated-region exception; legacy-device exception with an explicit end condition.
- Hostile element: include a nearby incompatible statement without an explicit child scope as a distractor, ensuring the gold does not reward invented reconciliation.

## g4-family-3c6fba4203605964 — supersedes

- Candidate: release builds use compiler 18 with package-manager lock format 2.
- New evidence: the authorized build owner states an effective date after which compiler 19 and lock format 3 replace that configuration.
- Gold boundary: explicit temporal replacement closes the prior interval while preserving it historically.
- Default transition: `supersedes / accept / close_and_replace / none`.
- Variants: dated build-owner directive; merged toolchain configuration plus explicit stale marker; release-train transition with a future effective boundary.
- Hostile element: a bare incompatible developer comment must remain unauthorized or contradictory rather than become supersession.

## g4-family-4699ce28941f2318 — unrelated

- Candidate: production builds use the repository-pinned compiler and package-manager versions.
- New evidence: a build report records test duration, artifact size, or cache-hit rate without asserting anything about the pinned versions.
- Gold boundary: shared build vocabulary is not material evidence about the candidate proposition.
- Default transition: `unrelated / no_op / none / silence` when action selection is explicitly requested.
- Variants: cache statistics; artifact signing duration; documentation build warning.
- Hostile element: high lexical overlap and realistic version-like numbers that refer to unrelated measurements.

## g4-family-22a3a454992530e7 — uncertain

- Candidate: the release branch uses the compiler version pinned in its checked-in toolchain file.
- New evidence: a late note says “it was switched back for the release,” but does not identify the compiler, branch, effective interval, or referent of “it.”
- Gold boundary: relevance is plausible, but the missing referent and temporal scope prevent a unique supports/contradicts/supersedes decision.
- Default transition: `uncertain / abstain / none / clarify`.
- Variants: ambiguous pronoun; redacted version identifier; late report with occurrence and recording times spanning two release branches.
- Hostile element: the surrounding chronology should tempt a newest-wins guess while remaining genuinely underdetermined.

## Batch exit condition

The batch is ready to expand only after all 18 rendered histories validate independently, the 72 pair opportunities have written rationales, and blind reviewers agree that none of the variants depends on unstated author intent or label-specific boilerplate.
