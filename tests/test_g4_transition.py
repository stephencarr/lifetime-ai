from copy import deepcopy
from dataclasses import replace

from lifetime_ai.evaluation.g4_transition import (
    G4TransitionProposal,
    preflight_g4_transition,
    prepare_g4_transition,
    witness_g4_transition,
)
from lifetime_ai.evaluation.canonical import sha256_value


def _fixtures():
    event = {
        "event_id": "event-2", "sequence": 2, "event_type": "message",
        "content": "The preference still stands", "occurred_at": "2026-09-22T10:00:00Z",
        "source_status": "present",
        "authority": {"may_assert_user_state": True, "may_request_transition": True},
    }
    pair = {
        "track": "pair_classification", "history_id": "history-1",
        "event": {key: event[key] for key in (
            "event_id", "event_type", "content", "occurred_at", "source_status")},
        "candidate_snapshot": {
            "snapshot_id": "snapshot-1", "item_id": "item-1",
            "captured_after_sequence": 1, "source_event_ids": ["event-1"],
            "counterevidence_event_ids": [],
            "canonical_payload": {
                "kind": "preference", "proposition": "The preference still stands",
                "scope": {}, "status": "active", "epistemic_basis": "asserted",
                "sensitivity": "normal", "valid_from": "2026-09-22T09:00:00Z",
                "valid_until": None,
            },
        },
    }
    pair["candidate_snapshot"]["sha256"] = sha256_value(
        pair["candidate_snapshot"]["canonical_payload"]
    )
    history = {
        "history_id": "history-1", "timeline": [
            {**event, "event_id": "event-1", "sequence": 1}, event,
        ],
    }
    proposal = G4TransitionProposal(
        "event-2", "snapshot-1", "supports", "reinforce", ("item-1",),
        evidence_event_ids=("event-1", "event-2"),
    )
    return proposal, pair, history


def test_authorized_reinforcement_passes_preflight_without_mutation():
    proposal, pair, history = _fixtures()
    before = deepcopy(history)
    assert preflight_g4_transition(proposal, pair, history).passed
    assert history == before


def test_authority_is_checked_outside_semantic_pair_projection():
    proposal, pair, history = _fixtures()
    history["timeline"][-1]["authority"]["may_assert_user_state"] = False
    result = preflight_g4_transition(proposal, pair, history)
    assert not result.passed and "cannot assert" in result.reason
    history["timeline"][-1]["authority"]["may_assert_user_state"] = True
    history["timeline"][-1]["authority"]["may_request_transition"] = False
    result = preflight_g4_transition(proposal, pair, history)
    assert not result.passed and "cannot request" in result.reason


def test_effect_not_inferred_from_supports():
    proposal, pair, history = _fixtures()
    resolve = G4TransitionProposal(
        proposal.event_id, proposal.candidate_snapshot_id, "supports", "resolve",
        proposal.affected_item_ids, evidence_event_ids=proposal.evidence_event_ids,
    )
    assert not preflight_g4_transition(resolve, pair, history).passed


def test_rejects_identity_future_evidence_and_deleted_source():
    proposal, pair, history = _fixtures()
    pair["candidate_snapshot"]["snapshot_id"] = "other"
    assert not preflight_g4_transition(proposal, pair, history).passed
    pair["candidate_snapshot"]["snapshot_id"] = "snapshot-1"
    history["timeline"].append({**history["timeline"][-1], "event_id": "event-3", "sequence": 3})
    assert not preflight_g4_transition(proposal, pair, history).passed
    history["timeline"].pop()
    history["timeline"][-1]["source_status"] = "deleted"
    assert not preflight_g4_transition(proposal, pair, history).passed


