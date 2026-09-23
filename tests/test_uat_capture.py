from lifetime_ai.uat import DeterministicDemoAdapter, FIXTURES, Source, UATStore


def test_demo_adapter_extracts_explicit_claim_and_abstains_on_outreach_and_receipts():
    adapter = DeterministicDemoAdapter()
    sources = [
        Source("mail:decision", "Project update", "Dear Stephen, I hope you are well. We decided to keep the project log current.\n\nOn Monday, Maya wrote:\n> We will switch vendors.", "2026-09-22", "Email from teammate"),
        Source("mail:outreach", "Consulting opportunity", "I would be happy to provide compensation if you advise our client.", "2026-09-22", "Email from recruiter"),
        Source("mail:receipt", "Order receipt", "Please use the link below to view your order.", "2026-09-22", "Email from store"),
    ]

    suggestions = adapter.suggest(sources)

    assert len(suggestions) == 1
    assert suggestions[0].source_id == "mail:decision"
    assert suggestions[0].kind == "fact"
    assert suggestions[0].proposition == "We decided to keep the project log current."


def test_confirmed_batch_import_captures_candidates_without_per_item_review(tmp_path):
    store = UATStore(tmp_path / "uat.sqlite3")
    try:
        assert store.load_sources(FIXTURES, DeterministicDemoAdapter(), auto_capture=True) == 3
        dashboard = store.dashboard()
        assert len(dashboard["state"]) == 3
        assert len(dashboard["suggestions"]) == 0
        assert {item["status"] for item in dashboard["reviews"]} == {"accepted"}
        assert store.retrieve("What did we decide about planning?")["matches"]
        assert set(store.event_types()) == {"shown", "accepted", "retrieved"}

        # Re-importing the same stable source IDs must not recreate or overwrite memory.
        store.correct(dashboard["state"][0]["item_id"], "Participant correction", confirmed=True)
        assert store.load_sources(FIXTURES, DeterministicDemoAdapter(), auto_capture=True) == 0
        assert "Participant correction" in {item["proposition"] for item in store.dashboard()["state"]}
    finally:
        store.close()
