from __future__ import annotations

import json
import hashlib
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .canonical import sha256_value
from .validation import CorpusValidationError, validate_history


def _config() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[2] / "evaluation" / "config" / "frozen-g4-v0.1.json"
    return json.loads(path.read_text(encoding="utf-8"))


_FROZEN_CONFIG = _config()
_COVERAGE_CONFIG = _FROZEN_CONFIG["coverage"]
_SPLIT_CONFIG = _FROZEN_CONFIG["split"]
RELATIONSHIPS = set(_COVERAGE_CONFIG["relationships"])
DISPOSITIONS = set(_COVERAGE_CONFIG["dispositions_per_partition"])
EFFECTS = set(_COVERAGE_CONFIG["effects_per_partition"])
ACTIONS = set(_COVERAGE_CONFIG["actions_per_partition"])
PARTITIONS = set(_SPLIT_CONFIG["partition_names"])
EXPECTED_HISTORY_COUNT = _SPLIT_CONFIG["families_total"] * _SPLIT_CONFIG["histories_per_family"]
EXPECTED_FAMILY_COUNTS = {
    "development": _SPLIT_CONFIG["development_families"],
    "holdout": _SPLIT_CONFIG["holdout_families"],
}
HISTORIES_PER_FAMILY = _SPLIT_CONFIG["histories_per_family"]
PAIRS_PER_HISTORY = _SPLIT_CONFIG["pair_opportunities_per_history"]
MIN_PAIRS_PER_RELATIONSHIP_PER_PARTITION = _COVERAGE_CONFIG[
    "minimum_relationship_pairs_per_partition"
]
MIN_HOLDOUT_FAMILIES_PER_RELATIONSHIP = _COVERAGE_CONFIG[
    "minimum_holdout_relationship_families"
]
MIN_BASELINE_FAVORING_HISTORIES = _COVERAGE_CONFIG[
    "minimum_baseline_favoring_histories_total"
]


