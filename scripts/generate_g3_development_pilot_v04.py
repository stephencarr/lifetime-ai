from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, file_manifest_entry, sha256_bytes
from lifetime_ai.evaluation.validation import validate_corpus
from scripts import generate_g3_development_pilot as base
from scripts import generate_g3_development_pilot_v03 as v03
from scripts.check_g3_v04_probes import check_probes


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evaluation" / "corpus" / "pilot-v0.4"
SEED = "g3-development-pilot-v0.4-fixed"


def _event_text(spec: dict[str, Any], history_index: int, lane: int) -> str | None:
    relation = spec["relationship"]
    if spec["event_type"] in {"deletion", "time_advance"}:
        return None
    subject = spec["subject"]
    source = base.STYLE_SOURCES[(history_index * 7 + lane * 3)
                                % len(base.STYLE_SOURCES)]
    rng = random.Random(f"{SEED}:{history_index}:{lane}:{relation}")

    if relation in {"supports", "contradicts"}:
        value = spec["old"] if relation == "supports" else spec["new"]
        frames = (
            f"The {source} lists {subject} with the value {value}.",
            f"For {subject}, the {source} gives {value} as the selected value.",
            f"The selected {subject} value is {value}, according to the {source}.",
            f"The {source} records {subject} as using {value}.",
        )
        return rng.choice(frames)

    if relation == "narrows_scope":
        condition, value = spec["condition"], spec["new"]
        frames = (
            f"For {condition}, the {source} specifies {value} for {subject}.",
            f"The {source} gives {subject} the value {value} within {condition}.",
            f"Within {condition}, {subject} uses {value}, according to the {source}.",
        )
        return rng.choice(frames)

    if relation == "supersedes":
        if spec["kind"] == "commitment":
            return (f"The completion record marks the {subject} migration to "
                    f"{spec['new']} finished today.")
        date = base.EVENT_TIME[:10]
        frames = (
            f"From {date}, the {source} says {subject} uses {spec['new']} instead of {spec['old']}.",
            f"The {source} replaces {spec['old']} with {spec['new']} for {subject}, effective {date}.",
            f"Effective {date}, {subject} uses {spec['new']} rather than {spec['old']}, per the {source}.",
        )
        return rng.choice(frames)

    if relation == "unrelated":
        # Keep the entity/topic words in play, but make the event about a
        # different property so the relation depends on the candidate.
        frames = (
            f"The {source} notes that {subject} appeared in the export index on Tuesday.",
            f"A {source} entry records the {subject} review as lasting twelve minutes.",
            f"For the {subject} record, the {source} lists two archived attachments.",
            f"The {source} says the {subject} dashboard had six viewers yesterday.",
        )
        return rng.choice(frames)

    # Natural short references retain real ambiguity without repeating the
    # previous conspicuous 'not stated / no distinguishing detail' template.
    frames = (
        f"Use the other {subject} option for that case.",
        f"Let's use the earlier {subject} choice for this one.",
        f"Apply the alternate {subject} setting to the same kind of request.",
        f"Switch it to the second {subject} configuration there.",
        f"Keep the preferred {subject} value for cases like that.",
    )
    return rng.choice(frames)


def _generate() -> list[dict[str, Any]]:
    old_text = v03._event_text
    v03._event_text = _event_text
    try:
        histories = v03._generate()
    finally:
        v03._event_text = old_text
    for history in histories:
        history["dataset_version"] = "pilot-v0.4"
        history["family_id"] = history["family_id"].replace(
            "surface-family", "surface-v04-family")
        history["evaluator_only"]["generation_and_review_provenance"]["generator"] = (
            "scripts/generate_g3_development_pilot_v04.py")
    validate_corpus(histories)
    return histories


def _write(output: Path, histories: list[dict[str, Any]], probe: dict[str, Any]) -> None:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    base.write(output, histories)

    card_path = output / "dataset-card.md"
    card = card_path.read_text(encoding="utf-8")
    card = card.replace("development pilot v0.2", "development pilot v0.4")
    card = card.replace("pilot-v0.2", "pilot-v0.4")
    card = card.replace("scripts/generate_g3_development_pilot.py",
                        "scripts/generate_g3_development_pilot_v04.py")
    card = card.replace("No model predictions, proprietary data",
                        "No semantic model predictions, proprietary data")
    card = card.replace(
        "Every history and pair remains pending human review.",
        "Every history and pair remains pending human review. Event-only relationship "
        f"shortcut diagnostic: {probe['relationship_shortcut_diagnostic']['accuracy']} "
        f"(limit {probe['relationship_shortcut_diagnostic']['limit']}); disposition "
        "event-only accuracy is diagnostic only because structured authority and validity "
        "inputs are required for that target.")
    card_path.write_text(card, encoding="utf-8")

    probe_path = output / "probe-diagnostics.json"
    probe_path.write_bytes(canonical_bytes(probe) + b"\n")
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["dataset_version"] = "pilot-v0.4"
    manifest["status"] = ("AWAITING_HUMAN_REVIEW"
                          if probe["gate_passed"] else "SHORTCUT_GATE_FAILED")
    manifest["files"].append({**file_manifest_entry(probe_path),
                              "path": "probe-diagnostics.json"})
    for entry in manifest["files"]:
        fresh = file_manifest_entry(output / entry["path"],
                                    record_count=entry.get("record_count"))
        entry["bytes"], entry["sha256"] = fresh["bytes"], fresh["sha256"]
    for relpath in ("scripts/generate_g3_development_pilot_v04.py",
                    "scripts/check_g3_v04_probes.py"):
        manifest["source_files"].append({
            **file_manifest_entry(ROOT / relpath), "path": relpath})
    manifest_path.write_bytes(canonical_bytes(manifest) + b"\n")
    (output / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_path.read_bytes())}  manifest.json\n",
        encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    histories = _generate()
    probe = check_probes(histories)
    _write(args.output, histories, probe)
    print(json.dumps({"histories": len(histories),
                      "pairs": sum(len(item["pair_inputs"]) for item in histories),
                      "probe": probe, "output": str(args.output)}, indent=2))
    if not probe["gate_passed"]:
        raise SystemExit("relationship shortcut gate failed; corpus is non-approvable")


if __name__ == "__main__":
    main()
