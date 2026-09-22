"""Diagnose a separate local state-effect head on G4 development families.

This does not construct transitions, predict disposition, or claim autonomy.
The relationship input is an existing out-of-fold development artifact, never
training labels or a holdout prediction.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import sha256_bytes
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_grouped_development import (
    MODEL_NAME, MODEL_REVISION, Case, _cases, _folds, _minilm_features,
)
from scripts.run_g4_local_development import _assert_development_authorized


EFFECT_NAMES = sorted({
    "reinforce", "preserve_conflict", "add_scoped_item", "close_and_replace",
    "resolve", "invalidate", "expire", "none",
})
DISPOSITION_NAMES = sorted({
    "accept", "reject_unauthorized", "reject_invalid", "abstain", "no_op",
})


def _relationship_rows(path: Path, cases: list[Case], folds: list[list[int]]) -> dict[str, dict[str, Any]]:
    # Experiment outputs use ordinary JSON floats; the sealed corpus reader is
    # intentionally stricter and must not be applied to model artifacts.
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    by_pair = {row["pair_id"]: row for row in rows}
    if len(rows) != len(cases) or len(by_pair) != len(cases):
        raise CorpusValidationError("relationship artifact must cover development pairs exactly once")
    expected_fold = {cases[index].pair_id: fold_number
                     for fold_number, fold in enumerate(folds) for index in fold}
    for case in cases:
        row = by_pair.get(case.pair_id)
        if row is None or any((
            row.get("family_id") != case.family_id,
            row.get("history_id") != case.history_id,
            row.get("candidate_snapshot_id") != case.snapshot_id,
            row.get("gold_relationship") != case.gold,
            row.get("model_fold") != expected_fold[case.pair_id],
        )):
            raise CorpusValidationError("relationship artifact identity or fold mismatch")
        if row.get("decision") not in row.get("probabilities", {}):
            raise CorpusValidationError("relationship artifact has invalid decision")
        confidence = float(row["confidence"])
        if confidence != float(row["probabilities"][row["decision"]]):
            raise CorpusValidationError("relationship artifact confidence mismatch")
    return by_pair


def _effect_features(cases: list[Case]):
    import numpy as np

    semantic = _minilm_features(cases)
    authority = np.array([
        [float(case.may_assert_user_state), float(case.may_request_transition)]
        for case in cases
    ])
    return np.concatenate((semantic, authority), axis=1)


def run(corpus: Path, relationships: Path, output: Path, predictions: Path) -> dict[str, Any]:
    _assert_development_authorized()
    manifest = verify_g4_development_partition(corpus)
    cases = _cases(corpus)
    if len(cases) != 1080 or len({case.family_id for case in cases}) != 90:
        raise CorpusValidationError("unexpected development case or family count")
    if {case.gold_effect for case in cases} != set(EFFECT_NAMES):
        raise CorpusValidationError("development effect vocabulary differs from frozen schema")
    if {case.gold_disposition for case in cases} != set(DISPOSITION_NAMES):
        raise CorpusValidationError("development disposition vocabulary differs from frozen schema")
    all_indices = list(range(len(cases)))
    folds = _folds(cases, all_indices, 5, "g4-outer-v1")
    relationship_by_pair = _relationship_rows(relationships, cases, folds)
    features = _effect_features(cases)

    from sklearn.linear_model import LogisticRegression

    rows = []
    for fold_number, held_indices in enumerate(folds):
        held = set(held_indices)
        train_indices = [index for index in all_indices if index not in held]
        if {cases[index].family_id for index in train_indices} & {
            cases[index].family_id for index in held_indices
        }:
            raise CorpusValidationError("effect training and evaluation families overlap")
        classifier = LogisticRegression(max_iter=1000, random_state=0)
        classifier.fit(features[train_indices], [cases[index].gold_effect for index in train_indices])
        probabilities = classifier.predict_proba(features[held_indices])
        classes = list(classifier.classes_)
        disposition_classifier = LogisticRegression(max_iter=1000, random_state=0)
        disposition_classifier.fit(
            features[train_indices], [cases[index].gold_disposition for index in train_indices]
        )
        disposition_probabilities = disposition_classifier.predict_proba(features[held_indices])
        disposition_classes = list(disposition_classifier.classes_)
        for index, vector, disposition_vector in zip(
            held_indices, probabilities, disposition_probabilities, strict=True,
        ):
            case = cases[index]
            effect_probabilities = {
                name: float(vector[classes.index(name)]) if name in classes else 0.0
                for name in EFFECT_NAMES
            }
            effect_decision = max(EFFECT_NAMES, key=lambda name: (effect_probabilities[name], name))
            disposition_probabilities_row = {
                name: float(disposition_vector[disposition_classes.index(name)])
                if name in disposition_classes else 0.0
                for name in DISPOSITION_NAMES
            }
            disposition_decision = max(
                DISPOSITION_NAMES,
                key=lambda name: (disposition_probabilities_row[name], name),
            )
            relationship = relationship_by_pair[case.pair_id]
            relationship_gated = (
                relationship["decision"] != "uncertain"
                and float(relationship["confidence"]) >= 0.95
            )
            rows.append({
                "family_id": case.family_id,
                "history_id": case.history_id,
                "pair_id": case.pair_id,
                "model_fold": fold_number,
                "gold_relationship": case.gold,
                "gold_effect": case.gold_effect,
                "gold_disposition": case.gold_disposition,
                "relationship_decision": relationship["decision"],
                "relationship_probability_gated": relationship_gated,
                "effect_decision": effect_decision,
                "effect_confidence_uncalibrated": effect_probabilities[effect_decision],
                "effect_probabilities_uncalibrated": effect_probabilities,
                "disposition_decision": disposition_decision,
                "disposition_confidence_uncalibrated": disposition_probabilities_row[disposition_decision],
                "disposition_probabilities_uncalibrated": disposition_probabilities_row,
                "relationship_correct": relationship["decision"] in {
                    case.gold, *case.acceptable_alternatives,
                },
                "effect_correct": effect_decision == case.gold_effect,
                "disposition_correct": disposition_decision == case.gold_disposition,
            })
    if len(rows) != len(cases) or len({row["pair_id"] for row in rows}) != len(cases):
        raise CorpusValidationError("effect folds did not cover development exactly once")
    gated = [row for row in rows if row["relationship_probability_gated"]]
    confusion = {gold: dict(Counter(
        row["effect_decision"] for row in rows if row["gold_effect"] == gold
    )) for gold in EFFECT_NAMES}
    result = {
        "status": "DEVELOPMENT_DIAGNOSTIC_ONLY",
        "partition": "development_only",
        "validator_applied": False,
        "effect_confidence_calibrated": False,
        "disposition_confidence_calibrated": False,
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "relationship_artifact_sha256": sha256_bytes(relationships.read_bytes()),
        "encoder": {"name": MODEL_NAME, "revision": MODEL_REVISION},
        "protocol": "5 whole-family outer folds aligned with relationship artifact; effect head trained only on other families",
        "pair_count": len(rows),
        "effect_correct": sum(row["effect_correct"] for row in rows),
        "effect_accuracy": sum(row["effect_correct"] for row in rows) / len(rows),
        "disposition_correct": sum(row["disposition_correct"] for row in rows),
        "disposition_accuracy": sum(row["disposition_correct"] for row in rows) / len(rows),
        "effect_confusion": confusion,
        "relationship_probability_gated_pairs": len(gated),
        "relationship_correct_among_gated": sum(row["relationship_correct"] for row in gated),
        "effect_correct_among_gated": sum(row["effect_correct"] for row in gated),
        "joint_relationship_and_effect_correct_among_gated": sum(
            row["relationship_correct"] and row["effect_correct"] for row in gated
        ),
        "joint_relationship_effect_disposition_correct_among_gated": sum(
            row["relationship_correct"] and row["effect_correct"] and row["disposition_correct"]
            for row in gated
        ),
        "predictions_artifact": str(predictions),
    }
    predictions.parent.mkdir(parents=True, exist_ok=True)
    predictions.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--relationships", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.corpus, args.relationships, args.output, args.predictions)
    print(json.dumps({key: result[key] for key in (
        "status", "effect_accuracy", "relationship_probability_gated_pairs",
        "joint_relationship_and_effect_correct_among_gated",
    )}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
