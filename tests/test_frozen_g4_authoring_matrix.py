from collections import Counter

from scripts.generate_frozen_g4_authoring_matrix import (
    FEATURES,
    RELATIONSHIPS,
    build_authoring_matrix,
)


def test_authoring_matrix_has_complete_unique_family_plan():
    matrix = build_authoring_matrix()
    families = matrix["families"]
    assert matrix["status"] == "AUTHORING_PLAN_NOT_CORPUS"
    assert len(families) == 135
    assert len({item["family_id"] for item in families}) == 135
    assert all(item["family_id"].startswith("g4-family-") for item in families)
    assert all(item["domain"] not in item["family_id"] for item in families)
    assert all(item["authoring_status"] == "planned" for item in families)


def test_authoring_matrix_balances_relationships_and_covers_targets():
    matrix = build_authoring_matrix()
    families = matrix["families"]
    relationships = Counter(item["primary_relationship"] for item in families)
    assert set(relationships) == set(RELATIONSHIPS)
    # Lifecycle controls are semantically unrelated rather than supersessions,
    # so primary-family counts intentionally need not be mechanically equal.
    assert relationships == Counter(matrix["summary"]["relationship_families"])
    assert all(
        set(item["planned_relationship_pair_counts"]) == set(RELATIONSHIPS)
        and sum(item["planned_relationship_pair_counts"].values()) == 12
        and item["planned_relationship_pair_counts"][item["primary_relationship"]] == 4
        for item in families
    )
    observed_features = {
        feature for item in families for feature in item["required_features"]
    }
    assert observed_features == set(FEATURES)
    assert {value for item in families for value in item["planned_dispositions"]} >= {
        "accept", "reject_unauthorized", "reject_invalid", "abstain", "no_op"
    }
    assert {value for item in families for value in item["planned_effects"]} >= {
        "reinforce", "preserve_conflict", "add_scoped_item", "close_and_replace",
        "resolve", "invalidate", "expire", "none",
    }
    assert {value for item in families for value in item["planned_actions"]} >= {
        "none", "clarify", "investigate", "outreach_candidate", "silence"
    }
    assert {value for item in families for value in item["expected_favors"]} == {
        "architecture", "baseline_a", "baseline_b", "baseline_c", "neutral"
    }
