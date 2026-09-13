#!/usr/bin/env python3
"""The operator's screen: who is attached, and what it takes to attach one more.

    EXCHANGE_URL=http://exchange:8110 EXCHANGE_ADMIN_TOKEN=… ./admin/server.py

**It holds no docker socket, and adding a backbone does not start one.** The dangerous part of "add a
backbone" was never the `mkdir` — it is granting container-execution rights to a service that faces a
network. What is actually tedious is the rest: picking a name, four directories, a secret, a
`peers.yaml`, a `members.yaml` entry, a compose block, and a port nobody else took. None of that needs
any privilege at all, so this does all of it and hands back one command to paste.

The split is the point. **This service thinks; docker runs.** An operator reads what to do and stays
the one who did it.

**It cannot read the knowledge and cannot make an area cross.** The exchange's operator door returns
membership and health and never a reflected row — an area crosses because somebody wrote
`use_when_export` on it, in its own repository, through its own review queue, and a screen that could
do that from here would be a way around the only rule that keeps sharing deliberate. Writes to an
ontology go to that backbone's own screen, which is the same rule a link follows.

English only, for now: this is the operator's surface, its audience is whoever runs `docker compose`,
and four translations of a page that did not exist yesterday would be premature. docs/I18N.md says so
where it says what else is not translated.
"""
from __future__ import annotations

import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
EXCHANGE = (os.environ.get("EXCHANGE_URL") or "http://exchange:8110").rstrip("/")
TOKEN = (os.environ.get("EXCHANGE_ADMIN_TOKEN") or "").strip()
PORT = int(os.environ.get("PORT") or 8090)
TIMEOUT = float(os.environ.get("ADMIN_TIMEOUT") or 6.0)


