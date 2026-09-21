from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, file_manifest_entry, sha256_bytes
from lifetime_ai.evaluation.coverage import validate_development_pilot_coverage
from lifetime_ai.evaluation.validation import validate_corpus
from scripts import generate_g3_development_pilot as base
from scripts import generate_g3_development_pilot_v06 as v06
from scripts.check_g3_projection_leakage import check_projection_leakage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evaluation" / "corpus" / "pilot-v0.7"
REPORT_DATE = "2026-09-18T10:00:00Z"


def _revise_semantics(histories: list[dict[str, Any]]) -> None:
    completion_ids = {
        "full-01-p2", "full-07-p2", "full-13-p1", "full-18-p3",
        "full-23-p1", "full-26-p4", "full-30-p2",
    }
    for history in histories:
        history["dataset_version"] = "pilot-v0.7"
        history["family_id"] = history["family_id"].replace(
            "surface-v06-family", "surface-v07-family")
        provenance = history["evaluator_only"]["generation_and_review_provenance"]
        provenance["generator"] = "scripts/generate_g3_development_pilot_v07.py"
        timeline = {event["event_id"]: event for event in history["timeline"]}

        # A completion confirms a commitment and resolves it; it does not replace it.
        for gold in history["evaluator_only"]["pair_gold"]:
            if gold["pair_id"].removesuffix("-pair") in completion_ids:
                assert gold["semantic_relationship"] == "supersedes"
                assert gold["expected_state_effect"]["effect"] == "resolve"
                gold["semantic_relationship"] = "supports"

        # Keep the explicit-precedence contradiction on a valid same-day boundary.
        if history["history_id"] == "full-30":
            p1 = timeline["full-30-p1-event"]
            p1["content"] = p1["content"].removeprefix(
                "Late report, effective 2026-09-16: ")
            p1["occurred_at"] = REPORT_DATE

            # Preserve the late-report probe on p3, whose declared effective date is
            # 2026-09-18, while recording that the report was received on that date.
            p3 = timeline["full-30-p3-event"]
            p3["content"] = "Late report recorded 2026-09-18: " + p3["content"]
            p3["occurred_at"] = "2026-09-16T10:00:00Z"
            p3["recorded_at"] = REPORT_DATE
            for gold in history["evaluator_only"]["pair_gold"]:
                if gold["pair_id"] == "full-30-p1-pair":
                    gold["feature_tags"] = sorted(
                        (set(gold["feature_tags"]) - {"late_or_retroactive_report"})
                        | {"explicit_precedence"})
                elif gold["pair_id"] == "full-30-p3-pair":
                    gold["feature_tags"] = sorted(
                        set(gold["feature_tags"]) | {"late_or_retroactive_report"})
            for checkpoint in history["evaluator_only"]["checkpoint_gold"]:
                for state in checkpoint["current_state"]:
                    if state["semantic_item_ref"] in {
                        "semantic:p1:target", "semantic:p1:target:replacement"}:
                        state["valid_until"] = (
                            REPORT_DATE if state["semantic_item_ref"] == "semantic:p1:target"
                            and state["status"] == "revoked" else state["valid_until"])
                        if state["semantic_item_ref"] == "semantic:p1:target:replacement":
                            state["valid_from"] = REPORT_DATE
                            state["proposition"] = p1["content"]
                    if state["semantic_item_ref"] in {
                        "semantic:p3:target", "semantic:p3:target:replacement"}:
                        if state["semantic_item_ref"] == "semantic:p3:target" and state["status"] == "revoked":
                            state["valid_until"] = REPORT_DATE
                        if state["semantic_item_ref"] == "semantic:p3:target:replacement":
                            state["valid_from"] = REPORT_DATE
                            state["proposition"] = p3["content"]

        # Checkpoints include all captured, independently represented runtime items.
        # The auxiliary snapshot is not duplicated when it is already evidence for
        # the same semantic item (the independent-support deletion cases).
        for checkpoint_request, checkpoint_gold in zip(
                history["checkpoint_requests"], history["evaluator_only"]["checkpoint_gold"]):
            assert checkpoint_request["checkpoint_id"] == checkpoint_gold["checkpoint_id"]
            after = checkpoint_request["after_sequence"]
            state_refs = {item["semantic_item_ref"] for item in checkpoint_gold["current_state"]}
            for snapshot in history["candidate_snapshots"]:
                if snapshot["captured_after_sequence"] > after or not snapshot["snapshot_id"].endswith("-snapshot-aux"):
                    continue
                source_ids = set(snapshot["source_event_ids"])
                if any(source_ids.issubset(set(item["evidence_ids"]))
                       for item in checkpoint_gold["current_state"]):
                    continue
                suffix = snapshot["snapshot_id"].split("-p", 1)[1].split("-", 1)[0]
                semantic_ref = f"semantic:p{suffix}:aux"
                if semantic_ref in state_refs:
                    continue
                payload = snapshot["canonical_payload"]
                checkpoint_gold["current_state"].append({
                    "semantic_item_ref": semantic_ref,
                    **{key: payload[key] for key in (
                        "kind", "proposition", "scope", "status", "valid_from",
                        "valid_until", "epistemic_basis", "sensitivity")},
                    "evidence_ids": snapshot["source_event_ids"],
                    "counterevidence_ids": snapshot["counterevidence_event_ids"],
                })
                state_refs.add(semantic_ref)

            # Preserve deleted-source invalidation while explicitly citing the
            # lifecycle event that establishes the current invalidated status.
            for derivative in checkpoint_gold["invalidated_derivatives"]:
                for state in checkpoint_gold["current_state"]:
                    if state["semantic_item_ref"] == derivative["derivative_id"]:
                        event_id = derivative["invalidated_by_event_id"]
                        if event_id not in state["evidence_ids"]:
                            state["evidence_ids"].append(event_id)

            # Gold history is exhaustive through the checkpoint, including source
            # assertions and evaluated observations; lifecycle control events are
            # state transitions, not assertions in their own right.
            lifecycle_targets: dict[str, str] = {}
            for event in history["timeline"]:
                if event["sequence"] > after:
                    continue
                if event["event_type"] in {"deletion", "redaction"}:
                    status = "deleted" if event["event_type"] == "deletion" else "redacted"
                    for target in event["deletion_target_ids"]:
                        lifecycle_targets[target] = status
            assertions = []
            for event in history["timeline"]:
                if (event["sequence"] > after or event["event_type"] not in
                        {"message", "observation", "action_outcome"} or not event["content"]):
                    continue
                assertions.append({
                    "assertion_id": f"{event['event_id']}-assertion",
                    "proposition": event["content"],
                    "asserted_at": event["occurred_at"],
                    "source_event_ids": [event["event_id"]],
                    "source_status": lifecycle_targets.get(event["event_id"], "present"),
                })
            checkpoint_gold["historical_assertions"] = assertions

        checkpoint_by_id = {
            item["checkpoint_id"]: item
            for item in history["evaluator_only"]["checkpoint_gold"]}
        task_checkpoint = {item["task_id"]: item["checkpoint_id"]
                           for item in history["downstream_tasks"]}
        for task_gold in history["evaluator_only"]["downstream_task_gold"]:
            checkpoint = checkpoint_by_id[task_checkpoint[task_gold["task_id"]]]
            state_by_ref = {item["semantic_item_ref"]: item
                            for item in checkpoint["current_state"]}
            for answer in task_gold["gold_response"].get("current_state", []):
                state = state_by_ref[answer["semantic_item_ref"]]
                answer["proposition"] = state["proposition"]
                answer["evidence_ids"] = list(state["evidence_ids"])

        history["feature_tags"] = sorted({
            tag for gold in history["evaluator_only"]["pair_gold"]
            for tag in gold["feature_tags"]})


