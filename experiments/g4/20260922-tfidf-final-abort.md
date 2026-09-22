# G4 TF-IDF final attempt — incomplete

**Date:** 22 September 2026  
**Frozen evaluator commit:** `92a0ce441b0e1ecd356ac04c32886500ca7e0278`  
**Authorization nonce:** `g4-poc-20260922-tfidf-01`  
**Decision:** `INCOMPLETE`; no G4 pass or fail inference from model outcomes

The first invocation failed during dependency setup, before the evaluator
started. The next invocation entered the evaluator, passed authorization and
sealed-corpus verification, read the development and holdout partitions, then
raised `ModuleNotFoundError: No module named 'sklearn'` when fitting the
TF-IDF model. The output directory contains only `.run-lock`; no prediction
or result artifact was written.

The declared evaluation dependency group was subsequently installed with
`uv sync --frozen --group evaluation`. A non-corpus import check confirmed
`scikit-learn 1.9.1`. The evaluator was not rerun: the runbook prohibits a
second holdout run under the same authorization. The v21 holdout remains
quarantined. Any new final evaluation requires a separately prepared and
authorized protocol consistent with the frozen holdout rules.

The earlier 22 September repository-search exposure remains disclosed in
`holdout-access-incident.md` in the local-encoder development experiment.
