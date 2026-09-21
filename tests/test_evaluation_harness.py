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
from lifetime_ai.evaluation.coverage import validate_development_pilot_coverage
from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection, build_retrieval_projection,
    build_system_history_projection, contains_evaluator_only_material,
)
from lifetime_ai.evaluation.split import (
    assign_disjoint_gate_holdouts, split_stratified_families, split_whole_families,
)
from lifetime_ai.evaluation.state_matching import (
    MatchConfiguration, greedy_semantic_matches, semantic_state_score,
)
from lifetime_ai.evaluation.validation import CorpusValidationError, validate_corpus
from scripts.generate_g3_pilot import _review_packet, generate, write
from scripts.generate_g3_development_pilot import (
    generate as generate_full_pilot, write as write_full_pilot,
)
from scripts.run_g3_pilot_smoke import run as run_pilot_smoke


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
    reviewed = {history["history_id"] for history in histories
                if history["reviewer_status"] == "reviewed"}
    assert reviewed == {f"pilot-{index:02d}" for index in range(1, 14)}
    assert sum(history["reviewer_status"] == "pending" for history in histories) == 0
    for history in histories:
        expected_status = "agreed" if history["history_id"] in reviewed else "pending"
        assert history["evaluator_only"]["pair_gold"][0]["adjudication_status"] == expected_status
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


def test_pair_classification_projection_is_authority_free_and_task_free():
    history = next(item for item in generate() if item["history_id"] == "pilot-12")
    pair_id = history["pair_inputs"][0]["pair_id"]
    projection = build_pair_classification_projection(history, pair_id)
    serialized = json.dumps(projection)
    assert "authority" not in serialized
    assert "downstream_tasks" not in serialized
    assert "action_selection" not in serialized
    assert "source/generated-schema discrepancy" not in serialized
    assert set(projection) == {
        "track", "history_id", "pair_id", "event", "context_events",
        "candidate_snapshot", "projection_sha256",
    }


def test_deletion_uses_event_path_and_removes_content_after_sequence():
    history = next(item for item in generate() if "source_deletion" in item["feature_tags"])
    source_id = history["timeline"][0]["event_id"]
    assert any(event["event_type"] == "deletion" and source_id in event["deletion_target_ids"]
               for event in history["timeline"])
    projection = build_system_history_projection(history)
    source = next(event for event in projection["timeline"] if event["event_id"] == source_id)
    assert source["content"] is None and source["source_status"] == "deleted"
    assert history["evaluator_only"]["deleted_source_content"][source_id] not in json.dumps(projection)

    pair_id = history["pair_inputs"][0]["pair_id"]
    retrieval = build_retrieval_projection(history, pair_id)
    classification = build_pair_classification_projection(history, pair_id)
    deleted_content = history["evaluator_only"]["deleted_source_content"][source_id]
    assert deleted_content not in json.dumps(retrieval)
    assert deleted_content not in json.dumps(classification)
    target = classification["candidate_snapshot"]
    assert target["tombstoned"] is True
    assert target["source_status"] == "deleted"
    assert "canonical_payload" not in target


def test_deletion_and_expiry_are_the_evaluated_lifecycle_events():
    histories = generate()
    deletion = next(item for item in histories if "sole_source_deletion" in item["feature_tags"])
    deletion_pair = deletion["pair_inputs"][0]
    deletion_event = next(item for item in deletion["timeline"]
                          if item["event_id"] == deletion_pair["event_id"])
    deletion_gold = deletion["evaluator_only"]["pair_gold"][0]
    assert deletion_event["event_type"] == "deletion"
    assert deletion_gold["expected_state_effect"]["effect"] == "invalidate"
    assert deletion_gold["semantic_relationship"] == "unrelated"
    assert deletion_event["deletion_target_ids"] == deletion["candidate_snapshots"][0]["source_event_ids"]
    deletion_state = deletion["evaluator_only"]["checkpoint_gold"][0]["current_state"][0]
    assert deletion_state["valid_until"] == deletion_event["occurred_at"]

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


