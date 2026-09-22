"""Fail-closed, read-only preflight for explicit G4 transition proposals.

This does not infer an effect from a semantic label, construct state, or commit
a mutation. Passing preflight is necessary but not sufficient for autonomy.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from .canonical import CanonicalizationError, sha256_value


_SNAPSHOT_SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "evaluation/schema/candidate-snapshot.schema.json")
    .read_text(encoding="utf-8")
)
_PAYLOAD_VALIDATOR = Draft202012Validator(_SNAPSHOT_SCHEMA["properties"]["canonical_payload"])
_SNAPSHOT_VALIDATOR = Draft202012Validator(_SNAPSHOT_SCHEMA)
_SENSITIVITY_RANK = {"normal": 0, "sensitive": 1, "highly_sensitive": 2}
_SIGNED_SOURCE = (
    "The owner-signed release log",
    "The responsible maintainer's signed note",
    "The approved configuration audit",
)


@dataclass(frozen=True)
class G4TransitionProposal:
    event_id: str
    candidate_snapshot_id: str
    relationship: str
    effect: str
    affected_item_ids: tuple[str, ...]
    new_item_ids: tuple[str, ...] = ()
    evidence_event_ids: tuple[str, ...] = ()
    new_item_payload: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class G4PreflightResult:
    passed: bool
    reason: str


@dataclass(frozen=True)
class G4PreparedTransition:
    prepared: bool
    reason: str
    candidate_after: dict[str, Any] | None = None
    new_items: tuple[dict[str, Any], ...] = ()
    write_authorized: bool = False


def _reject(reason: str) -> G4PreflightResult:
    return G4PreflightResult(False, reason)


def _instant(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def preflight_g4_transition(
    proposal: G4TransitionProposal,
    pair_projection: Mapping[str, Any],
    history_projection: Mapping[str, Any],
) -> G4PreflightResult:
    """Check proposal identity, visible authority, and conservative effect shape.

    Both projections must be system-visible and cut off at the proposed event.
    No evaluator fields are read. A passing result does not authorize a write:
    effect semantics and the resulting canonical state still need validation.
    """
    if pair_projection.get("track") != "pair_classification":
        return _reject("not a pair classification projection")
    pair_event = pair_projection.get("event")
    snapshot = pair_projection.get("candidate_snapshot")
    timeline = history_projection.get("timeline")
    if not isinstance(pair_event, Mapping) or not isinstance(snapshot, Mapping):
        return _reject("missing pair event or candidate snapshot")
    if not isinstance(timeline, list) or not timeline:
        return _reject("missing visible history timeline")
    if proposal.event_id != pair_event.get("event_id"):
        return _reject("event identity mismatch")
    if proposal.candidate_snapshot_id != snapshot.get("snapshot_id"):
        return _reject("candidate identity mismatch")
    if pair_projection.get("history_id") != history_projection.get("history_id"):
        return _reject("history identity mismatch")
    events = {event.get("event_id"): event for event in timeline if isinstance(event, Mapping)}
    event = events.get(proposal.event_id)
    if event is None or len(events) != len(timeline):
        return _reject("event absent or history IDs duplicated")
    if event.get("sequence") != max(item.get("sequence", -1) for item in timeline):
        return _reject("history projection extends beyond proposed event")
    for field in ("event_id", "event_type", "content", "occurred_at", "source_status"):
        if event.get(field) != pair_event.get(field):
            return _reject("pair and history event mismatch")
    if event.get("source_status") != "present":
        return _reject("source event unavailable")
    if snapshot.get("tombstoned") or snapshot.get("source_status") in {"deleted", "redacted"}:
        return _reject("candidate source unavailable")
    if not _SNAPSHOT_VALIDATOR.is_valid(snapshot):
        return _reject("candidate snapshot fails schema")
    payload = snapshot.get("canonical_payload")
    if not isinstance(payload, Mapping) or payload.get("status") != "active":
        return _reject("candidate is not active")
    if not _PAYLOAD_VALIDATOR.is_valid(payload):
        return _reject("candidate payload fails schema")
    try:
        payload_sha256 = sha256_value(dict(payload))
    except CanonicalizationError:
        return _reject("candidate payload cannot be canonicalized")
    if snapshot.get("sha256") != payload_sha256:
        return _reject("candidate payload hash mismatch")
    item_id = snapshot.get("item_id")
    if not isinstance(item_id, str) or not item_id:
        return _reject("candidate item missing")
    captured_after = snapshot.get("captured_after_sequence")
    if type(captured_after) is not int or captured_after >= event["sequence"]:
        return _reject("candidate snapshot must predate proposed event")
    source_ids = snapshot.get("source_event_ids")
    if (not isinstance(source_ids, list) or not source_ids
            or not all(isinstance(identity, str) for identity in source_ids)
            or not set(source_ids) <= set(events)):
        return _reject("candidate sources absent from visible history")
    if not all(isinstance(identity, str) and identity for identity in (
        *proposal.affected_item_ids, *proposal.new_item_ids, *proposal.evidence_event_ids,
    )):
        return _reject("proposal identifiers must be strings")
    if len(set(source_ids)) != len(source_ids):
        return _reject("duplicate candidate source")
    if any(events[identity].get("sequence", captured_after + 1) > captured_after
           for identity in source_ids):
        return _reject("candidate cites evidence after its snapshot")
    if any(events[identity].get("source_status") != "present" for identity in source_ids):
        return _reject("candidate source unavailable")
    if len(set(proposal.affected_item_ids)) != len(proposal.affected_item_ids):
        return _reject("duplicate affected item")
    if len(set(proposal.new_item_ids)) != len(proposal.new_item_ids):
        return _reject("duplicate new item")
    if set(proposal.affected_item_ids) & set(proposal.new_item_ids):
        return _reject("affected and new items overlap")
    if len(set(proposal.evidence_event_ids)) != len(proposal.evidence_event_ids):
        return _reject("duplicate evidence event")
    if not proposal.evidence_event_ids or proposal.event_id not in proposal.evidence_event_ids:
        return _reject("proposal lacks current-event evidence")
    if not set(proposal.evidence_event_ids) <= set(events):
        return _reject("evidence event outside visible history")
    if any(events[identity].get("source_status") != "present"
           for identity in proposal.evidence_event_ids):
        return _reject("evidence source unavailable")
    if event.get("event_type") in {"deletion", "redaction", "time_advance"}:
        return _reject("lifecycle event needs separate validation")

    # Relationship and effect are deliberately independent inputs. Only the
    # limited shapes below can pass this preliminary structural check; all
    # write authorization, replacement, resolution, and lifecycle work escalates.
    if proposal.relationship == "unrelated" and proposal.effect == "none":
        if proposal.affected_item_ids or proposal.new_item_ids or proposal.new_item_payload is not None:
            return _reject("no-op proposal includes state changes")
        return G4PreflightResult(True, "read-only no-op preflight")
    if proposal.relationship == "supports" and proposal.effect == "reinforce":
        if (proposal.affected_item_ids != (item_id,) or proposal.new_item_ids
                or proposal.new_item_payload is not None):
            return _reject("reinforcement target mismatch")
        if not set(source_ids) <= set(proposal.evidence_event_ids):
            return _reject("reinforcement drops candidate provenance")
        authority = event.get("authority")
        if not isinstance(authority, Mapping) or authority.get("may_assert_user_state") is not True:
            return _reject("source cannot assert user state")
        if authority.get("may_request_transition") is not True:
            return _reject("source cannot request transition")
        return G4PreflightResult(True, "reinforcement preflight only")
    if proposal.relationship == "narrows_scope" and proposal.effect == "add_scoped_item":
        if proposal.affected_item_ids != (item_id,) or len(proposal.new_item_ids) != 1:
            return _reject("scoped-item target or new-item count mismatch")
        if not set(source_ids) <= set(proposal.evidence_event_ids):
            return _reject("scoped item drops candidate provenance")
        authority = event.get("authority")
        if (not isinstance(authority, Mapping)
                or authority.get("may_assert_user_state") is not True
                or authority.get("may_request_transition") is not True):
            return _reject("source cannot create scoped state")
        new_payload = proposal.new_item_payload
        if not isinstance(new_payload, Mapping):
            return _reject("scoped item needs explicit canonical payload")
        if not _PAYLOAD_VALIDATOR.is_valid(new_payload):
            return _reject("scoped item payload fails schema")
        try:
            sha256_value(dict(new_payload))
        except CanonicalizationError:
            return _reject("scoped item payload cannot be canonicalized")
        prior_scope = payload.get("scope")
        next_scope = new_payload.get("scope")
        if (not isinstance(prior_scope, Mapping) or not isinstance(next_scope, Mapping)
                or len(next_scope) <= len(prior_scope)
                or any(next_scope.get(key) != value for key, value in prior_scope.items())):
            return _reject("new scope is not a strict refinement")
        source_text = event.get("content")
        if not isinstance(source_text, str):
            return _reject("scoped item source text unavailable")
        for key in next_scope.keys() - prior_scope.keys():
            value = next_scope[key]
            if (not isinstance(key, str) or not isinstance(value, str)
                    or not key.strip() or not value.strip()
                    or any(re.search(r"(?<!\w)" + re.escape(term.casefold()) + r"(?!\w)",
                                     source_text.casefold()) is None
                           for term in (key, value))):
                return _reject("new scope is not lexically grounded in source")
        if new_payload["kind"] != payload.get("kind") or new_payload["status"] != "active":
            return _reject("scoped item changes kind or starts inactive")
        if _SENSITIVITY_RANK[new_payload["sensitivity"]] < _SENSITIVITY_RANK[payload["sensitivity"]]:
            return _reject("scoped item downgrades sensitivity")
        if new_payload["epistemic_basis"] != "asserted":
            return _reject("scoped item must be source asserted")
        if (new_payload["proposition"] != event.get("content")
                or not new_payload["proposition"].strip()):
            return _reject("scoped item proposition lacks verbatim source")
        if (new_payload.get("valid_from") != event.get("occurred_at")
                or new_payload.get("valid_until") != payload.get("valid_until")):
            return _reject("scoped item validity differs from safe source interval")
        return G4PreflightResult(True, "scoped-item preflight only")
    if proposal.relationship == "supersedes" and proposal.effect == "close_and_replace":
        if proposal.affected_item_ids != (item_id,) or len(proposal.new_item_ids) != 1:
            return _reject("replacement target or new-item count mismatch")
        if not set(source_ids) <= set(proposal.evidence_event_ids):
            return _reject("replacement drops candidate provenance")
        authority = event.get("authority")
        if (not isinstance(authority, Mapping)
                or authority.get("may_assert_user_state") is not True
                or authority.get("may_request_transition") is not True):
            return _reject("source cannot replace state")
        new_payload = proposal.new_item_payload
        if not isinstance(new_payload, Mapping) or not _PAYLOAD_VALIDATOR.is_valid(new_payload):
            return _reject("replacement needs schema-valid new payload")
        try:
            sha256_value(dict(new_payload))
        except CanonicalizationError:
            return _reject("replacement payload cannot be canonicalized")
        if (new_payload["scope"] != payload["scope"]
                or new_payload["kind"] != payload["kind"]
                or new_payload["status"] != "active"
                or new_payload["epistemic_basis"] != "asserted"
                or _SENSITIVITY_RANK[new_payload["sensitivity"]]
                   < _SENSITIVITY_RANK[payload["sensitivity"]]):
            return _reject("replacement changes scope, kind, status, basis, or sensitivity")
        effective = new_payload.get("valid_from")
        effective_at = _instant(effective)
        prior_from = _instant(payload.get("valid_from"))
        prior_until = _instant(payload.get("valid_until"))
        if (effective != event.get("occurred_at")
                or new_payload.get("valid_until") != payload.get("valid_until")
                or effective_at is None
                or (payload.get("valid_from") is not None and prior_from is None)
                or (payload.get("valid_until") is not None and prior_until is None)
                or (prior_from is not None and effective_at <= prior_from)
                or (prior_until is not None and effective_at >= prior_until)):
            return _reject("replacement validity interval is unsafe")
        if not isinstance(new_payload["proposition"], str) or not new_payload["proposition"].strip():
            return _reject("replacement proposition missing")
        return G4PreflightResult(True, "replacement preflight only")
    return _reject("effect requires separate validator or escalation")


def witness_g4_transition(
    proposal: G4TransitionProposal,
    pair_projection: Mapping[str, Any],
    history_projection: Mapping[str, Any],
) -> G4PreflightResult:
    """Check a narrow, source-verbatim development grammar after preflight.

    This positive textual witness is not general semantic entailment, and even
    a passing witness has no write authority. Unsupported phrasing escalates.
    """
    preflight = preflight_g4_transition(proposal, pair_projection, history_projection)
    if not preflight.passed:
        return preflight
    if proposal.effect == "none":
        return _reject("no-op lacks positive source witness")
    event_text = pair_projection["event"]["content"]
    prior_payload = pair_projection["candidate_snapshot"]["canonical_payload"]
    prior_text = prior_payload["proposition"]
    if (not isinstance(event_text, str) or not isinstance(prior_text, str)
            or not prior_text.strip()):
        return _reject("source witness text unavailable")
    if proposal.effect == "reinforce":
        expected = (
            " independently confirms the existing entry: " + prior_text
            + " No route, scope or version change has been authorized for this period."
        )
        if any(event_text == prefix + expected for prefix in _SIGNED_SOURCE):
            return G4PreflightResult(True, "verbatim reinforcement witness only")
        return _reject("reinforcement lacks verbatim confirmation witness")
    if proposal.effect == "add_scoped_item":
        prior_scope = prior_payload["scope"]
        new_scope = proposal.new_item_payload["scope"]
        if (set(prior_scope) != {"product", "workflow"}
                or set(new_scope) != {"product", "workflow", "condition"}):
            return _reject("scoped witness requires product, workflow, condition")
        product = prior_scope["product"]
        workflow = prior_scope["workflow"]
        condition = new_scope["condition"]
        if not all(isinstance(value, str) and value for value in (product, workflow, condition)):
            return _reject("scoped witness fields unavailable")
        old_match = re.fullmatch(
            rf"For {re.escape(product)}, the {re.escape(workflow)} configuration "
            r"currently records setting ([0-9]+).+",
            prior_text,
        )
        if old_match is None:
            return _reject("prior setting lacks source witness")
        old_setting = old_match.group(1)
        for prefix in _SIGNED_SOURCE:
            opening = (
                f"{prefix} clarifies the earlier general setting {old_setting} entry: "
                f"the child workflow '{condition}' for {product} {workflow} "
                "configuration instead uses setting "
            )
            ending = (
                ". The earlier entry applies to all other workflows; "
                "the exception ends when its stated condition ends."
            )
            if event_text.startswith(opening) and event_text.endswith(ending):
                new_setting = event_text[len(opening):-len(ending)]
                if (new_setting.isascii() and new_setting.isdigit()
                        and (new_setting.lstrip("0") or "0") != (old_setting.lstrip("0") or "0")):
                    return G4PreflightResult(True, "verbatim scoped-change witness only")
        return _reject("scoped change lacks old/new setting witness")
    if proposal.effect == "close_and_replace":
        prior_scope = prior_payload["scope"]
        if set(prior_scope) != {"product", "workflow"}:
            return _reject("replacement witness requires product and workflow")
        product, workflow = prior_scope["product"], prior_scope["workflow"]
        if not all(isinstance(value, str) and value for value in (product, workflow)):
            return _reject("replacement witness identity unavailable")
        old_match = re.fullmatch(
            rf"For {re.escape(product)}, the {re.escape(workflow)} configuration "
            r"currently records setting ([0-9]+).+",
            prior_text,
        )
        if old_match is None:
            return _reject("replacement prior setting lacks source witness")
        old_setting = old_match.group(1)
        new_proposition = proposal.new_item_payload["proposition"]
        new_match = re.fullmatch(
            rf"{re.escape(product)} {re.escape(workflow)} configuration use setting ([0-9]+)\.",
            new_proposition,
        )
        if new_match is None:
            return _reject("replacement new proposition lacks source witness")
        new_setting = new_match.group(1)
        if (new_setting.lstrip("0") or "0") == (old_setting.lstrip("0") or "0"):
            return _reject("replacement does not change setting")
        effective = proposal.new_item_payload["valid_from"]
        suffix = (
            " The earlier configuration remains the historical record before noon; "
            "this event records activation at noon."
        )
        if any(event_text == (
            f"{prefix} authorizes {product} {workflow} configuration to replace "
            f"setting {old_setting} with setting {new_setting} effective {effective}." + suffix
        ) for prefix in _SIGNED_SOURCE):
            return G4PreflightResult(True, "verbatim replacement witness only")
        return _reject("replacement lacks explicit activation witness")
    return _reject("effect has no positive source witness")


def prepare_g4_transition(
    proposal: G4TransitionProposal,
    pair_projection: Mapping[str, Any],
    history_projection: Mapping[str, Any],
) -> G4PreparedTransition:
    """Materialize supported candidates without write authority.

    This prepares state for inspection only. It cannot validate the semantic
    correctness of the predicted relationship/effect and never commits state.
    """
    preflight = preflight_g4_transition(proposal, pair_projection, history_projection)
    if not preflight.passed:
        return G4PreparedTransition(False, preflight.reason)
    if proposal.effect == "none":
        return G4PreparedTransition(True, "no-op prepared")
    if proposal.effect not in {"reinforce", "add_scoped_item", "close_and_replace"}:
        return G4PreparedTransition(False, "unsupported preparation effect")

    before = pair_projection["candidate_snapshot"]
    event = pair_projection["event"]
    timeline_event = next(
        item for item in history_projection["timeline"]
        if item["event_id"] == proposal.event_id
    )
    if proposal.effect == "close_and_replace":
        effective = proposal.new_item_payload["valid_from"]
        closed = deepcopy(before)
        closed["snapshot_id"] = "g4-prepared:" + sha256_value({
            "prior_snapshot_id": before["snapshot_id"],
            "event_id": proposal.event_id,
            "effect": "close_prior",
        })[:32]
        closed["captured_after_sequence"] = timeline_event["sequence"]
        closed["canonical_payload"]["status"] = "expired"
        closed["canonical_payload"]["valid_until"] = effective
        closed["source_event_ids"] = list(dict.fromkeys(
            (*before["source_event_ids"], event["event_id"])
        ))
        closed["sha256"] = sha256_value(closed["canonical_payload"])
        new_payload = deepcopy(dict(proposal.new_item_payload))
        replacement = {
            "snapshot_id": "g4-prepared:" + sha256_value({
                "prior_snapshot_id": before["snapshot_id"],
                "event_id": proposal.event_id,
                "effect": "replacement_item",
                "new_item_id": proposal.new_item_ids[0],
            })[:32],
            "item_id": proposal.new_item_ids[0],
            "captured_after_sequence": timeline_event["sequence"],
            "canonical_payload": new_payload,
            "source_event_ids": list(dict.fromkeys(
                (*before["source_event_ids"], event["event_id"])
            )),
            "counterevidence_event_ids": deepcopy(before["counterevidence_event_ids"]),
            "sha256": sha256_value(new_payload),
        }
        if not _SNAPSHOT_VALIDATOR.is_valid(closed) or not _SNAPSHOT_VALIDATOR.is_valid(replacement):
            return G4PreparedTransition(False, "prepared replacement fails snapshot schema")
        return G4PreparedTransition(True, "replacement prepared", closed, (replacement,))
    if proposal.effect == "add_scoped_item":
        payload = deepcopy(dict(proposal.new_item_payload or {}))
        new_snapshot = {
            "snapshot_id": "g4-prepared:" + sha256_value({
                "prior_snapshot_id": before["snapshot_id"],
                "event_id": proposal.event_id,
                "effect": proposal.effect,
                "new_item_id": proposal.new_item_ids[0],
            })[:32],
            "item_id": proposal.new_item_ids[0],
            "captured_after_sequence": timeline_event["sequence"],
            "canonical_payload": payload,
            "source_event_ids": list(dict.fromkeys(
                (*before["source_event_ids"], event["event_id"])
            )),
            "counterevidence_event_ids": deepcopy(before["counterevidence_event_ids"]),
            "sha256": sha256_value(payload),
        }
        if not _SNAPSHOT_VALIDATOR.is_valid(new_snapshot):
            return G4PreparedTransition(False, "prepared scoped item fails snapshot schema")
        return G4PreparedTransition(True, "scoped item prepared", new_items=(new_snapshot,))
    after = deepcopy(before)
    after["snapshot_id"] = "g4-prepared:" + sha256_value({
        "prior_snapshot_id": before["snapshot_id"],
        "event_id": proposal.event_id,
        "effect": proposal.effect,
    })[:32]
    after["captured_after_sequence"] = timeline_event["sequence"]
    after["source_event_ids"] = list(dict.fromkeys(
        (*before["source_event_ids"], event["event_id"])
    ))
    if not _SNAPSHOT_VALIDATOR.is_valid(after):
        return G4PreparedTransition(False, "prepared reinforcement fails snapshot schema")
    return G4PreparedTransition(True, "reinforcement prepared", candidate_after=after)
