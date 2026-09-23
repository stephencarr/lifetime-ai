from __future__ import annotations

import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .uat import DeterministicDemoAdapter, FIXTURES, MiniLMAdapter, Source, UATStore, sources_from_json_payload, sources_from_mbox_text


ROOT = Path(__file__).parent.parent
DEFAULT_DB = Path(os.environ.get("LIFETIME_AI_UAT_DB", ROOT / ".uat" / "uat_observe.sqlite3"))
ADAPTER = MiniLMAdapter() if os.environ.get("LIFETIME_AI_MINILM_WEIGHTS") else DeterministicDemoAdapter()


WEB_ROOT = Path(__file__).parent / "uat_web"


def html_page() -> str:
    return (WEB_ROOT / "index.html").read_text(encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    store = UATStore(DEFAULT_DB)

    def _send(self, payload: object, status: int = 200) -> None:
        raw = json.dumps(payload).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

    def _body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0")); return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        if self.path == "/":
            raw = html_page().encode(); content_type = "text/html; charset=utf-8"
        elif self.path in {"/assets/style.css", "/assets/app.js"}:
            asset = WEB_ROOT / self.path.removeprefix("/assets/")
            raw = asset.read_bytes()
            content_type = "text/css; charset=utf-8" if asset.suffix == ".css" else "text/javascript; charset=utf-8"
        else:
            raw = None
        if raw is not None:
            self.send_response(200); self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'self'")
            self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw); return
        if self.path == "/api/dashboard":
            data = self.store.dashboard(); data["mode"] = ADAPTER.name; self._send(data); return
        if self.path == "/api/preview-fixtures":
            self._send({"sources": [item.__dict__ for item in FIXTURES], "candidates": [item.__dict__ for item in ADAPTER.suggest(FIXTURES)]}); return
        self._send({"error": "not found"}, 404)

    def do_POST(self) -> None:
        try:
            body = self._body(); path = urlparse(self.path).path
            if path == "/api/load-fixtures":
                if not body.get("confirmed"): raise ValueError("Explicit confirmation is required")
                self._send({"loaded": self.store.load_sources(FIXTURES, ADAPTER, auto_capture=True)}); return
            if path == "/api/preview-fixtures":
                self._send({"sources": [item.__dict__ for item in FIXTURES], "candidates": [item.__dict__ for item in ADAPTER.suggest(FIXTURES)]}); return
            if path == "/api/sources":
                if not body.get("confirmed"): raise ValueError("Explicit confirmation is required")
                self.store.load_sources([Source(f"local:{uuid.uuid4()}", str(body["title"]), str(body["excerpt"]), str(body["occurred_at"]), str(body["context"]))], ADAPTER, auto_capture=True); self._send({"ok": True}); return
            if path == "/api/import-json":
                if not body.get("confirmed"): raise ValueError("Explicit confirmation is required")
                self.store.load_sources(sources_from_json_payload(body.get("payload")), ADAPTER, auto_capture=True); self._send({"ok": True}); return
            if path == "/api/preview-sources":
                raw_sources = body.get("sources")
                if not isinstance(raw_sources, list) or not raw_sources:
                    raise ValueError("Provide at least one source to preview")
                sources = [Source(str(item["source_id"]), str(item["title"]), str(item["excerpt"]), str(item["occurred_at"]), str(item["context"])) for item in raw_sources]
                candidates = [item.__dict__ for item in ADAPTER.suggest(sources)]
                self._send({"candidate_count": len(candidates), "candidates": candidates}); return
            if path == "/api/preview-mbox":
                sources = sources_from_mbox_text(str(body.get("mbox_text", "")))
                candidates = [item.__dict__ for item in ADAPTER.suggest(sources)]
                self._send({"sources": [source.__dict__ for source in sources], "candidate_count": len(candidates), "candidates": candidates}); return
            if path == "/api/import-mbox":
                if not body.get("confirmed"): raise ValueError("Explicit confirmation is required")
                raw_sources = body.get("sources")
                if not isinstance(raw_sources, list): raise ValueError("Invalid MBOX preview payload")
                sources = [Source(str(item["source_id"]), str(item["title"]), str(item["excerpt"]), str(item["occurred_at"]), str(item["context"])) for item in raw_sources]
                self.store.load_sources(sources, ADAPTER, auto_capture=True); self._send({"ok": True}); return
            if path.startswith("/api/suggestions/") and path.endswith("/action"):
                sid = unquote(path[len("/api/suggestions/"):-len("/action")]); self.store.act(sid, str(body["action"]), confirmed=bool(body.get("confirmed")), proposition=body.get("proposition")); self._send({"ok": True}); return
            if path == "/api/suggestions/bulk-action":
                count = self.store.bulk_act([str(item) for item in body.get("suggestion_ids", [])], str(body["action"]), confirmed=bool(body.get("confirmed"))); self._send({"updated": count}); return
            if path == "/api/retrieve": self._send(self.store.retrieve(str(body.get("question", "")))); return
            if path == "/api/findings":
                finding_id = self.store.add_finding(str(body["target_type"]), str(body["target_id"]),
                    str(body["category"]), str(body.get("note", "")), confirmed=bool(body.get("confirmed")))
                self._send({"finding_id": finding_id}); return
            if path == "/api/reset": self.store.reset(confirmed=bool(body.get("confirmed"))); self._send({"ok": True}); return
            self._send({"error": "not found"}, 404)
        except (KeyError, ValueError, json.JSONDecodeError) as error: self._send({"error": str(error)}, 400)

    def do_PATCH(self) -> None:
        try:
            path = urlparse(self.path).path
            if path.startswith("/api/state/"):
                body = self._body()
                self.store.correct(unquote(path[len("/api/state/"):]), str(body["proposition"]), confirmed=bool(body.get("confirmed"))); self._send({"ok": True}); return
            self._send({"error": "not found"}, 404)
        except (KeyError, ValueError) as error: self._send({"error": str(error)}, 400)

    def do_DELETE(self) -> None:
        try:
            path = urlparse(self.path).path
            if path.startswith("/api/findings/"):
                body = self._body(); self.store.delete_finding(unquote(path[len("/api/findings/"):]), confirmed=bool(body.get("confirmed"))); self._send({"ok": True}); return
            if path.startswith("/api/state/"):
                body = self._body(); self.store.delete(unquote(path[len("/api/state/"):]), confirmed=bool(body.get("confirmed"))); self._send({"ok": True}); return
            self._send({"error": "not found"}, 404)
        except (KeyError, ValueError) as error: self._send({"error": str(error)}, 400)


def main() -> None:
    server = HTTPServer(("127.0.0.1", int(os.environ.get("LIFETIME_AI_UAT_PORT", "8766"))), Handler)
    print(f"Lifetime AI supervised UAT: http://{server.server_address[0]}:{server.server_address[1]}")
    print(f"Disposable local store: {DEFAULT_DB}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: Handler.store.close(); server.server_close()


if __name__ == "__main__": main()
