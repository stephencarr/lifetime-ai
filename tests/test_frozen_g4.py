from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import json
from pathlib import Path

import pytest

from lifetime_ai.evaluation.canonical import (
    canonical_bytes,
    file_manifest_entry,
    sha256_bytes,
    sha256_value,
)
from lifetime_ai.evaluation.frozen_g4 import (
    _validate_duplicate_adjudication,
    assign_frozen_g4_families,
    frozen_g4_near_duplicate_candidates,
    frozen_history_content_sha256,
    validate_frozen_g4_coverage,
)
from lifetime_ai.evaluation.frozen_g4 import _frozen_schema_validator
from lifetime_ai.evaluation.frozen_g4_pipeline import (
    ADJUDICATION_BLOCKER,
    REVIEW_BLOCKER,
    SEALED_PAYLOAD_PATHS,
    STAGED_PAYLOAD_PATHS,
    _apply_blind_review,
    _verify_staging_manifest,
    load_blueprints,
    load_authoring_matrix,
    render_blueprint,
    seal_staged_corpus,
    stage_blueprint_registry,
    validate_blueprints_against_authoring_matrix,
    verify_sealed_corpus,
)
from lifetime_ai.evaluation.validation import (
    CorpusValidationError,
    _project_invalidated_derivatives,
    review_content_sha256,
    validate_history,
)
from scripts.generate_g3_development_pilot_v07 import _generate


def _replace_history_id(value, old: str, new: str):
    if isinstance(value, dict):
        return {key: _replace_history_id(item, old, new) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_history_id(item, old, new) for item in value]
    if isinstance(value, str):
        return value.replace(old, new)
    return value


def _materialize_structural_history(source, family_id: str, new_history_id: str):
    history = _replace_history_id(deepcopy(source), source["history_id"], new_history_id)
    history.update(
        schema_version="1",
        dataset_version="frozen-g4-v0.1",
        corpus_stage="frozen_g4",
        history_id=new_history_id,
        family_id=family_id,
        partition="development",
        reviewer_status="pending",
    )
    for pair_gold in history["evaluator_only"]["pair_gold"]:
        pair_gold["expected_state_effect"].setdefault("affected_derivative_ids", [])
        if pair_gold["expected_state_effect"]["effect"] == "none":
            pair_gold["expected_state_effect"]["affected_item_ids"] = []
    history["evaluator_only"]["generation_and_review_provenance"][
        "reviewed_content_sha256"
    ] = None
    for pool in history["candidate_pools"]:
        pool["sha256"] = sha256_value({
            "captured_after_sequence": pool["captured_after_sequence"],
            "snapshot_ids": pool["snapshot_ids"],
        })
    first_pair = history["pair_inputs"][0]
    first_event_sequence = next(
        event["sequence"] for event in history["timeline"]
        if event["event_id"] == first_pair["event_id"]
    )
    baseline_sequence = first_event_sequence - 1
    first_checkpoint = history["checkpoint_requests"][0]
    first_gold = next(
        item for item in history["evaluator_only"]["checkpoint_gold"]
        if item["checkpoint_id"] == first_checkpoint["checkpoint_id"]
    )
    baseline_id = f"{new_history_id}-baseline-checkpoint"
    baseline_request = deepcopy(first_checkpoint)
    baseline_request.update(checkpoint_id=baseline_id, after_sequence=baseline_sequence)
    baseline_gold = deepcopy(first_gold)
    baseline_gold["checkpoint_id"] = baseline_id
    eligible_events = {
        event["event_id"] for event in history["timeline"]
        if event["sequence"] <= baseline_sequence
    }
    baseline_gold["historical_assertions"] = [
        assertion for assertion in baseline_gold["historical_assertions"]
        if set(assertion["source_event_ids"]) <= eligible_events
    ]
    history["checkpoint_requests"].append(baseline_request)
    history["evaluator_only"]["checkpoint_gold"].append(baseline_gold)
    return history


def test_frozen_g4_config_matches_validator_constants():
    from lifetime_ai.evaluation import frozen_g4

    config_path = Path(__file__).resolve().parents[1] / "evaluation" / "config" / "frozen-g4-v0.1.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    split = config["split"]
    assert split["families_total"] == sum(frozen_g4.EXPECTED_FAMILY_COUNTS.values())
    assert split["development_families"] == frozen_g4.EXPECTED_FAMILY_COUNTS["development"]
    assert split["holdout_families"] == frozen_g4.EXPECTED_FAMILY_COUNTS["holdout"]
    assert split["histories_per_family"] == frozen_g4.HISTORIES_PER_FAMILY
    assert split["pair_opportunities_per_history"] == frozen_g4.PAIRS_PER_HISTORY
    assert config["coverage"]["minimum_holdout_relationship_families"] == (
        frozen_g4.MIN_HOLDOUT_FAMILIES_PER_RELATIONSHIP
    )
    coverage = config["coverage"]
    assert set(coverage["relationships"]) == frozen_g4.RELATIONSHIPS
    assert set(coverage["dispositions_per_partition"]) == frozen_g4.DISPOSITIONS
    assert set(coverage["effects_per_partition"]) == frozen_g4.EFFECTS
    assert set(coverage["actions_per_partition"]) == frozen_g4.ACTIONS
    assert set(config["split"]["partition_names"]) == frozen_g4.PARTITIONS
    assert coverage["minimum_relationship_pairs_per_partition"] == (
        frozen_g4.MIN_PAIRS_PER_RELATIONSHIP_PER_PARTITION
    )
    assert coverage["minimum_baseline_favoring_histories_total"] == (
        frozen_g4.MIN_BASELINE_FAVORING_HISTORIES
    )
    assert config["planning_assumptions"]["minimum_holdout_autonomous_accepts"] == 100


