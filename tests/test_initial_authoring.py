from copy import deepcopy

import pytest

from lifetime_ai.evaluation.canonical import canonical_bytes
from lifetime_ai.evaluation.frozen_g4 import _frozen_schema_validator
from lifetime_ai.evaluation.frozen_g4_pipeline import render_blueprint
from lifetime_ai.evaluation.initial_authoring import build_initial_blueprints, remap_blueprint_identifiers
from lifetime_ai.evaluation.validation import CorpusValidationError, validate_history


@pytest.fixture(scope="module")
def batch():
    return build_initial_blueprints()


def test_batch_is_reproducible_pending_and_complete(batch):
    assert canonical_bytes(batch) == canonical_bytes(build_initial_blueprints())
    histories = [history for blueprint in batch for history in render_blueprint(blueprint)[0]]
    assert len(histories) == 18
    assert sum(len(history["pair_inputs"]) for history in histories) == 72
    assert len({history["history_id"] for history in histories}) == 18
    for history in histories:
        assert history["reviewer_status"] == "pending"
        assert history["partition"] == "development"
        assert history["evaluator_only"]["generation_and_review_provenance"]["reviewed_content_sha256"] is None
        assert all(gold["adjudication_status"] == "pending" and gold["adjudication_notes"]
                   for gold in history["evaluator_only"]["pair_gold"])


def test_calibration_batch_covers_every_relationship_and_transition_boundary(batch):
    expected = {
        "supports": ("accept", "reinforce", "none"),
        "contradicts": ("abstain", "preserve_conflict", "clarify"),
        "narrows_scope": ("accept", "add_scoped_item", "none"),
        "supersedes": ("accept", "close_and_replace", "none"),
        "unrelated": ("no_op", "none", "silence"),
        "uncertain": ("abstain", "none", "clarify"),
    }
    for blueprint in batch:
        golds = [
            gold
            for history in blueprint["histories"]
            for gold in history["evaluator_only"]["pair_gold"]
        ]
        assert {gold["semantic_relationship"] for gold in golds} == set(expected)
        for gold in golds:
            disposition, effect, action = expected[gold["semantic_relationship"]]
            assert gold["transition_disposition"] == disposition
            assert gold["expected_state_effect"]["effect"] == effect
            assert gold["expected_external_action"] == action
            if gold["semantic_relationship"] == "uncertain":
                assert gold["ambiguity_reason"]


def test_invented_resolution_and_unrecorded_reinforcement_rejected(batch):
    for family_index, field, value in ((0, "evidence_ids", []), (1, "status", "active")):
        history = deepcopy(render_blueprint(batch[family_index])[0][0])
        history["evaluator_only"]["checkpoint_gold"][1]["current_state"][0][field] = value
        with pytest.raises(CorpusValidationError):
            validate_history(history, schema_validator=_frozen_schema_validator(),
                             expected_corpus_stage="frozen_g4", allowed_partitions={"development"})


def test_opaque_remapping_preserves_references_and_rehashes_pools(batch):
    for blueprint in batch:
        remapped = remap_blueprint_identifiers(blueprint, salt="test-only-opaque-mapping")
        assert remapped["family_id"].startswith("opaque-")
        assert remapped["family_id"] != blueprint["family_id"]
        for history in remapped["histories"]:
            assert history["history_id"].startswith("opaque-")
            assert all(pair["pair_id"].startswith("opaque-") for pair in history["pair_inputs"])
            assert history["candidate_pools"][0]["sha256"] != blueprint["histories"][0]["candidate_pools"][0]["sha256"]
        assert remapped == remap_blueprint_identifiers(blueprint, salt="test-only-opaque-mapping")
