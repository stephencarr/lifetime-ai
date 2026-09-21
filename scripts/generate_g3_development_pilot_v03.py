from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import (
    canonical_bytes, file_manifest_entry, sha256_bytes,
)
from lifetime_ai.evaluation.coverage import validate_development_pilot_coverage
from lifetime_ai.evaluation.validation import validate_corpus
from scripts import generate_g3_development_pilot as base
from scripts.check_g3_text_leakage import check_text_leakage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evaluation" / "corpus" / "pilot-v0.3"
SEED = "g3-development-pilot-v0.3-fixed"
RELATIONSHIPS = base.RELATIONSHIPS
_ORIGINAL_PAIR_SPEC = base._pair_spec
_RELATION_SCHEDULE: dict[tuple[int, int], str] = {}
_OCCURRENCES: Counter[str] = Counter()


def _make_schedule() -> None:
    rng = random.Random(SEED)
    for family_number in range(1, 11):
        labels = [relationship for relationship in RELATIONSHIPS
                  for _ in range(2)]
        rng.shuffle(labels)
        family_histories = (family_number, family_number + 10, family_number + 20)
        for history_offset, history_index in enumerate(family_histories):
            for lane, relationship in enumerate(
                    labels[history_offset * 4:(history_offset + 1) * 4]):
                _RELATION_SCHEDULE[(history_index, lane)] = relationship


def _event_text(spec: dict[str, Any], history_index: int, lane: int) -> str | None:
    relation = spec["relationship"]
    subject, old, new, condition = (
        spec["subject"], spec["old"], spec["new"], spec["condition"])
    source = base.STYLE_SOURCES[(history_index * 7 + lane * 3)
                                % len(base.STYLE_SOURCES)]
    rng = random.Random(f"{SEED}:{history_index}:{lane}:{relation}")

    if spec["event_type"] in {"deletion", "time_advance"}:
        # These lifecycle controls are represented by typed event fields and target IDs.
        return None

    if relation in {"supports", "contradicts", "narrows_scope", "supersedes"}:
        value = old if relation == "supports" else new
        frames = (
            f"The {source} records {value} for {subject}.",
            f"For {subject}, the {source} gives {value} as the value.",
            f"The listed {subject} value is {value}, according to the {source}.",
            f"The {source} reports that {subject} uses {value}.",
        )
        return rng.choice(frames)

    if relation == "unrelated":
        frames = (
            "The facilities log recorded a brief power interruption during the morning shift.",
            "A staff update described road delays near the office after overnight construction.",
            "The maintenance note recorded a delivery arriving later than scheduled.",
            "The review notes mention a change to the meeting room booking for Friday.",
            "The daily report records that the test laboratory was closed for routine cleaning.",
        )
        return rng.choice(frames)

    frames = (
        f"That choice belongs to the case the previous entry described, though the entry itself is not identified here.",
        f"Proceed with the second configuration in the applicable context, whose boundaries are not stated in the message.",
        f"The selected arrangement depends on which request is meant; the current note gives no distinguishing detail.",
        f"A setting is referenced for one situation, but neither the situation nor its value is named in context.",
        f"The instruction points back to an earlier example without making clear which example should govern this request.",
    )
    return rng.choice(frames)


def _pair_spec(history_index: int, lane: int, _relationship: str,
               topic: tuple[str, str, str, str], _occurrence: int) -> dict[str, Any]:
    relation = _RELATION_SCHEDULE[(history_index, lane)]
    occurrence = _OCCURRENCES[relation]
    _OCCURRENCES[relation] += 1
    spec = _ORIGINAL_PAIR_SPEC(history_index, lane, relation, topic, occurrence)
    spec["event"] = _event_text(spec, history_index, lane)
    if relation == "narrows_scope":
        spec["event_metadata"]["scope"] = spec["scoped_scope"]
    if relation == "supersedes":
        spec["event_metadata"]["effective_from"] = base.EVENT_TIME
    if relation == "contradicts" and occurrence % 3 != 1:
        if occurrence % 3 == 0:
            spec.update(
                authorized=True, actor="system", disposition="accept",
                effect="close_and_replace", action="none",
                replacement_status="active",
                authority_reason="authorized source with explicit precedence",
            )
            spec["event_metadata"]["precedence_rank"] = 1
        else:
            spec.update(disposition="abstain", effect="preserve_conflict",
                        action="clarify")
    if relation == "supports" and spec["disposition"] == "reject_invalid":
        # Invalidity is machine-readable metadata, not a phrase in event prose.
        spec["event_metadata"] = {
            "valid_from": "2026-10-01T00:00:00Z",
            "valid_until": "2026-09-01T00:00:00Z",
        }
    return spec


