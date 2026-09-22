from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .canonical import (
    CANONICAL_PROFILE,
    canonical_bytes,
    canonical_jsonl_bytes,
    file_manifest_entry,
    sha256_bytes,
    sha256_value,
    strict_json_loads,
    read_jsonl,
)
from .frozen_g4 import (
    _FROZEN_CONFIG,
    _frozen_schema_validator,
    assign_frozen_g4_families,
    frozen_history_content_sha256,
    frozen_g4_near_duplicate_candidates,
    validate_frozen_g4_coverage,
)
from .validation import CorpusValidationError, review_content_sha256, validate_history


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_SCHEMA = ROOT / "evaluation" / "schema" / "frozen-g4-blueprint.schema.json"
FAMILY_SPEC_SCHEMA = ROOT / "evaluation" / "schema" / "frozen-g4-family-spec.schema.json"
FROZEN_HISTORY_SCHEMA = ROOT / "evaluation" / "schema" / "frozen-g4-history.schema.json"
REVIEW_RECORD_SCHEMA = ROOT / "evaluation" / "schema" / "frozen-g4-review-record.schema.json"
CONFIG_PATH = ROOT / "evaluation" / "config" / "frozen-g4-v0.1.json"
STAGED_PAYLOAD_PATHS = {
    "assignment-manifest.json",
    "blueprint-registry.jsonl",
    "development.jsonl",
    "family-specs.jsonl",
    "holdout.jsonl",
    "near-duplicate-candidates.json",
}
SEALED_PAYLOAD_PATHS = {
    "assignment-manifest.json",
    "development.jsonl",
    "family-specs.jsonl",
    "holdout.jsonl",
    "near-duplicate-adjudication.json",
    "review-record.json",
    "staging-manifest.json",
}
REVIEW_BLOCKER = "blind review of all histories and pair opportunities is not recorded"
ADJUDICATION_BLOCKER = "near-duplicate adjudication artifact is absent"
REGISTRY_PIN_BLOCKER = "family specification registry hash is not pinned in frozen config"


def _schema_validator(path: Path) -> Draft202012Validator:
    schema_root = ROOT / "evaluation" / "schema"
    schemas = [
        strict_json_loads(item.read_text(encoding="utf-8"))
        for item in sorted(schema_root.glob("*.schema.json"))
    ]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    target = strict_json_loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(target, registry=registry)


def load_blueprints(directory: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    """Load a closed registry of one JSON blueprint per family."""
    paths = sorted(directory.glob("*.json"))
    if not paths:
        raise CorpusValidationError(f"no frozen-G4 blueprints found in {directory}")
    validator = _schema_validator(BLUEPRINT_SCHEMA)
    blueprints: list[dict[str, Any]] = []
    family_ids: set[str] = set()
    for path in paths:
        value = strict_json_loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise CorpusValidationError(f"blueprint {path} is not a JSON object")
        errors = sorted(validator.iter_errors(value), key=lambda item: list(item.path))
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.path) or "$"
            raise CorpusValidationError(
                f"blueprint {path.name} schema violation at {location}: {first.message}"
            )
        family_id = value["family_id"]
        if family_id in family_ids:
            raise CorpusValidationError(f"duplicate blueprint family_id: {family_id}")
        family_ids.add(family_id)
        blueprints.append(value)
    return blueprints, paths


def load_authoring_matrix(path: Path) -> dict[str, Any]:
    matrix = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(matrix, dict):
        raise CorpusValidationError("authoring matrix must be a JSON object")
    required = {
        "matrix_version", "dataset_version", "status", "families", "summary",
        "matrix_sha256",
    }
    if set(matrix) != required:
        raise CorpusValidationError(
            f"authoring matrix fields differ from the frozen contract: {sorted(set(matrix))}"
        )
    material = {key: value for key, value in matrix.items() if key != "matrix_sha256"}
    if matrix["matrix_sha256"] != sha256_value(material):
        raise CorpusValidationError("authoring matrix hash mismatch")
    if matrix["dataset_version"] != _FROZEN_CONFIG["dataset_version"]:
        raise CorpusValidationError("authoring matrix dataset version mismatch")
    if matrix["status"] != "AUTHORING_PLAN_NOT_CORPUS":
        raise CorpusValidationError("unexpected authoring matrix status")
    return matrix


