"""Readable, evaluator-free features for the G4 pair-classification track."""

from __future__ import annotations

from typing import Any, Mapping


def _content(value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else "[unavailable]"


def pair_feature_texts(projection: Mapping[str, Any]) -> tuple[str, str, str]:
    """Return event, candidate, and context text from a system-visible projection.

    Opaque identifiers, projection hashes, authority, and evaluator fields never
    enter these features. Lifecycle status remains visible where the projection
    provides it.
    """
    event = projection["event"]
    snapshot = projection["candidate_snapshot"]
    event_text = (
        f"New event type: {event['event_type']}. "
        f"New event: {_content(event.get('content'))}. "
        f"Event source status: {event.get('source_status', 'present')}."
    )
    if snapshot.get("tombstoned"):
        candidate_text = (
            "Candidate state: source content unavailable. "
            f"Source status: {snapshot.get('source_status', 'unknown')}."
        )
    else:
        payload = snapshot["canonical_payload"]
        scope = payload.get("scope", {})
        scope_text = "; ".join(f"{key}: {scope[key]}" for key in sorted(scope))
        candidate_text = (
            f"Candidate kind: {payload['kind']}. "
            f"Candidate proposition: {_content(payload.get('proposition'))}. "
            f"Candidate scope: {scope_text or '[unspecified]'}. "
            f"Candidate status: {payload['status']}. "
            f"Candidate valid until: {payload.get('valid_until') or '[open]'}."
        )
    context_text = " ".join(
        f"Earlier event {index} ({item['event_type']}): {_content(item.get('content'))}."
        for index, item in enumerate(projection.get("context_events", ()), start=1)
    )
    return event_text, candidate_text, context_text


def pair_feature_document(projection: Mapping[str, Any]) -> str:
    event, candidate, context = pair_feature_texts(projection)
    return "\n".join((event, candidate, context))
