"""Run the frozen integrated local-model M5 development instrument."""

from __future__ import annotations

import hashlib
import json
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from .local_models import locked_clients
from .model_chat import ModelChatRuntime
from .model_semantics import PROMPT_VERSION
from .store import Store


ROOT = Path(__file__).resolve().parent.parent
INSTRUMENT = ROOT / "evaluation/m5_model_poc/v0.1"
LOCK = ROOT / "evaluation/m5_model_poc/model_lock.json"
RESULTS = ROOT / "experiments/m5_model_poc"
CLOCK = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


def load_frozen() -> tuple[dict, dict, dict]:
    freeze = json.loads((INSTRUMENT / "freeze.json").read_text())
    for name, field in (("cases.json", "cases_sha256"),
                        ("criteria.json", "criteria_sha256")):
        if hashlib.sha256((INSTRUMENT / name).read_bytes()).hexdigest() != freeze[field]:
            raise ValueError(f"frozen model POC instrument changed: {name}")
    cases = json.loads((INSTRUMENT / "cases.json").read_text())
    criteria = json.loads((INSTRUMENT / "criteria.json").read_text())
    steps = [step for scenario in cases["scenarios"] for step in scenario["steps"]]
    if (len(cases["scenarios"]) != freeze["scenario_count"] or
            sum(item["op"] == "send" for item in steps) != freeze["message_count"] or
            sum(item["op"] == "ask" for item in steps) != freeze["question_count"]):
        raise ValueError("frozen instrument counts changed")
    return cases, criteria, freeze


def _rate(pair: list[int]) -> float:
    return pair[0] / pair[1] if pair[1] else 0.0


