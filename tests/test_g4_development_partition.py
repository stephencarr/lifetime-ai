import json

import pytest

from lifetime_ai.evaluation import g4_development
from lifetime_ai.evaluation.canonical import canonical_bytes, sha256_bytes, sha256_value
from lifetime_ai.evaluation.validation import CorpusValidationError


def _corpus_without_holdout(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    development = b"{}\n"
    (corpus / "development.jsonl").write_bytes(development)
    material = {
        "state": "SEALED",
        "model_predictions_present": False,
        "files": [
            {"path": "development.jsonl", "bytes": len(development),
             "sha256": sha256_bytes(development), "record_count": 1},
            {"path": "holdout.jsonl", "bytes": 999,
             "sha256": "0" * 64, "record_count": 1},
        ],
    }
    manifest = {**material, "manifest_sha256": sha256_value(material)}
    manifest_bytes = canonical_bytes(manifest)
    (corpus / "manifest.json").write_bytes(manifest_bytes)
    (corpus / "manifest.sha256").write_text(
        f"{sha256_bytes(manifest_bytes)}  manifest.json\n", encoding="utf-8"
    )
    auth = tmp_path / "authorization.json"
    auth.write_text(json.dumps({"corpus_manifest_sha256": manifest["manifest_sha256"]}),
                    encoding="utf-8")
    monkeypatch.setattr(g4_development, "AUTHORIZATION_PATH", auth)
    return corpus


def test_development_verification_does_not_require_or_open_holdout(tmp_path, monkeypatch):
    corpus = _corpus_without_holdout(tmp_path, monkeypatch)
    assert not (corpus / "holdout.jsonl").exists()
    manifest = g4_development.verify_g4_development_partition(corpus)
    assert manifest["state"] == "SEALED"


def test_development_verification_rejects_tampered_bytes(tmp_path, monkeypatch):
    corpus = _corpus_without_holdout(tmp_path, monkeypatch)
    (corpus / "development.jsonl").write_bytes(b"{\"changed\":true}\n")
    with pytest.raises(CorpusValidationError, match="development payload"):
        g4_development.verify_g4_development_partition(corpus)


def test_development_verification_enforces_authorization_pin(tmp_path, monkeypatch):
    corpus = _corpus_without_holdout(tmp_path, monkeypatch)
    g4_development.AUTHORIZATION_PATH.write_text(
        json.dumps({"corpus_manifest_sha256": "0" * 64}), encoding="utf-8"
    )
    with pytest.raises(CorpusValidationError, match="authorization pin"):
        g4_development.verify_g4_development_partition(corpus)
