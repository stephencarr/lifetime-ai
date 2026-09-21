# G3 development pilot v0.7

Status: independent agent review passed; human signoff waived by project owner. No human review is claimed. G3 is not complete. See `agent-review-record.md`.

This synthetic development pilot contains 30 whole-family longitudinal histories and 120 independently labelled event–candidate pairs. The deterministic pilot split contains 21 development histories and 9 pilot holdout histories. The pilot holdout tests split and sealing machinery only and becomes development material after review; it is not a final G4, G5, G6, or G7 holdout.

Each history contains four pair-linked downstream task groups with explicit target scope. Records cover all six semantic relationships, all transition dispositions, declared state effects and actions, deletion, expiry, authority rejection, ambiguity, late reports, hostile baseline cases, and independent-support survival.

All records were generated from synthetic fixtures by `scripts/generate_g3_development_pilot_v07.py`. No model predictions, proprietary data, production connections, embeddings, or final holdout data were used. Every history and pair passed independent agent review; human signoff was waived by project owner. Checkpoint gold is exhaustive over authorized assertions and captured independent state through each checkpoint. System-facing projection canary check: 0 failures across 270 projections.

The corpus uses ten declared template families with three histories each. Whole template families are assigned to one partition, so generated siblings do not cross the 21/9 split. Relationship counts are mechanically controlled for instrument coverage, not prevalence: supports 27, supersedes 13, and 20 pairs in each other class. Candidate pools combine hard same-topic negatives with independent-support and action-policy context.

Review is pair-level for all 120 pairs, with a separate history/checkpoint decision. Ambiguity, authority rejection, lifecycle effects, invalid transitions, and conflict preservation require documented second review. Any approved record is later bound to a substantive-content hash, and content changes invalidate approval.

Known limitations: prose remains synthetic, each history contains exactly four evaluated pairs, and expected-favor labels are prospective judgments with written rationales rather than experimental results. The pilot is for annotation and harness validation only.
