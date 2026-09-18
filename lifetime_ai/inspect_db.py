from __future__ import annotations

import argparse
import json

from .store import Store


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect Lifetime AI state and provenance")
    parser.add_argument("database", help="path to the SQLite database")
    args = parser.parse_args()
    with Store(args.database) as store:
        print(json.dumps(store.inspect(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