def frozen_g4_near_duplicate_candidates(
    histories: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return deterministic cross-family candidates for blind adjudication."""
    family_histories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for history in histories:
        family_histories[history["family_id"]].append(history)
    family_features = {
        family_id: _family_text_features(members)
        for family_id, members in family_histories.items()
    }
    threshold = _FROZEN_CONFIG["family_integrity"][
        "near_duplicate_review_threshold_jaccard"
    ]
    minimum_tokens = _FROZEN_CONFIG["family_integrity"][
        "near_duplicate_minimum_tokens"
    ]
    records: list[dict[str, Any]] = []
    family_ids = sorted(family_features)
    for index, left in enumerate(family_ids):
        for right in family_ids[index + 1:]:
            left_tokens, left_shingles = family_features[left]
            right_tokens, right_shingles = family_features[right]
            union = left_shingles | right_shingles
            if min(len(left_tokens), len(right_tokens)) < minimum_tokens or not union:
                continue
            similarity = len(left_shingles & right_shingles) / len(union)
            if similarity >= threshold:
                records.append({
                    "family_ids": [left, right],
                    "similarity_jaccard_milli": round(similarity * 1000),
                })
    return records


def _family_text_features(members: list[dict[str, Any]]) -> tuple[list[str], set[tuple[str, ...]]]:
    excluded_keys = {
        "schema_version", "dataset_version", "corpus_stage", "history_id", "family_id",
        "partition", "generation_origin", "reviewer_status", "generation_and_review_provenance",
    }
    ignored_key_suffixes = ("_id", "_ids", "_sha256", "_at", "_sequence", "_status")
    texts: list[str] = []

    def collect(value: Any, key: str = "") -> None:
        if key in excluded_keys or key.endswith(ignored_key_suffixes):
            return
        if isinstance(value, dict):
            for child_key, child_value in sorted(value.items()):
                collect(child_value, child_key)
        elif isinstance(value, list):
            for child in value:
                collect(child, key)
        elif isinstance(value, str):
            # Remove embedded generated IDs and timestamps from otherwise meaningful prose.
            normalized = re.sub(r"\b(?:[a-z][a-z0-9_-]*-){1,}[a-z0-9_-]+\b", " ", value.casefold())
            normalized = re.sub(r"\b\d{4}-\d\d-\d\d(?:t\S+)?\b", " ", normalized)
            texts.append(normalized)

    for history in sorted(members, key=lambda item: item["history_id"]):
        collect(history)
    tokens = [token for text in texts for token in re.findall(r"[a-z0-9]+", text)]
    shingles = {tuple(tokens[index:index + 3]) for index in range(max(0, len(tokens) - 2))}
    return tokens, shingles


def frozen_history_content_sha256(history: dict[str, Any]) -> str:
    """Hash rendered semantic content, excluding only assignment/review metadata."""
    metadata_fields = {
        "schema_version", "dataset_version", "corpus_stage", "history_id",
        "family_id", "partition", "generation_origin", "reviewer_status",
    }
    content = {key: value for key, value in history.items() if key not in metadata_fields}
    evaluator_only = dict(content["evaluator_only"])
    evaluator_only.pop("generation_and_review_provenance", None)
    evaluator_only["pair_gold"] = [
        {
            key: value
            for key, value in gold.items()
            if key not in {"adjudication_status", "adjudication_notes"}
        }
        for gold in evaluator_only["pair_gold"]
    ]
    content["evaluator_only"] = evaluator_only
    return sha256_value(content)


def _normalized_duplicate_content(value: Any, key: str = "") -> Any:
    if key in {
        "schema_version", "dataset_version", "corpus_stage", "history_id", "family_id",
        "partition", "generation_origin", "reviewer_status", "generation_and_review_provenance",
    } or key.endswith(("_id", "_ids", "_sha256", "_at", "_sequence", "_status")):
        return None
    if isinstance(value, dict):
        return {
            child_key: normalized
            for child_key, child_value in value.items()
            if (normalized := _normalized_duplicate_content(child_value, child_key)) is not None
        }
    if isinstance(value, list):
        return [
            normalized for child in value
            if (normalized := _normalized_duplicate_content(child, key)) is not None
        ]
    if isinstance(value, str):
        text_value = re.sub(
            r"\b[a-z][a-z0-9_-]*-\d{2,}(?:-[a-z0-9_-]+)*\b", "<id>", value.casefold()
        )
        return " ".join(text_value.split())
    return value


def assign_frozen_g4_families(
    family_specs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create the frozen seeded, stratified, whole-family split manifest.

    Family labels cover relationship, feature, difficulty, expected-favor,
    deletion-presence, and ambiguity-presence marginals. A deterministic
    rare-label greedy assignment targets each label's rounded holdout share,
    breaking ties with a seed+spec-hash rank.
    """
    config = _FROZEN_CONFIG
    split = config["split"]
    expected_total = split["families_total"]
    if len(family_specs) != expected_total:
        raise CorpusValidationError(
            f"expected {expected_total} family specs, found {len(family_specs)}")
    schema_path = Path(__file__).resolve().parents[2] / "evaluation" / "schema" / "frozen-g4-family-spec.schema.json"
    family_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema_validator = Draft202012Validator(family_schema)
    allowed_features = set(config["coverage"]["feature_minimum_histories"])
    indexed: dict[str, dict[str, Any]] = {}
    for spec in family_specs:
        schema_errors = list(schema_validator.iter_errors(spec))
        if schema_errors:
            first = schema_errors[0]
            raise CorpusValidationError(f"family spec schema violation: {first.message}")
        family_id = spec.get("family_id")
        if not set(spec["feature_tags"]) <= allowed_features:
            raise CorpusValidationError(f"family {family_id!r} has undeclared feature tags")
        if family_id in indexed:
            raise CorpusValidationError(f"duplicate family spec id: {family_id}")
        indexed[family_id] = spec

    holdout_total = split["holdout_families"]
    seed = split["random_seed"] if "random_seed" in split else config["random_seed"]
    labels_by_family = {
        family_id: {
            f"relationship:{spec['primary_relationship']}",
            *(f"feature:{tag}" for tag in spec["feature_tags"]),
            *(f"difficulty:{tag}" for tag in spec["difficulty_tags"]),
            *(f"expected_favors:{value}" for value in spec["expected_favors"]),
            f"deletion_presence:{str(spec['deletion_presence']).lower()}",
            f"ambiguity_presence:{str(spec['ambiguity_presence']).lower()}",
        }
        for family_id, spec in indexed.items()
    }
    label_family_counts = Counter(label for labels in labels_by_family.values() for label in labels)
    label_targets = {
        label: (count * holdout_total + expected_total // 2) // expected_total
        for label, count in label_family_counts.items()
    }
    seed_rank = {
        family_id: sha256_value({
            "seed": seed,
            "family_id": family_id,
            "stratification_label_sha256": sha256_value(sorted(labels_by_family[family_id])),
        })
        for family_id in indexed
    }
    selected: set[str] = set()
    selected_label_counts: Counter[str] = Counter()
    while len(selected) < holdout_total:
        remaining = set(indexed) - selected

        def selection_key(family_id: str) -> tuple[float, str]:
            score = 0.0
            for label in sorted(labels_by_family[family_id]):
                count = label_family_counts[label]
                deficit = label_targets[label] - selected_label_counts[label]
                score += (1.0 if deficit > 0 else -1.0) / count
            return score, "".join(chr(255 - ord(char)) for char in seed_rank[family_id])

        chosen = max(remaining, key=selection_key)
        selected.add(chosen)
        selected_label_counts.update(labels_by_family[chosen])
    # Greedy construction can leave correlated strata imbalanced. Improve it
    # with deterministic one-for-one swaps while preserving exact holdout size.
    label_weights = {label: 1 / max(count, 1) for label, count in label_family_counts.items()}
    def balance_loss(counts: Counter[str]) -> float:
        return sum(
            label_weights[label] * (counts[label] - target) ** 2
            for label, target in label_targets.items()
        )
    while True:
        current_loss = balance_loss(selected_label_counts)
        best_swap: tuple[float, str, str, Counter[str]] | None = None
        for leaving in sorted(selected, key=lambda item: seed_rank[item]):
            for entering in sorted(set(indexed) - selected, key=lambda item: seed_rank[item]):
                proposed = selected_label_counts.copy()
                proposed.subtract(labels_by_family[leaving])
                proposed.update(labels_by_family[entering])
                loss = balance_loss(proposed)
                if loss < current_loss - 1e-12:
                    candidate = (loss, seed_rank[leaving], seed_rank[entering], proposed)
                    if best_swap is None or candidate[:3] < best_swap[:3]:
                        best_swap = candidate
        if best_swap is None:
            break
        _, leaving_rank, entering_rank, selected_label_counts = best_swap
        leaving = next(family_id for family_id, rank in seed_rank.items() if rank == leaving_rank)
        entering = next(family_id for family_id, rank in seed_rank.items() if rank == entering_rank)
        selected.remove(leaving)
        selected.add(entering)
    assignments = {
        family_id: "holdout" if family_id in selected else "development"
        for family_id in indexed
    }
    dimension_tolerances = split["maximum_holdout_count_deviation_by_dimension"]
    stratification_deviations = {
        label: selected_label_counts[label] - target
        for label, target in label_targets.items()
    }
    for label, deviation in stratification_deviations.items():
        dimension = label.split(":", 1)[0]
        tolerance = dimension_tolerances[dimension]
        if abs(deviation) > tolerance:
            raise CorpusValidationError(
                f"holdout stratum {label!r} deviates from target by {deviation}; "
                f"allowed deviation is +/-{tolerance}")
    records = [
        {
            "family_id": family_id,
            "stratification_labels": sorted(labels_by_family[family_id]),
            "partition": assignments[family_id],
            "family_spec_sha256": sha256_value(indexed[family_id]),
        }
        for family_id in sorted(indexed)
    ]
    if Counter(assignments.values()) != Counter({
        "development": split["development_families"],
        "holdout": split["holdout_families"],
    }):
        raise CorpusValidationError("stratified split failed configured family totals")
    config_path = Path(__file__).resolve().parents[2] / "evaluation" / "config" / "frozen-g4-v0.1.json"
    registry_hash = sha256_value([indexed[family_id] for family_id in sorted(indexed)])
    manifest = {
        "algorithm": split["algorithm"],
        "seed": seed,
        "family_spec_registry_sha256": registry_hash,
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "stratification_targets": dict(sorted(label_targets.items())),
        "stratification_observed": dict(sorted(selected_label_counts.items())),
        "stratification_deviations": dict(sorted(stratification_deviations.items())),
        "assignments": records,
    }
    manifest["assignment_sha256"] = sha256_value(manifest)
    return manifest


@lru_cache(maxsize=1)
def _frozen_schema_validator() -> Draft202012Validator:
    schema_root = Path(__file__).resolve().parents[2] / "evaluation" / "schema"
    schemas = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(schema_root.glob("*.schema.json"))
    ]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    frozen_schema = next(
        schema
        for schema in schemas
        if schema["$id"].endswith("frozen-g4-history-v1.json")
    )
    return Draft202012Validator(frozen_schema, registry=registry)


def _validate_histories(histories: list[dict[str, Any]]) -> None:
    validator = _frozen_schema_validator()
    for history in histories:
        validate_history(
            history,
            schema_validator=validator,
            expected_corpus_stage="frozen_g4",
            allowed_partitions=PARTITIONS,
        )


def _validate_duplicate_adjudication(
    artifact: dict[str, Any] | None,
    candidates: dict[tuple[str, str], float],
    known_family_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if artifact is None:
        return ["a blind near-duplicate adjudication artifact is required"]
    schema_path = Path(__file__).resolve().parents[2] / "evaluation" / "schema" / "frozen-g4-duplicate-adjudication.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema_errors = list(Draft202012Validator(schema).iter_errors(artifact))
    if schema_errors:
        return [f"near-duplicate adjudication schema violation: {schema_errors[0].message}"]
    expected_threshold = _FROZEN_CONFIG["family_integrity"]["near_duplicate_review_threshold_jaccard"]
    expected_threshold_milli = round(expected_threshold * 1000)
    if artifact["threshold_jaccard_milli"] != expected_threshold_milli:
        errors.append("near-duplicate adjudication threshold differs from frozen config")
    hash_material = {key: value for key, value in artifact.items() if key != "artifact_sha256"}
    if artifact["artifact_sha256"] != sha256_value(hash_material):
        errors.append("near-duplicate adjudication artifact hash mismatch")
    records: dict[tuple[str, str], dict[str, Any]] = {}
    known = known_family_ids or {
        family_id for pair in candidates for family_id in pair
    }
    for record in artifact["reviewed_family_pairs"]:
        pair = tuple(sorted(record["family_ids"]))
        if pair in records:
            errors.append(f"near-duplicate adjudication repeats family pair {pair}")
        records[pair] = record
        unknown = set(pair) - known
        if unknown:
            errors.append(
                f"near-duplicate adjudication names unknown families: {sorted(unknown)}"
            )
        if record["disposition"] != "distinct":
            errors.append(f"near-duplicate adjudication marks family pair {pair} as duplicate")
    extra_pairs = set(records) - set(candidates)
    if extra_pairs:
        errors.append(
            "near-duplicate adjudication contains non-candidate family pairs: "
            f"{sorted(extra_pairs)}"
        )
    for pair, similarity in candidates.items():
        record = records.get(pair)
        if record is None:
            errors.append(f"near-duplicate candidate {pair} lacks a blind adjudication")
        elif record["similarity_jaccard_milli"] != round(similarity * 1000):
            errors.append(f"near-duplicate adjudication similarity differs for {pair}")
    return errors


def _require_targets_in_both_partitions(
    observed: dict[str, set[str]],
    required: set[str],
    label: str,
    errors: list[str],
) -> None:
    for target in sorted(required):
        partitions = observed.get(target, set())
        if partitions != PARTITIONS:
            errors.append(
                f"{label} {target!r} must appear in both partitions; "
                f"found {sorted(partitions)}"
            )


def validate_frozen_g4_coverage(
    histories: list[dict[str, Any]],
    *,
    family_specs: list[dict[str, Any]],
    assignment_manifest: dict[str, Any],
    near_duplicate_adjudication: dict[str, Any] | None = None,
    require_sealing_artifacts: bool = True,
) -> None:
    """Validate the approved frozen-G4 corpus size, split, and target coverage.

    Staging uses ``require_sealing_artifacts=False`` so substantive corpus
    validation can run before blind review and the registry pin exist. The
    default remains fail-closed for any freeze/seal decision.
    """

    errors: list[str] = []
    validator = _frozen_schema_validator()
    structurally_valid_histories: list[dict[str, Any]] = []
    for history in histories:
        history_id = history.get("history_id", "<unknown>") if isinstance(history, dict) else "<unknown>"
        schema_errors = sorted(validator.iter_errors(history), key=lambda item: list(item.path))
        if schema_errors:
            first = schema_errors[0]
            location = ".".join(str(part) for part in first.path) or "$"
            errors.append(
                f"history {history_id}: schema violation at {location}: {first.message}"
            )
            continue
        structurally_valid_histories.append(history)
        try:
            validate_history(
                history,
                schema_validator=validator,
                expected_corpus_stage="frozen_g4",
                allowed_partitions=PARTITIONS,
            )
        except CorpusValidationError as exc:
            errors.append(f"history {history_id}: {exc}")
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(
                f"history {history_id}: malformed semantic reference: {exc}"
            )
    histories = structurally_valid_histories
    config = _FROZEN_CONFIG
    expected_manifest = assign_frozen_g4_families(family_specs)
    if assignment_manifest != expected_manifest:
        errors.append("family assignment manifest does not match frozen specs/config/seed")
    expected_registry_hash = config["family_integrity"]["expected_family_spec_registry_sha256"]
    if require_sealing_artifacts:
        if expected_registry_hash is None:
            errors.append("family specification registry hash is not pinned in the freeze config")
        elif expected_manifest["family_spec_registry_sha256"] != expected_registry_hash:
            errors.append("family specification registry hash does not match the pinned freeze config")
    assigned_partition = {
        record["family_id"]: record["partition"]
        for record in expected_manifest["assignments"]
    }

    if len(histories) != EXPECTED_HISTORY_COUNT:
        errors.append(
            f"expected {EXPECTED_HISTORY_COUNT} histories, found {len(histories)}"
        )

    history_ids = [history["history_id"] for history in histories]
    duplicate_history_ids = sorted(
        history_id
        for history_id, count in Counter(history_ids).items()
        if count > 1
    )
    if duplicate_history_ids:
        errors.append(f"duplicate history IDs: {duplicate_history_ids}")

    family_histories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    family_partitions: dict[str, set[str]] = defaultdict(set)
    partition_history_counts: Counter[str] = Counter()
    global_pair_ids: Counter[str] = Counter()
    global_entity_ids: dict[str, Counter[str]] = defaultdict(Counter)
    all_entity_ids: Counter[str] = Counter()
    for history in histories:
        family = history["family_id"]
        partition = history["partition"]
        family_histories[family].append(history)
        family_partitions[family].add(partition)
        partition_history_counts[partition] += 1
        for namespace, records, key in (
            ("event", history["timeline"], "event_id"),
            ("snapshot", history["candidate_snapshots"], "snapshot_id"),
            ("candidate pool", history["candidate_pools"], "candidate_pool_id"),
            ("pair", history["pair_inputs"], "pair_id"),
            ("checkpoint", history["checkpoint_requests"], "checkpoint_id"),
            ("downstream task", history["downstream_tasks"], "task_id"),
        ):
            identities = [item[key] for item in records]
            global_entity_ids[namespace].update(identities)
            all_entity_ids.update(identities)
        runtime_id_namespaces = {
            "assertion": {
            assertion["assertion_id"]
            for checkpoint in history["evaluator_only"]["checkpoint_gold"]
            for assertion in checkpoint["historical_assertions"]
            },
            "derivative": {
            derivative["derivative_id"]
            for checkpoint in history["evaluator_only"]["checkpoint_gold"]
            for derivative in checkpoint["invalidated_derivatives"]
            },
            "semantic item": {
            item["semantic_item_ref"]
            for checkpoint in history["evaluator_only"]["checkpoint_gold"]
            for item in checkpoint["current_state"]
            },
        }
        for namespace, identities in runtime_id_namespaces.items():
            global_entity_ids[namespace].update(identities)
            all_entity_ids.update(identities)

        pair_count = len(history["pair_inputs"])
        if pair_count != PAIRS_PER_HISTORY:
            errors.append(
                f"history {history['history_id']} must contain exactly "
                f"{PAIRS_PER_HISTORY} pair inputs, found {pair_count}"
            )
        pair_ids = [pair["pair_id"] for pair in history["pair_inputs"]]
        global_pair_ids.update(pair_ids)
        gold_ids = [gold["pair_id"] for gold in history["evaluator_only"]["pair_gold"]]
        if len(set(pair_ids)) != len(pair_ids):
            errors.append(f"history {history['history_id']} has duplicate pair input IDs")
        if len(set(gold_ids)) != len(gold_ids):
            errors.append(f"history {history['history_id']} has duplicate pair gold IDs")
        if set(pair_ids) != set(gold_ids):
            errors.append(
                f"history {history['history_id']} pair input/gold IDs do not match: "
                f"inputs={sorted(set(pair_ids))}, gold={sorted(set(gold_ids))}"
            )

    duplicate_pair_ids = sorted(
        pair_id for pair_id, count in global_pair_ids.items() if count > 1
    )
    if duplicate_pair_ids:
        errors.append(f"pair IDs must be globally unique; duplicates: {duplicate_pair_ids}")
    for namespace, counts in global_entity_ids.items():
        duplicates = sorted(identity for identity, count in counts.items() if count > 1)
        if duplicates:
            errors.append(f"{namespace} IDs must be globally unique; duplicates: {duplicates}")
    repeated_ids_across_namespaces = sorted(
        identity for identity, count in all_entity_ids.items() if count > 1
    )
    if repeated_ids_across_namespaces:
        errors.append(
            "entity IDs must be globally unique across namespaces; duplicates: "
            f"{repeated_ids_across_namespaces}"
        )

    expected_history_counts = {
        partition: family_count * HISTORIES_PER_FAMILY
        for partition, family_count in EXPECTED_FAMILY_COUNTS.items()
    }
    if partition_history_counts != Counter(expected_history_counts):
        errors.append(
            "expected development/holdout history counts "
            f"{expected_history_counts}, found {dict(partition_history_counts)}"
        )

    for family, members in sorted(family_histories.items()):
        if len(members) != HISTORIES_PER_FAMILY:
            errors.append(
                f"family {family!r} must contain exactly {HISTORIES_PER_FAMILY} "
                f"histories, found {len(members)}"
            )
        partitions = family_partitions[family]
        if len(partitions) != 1:
            errors.append(
                f"family {family!r} crosses partitions: {sorted(partitions)}"
            )
        if family not in assigned_partition:
            errors.append(f"family {family!r} is absent from the frozen assignment manifest")
        elif partitions != {assigned_partition[family]}:
            errors.append(
                f"family {family!r} partition does not match deterministic assignment "
                f"{assigned_partition[family]!r}"
            )
        spec = next((item for item in family_specs if item["family_id"] == family), None)
        if spec is not None:
            declared_content = {
                item["history_id"]: item["content_sha256"]
                for item in spec["rendered_histories"]
            }
            if len(declared_content) != len(spec["rendered_histories"]):
                errors.append(f"family {family!r} repeats a rendered history ID in its spec")
            actual_content = {
                history["history_id"]: frozen_history_content_sha256(history)
                for history in members
            }
            if declared_content != actual_content:
                errors.append(
                    f"family {family!r} rendered content does not match its predeclared content hashes")
            family_relationships = Counter(
                gold["semantic_relationship"]
                for history in members
                for gold in history["evaluator_only"]["pair_gold"]
            )
            relationship_priority = config["coverage"]["relationships"]
            derived_primary = max(
                relationship_priority,
                key=lambda label: (family_relationships[label], -relationship_priority.index(label)),
            )
            if spec["primary_relationship"] != derived_primary:
                errors.append(
                    f"family {family!r} primary_relationship does not match rendered pair-gold distribution"
                )
            rendered_features = {
                tag for history in members for tag in history["feature_tags"]
            }
            if set(spec["feature_tags"]) != rendered_features:
                errors.append(f"family {family!r} feature_tags do not match rendered histories")
            rendered_difficulty = {
                tag for history in members for tag in history["difficulty_tags"]
            }
            if set(spec["difficulty_tags"]) != rendered_difficulty:
                errors.append(f"family {family!r} difficulty_tags do not match rendered histories")
            rendered_favors = {
                history["evaluator_only"]["expected_favors"] for history in members
            }
            if set(spec["expected_favors"]) != rendered_favors:
                errors.append(f"family {family!r} expected_favors do not match rendered histories")
            rendered_deletion_presence = any(
                event["event_type"] in {"deletion", "redaction"}
                for history in members for event in history["timeline"]
            )
            if spec["deletion_presence"] != rendered_deletion_presence:
                errors.append(f"family {family!r} deletion_presence does not match rendered histories")
            rendered_ambiguity_presence = any(
                "genuine_ambiguity" in history["feature_tags"]
                or any(gold["semantic_relationship"] == "uncertain"
                       for gold in history["evaluator_only"]["pair_gold"])
                for history in members
            )
            if spec["ambiguity_presence"] != rendered_ambiguity_presence:
                errors.append(f"family {family!r} ambiguity_presence does not match rendered histories")
    extra_assigned_families = set(assigned_partition) - set(family_histories)
    if extra_assigned_families:
        errors.append(
            f"assignment manifest includes families absent from corpus: {sorted(extra_assigned_families)}"
        )

    if config["family_integrity"]["reject_exact_cross_family_content_duplicates"]:
        signatures: dict[str, str] = {}
        timeline_signatures: dict[str, str] = {}
        near_duplicate_candidates: dict[tuple[str, str], float] = {}
        for family, members in family_histories.items():
            signature = sha256_value(sorted(
                sha256_value(_normalized_duplicate_content(history)) for history in members
            ))
            timeline_signature = sha256_value(sorted(
                sha256_value([
                    [event["event_type"], _normalized_duplicate_content(event["content"])]
                    for event in history["timeline"]
                ])
                for history in members
            ))
            if signature in signatures:
                errors.append(
                    f"families {signatures[signature]!r} and {family!r} have identical normalized history content"
                )
            else:
                signatures[signature] = family
            if timeline_signature in timeline_signatures:
                errors.append(
                    f"families {timeline_signatures[timeline_signature]!r} and {family!r} "
                    "have identical normalized timeline content"
                )
            else:
                timeline_signatures[timeline_signature] = family
        for record in frozen_g4_near_duplicate_candidates(histories):
            pair = tuple(record["family_ids"])
            near_duplicate_candidates[pair] = (
                record["similarity_jaccard_milli"] / 1000
            )
        if require_sealing_artifacts:
            errors.extend(_validate_duplicate_adjudication(
                near_duplicate_adjudication,
                near_duplicate_candidates,
                set(family_histories),
            ))
    elif _FROZEN_CONFIG["review_and_sealing"].get(
        "near_duplicate_adjudication_artifact_required", False
    ) and require_sealing_artifacts:
        errors.extend(_validate_duplicate_adjudication(
            near_duplicate_adjudication, {}, set(family_histories)
        ))

    partition_families: dict[str, set[str]] = defaultdict(set)
    for family, partitions in family_partitions.items():
        for partition in partitions:
            partition_families[partition].add(family)
    actual_family_counts = {
        partition: len(partition_families.get(partition, set()))
        for partition in PARTITIONS
    }
    if actual_family_counts != EXPECTED_FAMILY_COUNTS:
        errors.append(
            f"expected family split {EXPECTED_FAMILY_COUNTS}, "
            f"found {actual_family_counts}"
        )

    relationship_partitions: dict[str, set[str]] = defaultdict(set)
    relationship_counts: dict[str, Counter[str]] = defaultdict(Counter)
    disposition_partitions: dict[str, set[str]] = defaultdict(set)
    effect_partitions: dict[str, set[str]] = defaultdict(set)
    action_partitions: dict[str, set[str]] = defaultdict(set)
    holdout_relationship_families: dict[str, set[str]] = defaultdict(set)
    baseline_favoring_counts: Counter[str] = Counter()
    feature_counts: dict[str, Counter[str]] = defaultdict(Counter)
    declared_features = set(config["coverage"]["feature_minimum_histories"])

    for history in histories:
        partition = history["partition"]
        family = history["family_id"]
        if not history["evaluator_only"].get("expected_favors_rationale"):
            errors.append(
                f"history {history['history_id']} requires expected_favors_rationale"
            )
        if history["evaluator_only"]["expected_favors"] in {"baseline_a", "baseline_b", "baseline_c"}:
            baseline_favoring_counts[partition] += 1
        undeclared_history_features = set(history["feature_tags"]) - declared_features
        if undeclared_history_features:
            errors.append(
                f"history {history['history_id']} has undeclared feature tags: {sorted(undeclared_history_features)}"
            )
        feature_counts[partition].update(set(history["feature_tags"]))
        for gold in history["evaluator_only"]["pair_gold"]:
            undeclared_pair_features = set(gold.get("feature_tags", [])) - declared_features
            if undeclared_pair_features:
                errors.append(
                    f"pair {gold['pair_id']} has undeclared feature tags: {sorted(undeclared_pair_features)}"
                )
            relationship = gold["semantic_relationship"]
            disposition = gold["transition_disposition"]
            effect = gold["expected_state_effect"]["effect"]
            action = gold["expected_external_action"]
            relationship_partitions[relationship].add(partition)
            relationship_counts[partition][relationship] += 1
            disposition_partitions[disposition].add(partition)
            effect_partitions[effect].add(partition)
            action_partitions[action].add(partition)
            if partition == "holdout":
                holdout_relationship_families[relationship].add(family)

    _require_targets_in_both_partitions(
        relationship_partitions, RELATIONSHIPS, "relationship", errors
    )
    _require_targets_in_both_partitions(
        disposition_partitions, DISPOSITIONS, "disposition", errors
    )
    _require_targets_in_both_partitions(effect_partitions, EFFECTS, "effect", errors)
    _require_targets_in_both_partitions(action_partitions, ACTIONS, "action", errors)

    for relationship in sorted(RELATIONSHIPS):
        for partition in sorted(PARTITIONS):
            pair_count = relationship_counts[partition][relationship]
            if pair_count < MIN_PAIRS_PER_RELATIONSHIP_PER_PARTITION:
                errors.append(
                    f"{partition} relationship {relationship!r} requires at least "
                    f"{MIN_PAIRS_PER_RELATIONSHIP_PER_PARTITION} pairs, "
                    f"found {pair_count}"
                )
        family_count = len(holdout_relationship_families[relationship])
        if family_count < MIN_HOLDOUT_FAMILIES_PER_RELATIONSHIP:
            errors.append(
                f"holdout relationship {relationship!r} requires at least "
                f"{MIN_HOLDOUT_FAMILIES_PER_RELATIONSHIP} distinct families, "
                f"found {family_count}"
            )

    baseline_favoring_total = sum(baseline_favoring_counts.values())
    if baseline_favoring_total < MIN_BASELINE_FAVORING_HISTORIES:
        errors.append(
            f"expected at least {MIN_BASELINE_FAVORING_HISTORIES} "
            "baseline-favoring histories, "
            f"found {baseline_favoring_total}"
        )
    missing_baseline_partitions = sorted(
        PARTITIONS - {partition for partition, count in baseline_favoring_counts.items() if count}
    ) if config["coverage"]["baseline_favoring_histories_in_each_partition"] else []
    if missing_baseline_partitions:
        errors.append(
            "baseline-favoring histories must appear in both partitions; "
            f"missing {missing_baseline_partitions}"
        )

    for feature, minimum in config["coverage"]["feature_minimum_histories"].items():
        feature_partitions = (
            sorted(PARTITIONS)
            if config["coverage"]["feature_coverage_in_each_partition"]
            else ["development"]
        )
        for partition in feature_partitions:
            count = feature_counts[partition][feature]
            if count < minimum:
                errors.append(
                    f"{partition} feature {feature!r} requires at least {minimum} "
                    f"histories, found {count}"
                )

    if errors:
        raise CorpusValidationError(
            "frozen G4 coverage validation failed: " + "; ".join(errors)
        )
