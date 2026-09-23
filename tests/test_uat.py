from lifetime_ai.uat import DeterministicDemoAdapter, FIXTURES, UATStore


def test_supervised_review_retrieval_correction_delete_and_reset(tmp_path):
    store = UATStore(tmp_path / "uat.sqlite3")
    try:
        assert store.load_sources(FIXTURES, DeterministicDemoAdapter()) == 3
        dashboard = store.dashboard()
        suggestion = next(item for item in dashboard["suggestions"] if "planning" in item["proposition"].lower())

        store.act(suggestion["suggestion_id"], "accepted", confirmed=True)
        item = store.dashboard()["state"][0]
        result = store.retrieve("What did we decide about planning?")
        assert result["matches"]
        assert result["matches"][0]["source"]["source_id"] == item["source_id"]

        store.correct(item["item_id"], "Corrected participant-approved decision", confirmed=True)
        assert store.dashboard()["state"][0]["proposition"] == "Corrected participant-approved decision"
        store.delete(item["item_id"], confirmed=True)
        assert store.dashboard()["state"] == []
        assert store.retrieve("What did we decide about planning?")["matches"] == []
        assert {"shown", "accepted", "retrieved", "corrected", "deleted"}.issubset(set(store.event_types()))

        store.reset(confirmed=True)
        assert store.dashboard() == {"sources": [], "suggestions": [], "reviews": [], "state": [], "findings": []}
        assert store.event_types() == ["reset"]
    finally:
        store.close()


def test_review_history_and_structured_findings_survive_restart(tmp_path):
    path = tmp_path / "uat.sqlite3"
    store = UATStore(path)
    store.load_sources(FIXTURES[:1], DeterministicDemoAdapter())
    suggestion = store.dashboard()["suggestions"][0]
    store.act(suggestion["suggestion_id"], "accepted", confirmed=True)
    item = store.dashboard()["state"][0]
    finding_id = store.add_finding("state", item["item_id"], "wrong_type",
                                   "A short synthetic observation", confirmed=True)
    store.close()

    store = UATStore(path)
    try:
        dashboard = store.dashboard()
        assert dashboard["suggestions"] == []
        assert dashboard["reviews"][0]["status"] == "accepted"
        assert dashboard["findings"][0]["category"] == "wrong_type"
        assert dashboard["findings"][0]["target_id"] == item["item_id"]
        store.delete_finding(finding_id, confirmed=True)
        assert store.dashboard()["findings"] == []
        assert "A short synthetic observation" not in str(store.event_types())
    finally:
        store.close()


def test_mutations_require_explicit_confirmation(tmp_path):
    store = UATStore(tmp_path / "uat.sqlite3")
    try:
        store.load_sources(FIXTURES[:1], DeterministicDemoAdapter())
        suggestion = store.dashboard()["suggestions"][0]
        try:
            store.act(suggestion["suggestion_id"], "accepted", confirmed=False)
        except ValueError as error:
            assert "confirmation" in str(error)
        else:
            raise AssertionError("unconfirmed action was accepted")
        assert store.dashboard()["state"] == []
    finally:
        store.close()
