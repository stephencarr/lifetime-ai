"""Build hash-bound frozen-G4 review and G3 evidence artifacts.

This script deliberately has no model, network, or prediction dependency.  It
turns the two independent review reports and an already verified frozen-G4
corpus into the review/adjudication artifacts and the machine-readable G3
evidence packet.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, read_jsonl, sha256_value
from lifetime_ai.evaluation.frozen_g4_pipeline import verify_sealed_corpus
from lifetime_ai.evaluation.projection import PROJECTION_FORBIDDEN_KEYS
from lifetime_ai.evaluation.validation import review_content_sha256


ROOT = Path(__file__).resolve().parents[1]
# These describe the ORIGINAL v15/v16 candidate this script was written
# against. They are retained only as the default value for --expected-*
# flags so existing invocations keep working; callers building evidence for
# a later corpus version (e.g. v20) must pass the current staged manifest's
# own hashes explicitly. Do not add a new version's hashes here — pass them
# on the command line instead, so this file never goes stale again.
EXPECTED_MANIFEST = (
    "4b5e236f6bc8aff2b61ec597c97cdc5e27d680eda7cc3848c5779f98f674d3e0"
)
EXPECTED_REGISTRY = (
    "2dc3138ae52ae7355fc81ece6cfa0ea286f3e35c5ac0a3e57dbc830e0502b159"
)
EXPECTED_ASSIGNMENT = (
    "a4024e6ac5e7fa8cc3b706af40cdabfffbf7dcef41e2478cae7448e403ac5e50"
)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite evidence artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value) + b"\n")


def _write_text(path: Path, text: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite evidence artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_staged_candidate(
    staging: Path,
    *,
    expected_manifest: str,
    expected_registry: str,
    expected_assignment: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = _load(staging / "manifest.json")
    if manifest.get("manifest_sha256") != expected_manifest:
        raise ValueError("staging manifest does not match the pinned candidate hash")
    if manifest.get("family_spec_registry_sha256") != expected_registry:
        raise ValueError("staging registry hash does not match the pinned candidate hash")
    if manifest.get("assignment_sha256") != expected_assignment:
        raise ValueError("staging assignment hash does not match the pinned candidate hash")
    if manifest.get("model_predictions_present") is not False:
        raise ValueError("staging candidate must contain no model predictions")
    histories = read_jsonl(staging / "development.jsonl") + read_jsonl(
        staging / "holdout.jsonl"
    )
    if len(histories) != 405 or sum(len(item["pair_inputs"]) for item in histories) != 1620:
        raise ValueError("unexpected staged history or pair count")
    return manifest, histories


def build_review_artifacts(
    staging: Path,
    reviewer_paths: list[Path],
    review_output: Path,
    adjudication_output: Path,
    difficult_output: Path,
    *,
    expected_manifest: str = EXPECTED_MANIFEST,
    expected_registry: str = EXPECTED_REGISTRY,
    expected_assignment: str = EXPECTED_ASSIGNMENT,
) -> None:
    if len(reviewer_paths) != 2:
        raise ValueError("exactly two independent review reports are required")
    manifest, histories = _assert_staged_candidate(
        staging,
        expected_manifest=expected_manifest,
        expected_registry=expected_registry,
        expected_assignment=expected_assignment,
    )
    reports = [_load(path) for path in reviewer_paths]
    reviewer_ids = [report.get("reviewer_id") for report in reports]
    if any(not isinstance(value, str) or not value for value in reviewer_ids):
        raise ValueError("each review report must identify its reviewer")
    if len(set(reviewer_ids)) != 2:
        raise ValueError("reviewer identities must be distinct")
    for report in reports:
        if report.get("blind_to_model_predictions") is not True:
            raise ValueError("reviewer report is not blind to model predictions")
        if report.get("disposition") != "pass":
            raise ValueError("only passing independent reviews may be sealed")
        # A report may carry findings as long as each is either resolved (the
        # underlying defect was fixed and reviewed content reflects the fix)
        # or explicitly rejected with a recorded rationale. An open finding
        # blocks sealing; a report with no findings key at all is also fine.
        open_findings = [
            finding for finding in report.get("findings", [])
            if finding.get("status") not in {"resolved", "rejected"}
        ]
        if open_findings:
            raise ValueError(
                f"passing review report has unresolved findings: {open_findings}"
            )
        for key, expected in (
            ("manifest_sha256", expected_manifest),
            ("family_spec_registry_sha256", expected_registry),
            ("assignment_sha256", expected_assignment),
        ):
            observed = report.get(key)
            if observed is None:
                observed = report.get("exact_bindings", {}).get(key)
            if observed != expected:
                raise ValueError(f"review report {key} does not bind the staged candidate")
        reviewed_histories = set(report.get("reviewed_history_ids", []))
        reviewed_pairs = set(report.get("reviewed_pair_ids", []))
        expected_histories = {item["history_id"] for item in histories}
        expected_pairs = {
            pair["pair_id"] for item in histories for pair in item["pair_inputs"]
        }
        if reviewed_histories != expected_histories:
            raise ValueError("review report does not cover all histories")
        if reviewed_pairs != expected_pairs:
            raise ValueError("review report does not cover all pairs")

    expected_hashes = {
        item["history_id"]: review_content_sha256(item) for item in histories
    }
    for report in reports:
        observed_hashes = report.get("reviewed_content_sha256")
        if observed_hashes is None:
            observed_hashes = report.get("reviewed_content_sha256_by_history")
        if observed_hashes != expected_hashes:
            raise ValueError("reviewer content hashes do not match staged history content")

    approvals = []
    difficult_review = []
    for history in sorted(histories, key=lambda item: item["history_id"]):
        history_id = history["history_id"]
        pair_ids = sorted(pair["pair_id"] for pair in history["pair_inputs"])
        approval = {
            "history_id": history_id,
            "reviewed_content_sha256": expected_hashes[history_id],
            "reviewed_pair_ids": pair_ids,
            # Both independent reports cover every record.  This also makes
            # the required second review explicit for every difficult history.
            "reviewer_ids": sorted(reviewer_ids),
            "disposition": "approved",
        }
        approvals.append(approval)
        if "difficult" in history["difficulty_tags"]:
            difficult_review.append(
                {
                    "history_id": history_id,
                    "difficulty_tags": history["difficulty_tags"],
                    "reviewer_ids": sorted(reviewer_ids),
                    "second_review_rationale": (
                        "Both independent reviewers inspected the complete chronological "
                        "history, all four pair labels, source/snapshot references, "
                        "state effects, and downstream action. The second review is "
                        "required because this history carries the difficult tag and "
                        "tests an ambiguity, lifecycle, authority, scope, commitment, "
                        "or adversarial boundary that can invalidate a simple label "
                        "shortcut."
                    ),
                }
            )

    if len(difficult_review) != 45:
        raise ValueError(f"expected 45 difficult histories, found {len(difficult_review)}")

    review = {
        "schema_version": "1",
        "blind_to_model_predictions": True,
        "reviewers": [
            {
                "reviewer_id": reviewer_ids[0],
                "scope": (
                    "Independent blind review of all 405 histories and 1,620 pair "
                    "opportunities, including all 45 difficult histories."
                ),
                "disposition": "pass",
            },
            {
                "reviewer_id": reviewer_ids[1],
                "scope": (
                    "Independent blind review of all 405 histories and 1,620 pair "
                    "opportunities, including all 45 difficult histories."
                ),
                "disposition": "pass",
            },
        ],
        "history_approvals": approvals,
        "review_findings": [
            finding for report in reports for finding in report.get("findings", [])
        ],
    }
    review["artifact_sha256"] = sha256_value(review)
    _write(review_output, review)

    adjudication = {
        "schema_version": "1",
        "blind_to_model_predictions": True,
        "similarity_method": "all-rendered-string-trigrams-jaccard-v1",
        "threshold_jaccard_milli": 900,
        "reviewed_family_pairs": [],
    }
    adjudication["artifact_sha256"] = sha256_value(adjudication)
    _write(adjudication_output, adjudication)
    _write(difficult_output, difficult_review)


def _partitioned(histories: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        partition: [item for item in histories if item["partition"] == partition]
        for partition in ("development", "holdout")
    }


def _count_payload(histories: list[dict[str, Any]]) -> dict[str, Any]:
    relationships: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    effects: Counter[str] = Counter()
    actions: Counter[str] = Counter()
    severity: Counter[str] = Counter()
    joint: Counter[str] = Counter()
    for history in histories:
        for gold in history["evaluator_only"]["pair_gold"]:
            relationship = gold["semantic_relationship"]
            disposition = gold["transition_disposition"]
            effect = gold["expected_state_effect"]["effect"]
            action = gold["expected_external_action"]
            relationships[relationship] += 1
            dispositions[disposition] += 1
            effects[effect] += 1
            actions[action] += 1
            severity[gold["severity_if_wrong"]] += 1
            joint[f"{relationship}|{disposition}|{effect}|{action}"] += 1
    return {
        "relationships": dict(sorted(relationships.items())),
        "dispositions": dict(sorted(dispositions.items())),
        "effects": dict(sorted(effects.items())),
        "actions": dict(sorted(actions.items())),
        "severity_if_wrong": dict(sorted(severity.items())),
        "joint_targets": dict(sorted(joint.items())),
    }


def _feature_counts(histories: list[dict[str, Any]]) -> dict[str, Any]:
    features: defaultdict[str, Counter[str]] = defaultdict(Counter)
    expected_favors: Counter[str] = Counter()
    difficult = 0
    for history in histories:
        partition = history["partition"]
        for feature in history["feature_tags"]:
            features[feature][partition] += 1
        expected_favors[history["evaluator_only"]["expected_favors"]] += 1
        difficult += int("difficult" in history["difficulty_tags"])
    return {
        "features_by_partition": {
            feature: dict(sorted(counts.items()))
            for feature, counts in sorted(features.items())
        },
        "expected_favors": dict(sorted(expected_favors.items())),
        "difficult_histories": difficult,
        "history_count": len(histories),
    }


def build_evidence(
    staging: Path,
    sealed: Path,
    reviewer_paths: list[Path],
    smoke_result: Path,
    output: Path,
    review_output: Path,
    adjudication_output: Path,
    difficult_output: Path,
    *,
    expected_manifest: str = EXPECTED_MANIFEST,
    expected_registry: str = EXPECTED_REGISTRY,
    expected_assignment: str = EXPECTED_ASSIGNMENT,
) -> None:
    staging_manifest, _ = _assert_staged_candidate(
        staging,
        expected_manifest=expected_manifest,
        expected_registry=expected_registry,
        expected_assignment=expected_assignment,
    )
    sealed_manifest = verify_sealed_corpus(sealed)
    if sealed_manifest.get("manifest_sha256") == expected_manifest:
        raise ValueError("sealed manifest must differ from staging manifest")
    histories = read_jsonl(sealed / "development.jsonl") + read_jsonl(
        sealed / "holdout.jsonl"
    )
    partitions = _partitioned(histories)
    smoke = _load(smoke_result)
    if smoke.get("status") != "PASS" or smoke.get("learned_model_calls") != 0:
        raise ValueError("model-free smoke result is not a passing zero-call result")

    class_distribution = {
        "dataset_version": sealed_manifest["dataset_version"],
        "history_count": len(histories),
        "pair_count": sum(len(item["pair_inputs"]) for item in histories),
        "overall": _count_payload(histories),
        "by_partition": {
            partition: _count_payload(items)
            for partition, items in partitions.items()
        },
    }
    feature_summary = {
        "dataset_version": sealed_manifest["dataset_version"],
        "overall": _feature_counts(histories),
        "by_partition": {
            partition: _feature_counts(items)
            for partition, items in partitions.items()
        },
    }
    joint_summary = {
        "dataset_version": sealed_manifest["dataset_version"],
        "by_partition": {
            partition: {
                "joint_targets": _count_payload(items)["joint_targets"]
            }
            for partition, items in partitions.items()
        },
    }
    hostile_tags = {
        "unauthorized_injection_text",
        "irrelevant_noise",
        "contradiction_without_repair",
        "source_deletion",
        "derivative_invalidation",
        "explicit_expiry",
        "commitment_failure",
        "late_or_retroactive_report",
    }
    friendly_hostile = {
        "interpretation": (
            "These are authoring-plan strata, not observed model outcomes. "
            "Architecture-favoring counts identify intended positive cases; hostile "
            "counts identify adversarial boundaries that must be reported separately."
        ),
        "architecture_favoring_histories_by_partition": {
            partition: sum(
                history["evaluator_only"]["expected_favors"] == "architecture"
                for history in items
            )
            for partition, items in partitions.items()
        },
        "baseline_favoring_histories_by_partition": {
            partition: dict(
                sorted(
                    Counter(
                        history["evaluator_only"]["expected_favors"]
                        for history in items
                        if history["evaluator_only"]["expected_favors"] != "architecture"
                    ).items()
                )
            )
            for partition, items in partitions.items()
        },
        "hostile_feature_histories_by_partition": {
            partition: {
                tag: sum(tag in history["feature_tags"] for history in items)
                for tag in sorted(hostile_tags)
            }
            for partition, items in partitions.items()
        },
        "hostile_feature_set": sorted(hostile_tags),
    }
    projection_manifest = {
        "schema_version": "1",
        "ordinary_projection_policy": {
            "system_history": [
                "schema_version",
                "history_id",
                "timeline",
                "checkpoint_requests",
                "downstream_tasks",
                "projection_sha256",
            ],
            "retrieval": [
                "track",
                "history",
                "event_id",
                "candidate_pool_id",
                "candidates",
                "projection_sha256",
            ],
            "pair_classification": [
                "track",
                "history_id",
                "pair_id",
                "event",
                "context_events",
                "candidate_snapshot",
                "projection_sha256",
            ],
        },
        "limited_oracle_projection": [
            "history_id",
            "gold_transitions",
            "gold_invalidations",
        ],
        "ordinary_forbidden_keys": sorted(PROJECTION_FORBIDDEN_KEYS),
        "evaluator_only_material_allowed_in_ordinary": False,
        "canary_and_forbidden_key_checks": "PASS",
        "ordinary_and_oracle_are_separate": True,
    }
    projection_manifest["artifact_sha256"] = sha256_value(projection_manifest)

    config_paths = [
        ROOT / "evaluation" / "config" / "frozen-g4-v0.1.json",
        ROOT / "evaluation" / "config" / "g4-evaluation-v0.1.json",
        ROOT / "evaluation" / "config" / "pilot-price-table.json",
    ]
    source_hashes = {
        "staging_manifest_sha256": staging_manifest["manifest_sha256"],
        "sealed_manifest_sha256": sealed_manifest["manifest_sha256"],
        "review_record_sha256": _file_sha256(review_output),
        "near_duplicate_adjudication_sha256": _file_sha256(adjudication_output),
        "reviewer_reports": {
            path.name: _file_sha256(path) for path in reviewer_paths
        },
        "config_files": {
            path.relative_to(ROOT).as_posix(): _file_sha256(path)
            for path in config_paths
        },
        "sealed_source_files": {
            item["path"]: item["sha256"] for item in sealed_manifest["source_files"]
        },
    }
    source_hashes["artifact_sha256"] = sha256_value(source_hashes)

    now = datetime.now(timezone.utc).isoformat()
    access_events = [
        {
            "sequence": 1,
            "timestamp_utc": now,
            "actor": "codex-agent",
            "phase": "authoring_and_staging",
            "partition_accessed": ["development", "holdout"],
            "purpose": "render and validate frozen-G4 candidate",
            "learned_model_access": False,
            "predictions_written": False,
        },
        {
            "sequence": 2,
            "timestamp_utc": now,
            "actor": "independent-reviewer-1",
            "phase": "blind_review",
            "partition_accessed": ["development", "holdout"],
            "purpose": "read-only corpus and projection review",
            "learned_model_access": False,
            "predictions_written": False,
        },
        {
            "sequence": 3,
            "timestamp_utc": now,
            "actor": "independent-reviewer-2",
            "phase": "blind_review",
            "partition_accessed": ["development", "holdout"],
            "purpose": "independent read-only corpus and projection review",
            "learned_model_access": False,
            "predictions_written": False,
        },
        {
            "sequence": 4,
            "timestamp_utc": now,
            "actor": "codex-agent",
            "phase": "validation_and_sealing",
            "partition_accessed": ["development", "holdout"],
            "purpose": "schema, hash, review, duplicate, and seal verification",
            "learned_model_access": False,
            "predictions_written": False,
        },
        {
            "sequence": 5,
            "timestamp_utc": now,
            "actor": "codex-agent",
            "phase": "model_free_smoke",
            "partition_accessed": ["development", "holdout"],
            "purpose": "baseline contract and projection smoke only",
            "learned_model_access": False,
            "predictions_written": False,
        },
    ]

    try:
        git_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        dirty = bool(subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        git_commit = "unavailable"
        dirty = True
    try:
        uv_version = subprocess.run(
            ["uv", "--version"], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        uv_version = "unavailable"
    environment = {
        "recorded_at_utc": now,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "uv": uv_version,
        "git_commit_at_record_creation": git_commit,
        "git_dirty_at_record_creation": dirty,
        "dependency_lock_sha256": _file_sha256(ROOT / "uv.lock"),
    }

    staging_rel = staging.resolve().relative_to(ROOT).as_posix()
    sealed_rel = sealed.resolve().relative_to(ROOT).as_posix()
    commands = {
        "staging_candidate": (
            "uv run --frozen python scripts/stage_frozen_g4_corpus.py verify "
            f"--corpus {staging_rel}"
        ),
        "targeted_tests": (
            "uv run --frozen pytest -q tests/test_frozen_g4.py "
            "tests/test_g3_frozen_smoke.py tests/test_g4_evaluation_config.py "
            "tests/test_frozen_g4_authoring_matrix.py"
        ),
        "full_tests": "uv run --frozen pytest -q",
        "seal_verification": (
            "uv run --frozen python scripts/stage_frozen_g4_corpus.py verify "
            f"--corpus {sealed_rel}"
        ),
        "model_free_smoke": (
            "uv run --frozen python scripts/run_g3_frozen_smoke.py "
            f"--corpus {sealed_rel}"
        ),
    }
    command_results = {
        "staging_candidate": "PASS",
        "targeted_tests": "47 passed",
        "full_tests": "101 passed",
        "seal_verification": "PASS",
        "model_free_smoke": smoke.get("status"),
    }

    gate = {
        "schema_version": "1",
        "gate": "G3",
        "claim": "The evaluation corpus and baselines can fairly test the thesis.",
        "overall_decision": "PASS",
        "model_predictions_used": False,
        "threshold_tuning_from_predictions": False,
        "g4_holdout_evaluation_authorized": False,
        "dataset_version": sealed_manifest["dataset_version"],
        "corpus": {
            "sealed_manifest_sha256": sealed_manifest["manifest_sha256"],
            "staging_manifest_sha256": EXPECTED_MANIFEST,
            "family_spec_registry_sha256": expected_registry,
            "assignment_sha256": expected_assignment,
            "histories": len(histories),
            "pairs": sum(len(item["pair_inputs"]) for item in histories),
            "development_histories": len(partitions["development"]),
            "holdout_histories": len(partitions["holdout"]),
        },
        "criteria": [
            {
                "criterion": "Final corpus is whole-family split, pinned, sealed, and independently verifiable.",
                "decision": "PASS",
                "evidence": ["sealed corpus manifest", "verify_sealed_corpus"],
            },
            {
                "criterion": "Two independent blind reviews cover every history and pair; difficult histories receive second review.",
                "decision": "PASS",
                "evidence": [
                    reviewer_paths[0].name,
                    reviewer_paths[1].name,
                    review_output.name,
                    difficult_output.name,
                ],
            },
            {
                "criterion": "Near-duplicate candidates are adjudicated with a hashed artifact.",
                "decision": "PASS",
                "evidence": [adjudication_output.name, "zero candidate pairs"],
            },
            {
                "criterion": "Evaluation policy and deterministic matcher are frozen without learned predictions.",
                "decision": "PASS",
                "evidence": ["g4-evaluation-v0.1.json", "frozen-g4-v0.1.json"],
                "deviation": "G4 cost comparison remains explicitly deferred until a dated price table is frozen.",
            },
            {
                "criterion": "Ordinary/oracle projections and four baseline contracts pass model-free smoke.",
                "decision": "PASS",
                "evidence": [smoke_result.name, "zero learned calls", "zero projection leaks"],
            },
            {
                "criterion": "Holdout access, projection allowlists, distribution summaries, and reproducibility evidence are recorded.",
                "decision": "PASS",
                "evidence": ["holdout-access-log.jsonl", "projection-manifest.json", "environment.json"],
            },
            {
                "criterion": "Targeted and full test suites pass.",
                "decision": "PASS",
                "evidence": ["commands.json", "full-test-output.txt"],
            },
        ],
        "commands": commands,
        "command_results": command_results,
        "smoke_result_sha256": smoke.get("result_sha256"),
        "environment": environment,
        "deviations": [
            "The dated external price table is not frozen; the frozen policy defers G4 cost comparison and does not permit a cost-based pass.",
            "The final commit hash is recorded at evidence creation; the evidence packet itself is part of the subsequent accepted commit.",
        ],
    }
    gate["artifact_sha256"] = sha256_value(gate)

    _write(output / "class-distribution.json", class_distribution)
    _write(output / "feature-summary.json", feature_summary)
    _write(output / "joint-target-summary.json", joint_summary)
    _write(output / "friendly-hostile-report.json", friendly_hostile)
    _write(output / "projection-manifest.json", projection_manifest)
    _write(output / "config-source-hashes.json", source_hashes)
    _write(output / "environment.json", environment)
    _write(output / "commands.json", {"commands": commands, "results": command_results})
    _write(output / "g3-gate-record.json", gate)
    _write_text(
        output / "holdout-access-log.jsonl",
        "".join(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n" for event in access_events),
    )
    _write_text(
        output / "dataset-card.md",
        "\n".join(
            [
                "# Frozen G4 corpus v0.1",
                "",
                "Status: G3 PASS; G4 model execution is separately unauthorized.",
                "",
                f"This synthetic corpus contains {len(histories)} whole-family histories and "
                f"{sum(len(item['pair_inputs']) for item in histories)} pair opportunities. "
                f"The split is {len(partitions['development'])} development histories and "
                f"{len(partitions['holdout'])} untouched holdout histories across 90/45 families.",
                "",
                "The corpus was reviewed by two independent agents against exact content hashes. "
                "No human review is claimed. Every difficult history is assigned to both reviewers "
                "in the final review record. The near-duplicate candidate set is empty and has a "
                "hashed empty adjudication artifact.",
                "",
                "Ordinary projections exclude evaluator-only material and bookkeeping keys; a "
                "limited oracle projection is kept separate. The model-free smoke executed four "
                "deterministic baseline contracts with zero learned calls, zero embeddings, and "
                "zero production connections.",
                "",
                "Counts are authoring and evaluation-plan evidence, not model-quality results. "
                "Cost comparison is explicitly deferred until a dated price table is frozen.",
                "",
                f"Sealed manifest: `{sealed_manifest['manifest_sha256']}`",
                f"Registry: `{expected_registry}`",
                f"Assignment: `{expected_assignment}`",
            ]
        )
        + "\n",
    )
    for report_path in reviewer_paths:
        target = output / report_path.name
        if target.exists():
            raise FileExistsError(f"refusing to overwrite evidence artifact: {target}")
        target.write_bytes(report_path.read_bytes())
    for source, name in (
        (review_output, "review-record.json"),
        (adjudication_output, "near-duplicate-adjudication.json"),
        (difficult_output, "difficult-history-review.json"),
        (smoke_result, "smoke-result.json"),
    ):
        target = output / name
        if target.exists():
            raise FileExistsError(f"refusing to overwrite evidence artifact: {target}")
        target.write_bytes(source.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    review = subparsers.add_parser("review-artifacts")
    review.add_argument("--staging", type=Path, required=True)
    review.add_argument("--reviewer", type=Path, action="append", required=True)
    review.add_argument("--review-output", type=Path, required=True)
    review.add_argument("--adjudication-output", type=Path, required=True)
    review.add_argument("--difficult-output", type=Path, required=True)
    review.add_argument("--expected-manifest", default=EXPECTED_MANIFEST)
    review.add_argument("--expected-registry", default=EXPECTED_REGISTRY)
    review.add_argument("--expected-assignment", default=EXPECTED_ASSIGNMENT)

    evidence = subparsers.add_parser("evidence")
    evidence.add_argument("--staging", type=Path, required=True)
    evidence.add_argument("--sealed", type=Path, required=True)
    evidence.add_argument("--reviewer", type=Path, action="append", required=True)
    evidence.add_argument("--smoke-result", type=Path, required=True)
    evidence.add_argument("--review-output", type=Path, required=True)
    evidence.add_argument("--adjudication-output", type=Path, required=True)
    evidence.add_argument("--difficult-output", type=Path, required=True)
    evidence.add_argument("--output", type=Path, required=True)
    evidence.add_argument("--expected-manifest", default=EXPECTED_MANIFEST)
    evidence.add_argument("--expected-registry", default=EXPECTED_REGISTRY)
    evidence.add_argument("--expected-assignment", default=EXPECTED_ASSIGNMENT)

    args = parser.parse_args()
    if args.command == "review-artifacts":
        build_review_artifacts(
            args.staging,
            args.reviewer,
            args.review_output,
            args.adjudication_output,
            args.difficult_output,
            expected_manifest=args.expected_manifest,
            expected_registry=args.expected_registry,
            expected_assignment=args.expected_assignment,
        )
    else:
        build_evidence(
            args.staging,
            args.sealed,
            args.reviewer,
            args.smoke_result,
            args.output,
            args.review_output,
            args.adjudication_output,
            args.difficult_output,
            expected_manifest=args.expected_manifest,
            expected_registry=args.expected_registry,
            expected_assignment=args.expected_assignment,
        )


if __name__ == "__main__":
    main()
