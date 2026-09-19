from __future__ import annotations

import json
from copy import deepcopy
from decimal import Decimal

import pytest

from lifetime_ai.evaluation.canonical import (
    CanonicalizationError, canonical_bytes, canonical_jsonl_bytes,
    sha256_bytes, sha256_value, strict_json_loads,
)
from lifetime_ai.evaluation.contracts import (
    MockCandidateRetriever, MockEvaluationSystem, MockPairClassifier,
    MockGeneralLLMBaseline, MockOracleBaseline, MockRollingSummaryBaseline,
    MockSchedulerBaseline,
    PredictedRelationship, RawLifecycleUsage, calculate_cost_cad,
)
from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection, build_retrieval_projection,
    build_system_history_projection, contains_evaluator_only_material,
)
from lifetime_ai.evaluation.split import assign_disjoint_gate_holdouts, split_whole_families
from lifetime_ai.evaluation.state_matching import (
    MatchConfiguration, greedy_semantic_matches, semantic_state_score,
)
from lifetime_ai.evaluation.validation import CorpusValidationError, validate_corpus
from scripts.generate_g3_pilot import generate, write


def test_canonical_serialization_and_hashing_are_deterministic():
    value = {"z": 2, "é": "kept", "a": [True, None, "x"]}
    expected = b'{"a":[true,null,"x"],"z":2,"\xc3\xa9":"kept"}'
    assert canonical_bytes(value) == expected
    assert sha256_value(value) == sha256_bytes(expected)
    assert canonical_jsonl_bytes([value]) == expected + b"\n"


@pytest.mark.parametrize("raw", ['{"x":1,"x":2}', '{"x":1.2}', '{"x":-0}'])
def test_canonical_parser_rejects_ambiguous_json(raw):
    with pytest.raises(CanonicalizationError):
        strict_json_loads(raw)


def test_canonicalizer_rejects_binary_float():
    with pytest.raises(CanonicalizationError, match="binary floating-point"):
        canonical_bytes({"probability": 0.5})


def test_pilot_histories_validate_and_use_whole_family_splits():
    histories = generate()
    validate_corpus(histories)
    assert len(histories) == 13
    assert all(history["reviewer_status"] == "pending" for history in histories)
    family_partitions = {}
    for history in histories:
        assert family_partitions.setdefault(history["family_id"], history["partition"]) == history["partition"]
    repeated = histories + [{**histories[0], "history_id": "variant"}]
    assignments = split_whole_families(repeated, seed="test")
    assert assignments[histories[0]["family_id"]] in {"pilot_development", "pilot_holdout"}


def test_final_gate_holdouts_are_disjoint_by_family():
    families = [f"family-{index}" for index in range(100)]
    assignments = assign_disjoint_gate_holdouts(families, seed="frozen")
    assert set(assignments) == set(families)
    assert set(assignments.values()) == {"g4_holdout", "g5_holdout", "g6_holdout", "g7_holdout"}
    assert len(assignments) == len(set(assignments))


def test_evaluator_projection_and_canaries_never_reach_system_inputs():
    for history in generate():
        canaries = {history["evaluator_only"]["generation_and_review_provenance"]["canary"]}
        projections = [build_system_history_projection(history)]
        for pair in history["pair_inputs"]:
            projections.extend([
                build_retrieval_projection(history, pair["pair_id"]),
                build_pair_classification_projection(history, pair["pair_id"]),
            ])
        assert all(not contains_evaluator_only_material(projection, canaries)
                   for projection in projections)
        assert all("evaluator_only" not in json.dumps(projection) for projection in projections)


def test_deletion_uses_event_path_and_removes_content_after_sequence():
    history = next(item for item in generate() if "source_deletion" in item["feature_tags"])
    source_id = history["timeline"][0]["event_id"]
    assert any(event["event_type"] == "deletion" and source_id in event["deletion_target_ids"]
               for event in history["timeline"])
    projection = build_system_history_projection(history)
    source = next(event for event in projection["timeline"] if event["event_id"] == source_id)
    assert source["content"] is None and source["source_status"] == "deleted"
    assert history["evaluator_only"]["deleted_source_content"][source_id] not in json.dumps(projection)


