"""A small pixel/terminal-style local chat interface for the M5 preflight."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from typing import TextIO

from .chat import ChatResponse, ChatRuntime, RuleBasedLocalExtractor
from .store import Store


BANNER = """\
┌──────────────────────────────────────────────┐
│  LIFETIME AI // LOCAL MEMORY                 │
│  source-backed state • no network • preflight │
└──────────────────────────────────────────────┘"""


class TerminalChat:
    def __init__(self, runtime: ChatRuntime, input_stream: TextIO = sys.stdin,
                 output_stream: TextIO = sys.stdout):
        self.runtime = runtime
        self.input = input_stream
        self.output = output_stream

    def write(self, text: str = "") -> None:
        self.output.write(text + "\n")
        self.output.flush()

    def run(self) -> None:
        self.write(BANNER)
        self.write("MODE // RULE EXTRACTOR // SYNTHETIC PREFLIGHT")
        self.write("Type a message to capture it, or ? question to retrieve state.")
        self.write("Commands: :help  :state  :correct ITEM TEXT  :forget SOURCE  :quit")
        while True:
            self.output.write("\n> ")
            self.output.flush()
            line = self.input.readline()
            if not line:
                self.write()
                return
            line = line.strip()
            if not line:
                continue
            if line in {":quit", ":q", ":exit"}:
                self.write("bye // state remains on disk")
                return
            self._handle(line)

    def _handle(self, line: str) -> None:
        if line == ":help":
            self.write("  ? QUESTION             retrieve current state with citations")
            self.write("  :state                 list active source-backed state")
            self.write("  :correct ITEM TEXT     replace an interpretation with provenance")
            self.write("  :forget SOURCE         hide source/state from retrieval; ledger retained")
            self.write("  :quit                  leave the local session")
            return
        if line == ":state":
            rows = self.runtime.store.active()
            if not rows:
                self.write("[state] empty")
                return
            self.write("[state]")
            for row in rows:
                self.write(f"  {row['item_id']} :: {row['proposition']} "
                           f"[source:{row['source_event_id']}]")
            return
        if line.startswith(":correct "):
            parts = line[len(":correct "):].split(maxsplit=1)
            if len(parts) != 2:
                self.write("[error] usage: :correct ITEM TEXT")
                return
            try:
                response = self.runtime.correct(parts[0], parts[1], self._now())
            except ValueError as error:
                self.write(f"[error] {error}")
                return
            self._show(response)
            return
        if line.startswith(":forget "):
            event_id = line[len(":forget "):].strip()
            if not event_id:
                self.write("[error] usage: :forget SOURCE")
                return
            try:
                changed = self.runtime.delete_source(event_id)
            except ValueError as error:
                self.write(f"[error] {error}")
                return
            self.write("[forgot] source hidden from retrieval; ledger record retained" if changed
                       else "[forgot] source was already invalidated")
            return
        if line.startswith("?"):
            query = line[1:].strip()
            if not query:
                self.write("[error] usage: ? QUESTION")
                return
            self._show(self.runtime.ask(query))
            return
        self._show(self.runtime.send(line, self._now()))

    def _show(self, response: ChatResponse) -> None:
        self.write(f"[{response.outcome}] {response.text}")
        for citation in response.citations:
            self.write(f"  └─ source:{citation.source_event_id} :: {citation.source_text}")

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local terminal chat for Lifetime AI")
    parser.add_argument("database", nargs="?", default="lifetime-ai.sqlite3",
                        help="SQLite path (default: lifetime-ai.sqlite3)")
    args = parser.parse_args()
    with Store(args.database) as store:
        TerminalChat(ChatRuntime(store, RuleBasedLocalExtractor())).run()


if __name__ == "__main__":
    main()
