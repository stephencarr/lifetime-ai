"""Hybrid FTS5 + local embedding/HNSW candidate retrieval for model claims."""

from __future__ import annotations

import hashlib
import json
import struct

import numpy as np
from usearch.index import Index

from .local_models import LocalEmbedder
from .store import Store


def _key(item_id: str) -> int:
    return int.from_bytes(hashlib.sha256(item_id.encode()).digest()[:8], "big") & ((1 << 63) - 1)


def _stored_embedding(row: object) -> list[float]:
    if row["embedding_format"] == "f16le-v1":
        raw = row["embedding"]
        if not isinstance(raw, bytes) or len(raw) != 768:
            raise ValueError("invalid packed model embedding")
        return list(struct.unpack("<384e", raw))
    if row["embedding_format"] == "json-v1":
        result = json.loads(row["embedding"])
        if not isinstance(result, list) or len(result) != 384:
            raise ValueError("invalid legacy model embedding")
        return result
    raise ValueError("unsupported model embedding format")


class ModelRetriever:
    """Rebuilds the disposable ANN index from canonical live SQLite state.

    Query search uses HNSW, never a vector scan. The rebuild cost is explicit
    and must be measured before any large-state claim.
    """

    def __init__(self, store: Store, embedder: LocalEmbedder):
        self.store = store
        self.embedder = embedder
        self.index = Index(ndim=384, metric="cos", dtype="f16",
                           connectivity=16, expansion_add=128, expansion_search=96)
        self.by_key: dict[int, str] = {}
        for row in store.iter_model_active_rows():
            self.add(row["item_id"], _stored_embedding(row))

    def add(self, item_id: str, vector: list[float]) -> None:
        key = _key(item_id)
        if key in self.by_key and self.by_key[key] != item_id:
            raise RuntimeError("model ANN key collision")
        if key in self.by_key:
            self.index.remove(key)
        self.index.add(key, np.asarray(vector, dtype=np.float32))
        self.by_key[key] = item_id

    def remove(self, item_id: str) -> None:
        key = _key(item_id)
        if self.by_key.get(key) == item_id:
            self.index.remove(key)
            del self.by_key[key]

    def candidates(self, query: str, *, lexical_k: int = 24,
                   semantic_k: int = 24, final_k: int = 16) -> list[object]:
        if not query.strip():
            return []
        # Model availability is required even when FTS finds a match. There is
        # no silent keyword-only product mode.
        vector = self.embedder.embed([query])[0]
        semantic = []
        if self.by_key:
            matches = self.index.search(np.asarray(vector, dtype=np.float32),
                                        min(semantic_k, len(self.by_key)))
            semantic = [self.by_key[int(match.key)] for match in matches
                        if int(match.key) in self.by_key]
        lexical = self.store.model_lexical_candidates(query, lexical_k)
        scores: dict[str, float] = {}
        for ranked in (semantic, lexical):
            for position, item_id in enumerate(ranked):
                scores[item_id] = scores.get(item_id, 0.0) + 1 / (60 + position + 1)
        ids = sorted(scores, key=lambda item_id: (-scores[item_id], item_id))
        rows = []
        for item_id in ids:
            row = self.store.model_row(item_id)
            if row is not None:
                rows.append(row)
            if len(rows) >= final_k:
                break
        return rows
