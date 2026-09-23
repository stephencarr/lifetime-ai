"""Run the frozen, synthetic M5 chat preflight and retain every result."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from .chat import ChatResponse, ChatRuntime, RuleBasedLocalExtractor
from .store import Store


ROOT = Path(__file__).resolve().parent.parent
INSTRUMENT = ROOT / "evaluation" / "m5_preflight" / "v0.1"


def _load_frozen() -> tuple[dict, dict, dict]:
    freeze = json.loads((INSTRUMENT / "freeze.json").read_text())
    for name, key in (("cases.json", "cases_sha256"),
                      ("criteria.json", "criteria_sha256")):
        digest = hashlib.sha256((INSTRUMENT / name).read_bytes()).hexdigest()
        if digest != freeze[key]:
            raise ValueError(f"frozen M5 instrument changed: {name}")
    return (json.loads((INSTRUMENT / "cases.json").read_text()),
            json.loads((INSTRUMENT / "criteria.json").read_text()), freeze)


def _response_record(response: ChatResponse) -> dict:
    return {"outcome": response.outcome, "text": response.text,
            "citations": [citation.__dict__ for citation in response.citations]}


def _probe(database: Path, query: str) -> dict:
    with Store(database) as store:
        return _response_record(ChatRuntime(store, RuleBasedLocalExtractor()).ask(query))


def _restart_probe(database: Path, query: str) -> dict:
    result = subprocess.run(
        [sys.executable, "-m", "lifetime_ai.m5_preflight", "--probe", str(database), query],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def _score_step(step: dict, actual: dict, store: Store,
                deleted: dict[str, str]) -> tuple[list[str], dict[str, bool]]:
    failures: list[str] = []
    checks: dict[str, bool] = {}
    if "outcome" in step:
        checks["outcome"] = actual.get("outcome") == step["outcome"]
        if not checks["outcome"]:
            failures.append(f"outcome: expected {step['outcome']}, got {actual.get('outcome')}")
    if "active" in step:
        present = sorted(row["proposition"] for row in store.active())
        expected = sorted(step["active"])
        actual["active"] = present
        checks["active"] = present == expected
        if not checks["active"]:
            failures.append(f"active state: expected {expected}, got {present}")
    if "citations" in step:
        citations = actual.get("citations", [])
        observed = sorted(item["source_event_id"] for item in citations)
        expected = sorted(step["citations"])
        valid = observed == expected
        for citation in citations:
            source = store.event(citation["source_event_id"])
            valid = valid and source is not None and source["deleted_at"] is None
            if source is not None:
                valid = valid and citation["source_text"] == source["text"]
            valid = valid and f"[source:{citation['source_event_id']}]" in actual["text"]
        checks["citation"] = bool(valid)
        if not valid:
            failures.append(f"citations: expected {expected}, got {observed}, source check={valid}")
    for field, predicate in (("contains", lambda value: value in actual.get("text", "")),
                             ("absent", lambda value: value not in actual.get("text", ""))):
        if field in step:
            checks[field] = predicate(step[field])
            if not checks[field]:
                failures.append(f"{field}: {step[field]!r} in {actual.get('text', '')!r}")
    leaks = [event_id for event_id, source_text in deleted.items()
             if event_id in {item["source_event_id"] for item in actual.get("citations", [])}
             or source_text in actual.get("text", "")]
    checks["no_deleted_leak"] = not leaks
    if leaks:
        failures.append(f"deleted source leaked: {leaks}")
    return failures, checks


def _rate(records: list[bool]) -> float:
    return sum(records) / len(records) if records else 0.0


def run() -> dict:
    cases, criteria, freeze = _load_frozen()
    if len(cases["scenarios"]) < criteria["minimum_scenarios"]:
        raise ValueError("frozen corpus is smaller than the predeclared minimum")
    clock = datetime.fromisoformat(cases["clock"])
    checks: dict[str, list[bool]] = {key: [] for key in (
        "positive_capture_rate", "negative_abstention_rate", "active_state_accuracy",
        "answer_outcome_accuracy", "citation_accuracy", "restart_accuracy")}
    results = []
    message_count = 0
    failed_expectations = 0
    deleted_canary_leaks = 0
    with tempfile.TemporaryDirectory(prefix="lifetime-m5-preflight-") as scratch:
        for scenario in cases["scenarios"]:
            database = Path(scratch) / f"{scenario['id']}.sqlite3"
            store = Store(database)
            runtime = ChatRuntime(store, RuleBasedLocalExtractor())
            deleted: dict[str, str] = {}
            observed_steps = []
            try:
                for step in scenario["steps"]:
                    actual: dict = {}
                    failures: list[str] = []
                    try:
                        operation = step["op"]
                        if operation == "send":
                            message_count += 1
                            actual = _response_record(runtime.send(
                                step["text"], clock, step["id"]))
                        elif operation == "correct":
                            actual = _response_record(runtime.correct(
                                step["item"], step["text"], clock, step["id"]))
                        elif operation == "ask":
                            actual = _response_record(runtime.ask(step["query"]))
                        elif operation == "restart_ask":
                            store.close()
                            actual = _restart_probe(database, step["query"])
                            store = Store(database)
                            runtime = ChatRuntime(store, RuleBasedLocalExtractor())
                        elif operation == "forget":
                            source = store.event(step["id"])
                            if source is not None:
                                deleted[step["id"]] = source["text"]
                            actual = {"changed": runtime.delete_source(step["id"])}
                        else:
                            raise ValueError(f"unknown preflight operation: {operation}")
                        failures, scored = _score_step(step, actual, store, deleted)
                        if operation == "send":
                            name = ("positive_capture_rate" if step["outcome"] == "accepted"
                                    else "negative_abstention_rate")
                            checks[name].append(scored["outcome"])
                        if "active" in scored:
                            checks["active_state_accuracy"].append(scored["active"])
                        if operation in {"ask", "restart_ask"}:
                            answer_ok = all(scored.get(key, True) for key in
                                            ("outcome", "contains", "absent"))
                            checks["answer_outcome_accuracy"].append(answer_ok)
                            checks["citation_accuracy"].append(scored["citation"])
                        if operation == "restart_ask":
                            checks["restart_accuracy"].append(not failures)
                        if not scored["no_deleted_leak"]:
                            deleted_canary_leaks += 1
                    except Exception as error:
                        failures.append(f"exception: {type(error).__name__}: {error}")
                    failed_expectations += len(failures)
                    observed_steps.append({"step": step, "actual": actual, "failures": failures})
            finally:
                store.close()
            results.append({"id": scenario["id"], "category": scenario["category"],
                            "passed": all(not item["failures"] for item in observed_steps),
                            "steps": observed_steps})
    metrics = {key: {"passed": sum(values), "total": len(values), "rate": _rate(values)}
               for key, values in checks.items()}
    metrics["deleted_canary_leaks"] = deleted_canary_leaks
    metrics["manual_repair_actions_per_20_messages"] = (
        failed_expectations * 20 / message_count if message_count else float("inf"))
    passed = all(
        metrics[key]["total"] > 0 and metrics[key]["rate"] >= target
        for key, target in criteria["thresholds"].items()
        if key not in {"deleted_canary_leaks", "manual_repair_actions_per_20_messages"}
    )
    passed = (passed and deleted_canary_leaks <= criteria["thresholds"]["deleted_canary_leaks"]
              and metrics["manual_repair_actions_per_20_messages"] <=
              criteria["thresholds"]["manual_repair_actions_per_20_messages"])
    git_hash = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
    git_status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True,
                                capture_output=True, text=True).stdout.strip()
    return {"instrument": freeze, "criteria": criteria, "git_commit": git_hash,
            "git_dirty": bool(git_status), "python": sys.version, "platform": platform.platform(),
            "message_count": message_count, "failed_expectations": failed_expectations,
            "metrics": metrics, "passed": passed, "scenarios": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", nargs=2, metavar=("DATABASE", "QUERY"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(_probe(Path(args.probe[0]), args.probe[1])))
        return
    report = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": report["passed"], "metrics": report["metrics"],
                      "failed_scenarios": [item["id"] for item in report["scenarios"]
                                           if not item["passed"]]}, indent=2))


if __name__ == "__main__":
    main()
