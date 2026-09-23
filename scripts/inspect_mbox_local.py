"""Read-only, local inventory and candidate preview for an mbox archive.

This is an exploratory curation aid. It does not create durable state or score UAT.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from email.message import Message
from email.parser import BytesParser
from email.policy import default
from pathlib import Path


CUE = re.compile(r"\b(?:I prefer|I will|I need|I plan to|please keep|I now prefer)\b", re.I)
QUOTE_BOUNDARY = re.compile(
    r"^(?:On .+(?:wrote:|<\s*$)|From:|-----Original Message-----|[-]+ Forwarded message [-]+|Begin forwarded message:|> |-- $|Sent from my )",
    re.I,
)


def authored_plain_text(message: Message) -> tuple[str, bool, int]:
    """Return a plain-text body before obvious quoted-thread/signature boundaries."""
    selected = None
    attachments = 0
    for part in message.walk():
        if part.get_content_disposition() == "attachment" or part.get_filename():
            attachments += 1
            continue
        if part.get_content_type() == "text/plain" and selected is None:
            selected = part
    if selected is None:
        return "", False, attachments
    payload = selected.get_payload(decode=True)
    if payload is None:
        return "", False, attachments
    charset = selected.get_content_charset() or "utf-8"
    try:
        body = payload.decode(charset, errors="replace")
    except LookupError:
        body = payload.decode("utf-8", errors="replace")
    kept = []
    clipped = False
    for line in body.splitlines():
        if QUOTE_BOUNDARY.match(line.strip()):
            clipped = True
            break
        kept.append(line)
    return "\n".join(kept).strip(), clipped, attachments


def read_only_messages(path: Path):
    """Yield messages from mbox separators without requesting write access."""
    parser = BytesParser(policy=default)
    buffer = bytearray()
    with path.open("rb") as stream:
        for line in stream:
            if line.startswith(b"From "):
                if buffer:
                    yield parser.parsebytes(bytes(buffer))
                    buffer.clear()
                continue
            buffer.extend(line)
    if buffer:
        yield parser.parsebytes(bytes(buffer))


def inventory(path: Path, *, preview_limit: int = 0) -> dict:
    counts = Counter()
    candidates: list[dict] = []
    seen = set()
    for index, message in enumerate(read_only_messages(path)):
        counts["messages"] += 1
        sent_label = "sent" in message.get("X-Gmail-Labels", "").lower()
        if sent_label:
            counts["sent_labeled_messages"] += 1
        message_id = message.get("Message-ID", "").strip()
        key = message_id or f"mbox-index:{index}"
        if key in seen:
            counts["duplicate_message_ids"] += 1
            continue
        seen.add(key)
        body, quote_clipped, attachments = authored_plain_text(message)
        counts["attachments_skipped"] += attachments
        if quote_clipped:
            counts["quoted_or_signature_tail_clipped"] += 1
        if not body:
            counts["without_authored_plain_text"] += 1
            continue
        counts["with_authored_plain_text"] += 1
        if CUE.search(body):
            counts["first_person_cue_candidates"] += 1
            if sent_label:
                counts["sent_labeled_cue_candidates"] += 1
            if len(candidates) < preview_limit:
                candidates.append({
                    "mbox_index": index,
                    "message_key_sha256": hashlib.sha256(key.encode()).hexdigest(),
                    "date_header": message.get("Date", ""),
                    "sent_label_present": sent_label,
                    "authored_preview": body[:600],
                    "preview_truncated": len(body) > 600,
                    "quoted_tail_clipped": quote_clipped,
                })
    return {"archive_bytes": path.stat().st_size, "counts": dict(counts),
            "candidate_previews": candidates,
            "warning": "Cue matches are unverified candidates, not claims; sender identity and time scope still require review."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mbox", type=Path)
    parser.add_argument("--preview", type=int, default=0,
                        help="include up to this many authored-body previews; default 0")
    args = parser.parse_args()
    if not args.mbox.is_file():
        parser.error("mbox file does not exist")
    if args.preview < 0 or args.preview > 20:
        parser.error("preview must be between 0 and 20")
    print(json.dumps(inventory(args.mbox, preview_limit=args.preview), indent=2))


if __name__ == "__main__":
    main()