def _generate() -> list[dict[str, Any]]:
    _make_schedule()
    _OCCURRENCES.clear()
    original_coverage_check = base.validate_development_pilot_coverage
    base._pair_spec = _pair_spec
    # The base generator validates while still carrying v0.2's template-level
    # expected-favors labels. Validate the final v0.3 corpus below instead.
    base.validate_development_pilot_coverage = lambda _histories: None
    try:
        histories = base.generate()
    finally:
        base._pair_spec = _ORIGINAL_PAIR_SPEC
        base.validate_development_pilot_coverage = original_coverage_check

    for history in histories:
        history["dataset_version"] = "pilot-v0.3"
        history["evaluator_only"]["generation_and_review_provenance"]["generator"] = (
            "scripts/generate_g3_development_pilot_v03.py")
        history["family_id"] = history["family_id"].replace(
            "template-family", "surface-family")
        feature_set = set(history["feature_tags"])
        expected_favors = (
            "architecture" if feature_set & {"source_deletion", "unauthorized_injection_text"}
            else "baseline_b" if "explicit_expiry" in feature_set
            else "baseline_c" if "genuine_ambiguity" in feature_set
            else "baseline_a"
        )
        history["evaluator_only"]["expected_favors"] = expected_favors
        history["evaluator_only"]["expected_favors_rationale"] = (
            "Lifecycle deletion or unauthorized input requires provenance-aware state handling."
            if expected_favors == "architecture" else
            "Explicit expiry is naturally handled by a conventional scheduler."
            if expected_favors == "baseline_b" else
            "The history contains ambiguity where a cautious general model may be strongest."
            if expected_favors == "baseline_c" else
            "The short local history is likely handled adequately by rolling summary and retrieval."
        )
        events = {event["event_id"]: event for event in history["timeline"]}
        for event in history["timeline"]:
            if event["event_type"] == "deletion":
                event["content"] = "The event was recorded at the stated time."
        checkpoints = {item["checkpoint_id"]: item
                       for item in history["evaluator_only"]["checkpoint_gold"]}
        tasks = {task["task_id"]: task for task in history["downstream_tasks"]}
        for task_gold in history["evaluator_only"]["downstream_task_gold"]:
            task = tasks[task_gold["task_id"]]
            if task["task_type"] != "deletion_query":
                continue
            checkpoint = checkpoints[task["checkpoint_id"]]
            refs = set(task["target_scope"]["semantic_item_refs"])
            task_gold["gold_response"]["invalidated_derivatives"] = [
                {"semantic_item_ref": item["derivative_id"],
                 "invalidated_by_event_id": item["invalidated_by_event_id"],
                 "reason": item["reason"]}
                for item in checkpoint["invalidated_derivatives"]
                if item["derivative_id"] in refs
                and events[item["invalidated_by_event_id"]]["event_type"] == "deletion"
            ]

    validate_corpus(histories)
    validate_development_pilot_coverage(histories)
    return histories


def _write(output: Path, histories: list[dict[str, Any]], probe: dict[str, Any]) -> None:
    if output.exists() and any(output.iterdir()):
        marker = output / "manifest.json"
        if not marker.exists():
            raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
        previous = json.loads(marker.read_text(encoding="utf-8"))
        if (previous.get("dataset_version") != "pilot-v0.2"
                or not any(item.get("path") ==
                           "scripts/generate_g3_development_pilot.py"
                           for item in previous.get("source_files", []))):
            raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    base.write(output, histories)

    card_path = output / "dataset-card.md"
    card = card_path.read_text(encoding="utf-8")
    card = card.replace("development pilot v0.2", "development pilot v0.3")
    card = card.replace("pilot-v0.2", "pilot-v0.3")
    card = card.replace("scripts/generate_g3_development_pilot.py",
                        "scripts/generate_g3_development_pilot_v03.py")
    card = card.replace("No model predictions, proprietary data",
                        "No semantic model predictions, proprietary data")
    card = card.replace(
        "Every history and pair remains pending human review.",
        "Every history and pair remains pending human review. The text-only leakage gate "
        f"scores {probe['metrics']['relationship']['accuracy']} for relationship and "
        f"{probe['metrics']['disposition']['accuracy']} for disposition on "
        "family-disjoint pilot partitions.")
    card_path.write_text(card, encoding="utf-8")

    probe_path = output / "leakage-probe.json"
    probe_path.write_bytes(canonical_bytes(probe) + b"\n")
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["dataset_version"] = "pilot-v0.3"
    manifest["status"] = ("AWAITING_HUMAN_REVIEW" if probe["passed"]
                          else "LEAKAGE_GATE_FAILED")
    manifest["files"].append({**file_manifest_entry(probe_path),
                              "path": "leakage-probe.json"})
    for entry in manifest["files"]:
        path = output / entry["path"]
        refreshed = file_manifest_entry(path, record_count=entry.get("record_count"))
        entry["bytes"] = refreshed["bytes"]
        entry["sha256"] = refreshed["sha256"]
    manifest["source_files"].append({
        **file_manifest_entry(ROOT / "scripts" / "generate_g3_development_pilot_v03.py"),
        "path": "scripts/generate_g3_development_pilot_v03.py",
    })
    manifest["source_files"].append({
        **file_manifest_entry(ROOT / "scripts" / "check_g3_text_leakage.py"),
        "path": "scripts/check_g3_text_leakage.py",
    })
    manifest_path.write_bytes(canonical_bytes(manifest) + b"\n")
    (output / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_path.read_bytes())}  manifest.json\n",
        encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    histories = _generate()
    probe = check_text_leakage(histories)
    _write(args.output, histories, probe)
    print(json.dumps({"histories": len(histories),
                      "pairs": sum(len(item["pair_inputs"]) for item in histories),
                      "probe": probe, "output": str(args.output)}, indent=2))
    if not probe["passed"]:
        raise SystemExit("text leakage gate failed; corpus is sealed as non-approvable")


if __name__ == "__main__":
    main()
