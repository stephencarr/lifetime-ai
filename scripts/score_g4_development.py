from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import read_jsonl, sha256_bytes, strict_json_loads
from lifetime_ai.evaluation.contracts import PredictedRelationship
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics
from lifetime_ai.evaluation.validation import CorpusValidationError, RELATIONSHIPS


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION_PATH = ROOT / "evaluation" / "config" / "g4-development-authorization.json"


def _load_json(path: Path) -> dict[str, Any]:
    value = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CorpusValidationError(f"expected JSON object at {path}")
    return value


def _prediction(row: dict[str, Any]) -> tuple[PredictedRelationship, bool]:
    required = {
        "history_id", "pair_id", "candidate_snapshot_id", "probabilities",
        "decision", "confidence", "escalate",
    }
    missing = required - set(row)
    if missing:
        raise CorpusValidationError(
            f"prediction row is missing required fields: {sorted(missing)}"
        )
    probabilities = row["probabilities"]
    if not isinstance(probabilities, dict) or set(probabilities) != RELATIONSHIPS:
        raise CorpusValidationError("prediction probabilities must contain exactly six relationships")
    prediction = PredictedRelationship(
        candidate_snapshot_id=row["candidate_snapshot_id"],
        probabilities={str(key): str(value) for key, value in probabilities.items()},
        decision=row["decision"],
        confidence=str(row["confidence"]),
        escalate=row["escalate"],
    )
    try:
        prediction.validate()
    except (TypeError, ValueError, ArithmeticError) as error:
        raise CorpusValidationError(f"invalid prediction row: {error}") from error
    if not isinstance(prediction.escalate, bool):
        raise CorpusValidationError("prediction escalate must be boolean")
    if prediction.decision == "uncertain" and not prediction.escalate:
        raise CorpusValidationError("uncertain relationship must escalate")
    eligible = row.get("eligible", True)
    if not isinstance(eligible, bool):
        raise CorpusValidationError("prediction eligible must be boolean")
    return prediction, eligible


def _authorization_allows_development() -> bool:
    authorization = _load_json(AUTHORIZATION_PATH)
    return bool(
        authorization["model_predictions_authorized"]
        and authorization["threshold_tuning_authorized"]
        and authorization["authorized_scope"] == "development_only"
        and not authorization["holdout_evaluation_authorized"]
    )


def score_development(
    corpus: Path,
    predictions_path: Path,
    *,
    require_authorization: bool = True,
) -> dict[str, Any]:
    """Score a complete prediction artifact against development pairs only."""
    if require_authorization and not _authorization_allows_development():
        raise CorpusValidationError(
            "G4 model predictions and threshold tuning lack development authorization"
        )

    manifest = verify_g4_development_partition(corpus)
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed corpus must not already contain model predictions")
    development = read_jsonl(corpus / "development.jsonl")
    expected: dict[tuple[str, str], dict[str, Any]] = {}
    for history in development:
        for pair in history["pair_inputs"]:
            gold = next(
                item for item in history["evaluator_only"]["pair_gold"]
                if item["pair_id"] == pair["pair_id"]
            )
            expected[(history["history_id"], pair["pair_id"])] = {
                "candidate_snapshot_id": pair["candidate_snapshot_id"],
                "gold_relationship": gold["semantic_relationship"],
                "acceptable_alternatives": tuple(gold["acceptable_alternatives"]),
            }

    prediction_bytes = predictions_path.read_bytes()
    rows = read_jsonl(predictions_path)
    evaluations: list[PairEvaluation] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise CorpusValidationError("prediction artifact rows must be objects")
        key = (row.get("history_id"), row.get("pair_id"))
        if key not in expected:
            raise CorpusValidationError(
                f"prediction references a missing or non-development pair: {key}"
            )
        if key in seen:
            raise CorpusValidationError(f"duplicate prediction for pair: {key}")
        prediction, eligible = _prediction(row)
        expected_pair = expected[key]
        if prediction.candidate_snapshot_id != expected_pair["candidate_snapshot_id"]:
            raise CorpusValidationError(f"candidate snapshot mismatch for pair: {key}")
        seen.add(key)
        evaluations.append(
            PairEvaluation(
                prediction, expected_pair["gold_relationship"], eligible,
                expected_pair["acceptable_alternatives"],
            )
        )

    missing = set(expected) - seen
    if missing:
        raise CorpusValidationError(
            f"prediction artifact is incomplete; missing {len(missing)} development pairs"
        )
    metrics = summarize_g4_metrics(evaluations)
    return {
        "status": "DEVELOPMENT_DIAGNOSTIC_ONLY",
        "partition": "development",
        "validator_applied": False,
        "decision_rule": "artifact escalation flags; frozen 0.95 transition policy not enforced",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "prediction_artifact_sha256": sha256_bytes(prediction_bytes),
        "pair_count": len(evaluations),
        "metrics": {
            "eligible_count": metrics.eligible_count,
            "candidate_accept_count": metrics.autonomous_count,
            "correct_candidate_accept_count": metrics.correct_autonomous_count,
            "candidate_accept_precision": metrics.autonomous_precision,
            "candidate_accept_coverage": metrics.autonomous_coverage,
            "per_class_precision": dict(metrics.per_class_precision),
            "per_class_recall": dict(metrics.per_class_recall),
            "multiclass_brier_score": metrics.multiclass_brier_score,
            "expected_calibration_error": metrics.expected_calibration_error,
            "candidate_accept_precision_wilson_95": (
                {
                    "lower": metrics.autonomous_precision_wilson_95.lower,
                    "upper": metrics.autonomous_precision_wilson_95.upper,
                }
                if metrics.autonomous_precision_wilson_95
                else None
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = score_development(args.corpus, args.predictions)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
