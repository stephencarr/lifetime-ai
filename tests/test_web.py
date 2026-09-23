import json
from threading import Thread
from urllib.request import Request, urlopen

from lifetime_ai.store import Store
from lifetime_ai.web import LocalChatServer


def test_loopback_web_chat_uses_core_state_and_citations(tmp_path):
    with Store(tmp_path / "web.sqlite"):
        pass
    server = LocalChatServer(0, tmp_path / "web.sqlite")
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base + "/") as response:
            page = response.read().decode()
        assert "LIFETIME AI // LOCAL MEMORY" in page
        assert "LIMITED ANSWER GRAMMAR // DEVELOPMENT" in page

        def post(path, body):
            request = Request(base + path, data=json.dumps(body).encode(),
                              headers={"Content-Type": "application/json"})
            with urlopen(request) as response:
                return json.load(response)

        captured = post("/api/chat", {"text": "I prefer concise answers."})["response"]
        assert captured["outcome"] == "accepted"
        source_id = captured["citations"][0]["source_event_id"]
        with urlopen(base + "/api/state") as response:
            item_id = json.load(response)["items"][0]["item_id"]
        assert post("/api/chat", {"text": "? What do I prefer?"})["response"][
            "citations"][0]["source_event_id"] == source_id
        corrected = post("/api/correct", {"item_id": item_id,
                                          "text": "I prefer detailed answers."})
        assert corrected["response"]["outcome"] == "accepted"
        replacement_source = corrected["response"]["citations"][0]["source_event_id"]
        post("/api/invalidate", {"source_event_id": replacement_source})
        assert post("/api/chat", {"text": "? What do I prefer?"})["response"][
            "outcome"] == "uncertain"
    finally:
        server.shutdown()
        worker.join(timeout=5)
        server.server_close()
