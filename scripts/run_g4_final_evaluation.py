"""Run one explicitly authorized, fixed-policy G4 POC evaluation.

This harness trains on development families only, applies the already-frozen
0.95 probability gate to holdout families, and never tunes on holdout data.
It is intentionally limited to pair-classification evidence; it does not
claim the full G4 gate until transition-validator metrics are added.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Any, Sequence

from lifetime_ai.evaluation.canonical import canonical_bytes
from lifetime_ai.evaluation.frozen_g4_pipeline import verify_sealed_corpus
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics
from lifetime_ai.evaluation.validation import CorpusValidationError
from scripts.run_g4_grouped_development import (
    MODEL_NAME,
    MODEL_REVISION,
    _cases,
    _fit_predict_minilm,
    _fit_predict_tfidf,
    _make_prediction,
    _minilm_features,
)


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION_PATH = ROOT / "evaluation/config/g4-final-run-authorization.json"
POLICY_PATH = ROOT / "evaluation/config/g4-evaluation-v0.1.json"
FIXED_THRESHOLD = 0.95


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CorpusValidationError(f"expected JSON object at {path}")
    return value


def _candidate_digest(model: str) -> str:
    spec = {
        "model": model,
        "sentence_encoder": {"name": MODEL_NAME, "revision": MODEL_REVISION},
        "threshold": FIXED_THRESHOLD,
        "policy": _load_object(POLICY_PATH)["config_version"],
    }
    return sha256(canonical_bytes(spec)).hexdigest()


def _authorize(corpus: Path, output: Path, model: str) -> dict[str, Any]:
    auth = _load_object(AUTHORIZATION_PATH)
    required = ("owner", "approved_at", "repository_commit", "candidate_artifact_sha256",
                "run_nonce", "exact_command", "output_directory")
    if auth.get("status") != "AUTHORIZED" or any(not auth.get(key) for key in required):
        raise CorpusValidationError("final run lacks complete owner authorization")
    if not auth.get("holdout_context_confirmation") or not auth.get("single_run_confirmation"):
        raise CorpusValidationError("final run authorization confirmations are incomplete")
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
    ).strip()
    if auth["repository_commit"] != commit:
        raise CorpusValidationError("authorization commit does not match checkout")
    if auth["candidate_artifact_sha256"] != _candidate_digest(model):
        raise CorpusValidationError("authorization candidate digest does not match runner")
    if auth["output_directory"] != str(output):
        raise CorpusValidationError("authorization output directory does not match command")
    if auth["exact_command"] != shlex.join(sys.argv):
        raise CorpusValidationError("authorization exact command does not match invocation")
    if output.exists():
        raise CorpusValidationError("output directory already exists; refusing a second run")
    output.mkdir(parents=True)
    (output / ".run-lock").write_text(auth["run_nonce"] + "\n", encoding="utf-8")
    return auth


def _predict(model: str, development: Sequence[Any], holdout: Sequence[Any]) -> list[dict[str, Any]]:
    cases = list(development) + list(holdout)
    if model == "structured_tfidf_logistic":
        holdout_probabilities = _fit_predict_tfidf(
            cases, range(len(development)), range(len(development), len(cases))
        )
    elif model == "structured_minilm_pair_logistic":
        features = _minilm_features(cases)
        holdout_probabilities = _fit_predict_minilm(
            cases, features, range(len(development)), range(len(development), len(cases))
        )
    else:
        raise CorpusValidationError(f"unsupported final model: {model}")

    rows: list[dict[str, Any]] = []
    for case, probabilities in zip(holdout, holdout_probabilities, strict=True):
        prediction = _make_prediction(case.snapshot_id, probabilities, FIXED_THRESHOLD)
        rows.append({
            "history_id": case.history_id,
            "family_id": case.family_id,
            "pair_id": case.pair_id,
            "candidate_snapshot_id": case.snapshot_id,
            "gold_relationship": case.gold,
            "acceptable_alternatives": list(case.acceptable_alternatives),
            "severity_if_wrong": case.severity_if_wrong,
            "probabilities": dict(prediction.probabilities),
            "decision": prediction.decision,
            "confidence": prediction.confidence,
            "escalate": prediction.escalate,
        })
    return rows


def run(corpus: Path, output: Path, model: str) -> dict[str, Any]:
    auth = _authorize(corpus, output, model)
    manifest = verify_sealed_corpus(corpus)
    if manifest["manifest_sha256"] != _load_object(AUTHORIZATION_PATH).get("corpus_manifest_sha256"):
        raise CorpusValidationError("sealed manifest does not match authorization pin")
    development = _cases(corpus, "development")
    holdout = _cases(corpus, "holdout")
    if not development or not holdout:
        raise CorpusValidationError("both development and holdout partitions are required")
    rows = _predict(model, development, holdout)
    evaluations = [
        PairEvaluation(
            _make_prediction(
                row["candidate_snapshot_id"],
                {key: float(value) for key, value in row["probabilities"].items()},
                FIXED_THRESHOLD,
            ),
            row["gold_relationship"],
            acceptable_alternatives=tuple(row["acceptable_alternatives"]),
        )
        for row in rows
    ]
    metrics = summarize_g4_metrics(evaluations)
    autonomous_errors = [
        row for row, evaluation in zip(rows, evaluations, strict=True)
        if not evaluation.prediction.escalate
        and evaluation.prediction.decision not in {
            evaluation.gold_relationship, *evaluation.acceptable_alternatives,
        }
    ]
    result = {
        "status": "PAIR_CLASSIFICATION_EVIDENCE_ONLY",
        "full_g4_gate_decision": "NOT_EVALUATED",
        "reason": "transition-validator metrics are not integrated in this harness",
        "run_nonce": auth["run_nonce"],
        "repository_commit": auth["repository_commit"],
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "model": model,
        "threshold": FIXED_THRESHOLD,
        "holdout_family_count": len({case.family_id for case in holdout}),
        "holdout_pair_count": len(rows),
        "metrics": {
            "eligible_count": metrics.eligible_count,
            "autonomous_count": metrics.autonomous_count,
            "correct_autonomous_count": metrics.correct_autonomous_count,
            "autonomous_precision": metrics.autonomous_precision,
            "autonomous_coverage": metrics.autonomous_coverage,
            "expected_calibration_error": metrics.expected_calibration_error,
            "multiclass_brier_score": metrics.multiclass_brier_score,
            "wilson_95_interval": (
                {"lower": metrics.autonomous_precision_wilson_95.lower,
                 "upper": metrics.autonomous_precision_wilson_95.upper}
                if metrics.autonomous_precision_wilson_95 else None
            ),
        },
        "autonomous_errors": autonomous_errors,
        "autonomous_errors_by_severity": dict(Counter(
            row["severity_if_wrong"] for row in autonomous_errors
        )),
        "incident_disclosure": "2026-09-22 repository-search holdout-access incident; v21 was quarantined and is not described as never accessed",
    }
    (output / "predictions.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8"
    )
    (output / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", choices=("structured_tfidf_logistic", "structured_minilm_pair_logistic"), required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.corpus, args.output, args.model), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