def test_deletion_and_expiry_are_the_evaluated_lifecycle_events():
    histories = generate()
    deletion = next(item for item in histories if "sole_source_deletion" in item["feature_tags"])
    deletion_pair = deletion["pair_inputs"][0]
    deletion_event = next(item for item in deletion["timeline"]
                          if item["event_id"] == deletion_pair["event_id"])
    deletion_gold = deletion["evaluator_only"]["pair_gold"][0]
    assert deletion_event["event_type"] == "deletion"
    assert deletion_gold["expected_state_effect"]["effect"] == "invalidate"
    assert deletion_event["deletion_target_ids"] == deletion["candidate_snapshots"][0]["source_event_ids"]

    expiry = next(item for item in histories if "explicit_expiry" in item["feature_tags"])
    expiry_pair = expiry["pair_inputs"][0]
    expiry_event = next(item for item in expiry["timeline"]
                        if item["event_id"] == expiry_pair["event_id"])
    expiry_gold = expiry["evaluator_only"]["pair_gold"][0]
    assert expiry_event["event_type"] == "time_advance"
    assert expiry_gold["expected_state_effect"]["effect"] == "expire"
    assert expiry_event["metadata"]["advance_to"] == expiry_event["occurred_at"]
    assert expiry["candidate_snapshots"][0]["canonical_payload"]["valid_until"] < expiry_event["metadata"]["advance_to"]

    missing_clock = deepcopy(expiry)
    missing_clock["timeline"][-1]["metadata"] = {}
    with pytest.raises(CorpusValidationError, match="advance_to"):
        validate_corpus([missing_clock])

    malformed_clock = deepcopy(expiry)
    malformed_clock["timeline"][-1]["metadata"]["advance_to"] = "not-a-timeZ"
    malformed_clock["timeline"][-1]["occurred_at"] = "not-a-timeZ"
    with pytest.raises(CorpusValidationError, match="RFC3339"):
        validate_corpus([malformed_clock])


def test_replacement_tasks_report_prior_and_active_state():
    histories = generate()
    for history_id in ("pilot-04", "pilot-11"):
        history = next(item for item in histories if item["history_id"] == history_id)
        task_gold = next(item for item in history["evaluator_only"]["downstream_task_gold"]
                         if item["task_id"].endswith("state-task"))
        states = task_gold["gold_response"]["current_state"]
        assert [(item["semantic_item_ref"], item["status"]) for item in states] == [
            ("semantic:target", "revoked"), ("semantic:replacement", "active")
        ]


def test_sdui_stale_docs_supersede_and_equal_authority_migration_abstains():
    histories = generate()
    stale_docs = next(item for item in histories if "stale_documentation" in item["feature_tags"])
    stale_gold = stale_docs["evaluator_only"]["pair_gold"][0]
    assert stale_gold["semantic_relationship"] == "supersedes"
    assert stale_gold["transition_disposition"] == "accept"
    assert stale_gold["expected_state_effect"]["effect"] == "close_and_replace"
    assert "current registry is authoritative" in stale_gold["adjudication_notes"]

    migration = next(item for item in histories if "migration_conflict" in item["feature_tags"])
    migration_gold = migration["evaluator_only"]["pair_gold"][0]
    assert migration_gold["semantic_relationship"] == "contradicts"
    assert migration_gold["transition_disposition"] == "abstain"
    assert migration_gold["expected_external_action"] == "clarify"
    assert "no precedence metadata" in migration_gold["adjudication_notes"]
    relevant_events = [migration["timeline"][0], migration["timeline"][2]]
    assert all(item["authority"]["may_assert_user_state"] for item in relevant_events)
    assert len({item["authority"]["reason"] for item in relevant_events}) == 1


