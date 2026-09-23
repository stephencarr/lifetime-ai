import mailbox
from email.message import EmailMessage

from scripts.inspect_mbox_local import inventory


def test_mbox_inventory_does_not_promote_quoted_or_attached_text(tmp_path):
    path = tmp_path / "sample.mbox"
    box = mailbox.mbox(path)
    message = EmailMessage()
    message["From"] = "example@example.invalid"
    message["Message-ID"] = "<synthetic-1@example.invalid>"
    message.set_content("I prefer concise answers.\n\nOn Tuesday, Alex wrote:\n> I prefer tea.")
    message.add_attachment(b"I prefer secret attachments", maintype="application",
                           subtype="octet-stream", filename="attachment.bin")
    box.add(message)
    box.flush()
    box.close()

    summary = inventory(path)
    assert summary["counts"]["messages"] == 1
    assert summary["counts"]["first_person_cue_candidates"] == 1
    assert summary["counts"]["attachments_skipped"] == 1
    assert summary["candidate_previews"] == []

    preview = inventory(path, preview_limit=1)["candidate_previews"][0]["authored_preview"]
    assert preview == "I prefer concise answers."


def test_sent_label_and_wrapped_quote_boundary(tmp_path):
    path = tmp_path / "wrapped.mbox"
    box = mailbox.mbox(path)
    message = EmailMessage()
    message["From"] = "self@example.invalid"
    message["Message-ID"] = "<synthetic-2@example.invalid>"
    message["X-Gmail-Labels"] = "INBOX,Sent"
    message.set_content("I need a refund.\n\nOn Tuesday, Alex <\nfriend@example.invalid> wrote:\nI prefer tea.")
    box.add(message)
    box.flush()
    box.close()

    summary = inventory(path, preview_limit=1)
    assert summary["counts"]["sent_labeled_messages"] == 1
    assert summary["counts"]["sent_labeled_cue_candidates"] == 1
    assert summary["candidate_previews"][0]["authored_preview"] == "I need a refund."
