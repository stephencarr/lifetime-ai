"""Render the complete matrix-bound frozen-G4 blueprint registry.

This writes pending-review blueprints only. It cannot approve, split, seal, or
run model predictions against the corpus.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from lifetime_ai.evaluation.canonical import canonical_bytes, file_manifest_entry
from lifetime_ai.evaluation.initial_authoring import build_blueprints


def render_registry(output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite blueprint registry: {output}")
    blueprints = build_blueprints()
    output.mkdir(parents=True)
    for blueprint in blueprints:
        path = output / f"{blueprint['family_id']}.json"
        path.write_bytes(canonical_bytes(blueprint) + b"\n")
    manifest = {
        "status": "DRAFT_PENDING_INDEPENDENT_REVIEW",
        "families": len(blueprints),
        "histories": sum(len(item["histories"]) for item in blueprints),
        "pairs": sum(
            len(history["pair_inputs"])
            for item in blueprints for history in item["histories"]
        ),
        "model_predictions_present": False,
        "files": [
            {**file_manifest_entry(path), "path": path.name}
            for path in sorted(output.glob("*.json"))
        ],
    }
    (output.parent / f"{output.name}-manifest.json").write_bytes(
        canonical_bytes(manifest) + b"\n"
    )
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = render_registry(args.output)
    print(
        f"{result['status']}: {result['families']} families, "
        f"{result['histories']} histories, {result['pairs']} pairs"
    )