def test_frozen_g4_family_assignment_is_deterministic_and_stratified(frozen_family_specs):
    first = assign_frozen_g4_families(frozen_family_specs)
    second = assign_frozen_g4_families(deepcopy(frozen_family_specs))
    assert first == second
    counts = defaultdict(int)
    for entry in first["assignments"]:
        counts[entry["partition"]] += 1
    assert counts == {"development": 90, "holdout": 45}
    observed = defaultdict(int)
    for entry in first["assignments"]:
        if entry["partition"] == "holdout":
            for label in entry["stratification_labels"]:
                observed[label] += 1
    assert dict(sorted(observed.items())) == first["stratification_observed"]


def test_frozen_g4_family_assignment_handles_uneven_strata_and_input_order(frozen_family_specs):
    uneven = deepcopy(frozen_family_specs)
    for index, spec in enumerate(uneven):
        spec["primary_relationship"] = (
            "supports" if index < 80 else "contradicts" if index < 120 else "unrelated"
        )
    forward = assign_frozen_g4_families(uneven)
    reverse = assign_frozen_g4_families(list(reversed(uneven)))
    assert forward == reverse
    holdout = defaultdict(int)
    for entry in forward["assignments"]:
        if entry["partition"] == "holdout":
            for label in entry["stratification_labels"]:
                if label.startswith("relationship:"):
                    holdout[label] += 1
    assert holdout == {
        "relationship:supports": 27,
        "relationship:contradicts": 13,
        "relationship:unrelated": 5,
    }


def test_frozen_g4_family_assignment_binds_full_spec_and_manifest(frozen_family_specs):
    original = assign_frozen_g4_families(frozen_family_specs)
    changed_specs = deepcopy(frozen_family_specs)
    changed_specs[0]["difficulty_tags"] = ["changed-after-freeze"]
    changed = assign_frozen_g4_families(changed_specs)
    assert original["family_spec_registry_sha256"] != changed["family_spec_registry_sha256"]
    tampered_manifest = deepcopy(original)
    tampered_manifest["assignments"][0]["partition"] = (
        "holdout" if tampered_manifest["assignments"][0]["partition"] == "development"
        else "development"
    )
    assert tampered_manifest != assign_frozen_g4_families(frozen_family_specs)


