import pytest

from lifetime_ai.uat import sources_from_json_payload


def test_source_json_import_is_narrow_and_typed():
    sources = sources_from_json_payload({
        "format": "lifetime-ai-uat-sources/v1",
        "sources": [{
            "source_id": "local:1",
            "title": "Note",
            "occurred_at": "2026-09-22",
            "context": "Test",
            "excerpt": "A short approved note.",
        }],
    })
    assert sources[0].source_id == "local:1"


def test_source_json_import_rejects_extra_fields():
    with pytest.raises(ValueError, match="unsupported fields"):
        sources_from_json_payload({
            "format": "lifetime-ai-uat-sources/v1",
            "sources": [{
                "source_id": "local:1", "title": "Note", "occurred_at": "2026-09-22",
                "context": "Test", "excerpt": "Approved", "gold_answer": "hidden",
            }],
        })
