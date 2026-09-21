from __future__ import annotations

import hashlib
from pathlib import Path

from lifetime_ai.evaluation.canonical import sha256_value, strict_json_loads


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "evaluation" / "config" / "g4-evaluation-v0.1.json"


def _config():
    value = strict_json_loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_g4_policy_preserves_approved_gate_thresholds():
    config = _config()
    assert config["status"] == "PROVISIONAL_PRE_G3_CORPUS_REVIEW"
    assert config["authorization"] == {
        "model_predictions_authorized": False,
        "threshold_tuning_authorized": False,
        "holdout_evaluation_authorized": False,
        "separate_g4_run_authorization_required": True,
    }
    assert config["approved_gate_thresholds"] == {
        "autonomous_precision_minimum": "0.95",
        "precision_pass_rule": "observed_point_precision",
        "autonomous_coverage_minimum": "0.30",
        "minimum_untouched_holdout_autonomous_decisions": 100,
        "unauthorized_mutations_maximum": 0,
        "high_severity_errors_maximum": 0,
        "expected_calibration_error_maximum": "0.10",
        "generative_semantic_decision_call_reduction_vs_baseline_c_minimum": "0.25",
        "local_median_decision_latency_rule": "strictly_less_than_baseline_c_median",
    }
    interval = config["reporting"]["confidence_interval"]
    assert interval == {
        "metric": "autonomous_precision",
        "method": "wilson_score_interval",
        "confidence_level": "0.95",
        "sidedness": "two_sided",
        "used_as_pass_threshold": False,
    }


def test_g4_policy_fails_closed_on_unapproved_choices():
    config = _config()
    assert config["freeze_blockers"]
    assert config["decision_policy"]["autonomous_acceptance_threshold"].startswith("UNSET_")
    assert config["failure_handling"]["timeout_seconds"].startswith("UNSET_")
    assert config["exclusions"]["prespecified_rules"].startswith("UNSET_")
    assert config["semantic_state_matching"]["status"] == (
        "PROVISIONAL_PILOT_CANDIDATE_NOT_FROZEN"
    )
    assert config["lifecycle_accounting"]["price_table"]["replacement_required_before_g3_pass"]


def test_g4_policy_price_table_hashes_match_referenced_file():
    config = _config()
    price = config["lifecycle_accounting"]["price_table"]
    path = ROOT / price["path"]
    raw = path.read_bytes()
    value = strict_json_loads(raw.decode("utf-8"))
    assert hashlib.sha256(raw).hexdigest() == price["file_sha256"]
    assert sha256_value(value) == price["canonical_value_sha256"]


def test_g4_policy_accounts_for_every_required_metric_and_lifecycle_phase():
    config = _config()
    assert set(config["reporting"]["relationship_metrics"]) == {
        "accuracy", "per_class_precision", "per_class_recall",
        "multiclass_brier_score", "expected_calibration_error",
    }
    assert set(config["reporting"]["tracks_reported_separately"]) == {
        "candidate_retrieval", "pair_classification", "end_to_end_longitudinal",
    }
    assert set(config["lifecycle_accounting"]["phases_reported_separately"]) == {
        "ingestion", "retrieval", "consolidation", "classification",
        "escalation", "repair", "final_response",
    }
    assert config["exclusions"]["post_holdout_outcome_driven_exclusions_allowed"] is False
    assert config["exclusions"]["failed_examples_retained_in_reports"] is True
    assert config["baseline_parity"]["oracle_receives_only_limited_oracle_projection"]
