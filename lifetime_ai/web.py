"""Loopback-only terminal-style browser view for the M5 local chat preflight."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from .chat import ChatResponse, ChatRuntime, RuleBasedLocalExtractor
from .store import Store


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lifetime AI // Local Memory</title>
<style>
:root { color-scheme: dark; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  background:#0b1110; color:#d9e8dd; }
* { box-sizing:border-box; } body { margin:0; min-height:100vh; }
.shell { max-width:1120px; margin:auto; padding:24px; }
header { border:2px solid #6cae84; padding:16px 20px; display:flex; justify-content:space-between; gap:16px; align-items:center; }
h1 { font-size:20px; letter-spacing:.09em; margin:0; } h2 { font-size:13px; text-transform:uppercase; letter-spacing:.12em; margin:0 0 14px; }
.sub,.meta { color:#9bb5a2; font-size:12px; } .badge { color:#bceac1; font-size:12px; text-align:right; }
.layout { display:grid; grid-template-columns:minmax(0,2fr) minmax(260px,1fr); gap:16px; margin-top:16px; }
.pane { border:1px solid #3b5b48; background:#101a16; padding:18px; min-height:420px; }
#log { height:54vh; min-height:320px; overflow:auto; padding-right:8px; }
.entry { border-bottom:1px solid #2b4435; padding:12px 0; white-space:pre-wrap; overflow-wrap:anywhere; }
.entry:first-child { padding-top:0; } .role { display:block; color:#8dd7a0; font-size:11px; margin-bottom:6px; text-transform:uppercase; }
.evidence { display:block; color:#a5c8aa; font-size:12px; margin-top:7px; }
.inputrow { display:flex; gap:8px; margin-top:16px; }
input { flex:1; min-width:0; padding:12px; background:#08110d; border:1px solid #6cae84; color:#e5f6e8; font:inherit; }
button { background:#1c3828; color:#e5f6e8; border:1px solid #6cae84; padding:10px 13px; font:inherit; cursor:pointer; }
button:hover,button:focus { background:#2d5540; } button:disabled { opacity:.5; cursor:wait; }
.item { border-top:1px solid #2b4435; padding:12px 0; overflow-wrap:anywhere; }
.item:first-of-type { border-top:0; } .itemtext { margin:5px 0; } .actions { display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; }
.actions button { font-size:11px; padding:6px 8px; } .empty { color:#9bb5a2; font-size:13px; }
.editbox,.confirmbox { margin-top:10px; padding:10px; border:1px solid #3b5b48; }
.editbox input { width:100%; } .editbox .actions,.confirmbox .actions { margin-top:8px; }
[hidden] { display:none !important; }
footer { color:#9bb5a2; font-size:12px; margin-top:16px; line-height:1.6; }
@media(max-width:720px) { .shell { padding:12px; } header { display:block; } .badge { text-align:left; margin-top:8px; } .layout { grid-template-columns:1fr; } .pane { min-height:auto; } #log { height:40vh; } }
</style></head><body><div class="shell">
<header><div><h1>LIFETIME AI // LOCAL MEMORY</h1><div class="sub">Source-backed state, one conversation at a time</div></div>
<div class="badge">LOCAL // RULE EXTRACTOR<br>LIMITED ANSWER GRAMMAR // DEVELOPMENT</div></header>
<div class="layout"><section class="pane"><h2>Conversation</h2><div id="log" aria-live="polite"></div>
<form id="chat" class="inputrow"><input id="message" autocomplete="off" aria-label="Message or question" placeholder="Say something, or start with ? to ask" required><button id="send">SEND</button></form>
</section><aside class="pane"><h2>Current state</h2><div id="state"></div></aside></div>
<footer>Development demo: the answer check supports a declared, limited question grammar and abstains outside it. ANSWERED cites current source-backed state at the supported scope; it is not a general-language guarantee. Direct first-person preferences and commitments may become durable state. Invalidate hides a source from retrieval; its text remains in the local ledger. No data is sent to an external service. Participant UAT remains paused.</footer>
</div><script>
const log=document.getElementById('log'), state=document.getElementById('state'), input=document.getElementById('message');
function line(role,text,evidence=[]) { const box=document.createElement('div'); box.className='entry';
  const r=document.createElement('span'); r.className='role'; r.textContent=role; box.append(r);
  const t=document.createElement('span'); t.textContent=text; box.append(t);
  for(const cite of evidence){const e=document.createElement('span');e.className='evidence';e.textContent='└─ source:'+cite.source_event_id+' :: '+cite.source_text;box.append(e)}
  log.append(box);log.scrollTop=log.scrollHeight; }
async function api(path,payload){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data=await r.json();if(!r.ok)throw Error(data.error||'Request failed');return data;}
async function refresh(){const r=await fetch('/api/state');const data=await r.json();state.replaceChildren();
  if(!data.items.length){const e=document.createElement('p');e.className='empty';e.textContent='No current source-backed state.';state.append(e);return}
  for(const item of data.items){const card=document.createElement('div');card.className='item';
    const id=document.createElement('div');id.className='meta';id.textContent=item.kind.toUpperCase()+' // '+item.item_id;
    const value=document.createElement('div');value.className='itemtext';value.textContent=item.proposition;
    const source=document.createElement('div');source.className='meta';source.textContent='source:'+item.source_event_id;
    const actions=document.createElement('div');actions.className='actions';
    const edit=document.createElement('form');edit.className='editbox';edit.hidden=true;
    const editLabel=document.createElement('label');editLabel.textContent='Correct interpretation';
    const editInput=document.createElement('input');editInput.value=item.proposition;editInput.setAttribute('aria-label','Correct interpretation for '+item.item_id);editInput.required=true;
    const editActions=document.createElement('div');editActions.className='actions';
    const save=document.createElement('button');save.type='submit';save.textContent='SAVE CORRECTION';
    const cancelEdit=document.createElement('button');cancelEdit.type='button';cancelEdit.textContent='CANCEL';cancelEdit.onclick=()=>{edit.hidden=true};
    editActions.append(save,cancelEdit);editLabel.append(editInput);edit.append(editLabel,editActions);
    edit.onsubmit=async event=>{event.preventDefault();const text=editInput.value.trim();if(!text)return;save.disabled=true;
      try{const result=await api('/api/correct',{item_id:item.item_id,text});line(result.response.outcome,result.response.text,result.response.citations);await refresh()}
      catch(error){line('error',error.message);save.disabled=false}};
    const confirmBox=document.createElement('div');confirmBox.className='confirmbox';confirmBox.hidden=true;
    const warning=document.createElement('div');warning.textContent='Hide this source from retrieval? Its text remains in the local ledger.';
    const confirmActions=document.createElement('div');confirmActions.className='actions';
    const yes=document.createElement('button');yes.type='button';yes.textContent='INVALIDATE';
    const cancelInvalidate=document.createElement('button');cancelInvalidate.type='button';cancelInvalidate.textContent='CANCEL';cancelInvalidate.onclick=()=>{confirmBox.hidden=true};
    yes.onclick=async()=>{yes.disabled=true;try{const result=await api('/api/invalidate',{source_event_id:item.source_event_id});line('invalidation',result.message);await refresh()}
      catch(error){line('error',error.message);yes.disabled=false}};
    confirmActions.append(yes,cancelInvalidate);confirmBox.append(warning,confirmActions);
    const correct=document.createElement('button');correct.type='button';correct.textContent='CORRECT';correct.onclick=()=>{confirmBox.hidden=true;edit.hidden=false;editInput.focus()};
    const invalidate=document.createElement('button');invalidate.type='button';invalidate.textContent='INVALIDATE SOURCE';invalidate.onclick=()=>{edit.hidden=true;confirmBox.hidden=false};
    actions.append(correct,invalidate);card.append(id,value,source,actions,edit,confirmBox);state.append(card)}}
document.getElementById('chat').onsubmit=async e=>{e.preventDefault();const text=input.value.trim();if(!text)return;
  input.value='';line('you',text);document.getElementById('send').disabled=true;
  try{const result=await api('/api/chat',{text});line(result.response.outcome,result.response.text,result.response.citations);await refresh()}
  catch(error){line('error',error.message)}finally{document.getElementById('send').disabled=false;input.focus()}};
line('system','Local chat ready. Type a statement, or begin with ? to ask about current state.');refresh();input.focus();
</script></body></html>"""