def validate_blueprints_against_authoring_matrix(
    blueprints: list[dict[str, Any]], matrix: dict[str, Any], *, require_complete: bool = True
) -> None:
    plans = {item["family_id"]: item for item in matrix["families"]}
    if len(plans) != len(matrix["families"]):
        raise CorpusValidationError("authoring matrix repeats a family ID")
    authored = {item["family_id"]: item for item in blueprints}
    if require_complete and set(authored) != set(plans):
        raise CorpusValidationError(
            "blueprint registry must exactly match authoring matrix family IDs"
        )
    if not set(authored) <= set(plans):
        raise CorpusValidationError("blueprint registry contains families absent from authoring matrix")
    for family_id, blueprint in authored.items():
        plan = plans[family_id]
        comparisons = {
            "primary_relationship": blueprint["primary_relationship"],
            "feature_tags": sorted(blueprint["feature_tags"]),
            "difficulty_tags": sorted(blueprint["difficulty_tags"]),
            "expected_favors": sorted(blueprint["expected_favors"]),
            "deletion_presence": blueprint["deletion_presence"],
            "ambiguity_presence": blueprint["ambiguity_presence"],
        }
        expected = {
            "primary_relationship": plan["primary_relationship"],
            "feature_tags": sorted(plan["required_features"]),
            "difficulty_tags": sorted(plan["difficulty_tags"]),
            "expected_favors": sorted(plan["expected_favors"]),
            "deletion_presence": plan["deletion_presence"],
            "ambiguity_presence": plan["ambiguity_presence"],
        }
        if comparisons != expected:
            raise CorpusValidationError(
                f"blueprint {family_id!r} does not match its authoring matrix strata"
            )
        observed_relationships = Counter(
            gold["semantic_relationship"]
            for history in blueprint["histories"]
            for gold in history["evaluator_only"]["pair_gold"]
        )
        if dict(sorted(observed_relationships.items())) != plan[
            "planned_relationship_pair_counts"
        ]:
            raise CorpusValidationError(
                f"blueprint {family_id!r} relationship mix differs from authoring matrix"
            )
        observed_dispositions = sorted({
            gold["transition_disposition"]
            for history in blueprint["histories"]
            for gold in history["evaluator_only"]["pair_gold"]
        })
        observed_effects = sorted({
            gold["expected_state_effect"]["effect"]
            for history in blueprint["histories"]
            for gold in history["evaluator_only"]["pair_gold"]
        })
        observed_actions = sorted({
            gold["expected_external_action"]
            for history in blueprint["histories"]
            for gold in history["evaluator_only"]["pair_gold"]
        })
        for label, observed in (
            ("planned_dispositions", observed_dispositions),
            ("planned_effects", observed_effects),
            ("planned_actions", observed_actions),
        ):
            if observed != plan[label]:
                raise CorpusValidationError(
                    f"blueprint {family_id!r} {label} differ from authoring matrix"
                )


