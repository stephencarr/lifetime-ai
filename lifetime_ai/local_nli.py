"""Pinned, offline ONNX source-entailment classifier.

This classifier scores whether source text entails a proposed statement. It
does not decide whether a statement deserves durable storage on its own.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class NLIUnavailable(RuntimeError):
    pass


class LocalNLI:
    def __init__(self, lock_path: Path):
        self.lock = json.loads(lock_path.read_text())
        repository = self.lock["repository"]
        revision = self.lock["revision"]
        root = (Path.home() / ".cache/huggingface/hub" /
                ("models--" + repository.replace("/", "--")) / "snapshots" / revision)
        for name, expected in self.lock["files"].items():
            path = root / name
            if not path.is_file():
                raise NLIUnavailable(f"pinned NLI file missing: {name}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != expected:
                raise NLIUnavailable(f"pinned NLI file changed: {name}")
        config = json.loads((root / "config.json").read_text())
        if config.get("id2label") != {"0": "entailment", "1": "not_entailment"}:
            raise NLIUnavailable("unexpected NLI labels")
        self.tokenizer = Tokenizer.from_file(str(root / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=512)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 4
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(root / "onnx/model_int8.onnx"),
                                            sess_options=options,
                                            providers=["CPUExecutionProvider"])
        if [item.name for item in self.session.get_inputs()] != ["input_ids", "attention_mask"]:
            raise NLIUnavailable("unexpected NLI model inputs")

    def entailment_probability(self, source: str, hypothesis: str) -> float:
        if not source.strip() or not hypothesis.strip():
            raise ValueError("NLI source and hypothesis must be nonempty")
        encoded = self.tokenizer.encode(source, hypothesis)
        inputs = {
            "input_ids": np.asarray([encoded.ids], dtype=np.int64),
            "attention_mask": np.asarray([[1] * len(encoded.ids)], dtype=np.int64),
        }
        try:
            logits = self.session.run(["logits"], inputs)[0][0]
        except Exception as error:
            raise NLIUnavailable("local NLI inference failed") from error
        scores = np.asarray(logits, dtype=np.float64)
        if scores.shape != (2,) or not np.all(np.isfinite(scores)):
            raise NLIUnavailable("local NLI scores malformed")
        shifted = scores - scores.max()
        probabilities = np.exp(shifted) / np.exp(shifted).sum()
        result = float(probabilities[0])
        if not math.isfinite(result):
            raise NLIUnavailable("local NLI probability malformed")
        return result
