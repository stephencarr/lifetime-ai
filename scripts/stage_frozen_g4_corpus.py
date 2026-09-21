from __future__ import annotations

import argparse
from pathlib import Path

from lifetime_ai.evaluation.frozen_g4_pipeline import (
    seal_staged_corpus,
    stage_blueprint_registry,
    verify_sealed_corpus,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a complete frozen-G4 blueprint registry into a new staging directory"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    stage = subparsers.add_parser("stage")
    stage.add_argument("--blueprints", type=Path, required=True)
    stage.add_argument("--authoring-matrix", type=Path, required=True)
    stage.add_argument("--output", type=Path, required=True)
    seal = subparsers.add_parser("seal")
    seal.add_argument("--staging", type=Path, required=True)
    seal.add_argument("--review-record", type=Path, required=True)
    seal.add_argument("--duplicate-adjudication", type=Path, required=True)
    seal.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--corpus", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "stage":
        manifest = stage_blueprint_registry(
            args.blueprints, args.authoring_matrix, args.output
        )
        print(
            "staged frozen-G4 corpus; not sealed; "
            f"registry={manifest['family_spec_registry_sha256']}"
        )
    elif args.command == "seal":
        manifest = seal_staged_corpus(
            args.staging, args.review_record, args.duplicate_adjudication, args.output
        )
        print(f"sealed frozen-G4 corpus; manifest={manifest['manifest_sha256']}")
    else:
        manifest = verify_sealed_corpus(args.corpus)
        print(f"verified sealed frozen-G4 corpus; manifest={manifest['manifest_sha256']}")


if __name__ == "__main__":
    main()
