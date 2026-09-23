"""Frozen synthetic ANN capacity probe, separate from semantic M5 scoring."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import resource
import statistics
import tempfile
import time
from pathlib import Path

import numpy as np
from usearch.index import Index


ROOT = Path(__file__).resolve().parent.parent
INSTRUMENT_ROOT = ROOT / "evaluation/m5_index_scale"
RESULTS = ROOT / "experiments/m5_index_scale"


def _rss_gib() -> float:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return raw / (1024 ** 3 if platform.system() == "Darwin" else 1024 ** 2)


def _check(index: Index, probes: dict[int, np.ndarray], count: int,
           top_k: int) -> dict:
    times = []
    found = 0
    for key, vector in probes.items():
        start = time.monotonic()
        matches = index.search(vector, top_k)
        times.append(time.monotonic() - start)
        found += key in {int(match.key) for match in matches}
    ordered = sorted(times)
    return {"count": count, "planted_recall_at_k": [found, len(probes)],
            "query_p50_seconds": statistics.median(ordered),
            "query_p95_seconds": ordered[int(0.95 * (len(ordered) - 1))],
            "index_bytes": int(index.memory_usage), "peak_rss_gib": _rss_gib()}


def run(path: Path, instrument: Path) -> dict:
    raw = (instrument / "config.json").read_bytes()
    freeze = json.loads((instrument / "freeze.json").read_text())
    if hashlib.sha256(raw).hexdigest() != freeze["config_sha256"]:
        raise ValueError("frozen index-scale configuration changed")
    config = json.loads(raw)
    counts = config["counts"]
    rng = np.random.default_rng(config["seed"])
    targets = {count: {int(value) for value in np.linspace(
        0, count - 1, config["queries_per_count"], dtype=np.int64)}
               for count in counts}
    all_targets = set().union(*targets.values())
    planted: dict[int, np.ndarray] = {}
    index = Index(ndim=config["dimensions"], metric=config["metric"],
                  dtype=config["dtype"], connectivity=config["connectivity"],
                  expansion_add=config["expansion_add"],
                  expansion_search=config["expansion_search"])
    result = {"freeze": freeze, "config": config, "status": "running",
              "tiers": [], "scope": config["scope"]}
    path.write_text(json.dumps(result, indent=2) + "\n")
    current = 0
    started = time.monotonic()
    try:
        for count in counts:
            while current < count:
                size = min(config["batch_size"], count - current)
                vectors = rng.standard_normal((size, config["dimensions"]),
                                              dtype=np.float32)
                vectors /= np.maximum(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-12)
                keys = np.arange(current, current + size, dtype=np.uint64)
                for offset, key in enumerate(keys):
                    if int(key) in all_targets:
                        planted[int(key)] = vectors[offset].copy()
                index.add(keys, vectors)
                current += size
            probes = {key: planted[key] for key in targets[count]}
            tier = _check(index, probes, count, config["top_k"])
            tier["cumulative_build_seconds"] = time.monotonic() - started
            result["tiers"].append(tier)
            path.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(tier), flush=True)
        with tempfile.TemporaryDirectory(prefix="m5-hnsw-scale-") as scratch:
            index_path = Path(scratch) / "index.usearch"
            save_start = time.monotonic()
            index.save(index_path)
            result["persisted_index_bytes"] = index_path.stat().st_size
            result["save_seconds"] = time.monotonic() - save_start
            del index
            gc.collect()
            reloaded = Index(ndim=config["dimensions"], metric=config["metric"],
                             dtype=config["dtype"], connectivity=config["connectivity"],
                             expansion_add=config["expansion_add"],
                             expansion_search=config["expansion_search"])
            load_start = time.monotonic()
            reloaded.load(index_path)
            result["load_seconds"] = time.monotonic() - load_start
            result["reloaded"] = _check(reloaded,
                                        {key: planted[key] for key in targets[counts[-1]]},
                                        counts[-1], config["top_k"])
        last = result["tiers"][-1]
        result["gates"] = {
            "planted_recall": all(tier["planted_recall_at_k"][0] /
                                  tier["planted_recall_at_k"][1] >=
                                  config["minimum_planted_recall_at_k"]
                                  for tier in result["tiers"]),
            "query_p95": all(tier["query_p95_seconds"] <=
                             config["maximum_p95_query_seconds"] for tier in result["tiers"]),
            "peak_rss": last["peak_rss_gib"] <= config["maximum_peak_rss_gib"],
            "build_time": last["cumulative_build_seconds"] <=
                          config["maximum_total_build_seconds"],
        }
        result["passed"] = all(result["gates"].values())
        result["status"] = "complete"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = f"{type(error).__name__}: {error}"
    path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=("v0.1", "v0.2"), default="v0.1")
    args = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    attempt = 1
    prefix = "attempt-" if args.version == "v0.1" else f"{args.version}-attempt-"
    while (RESULTS / f"{prefix}{attempt:02d}.json").exists():
        attempt += 1
    path = RESULTS / f"{prefix}{attempt:02d}.json"
    result = run(path, INSTRUMENT_ROOT / args.version)
    print(json.dumps({"path": str(path), "status": result["status"],
                      "passed": result.get("passed"), "gates": result.get("gates"),
                      "error": result.get("error")}, indent=2))


if __name__ == "__main__":
    main()