def test_frozen_g4_family_spec_hashes_rendered_history_content(
    structural_frozen_corpus, frozen_family_specs
):
    histories = deepcopy(structural_frozen_corpus)
    histories[0]["timeline"][0]["content"] += " changed after family freeze"
    with pytest.raises(CorpusValidationError, match="rendered content does not match"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_near_duplicate_adjudication_requires_complete_blind_hashed_record():
    artifact = {
        "schema_version": "1",
        "blind_to_model_predictions": True,
        "similarity_method": "all-rendered-string-trigrams-jaccard-v1",
        "threshold_jaccard_milli": 900,
        "reviewed_family_pairs": [{
            "family_ids": ["family-a", "family-b"],
            "similarity_jaccard_milli": 930,
            "disposition": "distinct",
            "rationale": "The similar wording represents different meanings.",
            "reviewer_id": "reviewer-opaque-1",
            "blind_to_model_predictions": True,
        }],
    }
    artifact["artifact_sha256"] = sha256_value(artifact)
    assert _validate_duplicate_adjudication(
        artifact, {("family-a", "family-b"): 0.93}
    ) == []
    artifact["blind_to_model_predictions"] = False
    assert _validate_duplicate_adjudication(artifact, {})


def test_near_duplicate_adjudication_rejects_extra_and_unknown_pairs():
    artifact = {
        "schema_version": "1",
        "blind_to_model_predictions": True,
        "similarity_method": "all-rendered-string-trigrams-jaccard-v1",
        "threshold_jaccard_milli": 900,
        "reviewed_family_pairs": [
            {
                "family_ids": ["family-a", "family-b"],
                "similarity_jaccard_milli": 930,
                "disposition": "distinct",
                "rationale": "Similar wording, but materially different semantics.",
                "reviewer_id": "reviewer-opaque-1",
                "blind_to_model_predictions": True,
            },
            {
                "family_ids": ["unknown-x", "unknown-y"],
                "similarity_jaccard_milli": 999,
                "disposition": "distinct",
                "rationale": "This pair was not emitted by the candidate detector.",
                "reviewer_id": "reviewer-opaque-1",
                "blind_to_model_predictions": True,
            },
        ],
    }
    artifact["artifact_sha256"] = sha256_value(artifact)
    errors = _validate_duplicate_adjudication(
        artifact,
        {("family-a", "family-b"): 0.93},
        {"family-a", "family-b"},
    )
    assert any("non-candidate" in error for error in errors)
    assert any("unknown families" in error for error in errors)


def test_near_duplicate_candidate_report_is_deterministic(structural_frozen_corpus):
    forward = frozen_g4_near_duplicate_candidates(structural_frozen_corpus)
    reverse = frozen_g4_near_duplicate_candidates(list(reversed(structural_frozen_corpus)))
    assert forward == reverse
    assert forward
    assert all(record["family_ids"] == sorted(record["family_ids"]) for record in forward)


@pytest.fixture(scope="module")
def frozen_family_specs():
    pilot = _generate()
    by_family = defaultdict(list)
    for history in pilot:
        by_family[history["family_id"]].append(history)
    config_path = Path(__file__).resolve().parents[1] / "evaluation" / "config" / "frozen-g4-v0.1.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    relationship_order = config["coverage"]["relationships"]
    declared_features = set(config["coverage"]["feature_minimum_histories"])
    source_families = sorted(by_family)
    specs = []
    for index in range(1, 136):
        source_members = by_family[source_families[(index - 1) % len(source_families)]]
        relationship_counts = defaultdict(int)
        for history in source_members:
            for gold in history["evaluator_only"]["pair_gold"]:
                relationship_counts[gold["semantic_relationship"]] += 1
        primary_relationship = max(
            relationship_order,
            key=lambda label: (relationship_counts[label], -relationship_order.index(label)),
        )
        family_id = f"frozen-structure-family-{index:03d}"
        rendered_histories = [
            _materialize_structural_history(
                source, family_id,
                f"frozen-structure-history-{(index - 1) * 3 + offset:03d}",
            )
            for offset, source in enumerate(
                sorted(source_members, key=lambda item: item["history_id"]), start=1
            )
        ]
        specs.append({
            "family_id": family_id,
            "primary_relationship": primary_relationship,
            "feature_tags": sorted({tag for item in source_members for tag in item["feature_tags"]} & declared_features),
            "difficulty_tags": sorted({tag for item in source_members for tag in item["difficulty_tags"]}),
            "expected_favors": sorted({item["evaluator_only"]["expected_favors"] for item in source_members}),
            "deletion_presence": any(
                event["event_type"] in {"deletion", "redaction"}
                for item in source_members for event in item["timeline"]
            ),
            "ambiguity_presence": any(
                "genuine_ambiguity" in item["feature_tags"]
                or any(gold["semantic_relationship"] == "uncertain"
                       for gold in item["evaluator_only"]["pair_gold"])
                for item in source_members
            ),
            "rendered_histories": [
                {
                    "history_id": history["history_id"],
                    "content_sha256": frozen_history_content_sha256(history),
                }
                for history in rendered_histories
            ],
        })
    return specs


@pytest.fixture(scope="module")
def structural_frozen_corpus(frozen_family_specs):
    """Scale pilot fixtures only to exercise validator structure, never as benchmark data."""
    pilot = _generate()
    by_family = defaultdict(list)
    for history in pilot:
        by_family[history["family_id"]].append(history)
    source_families = sorted(by_family)
    assignment = assign_frozen_g4_families(frozen_family_specs)
    family_partitions = {entry["family_id"]: entry["partition"] for entry in assignment["assignments"]}
    histories = []
    for family_number, family_spec in enumerate(frozen_family_specs, start=1):
        source_family = source_families[(family_number - 1) % len(source_families)]
        family_id = family_spec["family_id"]
        for source in sorted(by_family[source_family], key=lambda item: item["history_id"]):
            new_history_id = f"frozen-structure-history-{len(histories) + 1:03d}"
            history = _materialize_structural_history(source, family_id, new_history_id)
            history["partition"] = family_partitions[family_id]
            histories.append(history)
    return histories


def _blueprint_from_rendered_family(family_spec, members):
    omitted = {
        "schema_version", "dataset_version", "corpus_stage", "family_id",
        "partition", "generation_origin", "reviewer_status",
    }
    return {
        "blueprint_version": "1",
        "family_id": family_spec["family_id"],
        "generation_origin": members[0]["generation_origin"],
        "primary_relationship": family_spec["primary_relationship"],
        "feature_tags": family_spec["feature_tags"],
        "difficulty_tags": family_spec["difficulty_tags"],
        "expected_favors": family_spec["expected_favors"],
        "deletion_presence": family_spec["deletion_presence"],
        "ambiguity_presence": family_spec["ambiguity_presence"],
        "histories": [
            {key: deepcopy(value) for key, value in history.items() if key not in omitted}
            for history in members
        ],
    }


def test_frozen_g4_blueprint_renders_bound_pending_histories(
    structural_frozen_corpus, frozen_family_specs
):
    spec = frozen_family_specs[0]
    members = [
        history for history in structural_frozen_corpus
        if history["family_id"] == spec["family_id"]
    ]
    blueprint = _blueprint_from_rendered_family(spec, members)
    rendered, rendered_spec = render_blueprint(blueprint)
    assert rendered_spec == spec
    assert {history["reviewer_status"] for history in rendered} == {"pending"}
    assert {history["partition"] for history in rendered} == {"development"}
    assert [
        frozen_history_content_sha256(history)
        for history in sorted(rendered, key=lambda item: item["history_id"])
    ] == [item["content_sha256"] for item in spec["rendered_histories"]]


def test_frozen_g4_blueprint_schema_is_closed(
    tmp_path, structural_frozen_corpus, frozen_family_specs
):
    spec = frozen_family_specs[0]
    members = [
        history for history in structural_frozen_corpus
        if history["family_id"] == spec["family_id"]
    ]
    blueprint = _blueprint_from_rendered_family(spec, members)
    blueprint["unreviewed_extension"] = True
    path = tmp_path / "family.json"
    path.write_text(json.dumps(blueprint), encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="schema violation"):
        load_blueprints(tmp_path)


def test_frozen_g4_authoring_matrix_is_hash_bound_and_registry_exact(tmp_path):
    matrix_path = (
        Path(__file__).resolve().parents[1]
        / "evaluation" / "blueprints" / "frozen-g4-v0.1" / "authoring-matrix.json"
    )
    matrix = load_authoring_matrix(matrix_path)
    with pytest.raises(CorpusValidationError, match="exactly match"):
        validate_blueprints_against_authoring_matrix([], matrix)
    tampered = deepcopy(matrix)
    tampered["families"][0]["primary_relationship"] = "uncertain"
    path = tmp_path / "tampered-matrix.json"
    path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="hash mismatch"):
        load_authoring_matrix(path)


