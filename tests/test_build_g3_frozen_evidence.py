import json
from pathlib import Path

import pytest

from lifetime_ai.evaluation.canonical import canonical_bytes, sha256_bytes
from scripts import build_g3_frozen_evidence


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "evaluation" / "corpus" / "frozen-g4-v0.1-staging-v21"
SEALED = ROOT / "evaluation" / "corpus" / "frozen-g4-v0.1-sealed-v21"


def _build_evidence_kwargs(tmp_path, *, review_output):
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
    return dict(
        staging=STAGING,
        sealed=SEALED,
        reviewer_paths=reviewer_paths,
        smoke_result=smoke_result,
        review_output=review_output,
        adjudication_output=SEALED / "near-duplicate-adjudication.json",
        difficult_output=difficult_review,
        expected_manifest=staging_manifest["manifest_sha256"],
        expected_registry=staging_manifest["family_spec_registry_sha256"],
        expected_assignment=staging_manifest["assignment_sha256"],
    )


def _review_record_with_findings(findings):
    record = json.loads((SEALED / "review-record.json").read_text(encoding="utf-8"))
    record["review_findings"] = findings
    material = {key: value for key, value in record.items() if key != "artifact_sha256"}
    record["artifact_sha256"] = sha256_bytes(canonical_bytes(material))
    return record


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
    kwargs = _build_evidence_kwargs(tmp_path, review_output=SEALED / "review-record.json")
    staging_manifest = json.loads((STAGING / "manifest.json").read_text(encoding="utf-8"))
    output = tmp_path / "evidence"

    build_g3_frozen_evidence.build_evidence(
        kwargs["staging"],
        kwargs["sealed"],
        kwargs["reviewer_paths"],
        kwargs["smoke_result"],
        output,
        kwargs["review_output"],
        kwargs["adjudication_output"],
        kwargs["difficult_output"],
        expected_manifest=kwargs["expected_manifest"],
        expected_registry=kwargs["expected_registry"],
        expected_assignment=kwargs["expected_assignment"],
    )

    gate = json.loads((output / "g3-gate-record.json").read_text(encoding="utf-8"))
    assert gate["corpus"]["staging_manifest_sha256"] == staging_manifest["manifest_sha256"]


def test_build_evidence_rejects_malformed_review_output(tmp_path):
    """build_evidence() must not accept a bare {} or other non-schema-valid
    stand-in for review_output -- this is the real review-record file that
    becomes part of the sealed evidence packet, and skipping validation here
    would let an unreviewed/fabricated review record through even though
    _validate_review_findings exists."""
    review_output = tmp_path / "review-output.json"
    review_output.write_text("{}", encoding="utf-8")
    kwargs = _build_evidence_kwargs(tmp_path, review_output=review_output)

    with pytest.raises(Exception, match="schema violation|required property"):
        build_g3_frozen_evidence.build_evidence(
            kwargs["staging"],
            kwargs["sealed"],
            kwargs["reviewer_paths"],
            kwargs["smoke_result"],
            tmp_path / "evidence-malformed",
            kwargs["review_output"],
            kwargs["adjudication_output"],
            kwargs["difficult_output"],
            expected_manifest=kwargs["expected_manifest"],
            expected_registry=kwargs["expected_registry"],
            expected_assignment=kwargs["expected_assignment"],
        )


def test_build_evidence_rejects_open_finding_in_review_output(tmp_path):
    """A schema-valid review_output with a genuinely open finding must still
    be rejected -- schema validity alone is not enough."""
    record = _review_record_with_findings([
        {"finding_id": "test-open", "status": "open", "summary": "Not fixed yet."}
    ])
    review_output = tmp_path / "review-output.json"
    review_output.write_text(json.dumps(record), encoding="utf-8")
    kwargs = _build_evidence_kwargs(tmp_path, review_output=review_output)

    with pytest.raises(ValueError, match="unresolved finding"):
        build_g3_frozen_evidence.build_evidence(
            kwargs["staging"],
            kwargs["sealed"],
            kwargs["reviewer_paths"],
            kwargs["smoke_result"],
            tmp_path / "evidence-open-finding",
            kwargs["review_output"],
            kwargs["adjudication_output"],
            kwargs["difficult_output"],
            expected_manifest=kwargs["expected_manifest"],
            expected_registry=kwargs["expected_registry"],
            expected_assignment=kwargs["expected_assignment"],
        )


def test_build_evidence_accepts_real_review_output_with_resolved_and_rejected_findings(tmp_path):
    """Sanity check: the actual v20/v21 review record (genuine resolved and
    rejected findings, each with a real rationale) must still be accepted --
    the new validation must not be so strict it rejects legitimate evidence."""
    kwargs = _build_evidence_kwargs(tmp_path, review_output=SEALED / "review-record.json")
    build_g3_frozen_evidence.build_evidence(
        kwargs["staging"],
        kwargs["sealed"],
        kwargs["reviewer_paths"],
        kwargs["smoke_result"],
        tmp_path / "evidence-real",
        kwargs["review_output"],
        kwargs["adjudication_output"],
        kwargs["difficult_output"],
        expected_manifest=kwargs["expected_manifest"],
        expected_registry=kwargs["expected_registry"],
        expected_assignment=kwargs["expected_assignment"],
    )
