# Supervised local UAT

This is a local UAT workbench for testing whether source-backed context survives a session and helps with retrieval. It is separate from the evaluation corpus and the core authoritative-state store. One explicit import confirmation captures high-signal candidates locally; participants do not approve each item. They can inspect, correct, or delete stored memory afterward. The deterministic adapter is a prototype baseline, not evidence of model quality.

The UI accepts a narrow JSON import format for batches of already-approved source excerpts. A sample file is provided at `fixtures/uat_synthetic_sources.json`.

It also accepts a small Gmail Takeout MBOX slice. Parsing is local, attachments are ignored, and the UI shows a preview before import. Keep the first slice bounded (for example, two weeks and no more than 200 messages) and exclude sensitive or consequential mail.

## Setup and launch

From the repository root:

```sh
uv sync --frozen
LIFETIME_AI_UAT_DB=.uat/uat_observe.sqlite3 LIFETIME_AI_UAT_PORT=8766 uv run --no-sync python scripts/run_uat.py
```

Open [http://127.0.0.1:8766](http://127.0.0.1:8766). Stop with `Ctrl-C`. To use another disposable database or port:

```sh
LIFETIME_AI_UAT_DB=/tmp/lifetime-ai-uat.sqlite3 LIFETIME_AI_UAT_PORT=8766 uv run python scripts/run_uat.py
```

The UAT uses `.uat/uat_observe.sqlite3`, ignored by Git and separate from the prior `.uat/workspace.sqlite3` dataset. The UI uses a swappable local suggestion adapter. MiniLM remains the candidate, but when weights are absent the UI reports deterministic demo mode and uses explicit local text cues with abstention. No network call or hosted model is made. The server serves the interface from `lifetime_ai/uat_web/` with no frontend build step.

## Workbench views

- **Overview:** counts for sources, suggestions, active test memory, and human findings; review outcomes and proposed type distributions. These are workspace counts, not precision or recall estimates.
- **Capture inspector:** search and filter captured candidates and outcomes. A focused inspector shows the claim, rationale, uncertainty, source date, context, and excerpt. Item-by-item review is optional; a confirmed batch import captures candidates in one step.
- **Stored memory:** search/filter active items, open their source evidence, correct or delete a test item after confirmation.
- **Sources:** search imported material, inspect one source at a time, and follow its path to a suggestion or active state.
- **Retrieval lab:** ask a question and inspect citations for each match.
- **UAT findings:** tag a source, suggestion, or stored item with a structured issue category and an optional short note. Findings persist across local restarts and can be removed. Notes are limited to 240 characters; avoid copying message text into them.
- **Import & setup:** synthetic fixtures, JSON, MBOX, one approved source, and workspace reset.

Lists show 25 rows per page. The full source excerpt appears only in the inspector when requested. A reset clears sources, suggestions, state, findings, and prior interaction events. The reset event itself remains.

## Participant test script

1. Read the safety notice. Use synthetic fixtures first; do not paste sensitive or consequential data.
2. Load the synthetic fixtures and inspect the preview: note which statements become candidates and which are omitted.
3. Confirm once. Check **Stored memory** to see the automatically captured items and open a row to inspect its source excerpt, date, and context.
4. Ask: “What did we decide about planning?” and inspect the cited source. Try a question where the memory should have abstained.
5. Correct one stored item, retrieve it again, then delete it and verify it no longer appears in active memory or retrieval.
6. Add one participant-approved, non-sensitive source with an explicit preference or decision. Confirm the single-source import and see if retrieval finds it later.
7. Reset the disposable workspace and verify that sources, suggestions, state, and findings are empty.

The import schema is:

```json
{
  "format": "lifetime-ai-uat-sources/v1",
  "sources": [
    {
      "source_id": "local:example-1",
      "title": "A source title",
      "occurred_at": "2026-09-22",
      "context": "Why this excerpt matters",
      "excerpt": "A short participant-approved source excerpt."
    }
  ]
}
```

Only those five source fields are accepted. Evaluator labels, gold answers, holdout paths, predictions, and other metadata are rejected by the importer.

The only interaction log values are `shown`, `accepted`, `edited`, `rejected`, `deferred`, `retrieved`, `corrected`, `deleted`, and `reset`; raw content is not written to the interaction log. Structured UAT findings are stored separately and include target reference, category, timestamp, and optional short human note.

## Safety boundaries and limitations

- Localhost only; no authentication, multi-user support, hosted API, external connector, or model-training path.
- MBOX import reads message headers and plain-text bodies locally; it ignores attachments and caps a batch at 200 messages. The raw MBOX is not stored by the importer.
- Every import, correction, deletion, and reset requires browser confirmation; an import confirmation authorizes local capture of the candidates shown in preview. The server checks explicit confirmation for write operations. Suggestions do not trigger actions outside the local store.
- Delete and reset are permanent in this disposable workspace; a complete undo/audit UX is not claimed.
- Retrieval is deterministic keyword matching and may miss relevant items or return weak matches. It shows source citations and an uncertainty notice.
- Demo suggestions are heuristic and must be human-reviewed. MiniLM weights are not bundled and are not required for UAT.
- The deterministic demo adapter now abstains unless it finds a narrow explicit decision, preference, or commitment cue. It extracts one matching sentence from the unquoted main message; this can still miss context, attribution, negation, or lifecycle updates. Overview counts and retrieval/correction sessions are qualitative UAT evidence, not classifier metrics. There is no A/B classifier comparison yet.
- Source excerpts are stored locally because citation review is part of the UAT. Avoid sensitive data and clear the workspace after the session.
- Evaluator labels, gold answers, holdout paths, and holdout-derived content are not loaded by the UI or passed to the adapter.
