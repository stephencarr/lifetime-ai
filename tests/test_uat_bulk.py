from lifetime_ai.uat import DeterministicDemoAdapter, FIXTURES, UATStore


def test_bulk_accept_requires_confirmation_and_updates_selected_items(tmp_path):
    store = UATStore(tmp_path / "uat.sqlite3")
    try:
        store.load_sources(FIXTURES, DeterministicDemoAdapter())
        ids = [item["suggestion_id"] for item in store.dashboard()["suggestions"][:2]]
        try:
            store.bulk_act(ids, "accepted", confirmed=False)
        except ValueError:
            pass
        else:
            raise AssertionError("unconfirmed bulk action was accepted")
        assert len(store.dashboard()["state"]) == 0
        assert store.bulk_act(ids, "accepted", confirmed=True) == 2
        assert len(store.dashboard()["state"]) == 2
    finally:
        store.close()
