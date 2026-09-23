from lifetime_ai.uat import sources_from_mbox_text


def test_mbox_import_extracts_headers_and_plain_text_without_writing():
    raw = """From sender@example.test Tue Sep 22 10:00:00 2026
Subject: Synthetic email decision
From: Sender <sender@example.test>
To: Team <team@example.test>
Date: Tue, 22 Sep 2026 10:00:00 +0000
Message-ID: <one@example.test>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

We decided to keep the project log current.
"""
    sources = sources_from_mbox_text(raw)
    assert sources[0].title == "Synthetic email decision"
    assert "project log" in sources[0].excerpt
    assert "sender@example.test" in sources[0].context
