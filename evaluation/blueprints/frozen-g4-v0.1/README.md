# Frozen G4 blueprint authoring workspace

This directory contains development inputs for the proposed frozen G4 corpus. Nothing here is a holdout, reviewed corpus, sealed artifact, or model input.

`authoring-matrix.json` is a canonical planning artifact with 135 family slots. Its `AUTHORING_PLAN_NOT_CORPUS` status is intentional. It predeclares domain, primary relationship, required feature, disposition/effect/action coverage, and expected baseline affinity before substantive histories are written.

`initial-authoring-batch.md` defines the first six family briefs. Each brief covers one primary semantic relationship and records the intended evidence boundary before event wording, candidate snapshots, checkpoints, and task gold are authored.

Authoring rules:

- Write three independently worded histories and four pair opportunities per family.
- Do not copy or relabel the v0.7 pilot narratives.
- Keep relationship, authority/disposition, state effect, and external action independent.
- Include a pre-event checkpoint and a checkpoint at every pair event.
- Derive the family specification from rendered content; do not hand-edit its hashes.
- Keep every record `pending` until blind review has approved its exact substantive hash.
- Do not run models, generate predictions, or expose a final holdout during authoring.

The staging command will accept only a complete 135-family registry and will reject structural, semantic, coverage, split, identifier, hash, and duplicate failures.
