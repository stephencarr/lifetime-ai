from __future__ import annotations

from collections import Counter
from typing import Any


RELATIONSHIP_LIMIT = 0.40


def check_probes(histories: list[dict[str, Any]]) -> dict[str, Any]:
    """Run an event-only shortcut diagnostic for relationship labels.

    Disposition is deliberately reported descriptively only: it depends on
    structured authority/validity inputs and is not a text-classification task.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    rows = []
    partitions = {h["family_id"]: h["partition"] for h in histories}
    for history in histories:
        events = {event["event_id"]: event for event in history["timeline"]}
        gold = {item["pair_id"]: item
                for item in history["evaluator_only"]["pair_gold"]}
        for pair in history["pair_inputs"]:
            label = gold[pair["pair_id"]]
            rows.append((history["family_id"],
                         events[pair["event_id"]]["content"] or "",
                         label["semantic_relationship"],
                         label["transition_disposition"]))

    train = [r for r in rows if partitions[r[0]] == "pilot_development"]
    test = [r for r in rows if partitions[r[0]] == "pilot_holdout"]
    train_families = {r[0] for r in train}
    test_families = {r[0] for r in test}
    if not train or not test or train_families & test_families:
        raise ValueError("probe requires nonempty family-disjoint partitions")

    def fit_predict(column: int) -> tuple[list[str], list[str], float]:
        model = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True,
                            max_features=1000),
            LogisticRegression(max_iter=2000, C=10, random_state=0),
        )
        model.fit([r[1] for r in train], [r[column] for r in train])
        predicted = model.predict([r[1] for r in test]).tolist()
        truth = [r[column] for r in test]
        return truth, predicted, sum(p == y for p, y in zip(predicted, truth)) / len(truth)

    rel_truth, rel_pred, rel_accuracy = fit_predict(2)
    disp_truth, disp_pred, disp_accuracy = fit_predict(3)
    rel_majority = max(Counter(r[2] for r in train).values()) / len(train)
    disp_majority = max(Counter(r[3] for r in train).values()) / len(train)
    labels = sorted(set(rel_truth) | set(rel_pred))
    return {
        "protocol": "g3-v0.4-event-only-shortcut-diagnostic",
        "partitioning": "family_disjoint",
        "train_pairs": len(train), "test_pairs": len(test),
        "train_families": sorted(train_families),
        "test_families": sorted(test_families),
        "family_overlap": sorted(train_families & test_families),
        "relationship_shortcut_diagnostic": {
            "input": "evaluated_event.content_only",
            "correct": sum(p == y for p, y in zip(rel_pred, rel_truth)),
            "total": len(rel_truth), "accuracy": f"{rel_accuracy:.1%}",
            "training_majority_baseline": f"{rel_majority:.1%}",
            "limit": f"{RELATIONSHIP_LIMIT:.0%}",
            "confusion": {label: {pred: sum(y == label and p == pred
                                              for y, p in zip(rel_truth, rel_pred))
                                    for pred in labels}
                          for label in labels},
            "passed": rel_accuracy <= RELATIONSHIP_LIMIT,
        },
        "disposition_diagnostic_only": {
            "input": "evaluated_event.content_only (intentionally incomplete)",
            "reason_not_a_gate": (
                "Disposition depends on structured authority, validity, and transition "
                "policy; event prose alone is not the disposition decision input."),
            "correct": sum(p == y for p, y in zip(disp_pred, disp_truth)),
            "total": len(disp_truth), "accuracy": f"{disp_accuracy:.1%}",
            "training_majority_baseline": f"{disp_majority:.1%}",
            "test_class_counts": dict(sorted(Counter(disp_truth).items())),
        },
        "gate_passed": rel_accuracy <= RELATIONSHIP_LIMIT,
    }
