"""Explicit local-model chat terminal; never falls back to diagnostic rules."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .local_models import locked_clients
from .model_chat import ModelChatRuntime
from .store import Store


ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "evaluation/m5_model_poc/model_lock.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="explicit path to the local model POC database")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--create", action="store_true", help="create a new database")
    choice.add_argument("--open-existing", action="store_true", help="open an existing database")
    args = parser.parse_args()
    if args.create and args.database.exists():
        parser.error("database already exists; use --open-existing explicitly")
    if args.open_existing and not args.database.is_file():
        parser.error("database does not exist; use --create explicitly")
    generator, embedder, lock = locked_clients(LOCK)
    with Store(args.database) as store:
        runtime = ModelChatRuntime(store, generator, embedder)
        print("LOCAL MODEL POC // synthetic development only // UAT paused")
        print("Model:", lock["generator"]["repository"], "Embedding:",
              lock["embedder"]["repository"])
        print("Type a chat message; prefix a question with ?; :state, :forget SOURCE, :quit")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line in {":quit", ":q"}:
                return
            if line == ":state":
                for row in store.model_active_rows():
                    print(row["item_id"], row["proposition"],
                          f"[source:{row['source_event_id']}]")
                continue
            if line.startswith(":forget "):
                source_id = line[len(":forget "):].strip()
                try:
                    print("invalidated" if runtime.delete_source(source_id) else "already invalidated")
                except ValueError as error:
                    print("error:", error)
                continue
            response = (runtime.ask(line[1:].strip()) if line.startswith("?") else
                        runtime.send(line, datetime.now(timezone.utc)))
            print(f"[{response.outcome}] {response.text}")
            for cite in response.citations:
                print(f"  source:{cite.source_event_id} :: {cite.source_text}")


if __name__ == "__main__":
    main()
