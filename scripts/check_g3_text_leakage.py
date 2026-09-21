from __future__ import annotations

from collections import Counter
from typing import Any


RELATIONSHIP_LIMIT = 0.40
DISPOSITION_LIMIT = 0.60


def check_text_leakage(histories: list[dict[str, Any]]) -> dict[str, Any]:
    """Fit text-only probes on development families and score pilot holdout."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    rows = []
    partition_by_family = {history["family_id"]: history["partition"]
                           for history in histories}
    for history in histories:
        events = {event["event_id"]: event for event in history["timeline"]}
        gold = {item["pair_id"]: item
                for item in history["evaluator_only"]["pair_gold"]}
        for pair in history["pair_inputs"]:
            text = events[pair["event_id"]]["content"] or ""
            item = gold[pair["pair_id"]]
            rows.append((history["family_id"], text,
                         item["semantic_relationship"],
                         item["transition_disposition"]))

    train = [row for row in rows
             if partition_by_family[row[0]] == "pilot_development"]
    test = [row for row in rows
            if partition_by_family[row[0]] == "pilot_holdout"]
    train_families = {row[0] for row in train}
    test_families = {row[0] for row in test}
    if not train or not test or train_families & test_families:
        raise ValueError("leakage probe requires nonempty family-disjoint partitions")

    metrics: dict[str, Any] = {}
    for label_index, label_name, limit in (
        (2, "relationship", RELATIONSHIP_LIMIT),
        (3, "disposition", DISPOSITION_LIMIT),
    ):
        train_labels = [row[label_index] for row in train]
        test_labels = [row[label_index] for row in test]
        model = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True,
                            max_features=1000),
            LogisticRegression(max_iter=2000, C=10, random_state=0),
        )
        model.fit([row[1] for row in train], train_labels)
        predictions = model.predict([row[1] for row in test])
        correct = sum(prediction == expected
                      for prediction, expected in zip(predictions, test_labels))
        accuracy = correct / len(test_labels)
        majority = max(Counter(train_labels).values()) / len(train_labels)
        metrics[label_name] = {
            "correct": correct, "total": len(test_labels),
            "accuracy": f"{accuracy:.1%}",
            "training_majority_baseline": f"{majority:.1%}",
            "threshold": f"{limit:.0%}", "passed": accuracy <= limit,
        }

    return {
        "procedure": "tfidf_logistic_family_disjoint_v1",
        "input_field": "evaluated_event.content_only",
        "train_pairs": len(train), "test_pairs": len(test),
        "train_families": sorted(train_families),
        "test_families": sorted(test_families),
        "family_overlap": sorted(train_families & test_families),
        "metrics": metrics,
        "passed": all(value["passed"] for value in metrics.values()),
    }
