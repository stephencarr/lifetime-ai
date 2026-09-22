"""Compare local G4 classifiers with nested family-grouped development folds."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Sequence

from lifetime_ai.evaluation.canonical import read_jsonl
from lifetime_ai.evaluation.g4_development import verify_g4_development_partition
from lifetime_ai.evaluation.g4_features import pair_feature_document, pair_feature_texts
from lifetime_ai.evaluation.g4_metrics import PairEvaluation, summarize_g4_metrics
from lifetime_ai.evaluation.projection import build_pair_classification_projection
from lifetime_ai.evaluation.validation import CorpusValidationError, RELATIONSHIPS
from scripts.run_g4_local_development import _assert_development_authorized, _make_prediction


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
RELATIONSHIP_NAMES = sorted(RELATIONSHIPS)


@dataclass(frozen=True)
class Case:
    family_id: str
    history_id: str
    pair_id: str
    snapshot_id: str
    gold: str
    acceptable_alternatives: tuple[str, ...]
    severity_if_wrong: str
    document: str
    event_text: str
    candidate_text: str
    context_text: str
    gold_effect: str = "none"
    gold_disposition: str = "no_op"
    may_assert_user_state: bool = False
    may_request_transition: bool = False


def _cases(corpus: Path) -> list[Case]:
    cases: list[Case] = []
    # This runner opens only the development payload after its pinned hash check.
    for history in read_jsonl(corpus / "development.jsonl"):
        if history.get("partition") != "development":
            raise CorpusValidationError("development payload contains another partition")
        gold = {item["pair_id"]: item for item in history["evaluator_only"]["pair_gold"]}
        events = {item["event_id"]: item for item in history["timeline"]}
        for pair in history["pair_inputs"]:
            projection = build_pair_classification_projection(history, pair["pair_id"])
            event_text, candidate_text, context_text = pair_feature_texts(projection)
            authority = events[pair["event_id"]]["authority"]
            cases.append(Case(
                family_id=history["family_id"],
                history_id=history["history_id"],
                pair_id=pair["pair_id"],
                snapshot_id=pair["candidate_snapshot_id"],
                gold=gold[pair["pair_id"]]["semantic_relationship"],
                acceptable_alternatives=tuple(gold[pair["pair_id"]]["acceptable_alternatives"]),
                severity_if_wrong=gold[pair["pair_id"]]["severity_if_wrong"],
                document=pair_feature_document(projection),
                event_text=event_text,
                candidate_text=candidate_text,
                context_text=context_text,
                gold_effect=gold[pair["pair_id"]]["expected_state_effect"]["effect"],
                gold_disposition=gold[pair["pair_id"]]["transition_disposition"],
                may_assert_user_state=authority["may_assert_user_state"],
                may_request_transition=authority["may_request_transition"],
            ))
    return cases


def _folds(cases: Sequence[Case], indices: Sequence[int], count: int, salt: str) -> list[list[int]]:
    families = sorted(
        {cases[index].family_id for index in indices},
        key=lambda value: sha256(f"{salt}:{value}".encode()).hexdigest(),
    )
    if len(families) < count:
        raise ValueError("too few families for grouped folds")
    fold_by_family = {family: position % count for position, family in enumerate(families)}
    folds = [[] for _ in range(count)]
    for index in indices:
        folds[fold_by_family[cases[index].family_id]].append(index)
    return folds


def _fit_predict_tfidf(cases: Sequence[Case], train: Sequence[int], validation: Sequence[int]) -> list[dict[str, float]]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    train_vectors = vectorizer.fit_transform([cases[index].document for index in train])
    classifier = LogisticRegression(max_iter=1000, random_state=0)
    classifier.fit(train_vectors, [cases[index].gold for index in train])
    raw = classifier.predict_proba(vectorizer.transform([cases[index].document for index in validation]))
    return [
        {name: float(row[list(classifier.classes_).index(name)]) if name in classifier.classes_ else 0.0
         for name in RELATIONSHIP_NAMES}
        for row in raw
    ]


def _minilm_features(cases: Sequence[Case]):
    import numpy as np
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION, local_files_only=True)
    event = encoder.encode(
        [case.event_text + " " + case.context_text for case in cases],
        normalize_embeddings=True, show_progress_bar=False,
    )
    candidate = encoder.encode(
        [case.candidate_text for case in cases],
        normalize_embeddings=True, show_progress_bar=False,
    )
    return np.concatenate((event, candidate, np.abs(event - candidate), event * candidate), axis=1)


def _fit_predict_minilm(cases: Sequence[Case], features, train: Sequence[int], validation: Sequence[int]) -> list[dict[str, float]]:
    from sklearn.linear_model import LogisticRegression

    classifier = LogisticRegression(max_iter=1000, random_state=0)
    classifier.fit(features[list(train)], [cases[index].gold for index in train])
    raw = classifier.predict_proba(features[list(validation)])
    return [
        {name: float(row[list(classifier.classes_).index(name)]) if name in classifier.classes_ else 0.0
         for name in RELATIONSHIP_NAMES}
        for row in raw
    ]


def _select_threshold(cases: Sequence[Case], indexed_probabilities: Sequence[tuple[int, dict[str, float]]]) -> float:
    ranked = []
    for index, probabilities in indexed_probabilities:
        decision = max(RELATIONSHIP_NAMES, key=lambda name: (probabilities[name], name))
        if decision == "uncertain":
            continue
        ranked.append((
            probabilities[decision],
            decision in {cases[index].gold, *cases[index].acceptable_alternatives},
        ))
    ranked.sort(reverse=True)
    accepted = correct = 0
    best_count = 0
    best_threshold = 1.0
    position = 0
    while position < len(ranked):
        confidence = ranked[position][0]
        while position < len(ranked) and ranked[position][0] == confidence:
            accepted += 1
            correct += ranked[position][1]
            position += 1
        if correct / accepted >= 0.95 and accepted > best_count:
            best_count = accepted
            best_threshold = confidence
    return best_threshold


def _fit_temperature(cases: Sequence[Case], indexed_probabilities: Sequence[tuple[int, dict[str, float]]]) -> float:
    """Fit one temperature on inner out-of-fold predictions only."""
    import numpy as np
    from scipy.optimize import minimize_scalar
    from scipy.special import logsumexp

    indices = [index for index, _ in indexed_probabilities]
    matrix = np.array([
        [probabilities[name] for name in RELATIONSHIP_NAMES]
        for _, probabilities in indexed_probabilities
    ])
    logits = np.log(np.clip(matrix, 1e-12, 1.0))
    gold = np.array([RELATIONSHIP_NAMES.index(cases[index].gold) for index in indices])

    def log_loss(temperature: float) -> float:
        scaled = logits / temperature
        selected = scaled[np.arange(len(gold)), gold]
        return float(np.mean(logsumexp(scaled, axis=1) - selected))

    optimum = minimize_scalar(log_loss, bounds=(0.05, 5.0), method="bounded")
    if not optimum.success:
        raise RuntimeError("inner-fold temperature calibration failed")
    return float(optimum.x)


def _apply_temperature(probabilities: dict[str, float], temperature: float) -> dict[str, float]:
    import numpy as np

    logits = np.log(np.clip(
        np.array([probabilities[name] for name in RELATIONSHIP_NAMES]), 1e-12, 1.0,
    )) / temperature
    weights = np.exp(logits - max(logits))
    weights /= weights.sum()
    return {name: float(weights[position]) for position, name in enumerate(RELATIONSHIP_NAMES)}


def _evaluate(cases: Sequence[Case], predictor: Callable[[Sequence[int], Sequence[int]], list[dict[str, float]]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    all_indices = list(range(len(cases)))
    outer_folds = _folds(cases, all_indices, 5, "g4-outer-v1")
    out_rows: list[dict[str, Any]] = []
    thresholds: list[float] = []
    temperatures: list[float] = []
    for outer_number, outer_validation in enumerate(outer_folds):
        outer_held = set(outer_validation)
        outer_train = [index for index in all_indices if index not in outer_held]
        train_families = {cases[index].family_id for index in outer_train}
        validation_families = {cases[index].family_id for index in outer_validation}
        assert train_families.isdisjoint(validation_families)

        inner_folds = _folds(cases, outer_train, 4, f"g4-inner-v1-{outer_number}")
        inner_predictions: list[tuple[int, dict[str, float]]] = []
        for inner_validation in inner_folds:
            held = set(inner_validation)
            inner_train = [index for index in outer_train if index not in held]
            assert {cases[index].family_id for index in inner_train}.isdisjoint(
                {cases[index].family_id for index in inner_validation}
            )
            inner_predictions.extend(zip(
                inner_validation, predictor(inner_train, inner_validation), strict=True,
            ))
        temperature = _fit_temperature(cases, inner_predictions)
        temperatures.append(temperature)
        calibrated_inner = [
            (index, _apply_temperature(probabilities, temperature))
            for index, probabilities in inner_predictions
        ]
        threshold = _select_threshold(cases, calibrated_inner)
        thresholds.append(threshold)
        probabilities = [
            _apply_temperature(vector, temperature)
            for vector in predictor(outer_train, outer_validation)
        ]
        for index, vector in zip(outer_validation, probabilities, strict=True):
            case = cases[index]
            prediction = _make_prediction(case.snapshot_id, vector, threshold)
            out_rows.append({
                "model_fold": outer_number,
                "history_id": case.history_id,
                "pair_id": case.pair_id,
                "family_id": case.family_id,
                "candidate_snapshot_id": case.snapshot_id,
                "gold_relationship": case.gold,
                "acceptable_alternatives": list(case.acceptable_alternatives),
                "severity_if_wrong": case.severity_if_wrong,
                "probabilities": dict(prediction.probabilities),
                "decision": prediction.decision,
                "confidence": prediction.confidence,
                "escalate": prediction.escalate,
                "threshold": threshold,
            })

    if len(out_rows) != len(cases) or len({row["pair_id"] for row in out_rows}) != len(cases):
        raise CorpusValidationError("outer folds did not yield exactly one prediction per pair")
    evaluations = [PairEvaluation(
        _make_prediction(row["candidate_snapshot_id"],
                         {key: float(value) for key, value in row["probabilities"].items()},
                         row["threshold"]),
        row["gold_relationship"],
        acceptable_alternatives=tuple(row["acceptable_alternatives"]),
    ) for row in out_rows]
    metrics = summarize_g4_metrics(evaluations)
    confusion = {gold: {predicted: 0 for predicted in RELATIONSHIP_NAMES}
                 for gold in RELATIONSHIP_NAMES}
    for row in out_rows:
        confusion[row["gold_relationship"]][row["decision"]] += 1
    errors = [row for row in out_rows if row["decision"] not in {
        row["gold_relationship"], *row["acceptable_alternatives"]
    }]
    tuned_candidate_errors = [row for row in errors if not row["escalate"]]
    fixed_policy_evaluations = [PairEvaluation(
        _make_prediction(row["candidate_snapshot_id"],
                         {key: float(value) for key, value in row["probabilities"].items()},
                         0.95),
        row["gold_relationship"],
        acceptable_alternatives=tuple(row["acceptable_alternatives"]),
    ) for row in out_rows]
    fixed_policy = summarize_g4_metrics(fixed_policy_evaluations)
    fixed_policy_errors = [
        row for row in errors
        if float(row["confidence"]) >= 0.95 and row["decision"] != "uncertain"
    ]
    return {
        "eligible_pairs": metrics.eligible_count,
        "tuned_candidate_accepts": metrics.autonomous_count,
        "correct_tuned_candidate_accepts": metrics.correct_autonomous_count,
        "tuned_candidate_precision": metrics.autonomous_precision,
        "tuned_candidate_coverage": metrics.autonomous_coverage,
        "expected_calibration_error": metrics.expected_calibration_error,
        "multiclass_brier_score": metrics.multiclass_brier_score,
        "per_class_precision": dict(metrics.per_class_precision),
        "per_class_recall": dict(metrics.per_class_recall),
        "confusion_matrix": confusion,
        "thresholds_by_outer_fold": thresholds,
        "temperatures_by_outer_fold": temperatures,
        "errors_by_gold_class": dict(Counter(row["gold_relationship"] for row in errors)),
        "wrong_tuned_candidate_accepts": len(tuned_candidate_errors),
        "wrong_tuned_candidate_accepts_by_severity": dict(Counter(
            row["severity_if_wrong"] for row in tuned_candidate_errors
        )),
        "frozen_0_95_probability_gate_only": {
            "candidate_accepts": fixed_policy.autonomous_count,
            "correct_candidate_accepts": fixed_policy.correct_autonomous_count,
            "precision": fixed_policy.autonomous_precision,
            "coverage": fixed_policy.autonomous_coverage,
            "wilson_95_interval": (
                {
                    "lower": fixed_policy.autonomous_precision_wilson_95.lower,
                    "upper": fixed_policy.autonomous_precision_wilson_95.upper,
                }
                if fixed_policy.autonomous_precision_wilson_95 else None
            ),
            "errors_by_severity": dict(Counter(
                row["severity_if_wrong"] for row in fixed_policy_errors
            )),
            "validator_applied": False,
        },
    }, out_rows


def run(corpus: Path, output: Path, artifacts: Path) -> dict[str, Any]:
    _assert_development_authorized()
    manifest = verify_g4_development_partition(corpus)
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed corpus must be prediction-free")
    cases = _cases(corpus)
    if len(cases) != 1080 or len({case.family_id for case in cases}) != 90:
        raise CorpusValidationError("unexpected development case or family count")
    results = {}
    for model_name, predictor in (
        ("structured_tfidf_logistic", lambda train, val: _fit_predict_tfidf(cases, train, val)),
        ("structured_minilm_pair_logistic", None),
    ):
        if predictor is None:
            features = _minilm_features(cases)
            predictor = lambda train, val: _fit_predict_minilm(cases, features, train, val)
        metrics, rows = _evaluate(cases, predictor)
        artifacts.mkdir(parents=True, exist_ok=True)
        path = artifacts / f"{model_name}-out-of-fold.jsonl"
        path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        metrics["prediction_artifact"] = str(path)
        results[model_name] = metrics
    result = {
        "status": "DEVELOPMENT_COMPLETE",
        "partition": "development_only",
        "protocol": "5 outer family folds; 4 inner family folds per outer train; temperature and threshold selected on inner out-of-fold predictions",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "sentence_encoder": {"name": MODEL_NAME, "revision": MODEL_REVISION},
        "models": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.corpus, args.output, args.artifacts)
    summary_keys = {
        "tuned_candidate_accepts", "tuned_candidate_precision", "tuned_candidate_coverage",
        "expected_calibration_error", "multiclass_brier_score", "wrong_tuned_candidate_accepts",
    }
    summary = {
        name: {key: value for key, value in metrics.items() if key in summary_keys}
        for name, metrics in result["models"].items()
    }
    print(json.dumps({"status": result["status"], "models": summary}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
