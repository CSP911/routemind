#!/usr/bin/env python3
"""An exchange: where backbones meet, and nothing else.

    EXCHANGE_MEMBERS=/data/members.yaml EXCHANGE_TOKEN_<MEMBER>=… ./exchange/server.py

**It is not a backbone and cannot become one.** It has no repository, no areas, no vocabulary and no
`/v1/regions` — so it has no hop 0, and the sentence the whole design rests on (*only hop 0 may say
something is not here*) has no third kind of thing to be confused about. That is why this is called an
exchange and not a backbone: an IX carries no prefixes of its own, and nobody mistakes one for a
network. Naming it "backbone zero" would have invited the next person to give it areas.

What it does is one thing: **gather what each member advertises and offer the union to all of them.**
Six backbones that all want to see each other need fifteen links; through here they need six. That is
a route reflector, and the arithmetic is the whole reason it exists.

To a backbone it is indistinguishable from any other peer — same `/v1/export` contract, same token
header, same read-only rule. No backbone has any code that knows what an exchange is, which is what
keeps this from being a second thing to keep in step with the first.

Three things it deliberately does not do:

  * **It does not decide what is shared.** An area crosses because somebody wrote `use_when_export` on
    it, in its own repository, through its own review queue. This reads what each member chose to
    publish and can no more widen that than any other peer can. If the export decision could be made
    here, the point of making it in the ontology would be gone.
  * **It does not store.** No repository, and answers are held only for the few seconds that stop a
    dead member costing every request a timeout. A copy of everyone's ontology in the middle is the
    thing all of this exists to avoid.
  * **It does not accept writes.** A link is read-only in both directions; a write goes to the
    backbone that owns the area.

One secret per member, used both ways: the exchange presents it when reading that member, and the
member presents it when reading the exchange. There is no shared password and no observer — so every
caller has a name, which is what lets a member be spared its own advertisement coming back at it.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

# The backbone's own peer client, not a second one. Reading a peer means telling three answers apart
# — it said no, I could not reach it, I could not read what it sent — and a second implementation of
# that would be a second thing to get wrong, in the one place where being wrong takes the absence rule
# down at every backbone attached.
#
# Beside this file in the image, where the Dockerfile copies it; in ontology/service when this is run
# from the repository, which is how the checks run it. Looking in both is what lets the same file be
# the thing that ships and the thing that is tested.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_HERE, os.path.join(os.path.dirname(_HERE), "ontology", "service")]
import peers as peering                                          # noqa: E402

NAME = (os.environ.get("EXCHANGE_NAME") or "exchange").strip()
MEMBERS = Path(os.environ.get("EXCHANGE_MEMBERS") or "/data/members.yaml")
PORT = int(os.environ.get("PORT") or 8110)
NAME_OK = re.compile(r"^[a-z][a-z0-9-]{0,30}$")


def members() -> list[dict]:
    """Who is attached, from `members.yaml`. Tokens come from the environment.

    Both sides declare: a backbone names this exchange in its own `peers.yaml`, and this names the
    backbone here. Nobody is enrolled by one side alone, which for a room that companies meet in is
    not a formality.
    """
    import yaml
    if not MEMBERS.is_file(): return []
    try: doc = yaml.safe_load(MEMBERS.read_text(encoding="utf-8")) or {}
    except Exception: return []
    out = []
    for row in (doc.get("members") or []):
        if not isinstance(row, dict): continue
        name, url = str(row.get("name") or "").strip(), str(row.get("url") or "").strip().rstrip("/")
        if not NAME_OK.match(name) or not url: continue
        env = str(row.get("token_env") or f"EXCHANGE_TOKEN_{name.upper().replace('-', '_')}")
        out.append({"name": name, "url": url, "token_env": env,
                    "token": (os.environ.get(env) or "").strip(),
                    "label": str(row.get("label") or name)})
    return out


def caller(token: str) -> dict | None:
    """Which member is asking, by the token it presented.

    One secret per member, used in both directions: the exchange presents it when reading that member
    and the member presents it when reading the exchange. So the two ends of a link share exactly one
    thing, and **the exchange always knows who is on the line** — which is what makes split horizon
    below possible at all. A shared password for everyone would have been simpler and would have made
    every caller anonymous, and an anonymous caller has to be sent its own areas back.
    """
    if not token: return None
    return next((m for m in members() if m["token"] and m["token"] == token), None)


def reflect(asking: dict | None = None) -> dict:
    """Everything the members are advertising, as one table.

    Each row keeps **the path it came by** — the members it passed through, nearest last. Two uses,
    and the second is the one that makes it necessary rather than nice:

      * an agent can see how far away a piece of knowledge is, and two hops away is somebody else's
        somebody else;
      * a row whose path already contains this exchange is dropped. Backbones never re-advertise what
        they learn, so a single exchange cannot loop — but two exchanges peering can, and then a row
        goes round for ever. This is BGP's AS_PATH, for BGP's reason.

    A member that cannot be read is reported, not hidden and not answered for. Whoever reads this has
    to be able to tell an empty room from a room it could not see into.
    """
    # Split horizon: a member is never sent what it advertised. Without it every backbone would see
    # its own areas twice — once locally, once reflected — under two different addresses, and the map
    # would draw its own expense area hanging off the exchange as if it belonged to somebody else.
    # The path makes this exact rather than approximate: it is dropped if the member is anywhere in
    # the path, not only at the end, so knowledge that went out through it and came back around a ring
    # of exchanges is dropped too.
    mine = asking["name"] if asking else None
    rows, links = [], []
    for m in members():
        state = {"name": m["name"], "label": m["label"], "url": m["url"],
                 "reachable": True, "revision": None, "areas": 0, "error": None}
        if not m["token"]:
            state.update(reachable=False, error=f"no token — set {m['token_env']}")
            links.append(state); continue
        try:
            adv = peering.advertisement(m)
        except peering.PeerError as e:
            state.update(reachable=False, error=str(e)); links.append(state); continue
        state["revision"] = adv.get("revision")
        kept = 0
        for r in (adv.get("regions") or []):
            path = [m["name"], *(r.get("path") or [])]
            if NAME in path: continue                       # it has been here before
            if mine and mine in path: continue              # split horizon — it came from the asker
            tail = str(r.get("fetch") or "")
            if not tail.startswith("/v1/export"): continue  # not something this contract can carry
            rows.append({**r, "path": path, "origin": path[-1],
                         "origin_revision": r.get("origin_revision") or adv.get("revision"),
                         "fetch": f"/v1/export/peers/{m['name']}" + tail[len("/v1/export"):]})
            kept += 1
        state["areas"] = kept
        links.append(state)
    # No repository, so no revision of its own. A digest of what was gathered is the honest answer to
    # "has anything changed since I last looked" and is what the members' staleness checks read.
    digest = hashlib.sha1(json.dumps([r.get("fetch") for r in rows] +
                                     [l.get("revision") for l in links],
                                     sort_keys=True).encode()).hexdigest()
    return {"revision": digest, "schema": "routemind-exchange/v1", "regions": rows, "members": links}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write(f"{self.address_string()} {fmt % args}\n")

    def _send(self, code, payload, ctype="application/json; charset=utf-8"):
        body = payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=1).encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def _err(self, code, msg, reason=None, data=None):
        self._send(code, {"error": msg, **({"reason": reason} if reason else {}),
                          **({"values": data} if data else {})})

    def do_GET(self):
        parts = [unquote(p) for p in urlparse(self.path).path.strip("/").split("/") if p]
        if parts == ["healthz"]:
            ms = members()
            return self._send(200, {"ok": True, "name": NAME, "members": [m["name"] for m in ms],
                                    "open": any(m["token"] for m in ms)})
        ms = members()
        if not any(m["token"] for m in ms):
            return self._err(501, "this exchange has no member it can speak to — see members.yaml "
                                  "and the token each entry names")
        who = caller(self.headers.get("X-Peer-Token") or "")
        if not who:
            # Only members read an exchange. There is no observer role: everything here belongs to
            # somebody, and handing it to an unnamed caller would be this exchange sharing what it
            # was only ever asked to carry.
            return self._err(401, "peer token missing or wrong")
        if parts[:2] != ["v1", "export"]: return self._err(404, "unknown path")
        rest = parts[2:]

        if rest == ["regions"]:
            return self._send(200, reflect(who))

        # Everything else is somebody's, and the address says whose.
        if len(rest) >= 3 and rest[0] == "peers":
            m = next((x for x in members() if x["name"] == rest[1]), None)
            if not m: return self._err(404, f"no member {rest[1]}")
            if not m["token"]: return self._err(503, f"member {rest[1]} has no token — set {m['token_env']}")
            try:
                raw, ctype = peering._fetch(m, "/v1/export/" + "/".join(rest[2:]))
            except peering.PeerError as e:
                return self._err(e.status, str(e),
                                 reason=("peer_said_no" if e.reachable else "peer_unreachable"),
                                 data={"peer": rest[1], "reachable": e.reachable})
            if "json" not in ctype.lower():
                # A document is carried as it is. There is nothing in one to rewrite, and re-encoding
                # somebody's prose on the way past would be this exchange editing it.
                return self._send(200, raw.decode("utf-8", "replace"), ctype)
            try: d = json.loads(raw or b"{}")
            except Exception as e:
                return self._err(502, f"member {rest[1]} sent something this exchange could not read: {type(e).__name__}",
                                 reason="peer_said_no", data={"peer": rest[1], "reachable": True})
            return self._send(200, _through(d, rest[1]), ctype)

        return self._err(404, "unknown export path")

    def do_POST(self): self._err(405, "an exchange is read-only — write to the backbone that owns it")
    do_PUT = do_PATCH = do_DELETE = do_POST


def _through(value, member: str):
    """Move every address in a member's answer onto this exchange.

    The member prints `/v1/export/nodes/x`, which at the reader would mean *the reader's* export
    surface. One prefix, applied to `fetch` and to nothing else — rewriting anything path-shaped would
    catch ids, prose and the bookkeeping fields nobody is meant to follow.
    """
    if isinstance(value, dict):
        return {k: (f"/v1/export/peers/{member}" + v[len("/v1/export"):]
                    if k == "fetch" and isinstance(v, str) and v.startswith("/v1/export/")
                    else _through(v, member))
                for k, v in value.items()}
    if isinstance(value, list): return [_through(v, member) for v in value]
    return value


def main():
    ms = members()
    sys.stderr.write(f"routemind-exchange name={NAME} members={[m['name'] for m in ms]} "
                     f"open={sum(1 for m in ms if m['token'])}/{len(ms)} port={PORT}\n")
    for m in ms:
        if not m["token"]: sys.stderr.write(f"  member {m['name']} has no token — set {m['token_env']}\n")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
