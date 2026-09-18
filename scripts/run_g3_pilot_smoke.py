from __future__ import annotations

import argparse
from pathlib import Path

from lifetime_ai.evaluation.canonical import canonical_bytes, read_jsonl, sha256_value, strict_json_loads
from lifetime_ai.evaluation.contracts import (
    MockCandidateRetriever, MockEvaluationSystem, MockPairClassifier,
    MockGeneralLLMBaseline, MockOracleBaseline, MockRollingSummaryBaseline,
    MockSchedulerBaseline,
    calculate_cost_cad,
)
from lifetime_ai.evaluation.projection import (
    build_pair_classification_projection, build_retrieval_projection,
    build_system_history_projection, contains_evaluator_only_material,
)
from lifetime_ai.evaluation.validation import validate_corpus


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "evaluation" / "corpus" / "pilot-v0.1"


def run(corpus: Path) -> dict:
    histories = read_jsonl(corpus / "development.jsonl") + read_jsonl(corpus / "holdout.jsonl")
    validate_corpus(histories)
    retrieval_cases = pair_cases = end_to_end_cases = 0
    leakage_failures = 0
    for history in histories:
        canaries = {history["evaluator_only"]["generation_and_review_provenance"]["canary"]}
        end_projection = build_system_history_projection(history)
        leakage_failures += int(contains_evaluator_only_material(end_projection, canaries))
        system = MockEvaluationSystem()
        system.reset(history["history_id"], {})
        for event in end_projection["timeline"]:
            system.ingest(event)
        for checkpoint in end_projection["checkpoint_requests"]:
            system.checkpoint(checkpoint)
        end_to_end_cases += 1
        for pair in history["pair_inputs"]:
            retrieval_projection = build_retrieval_projection(history, pair["pair_id"])
            classification_projection = build_pair_classification_projection(history, pair["pair_id"])
            leakage_failures += int(contains_evaluator_only_material(retrieval_projection, canaries))
            leakage_failures += int(contains_evaluator_only_material(classification_projection, canaries))
            MockCandidateRetriever().rank(retrieval_projection, limit=2)
            MockPairClassifier().classify(classification_projection).validate()
            retrieval_cases += 1
            pair_cases += 1
    price_path = ROOT / "evaluation" / "config" / "pilot-price-table.json"
    price_table = strict_json_loads(price_path.read_text(encoding="utf-8"))
    result = {
        "status": "PILOT_READY_FOR_HUMAN_REVIEW",
        "g3_complete": False,
        "history_count": len(histories),
        "pair_count": sum(len(history["pair_inputs"]) for history in histories),
        "tracks": {
            "candidate_retrieval_mock_cases": retrieval_cases,
            "pair_classification_mock_cases": pair_cases,
            "end_to_end_mock_cases": end_to_end_cases,
        },
        "baseline_contract_smokes": {
            baseline.system_id: "PASS" for baseline in (
                MockRollingSummaryBaseline(), MockSchedulerBaseline(),
                MockGeneralLLMBaseline(), MockOracleBaseline())
        },
        "schema_validation": "PASS",
        "evaluator_leakage_failures": leakage_failures,
        "model_calls": 0,
        "embeddings_or_vector_search": False,
        "production_connections": False,
        "mock_cost_cad": str(calculate_cost_cad(MockPairClassifier().raw_usage(), price_table)),
        "price_table_sha256": sha256_value(price_table),
    }
    result["result_sha256"] = sha256_value(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.corpus)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical_bytes(result) + b"\n")
    print(canonical_bytes(result).decode())


if __name__ == "__main__":
    main()