def test_revised_pilot_tasks_require_content_scope_status_and_evidence():
    histories = generate()
    revised_ids = {
        "pilot-01", "pilot-02", "pilot-03", "pilot-05",
        "pilot-06", "pilot-07", "pilot-12", "pilot-13",
    }
    for history in histories:
        if history["history_id"] not in revised_ids:
            continue
        task_gold = next(item for item in history["evaluator_only"]["downstream_task_gold"]
                         if item["task_id"].endswith("state-task"))
        states = task_gold["gold_response"]["current_state"]
        assert states
        assert all(set(item) == {
            "semantic_item_ref", "proposition", "scope", "status", "evidence_ids"
        } for item in states)

    scoped = next(item for item in histories if item["history_id"] == "pilot-03")
    snapshot_scope = scoped["candidate_snapshots"][0]["canonical_payload"]["scope"]
    scoped_states = scoped["evaluator_only"]["checkpoint_gold"][0]["current_state"]
    assert snapshot_scope == {"domain": "all_answers"}
    assert [item["scope"] for item in scoped_states] == [
        {"domain": "all_answers"}, {"domain": "personal_research"}
    ]

    generated_schema = next(item for item in histories if item["history_id"] == "pilot-12")
    action_task = next(item for item in generated_schema["downstream_tasks"]
                       if item["task_type"] == "action_selection")
    assert "system" in action_task["request"]["question"]
    assert "schema" in action_task["request"]["question"]


def test_sdui_stale_docs_supersede_and_equal_authority_migration_abstains():
    histories = generate()
    stale_docs = next(item for item in histories if "stale_documentation" in item["feature_tags"])
    stale_gold = stale_docs["evaluator_only"]["pair_gold"][0]
    stale_snapshot = stale_docs["candidate_snapshots"][0]
    assert stale_snapshot["sha256"] == "0b5abec58a014fea359dccdbd8f18b3720825a913373a39ecdcc9067674d6936"
    assert stale_gold["semantic_relationship"] == "supersedes"
    assert stale_gold["transition_disposition"] == "accept"
    assert stale_gold["expected_state_effect"]["effect"] == "close_and_replace"
    assert stale_gold["expected_external_action"] == "none"
    assert not any(task["task_type"] == "action_selection"
                   for task in stale_docs["downstream_tasks"])
    assert "current registry is authoritative" in stale_gold["adjudication_notes"]
    assert "No investigation is required" in stale_gold["adjudication_notes"]

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


def test_stratified_split_is_deterministic_and_preserves_21_9_counts():
    base = generate()[0]
    histories = []
    for index in range(30):
        history = deepcopy(base)
        history["history_id"] = f"synthetic-{index:02d}"
        history["family_id"] = f"synthetic-family-{index:02d}"
        histories.append(history)
    first = split_stratified_families(histories, seed="coverage")
    second = split_stratified_families(histories, seed="coverage")
    assert first == second
    assert sum(value == "pilot_holdout" for value in first.values()) == 9
    assert sum(value == "pilot_development" for value in first.values()) == 21


def test_full_pilot_coverage_gate_rejects_seed_corpus():
    with pytest.raises(CorpusValidationError, match="expected 30 histories"):
        validate_development_pilot_coverage(generate())


def test_expanded_development_pilot_meets_frozen_scale_and_coverage():
    histories = generate_full_pilot()
    validate_corpus(histories)
    validate_development_pilot_coverage(histories)
    assert len(histories) == 30
    assert sum(len(history["pair_inputs"]) for history in histories) == 120
    assert sum(history["partition"] == "pilot_development" for history in histories) == 21
    assert sum(history["partition"] == "pilot_holdout" for history in histories) == 9
    assert all(history["reviewer_status"] == "pending" for history in histories)
    assert all(history["dataset_version"] == "pilot-v0.2" for history in histories)
    family_partitions = {}
    for history in histories:
        assert family_partitions.setdefault(
            history["family_id"], history["partition"]) == history["partition"]
    assert len(family_partitions) == 10


def test_expanded_pilot_temporal_resolution_and_action_context_are_coherent():
    histories = generate_full_pilot()
    events = {event["event_id"]: event for history in histories for event in history["timeline"]}
    for history in histories:
        gold_by_pair = {gold["pair_id"]: gold for gold in history["evaluator_only"]["pair_gold"]}
        checkpoints = {item["checkpoint_id"]: item
                       for item in history["evaluator_only"]["checkpoint_gold"]}
        tasks = {task["pair_id"]: task for task in history["downstream_tasks"]
                 if task["task_id"].endswith("state-task")}
        for pair in history["pair_inputs"]:
            gold = gold_by_pair[pair["pair_id"]]
            event = events[pair["event_id"]]
            if "late_or_retroactive_report" in gold.get("feature_tags", []):
                assert event["event_type"] not in {"deletion", "redaction", "time_advance"}
                assert event["occurred_at"] < event["recorded_at"]
            checkpoint = checkpoints[tasks[pair["pair_id"]]["checkpoint_id"]]
            if gold["expected_state_effect"]["effect"] == "resolve":
                refs = gold["expected_state_effect"]["affected_item_ids"]
                resolved = [item for item in checkpoint["current_state"]
                            if item["semantic_item_ref"] in refs]
                assert len(resolved) == 1
                assert resolved[0]["status"] == "resolved"
                assert not gold["expected_state_effect"]["expected_new_item_ids"]
            if gold["expected_external_action"] in {"outreach_candidate", "investigate"}:
                assert len(pair["context_event_ids"]) == 2
                assert set(pair["context_event_ids"]) <= set(gold["required_evidence_ids"])


