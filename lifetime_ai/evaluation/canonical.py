from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


CANONICAL_PROFILE = "lifetime-ai-canonical-json-v1"


class CanonicalizationError(ValueError):
    pass


def _validate(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise CanonicalizationError(f"binary floating-point value forbidden at {path}")
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(f"non-string key at {path}")
            _validate(item, f"{path}.{key}")
        return
    raise CanonicalizationError(f"unsupported value {type(value).__name__} at {path}")


def canonical_bytes(value: Any) -> bytes:
    _validate(value)
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def canonical_jsonl_bytes(records: Iterable[dict[str, Any]]) -> bytes:
    rows = [canonical_bytes(record) for record in records]
    return b"\n".join(rows) + (b"\n" if rows else b"")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def strict_json_loads(text: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise CanonicalizationError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def parse_int(raw: str) -> int:
        if raw == "-0":
            raise CanonicalizationError("negative zero forbidden")
        return int(raw)

    value = json.loads(text, object_pairs_hook=pairs, parse_int=parse_int,
                       parse_float=lambda raw: (_ for _ in ()).throw(
                           CanonicalizationError(f"binary floating-point JSON number forbidden: {raw}")))
    _validate(value)
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            value = strict_json_loads(line)
            if not isinstance(value, dict):
                raise CanonicalizationError(f"JSONL record {line_number} is not an object")
            records.append(value)
    return records


def file_manifest_entry(path: Path, *, record_count: int | None = None) -> dict[str, Any]:
    content = path.read_bytes()
    entry: dict[str, Any] = {
        "path": path.as_posix(),
        "bytes": len(content),
        "sha256": sha256_bytes(content),
    }
    if record_count is not None:
        entry["record_count"] = record_count
    return entry