def call(method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    """The exchange's operator door. The token lives here and never reaches the browser — the same
    reason a link relays instead of handing out credentials."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(EXCHANGE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json", "X-Admin-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: return e.code, json.loads(raw or b"{}")
        except Exception: return e.code, {"error": raw.decode(errors="replace")[:200]}
    except Exception as e:
        return 0, {"error": f"the exchange is not answering at {EXCHANGE}: {type(e).__name__}"}


def plan(name: str, label: str, port: int, taken: list[int]) -> dict:
    """Everything needed to attach one more backbone, as text to paste.

    One secret, not two. The token a backbone presents to the exchange is the same one the exchange
    presents back to it — one per member, both directions — which is what lets the exchange know who
    is calling and spare a member its own advertisement coming back at it.

    The port is nudged past anything already spoken for rather than refused: an operator asked for a
    backbone, not for a lecture about 8080.
    """
    up = name.upper().replace("-", "_")
    token = secrets.token_urlsafe(24)
    while port in taken: port += 1
    return {
        "name": name, "label": label, "port": port, "token_env": f"EXCHANGE_TOKEN_{up}",
        "env": (f"# .env — one secret, used in both directions between {label} and the exchange\n"
                f"EXCHANGE_TOKEN_{up}={token}\n"),
        "compose": (
            f"# docker-compose.{name}.yml — a backbone of its own: its own repository, its own review\n"
            f"# queue, its own vocabulary. Nothing here says what it shares; that is written in its\n"
            f"# ontology, area by area, and reviewed there.\n"
            f"services:\n"
            f"  ontology-{name}:\n"
            f"    build: {{ context: ., dockerfile: ontology/Dockerfile }}\n"
            f"    image: knowledge-ontology:0.1.0\n"
            f'    user: "${{KNOWLEDGE_UID:-1000}}:${{KNOWLEDGE_GID:-1000}}"\n'
            f"    environment:\n"
            f"      ONTOLOGY_DATA: /data/repo\n"
            f"      ONTOLOGY_PUBLISH: /data/publish\n"
            f"      ONTOLOGY_OVERLAYS: /data/overlays\n"
            f"      ONTOLOGY_HARNESS: /data/harness\n"
            f'      ONTOLOGY_PEER_TOKEN: "${{EXCHANGE_TOKEN_{up}}}"\n'
            f'      ONTOLOGY_PEER_TOKEN_IX: "${{EXCHANGE_TOKEN_{up}}}"\n'
            f"    volumes:\n"
            f"      - ./data-{name}/repo:/data/repo\n"
            f"      - ./data-{name}/publish:/data/publish\n"
            f"      - ./data-{name}/overlays:/data/overlays\n"
            f"      - ./data-{name}/harness:/data/harness\n"
            f"    restart: unless-stopped\n"
            f"  web-{name}:\n"
            f"    build: {{ context: ., dockerfile: web/Dockerfile }}\n"
            f"    image: knowledge-web:0.1.0\n"
            f"    depends_on: {{ ontology-{name}: {{ condition: service_healthy }} }}\n"
            f"    environment:\n"
            f"      KNOWLEDGE_API_URL: http://ontology-{name}:8100\n"
            f'      KNOWLEDGE_ACTOR: "web-{name}"\n'
            f'    ports: [ "{port}:8080" ]\n'
            f"    restart: unless-stopped\n"
            f"  exchange:\n"
            f"    environment:\n"
            f'      EXCHANGE_TOKEN_{up}: "${{EXCHANGE_TOKEN_{up}}}"\n'),
        "peers": (f"# data-{name}/repo/peers.yaml — its half of the declaration. The exchange's half is\n"
                  f"# the member entry this screen adds; neither side alone enrols anybody.\n"
                  f"peers:\n"
                  f"  - name: ix\n"
                  f"    label: EXCHANGE\n"
                  f"    url: http://exchange:8110\n"
                  f"    token_env: ONTOLOGY_PEER_TOKEN_IX\n"),
        "shell": (f"mkdir -p data-{name}/repo data-{name}/publish data-{name}/overlays data-{name}/harness\n"
                  f"cp -r examples/back-office/. data-{name}/repo/     # or start empty\n"
                  f"#  write the two files above, then:\n"
                  f"docker compose -f docker-compose.yml -f docker-compose.{name}.yml up -d\n"),
    }


def plan_link(name: str, label: str, url: str, mine: str, my_url: str) -> dict:
    """Everything needed to meet a second exchange, as text — half of it for somebody else to paste.

    The shape of this plan is the answer to *who may enrol whom*: **each side enrols the other, or
    there is no link.** It is the same two halves as a backbone joining a room, with both halves now
    held by operators, and it is deliberately not something one screen can finish. What comes back is
    one secret and two entries — one to add here, one to send over — and the link starts working when
    the second person has agreed enough to paste theirs.

    Nothing here is built and nothing is started: two rooms already exist, and meeting is a line in
    each of their files.
    """
    up, mine_up = name.upper().replace("-", "_"), mine.upper().replace("-", "_")
    token = secrets.token_urlsafe(24)
    return {
        "name": name, "label": label, "kind": "exchange", "token_env": f"EXCHANGE_TOKEN_{up}",
        "env": (f"# .env, here — one secret for this link, used in both directions.\n"
                f"EXCHANGE_TOKEN_{up}={token}\n"),
        "their_env": (f"# .env, at {label} — the same secret, under the name their room will look it\n"
                      f"# up by. The value is shared; the variable is each side's own.\n"
                      f"EXCHANGE_TOKEN_{mine_up}={token}\n"),
        "mine": (f"# members.yaml, here. `kind: exchange` is what stops this room carrying {label}'s\n"
                 f"# neighbours to its own — and what stops the two rooms asking each other what they\n"
                 f"# are advertising and neither ever answering.\n"
                 f"  - name: {name}\n    label: {label}\n    url: {url}\n"
                 f"    kind: exchange\n    token_env: EXCHANGE_TOKEN_{up}\n"),
        "theirs": (f"# members.yaml, at {label}. Their half; send it to whoever runs that room.\n"
                   f"  - name: {mine}\n    label: {mine.upper()}\n    url: {my_url}\n"
                   f"    kind: exchange\n    token_env: EXCHANGE_TOKEN_{mine_up}\n"),
    }


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write(f"{self.address_string()} {fmt % args}\n")

    def _send(self, code, payload, ctype="application/json; charset=utf-8"):
        body = payload if isinstance(payload, bytes) else (
            payload.encode("utf-8") if isinstance(payload, str)
            else json.dumps(payload, ensure_ascii=False, indent=1).encode("utf-8"))
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        try: return json.loads(self.rfile.read(n) or b"{}")
        except Exception: return {}

    def do_GET(self):
        parts = [unquote(p) for p in urlparse(self.path).path.strip("/").split("/") if p]
        if not parts or parts == ["admin"]:
            page = (HERE / "static" / "admin.html").read_bytes()
            return self._send(200, page, "text/html; charset=utf-8")
        if parts[:1] == ["static"] and len(parts) == 2 and parts[1] in ("admin.css", "admin.js"):
            kind = "text/css" if parts[1].endswith(".css") else "text/javascript"
            return self._send(200, (HERE / "static" / parts[1]).read_bytes(), f"{kind}; charset=utf-8")
        if parts == ["api", "state"]:
            if not TOKEN: return self._send(501, {"error": "no admin token — set EXCHANGE_ADMIN_TOKEN"})
            code, d = call("GET", "/admin/state")
            return self._send(200 if code == 200 else code or 502, d)
        if parts == ["healthz"]:
            return self._send(200, {"ok": True, "exchange": EXCHANGE, "token": bool(TOKEN)})
        return self._send(404, {"error": "unknown path"})

    def do_POST(self):
        parts = [unquote(p) for p in urlparse(self.path).path.strip("/").split("/") if p]
        if not TOKEN: return self._send(501, {"error": "no admin token — set EXCHANGE_ADMIN_TOKEN"})
        body = self._body()
        if parts == ["api", "members"]:
            code, d = call("POST", "/admin/members", body)
            return self._send(code or 502, d)
        if parts == ["api", "members", "remove"]:
            code, d = call("DELETE", "/admin/members", body)
            return self._send(code or 502, d)
        if parts == ["api", "plan"]:
            name = str(body.get("name") or "").strip().lower()
            if not name or not name.replace("-", "").isalnum() or not name[0].isalpha():
                return self._send(400, {"error": "name must be ASCII kebab-case, starting with a letter"})
            code, st = call("GET", "/admin/state")
            if str(body.get("kind") or "") == "exchange":
                url = str(body.get("url") or "").strip().rstrip("/")
                my_url = str(body.get("my_url") or "").strip().rstrip("/")
                if not url.startswith(("http://", "https://")):
                    return self._send(400, {"error": "their address must be http(s)"})
                if not my_url.startswith(("http://", "https://")):
                    return self._send(400, {"error": "this exchange's address must be http(s) — it is "
                                                     "what the other room will call, and only you know it"})
                return self._send(200, plan_link(name, str(body.get("label") or name.upper()), url,
                                                 str(st.get("name") or "exchange"), my_url))
            taken = [8080, 8081, 8090]
            return self._send(200, plan(name, str(body.get("label") or name.upper()),
                                        int(body.get("port") or 8082), taken))
        return self._send(404, {"error": "unknown path"})


def main():
    sys.stderr.write(f"routemind-admin exchange={EXCHANGE} token={bool(TOKEN)} port={PORT}\n")
    if not TOKEN:
        sys.stderr.write("  no EXCHANGE_ADMIN_TOKEN — the screen will load and every call will say so\n")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
