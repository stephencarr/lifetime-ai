import json
from pathlib import Path

import pytest

from scripts import build_g3_frozen_evidence


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "evaluation" / "corpus" / "frozen-g4-v0.1-staging-v21"
SEALED = ROOT / "evaluation" / "corpus" / "frozen-g4-v0.1-sealed-v21"


@pytest.mark.parametrize("status", ["resolved", "rejected"])
def test_closed_review_finding_requires_summary_rationale(status):
    with pytest.raises(ValueError, match="non-empty summary rationale"):
        build_g3_frozen_evidence._validate_review_findings([
            {"finding_id": "finding-1", "status": status}
        ])


def test_open_review_finding_is_rejected():
    with pytest.raises(ValueError, match="unresolved finding"):
        build_g3_frozen_evidence._validate_review_findings([
            {"finding_id": "finding-1", "status": "open", "summary": "Still needs work."}
        ])


@pytest.mark.parametrize("status", ["resolved", "rejected"])
def test_closed_review_finding_with_summary_is_accepted(status):
    build_g3_frozen_evidence._validate_review_findings([
        {
            "finding_id": "finding-1",
            "status": status,
            "summary": "The disposition and its evidence were recorded.",
        }
    ])


def test_build_evidence_records_the_supplied_staging_manifest_hash(tmp_path):
    """The gate record must not fall back to the legacy v15 default pin."""
    staging_manifest = json.loads((STAGING / "manifest.json").read_text(encoding="utf-8"))
    smoke_result = tmp_path / "smoke-result.json"
    smoke_result.write_text(
        json.dumps({"status": "PASS", "learned_model_calls": 0}), encoding="utf-8"
    )
    reviewer_paths = []
    for index in (1, 2):
        path = tmp_path / f"reviewer-{index}.json"
        path.write_text("{}", encoding="utf-8")
        reviewer_paths.append(path)
    difficult_review = tmp_path / "difficult-history-review.json"
    difficult_review.write_text("[]\n", encoding="utf-8")

    output = tmp_path / "evidence"
    build_g3_frozen_evidence.build_evidence(
        STAGING,
        SEALED,
        reviewer_paths,
        smoke_result,
        output,
        SEALED / "review-record.json",
        SEALED / "near-duplicate-adjudication.json",
        difficult_review,
        expected_manifest=staging_manifest["manifest_sha256"],
        expected_registry=staging_manifest["family_spec_registry_sha256"],
        expected_assignment=staging_manifest["assignment_sha256"],
    )

    gate = json.loads((output / "g3-gate-record.json").read_text(encoding="utf-8"))
    assert gate["corpus"]["staging_manifest_sha256"] == staging_manifest["manifest_sha256"]