def _response_record(response: ChatResponse) -> dict:
    return {"outcome": response.outcome, "text": response.text,
            "citations": [citation.__dict__ for citation in response.citations]}


class LocalChatServer(HTTPServer):
    def __init__(self, port: int, database: Path):
        super().__init__(("127.0.0.1", port), LocalChatHandler)
        self.database = database


class LocalChatHandler(BaseHTTPRequestHandler):
    server: LocalChatServer

    def _send(self, status: int, payload: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, status: int, value: dict) -> None:
        self._send(status, json.dumps(value).encode(), "application/json; charset=utf-8")

    def _same_origin(self) -> bool:
        host = f"127.0.0.1:{self.server.server_port}"
        return (self.headers.get("Host") == host and
                self.headers.get("Origin", f"http://{host}") == f"http://{host}")

    def do_GET(self) -> None:
        if not self._same_origin():
            self._json(403, {"error": "local origin required"})
        elif self.path == "/":
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif self.path == "/api/state":
            with Store(self.server.database) as store:
                self._json(200, {"items": [
                    {"item_id": row["item_id"], "kind": row["kind"],
                     "proposition": row["proposition"], "source_event_id": row["source_event_id"]}
                    for row in store.active()]})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._same_origin():
            self._json(403, {"error": "local origin required"})
            return
        if self.headers.get("Content-Type") != "application/json":
            self._json(415, {"error": "JSON required"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536:
                raise ValueError("request size must be between 1 and 65536 bytes")
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError("JSON object required")
            with Store(self.server.database) as store:
                runtime = ChatRuntime(store, RuleBasedLocalExtractor())
                if self.path == "/api/chat":
                    message = str(body.get("text", "")).strip()
                    if not message or message == "?":
                        raise ValueError("message or question is empty")
                    response = (runtime.ask(message[1:].strip()) if message.startswith("?")
                                else runtime.send(message, datetime.now(timezone.utc)))
                    result = {"response": _response_record(response)}
                elif self.path == "/api/correct":
                    item_id = str(body.get("item_id", "")).strip()
                    message = str(body.get("text", "")).strip()
                    if not item_id or not message:
                        raise ValueError("item and correction text required")
                    result = {"response": _response_record(runtime.correct(
                        item_id, message, datetime.now(timezone.utc)))}
                elif self.path == "/api/invalidate":
                    event_id = str(body.get("source_event_id", "")).strip()
                    if not event_id:
                        raise ValueError("source event required")
                    changed = runtime.delete_source(event_id)
                    result = {"message": ("Source hidden from retrieval; ledger record retained."
                                          if changed else "Source was already invalidated.")}
                else:
                    self._json(404, {"error": "not found"})
                    return
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})
            return
        self._json(200, result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local browser chat for Lifetime AI")
    parser.add_argument("database", type=Path, help="SQLite path")
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()
    with Store(args.database):
        pass
    server = LocalChatServer(args.port, args.database)
    print(f"Lifetime AI local chat: http://127.0.0.1:{server.server_port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