def render_blueprint(blueprint: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Render one family without assigning its final partition."""
    family_id = blueprint["family_id"]
    histories: list[dict[str, Any]] = []
    seen_history_ids: set[str] = set()
    for template in blueprint["histories"]:
        history_id = template["history_id"]
        if history_id in seen_history_ids:
            raise CorpusValidationError(
                f"blueprint {family_id!r} repeats history_id {history_id!r}"
            )
        seen_history_ids.add(history_id)
        history = {
            "schema_version": "1",
            "dataset_version": _FROZEN_CONFIG["dataset_version"],
            "corpus_stage": _FROZEN_CONFIG["corpus_stage"],
            "history_id": history_id,
            "family_id": family_id,
            # Partition is deliberately provisional. It is excluded from the
            # substantive content hash and replaced exactly once after split.
            "partition": "development",
            "generation_origin": blueprint["generation_origin"],
            "reviewer_status": "pending",
            **deepcopy({key: value for key, value in template.items() if key != "history_id"}),
        }
        histories.append(history)

    spec = {
        "family_id": family_id,
        "primary_relationship": blueprint["primary_relationship"],
        "feature_tags": sorted(blueprint["feature_tags"]),
        "difficulty_tags": sorted(blueprint["difficulty_tags"]),
        "expected_favors": sorted(blueprint["expected_favors"]),
        "deletion_presence": blueprint["deletion_presence"],
        "ambiguity_presence": blueprint["ambiguity_presence"],
        "rendered_histories": [
            {
                "history_id": history["history_id"],
                "content_sha256": frozen_history_content_sha256(history),
            }
            for history in sorted(histories, key=lambda item: item["history_id"])
        ],
    }
    errors = list(_schema_validator(FAMILY_SPEC_SCHEMA).iter_errors(spec))
    if errors:
        raise CorpusValidationError(
            f"rendered family spec {family_id!r} is invalid: {errors[0].message}"
        )
    return histories, spec


def render_blueprint_registry(
    blueprints: Iterable[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Render, bind, split, and validate a complete frozen-G4 registry."""
    histories: list[dict[str, Any]] = []
    family_specs: list[dict[str, Any]] = []
    for blueprint in sorted(blueprints, key=lambda item: item["family_id"]):
        family_histories, spec = render_blueprint(blueprint)
        histories.extend(family_histories)
        family_specs.append(spec)

    assignment = assign_frozen_g4_families(family_specs)
    partitions = {
        record["family_id"]: record["partition"]
        for record in assignment["assignments"]
    }
    validator = _frozen_schema_validator()
    global_history_ids: set[str] = set()
    for history in histories:
        history_id = history["history_id"]
        if history_id in global_history_ids:
            raise CorpusValidationError(f"duplicate rendered history_id: {history_id}")
        global_history_ids.add(history_id)
        history["partition"] = partitions[history["family_id"]]
        validate_history(
            history,
            schema_validator=validator,
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )
    return histories, family_specs, assignment


def _root_entry(path: Path) -> dict[str, Any]:
    return {**file_manifest_entry(path), "path": path.relative_to(ROOT).as_posix()}


def stage_blueprint_registry(
    blueprint_directory: Path, authoring_matrix_path: Path, output: Path
) -> dict[str, Any]:
    """Write a new, reviewable staging corpus. Existing paths are never overwritten."""
    blueprint_directory = blueprint_directory.resolve()
    authoring_matrix_path = authoring_matrix_path.resolve()
    output = output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing staging path: {output}")
    blueprints, blueprint_paths = load_blueprints(blueprint_directory)
    matrix = load_authoring_matrix(authoring_matrix_path)
    validate_blueprints_against_authoring_matrix(blueprints, matrix)
    outside_repository = [path for path in blueprint_paths if not path.is_relative_to(ROOT)]
    if outside_repository:
        raise CorpusValidationError(
            "blueprint registry must be repository-backed for dependency hashing: "
            f"{outside_repository}"
        )
    histories, family_specs, assignment = render_blueprint_registry(blueprints)
    validate_frozen_g4_coverage(
        histories,
        family_specs=family_specs,
        assignment_manifest=assignment,
        require_sealing_artifacts=False,
    )
    development = sorted(
        (item for item in histories if item["partition"] == "development"),
        key=lambda item: item["history_id"],
    )
    holdout = sorted(
        (item for item in histories if item["partition"] == "holdout"),
        key=lambda item: item["history_id"],
    )

    payloads = {
        "blueprint-registry.jsonl": canonical_jsonl_bytes(
            sorted(blueprints, key=lambda item: item["family_id"])
        ),
        "family-specs.jsonl": canonical_jsonl_bytes(
            sorted(family_specs, key=lambda item: item["family_id"])
        ),
        "assignment-manifest.json": canonical_bytes(assignment) + b"\n",
        "development.jsonl": canonical_jsonl_bytes(development),
        "holdout.jsonl": canonical_jsonl_bytes(holdout),
        "near-duplicate-candidates.json": canonical_bytes({
            "schema_version": "1",
            "similarity_method": _FROZEN_CONFIG["review_and_sealing"][
                "near_duplicate_adjudication_method"
            ],
            "threshold_jaccard_milli": round(
                _FROZEN_CONFIG["family_integrity"][
                    "near_duplicate_review_threshold_jaccard"
                ] * 1000
            ),
            "candidate_family_pairs": frozen_g4_near_duplicate_candidates(histories),
            "blind_to_model_predictions": True,
        }) + b"\n",
    }
    output.mkdir(parents=True)
    for name, content in payloads.items():
        (output / name).write_bytes(content)

    record_counts = {
        "blueprint-registry.jsonl": len(blueprints),
        "family-specs.jsonl": len(family_specs),
        "development.jsonl": len(development),
        "holdout.jsonl": len(holdout),
    }
    schema_paths = sorted((ROOT / "evaluation" / "schema").glob("*.schema.json"))
    source_paths = [
        CONFIG_PATH,
        ROOT / "evaluation" / "config" / "g4-evaluation-v0.1.json",
        authoring_matrix_path,
        *schema_paths,
        ROOT / "lifetime_ai" / "evaluation" / "canonical.py",
        ROOT / "lifetime_ai" / "evaluation" / "frozen_g4.py",
        ROOT / "lifetime_ai" / "evaluation" / "frozen_g4_pipeline.py",
        ROOT / "lifetime_ai" / "evaluation" / "contracts.py",
        ROOT / "lifetime_ai" / "evaluation" / "projection.py",
        ROOT / "lifetime_ai" / "evaluation" / "validation.py",
        ROOT / "scripts" / "run_g3_frozen_smoke.py",
        ROOT / "uv.lock",
        *blueprint_paths,
    ]
    manifest = {
        "manifest_version": "1",
        "state": "STAGED_NOT_SEALED",
        "canonical_profile": CANONICAL_PROFILE,
        "dataset_version": _FROZEN_CONFIG["dataset_version"],
        "authoring_matrix_sha256": matrix["matrix_sha256"],
        "family_spec_registry_sha256": assignment["family_spec_registry_sha256"],
        "assignment_sha256": assignment["assignment_sha256"],
        "files": [
            {
                **file_manifest_entry(output / name, record_count=record_counts.get(name)),
                "path": name,
            }
            for name in sorted(payloads)
        ],
        "source_files": [_root_entry(path) for path in sorted(set(source_paths))],
        "sealing_blockers": [
            REVIEW_BLOCKER,
            ADJUDICATION_BLOCKER,
            *(
                []
                if _FROZEN_CONFIG["family_integrity"][
                    "expected_family_spec_registry_sha256"
                ] == assignment["family_spec_registry_sha256"]
                else [REGISTRY_PIN_BLOCKER]
            ),
        ],
        "model_predictions_present": False,
    }
    manifest["manifest_sha256"] = sha256_value(manifest)
    manifest_bytes = canonical_bytes(manifest) + b"\n"
    (output / "manifest.json").write_bytes(manifest_bytes)
    checksum = hashlib.sha256(manifest_bytes).hexdigest()
    (output / "manifest.sha256").write_text(
        f"{checksum}  manifest.json\n", encoding="utf-8"
    )
    return manifest


def _load_hashed_artifact(path: Path, schema_path: Path) -> dict[str, Any]:
    value = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CorpusValidationError(f"artifact {path} is not a JSON object")
    errors = sorted(_schema_validator(schema_path).iter_errors(value), key=lambda item: list(item.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "$"
        raise CorpusValidationError(
            f"artifact {path.name} schema violation at {location}: {first.message}"
        )
    material = {key: item for key, item in value.items() if key != "artifact_sha256"}
    if value["artifact_sha256"] != sha256_value(material):
        raise CorpusValidationError(f"artifact {path.name} hash mismatch")
    return value


def _safe_relative_manifest_path(raw: Any, *, group: str) -> Path:
    if not isinstance(raw, str) or not raw:
        raise CorpusValidationError(f"{group} manifest path must be a non-empty string")
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw:
        raise CorpusValidationError(f"unsafe {group} manifest path: {raw!r}")
    return path


def _jsonl_record_count(path: Path) -> int:
    return len(read_jsonl(path))


def _verify_manifest_entries(
    entries: Any,
    *,
    base: Path,
    group: str,
    expected_paths: set[str] | None = None,
) -> set[str]:
    if not isinstance(entries, list):
        raise CorpusValidationError(f"manifest {group} must be a list")
    paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise CorpusValidationError(f"manifest {group} entry must be an object")
        relative = _safe_relative_manifest_path(entry.get("path"), group=group)
        raw_path = relative.as_posix()
        if raw_path in paths:
            raise CorpusValidationError(f"manifest {group} repeats path: {raw_path}")
        paths.add(raw_path)
        path = base / relative
        if not path.is_file():
            raise CorpusValidationError(f"manifest file is missing: {raw_path}")
        fresh = file_manifest_entry(path)
        for field in ("bytes", "sha256"):
            if entry.get(field) != fresh[field]:
                raise CorpusValidationError(
                    f"manifest mismatch for {raw_path} field {field}"
                )
        if raw_path.endswith(".jsonl"):
            if not isinstance(entry.get("record_count"), int):
                raise CorpusValidationError(
                    f"JSONL manifest entry lacks record_count: {raw_path}"
                )
            if entry["record_count"] != _jsonl_record_count(path):
                raise CorpusValidationError(
                    f"manifest mismatch for {raw_path} field record_count"
                )
        elif "record_count" in entry:
            raise CorpusValidationError(
                f"non-JSONL manifest entry carries record_count: {raw_path}"
            )
    if expected_paths is not None and paths != expected_paths:
        raise CorpusValidationError(
            f"manifest {group} paths differ; expected={sorted(expected_paths)}, "
            f"found={sorted(paths)}"
        )
    return paths


def _verify_directory_contents(directory: Path, payload_paths: set[str]) -> None:
    expected = payload_paths | {"manifest.json", "manifest.sha256"}
    found = {item.name for item in directory.iterdir()}
    if found != expected:
        raise CorpusValidationError(
            "directory contains unknown or unmanifested paths; "
            f"expected={sorted(expected)}, found={sorted(found)}"
        )
    if any(not item.is_file() for item in directory.iterdir()):
        raise CorpusValidationError("manifest directories must contain only regular files")


def _load_verified_manifest(
    directory: Path,
    *,
    expected_state: str,
    expected_payload_paths: set[str],
) -> dict[str, Any]:
    manifest_path = directory / "manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = strict_json_loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("state") != expected_state:
        raise CorpusValidationError(
            f"input is not a frozen-G4 {expected_state.lower()} manifest"
        )
    material = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if manifest.get("manifest_sha256") != sha256_value(material):
        raise CorpusValidationError("staging manifest content hash mismatch")
    sidecar = (directory / "manifest.sha256").read_text(encoding="utf-8").strip().split()
    if sidecar != [sha256_bytes(manifest_bytes), "manifest.json"]:
        raise CorpusValidationError("manifest checksum sidecar mismatch")
    _verify_manifest_entries(
        manifest.get("files"), base=directory, group="files",
        expected_paths=expected_payload_paths,
    )
    _verify_manifest_entries(
        manifest.get("source_files"), base=ROOT, group="source_files"
    )
    _verify_directory_contents(directory, expected_payload_paths)
    return manifest


def _verify_staging_manifest(staging: Path) -> dict[str, Any]:
    return _load_verified_manifest(
        staging,
        expected_state="STAGED_NOT_SEALED",
        expected_payload_paths=STAGED_PAYLOAD_PATHS,
    )


def verify_sealed_corpus(directory: Path) -> dict[str, Any]:
    """Verify a sealed corpus manifest, payloads, provenance, and staging link."""
    manifest = _load_verified_manifest(
        directory,
        expected_state="SEALED",
        expected_payload_paths=SEALED_PAYLOAD_PATHS,
    )
    staging_manifest = strict_json_loads(
        (directory / "staging-manifest.json").read_text(encoding="utf-8")
    )
    if not isinstance(staging_manifest, dict):
        raise CorpusValidationError("embedded staging manifest is not an object")
    staging_material = {
        key: value for key, value in staging_manifest.items() if key != "manifest_sha256"
    }
    if staging_manifest.get("manifest_sha256") != sha256_value(staging_material):
        raise CorpusValidationError("embedded staging manifest content hash mismatch")
    if staging_manifest.get("state") != "STAGED_NOT_SEALED":
        raise CorpusValidationError("embedded manifest is not a staging manifest")
    if manifest.get("staging_manifest_sha256") != staging_manifest["manifest_sha256"]:
        raise CorpusValidationError("sealed manifest staging link mismatch")
    if manifest.get("source_files") != staging_manifest.get("source_files"):
        raise CorpusValidationError("sealed source dependencies differ from staging manifest")
    review = _load_hashed_artifact(directory / "review-record.json", REVIEW_RECORD_SCHEMA)
    duplicate_schema = ROOT / "evaluation" / "schema" / "frozen-g4-duplicate-adjudication.schema.json"
    adjudication = _load_hashed_artifact(
        directory / "near-duplicate-adjudication.json", duplicate_schema
    )
    histories = read_jsonl(directory / "development.jsonl") + read_jsonl(
        directory / "holdout.jsonl"
    )
    family_specs = read_jsonl(directory / "family-specs.jsonl")
    assignment = strict_json_loads(
        (directory / "assignment-manifest.json").read_text(encoding="utf-8")
    )
    if not isinstance(assignment, dict):
        raise CorpusValidationError("sealed assignment manifest is not an object")
    if manifest.get("family_spec_registry_sha256") != assignment.get(
        "family_spec_registry_sha256"
    ):
        raise CorpusValidationError("sealed registry field differs from assignment payload")
    if manifest.get("assignment_sha256") != assignment.get("assignment_sha256"):
        raise CorpusValidationError("sealed assignment field differs from assignment payload")
    if staging_manifest.get("family_spec_registry_sha256") != assignment.get(
        "family_spec_registry_sha256"
    ) or staging_manifest.get("assignment_sha256") != assignment.get("assignment_sha256"):
        raise CorpusValidationError("embedded staging assignment fields differ from payload")
    unreviewed = deepcopy(histories)
    for history in unreviewed:
        history["reviewer_status"] = "pending"
        history["evaluator_only"]["generation_and_review_provenance"][
            "reviewed_content_sha256"
        ] = None
        for gold in history["evaluator_only"]["pair_gold"]:
            gold["adjudication_status"] = "pending"
    reapplied = _apply_blind_review(unreviewed, review)
    if canonical_jsonl_bytes(sorted(reapplied, key=lambda item: item["history_id"])) != canonical_jsonl_bytes(
        sorted(histories, key=lambda item: item["history_id"])
    ):
        raise CorpusValidationError("sealed histories differ from re-applied review approvals")
    validate_frozen_g4_coverage(
        histories,
        family_specs=family_specs,
        assignment_manifest=assignment,
        near_duplicate_adjudication=adjudication,
        require_sealing_artifacts=True,
    )
    return manifest


def _apply_blind_review(
    histories: list[dict[str, Any]], review: dict[str, Any]
) -> list[dict[str, Any]]:
    reviewer_ids = {item["reviewer_id"] for item in review["reviewers"]}
    if len(reviewer_ids) != len(review["reviewers"]):
        raise CorpusValidationError("review record repeats a reviewer ID")
    if len(reviewer_ids) < 2:
        raise CorpusValidationError("frozen corpus review requires at least two reviewers")
    if any(item["disposition"] != "pass" for item in review["reviewers"]):
        raise CorpusValidationError("every corpus reviewer must record a pass disposition")
    if any(item["status"] == "open" for item in review["review_findings"]):
        raise CorpusValidationError("review record contains open findings")
    approvals: dict[str, dict[str, Any]] = {}
    for approval in review["history_approvals"]:
        history_id = approval["history_id"]
        if history_id in approvals:
            raise CorpusValidationError(f"duplicate review approval for {history_id}")
        if not set(approval["reviewer_ids"]) <= reviewer_ids:
            raise CorpusValidationError(f"approval for {history_id} names an unknown reviewer")
        approvals[history_id] = approval
    history_ids = {history["history_id"] for history in histories}
    if set(approvals) != history_ids:
        missing = sorted(history_ids - set(approvals))
        extra = sorted(set(approvals) - history_ids)
        raise CorpusValidationError(
            f"review approvals must exactly cover staged histories; missing={missing}, extra={extra}"
        )
    reviewed: list[dict[str, Any]] = []
    reviewed_pair_ids: set[str] = set()
    independently_second_reviewed = 0
    for source in histories:
        history = deepcopy(source)
        approval = approvals[history["history_id"]]
        if approval["disposition"] != "approved":
            raise CorpusValidationError(f"history {history['history_id']} is not approved")
        if "difficult" in history["difficulty_tags"]:
            if len(approval["reviewer_ids"]) < 2:
                raise CorpusValidationError(
                    f"difficult history {history['history_id']} requires independent second review"
                )
            independently_second_reviewed += 1
        generator = history["evaluator_only"]["generation_and_review_provenance"]["generator"]
        if generator in approval["reviewer_ids"]:
            raise CorpusValidationError(
                f"history {history['history_id']} reviewer cannot be its recorded generator"
            )
        content_hash = review_content_sha256(history)
        if approval["reviewed_content_sha256"] != content_hash:
            raise CorpusValidationError(
                f"reviewed content hash mismatch for history {history['history_id']}"
            )
        pair_ids = {pair["pair_id"] for pair in history["pair_inputs"]}
        if set(approval["reviewed_pair_ids"]) != pair_ids:
            raise CorpusValidationError(
                f"reviewed pair IDs do not match history {history['history_id']}"
            )
        overlap = reviewed_pair_ids & pair_ids
        if overlap:
            raise CorpusValidationError(f"review record repeats pair IDs: {sorted(overlap)}")
        reviewed_pair_ids.update(pair_ids)
        history["reviewer_status"] = "reviewed"
        history["evaluator_only"]["generation_and_review_provenance"][
            "reviewed_content_sha256"
        ] = content_hash
        for gold in history["evaluator_only"]["pair_gold"]:
            gold["adjudication_status"] = "agreed"
        reviewed.append(history)
    expected_pairs = (
        _FROZEN_CONFIG["split"]["families_total"]
        * _FROZEN_CONFIG["split"]["histories_per_family"]
        * _FROZEN_CONFIG["split"]["pair_opportunities_per_history"]
    )
    if len(reviewed_pair_ids) != expected_pairs:
        raise CorpusValidationError(
            f"review must cover {expected_pairs} unique pair opportunities, found {len(reviewed_pair_ids)}"
        )
    if independently_second_reviewed < 10:
        raise CorpusValidationError(
            "at least ten difficult histories require documented independent second review"
        )
    return reviewed


def seal_staged_corpus(
    staging: Path,
    review_record_path: Path,
    duplicate_adjudication_path: Path,
    output: Path,
) -> dict[str, Any]:
    """Seal a fully reviewed staged corpus into a new immutable directory."""
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing sealed path: {output}")
    staging_manifest = _verify_staging_manifest(staging)
    unresolved = set(staging_manifest.get("sealing_blockers", [])) - {
        REVIEW_BLOCKER,
        ADJUDICATION_BLOCKER,
    }
    if unresolved:
        raise CorpusValidationError(
            f"staging manifest has unresolved sealing blockers: {sorted(unresolved)}"
        )
    histories = read_jsonl(staging / "development.jsonl") + read_jsonl(staging / "holdout.jsonl")
    family_specs = read_jsonl(staging / "family-specs.jsonl")
    assignment = strict_json_loads((staging / "assignment-manifest.json").read_text(encoding="utf-8"))
    review = _load_hashed_artifact(review_record_path, REVIEW_RECORD_SCHEMA)
    duplicate_schema = ROOT / "evaluation" / "schema" / "frozen-g4-duplicate-adjudication.schema.json"
    adjudication = _load_hashed_artifact(duplicate_adjudication_path, duplicate_schema)
    reviewed = _apply_blind_review(histories, review)
    validate_frozen_g4_coverage(
        reviewed,
        family_specs=family_specs,
        assignment_manifest=assignment,
        near_duplicate_adjudication=adjudication,
        require_sealing_artifacts=True,
    )

    development = sorted(
        (item for item in reviewed if item["partition"] == "development"),
        key=lambda item: item["history_id"],
    )
    holdout = sorted(
        (item for item in reviewed if item["partition"] == "holdout"),
        key=lambda item: item["history_id"],
    )
    payloads = {
        "development.jsonl": canonical_jsonl_bytes(development),
        "holdout.jsonl": canonical_jsonl_bytes(holdout),
        "family-specs.jsonl": canonical_jsonl_bytes(family_specs),
        "assignment-manifest.json": canonical_bytes(assignment) + b"\n",
        "review-record.json": canonical_bytes(review) + b"\n",
        "near-duplicate-adjudication.json": canonical_bytes(adjudication) + b"\n",
        "staging-manifest.json": canonical_bytes(staging_manifest) + b"\n",
    }
    output.mkdir(parents=True)
    for name, content in payloads.items():
        (output / name).write_bytes(content)
    counts = {"development.jsonl": len(development), "holdout.jsonl": len(holdout),
              "family-specs.jsonl": len(family_specs)}
    manifest = {
        "manifest_version": "1",
        "state": "SEALED",
        "canonical_profile": CANONICAL_PROFILE,
        "dataset_version": _FROZEN_CONFIG["dataset_version"],
        "family_spec_registry_sha256": assignment["family_spec_registry_sha256"],
        "assignment_sha256": assignment["assignment_sha256"],
        "staging_manifest_sha256": staging_manifest["manifest_sha256"],
        "model_predictions_present": False,
        "source_files": staging_manifest["source_files"],
        "files": [{
            **file_manifest_entry(output / name, record_count=counts.get(name)),
            "path": name,
        } for name in sorted(payloads)],
    }
    manifest["manifest_sha256"] = sha256_value(manifest)
    manifest_bytes = canonical_bytes(manifest) + b"\n"
    (output / "manifest.json").write_bytes(manifest_bytes)
    (output / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_bytes)}  manifest.json\n", encoding="utf-8"
    )
    verify_sealed_corpus(output)
    return manifest
