from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, file_manifest_entry, sha256_bytes
from lifetime_ai.evaluation.coverage import validate_development_pilot_coverage
from lifetime_ai.evaluation.validation import validate_corpus
from scripts import generate_g3_development_pilot as base
from scripts import generate_g3_development_pilot_v04 as v04
from scripts.check_g3_projection_leakage import check_projection_leakage


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evaluation" / "corpus" / "pilot-v0.5"


def _generate() -> list[dict[str, Any]]:
    histories = v04._generate()
    for history in histories:
        history["dataset_version"] = "pilot-v0.5"
        history["family_id"] = history["family_id"].replace(
            "surface-v04-family", "surface-v05-family")
        history["evaluator_only"]["generation_and_review_provenance"]["generator"] = (
            "scripts/generate_g3_development_pilot_v05.py")
    validate_corpus(histories)
    validate_development_pilot_coverage(histories)
    return histories


def _write(output: Path, histories: list[dict[str, Any]],
           leakage: dict[str, Any]) -> None:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    base.write(output, histories)

    card_path = output / "dataset-card.md"
    card = card_path.read_text(encoding="utf-8")
    card = card.replace("development pilot v0.2", "development pilot v0.5")
    card = card.replace("pilot-v0.2", "pilot-v0.5")
    card = card.replace("scripts/generate_g3_development_pilot.py",
                        "scripts/generate_g3_development_pilot_v05.py")
    card = card.replace("No model predictions, proprietary data",
                        "No semantic model predictions, proprietary data")
    card = card.replace(
        "Every history and pair remains pending human review.",
        "Every history and pair remains pending human review. System-facing projection "
        f"canary check: {leakage['leakage_failures']} failures across "
        f"{sum(leakage['checked_projection_counts'].values())} projections. Statistical "
        "event-text accuracy is not treated as a leakage gate: relationship requires a "
        "candidate, while disposition is governed by structured policy inputs.")
    card_path.write_text(card, encoding="utf-8")

    diagnostic_path = output / "projection-leakage.json"
    diagnostic_path.write_bytes(canonical_bytes(leakage) + b"\n")
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["dataset_version"] = "pilot-v0.5"
    manifest["status"] = ("AWAITING_HUMAN_REVIEW" if leakage["passed"]
                          else "PROJECTION_LEAKAGE_FAILED")
    manifest["files"].append({**file_manifest_entry(diagnostic_path),
                              "path": diagnostic_path.name})
    for entry in manifest["files"]:
        fresh = file_manifest_entry(output / entry["path"],
                                    record_count=entry.get("record_count"))
        entry["bytes"], entry["sha256"] = fresh["bytes"], fresh["sha256"]
    for relpath in (
        "scripts/generate_g3_development_pilot_v04.py",
        "scripts/check_g3_v04_probes.py",
        "scripts/generate_g3_development_pilot_v05.py",
        "scripts/check_g3_projection_leakage.py",
    ):
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
