from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import (
    canonical_bytes,
    read_jsonl,
    sha256_value,
    strict_json_loads,
)
from lifetime_ai.evaluation.contracts import (
    MockCandidateRetriever,
    MockEvaluationSystem,
    MockGeneralLLMBaseline,
    MockOracleBaseline,
    MockPairClassifier,
    MockRollingSummaryBaseline,
    MockSchedulerBaseline,
    calculate_cost_cad,
)
from lifetime_ai.evaluation.frozen_g4 import validate_frozen_g4_coverage
from lifetime_ai.evaluation.frozen_g4_pipeline import verify_sealed_corpus
from lifetime_ai.evaluation.projection import (
    build_limited_oracle_projection,
    build_pair_classification_projection,
    build_retrieval_projection,
    build_system_history_projection,
    contains_forbidden_projection_key,
    contains_evaluator_only_material,
)
from lifetime_ai.evaluation.validation import CorpusValidationError


ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    value = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CorpusValidationError(f"expected JSON object at {path}")
    return value


def run(corpus: Path) -> dict[str, Any]:
    manifest = verify_sealed_corpus(corpus)
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed manifest must attest that model predictions are absent")
    histories = read_jsonl(corpus / "development.jsonl") + read_jsonl(corpus / "holdout.jsonl")
    family_specs = read_jsonl(corpus / "family-specs.jsonl")
    assignment = _load_json(corpus / "assignment-manifest.json")
    adjudication = _load_json(corpus / "near-duplicate-adjudication.json")
    validate_frozen_g4_coverage(
        histories,
        family_specs=family_specs,
        assignment_manifest=assignment,
        near_duplicate_adjudication=adjudication,
        require_sealing_artifacts=True,
    )
    if {history["reviewer_status"] for history in histories} - {"reviewed", "adjudicated"}:
        raise CorpusValidationError("every frozen history must be reviewed before G3 smoke")

    retrieval_cases = 0
    pair_cases = 0
    end_to_end_cases = 0
    leakage_failures = 0
    baseline_types = (
        MockRollingSummaryBaseline,
        MockSchedulerBaseline,
        MockGeneralLLMBaseline,
        MockOracleBaseline,
    )
    baseline_case_counts = {baseline().system_id: 0 for baseline in baseline_types}
    for history in histories:
        canary = history["evaluator_only"]["generation_and_review_provenance"]["canary"]
        end_projection = build_system_history_projection(history)
        leakage_failures += int(contains_evaluator_only_material(end_projection, {canary}))
        leakage_failures += int(contains_forbidden_projection_key(end_projection))
        system = MockEvaluationSystem()
        system.reset(history["history_id"], {})
        baselines = [baseline_type() for baseline_type in baseline_types]
        for baseline in baselines:
            baseline.reset(history["history_id"], {})
        next_event_index = 0
        ordered_events = sorted(end_projection["timeline"], key=lambda item: item["sequence"])
        for checkpoint in sorted(
            end_projection["checkpoint_requests"], key=lambda item: item["after_sequence"]
        ):
            while (next_event_index < len(ordered_events)
                   and ordered_events[next_event_index]["sequence"] <= checkpoint["after_sequence"]):
                event = ordered_events[next_event_index]
                system.ingest(event)
                for baseline in baselines:
                    baseline.ingest(event)
                next_event_index += 1
            system.checkpoint(checkpoint)
            for baseline in baselines:
                if isinstance(baseline, MockOracleBaseline):
                    baseline.configuration["limited_oracle_projection"] = (
                        build_limited_oracle_projection(
                            history, sequence=checkpoint["after_sequence"]
                        )
                    )
                baseline.checkpoint(checkpoint)
        end_to_end_cases += 1
        for baseline in baselines:
            baseline_case_counts[baseline.system_id] += 1
        for pair in history["pair_inputs"]:
            pair_id = pair["pair_id"]
            retrieval_projection = build_retrieval_projection(history, pair_id)
            classification_projection = build_pair_classification_projection(history, pair_id)
            leakage_failures += int(
                contains_evaluator_only_material(retrieval_projection, {canary})
            )
            leakage_failures += int(
                contains_evaluator_only_material(classification_projection, {canary})
            )
            leakage_failures += int(contains_forbidden_projection_key(retrieval_projection))
            leakage_failures += int(contains_forbidden_projection_key(classification_projection))
            MockCandidateRetriever().rank(retrieval_projection, limit=2)
            # Contract-only deterministic fixture. This is not a learned model
            # and its output is not scored or written to the corpus.
            MockPairClassifier().classify(classification_projection).validate()
            retrieval_cases += 1
            pair_cases += 1

    price_table = _load_json(ROOT / "evaluation" / "config" / "pilot-price-table.json")
    result: dict[str, Any] = {
        "status": "PASS" if leakage_failures == 0 else "FAIL",
        "g3_gate_decision": "NOT_RECORDED_BY_SMOKE",
        "corpus_manifest_sha256": manifest["manifest_sha256"],
        "history_count": len(histories),
        "pair_count": sum(len(history["pair_inputs"]) for history in histories),
        "tracks": {
            "candidate_retrieval_contract_cases": retrieval_cases,
            "pair_classification_contract_cases": pair_cases,
            "end_to_end_contract_cases": end_to_end_cases,
        },
        "baseline_contract_smokes": {
            system_id: "PASS" for system_id in baseline_case_counts
        },
        "baseline_contract_cases": baseline_case_counts,
        "schema_semantic_coverage_validation": "PASS",
        "evaluator_leakage_failures": leakage_failures,
        "learned_model_calls": 0,
        "embeddings_or_vector_search": False,
        "production_connections": False,
        "mock_cost_cad": str(calculate_cost_cad(MockPairClassifier().raw_usage(), price_table)),
        "price_table_sha256": sha256_value(price_table),
    }
    result["result_sha256"] = sha256_value(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run model-free G3 contract and leakage smoke checks on a sealed corpus"
    )
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.corpus)
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite smoke evidence: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical_bytes(result) + b"\n")
    print(canonical_bytes(result).decode())


if __name__ == "__main__":
    main()
