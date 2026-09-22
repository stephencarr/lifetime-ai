"""Development-only corpus check that never opens the holdout payload.

This is intentionally narrower than full sealed-corpus verification: it
authenticates the pinned manifest and development JSONL, not the holdout or
every sealed source file. Use the full verifier only with holdout access.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import sha256_bytes, sha256_value, strict_json_loads
from .validation import CorpusValidationError


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION_PATH = ROOT / "evaluation" / "config" / "g4-development-authorization.json"


def verify_g4_development_partition(corpus: Path) -> dict[str, Any]:
    """Verify only the pinned manifest and development partition bytes."""
    authorization = strict_json_loads(AUTHORIZATION_PATH.read_text(encoding="utf-8"))
    manifest_bytes = (corpus / "manifest.json").read_bytes()
    manifest = strict_json_loads(manifest_bytes.decode("utf-8"))
    if not isinstance(manifest, dict) or manifest.get("state") != "SEALED":
        raise CorpusValidationError("development input requires a sealed manifest")
    material = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if manifest.get("manifest_sha256") != sha256_value(material):
        raise CorpusValidationError("manifest content hash mismatch")
    if manifest["manifest_sha256"] != authorization.get("corpus_manifest_sha256"):
        raise CorpusValidationError("manifest differs from development authorization pin")
    sidecar = (corpus / "manifest.sha256").read_text(encoding="utf-8").strip().split()
    if sidecar != [sha256_bytes(manifest_bytes), "manifest.json"]:
        raise CorpusValidationError("manifest checksum sidecar mismatch")
    if manifest.get("model_predictions_present") is not False:
        raise CorpusValidationError("sealed corpus must be prediction-free")

    entries = [entry for entry in manifest.get("files", [])
               if isinstance(entry, dict) and entry.get("path") == "development.jsonl"]
    if len(entries) != 1:
        raise CorpusValidationError("manifest must contain one development payload entry")
    entry = entries[0]
    development_bytes = (corpus / "development.jsonl").read_bytes()
    if len(development_bytes) != entry.get("bytes"):
        raise CorpusValidationError("development payload byte count mismatch")
    if sha256_bytes(development_bytes) != entry.get("sha256"):
        raise CorpusValidationError("development payload hash mismatch")
    if len(development_bytes.splitlines()) != entry.get("record_count"):
        raise CorpusValidationError("development payload record count mismatch")
    return manifest