def test_noop_cannot_hide_lifecycle_effect_or_state_change():
    proposal, pair, history = _fixtures()
    noop = G4TransitionProposal("event-2", "snapshot-1", "unrelated", "none", (),
                                evidence_event_ids=("event-2",))
    assert preflight_g4_transition(noop, pair, history).passed
    invalid = G4TransitionProposal("event-2", "snapshot-1", "unrelated", "none", ("item-1",),
                                   evidence_event_ids=("event-2",))
    assert not preflight_g4_transition(invalid, pair, history).passed
    history["timeline"][-1]["event_type"] = "deletion"
    pair["event"]["event_type"] = "deletion"
    assert not preflight_g4_transition(noop, pair, history).passed
    reinforce, _, _ = _fixtures()
    assert not preflight_g4_transition(reinforce, pair, history).passed


def test_candidate_must_preexist_event_with_present_sources():
    proposal, pair, history = _fixtures()
    pair["candidate_snapshot"]["captured_after_sequence"] = 3
    assert not preflight_g4_transition(proposal, pair, history).passed
    pair["candidate_snapshot"]["captured_after_sequence"] = 1
    pair["candidate_snapshot"]["source_event_ids"] = ["event-2"]
    assert not preflight_g4_transition(proposal, pair, history).passed
    pair["candidate_snapshot"]["source_event_ids"] = ["event-1"]
    history["timeline"][0]["source_status"] = "redacted"
    assert not preflight_g4_transition(proposal, pair, history).passed


def test_reinforcement_cannot_drop_candidate_source_provenance():
    proposal, pair, history = _fixtures()
    missing_source = G4TransitionProposal(
        proposal.event_id, proposal.candidate_snapshot_id, proposal.relationship,
        proposal.effect, proposal.affected_item_ids,
        evidence_event_ids=(proposal.event_id,),
    )
    result = preflight_g4_transition(missing_source, pair, history)
    assert not result.passed and "drops candidate provenance" in result.reason


def test_prepare_reinforcement_preserves_payload_and_sources_without_write():
    proposal, pair, history = _fixtures()
    before = deepcopy(pair)
    prepared = prepare_g4_transition(proposal, pair, history)
    assert prepared.prepared and not prepared.write_authorized
    assert prepared.candidate_after is not None
    assert prepared.candidate_after["canonical_payload"] == before["candidate_snapshot"]["canonical_payload"]
    assert prepared.candidate_after["sha256"] == before["candidate_snapshot"]["sha256"]
    assert prepared.candidate_after["source_event_ids"] == ["event-1", "event-2"]
    assert prepared.candidate_after["counterevidence_event_ids"] == []
    assert prepared.candidate_after["captured_after_sequence"] == 2
    assert pair == before


def test_prepare_noop_makes_no_state_candidate_and_rejects_tampered_hash():
    _, pair, history = _fixtures()
    noop = G4TransitionProposal("event-2", "snapshot-1", "unrelated", "none", (),
                                evidence_event_ids=("event-2",))
    result = prepare_g4_transition(noop, pair, history)
    assert result.prepared and result.candidate_after is None
    pair["candidate_snapshot"]["canonical_payload"]["proposition"] = "tampered"
    result = prepare_g4_transition(noop, pair, history)
    assert not result.prepared and "hash mismatch" in result.reason


def test_preflight_fails_closed_on_noncanonical_payload():
    proposal, pair, history = _fixtures()
    pair["candidate_snapshot"]["canonical_payload"]["scope"]["weight"] = 0.5
    result = preflight_g4_transition(proposal, pair, history)
    assert not result.passed and "cannot be canonicalized" in result.reason


def _scoped_proposal(pair, history):
    pair["event"]["content"] = "For the mobile segment, the preference still stands"
    history["timeline"][-1]["content"] = pair["event"]["content"]
    payload = deepcopy(pair["candidate_snapshot"]["canonical_payload"])
    payload["scope"] = {"segment": "mobile"}
    payload["proposition"] = pair["event"]["content"]
    payload["valid_from"] = pair["event"]["occurred_at"]
    return G4TransitionProposal(
        "event-2", "snapshot-1", "narrows_scope", "add_scoped_item",
        ("item-1",), new_item_ids=("item-2",),
        evidence_event_ids=("event-1", "event-2"), new_item_payload=payload,
    )


