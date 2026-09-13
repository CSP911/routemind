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
# The operator's door, and a different one from the members'. What an operator needs is the plumbing —
# who is attached, is it answering, which revision — and **not** the knowledge, which is why /admin
# never returns a reflected row. A member reads what everyone published; an operator reads whether the
# room is working. Unset closes the door entirely.
ADMIN_TOKEN = (os.environ.get("EXCHANGE_ADMIN_TOKEN") or "").strip()
MEMBERS = Path(os.environ.get("EXCHANGE_MEMBERS") or "/data/members.yaml")
PORT = int(os.environ.get("PORT") or 8110)
NAME_OK = re.compile(r"^[a-z][a-z0-9-]{0,30}$")
# What an exchange calls itself in an advertisement. A neighbour reads it to know what it is talking
# to, which is how a mislabelled member is caught rather than believed.
SCHEMA = "routemind-exchange/v1"


def members() -> list[dict]:
    """Who is attached, from `members.yaml`. Tokens come from the environment.

    Both sides declare: a backbone names this exchange in its own `peers.yaml`, and this names the
    backbone here. Nobody is enrolled by one side alone, which for a room that companies meet in is
    not a formality.

    A member may itself be an exchange (`kind: exchange`), and the declaration rule does not change —
    it is the same two halves, with both of them now held by operators. Neither room joins the other
    on its own say-so, which is the whole of the answer to "who may enrol whom": **each side enrols
    the other, or there is no link.** What `kind` changes is not who may join but what is passed on;
    see `reflect`.
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
        kind = "exchange" if str(row.get("kind") or "").strip() == "exchange" else "backbone"
        out.append({"name": name, "url": url, "token_env": env, "kind": kind,
                    "token": (os.environ.get(env) or "").strip(),
                    # Every read this room makes says what is doing the reading. See `_fetch`.
                    "self_kind": "exchange",
                    "label": str(row.get("label") or name)})
    return out


def _raw_members() -> list[dict]:
    """The file as written, unresolved. Editing goes through this rather than through `members()`,
    which has already turned `token_env` into a token — writing that back would put a secret in a
    file whose whole point is that it holds none."""
    import yaml
    if not MEMBERS.is_file(): return []
    try: doc = yaml.safe_load(MEMBERS.read_text(encoding="utf-8")) or {}
    except Exception: return []
    return [m for m in (doc.get("members") or []) if isinstance(m, dict)]


def _write_members(rows: list[dict]) -> None:
    import yaml
    head = ("# Who meets here. The token for each is in the environment, not in this file.\n"
            "#\n"
            "# This is the exchange's half of the declaration; each backbone names the exchange in its\n"
            "# own peers.yaml. Both halves are needed, so nobody is enrolled by one side alone.\n")
    tmp = MEMBERS.with_suffix(".tmp")
    tmp.write_text(head + yaml.safe_dump({"members": rows}, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")
    tmp.replace(MEMBERS)                      # a reader never sees half a room


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


def reflect(asking: dict | None = None, claimed_kind: str | None = None) -> dict:
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

    **No transit.** An exchange offers a neighbouring exchange its own backbones, and never what a
    third exchange told it. So a row crosses at most one exchange-to-exchange hop, and the reason is
    not tidiness: carrying somebody else's knowledge to somebody else is a relationship neither of
    them agreed to, and the operator in the middle would be answering for two rooms that never met.
    An IX route server declines transit for the same reason, and it is what makes a ring of exchanges
    structurally unable to loop rather than merely unlikely to — the path can never grow long enough.
    Two rooms that do want each other's whole reach say so by both joining the third.

    The rule is applied **before** the neighbour is read, not to the rows that come back, and that is
    not an optimisation. Reading is a request, and a request that has to be answered by making the
    same request is how two rooms hang each other up: IX1 asks IX2 what it is advertising, IX2 asks
    IX1 to find out, and neither ever answers. Filtering afterwards would leave that intact and
    perfectly hidden — the rows would come out right whenever the timeout was longer than the wait.
    Skipping the read means an exchange answering an exchange asks nobody but its own backbones, so
    the depth of any gather is two and a room cannot be waiting on a room that is waiting on it.

    A member skipped this way is not reported either. Whether a third room is up is that room's
    business and the middle operator's; it is not part of what a neighbour is owed.

    **An audience is enforced here, and that is not a detail.** An area may name who it crosses to
    (`export_to`), and a backbone answering a room cannot apply that itself — it sees the room, not
    the reader. So it hands the room the rows with the audience written on them and this drops the
    ones the asker is not named in. Which means the room *sees* what it will not pass on: unavoidable,
    inherent to anything on the data path, and the reason docs/PEERING.md is blunt about who should
    run one. The document behind such a row is a different matter and is refused at the backbone that
    owns it — the listing is composed by whoever is speaking to the reader, the prose is served by
    whoever wrote it, and only the second of those is a boundary rather than a policy.

    The audience is stripped on the way out. It names members of *this* room, and a neighbouring room
    would be reading our roster in its own namespace — a list of strangers that happens to match some
    of its own members. To reach a neighbouring room, an area names the room.

    Two things say the asker is a room, and both are needed. `kind` in members.yaml is what stops the
    read from happening, and only a decision made before the read can prevent the hang. The asker's
    own `X-Peer-Kind` is what still holds when that label is typed wrong — and a mislabel is not a
    hypothetical, it is one word in one file with no way to be wrong loudly. Believing the asker is
    safe here and nowhere else, because the claim only ever gets the claimant less.
    """
    # Split horizon: a member is never sent what it advertised. Without it every backbone would see
    # its own areas twice — once locally, once reflected — under two different addresses, and the map
    # would draw its own expense area hanging off the exchange as if it belonged to somebody else.
    # The path makes this exact rather than approximate: it is dropped if the member is anywhere in
    # the path, not only at the end, so knowledge that went out through it and came back around a ring
    # of exchanges is dropped too.
    mine = asking["name"] if asking else None
    # An exchange asking is a different reader from a backbone asking, and the difference is what it
    # may be told about third parties — not what it may be told about this room's own members.
    to_exchange = (bool(asking) and asking.get("kind") == "exchange") or claimed_kind == "exchange"
    rows, links = [], []
    for m in members():
        if to_exchange and m["kind"] == "exchange": continue     # no transit, and no deadlock
        state = {"name": m["name"], "label": m["label"], "url": m["url"], "kind": m["kind"],
                 "reachable": True, "revision": None, "areas": 0, "error": None}
        if not m["token"]:
            state.update(reachable=False, error=f"no token — set {m['token_env']}")
            links.append(state); continue
        try:
            adv = peering.advertisement(m)
        except peering.PeerError as e:
            state.update(reachable=False, error=str(e)); links.append(state); continue
        state["revision"] = adv.get("revision")
        # What it answered, not what it was called. `kind` is written by hand and the cost of getting
        # it wrong is the one thing this rule exists to prevent — a room quietly carrying a third
        # room's knowledge — so the transit rule is decided by the schema the neighbour actually
        # sent. The declaration still matters: it is what stops the read from happening at all, and
        # only it can prevent the deadlock. This is the net under the leak, not under the hang.
        if adv.get("schema") == SCHEMA and m["kind"] != "exchange":
            state["error"] = (f"declared as a backbone but answers as an exchange — "
                              f"set kind: exchange on {m['name']} in members.yaml")
            if to_exchange: state["areas"] = 0; links.append(state); continue
        kept = 0
        for r in (adv.get("regions") or []):
            path = [m["name"], *(r.get("path") or [])]
            if NAME in path: continue                       # it has been here before
            if mine and mine in path: continue              # split horizon — it came from the asker
            aud = r.get("export_to") or []
            # No asker is the operator's health view, which counts rows and emits none.
            if aud and mine and mine not in aud: continue
            tail = str(r.get("fetch") or "")
            if not tail.startswith("/v1/export"): continue  # not something this contract can carry
            rows.append({**{k: v for k, v in r.items() if k != "export_to"},
                         "path": path, "origin": path[-1], "via_kind": m["kind"],
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
    return {"revision": digest, "schema": SCHEMA, "regions": rows, "members": links}


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
        if parts[:1] == ["admin"]: return self._admin("GET", parts[1:])
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
            return self._send(200, reflect(who, self.headers.get("X-Peer-Kind")))

        # Everything else is somebody's, and the address says whose.
        if len(rest) >= 3 and rest[0] == "peers":
            m = next((x for x in members() if x["name"] == rest[1]), None)
            if not m: return self._err(404, f"no member {rest[1]}")
            if not m["token"]: return self._err(503, f"member {rest[1]} has no token — set {m['token_env']}")
            try:
                # Whose reading this is. The member that owns the document applies the audience —
                # this room only says who is at the other end of it, which is the one thing it knows
                # and the backbone cannot.
                raw, ctype = peering._fetch(m, "/v1/export/" + "/".join(rest[2:]),
                                            on_behalf_of=who["name"])
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

    # ---- the operator's door ----
    def _admin_ok(self) -> bool:
        return bool(ADMIN_TOKEN) and self.headers.get("X-Admin-Token") == ADMIN_TOKEN

    def _admin(self, method: str, rest: list[str]):
        """Membership and health. Never the knowledge.

        An operator can see that BRANCH is attached, answering, and advertising two areas. What those
        areas are, and what is in them, is between the members — and an admin screen that could read
        it would be a way around the one rule this whole design turns on: an area crosses because
        somebody wrote `use_when_export` on it, in its own repository, through its own review queue.
        Nothing here can make an area cross, and nothing here can read one.
        """
        if not ADMIN_TOKEN:
            return self._err(501, "no operator door — set EXCHANGE_ADMIN_TOKEN")
        if not self._admin_ok():
            return self._err(401, "admin token missing or wrong")

        if rest == ["state"] and method == "GET":
            # Same gather the members get, with the rows thrown away. One code path, so the health an
            # operator reads is the health a member experiences and not a second opinion about it.
            r = reflect(None)
            counts = {}
            for row in r["regions"]: counts[row["origin"]] = counts.get(row["origin"], 0) + 1
            return self._send(200, {"ok": True, "name": NAME,
                                    "members": [{**m, "advertising": counts.get(m["name"], 0)}
                                                for m in r["members"]]})

        if rest == ["members"] and method in ("POST", "DELETE"):
            n = int(self.headers.get("Content-Length") or 0)
            try: body = json.loads(self.rfile.read(n) or b"{}")
            except Exception: return self._err(422, "body must be JSON")
            if not isinstance(body, dict): return self._err(422, "body must be an object")
            name = str(body.get("name") or "").strip()
            if not NAME_OK.match(name): return self._err(400, "name must be ASCII kebab-case")
            try:
                if method == "DELETE": _write_members([m for m in _raw_members() if m.get("name") != name])
                else:
                    url = str(body.get("url") or "").strip().rstrip("/")
                    if not url.startswith(("http://", "https://")): return self._err(400, "url must be http(s)")
                    kind = str(body.get("kind") or "backbone").strip()
                    if kind not in ("backbone", "exchange"):
                        return self._err(400, "kind must be backbone or exchange")
                    rows = [m for m in _raw_members() if m.get("name") != name]
                    rows.append({"name": name, "label": str(body.get("label") or name.upper()),
                                 "url": url, "kind": kind,
                                 "token_env": str(body.get("token_env")
                                                  or f"EXCHANGE_TOKEN_{name.upper().replace('-', '_')}")})
                    _write_members(sorted(rows, key=lambda m: m["name"]))
            except OSError as e:
                return self._err(500, f"members.yaml is not writable: {e}")
            peering.forget()          # the room changed; do not answer from the old one
            return self._send(200, {"ok": True, "members": [m["name"] for m in members()]})

        return self._err(404, "unknown admin path")

    def do_POST(self):
        parts = [unquote(p) for p in urlparse(self.path).path.strip("/").split("/") if p]
        if parts[:1] == ["admin"]: return self._admin("POST", parts[1:])
        self._err(405, "an exchange is read-only — write to the backbone that owns it")

    def do_DELETE(self):
        parts = [unquote(p) for p in urlparse(self.path).path.strip("/").split("/") if p]
        if parts[:1] == ["admin"]: return self._admin("DELETE", parts[1:])
        self._err(405, "an exchange is read-only — write to the backbone that owns it")

    def do_PUT(self): self._err(405, "an exchange is read-only — write to the backbone that owns it")
    do_PATCH = do_PUT


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
