"""Manually seed the approved mbox shortlist into a local POC store.

This is a reviewed, fixed six-message import, not an automatic email extractor
or an evaluation run. It never reads attachments or quoted reply tails.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

from lifetime_ai.store import Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, StateStatus, Transition
from scripts.inspect_mbox_local import authored_plain_text, read_only_messages


ARCHIVE_SHA256 = "e875138e9ef20698a4053596577f93fcddeb1c5dcf5c1a9425d81b8e936979a6"


@dataclass(frozen=True)
class ReviewedClaim:
    index: int
    witness: str
    proposition: str
    status: StateStatus = StateStatus.ACTIVE


REVIEWED = (
    ReviewedClaim(19, "co founded", "In September 2026, I said I co-founded Ship & Bunker and handled web-platform technical execution and data gathering, but had little bunker-industry strategic expertise."),
    ReviewedClaim(26, "October 19th works", "On September 18, 2026, I confirmed that October 19 worked for us and said solar-install scheduling was still awaited."),
    ReviewedClaim(79, "idea of the spa", "For a September 2026 weekend outing, I liked the spa idea more than a water-park day."),
    ReviewedClaim(89, "lines and stripes", "On September 2, 2026, I reported that TRMNL had lines and stripes on my device and was not usable for me.", StateStatus.EXPIRED),
    ReviewedClaim(85, "stripes were resolved", "On September 3, 2026, I reported that two-bit images resolved stripes in my custom ESPHome firmware, but I was unsure which TRMNL firmware I had flashed.", StateStatus.EXPIRED),
    ReviewedClaim(83, "I've written my own firmware", "On September 11, 2026, I reported that my own firmware met my needs and could use the sensors and mic; I requested a refund, which was not confirmed."),
)


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def prepare(path: Path) -> list[tuple[Event, Transition]]:
    if _digest(path) != ARCHIVE_SHA256:
        raise ValueError("archive hash differs from reviewed archive")
    wanted = {entry.index: entry for entry in REVIEWED}
    prepared = []
    for index, message in enumerate(read_only_messages(path)):
        entry = wanted.get(index)
        if entry is None:
            continue
        if "sent" not in message.get("X-Gmail-Labels", "").lower():
            raise ValueError(f"message {index} is not Sent-labeled")
        body, _, _ = authored_plain_text(message)
        if entry.witness.casefold() not in " ".join(body.split()).casefold():
            raise ValueError(f"message {index} lacks reviewed witness")
        message_id = str(message.get("Message-ID", "")).strip()
        if not message_id:
            raise ValueError(f"message {index} lacks Message-ID")
        occurred_at = parsedate_to_datetime(str(message["Date"]))
        if not isinstance(occurred_at, datetime) or occurred_at.tzinfo is None:
            raise ValueError(f"message {index} lacks a dated timezone")
        source_id = "email:" + hashlib.sha256(message_id.encode()).hexdigest()[:24]
        item_id = f"reviewed-email:{index}"
        event = Event(source_id, EventType.OBSERVATION, body, occurred_at, {
            "channel": "reviewed_mbox_import", "archive_sha256": ARCHIVE_SHA256,
            "mbox_index": index, "subject": str(message.get("Subject", "")),
            "review_status": "user_approved_shortlist_2026-09-23",
        })
        item = StateItem(item_id, StateKind.FACT, entry.proposition,
                         source_id, EventType.OBSERVATION, occurred_at,
                         status=entry.status, valid_from=occurred_at,
                         valid_until=occurred_at if entry.status is StateStatus.EXPIRED else None)
        transition = Transition(f"transition:{source_id}:reviewed-import", source_id, item,
                                reason="explicitly approved local mbox shortlist")
        prepared.append((event, transition))
    if len(prepared) != len(REVIEWED):
        raise ValueError("not all reviewed messages were found")
    return prepared


def apply(database: Path, prepared: list[tuple[Event, Transition]]) -> tuple[int, int]:
    inserted_events = inserted_claims = 0
    with Store(database) as store:
        for event, transition in prepared:
            event_added, claim_added = store.ingest_and_apply(event, transition)
            inserted_events += event_added
            inserted_claims += claim_added
    return inserted_events, inserted_claims


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mbox", type=Path)
    parser.add_argument("database", type=Path)
    parser.add_argument("--apply", action="store_true", help="write to the local POC database")
    args = parser.parse_args()
    prepared = prepare(args.mbox)
    if not args.apply:
        print(f"DRY RUN: {len(prepared)} reviewed messages; 4 active, 2 expired; no store writes")
        return
    event_count, claim_count = apply(args.database, prepared)
    print(f"Imported {event_count} source events and {claim_count} claims; "
          f"{len(prepared) - claim_count} already present")


if __name__ == "__main__":
    main()
