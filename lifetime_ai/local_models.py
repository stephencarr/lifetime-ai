"""Explicit loopback clients for pinned local generation and embeddings.

There is deliberately no rule or hosted-service fallback. Callers receive a
ModelUnavailable error and leave durable state unchanged when a model fails.
"""

from __future__ import annotations

import json
import hashlib
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


class ModelUnavailable(RuntimeError):
    pass


def _loopback_url(base: str) -> str:
    parsed = urlparse(base)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError("local model URL must use loopback HTTP")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment or not parsed.port:
        raise ValueError("local model URL must be an origin with an explicit port")
    return base.rstrip("/")


@dataclass(frozen=True)
class ModelResult:
    value: dict
    prompt_tokens: int
    completion_tokens: int


class LocalChatModel:
    def __init__(self, base_url: str, expected_model_id: str, *, timeout: int = 120):
        self.base_url = _loopback_url(base_url)
        self.expected_model_id = expected_model_id
        self.timeout = timeout

    def _request(self, path: str, body: dict | None = None) -> dict:
        request = urllib.request.Request(
            self.base_url + path,
            None if body is None else json.dumps(body).encode(),
            {"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except (OSError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            raise ModelUnavailable(f"local model request failed: {type(error).__name__}") from error

    def verify_identity(self) -> None:
        data = self._request("/v1/models")
        ids = {item.get("id") for item in data.get("data", [])}
        if self.expected_model_id not in ids:
            raise ModelUnavailable("unexpected local generation model")

    def structured(self, system: str, user: str, schema: dict, *, name: str,
                   max_tokens: int = 400) -> ModelResult:
        self.verify_identity()
        data = self._request("/v1/chat/completions", {
            "model": self.expected_model_id,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": 0,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_schema", "json_schema": {
                "name": name, "schema": schema, "strict": True}},
        })
        try:
            choice = data["choices"][0]
            if choice.get("finish_reason") != "stop":
                raise ValueError("generation incomplete")
            value = json.loads(choice["message"]["content"])
            if not isinstance(value, dict):
                raise ValueError("model returned no JSON object")
            usage = data.get("usage", {})
            return ModelResult(value, int(usage.get("prompt_tokens", 0)),
                               int(usage.get("completion_tokens", 0)))
        except (IndexError, KeyError, TypeError, ValueError) as error:
            raise ModelUnavailable("malformed or incomplete local model response") from error


class LocalEmbedder:
    def __init__(self, base_url: str, expected_model_id: str, *, timeout: int = 60):
        self.base_url = _loopback_url(base_url)
        self.expected_model_id = expected_model_id
        self.timeout = timeout

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        try:
            with urllib.request.urlopen(self.base_url + "/v1/models", timeout=self.timeout) as response:
                data = json.load(response)
            if self.expected_model_id not in {item.get("id") for item in data.get("data", [])}:
                raise ValueError("unexpected embedding model")
        except (OSError, TimeoutError, KeyError, ValueError) as error:
            raise ModelUnavailable("local embedding model identity unavailable") from error
        request = urllib.request.Request(
            self.base_url + "/v1/embeddings",
            json.dumps({"model": self.expected_model_id, "input": texts}).encode(),
            {"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.load(response)
            rows = sorted(data["data"], key=lambda item: item["index"])
            vectors = [item["embedding"] for item in rows]
            if len(vectors) != len(texts) or not all(len(v) == 384 for v in vectors):
                raise ValueError("unexpected embedding count or dimension")
            return [[float(value) for value in vector] for vector in vectors]
        except (OSError, TimeoutError, KeyError, TypeError, ValueError) as error:
            raise ModelUnavailable("local embedding model unavailable or malformed") from error


def locked_clients(lock_path: Path) -> tuple[LocalChatModel, LocalEmbedder, dict]:
    """Verify the exact cached GGUF files before connecting to loopback servers."""
    lock = json.loads(lock_path.read_text())
    hub = Path.home() / ".cache" / "huggingface" / "hub"
    for key in ("generator", "embedder"):
        item = lock[key]
        directory = "models--" + item["repository"].replace("/", "--")
        path = hub / directory / "snapshots" / item["revision"] / item["filename"]
        if not path.is_file():
            raise ModelUnavailable(f"pinned {key} weights are missing")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != item["sha256"]:
            raise ModelUnavailable(f"pinned {key} weights changed")
    generator = LocalChatModel(lock["generator"]["url"],
                               lock["generator"]["api_model_id"])
    generator.verify_identity()
    embedder = LocalEmbedder(lock["embedder"]["url"],
                             lock["embedder"]["api_model_id"])
    return generator, embedder, lock
