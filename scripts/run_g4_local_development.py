from __future__ import annotations

import argparse
import json
import time
from hashlib import sha256
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, read_jsonl, sha256_value
from lifetime_ai.evaluation.contracts import PredictedRelationship
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics
from lifetime_ai.evaluation.projection import build_pair_classification_projection
from lifetime_ai.evaluation.validation import CorpusValidationError, RELATIONSHIPS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THRESHOLD = 0.95


def _authorization() -> dict[str, Any]:
    return json.loads(
        (ROOT / "evaluation" / "config" / "g4-development-authorization.json").read_text(
            encoding="utf-8"
        )
    )


def _assert_development_authorized() -> None:
    authorization = _authorization()
    if not (
        authorization.get("model_predictions_authorized")
        and authorization.get("threshold_tuning_authorized")
        and authorization.get("authorized_scope") == "development_only"
        and not authorization.get("holdout_evaluation_authorized")
    ):
        raise CorpusValidationError(
            "local G4 development run requires development-only authorization"
        )


def _feature_text(projection: dict[str, Any]) -> str:
    """Serialize only the system-visible pair projection into model features."""
    return json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _family_split(histories: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    families = sorted({history["family_id"] for history in histories})
    ranked = sorted(
        families,
        key=lambda family: sha256(f"g4-development:{family}".encode()).hexdigest(),
    )
    validation_count = max(1, round(len(ranked) * 0.2))
    validation_families = set(ranked[:validation_count])
    train = [history for history in histories if history["family_id"] not in validation_families]
    validation = [history for history in histories if history["family_id"] in validation_families]
    return train, validation


def _pairs(histories: list[dict[str, Any]]) -> list[tuple[str, str, str, str, dict[str, Any]]]:
    result = []
    for history in histories:
        gold_by_pair = {
            gold["pair_id"]: gold for gold in history["evaluator_only"]["pair_gold"]
        }
        for pair in history["pair_inputs"]:
            projection = build_pair_classification_projection(history, pair["pair_id"])
            result.append(
                (
                    history["history_id"],
                    history["family_id"],
                    pair["pair_id"],
                    pair["candidate_snapshot_id"],
                    {
                        "text": _feature_text(projection),
                        "gold": gold_by_pair[pair["pair_id"]]["semantic_relationship"],
                    },
                )
            )
    return result


def _threshold_candidates(confidences: list[float]) -> list[float]:
    return sorted({DEFAULT_THRESHOLD, *[round(value, 6) for value in confidences]}, reverse=True)


def _make_prediction(
    candidate_snapshot_id: str,
    probabilities: dict[str, float],
    threshold: float,
) -> PredictedRelationship:
    decision = max(sorted(RELATIONSHIPS), key=lambda name: (probabilities[name], name))
    confidence = probabilities[decision]
    prediction = PredictedRelationship(
        candidate_snapshot_id=candidate_snapshot_id,
        probabilities={name: str(probabilities[name]) for name in RELATIONSHIPS},
        decision=decision,
        confidence=str(confidence),
        escalate=confidence < threshold or decision == "uncertain",
    )
    prediction.validate()
    return prediction


def run(corpus: Path, *, output: Path | None = None, predictions_output: Path | None = None) -> dict[str, Any]:
    """Train and evaluate a local classifier using only the frozen development partition."""
    _assert_development_authorized()
    manifest = verify_g4_development_partition(corpus)
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed corpus must not contain model predictions")
    histories = read_jsonl(corpus / "development.jsonl")
    train_histories, validation_histories = _family_split(histories)
    train_pairs = _pairs(train_histories)
    validation_pairs = _pairs(validation_histories)

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    x_train = vectorizer.fit_transform([item[4]["text"] for item in train_pairs])
    classifier = LogisticRegression(max_iter=1000, random_state=0)
    classifier.fit(x_train, [item[4]["gold"] for item in train_pairs])

    started = time.perf_counter()
    x_validation = vectorizer.transform([item[4]["text"] for item in validation_pairs])
    raw_probabilities = classifier.predict_proba(x_validation)
    elapsed_ms = (time.perf_counter() - started) * 1000
    classes = list(classifier.classes_)
    probability_rows = []
    for index, item in enumerate(validation_pairs):
        probabilities = {name: 0.0 for name in RELATIONSHIPS}
        probabilities.update({name: float(raw_probabilities[index][column]) for column, name in enumerate(classes)})
        probability_rows.append((item, probabilities))

    candidates = _threshold_candidates(
        [max(probabilities.values()) for _, probabilities in probability_rows]
    )
    selected_threshold = DEFAULT_THRESHOLD
    selected_metrics = None
    selected_predictions: list[tuple[tuple[str, str, str, str, dict[str, Any]], PredictedRelationship]] = []
    for threshold in sorted(candidates):
        predictions = [
            (item, _make_prediction(item[3], probabilities, threshold))
            for item, probabilities in probability_rows
        ]
        metrics = summarize_g4_metrics(
            [PairEvaluation(prediction, item[4]["gold"]) for item, prediction in predictions]
        )
        if metrics.autonomous_precision is not None and metrics.autonomous_precision >= 0.95:
            if selected_metrics is None or metrics.autonomous_coverage > selected_metrics.autonomous_coverage:
                selected_threshold, selected_metrics, selected_predictions = threshold, metrics, predictions
    if selected_metrics is None:
        selected_predictions = [
            (item, _make_prediction(item[3], probabilities, DEFAULT_THRESHOLD))
            for item, probabilities in probability_rows
        ]
        selected_metrics = summarize_g4_metrics(
            [PairEvaluation(prediction, item[4]["gold"]) for item, prediction in selected_predictions]
        )

    precision_pass = (
        selected_metrics.autonomous_precision is not None
        and selected_metrics.autonomous_precision >= 0.95
    )
    coverage_pass = selected_metrics.autonomous_coverage >= 0.30
    calibration_pass = selected_metrics.expected_calibration_error <= 0.10
    result: dict[str, Any] = {
        "status": "DEVELOPMENT_COMPLETE",
        "provisional_thresholds_met_on_inner_validation": (
            precision_pass and coverage_pass and calibration_pass
        ),
        "model": "tfidf-ngram-logistic-regression",
        "partition": "development_inner_validation",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "training_family_count": len({item["family_id"] for item in train_histories}),
        "validation_family_count": len({item["family_id"] for item in validation_histories}),
        "training_pair_count": len(train_pairs),
        "validation_pair_count": len(validation_pairs),
        "selected_threshold": selected_threshold,
        "inner_validation_checks": {
            "precision_minimum_0.95": precision_pass,
            "coverage_minimum_0.30": coverage_pass,
            "expected_calibration_error_maximum_0.10": calibration_pass,
        },
        "validation_elapsed_ms": elapsed_ms,
        "feature_vocabulary_size": len(vectorizer.vocabulary_),
        "metrics": {
            "eligible_count": selected_metrics.eligible_count,
            "autonomous_count": selected_metrics.autonomous_count,
            "correct_autonomous_count": selected_metrics.correct_autonomous_count,
            "autonomous_precision": selected_metrics.autonomous_precision,
            "autonomous_coverage": selected_metrics.autonomous_coverage,
            "multiclass_brier_score": selected_metrics.multiclass_brier_score,
            "expected_calibration_error": selected_metrics.expected_calibration_error,
        },
    }
    if predictions_output:
        rows = []
        for item, prediction in selected_predictions:
            rows.append({
                "history_id": item[0],
                "pair_id": item[2],
                "candidate_snapshot_id": item[3],
                "probabilities": dict(prediction.probabilities),
                "decision": prediction.decision,
                "confidence": prediction.confidence,
                "escalate": prediction.escalate,
            })
        predictions_output.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        result["predictions_artifact_sha256"] = sha256(canonical_bytes(rows)).hexdigest()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.write_text(encoded, encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--predictions-output", type=Path)
    args = parser.parse_args()
    result = run(args.corpus, output=args.output, predictions_output=args.predictions_output)
    if not args.output:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