def _generate() -> list[dict[str, Any]]:
    histories = v06._generate()
    _revise_semantics(histories)
    validate_corpus(histories)
    validate_development_pilot_coverage(histories)
    return histories


def _write(output: Path, histories: list[dict[str, Any]], leakage: dict[str, Any]) -> None:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    base.write(output, histories)
    card_path = output / "dataset-card.md"
    card = card_path.read_text(encoding="utf-8")
    card = card.replace("development pilot v0.2", "development pilot v0.7")
    card = card.replace("pilot-v0.2", "pilot-v0.7")
    card = card.replace("scripts/generate_g3_development_pilot.py",
                        "scripts/generate_g3_development_pilot_v07.py")
    card = card.replace(
        "Relationship counts are mechanically balanced at 20 pairs per class to exercise the instrument; this balance is not intended to estimate real-world prevalence.",
        "Relationship counts are mechanically controlled for instrument coverage, not prevalence: supports 27, supersedes 13, and 20 pairs in each other class.")
    card = card.replace(
        "Every history and pair remains pending human review.",
        "Every history and pair remains pending human review. Checkpoint gold is exhaustive "
        "over authorized assertions and captured independent state through each checkpoint. "
        f"System-facing projection canary check: {leakage['leakage_failures']} failures "
        f"across {sum(leakage['checked_projection_counts'].values())} projections.")
    card_path.write_text(card, encoding="utf-8")

    diagnostic_path = output / "projection-leakage.json"
    diagnostic_path.write_bytes(canonical_bytes(leakage) + b"\n")
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["dataset_version"] = "pilot-v0.7"
    manifest["status"] = ("AWAITING_HUMAN_REVIEW" if leakage["passed"]
                          else "PROJECTION_LEAKAGE_FAILED")
    manifest["files"].append({**file_manifest_entry(diagnostic_path),
                              "path": diagnostic_path.name})
    for entry in manifest["files"]:
        fresh = file_manifest_entry(output / entry["path"],
                                    record_count=entry.get("record_count"))
        entry["bytes"], entry["sha256"] = fresh["bytes"], fresh["sha256"]
    manifest["source_files"].append({
        **file_manifest_entry(ROOT / "scripts/generate_g3_development_pilot_v07.py"),
        "path": "scripts/generate_g3_development_pilot_v07.py"})
    manifest_path.write_bytes(canonical_bytes(manifest) + b"\n")
    (output / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_path.read_bytes())}  manifest.json\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    histories = _generate()
    leakage = check_projection_leakage(histories)
    _write(args.output, histories, leakage)
    print(json.dumps({"histories": len(histories),
                      "pairs": sum(len(item["pair_inputs"]) for item in histories),
                      "projection_leakage": leakage,
                      "output": str(args.output)}, indent=2))
    if not leakage["passed"]:
        raise SystemExit("system-facing projection leakage detected")


if __name__ == "__main__":
    main()
