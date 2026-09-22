from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import read_jsonl
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics
from lifetime_ai.evaluation.validation import CorpusValidationError, RELATIONSHIPS
from scripts.run_g4_local_development import (
    _assert_development_authorized,
    _family_split,
    _make_prediction,
    _pairs,
    _threshold_candidates,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"


def run(corpus: Path, *, output: Path | None = None) -> dict[str, Any]:
    _assert_development_authorized()
    manifest = verify_g4_development_partition(corpus)
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed corpus must not contain model predictions")
    histories = read_jsonl(corpus / "development.jsonl")
    train_histories, validation_histories = _family_split(histories)
    train_pairs = _pairs(train_histories)
    validation_pairs = _pairs(validation_histories)

    from sentence_transformers import SentenceTransformer
    from sklearn.linear_model import LogisticRegression

    encoder = SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION, local_files_only=True)
    train_text = [item[4]["text"] for item in train_pairs]
    validation_text = [item[4]["text"] for item in validation_pairs]
    started = time.perf_counter()
    train_embeddings = encoder.encode(train_text, normalize_embeddings=True, show_progress_bar=False)
    validation_embeddings = encoder.encode(
        validation_text, normalize_embeddings=True, show_progress_bar=False
    )
    encoding_elapsed_ms = (time.perf_counter() - started) * 1000
    classifier = LogisticRegression(max_iter=1000, random_state=0)
    classifier.fit(train_embeddings, [item[4]["gold"] for item in train_pairs])
    raw_probabilities = classifier.predict_proba(validation_embeddings)
    classes = list(classifier.classes_)
    probability_rows = []
    for index, item in enumerate(validation_pairs):
        probabilities = {name: 0.0 for name in RELATIONSHIPS}
        probabilities.update(
            {name: float(raw_probabilities[index][column]) for column, name in enumerate(classes)}
        )
        probability_rows.append((item, probabilities))

    selected_threshold = 0.95
    selected_metrics = None
    for threshold in sorted(
        _threshold_candidates([max(probabilities.values()) for _, probabilities in probability_rows])
    ):
        predictions = [
            (item, _make_prediction(item[3], probabilities, threshold))
            for item, probabilities in probability_rows
        ]
        metrics = summarize_g4_metrics(
            [PairEvaluation(prediction, item[4]["gold"]) for item, prediction in predictions]
        )
        if metrics.autonomous_precision is not None and metrics.autonomous_precision >= 0.95:
            if selected_metrics is None or metrics.autonomous_coverage > selected_metrics.autonomous_coverage:
                selected_threshold, selected_metrics = threshold, metrics
    if selected_metrics is None:
        selected_threshold = 0.95
        predictions = [
            (item, _make_prediction(item[3], probabilities, selected_threshold))
            for item, probabilities in probability_rows
        ]
        selected_metrics = summarize_g4_metrics(
            [PairEvaluation(prediction, item[4]["gold"]) for item, prediction in predictions]
        )

    precision_pass = selected_metrics.autonomous_precision is not None and selected_metrics.autonomous_precision >= 0.95
    coverage_pass = selected_metrics.autonomous_coverage >= 0.30
    calibration_pass = selected_metrics.expected_calibration_error <= 0.10
    result: dict[str, Any] = {
        "status": "DEVELOPMENT_COMPLETE",
        "provisional_thresholds_met_on_inner_validation": precision_pass and coverage_pass and calibration_pass,
        "model": MODEL_NAME,
        "partition": "development_inner_validation",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "training_family_count": len({item["family_id"] for item in train_histories}),
        "validation_family_count": len({item["family_id"] for item in validation_histories}),
        "training_pair_count": len(train_pairs),
        "validation_pair_count": len(validation_pairs),
        "selected_threshold": selected_threshold,
        "encoding_elapsed_ms": encoding_elapsed_ms,
        "embedding_dimension": int(train_embeddings.shape[1]),
        "inner_validation_checks": {
            "precision_minimum_0.95": precision_pass,
            "coverage_minimum_0.30": coverage_pass,
            "expected_calibration_error_maximum_0.10": calibration_pass,
        },
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
    if output:
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.corpus, output=args.output)
    if not args.output:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