def test_frozen_g4_stager_refuses_overwrite(tmp_path):
    output = tmp_path / "existing"
    output.mkdir()
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        stage_blueprint_registry(
            tmp_path / "missing-blueprints", tmp_path / "missing-matrix.json", output
        )


def _complete_review_record(histories):
    record = {
        "schema_version": "1",
        "blind_to_model_predictions": True,
        "reviewers": [{
            "reviewer_id": "independent-reviewer-1",
            "scope": "Every rendered history and pair opportunity.",
            "disposition": "pass",
        }, {
            "reviewer_id": "independent-reviewer-2",
            "scope": "Independent second review of difficult histories.",
            "disposition": "pass",
        }],
        "history_approvals": [{
            "history_id": history["history_id"],
            "reviewed_content_sha256": review_content_sha256(history),
            "reviewed_pair_ids": sorted(pair["pair_id"] for pair in history["pair_inputs"]),
            "reviewer_ids": (
                ["independent-reviewer-1", "independent-reviewer-2"]
                if "difficult" in history["difficulty_tags"]
                else ["independent-reviewer-1"]
            ),
            "disposition": "approved",
        } for history in histories],
        "review_findings": [],
    }
    record["artifact_sha256"] = sha256_value(record)
    return record


def test_frozen_g4_blind_review_binds_every_history_and_pair(structural_frozen_corpus):
    histories = deepcopy(structural_frozen_corpus)
    for history in histories[:10]:
        history["difficulty_tags"] = sorted({*history["difficulty_tags"], "difficult"})
    reviewed = _apply_blind_review(
        histories, _complete_review_record(histories)
    )
    assert len(reviewed) == 405
    assert {history["reviewer_status"] for history in reviewed} == {"reviewed"}
    assert all(
        history["evaluator_only"]["generation_and_review_provenance"][
            "reviewed_content_sha256"
        ] == review_content_sha256(history)
        for history in reviewed
    )
    # This pilot-derived structural fixture is intentionally invalid corpus
    # material, but its first member is sufficient to exercise the review-hash
    # contract that previously made every real reviewed history unsealable.
    validate_history(
        reviewed[0],
        schema_validator=_frozen_schema_validator(),
        expected_corpus_stage="frozen_g4",
        allowed_partitions={"development", "holdout"},
    )


def test_frozen_g4_blind_review_rejects_incomplete_coverage(structural_frozen_corpus):
    review = _complete_review_record(structural_frozen_corpus)
    review["history_approvals"].pop()
    with pytest.raises(CorpusValidationError, match="exactly cover"):
        _apply_blind_review(structural_frozen_corpus, review)


def test_frozen_g4_sealer_refuses_overwrite(tmp_path):
    output = tmp_path / "existing-seal"
    output.mkdir()
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        seal_staged_corpus(
            tmp_path / "missing-stage",
            tmp_path / "missing-review.json",
            tmp_path / "missing-adjudication.json",
            output,
        )


def _write_payloads(directory: Path, names: set[str]) -> None:
    directory.mkdir()
    for name in names:
        content = b"{}\n" if name.endswith(".jsonl") else b"{}\n"
        (directory / name).write_bytes(content)


def _write_directory_manifest(
    directory: Path,
    *,
    state: str,
    payload_names: set[str],
    source_files=None,
    **extra,
):
    files = []
    for name in sorted(payload_names):
        entry = file_manifest_entry(directory / name)
        entry["path"] = name
        if name.endswith(".jsonl"):
            entry["record_count"] = 1
        files.append(entry)
    manifest = {
        "manifest_version": "1",
        "state": state,
        "files": files,
        "source_files": [] if source_files is None else source_files,
        **extra,
    }
    manifest["manifest_sha256"] = sha256_value(manifest)
    content = canonical_bytes(manifest) + b"\n"
    (directory / "manifest.json").write_bytes(content)
    (directory / "manifest.sha256").write_text(
        f"{sha256_bytes(content)}  manifest.json\n", encoding="utf-8"
    )
    return manifest