def test_pilot_writer_emits_one_packet_and_no_legacy_review_copy(tmp_path):
    output = tmp_path / "pilot"
    write(output, generate())
    assert (output / "development.jsonl").exists()
    assert (output / "holdout.jsonl").exists()
    assert not (output / "review.jsonl").exists()
    assert [path.name for path in (output / "reviews").glob("*.md")] == [
        "pilot_review_packet.md"
    ]


def test_multi_pair_history_validates_renders_and_runs_all_tracks():
    history = deepcopy(generate()[0])
    history["reviewer_status"] = "pending"
    history["evaluator_only"]["generation_and_review_provenance"][
        "reviewed_content_sha256"] = None
    for gold in history["evaluator_only"]["pair_gold"]:
        gold["adjudication_status"] = "pending"

    second_pair = deepcopy(history["pair_inputs"][0])
    second_pair["pair_id"] = "pilot-01-pair-2"
    history["pair_inputs"].append(second_pair)
    second_gold = deepcopy(history["evaluator_only"]["pair_gold"][0])
    second_gold["pair_id"] = second_pair["pair_id"]
    second_gold["expected_external_action"] = "silence"
    history["evaluator_only"]["pair_gold"].append(second_gold)
    action_task = {
        "task_id": "pilot-01-action-task-2", "pair_id": second_pair["pair_id"],
        "checkpoint_id": "pilot-01-checkpoint", "task_type": "action_selection",
        "request": {"question": "What external action, if any, should be taken now?"},
        "target_scope": {"mode": "pair", "pair_id": second_pair["pair_id"]},
        "maximum_context_budget": 800, "scale_family_id": None,
        "irrelevant_history_target": None,
    }
    history["downstream_tasks"].append(action_task)
    history["evaluator_only"]["downstream_task_gold"].append({
        "task_id": action_task["task_id"], "gold_response": {"action": "silence"},
        "relevant_dependency_ids": ["pilot-01-source", "pilot-01-event"],
        "counterevidence_ids": [], "primary_metric": "external_action_accuracy",
    })

    validate_corpus([history])
    packet = _review_packet([history], {history["history_id"]: ("development.jsonl", 1)})
    assert packet.count("### Pair `") == 2
    assert packet.count("Pair decision:") == 2
    for pair in history["pair_inputs"]:
        retrieval = build_retrieval_projection(history, pair["pair_id"])
        classification = build_pair_classification_projection(history, pair["pair_id"])
        assert MockCandidateRetriever().rank(retrieval, limit=2)
        MockPairClassifier().classify(classification).validate()
    system_projection = build_system_history_projection(history)
    system = MockEvaluationSystem()
    system.reset(history["history_id"], {})
    for event in system_projection["timeline"]:
        system.ingest(event)
    for checkpoint in system_projection["checkpoint_requests"]:
        system.checkpoint(checkpoint)


def test_smoke_status_reports_completed_pilot_review(tmp_path):
    output = tmp_path / "pilot"
    write(output, generate())
    result = run_pilot_smoke(output)
    assert result["status"] == "PILOT_HUMAN_REVIEW_COMPLETE"
    assert result["g3_complete"] is False
    assert set(result["baseline_contract_cases"].values()) == {13}


def test_expanded_pilot_writer_and_smoke_remain_non_final(tmp_path):
    output = tmp_path / "pilot-v0.2"
    write_full_pilot(output, generate_full_pilot())
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["status"] == "AWAITING_HUMAN_REVIEW"
    assert manifest["final_gate_holdouts_created"] is False
    assert (output / "dataset-card.md").exists()
    distribution = json.loads((output / "class-distribution.json").read_text())
    assert set(distribution["relationships"].values()) == {20}
    feature_summary = json.loads((output / "feature-summary.json").read_text())
    assert feature_summary["multi_pair_histories"] == 30
    packet = (output / "reviews" / "pilot_review_packet.md").read_text()
    assert packet.count("Pair decision:") == 120
    assert packet.count("History/checkpoint decision:") == 30
    result = run_pilot_smoke(output)
    assert result["status"] == "AWAITING_HUMAN_REVIEW"
    assert set(result["baseline_contract_cases"].values()) == {30}


def test_review_approval_hash_is_invalidated_by_content_change():
    history = deepcopy(generate()[0])
    history["timeline"][-1]["content"] = "Changed after approval."
    with pytest.raises(CorpusValidationError, match="review approval hash"):
        validate_corpus([history])


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
