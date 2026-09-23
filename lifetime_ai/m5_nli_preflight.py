"""Score the frozen synthetic local NLI development instrument."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from .local_nli import LocalNLI


ROOT = Path(__file__).resolve().parent.parent
INSTRUMENT = ROOT / "evaluation/m5_nli_preflight/v0.1"
RESULTS = ROOT / "experiments/m5_nli_preflight"


def run() -> dict:
    freeze = json.loads((INSTRUMENT / "freeze.json").read_text())
    for name, field in (("cases.json", "cases_sha256"),
                        ("criteria.json", "criteria_sha256"),
                        ("model_lock.json", "model_lock_sha256")):
        if hashlib.sha256((INSTRUMENT / name).read_bytes()).hexdigest() != freeze[field]:
            raise ValueError(f"frozen NLI instrument changed: {name}")
    cases = json.loads((INSTRUMENT / "cases.json").read_text())["cases"]
    criteria = json.loads((INSTRUMENT / "criteria.json").read_text())
    if (len(cases) != freeze["case_count"] or
            sum(item["expected"] == "entailed" for item in cases) != freeze["positive_count"] or
            sum(item["expected"] == "not_entailed" for item in cases) != freeze["negative_count"]):
        raise ValueError("frozen NLI counts changed")
    classifier = LocalNLI(INSTRUMENT / "model_lock.json")
    records = []
    for case in cases:
        started = time.monotonic()
        probability = classifier.entailment_probability(case["source"], case["hypothesis"])
        predicted = "entailed" if probability >= criteria["support_probability_threshold"] else "not_entailed"
        records.append({**case, "entailment_probability": probability,
                        "predicted": predicted, "passed": predicted == case["expected"],
                        "elapsed_seconds": round(time.monotonic() - started, 6)})
    positives = [item for item in records if item["expected"] == "entailed"]
    negatives = [item for item in records if item["expected"] == "not_entailed"]
    p95 = sorted(item["elapsed_seconds"] for item in records)[int(0.95 * (len(records) - 1))]
    metrics = {
        "positive_recall": [sum(item["passed"] for item in positives), len(positives)],
        "false_supports": [sum(not item["passed"] for item in negatives), len(negatives)],
        "all_correct": [sum(item["passed"] for item in records), len(records)],
        "p95_inference_seconds": p95,
    }
    gates = {
        "positive_recall": metrics["positive_recall"][0] / len(positives) >= criteria["minimum_positive_recall"],
        "false_supports": metrics["false_supports"][0] <= criteria["maximum_false_supports"],
        "item_count": len(records) >= criteria["minimum_items"],
        "latency": p95 <= criteria["max_p95_inference_seconds"],
    }
    return {"freeze": freeze, "criteria": criteria, "metrics": metrics,
            "gates": gates, "passed": all(gates.values()), "items": records}


def main() -> None:
    result = run()
    RESULTS.mkdir(parents=True, exist_ok=True)
    index = 1
    while (RESULTS / f"attempt-{index:02d}.json").exists():
        index += 1
    path = RESULTS / f"attempt-{index:02d}.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "passed": result["passed"],
                      "metrics": result["metrics"], "gates": result["gates"]}, indent=2))


if __name__ == "__main__":
    main()