def test_prepare_scoped_item_is_read_only_and_source_linked():
    _, pair, history = _fixtures()
    proposal = _scoped_proposal(pair, history)
    before = deepcopy(pair)
    result = prepare_g4_transition(proposal, pair, history)
    assert result.prepared and not result.write_authorized
    assert result.candidate_after is None and len(result.new_items) == 1
    item = result.new_items[0]
    assert item["item_id"] == "item-2"
    assert item["canonical_payload"]["scope"] == {"segment": "mobile"}
    assert item["source_event_ids"] == ["event-1", "event-2"]
    assert item["sha256"] == sha256_value(item["canonical_payload"])
    assert pair == before


def test_scoped_item_rejects_missing_scope_or_fabricated_content():
    _, pair, history = _fixtures()
    proposal = _scoped_proposal(pair, history)
    same_scope = deepcopy(dict(proposal.new_item_payload))
    same_scope["scope"] = {}
    result = preflight_g4_transition(replace(proposal, new_item_payload=same_scope), pair, history)
    assert not result.passed and "strict refinement" in result.reason
    fabricated = deepcopy(dict(proposal.new_item_payload))
    fabricated["proposition"] = "invented claim"
    result = preflight_g4_transition(replace(proposal, new_item_payload=fabricated), pair, history)
    assert not result.passed and "verbatim source" in result.reason
    missing_id = replace(proposal, new_item_ids=())
    assert not preflight_g4_transition(missing_id, pair, history).passed


def test_scoped_item_rejects_unauthorized_source_and_sensitivity_downgrade():
    _, pair, history = _fixtures()
    proposal = _scoped_proposal(pair, history)
    history["timeline"][-1]["authority"]["may_request_transition"] = False
    assert not preflight_g4_transition(proposal, pair, history).passed
    history["timeline"][-1]["authority"]["may_request_transition"] = True
    pair["candidate_snapshot"]["canonical_payload"]["sensitivity"] = "sensitive"
    pair["candidate_snapshot"]["sha256"] = sha256_value(
        pair["candidate_snapshot"]["canonical_payload"]
    )
    assert not preflight_g4_transition(proposal, pair, history).passed


def test_scoped_item_rejects_scope_not_stated_in_source():
    _, pair, history = _fixtures()
    proposal = _scoped_proposal(pair, history)
    invented = deepcopy(dict(proposal.new_item_payload))
    invented["scope"] = {"segment": "desktop"}
    result = preflight_g4_transition(replace(proposal, new_item_payload=invented), pair, history)
    assert not result.passed and "lexically grounded" in result.reason
    invented["scope"] = {"device": "mobile"}
    result = preflight_g4_transition(replace(proposal, new_item_payload=invented), pair, history)
    assert not result.passed and "lexically grounded" in result.reason


def test_reinforcement_witness_requires_exact_positive_confirmation():
    proposal, pair, history = _fixtures()
    prior = pair["candidate_snapshot"]["canonical_payload"]["proposition"]
    content = (
        "The approved configuration audit independently confirms the existing entry: "
        + prior + " No route, scope or version change has been authorized for this period."
    )
    pair["event"]["content"] = content
    history["timeline"][-1]["content"] = content
    assert witness_g4_transition(proposal, pair, history).passed
    misleading = content.replace("independently confirms", "does not independently confirm")
    pair["event"]["content"] = misleading
    history["timeline"][-1]["content"] = misleading
    assert preflight_g4_transition(proposal, pair, history).passed
    assert not witness_g4_transition(proposal, pair, history).passed


