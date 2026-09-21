"""Render the six original briefs as pending, provisionally development drafts."""
from __future__ import annotations

import argparse
from pathlib import Path

from lifetime_ai.evaluation.canonical import canonical_bytes, canonical_jsonl_bytes, file_manifest_entry
from lifetime_ai.evaluation.frozen_g4_pipeline import render_blueprint
from lifetime_ai.evaluation.initial_authoring import build_initial_blueprints


def render_initial_batch(output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite draft directory: {output}")
    blueprints = build_initial_blueprints()
    histories, specs = [], []
    for blueprint in blueprints:
        records, spec = render_blueprint(blueprint)
        histories.extend(records)
        specs.append(spec)
    output.mkdir(parents=True)
    registry = output / "blueprints"
    registry.mkdir()
    for blueprint in blueprints:
        (registry / f"{blueprint['family_id']}.json").write_bytes(canonical_bytes(blueprint) + b"\n")
    (output / "draft-histories.jsonl").write_bytes(canonical_jsonl_bytes(histories))
    (output / "draft-family-specs.jsonl").write_bytes(canonical_jsonl_bytes(specs))
    files = sorted(registry.glob("*.json")) + [output / "draft-histories.jsonl", output / "draft-family-specs.jsonl"]
    manifest = {"status": "DRAFT_PENDING_REVIEW_NOT_SEALED", "families": len(blueprints),
                "histories": len(histories), "pairs": sum(len(item["pair_inputs"]) for item in histories),
                "partition_note": "development is provisional; no final split or holdout assignment has occurred",
                "source": "lifetime_ai/evaluation/initial_authoring.py",
                "predictions_generated": False,
                "review_blockers": ["All 18 histories and 72 pair opportunities require independent blind review.",
                                    "Planning-matrix supplemental features and baseline affinities are not claimed by these brief-only drafts.",
                                    "This partial registry cannot be staged as a frozen corpus."],
                "files": [{**file_manifest_entry(path), "path": path.relative_to(output).as_posix()} for path in files]}
    (output / "draft-manifest.json").write_bytes(canonical_bytes(manifest) + b"\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = render_initial_batch(args.output)
    print(f"{result['status']}: {result['families']} families, {result['histories']} histories, {result['pairs']} pairs")