def test_staging_manifest_recounts_jsonl_and_rejects_unknown_files(tmp_path):
    staging = tmp_path / "staging"
    _write_payloads(staging, STAGED_PAYLOAD_PATHS)
    _write_directory_manifest(
        staging,
        state="STAGED_NOT_SEALED",
        payload_names=STAGED_PAYLOAD_PATHS,
        sealing_blockers=[REVIEW_BLOCKER, ADJUDICATION_BLOCKER],
    )
    assert _verify_staging_manifest(staging)["state"] == "STAGED_NOT_SEALED"

    (staging / "unexpected-model-output.txt").write_text("unexpected", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="unknown or unmanifested"):
        _verify_staging_manifest(staging)
    (staging / "unexpected-model-output.txt").unlink()

    manifest = json.loads((staging / "manifest.json").read_text(encoding="utf-8"))
    jsonl_entry = next(item for item in manifest["files"] if item["path"].endswith(".jsonl"))
    jsonl_entry["record_count"] = 2
    manifest.pop("manifest_sha256")
    manifest["manifest_sha256"] = sha256_value(manifest)
    content = canonical_bytes(manifest) + b"\n"
    (staging / "manifest.json").write_bytes(content)
    (staging / "manifest.sha256").write_text(
        f"{sha256_bytes(content)}  manifest.json\n", encoding="utf-8"
    )
    with pytest.raises(CorpusValidationError, match="record_count"):
        _verify_staging_manifest(staging)


def test_sealer_rejects_non_artifact_staging_blockers(tmp_path):
    staging = tmp_path / "staging-blocked"
    _write_payloads(staging, STAGED_PAYLOAD_PATHS)
    _write_directory_manifest(
        staging,
        state="STAGED_NOT_SEALED",
        payload_names=STAGED_PAYLOAD_PATHS,
        sealing_blockers=[
            REVIEW_BLOCKER,
            ADJUDICATION_BLOCKER,
            "family specification registry hash is not pinned in frozen config",
        ],
    )
    with pytest.raises(CorpusValidationError, match="unresolved sealing blockers"):
        seal_staged_corpus(
            staging,
            tmp_path / "unused-review.json",
            tmp_path / "unused-adjudication.json",
            tmp_path / "sealed",
        )


def test_verify_sealed_corpus_checks_staging_link_and_sources(tmp_path):
    sealed = tmp_path / "sealed"
    _write_payloads(sealed, SEALED_PAYLOAD_PATHS)
    embedded = {
        "manifest_version": "1",
        "state": "STAGED_NOT_SEALED",
        "source_files": [],
    }
    embedded["manifest_sha256"] = sha256_value(embedded)
    (sealed / "staging-manifest.json").write_bytes(canonical_bytes(embedded) + b"\n")
    manifest = _write_directory_manifest(
        sealed,
        state="SEALED",
        payload_names=SEALED_PAYLOAD_PATHS,
        staging_manifest_sha256=embedded["manifest_sha256"],
    )
    assert verify_sealed_corpus(sealed) == manifest

    manifest.pop("manifest_sha256")
    manifest["staging_manifest_sha256"] = "0" * 64
    manifest["manifest_sha256"] = sha256_value(manifest)
    content = canonical_bytes(manifest) + b"\n"
    (sealed / "manifest.json").write_bytes(content)
    (sealed / "manifest.sha256").write_text(
        f"{sha256_bytes(content)}  manifest.json\n", encoding="utf-8"
    )
    with pytest.raises(CorpusValidationError, match="staging link"):
        verify_sealed_corpus(sealed)