def test_scoped_witness_requires_different_setting_and_general_rule():
    _, pair, history = _fixtures()
    prior = pair["candidate_snapshot"]["canonical_payload"]
    prior["proposition"] = "For Widget 1, the primary configuration currently records setting 18."
    prior["scope"] = {"product": "Widget 1", "workflow": "primary"}
    pair["candidate_snapshot"]["sha256"] = sha256_value(prior)
    content = (
        "The approved configuration audit clarifies the earlier general setting 18 entry: "
        "the child workflow 'mobile requests' for Widget 1 primary configuration instead uses "
        "setting 17. The earlier entry applies to all other workflows; "
        "the exception ends when its stated condition ends."
    )
    pair["event"]["content"] = content
    history["timeline"][-1]["content"] = content
    payload = deepcopy(prior)
    payload["scope"] = {**prior["scope"], "condition": "mobile requests"}
    payload["proposition"] = content
    payload["valid_from"] = pair["event"]["occurred_at"]
    proposal = G4TransitionProposal(
        "event-2", "snapshot-1", "narrows_scope", "add_scoped_item", ("item-1",),
        new_item_ids=("item-2",), evidence_event_ids=("event-1", "event-2"),
        new_item_payload=payload,
    )
    assert witness_g4_transition(proposal, pair, history).passed
    same_setting = content.replace("instead uses setting 17", "instead uses setting 18")
    pair["event"]["content"] = same_setting
    history["timeline"][-1]["content"] = same_setting
    payload["proposition"] = same_setting
    assert preflight_g4_transition(proposal, pair, history).passed
    assert not witness_g4_transition(proposal, pair, history).passed
    no_general_rule = content.replace("applies to all other workflows", "no longer applies")
    pair["event"]["content"] = no_general_rule
    history["timeline"][-1]["content"] = no_general_rule
    payload["proposition"] = no_general_rule
    assert preflight_g4_transition(proposal, pair, history).passed
    assert not witness_g4_transition(proposal, pair, history).passed


def test_replacement_witness_and_preparation_close_parent_without_write():
    _, pair, history = _fixtures()
    prior = pair["candidate_snapshot"]["canonical_payload"]
    prior["proposition"] = "For Widget 1, the primary configuration currently records setting 18."
    prior["scope"] = {"product": "Widget 1", "workflow": "primary"}
    pair["candidate_snapshot"]["sha256"] = sha256_value(prior)
    pair["event"]["occurred_at"] = "2026-09-22T12:00:00Z"
    history["timeline"][-1]["occurred_at"] = pair["event"]["occurred_at"]
    content = (
        "The approved configuration audit authorizes Widget 1 primary configuration "
        "to replace setting 18 with setting 19 effective 2026-09-22T12:00:00Z. "
        "The earlier configuration remains the historical record before noon; "
        "this event records activation at noon."
    )
    pair["event"]["content"] = content
    history["timeline"][-1]["content"] = content
    new_payload = deepcopy(prior)
    new_payload["proposition"] = "Widget 1 primary configuration use setting 19."
    new_payload["valid_from"] = pair["event"]["occurred_at"]
    proposal = G4TransitionProposal(
        "event-2", "snapshot-1", "supersedes", "close_and_replace", ("item-1",),
        new_item_ids=("item-2",), evidence_event_ids=("event-1", "event-2"),
        new_item_payload=new_payload,
    )
    before = deepcopy(pair)
    assert preflight_g4_transition(proposal, pair, history).passed
    assert witness_g4_transition(proposal, pair, history).passed
    prepared = prepare_g4_transition(proposal, pair, history)
    assert prepared.prepared and not prepared.write_authorized
    assert prepared.candidate_after["canonical_payload"]["status"] == "expired"
    assert prepared.candidate_after["canonical_payload"]["valid_until"] == pair["event"]["occurred_at"]
    assert prepared.candidate_after["source_event_ids"] == ["event-1", "event-2"]
    assert len(prepared.new_items) == 1
    assert prepared.new_items[0]["canonical_payload"] == new_payload
    assert prepared.new_items[0]["source_event_ids"] == ["event-1", "event-2"]
    assert pair == before
    wrong_old = content.replace("replace setting 18", "replace setting 17")
    pair["event"]["content"] = wrong_old
    history["timeline"][-1]["content"] = wrong_old
    assert preflight_g4_transition(proposal, pair, history).passed
    assert not witness_g4_transition(proposal, pair, history).passed
