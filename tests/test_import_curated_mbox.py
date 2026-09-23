from datetime import datetime, timezone

from lifetime_ai.store import Store
from lifetime_ai.types import Event, EventType, StateItem, StateKind, StateStatus, Transition
from scripts.import_curated_mbox import apply


def test_reviewed_import_is_idempotent_and_preserves_historical_status(tmp_path):
    moment = datetime(2026, 9, 1, tzinfo=timezone.utc)
    prepared = []
    for index, status in enumerate((StateStatus.ACTIVE, StateStatus.EXPIRED)):
        source_id = f"email:synthetic-{index}"
        event = Event(source_id, EventType.OBSERVATION, f"source text {index}", moment,
                      {"channel": "reviewed_mbox_import"})
        item = StateItem(f"reviewed-email:{index}", StateKind.FACT,
                         f"claim {index}", source_id, EventType.OBSERVATION,
                         moment, status=status)
        prepared.append((event, Transition(f"transition:{source_id}:reviewed-import",
                                           source_id, item)))

    database = tmp_path / "store.sqlite3"
    assert apply(database, prepared) == (2, 2)
    assert apply(database, prepared) == (0, 0)
    with Store(database) as store:
        assert len(store.active()) == 1
        assert len(store.inspect()) == 2