def test_sdui_codebase_pilot_coverage_and_action_task_semantics():
    histories = generate()
    sdui = [item for item in histories if "sdui" in item["feature_tags"]]
    assert len(sdui) == 5
    assert {tag for item in sdui for tag in item["feature_tags"]} >= {
        "stale_documentation", "migration_conflict", "ownership_change",
        "generated_schema", "intentional_duplication",
    }
    for history in histories:
        action = history["evaluator_only"]["pair_gold"][0]["expected_external_action"]
        has_action_task = any(task["task_type"] == "action_selection"
                              for task in history["downstream_tasks"])
        assert has_action_task == (action != "none")


def test_only_normalized_pilot_partition_values_are_used():
    assert {history["partition"] for history in generate()} == {
        "pilot_development", "pilot_holdout"
    }


def test_pilot_writer_emits_one_packet_and_no_legacy_review_copy(tmp_path):
    output = tmp_path / "pilot"
    write(output, generate())
    assert (output / "development.jsonl").exists()
    assert (output / "holdout.jsonl").exists()
    assert not (output / "review.jsonl").exists()
    assert [path.name for path in (output / "reviews").glob("*.md")] == [
        "pilot_review_packet.md"
    ]


def test_retrieval_projection_is_limited_to_declared_pool_without_future_snapshots():
    history = generate()[0]
    pair = history["pair_inputs"][0]
    projection = build_retrieval_projection(history, pair["pair_id"])
    pool = history["candidate_pools"][0]
    assert [item["snapshot_id"] for item in projection["candidates"]] == pool["snapshot_ids"]
    event_sequence = next(event["sequence"] for event in history["timeline"]
                          if event["event_id"] == pair["event_id"])
    assert all(item["captured_after_sequence"] <= event_sequence for item in projection["candidates"])


def test_state_matching_is_semantic_not_runtime_id_based():
    gold = {"item_id": "gold-id", "kind": "preference", "proposition": "Concise work answers",
            "scope": {"domain": "work"}, "status": "active", "valid_from": None,
            "valid_until": None, "epistemic_basis": "asserted", "sensitivity": "normal",
            "evidence_ids": ["event-1"]}
    predicted = {**gold, "item_id": "runtime-generated-999"}
    config = MatchConfiguration()
    assert semantic_state_score(predicted, gold, config) == 100
    assert greedy_semantic_matches([predicted], [gold], config) == [(0, 0, 100)]


def test_mock_baseline_contracts_and_full_probability_vector():
    history = generate()[0]
    pair_id = history["pair_inputs"][0]["pair_id"]
    retrieval = build_retrieval_projection(history, pair_id)
    classification = build_pair_classification_projection(history, pair_id)
    assert len(MockCandidateRetriever().rank(retrieval, limit=2)) == 2
    prediction = MockPairClassifier().classify(classification)
    prediction.validate()
    assert set(prediction.probabilities) == {
        "supports", "contradicts", "narrows_scope", "supersedes", "unrelated", "uncertain"}
    system = MockEvaluationSystem()
    system.reset(history["history_id"], {})
    for event in history["timeline"]:
        system.ingest(event)
    assert system.raw_usage().model_calls == 0
    for baseline in (MockRollingSummaryBaseline(), MockSchedulerBaseline(),
                     MockGeneralLLMBaseline(), MockOracleBaseline()):
        baseline.reset(history["history_id"], {})
        baseline.ingest(history["timeline"][0])
        assert baseline.checkpoint(history["checkpoint_requests"][0])["current_state"] == []
        assert baseline.raw_usage().model_calls == 0


def test_probability_contract_rejects_incomplete_vector():
    prediction = PredictedRelationship("snapshot", {"uncertain": "1"}, "uncertain", "1", True)
    with pytest.raises(ValueError, match="exactly six"):
        prediction.validate()


def test_harness_calculates_cost_from_raw_usage():
    usage = RawLifecycleUsage(input_tokens=100, output_tokens=20,
                              provider_usage_records=({"cost_cad": "0.03"},))
    cost = calculate_cost_cad(
        usage, {"input_per_token_cad": "0.00001", "output_per_token_cad": "0.00002"})
    assert cost == Decimal("0.03140")
