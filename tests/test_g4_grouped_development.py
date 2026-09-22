from lifetime_ai.evaluation.g4_features import pair_feature_document
from scripts.run_g4_grouped_development import Case, _folds, _select_threshold
from scripts.run_g4_local_development import _make_prediction


def _case(family: str, gold: str = "supports") -> Case:
    return Case(family, family, family, family, gold, (), "medium", "", "", "", "")


def test_grouped_folds_keep_each_family_together():
    cases = [_case(str(family)) for family in range(10) for _ in range(3)]
    folds = _folds(cases, list(range(len(cases))), 5, "test")
    assert sorted(index for fold in folds for index in fold) == list(range(len(cases)))
    assert all(len({cases[index].family_id for index in fold}) == 2 for fold in folds)


def test_threshold_selection_counts_equal_confidence_as_one_group():
    cases = [_case("correct"), _case("wrong", gold="contradicts")]
    tied = {"supports": 0.99, "contradicts": 0.01,
            "narrows_scope": 0.0, "supersedes": 0.0,
            "unrelated": 0.0, "uncertain": 0.0}
    assert _select_threshold(cases, [(0, tied), (1, tied)]) == 1.0


def test_uncertain_always_escalates_and_features_exclude_evaluator_fields():
    probabilities = {"supports": 0.01, "contradicts": 0.01,
                     "narrows_scope": 0.01, "supersedes": 0.01,
                     "unrelated": 0.01, "uncertain": 0.95}
    assert _make_prediction("snapshot", probabilities, 0.95).escalate

    projection = {
        "event": {"event_type": "message", "content": "new content", "source_status": "present",
                  "event_id": "opaque-event"},
        "candidate_snapshot": {"canonical_payload": {
            "kind": "fact", "proposition": "old content", "scope": {"domain": "work"},
            "status": "active", "valid_until": None,
        }, "snapshot_id": "opaque-snapshot"},
        "context_events": [],
        "evaluator_only": {"semantic_relationship": "CANARY_GOLD"},
    }
    document = pair_feature_document(projection)
    assert "new content" in document and "old content" in document
    assert "CANARY_GOLD" not in document
    assert "opaque-event" not in document and "opaque-snapshot" not in document
