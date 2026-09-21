from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import (
    canonical_bytes, canonical_jsonl_bytes, file_manifest_entry, sha256_bytes,
)
from lifetime_ai.evaluation.coverage import validate_development_pilot_coverage
from lifetime_ai.evaluation.validation import review_content_sha256, validate_corpus


ROOT = Path(__file__).resolve().parents[1]
REVIEW_TEXT = (
    "Waived by project owner on 2026-09-19; independent agent review passed. "
    "No human review is claimed; see agent-review-record.md."
)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _write_reviewed_corpus(corpus: Path) -> list[dict[str, Any]]:
    manifest_path = corpus / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("dataset_version") != "pilot-v0.7":
        raise ValueError("this review record applies only to pilot-v0.7")
    if manifest.get("status") != "AWAITING_HUMAN_REVIEW":
        raise ValueError("refusing to reapply review to a corpus not awaiting review")

    histories = _read_jsonl(corpus / "development.jsonl")
    histories += _read_jsonl(corpus / "holdout.jsonl")
    if len(histories) != 30 or sum(len(item["pair_inputs"]) for item in histories) != 120:
        raise ValueError("unexpected pilot size; review record not applied")

    for history in histories:
        history["reviewer_status"] = "reviewed"
        provenance = history["evaluator_only"]["generation_and_review_provenance"]
        provenance["human_review"] = REVIEW_TEXT
        for gold in history["evaluator_only"]["pair_gold"]:
            gold["adjudication_status"] = "agreed"
        provenance["reviewed_content_sha256"] = review_content_sha256(history)

    validate_corpus(histories)
    validate_development_pilot_coverage(histories)
    for partition in ("development", "holdout"):
        selected = [item for item in histories
                    if item["partition"] == ("pilot_development" if partition == "development"
                                              else "pilot_holdout")]
        (corpus / f"{partition}.jsonl").write_bytes(canonical_jsonl_bytes(selected))

    packet_path = corpus / "reviews" / "pilot_review_packet.md"
    packet = packet_path.read_text(encoding="utf-8")
    packet = packet.replace(
        "Status: **awaiting human review** — 30 histories and 120 pairs generated for development-pilot review. G3 is not complete.",
        "Status: **agent review passed; human signoff waived by project owner** — 30 histories and 120 pairs reviewed. No human review is claimed. G3 is not complete. See `../agent-review-record.md`.")
    packet = packet.replace(
        "Pair decision: [ ] approve  [ ] revise  [ ] reject",
        "Pair decision: [x] approve  [ ] revise  [ ] reject")
    packet = packet.replace(
        "History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject",
        "History/checkpoint decision: [x] approve  [ ] revise  [ ] reject")
    packet = packet.replace(
        "Second review: [ ] required  [ ] complete",
        "Second review: agent review coverage documented in `../agent-review-record.md`; human signoff waived")
    packet_path.write_text(packet, encoding="utf-8")

    card_path = corpus / "dataset-card.md"
    card = card_path.read_text(encoding="utf-8")
    card = card.replace(
        "Status: awaiting human review. G3 is not complete.",
        "Status: independent agent review passed; human signoff waived by project owner. No human review is claimed. G3 is not complete. See `agent-review-record.md`.")
    card = card.replace(
        "Every history and pair remains pending human review.",
        "Every history and pair passed independent agent review; human signoff was waived by project owner.")
    card_path.write_text(card, encoding="utf-8")

    manifest["status"] = "AGENT_REVIEWED"
    record_path = corpus / "agent-review-record.md"
    if not any(item["path"] == record_path.name for item in manifest["files"]):
        manifest["files"].append({**file_manifest_entry(record_path),
                                  "path": record_path.name})
    for item in manifest["files"]:
        fresh = file_manifest_entry(corpus / item["path"],
                                    record_count=item.get("record_count"))
        item["bytes"], item["sha256"] = fresh["bytes"], fresh["sha256"]
    source = ROOT / "scripts" / "record_g3_agent_review.py"
    manifest["source_files"].append({**file_manifest_entry(source),
                                     "path": source.relative_to(ROOT).as_posix()})
    manifest_path.write_bytes(canonical_bytes(manifest) + b"\n")
    (corpus / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_path.read_bytes())}  manifest.json\n",
        encoding="utf-8")
    return histories


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path,
                        default=ROOT / "evaluation" / "corpus" / "pilot-v0.7")
    args = parser.parse_args()
    _write_reviewed_corpus(args.corpus)
    print(json.dumps({"status": "AGENT_REVIEWED", "histories": 30, "pairs": 120,
                      "human_signoff": "waived_by_owner", "g3_complete": False},
                     indent=2))


if __name__ == "__main__":
    main()