def test_frozen_g4_rejects_relabelled_pilot_family_clones(
    structural_frozen_corpus, frozen_family_specs
):
    # Repeated pilot content is a deliberately invalid fixture, not benchmark data.
    with pytest.raises(CorpusValidationError, match="identical normalized .* content"):
        validate_frozen_g4_coverage(
            structural_frozen_corpus,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_global_pair_id_reuse(structural_frozen_corpus, frozen_family_specs):
    histories = deepcopy(structural_frozen_corpus)
    duplicate_id = histories[0]["pair_inputs"][0]["pair_id"]
    original_id = histories[1]["pair_inputs"][0]["pair_id"]
    histories[1] = _replace_history_id(histories[1], original_id, duplicate_id)
    with pytest.raises(CorpusValidationError, match="globally unique"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_global_event_id_reuse(structural_frozen_corpus, frozen_family_specs):
    histories = deepcopy(structural_frozen_corpus)
    duplicate_id = histories[0]["timeline"][0]["event_id"]
    original_id = histories[1]["timeline"][0]["event_id"]
    histories[1] = _replace_history_id(histories[1], original_id, duplicate_id)
    with pytest.raises(CorpusValidationError, match="event IDs must be globally unique"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_partition_not_in_assignment_manifest(
    structural_frozen_corpus, frozen_family_specs
):
    histories = deepcopy(structural_frozen_corpus)
    first_family = histories[0]["family_id"]
    wrong_partition = "holdout" if histories[0]["partition"] == "development" else "development"
    for history in histories:
        if history["family_id"] == first_family:
            history["partition"] = wrong_partition
    with pytest.raises(CorpusValidationError, match="deterministic assignment"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_incomplete_holdout_relationship_coverage(
    structural_frozen_corpus, frozen_family_specs,
):
    histories = deepcopy(structural_frozen_corpus)
    for history in histories:
        if history["partition"] != "holdout":
            continue
        for gold in history["evaluator_only"]["pair_gold"]:
            if gold["semantic_relationship"] == "unrelated":
                gold["semantic_relationship"] = "supports"
    with pytest.raises(CorpusValidationError, match="holdout relationship"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_pair_candidate_item_snapshot_mismatch(structural_frozen_corpus):
    history = deepcopy(structural_frozen_corpus[0])
    history["pair_inputs"][0]["candidate_item_id"] = "wrong-item"
    with pytest.raises(CorpusValidationError, match="candidate_item_id"):
        validate_history(
            history,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )


def test_frozen_g4_semantic_task_cannot_omit_current_state_gold(structural_frozen_corpus):
    history = deepcopy(structural_frozen_corpus[0])
    semantic_task = next(
        task for task in history["downstream_tasks"]
        if task["target_scope"]["mode"] == "semantic_items"
    )
    gold = next(
        item for item in history["evaluator_only"]["downstream_task_gold"]
        if item["task_id"] == semantic_task["task_id"]
    )
    gold["gold_response"] = {}
    for pair_gold in history["evaluator_only"]["pair_gold"]:
        if pair_gold["expected_state_effect"]["effect"] == "none":
            pair_gold["expected_state_effect"]["affected_item_ids"] = []
    with pytest.raises(CorpusValidationError, match="declared response fields"):
        validate_history(
            history,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )


def test_frozen_g4_malformed_record_returns_corpus_error(
    structural_frozen_corpus, frozen_family_specs
):
    histories = deepcopy(structural_frozen_corpus)
    del histories[0]["feature_tags"]
    with pytest.raises(CorpusValidationError, match="schema violation"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_state_effect_requires_affected_items(structural_frozen_corpus):
    for original in structural_frozen_corpus:
        for gold in original["evaluator_only"]["pair_gold"]:
            if gold["expected_state_effect"]["effect"] == "none":
                continue
            history = deepcopy(original)
            mutated_gold = next(
                item for item in history["evaluator_only"]["pair_gold"]
                if item["pair_id"] == gold["pair_id"]
            )
            mutated_gold["expected_state_effect"]["affected_item_ids"] = []
            try:
                validate_history(
                    history,
                    schema_validator=_frozen_schema_validator(),
                    expected_corpus_stage="frozen_g4",
                    allowed_partitions={"development", "holdout"},
                )
            except CorpusValidationError as exc:
                if "requires affected_item_ids" in str(exc):
                    return
    pytest.fail("no nontrivial state effect rejected an empty affected_item_ids list")


def test_frozen_g4_action_gold_matches_pair_action(structural_frozen_corpus):
    for original in structural_frozen_corpus:
        for task in original["downstream_tasks"]:
            if task["task_type"] != "action_selection":
                continue
            history = deepcopy(original)
            for item in history["evaluator_only"]["pair_gold"]:
                if item["expected_state_effect"]["effect"] == "none":
                    item["expected_state_effect"]["affected_item_ids"] = []
            task_gold = next(
                item for item in history["evaluator_only"]["downstream_task_gold"]
                if item["task_id"] == task["task_id"]
            )
            expected = next(
                item["expected_external_action"]
                for item in history["evaluator_only"]["pair_gold"]
                if item["pair_id"] == task["pair_id"]
            )
            task_gold["gold_response"] = {"action": expected, "unfrozen_extra": True}
            try:
                validate_history(
                    history,
                    schema_validator=_frozen_schema_validator(),
                    expected_corpus_stage="frozen_g4",
                    allowed_partitions={"development", "holdout"},
                )
            except CorpusValidationError as exc:
                if "action-selection task gold must contain only" in str(exc):
                    return
    pytest.fail("no inconsistent action-selection gold was rejected")


def test_frozen_g4_rejects_tampered_assignment_manifest(
    structural_frozen_corpus, frozen_family_specs
):
    manifest = assign_frozen_g4_families(frozen_family_specs)
    manifest["assignments"][0]["family_spec_sha256"] = "0" * 64
    with pytest.raises(CorpusValidationError, match="manifest does not match"):
        validate_frozen_g4_coverage(
            structural_frozen_corpus,
            family_specs=frozen_family_specs,
            assignment_manifest=manifest,
        )


def test_frozen_g4_requires_registry_hash_match(structural_frozen_corpus, frozen_family_specs):
    with pytest.raises(CorpusValidationError, match="registry hash does not match"):
        validate_frozen_g4_coverage(
            structural_frozen_corpus,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_staging_validation_defers_only_sealing_artifacts(
    structural_frozen_corpus, frozen_family_specs
):
    with pytest.raises(CorpusValidationError) as caught:
        validate_frozen_g4_coverage(
            structural_frozen_corpus,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
            require_sealing_artifacts=False,
        )
    message = str(caught.value)
    assert "identical normalized" in message
    assert "registry hash is not pinned" not in message
    assert "adjudication artifact is required" not in message


def test_frozen_g4_non_accepting_disposition_cannot_mutate_state(structural_frozen_corpus):
    for original in structural_frozen_corpus:
        for pair_gold in original["evaluator_only"]["pair_gold"]:
            if pair_gold["transition_disposition"] not in {
                "reject_unauthorized", "reject_invalid", "abstain", "no_op"
            }:
                continue
            history = deepcopy(original)
            for item in history["evaluator_only"]["pair_gold"]:
                if item["expected_state_effect"]["effect"] == "none":
                    item["expected_state_effect"]["affected_item_ids"] = []
            target = next(
                item for item in history["evaluator_only"]["pair_gold"]
                if item["pair_id"] == pair_gold["pair_id"]
            )
            pair_input = next(
                item for item in history["pair_inputs"] if item["pair_id"] == pair_gold["pair_id"]
            )
            target["expected_state_effect"] = {
                "effect": "reinforce",
                "affected_item_ids": [pair_input["candidate_item_id"]],
                "affected_derivative_ids": [],
                "expected_new_item_ids": [],
            }
            try:
                validate_history(
                    history,
                    schema_validator=_frozen_schema_validator(),
                    expected_corpus_stage="frozen_g4",
                    allowed_partitions={"development", "holdout"},
                )
            except CorpusValidationError as exc:
                if "non-accepting disposition cannot mutate" in str(exc):
                    return
    pytest.fail("no non-accepting disposition rejected a mutating state effect")


def test_frozen_g4_deletion_response_requires_derivative_gold(structural_frozen_corpus):
    for original in structural_frozen_corpus:
        history = deepcopy(original)
        for item in history["evaluator_only"]["pair_gold"]:
            if item["expected_state_effect"]["effect"] == "none":
                item["expected_state_effect"]["affected_item_ids"] = []
        source_task = next(
            task for task in history["downstream_tasks"]
            if task["target_scope"]["mode"] == "semantic_items"
        )
        task_id = f"{source_task['task_id']}-deletion-contract"
        deletion_task = deepcopy(source_task)
        deletion_task.update(task_id=task_id, task_type="deletion_query")
        history["downstream_tasks"].append(deletion_task)
        source_gold = next(
            item for item in history["evaluator_only"]["downstream_task_gold"]
            if item["task_id"] == source_task["task_id"]
        )
        deletion_gold = deepcopy(source_gold)
        deletion_gold.update(task_id=task_id, gold_response={
            **source_gold["gold_response"], "invalidated_derivatives": []
        })
        history["evaluator_only"]["downstream_task_gold"].append(deletion_gold)
        deletion_gold["gold_response"].pop("invalidated_derivatives")
        with pytest.raises(CorpusValidationError, match="declared response fields"):
            validate_history(
                history,
                schema_validator=_frozen_schema_validator(),
                expected_corpus_stage="frozen_g4",
                allowed_partitions={"development", "holdout"},
            )
        return
    pytest.fail("synthetic corpus fixture was unexpectedly empty")


def test_frozen_g4_deletion_query_can_address_nonempty_derivative_gold():
    derivative = {
        "derivative_id": "derivative:summary:1",
        "invalidated_by_event_id": "event:delete:1",
        "reason": "Its only supporting source was deleted.",
    }
    checkpoint = {"invalidated_derivatives": [derivative]}
    assert _project_invalidated_derivatives(
        checkpoint, {"derivative:summary:1"}
    ) == [derivative]
    assert _project_invalidated_derivatives(checkpoint, set()) == []


def test_frozen_g4_allows_abstain_while_preserving_conflict(structural_frozen_corpus):
    history = deepcopy(structural_frozen_corpus[0])
    for item in history["evaluator_only"]["pair_gold"]:
        if item["expected_state_effect"]["effect"] == "none":
            item["expected_state_effect"]["affected_item_ids"] = []
    pair = history["pair_inputs"][0]
    pair_event_id = pair["event_id"]
    checkpoint_id = history["checkpoint_requests"][0]["checkpoint_id"]
    checkpoint = next(
        item for item in history["evaluator_only"]["checkpoint_gold"]
        if item["checkpoint_id"] == checkpoint_id
    )
    state_item = checkpoint["current_state"][0]
    target_ref = state_item["semantic_item_ref"]
    gold = next(
        item for item in history["evaluator_only"]["pair_gold"]
        if item["pair_id"] == pair["pair_id"]
    )
    gold["transition_disposition"] = "abstain"
    gold["expected_state_effect"] = {
        "effect": "preserve_conflict",
        "affected_item_ids": [target_ref],
        "affected_derivative_ids": [],
        "expected_new_item_ids": [],
    }
    for checkpoint_state in history["evaluator_only"]["checkpoint_gold"]:
        if checkpoint_state["checkpoint_id"] == history["checkpoint_requests"][-1]["checkpoint_id"]:
            continue
        for item in checkpoint_state["current_state"]:
            if item["semantic_item_ref"] == target_ref:
                item["status"] = "disputed"
                if pair_event_id not in item["counterevidence_ids"]:
                    item["counterevidence_ids"].append(pair_event_id)
    task = next(
        item for item in history["downstream_tasks"]
        if item["pair_id"] == pair["pair_id"] and item["task_type"] != "action_selection"
    )
    response = next(item for item in history["evaluator_only"]["downstream_task_gold"]
                    if item["task_id"] == task["task_id"])["gold_response"]
    next(item for item in response["current_state"]
         if item["semantic_item_ref"] == target_ref)["status"] = "disputed"
    validate_history(
        history,
        schema_validator=_frozen_schema_validator(),
        expected_corpus_stage="frozen_g4",
        allowed_partitions={"development", "holdout"},
    )


def test_frozen_g4_noop_cannot_change_derivative_state(structural_frozen_corpus):
    history = deepcopy(structural_frozen_corpus[0])
    for item in history["evaluator_only"]["pair_gold"]:
        if item["expected_state_effect"]["effect"] == "none":
            item["expected_state_effect"]["affected_item_ids"] = []
    pair = history["pair_inputs"][0]
    checkpoint = next(
        item for item in history["evaluator_only"]["checkpoint_gold"]
        if item["checkpoint_id"] == history["checkpoint_requests"][0]["checkpoint_id"]
    )
    checkpoint["invalidated_derivatives"].append({
        "derivative_id": "new-derivative",
        "invalidated_by_event_id": pair["event_id"],
        "reason": "test mutation",
    })
    with pytest.raises(CorpusValidationError, match="undeclared derivative changes"):
        validate_history(
            history,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )


def test_frozen_g4_close_and_replace_requires_active_prior_state(structural_frozen_corpus):
    history = deepcopy(structural_frozen_corpus[0])
    pair = history["pair_inputs"][0]
    pair_gold = next(item for item in history["evaluator_only"]["pair_gold"]
                     if item["pair_id"] == pair["pair_id"])
    pair_gold["expected_state_effect"] = {
        "effect": "close_and_replace",
        "affected_item_ids": ["semantic:p1:target"],
        "affected_derivative_ids": [],
        "expected_new_item_ids": ["semantic:p1:replacement"],
    }
    pair_gold["transition_disposition"] = "accept"
    event_id = pair["event_id"]
    baseline_id = history["checkpoint_requests"][-1]["checkpoint_id"]
    baseline = next(item for item in history["evaluator_only"]["checkpoint_gold"]
                    if item["checkpoint_id"] == baseline_id)
    baseline_target = next(item for item in baseline["current_state"]
                           if item["semantic_item_ref"] == "semantic:p1:target")
    baseline_target["status"] = "resolved"
    post = next(item for item in history["evaluator_only"]["checkpoint_gold"]
                if item["checkpoint_id"] == history["checkpoint_requests"][0]["checkpoint_id"])
    target = next(item for item in post["current_state"]
                  if item["semantic_item_ref"] == "semantic:p1:target")
    target["status"] = "resolved"
    replacement = deepcopy(target)
    replacement.update(
        semantic_item_ref="semantic:p1:replacement",
        proposition="A replacement semantic item with a distinct scope.",
        scope={"system": "replacement", "audience": "all"},
        status="active",
        evidence_ids=[event_id],
    )
    post["current_state"].append(replacement)
    with pytest.raises(CorpusValidationError, match="requires active prior state"):
        validate_history(
            history,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )


def test_frozen_g4_checks_runtime_identifiers_across_namespaces(
    structural_frozen_corpus, frozen_family_specs
):
    histories = deepcopy(structural_frozen_corpus)
    history = histories[0]
    history["evaluator_only"]["checkpoint_gold"][0]["historical_assertions"][0][
        "assertion_id"
    ] = history["timeline"][0]["event_id"]
    with pytest.raises(CorpusValidationError, match="globally unique across namespaces"):
        validate_frozen_g4_coverage(
            histories,
            family_specs=frozen_family_specs,
            assignment_manifest=assign_frozen_g4_families(frozen_family_specs),
        )


def test_frozen_g4_rejects_duplicate_checkpoint_runtime_ids(structural_frozen_corpus):
    original = structural_frozen_corpus[0]
    duplicated_assertion = deepcopy(original)
    assertion_checkpoint = duplicated_assertion["evaluator_only"]["checkpoint_gold"][0]
    assertions = assertion_checkpoint["historical_assertions"]
    assertions[1]["assertion_id"] = assertions[0]["assertion_id"]
    with pytest.raises(CorpusValidationError, match="duplicate assertion IDs"):
        validate_history(
            duplicated_assertion,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )

    duplicated_derivative = deepcopy(original)
    derivative_checkpoint = duplicated_derivative["evaluator_only"]["checkpoint_gold"][0]
    event_id = duplicated_derivative["timeline"][0]["event_id"]
    derivative = {
        "derivative_id": "duplicate-derivative",
        "invalidated_by_event_id": event_id,
        "reason": "duplicate-ID test",
    }
    derivative_checkpoint["invalidated_derivatives"] = [deepcopy(derivative), derivative]
    with pytest.raises(CorpusValidationError, match="duplicate derivative IDs"):
        validate_history(
            duplicated_derivative,
            schema_validator=_frozen_schema_validator(),
            expected_corpus_stage="frozen_g4",
            allowed_partitions={"development", "holdout"},
        )