def run() -> dict:
    cases, criteria, freeze = load_frozen()
    generator, embedder, lock = locked_clients(LOCK)
    records = []
    with tempfile.TemporaryDirectory(prefix="lifetime-m5-model-poc-") as scratch:
        for scenario in cases["scenarios"]:
            with Store(Path(scratch) / (scenario["id"] + ".sqlite3")) as store:
                runtime = ModelChatRuntime(store, generator, embedder)
                deleted: set[str] = set()
                for step in scenario["steps"]:
                    start = time.monotonic()
                    before_usage = runtime.usage.copy()
                    actual = {}
                    failures = []
                    checks = {}
                    try:
                        if step["op"] == "send":
                            response = runtime.send(step["text"], CLOCK, step["id"])
                            new_rows = [row for row in store.model_active_rows()
                                        if row["source_event_id"] == step["id"]]
                            actual = {"outcome": response.outcome,
                                      "claim_count": len(new_rows),
                                      "claims": [{"item_id": row["item_id"],
                                                  "proposition": row["proposition"],
                                                  "actor": row["actor"], "scope": row["scope"],
                                                  "source_quote": row["source_quote"]}
                                                 for row in new_rows]}
                            checks["capture"] = response.outcome == step["expected_capture"]
                            checks["claim_count"] = len(new_rows) == step["expected_claim_count"]
                        elif step["op"] == "ask":
                            candidates = runtime.retriever.candidates(step["query"])
                            candidate_sources = [row["source_event_id"] for row in candidates]
                            response = runtime.ask(step["query"])
                            cited_sources = [cite.source_event_id for cite in response.citations]
                            valid = all(
                                (source := store.event(cite.source_event_id)) is not None
                                and source["deleted_at"] is None
                                and source["text"] == cite.source_text
                                and f"[source:{cite.source_event_id}]" in response.text
                                for cite in response.citations)
                            actual = {"outcome": response.outcome, "text": response.text,
                                      "candidate_sources": candidate_sources,
                                      "citations": [cite.__dict__ for cite in response.citations]}
                            checks = {"outcome": response.outcome == step["expected_outcome"],
                                      "candidate_recall": set(step["expected_candidate_sources"]).issubset(candidate_sources),
                                      "citations": sorted(cited_sources) == sorted(step["expected_citations"]),
                                      "citation_validity": valid,
                                      "no_deleted_leak": not (set(cited_sources) & deleted)}
                        elif step["op"] == "forget":
                            actual = {"changed": runtime.delete_source(step["id"])}
                            deleted.add(step["id"])
                            checks = {"changed": actual["changed"]}
                        else:
                            raise ValueError("unknown instrument operation")
                    except Exception as error:
                        failures.append(f"exception: {type(error).__name__}: {error}")
                    failures.extend(key for key, passed in checks.items() if not passed)
                    records.append({"scenario": scenario["id"], "family": scenario["family"],
                                    "step": step, "actual": actual, "checks": checks,
                                    "failures": failures,
                                    "elapsed_seconds": round(time.monotonic() - start, 3),
                                    "model_usage": {key: runtime.usage[key] - before_usage[key]
                                                    for key in before_usage}})
    sends = [r for r in records if r["step"]["op"] == "send"]
    positives = [r for r in sends if r["step"]["expected_capture"] == "accepted"]
    negatives = [r for r in sends if r["step"]["expected_capture"] == "abstained"]
    answers = [r for r in records if r["step"]["op"] == "ask"]
    supported = [r for r in answers if r["step"]["expected_outcome"] == "answered"]
    unsupported = [r for r in answers if r["step"]["expected_outcome"] == "uncertain"]
    metrics = {
        "clear_capture": [sum(r["checks"].get("capture", False) and
                              r["checks"].get("claim_count", False) for r in positives), len(positives)],
        "false_durable_capture": [sum(r["actual"].get("claim_count", 0) > 0 for r in negatives), len(negatives)],
        "supported_answer": [sum(r["checks"].get("outcome", False) and
                                 r["checks"].get("citations", False) for r in supported), len(supported)],
        "unsupported_false_answer": [sum(r["actual"].get("outcome") == "answered"
                                         for r in unsupported), len(unsupported)],
        "candidate_recall_supported": [sum(r["checks"].get("candidate_recall", False)
                                           for r in supported), len(supported)],
        "citation_validity": [sum(r["checks"].get("citation_validity", False)
                                  for r in answers if r["actual"].get("citations")),
                              sum(bool(r["actual"].get("citations")) for r in answers)],
        "deleted_source_leaks": [sum(not r["checks"].get("no_deleted_leak", True)
                                     for r in answers), len(answers)],
        "all_item_passes": [sum(not r["failures"] for r in records), len(records)],
    }
    durations = sorted(r["elapsed_seconds"] for r in records if r["step"]["op"] in {"send", "ask"})
    p95 = durations[min(len(durations) - 1, int(0.95 * len(durations)))]
    gates = {
        "clear_capture": _rate(metrics["clear_capture"]) >= criteria["clear_capture_rate_min"],
        "false_durable_capture": metrics["false_durable_capture"][0] <= criteria["false_durable_capture_max"],
        "supported_answer": _rate(metrics["supported_answer"]) >= criteria["supported_answer_accuracy_min"],
        "unsupported_false_answer": metrics["unsupported_false_answer"][0] <= criteria["unsupported_false_answer_max"],
        "candidate_recall_supported": _rate(metrics["candidate_recall_supported"]) >= criteria["candidate_recall_supported_min"],
        "citation_validity": _rate(metrics["citation_validity"]) >= criteria["citation_validity_min"],
        "deleted_source_leaks": metrics["deleted_source_leaks"][0] <= criteria["deleted_source_leaks_max"],
        "latency_p95": p95 <= criteria["latency_p95_seconds_max"],
    }
    return {"instrument": freeze, "model_lock": lock,
            "prompt_version": PROMPT_VERSION, "criteria": criteria,
            "metrics": metrics, "latency_p95_seconds": p95,
            "total_model_calls": sum(r["model_usage"]["calls"] for r in records),
            "total_model_tokens": sum(r["model_usage"]["prompt_tokens"] +
                                      r["model_usage"]["completion_tokens"] for r in records),
            "gates": gates, "passed": all(gates.values()), "items": records}


def main() -> None:
    result = run()
    RESULTS.mkdir(parents=True, exist_ok=True)
    attempt = 1
    while (RESULTS / f"attempt-{attempt:02d}.json").exists():
        attempt += 1
    path = RESULTS / f"attempt-{attempt:02d}.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"path": str(path), "passed": result["passed"],
                      "metrics": result["metrics"], "gates": result["gates"],
                      "latency_p95_seconds": result["latency_p95_seconds"],
                      "total_model_calls": result["total_model_calls"],
                      "total_model_tokens": result["total_model_tokens"]}, indent=2))


if __name__ == "__main__":
    main()
