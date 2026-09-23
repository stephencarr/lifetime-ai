"""Score the frozen synthetic M5 retrieval and answerability instrument."""

from __future__ import annotations

import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .chat import ChatRuntime, RuleBasedLocalExtractor
from .store import Store
from .types import Event, EventType, StateItem, StateKind, Transition


ROOT = Path(__file__).resolve().parent.parent
INSTRUMENT = ROOT / "evaluation/m5_answerability/v0.1"
RESULTS = ROOT / "experiments/m5_answerability"
CLOCK = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


def load_frozen() -> tuple[dict, dict, dict]:
    freeze = json.loads((INSTRUMENT / "freeze.json").read_text())
    for name, key in (("cases.json", "cases_sha256"),
                      ("criteria.json", "criteria_sha256")):
        if hashlib.sha256((INSTRUMENT / name).read_bytes()).hexdigest() != freeze[key]:
            raise ValueError(f"frozen M5 answerability instrument changed: {name}")
    cases = json.loads((INSTRUMENT / "cases.json").read_text())
    criteria = json.loads((INSTRUMENT / "criteria.json").read_text())
    count = sum(len(item["questions"]) for item in cases["scenarios"])
    if count != freeze["question_count"] or count < criteria["minimum_questions"]:
        raise ValueError("frozen question count differs")
    return cases, criteria, freeze


def _seed(store: Store, scenario: dict) -> None:
    for source in scenario["sources"]:
        event = Event(source["id"], EventType.USER_MESSAGE, source["text"], CLOCK,
                      {"synthetic": True})
        item = StateItem("item:" + source["id"], StateKind(source["kind"]),
                         source["text"], source["id"], event.event_type, CLOCK,
                         valid_from=CLOCK)
        store.ingest_and_apply(event, Transition("transition:" + source["id"],
                                                 source["id"], item))
    for source_id in scenario["deleted_sources"]:
        store.delete_event(source_id)


def run() -> dict:
    cases, criteria, freeze = load_frozen()
    records = []
    with tempfile.TemporaryDirectory(prefix="lifetime-m5-answerability-") as scratch:
        for scenario in cases["scenarios"]:
            with Store(Path(scratch) / (scenario["id"] + ".sqlite3")) as store:
                _seed(store, scenario)
                runtime = ChatRuntime(store, RuleBasedLocalExtractor())
                for item in scenario["questions"]:
                    response = runtime.ask(item["query"])
                    candidate_ids = [row["source_event_id"] for row in store.retrieve(item["query"])]
                    actual_ids = [cite.source_event_id for cite in response.citations]
                    valid_citations = all(
                        (source := store.event(cite.source_event_id)) is not None
                        and source["deleted_at"] is None
                        and source["text"] == cite.source_text
                        and f"[source:{cite.source_event_id}]" in response.text
                        for cite in response.citations)
                    checks = {
                        "outcome": response.outcome == item["expected_outcome"],
                        "candidate_recall": set(item["expected_candidate_sources"]).issubset(candidate_ids),
                        "citations": sorted(actual_ids) == sorted(item["expected_citations"]),
                        "citation_validity": valid_citations,
                        "content": (item["expected_content"] is None or
                                    item["expected_content"].casefold() in response.text.casefold()),
                        "no_deleted_leak": not (set(actual_ids) & set(scenario["deleted_sources"])),
                    }
                    records.append({"id": item["id"], "family": item["family"],
                                    "query": item["query"],
                                    "expected": {key: value for key, value in item.items()
                                                 if key != "query"},
                                    "candidate_sources": candidate_ids,
                                    "actual": {"outcome": response.outcome, "text": response.text,
                                               "citations": [cite.__dict__ for cite in response.citations]},
                                    "checks": checks,
                                    "failures": [key for key, passed in checks.items() if not passed]})
    supported = [r for r in records if r["expected"]["expected_outcome"] == "answered"]
    unsupported = [r for r in records if r["expected"]["expected_outcome"] == "uncertain"]
    compatible = [r for r in records if r["family"] == "compatible"]
    all_citations = [r for r in records if r["actual"]["citations"]]
    rate = lambda passed, total: passed / total if total else 0.0
    metrics = {
        "candidate_recall_supported": [sum(r["checks"]["candidate_recall"] for r in supported), len(supported)],
        "supported_answer_accuracy": [sum(all(r["checks"][k] for k in ("outcome", "citations", "content")) for r in supported), len(supported)],
        "unsupported_false_answers": [sum(r["actual"]["outcome"] == "answered" for r in unsupported), len(unsupported)],
        "citation_validity": [sum(r["checks"]["citation_validity"] for r in all_citations), len(all_citations)],
        "false_conflicts_compatible": [sum(r["actual"]["outcome"] == "conflict" for r in compatible), len(compatible)],
        "deleted_source_leaks": [sum(not r["checks"]["no_deleted_leak"] for r in records), len(records)],
        "all_item_passes": [sum(not r["failures"] for r in records), len(records)],
    }
    gates = {
        "candidate_recall_supported": rate(*metrics["candidate_recall_supported"]) >= criteria["candidate_recall_supported_min"],
        "supported_answer_accuracy": rate(*metrics["supported_answer_accuracy"]) >= criteria["supported_answer_accuracy_min"],
        "unsupported_false_answers": metrics["unsupported_false_answers"][0] <= criteria["unsupported_false_answers_max"],
        "citation_validity": rate(*metrics["citation_validity"]) >= criteria["citation_validity_min"],
        "false_conflicts_compatible": metrics["false_conflicts_compatible"][0] <= criteria["false_conflicts_compatible_max"],
        "deleted_source_leaks": metrics["deleted_source_leaks"][0] <= criteria["deleted_source_leaks_max"],
    }
    return {"instrument": freeze, "criteria": criteria, "metrics": metrics,
            "gates": gates, "passed": all(gates.values()), "items": records}


def main() -> None:
    result = run()
    RESULTS.mkdir(exist_ok=True, parents=True)
    attempt = 1
    while (RESULTS / f"attempt-{attempt:02d}.json").exists():
        attempt += 1
    path = RESULTS / f"attempt-{attempt:02d}.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "passed": result["passed"],
                      "metrics": result["metrics"], "gates": result["gates"]}, indent=2))


if __name__ == "__main__":
    main()
