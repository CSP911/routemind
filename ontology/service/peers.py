"""Links to other backbones: reading what they advertise, and relaying what they hold.

A peer is another RouteMind, declared in `peers.yaml` in this repository. What crosses is its
**export advertisement** — the areas it set `export` on — and, on request, the
documents behind them. Nothing crosses the other way: writes go to the backbone that owns the area.

Three decisions live here, and each of them is the interesting kind.

**Documents are relayed, not linked to.** The table this backbone prints hands out its own addresses
(`/v1/peers/<name>/…`), and reading one makes this service fetch from the peer. The alternative —
printing the peer's own URL and letting the agent fetch it — is simpler and wrong for one reason
that outweighs the rest: every agent would then need every peer's credential. Relaying keeps the
credential in one place, in this service's environment, the way the LLM key already is. Firewalls
are the second reason and the smaller one.

**Nothing is cached beyond a breath.** `ADVERT_TTL` is five seconds and covers failures as well as
answers: it is there so that a peer which is slow or gone does not cost every request the full
timeout, not so that this backbone can answer for one. A failure is never served from an earlier
success. Documents are not cached at all — a cache of somebody else's ontology is a copy of it, and a
copy is the thing a link exists to avoid; the moment this service can answer from a copy, two
installs that were meant to stay separate have quietly become one with a replication lag.

**"The peer said no", "I could not reach the peer", and "I could not use what it sent" are three
answers, not two.** Only a backbone's own hop 0 may say something is not there. A 404 relayed from a
peer is that backbone speaking; a timeout is nobody speaking and must never be dressed as an absence;
and a reply this code could not parse is **our** failure, not the link's. Collapsing the third into
the second is how a bug here gets reported as somebody else's outage — and it did: a document body is
Markdown, this module assumed JSON, and every remote document came back as "peer is unreachable"
while the peer was answering perfectly. `reachable` is the flag hop 0 stops claiming absence on, so
mislabelling one of these suspends the absence rule for a reason that is not true.
"""
from __future__ import annotations

import contextlib
import hashlib
import hmac
import ipaddress
import json
import os
import secrets
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

# Five seconds, not thirty. The cache exists for the sad path — a peer that is slow or gone would
# otherwise cost every single request the full timeout — and for collapsing the burst of calls one
# agent run makes. It is not there to spare the happy path a few milliseconds on a local network.
#
# The number is small because of what it bounds. While a success is cached, a link that has just died
# still reads as alive, and hop 0 still tells an agent it may claim absence — the one thing the design
# does not allow. No cache makes that window zero, so the honest thing is to keep it short and say
# what it is, which docs/PEERING.md does.
ADVERT_TTL = float(os.environ.get("ONTOLOGY_PEER_TTL") or 5.0)
TIMEOUT = float(os.environ.get("ONTOLOGY_PEER_TIMEOUT") or 4.0)
# How far a "re-read me" is passed on. Two covers the shape this supports — a backbone, its room, and
# the rooms that room meets — and any bound at all is what makes the flood terminate. Not a setting:
# it is a safety bound, and the only reason to turn it up is a topology this does not have.
REFRESH_HOPS = 2
NAME_OK = __import__("re").compile(r"^[a-z][a-z0-9-]{0,30}$")

# ── session tokens ────────────────────────────────────────────────────────────
# The secret in `.env` used to be presented on every read, so it was in every request, every proxy
# log and every transcript — and it never expired. Two of them leaked into a working session while
# this was being built, and both stayed valid.
#
# Operator, 2026-09-29: six hours. The secret becomes an **enrolment key**, good for one thing —
# asking for a session token — and the session token is what the read path carries. The long-lived
# secret is then used about four times a day per link instead of on every request, and anything that
# does leak off the read path dies by the end of the shift.
#
# What this does **not** fix, said here so nobody reads it as more than it is: a short-lived bearer
# token handed to an endpoint that is not who it claims to be is still handed over. This shortens
# how long a leak is worth something; it does not prove who is at the far end.
SESSION_TTL = float(os.environ.get("ONTOLOGY_PEER_SESSION_TTL") or 6 * 3600)
# In memory, so a restart revokes every session. That is a feature and the cheapest revocation there
# is: the clients below re-mint on a 401, so the cost of it is one extra round trip per link.
_SESSIONS: dict[str, dict] = {}
_SESSION_LOCK = threading.Lock()
# A ceiling, so a caller that mints in a loop cannot grow this without bound. Well above one per
# link per six hours; reaching it means something is wrong, and dropping the oldest is the failure
# that costs a round trip rather than memory.
MAX_SESSIONS = 512


def mint_session(peer: str | None) -> tuple[str, int]:
    """A session token for `peer`, and how many seconds it is good for."""
    now = time.time()
    token = secrets.token_urlsafe(32)
    with _SESSION_LOCK:
        for k in [k for k, v in _SESSIONS.items() if v["expires"] <= now]: _SESSIONS.pop(k, None)
        while len(_SESSIONS) >= MAX_SESSIONS:
            _SESSIONS.pop(min(_SESSIONS, key=lambda k: _SESSIONS[k]["expires"]), None)
        _SESSIONS[token] = {"peer": peer, "expires": now + SESSION_TTL}
    return token, int(SESSION_TTL)


def session_peer(token: str | None) -> dict | None:
    """Whose session this is, or None. Expiry is checked here and nowhere else.

    Compared with `compare_digest` against each candidate rather than by dict lookup: a dict lookup
    on a secret is a hash-table probe whose timing depends on the key, and this runs on every read
    across every link.
    """
    if not token: return None
    now = time.time()
    with _SESSIONS_snapshot() as rows:
        for stored, row in rows:
            if row["expires"] > now and hmac.compare_digest(stored, token):
                return {"peer": row["peer"], "expires": row["expires"]}
    return None


@contextlib.contextmanager
def _SESSIONS_snapshot():
    with _SESSION_LOCK:
        rows = list(_SESSIONS.items())
    yield rows


# ── the other side of it: holding one ────────────────────────────────────────
# What this backbone presents when it reads somebody else. One session per (url, key), renewed a
# minute before it expires so a read never lands on the boundary, and dropped on a 401 so a restart
# at the far end costs one extra round trip rather than an outage.
_HELD: dict[str, dict] = {}
_HELD_LOCK = threading.Lock()
RENEW_MARGIN = 60.0


def session_for(url: str, key: str, timeout: float | None = None) -> str:
    """A session token to read `url` with, minted from `key` if there is not a live one.

    Raises PeerError on failure, so a caller sees the same shape as any other link failure — a peer
    that will not issue a token is a peer that cannot be read, and the two must not be distinguished
    by how the error arrives.
    """
    ident = url.rstrip("/")
    now = time.time()
    with _HELD_LOCK:
        held = _HELD.get(ident)
        if held and held["expires"] - RENEW_MARGIN > now and hmac.compare_digest(held["key"], key):
            return held["token"]
    req = urllib.request.Request(ident + "/v1/peers/token", data=b"", method="POST",
                                 headers={"X-Peer-Token": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout or TIMEOUT) as r:
            doc = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 401 here is the enrolment key being wrong, which is a different thing from a session having
        # expired and needs saying differently — one is a configuration error and the other is time
        # passing.
        raise PeerError(f"{ident} refused the enrolment key (HTTP {e.code}) — check the token in the "
                        f"environment against what that backbone accepts", status=e.code, reachable=True)
    except Exception as e:
        raise PeerError(f"{ident} could not be asked for a session token ({e})", status=504, reachable=False)
    token = str(doc.get("token") or "")
    if not token:
        raise PeerError(f"{ident} answered the token request without a token", status=502, reachable=True)
    with _HELD_LOCK:
        _HELD[ident] = {"token": token, "key": key,
                        "expires": now + float(doc.get("expires_in") or SESSION_TTL)}
    return token


def forget_session(url: str) -> None:
    """Drop the held token for a backbone. Called on a 401, so the next read mints a fresh one."""
    with _HELD_LOCK:
        _HELD.pop(url.rstrip("/"), None)


_DECLARED_SEEN: dict[str, str] = {}


def sessions_follow(rows: list[dict], where: str = "self") -> bool:
    """Drop every session when the set of declared peers changes. True when it did.

    A session records who the far end decided the caller was, at the moment it was minted. So a
    backbone that starts recognising somebody by name — or stops — would otherwise keep answering
    them as they were for up to six hours, and "I added them to peers.yaml and nothing happened" is
    the shape of that.

    Cheap enough to do on the read path: `declared()` already reads the file per request, so this is
    a hash of what it returned. Dropping *all* sessions rather than the affected ones is deliberate —
    who a caller is can change without their own row changing, because an audience is a list and
    removing one name changes what every other name means.
    """
    mark = hashlib.sha256(json.dumps(
        sorted((r.get("name"), tuple(sorted(r.get("accept") or []))) for r in rows)).encode()
    ).hexdigest()
    if _DECLARED_SEEN.get(where) == mark: return False
    first = where not in _DECLARED_SEEN
    _DECLARED_SEEN[where] = mark
    if not first: drop_sessions()
    return not first


def drop_sessions(peer: str | None = None) -> int:
    """Revoke. All of them, or one peer's — what "stop renewing" looks like when it has to be now."""
    with _SESSION_LOCK:
        doomed = [k for k, v in _SESSIONS.items() if peer is None or v["peer"] == peer]
        for k in doomed: _SESSIONS.pop(k, None)
    return len(doomed)


def same_secret(given: str | None, expected: str | None) -> bool:
    """Compare two secrets without leaking how far the comparison got.

    `==` on strings stops at the first differing byte, so how long it takes says how much of a guess
    was right. Over a link between organisations that is a way in that needs no bug and no mistake by
    anybody — just patience — and the fix is one function. An empty expected secret matches nothing:
    a link with no token configured is closed, never open to everyone.
    """
    if not given or not expected: return False
    return hmac.compare_digest(str(given), str(expected))


def public_address(url: str) -> bool:
    """Would a secret sent here cross a network nobody in this deployment controls?

    `http://` to a name that resolves outside the machine and outside a private range is a bearer
    token in clear text on the wire. Inside a compose network or a VPN that is the normal, reasonable
    shape and this must not get in its way; to a public address it is the difference between a link
    between two companies and a link between two companies and whoever is in between.

    Unresolvable is **not** treated as public. A peer that is simply down would otherwise turn into a
    refusal about secrecy, which sends whoever reads it looking in the wrong place entirely.
    """
    try:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "http": return False              # https carries it, and so does anything else declared
        host = parts.hostname or ""
        if not host: return False
        try: infos = socket.getaddrinfo(host, None)
        except OSError: return False                         # cannot say; not the same as "it is public"
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            if not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved):
                return True
        return False
    except Exception:
        return False


class PeerError(Exception):
    """A link failed. `reachable` says whether the peer answered at all — see the module docstring:
    a refusal from a peer and a peer that is not there are not the same fact."""

    def __init__(self, message: str, *, status: int = 502, reachable: bool = False):
        super().__init__(message)
        self.status, self.reachable = status, reachable


def declared(root: Path) -> list[dict]:
    """The peers this backbone has, from `peers.yaml`.

    In the repository and not in the environment, because who this backbone is linked to is part of
    what it is: it belongs in git, in review, and in the history. The *token* is the opposite and
    comes from the environment — the same split `.env` already makes for the LLM key.

    A malformed file is empty rather than fatal. A backbone that cannot read its peer list still
    serves its own areas correctly, and refusing to start over a link would make the link a
    dependency of the thing it is supposed to be beside.
    """
    p = Path(root) / "peers.yaml"
    if not p.is_file(): return []
    try: doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception: return []
    out = []
    for row in (doc.get("peers") or []):
        if not isinstance(row, dict): continue
        name, url = str(row.get("name") or "").strip(), str(row.get("url") or "").strip().rstrip("/")
        if not NAME_OK.match(name) or not url: continue
        # The name is a path segment in every address this backbone prints for that peer, so it is
        # held to the same shape an id is. A peer called "../" would be an address nobody could trust.
        env = str(row.get("token_env") or f"ONTOLOGY_PEER_TOKEN_{name.upper().replace('-', '_')}")
        # An exchange is a peer like any other to read *from* — no backbone has code that knows what
        # one is. Saying so here changes one thing only, and in the other direction: a peer marked
        # this way is believed when it says which of its members it is fetching on behalf of. An
        # ordinary peer is not, because that claim can only ever get a caller **more**.
        kind = "exchange" if str(row.get("kind") or "").strip() == "exchange" else "backbone"
        out.append({"name": name, "url": url, "token_env": env, "kind": kind,
                    "token": (os.environ.get(env) or "").strip(),
                    # What is still accepted from this peer while a secret is being changed. One
                    # secret per link means changing it is a flag day unless both are good for a
                    # while: add the new one here on both sides, switch what each presents, then
                    # drop the old. Without it the only way to rotate is to stop both ends together,
                    # which is why nobody rotates.
                    "accept": _accepted(env, row.get("also_accept_env")),
                    "label": str(row.get("label") or name)})
    return out


def _accepted(env: str, also: object) -> list[str]:
    """Every secret a peer may present: the current one, and the one being retired if there is one."""
    names = [env] + ([str(also).strip()] if str(also or "").strip() else [])
    return [v for v in ((os.environ.get(n) or "").strip() for n in names) if v]


# name -> (when, advertisement or None, error). A failure is remembered for the same window as a
# success, and for the stronger reason: without it a peer that is down costs every request the full
# timeout, and hop 0 — which every run reads — becomes as slow as the slowest thing anyone linked to.
_cache: dict[str, tuple[float, dict | None, str]] = {}


def _fetch(peer: dict, path: str, *, on_behalf_of: str | None = None) -> tuple[bytes, str]:
    """The bytes a peer sent, and what it says they are. Not parsed here.

    A backbone answers JSON for tables and `text/markdown` for a document body, and which one is a
    property of the address, not of the link. Deciding here would mean this module knowing the shape
    of every answer the other side can give — a second place to update whenever that changes, and the
    place a Markdown body was being fed to a JSON parser.
    """
    url = peer["url"] + path
    if peer["token"] and public_address(peer["url"]):
        # Refused here rather than sent and regretted. This is the one failure in this module that is
        # neither the peer saying no nor the peer being unreachable, and it is ours — so it is
        # `reachable=True`: the absence rule must not be suspended over a link this end declined to
        # use. See docs/PEERING.md, "A secret and a public address".
        raise PeerError(f"peer {peer['name']} is at a public address over plain http — its token "
                        f"would go out in clear text. Use https, or put the link on a network you "
                        f"control", status=502, reachable=True)
    def build(tok):
        r = urllib.request.Request(url, headers={"Accept": "application/json, text/markdown, */*"})
        # A six-hour session rather than the enrolment key, which now opens nothing but the mint.
        # Held per backbone and renewed a minute early, so this costs one extra round trip about
        # four times a day per link instead of carrying a permanent secret on every read.
        if tok: r.add_header("X-Peer-Token", tok)
        if peer.get("self_kind"): r.add_header("X-Peer-Kind", str(peer["self_kind"]))
        if on_behalf_of: r.add_header("X-Peer-For", on_behalf_of)
        return r

    req = build(session_for(peer["url"], peer["token"]) if peer["token"] else "")
    # What the *caller* is, said by the caller (`X-Peer-Kind`, set in `build`): an exchange announces
    # itself so the far end can withhold what it does not carry for third parties, and this is safe
    # to believe for the reason that makes self-declaration usually unsafe reversed — the claim can
    # only ever get the claimant **less**. Nobody lies their way into more. `X-Peer-For` says who it
    # is being fetched for, when that is not us; only an exchange sets it.
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read(), (r.headers.get("Content-Type") or "application/json")
    except urllib.error.HTTPError as e:
        # A 401 is the far end having restarted, or six hours having passed at an awkward moment.
        # Held tokens are dropped and it is tried once more — a peer that restarts must cost a round
        # trip, not an outage, and without this every link would fail for one read after any restart.
        if e.code == 401 and peer["token"]:
            forget_session(peer["url"])
            try:
                with urllib.request.urlopen(build(session_for(peer["url"], peer["token"])),
                                            timeout=TIMEOUT) as r:
                    return r.read(), (r.headers.get("Content-Type") or "application/json")
            except urllib.error.HTTPError as e2:
                raise PeerError(f"peer {peer['name']} answered {e2.code}", status=e2.code, reachable=True) from e2
            except Exception as e2:
                raise PeerError(f"peer {peer['name']} is unreachable: {type(e2).__name__}", status=504,
                                reachable=False) from e2
        # The peer answered. Whatever it said is its own answer and is carried through as one —
        # a 404 from over there means *that* backbone does not have it, which is a fact worth having.
        raise PeerError(f"peer {peer['name']} answered {e.code}", status=e.code, reachable=True) from e
    except Exception as e:
        raise PeerError(f"peer {peer['name']} is unreachable: {type(e).__name__}", status=504,
                        reachable=False) from e


def _fetch_json(peer: dict, path: str) -> dict:
    raw, _ = _fetch(peer, path)
    try:
        return json.loads(raw or b"{}")
    except Exception as e:
        # Reachable, on purpose. The peer answered; this side could not read it. Saying "unreachable"
        # would take the absence rule down over a bug in here.
        raise PeerError(f"peer {peer['name']} sent something this backbone could not read: "
                        f"{type(e).__name__}", status=502, reachable=True) from e


def advertisement(peer: dict) -> dict:
    """What this peer is advertising, or the failure, remembered for `ADVERT_TTL` either way.

    A failure is **never** answered from an earlier success. A stale advertisement served as a live
    one is how a link that is down looks exactly like a link that is up, and the whole point of
    telling those apart is that hop 0 stops claiming absence when one is down. Falling back to the
    last good answer would make that impossible to notice, which is worse than the outage.
    """
    hit = _cache.get(peer["name"])
    if hit and (time.monotonic() - hit[0]) < ADVERT_TTL:
        if hit[1] is not None: return hit[1]
        raise PeerError(hit[2], status=504, reachable=False)
    try:
        d = _fetch_json(peer, "/v1/export/regions")
    except PeerError as e:
        _cache[peer["name"]] = (time.monotonic(), None, str(e))
        raise
    _cache[peer["name"]] = (time.monotonic(), d, "")
    return d


def forget(name: str | None = None) -> None:
    """Drop what is remembered about a peer, so the next read goes to the wire. For the checks, and
    for a person who has just fixed something on the other side and does not want to wait it out."""
    if name is None: _cache.clear()
    else: _cache.pop(name, None)


def announce(root: Path, *, self_kind: str | None = None) -> None:
    """Tell every peer that what this backbone advertises has changed, so they re-read it now.

    **A hint, not a protocol.** Nothing depends on it arriving: `ADVERT_TTL` is the guarantee and this
    only shortens the window it leaves. Failures are swallowed for that reason — a peer that is down
    is not a reason to fail somebody's save, and it will read the new set within seconds of coming
    back anyway.

    Worth having for one case, and it is not symmetry. Advertising something a few seconds late is a
    delay; **withdrawing** something a few seconds late is the withdrawn thing still sitting on
    somebody else's table, and narrowing an audience is a withdrawal for whoever just left the list.
    The two directions are not equally forgiving, so the one that is not gets a push.
    """
    poke(declared(root), self_kind=self_kind)


def poke(targets: list[dict], *, hops: int = REFRESH_HOPS, self_kind: str | None = None) -> None:
    """Send the hint to these peers. `hops` is a budget and not a route.

    A room passes the hint on to its own members, which is the only way a withdrawal two rooms out
    arrives before the cache expires. Passing it on is also how a ring of rooms would send it round
    for ever, and unlike an advertisement a hint carries no path to check itself against. So it
    carries a number that only goes down, and the flood stops because it must, not because the
    topology happens to be a tree.
    """
    for peer in targets:
        if not peer["token"]: continue
        req = urllib.request.Request(peer["url"] + "/v1/export/refresh", data=b"", method="POST")
        # `refresh` is on the export surface and takes a session like every other call there. A
        # failure here is already swallowed below — a peer that will not answer a hint is a peer that
        # re-reads a few seconds later — so a token this cannot mint is the same non-event.
        try:
            req.add_header("X-Peer-Token", session_for(peer["url"], peer["token"]))
        except PeerError:
            continue
        req.add_header("X-Refresh-Hops", str(max(0, int(hops))))
        if self_kind or peer.get("self_kind"):
            req.add_header("X-Peer-Kind", str(self_kind or peer["self_kind"]))
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r: r.read()
        except Exception:
            pass


def rows(root: Path) -> tuple[list[dict], list[dict]]:
    """Every peer's advertised areas, as hop-0 rows, and the state of each link.

    The rows carry **this** backbone's addresses, not the peer's: an agent follows `/v1/peers/hq/…`
    and this service does the fetching. The advertisement's own `fetch` is on the peer's export
    surface and is not something anyone here should hand out.
    """
    out, links = [], []
    for peer in declared(root):
        # `note` is not `error`: the link is up and carrying rows, and calling it down would suspend
        # the absence rule over a configuration detail. It is the other thing a link can be — working,
        # and not doing what somebody thinks it is doing.
        state = {"name": peer["name"], "label": peer["label"], "url": peer["url"],
                 "reachable": True, "revision": None, "areas": 0, "error": None, "note": None}
        if not peer["token"]:
            # Named, so that "the link is doing nothing" is never a mystery: the variable this
            # install has to set is in the answer.
            state.update(reachable=False, error=f"no token — set {peer['token_env']}")
            links.append(state); continue
        try:
            adv = advertisement(peer)
        except PeerError as e:
            state.update(reachable=False, error=str(e)); links.append(state); continue
        state["revision"] = adv.get("revision")
        # What it answered, against what it was called. `kind: exchange` is one word typed by hand
        # into a file, and getting it wrong here fails **silently**: a room is handed the filtered
        # set instead of the tagged one, so audiences and per-peer lines quietly stop working, and a
        # document restricted to this backbone comes back 404 because the room could not say who it
        # was fetching for. Everything looks up. This is the same net the exchange has for the
        # mirror-image mistake — and unlike there, no header can stand in for the label: believing a
        # caller that says it is a room would get that caller **more**, which is the one direction a
        # claim must never be taken on the caller's word.
        if adv.get("schema") == "routemind-exchange/v1" and peer["kind"] != "exchange":
            state["note"] = (f"declared as a backbone but answers as an exchange — add `kind: exchange` "
                             f"to {peer['name']} in peers.yaml. Until then this backbone filters for "
                             f"the room instead of for its members, so an audience and a line written "
                             f"for one peer do nothing")
        for r in (adv.get("regions") or []):
            # From the peer's own `fetch`, not rebuilt from `source`. Rebuilding assumed the thing was
            # one hop away and always produced `/v1/peers/<peer>/regions/<src>` — which is right for a
            # backbone and drops the middle of `/v1/export/peers/gamma/regions/x`, the shape an
            # exchange prints for something behind it. The address is the peer's to compose; this end
            # only moves it onto its own surface, the same rule `_rewrite` applies coming back.
            tail = str(r.get("fetch") or "")
            if not tail.startswith("/v1/export"): continue
            out.append({**{k: r.get(k) for k in ("id", "source", "title", "description", "use_when",
                                                 "representative")},
                        "peer": peer["name"], "peer_label": peer["label"],
                        "peer_revision": r.get("origin_revision") or adv.get("revision"),
                        # How far away, and through whom. Nearest last, this end prepended — so a row
                        # reads as the trail it actually travelled.
                        "path": [peer["name"], *(r.get("path") or [])],
                        "origin": r.get("origin") or peer["name"],
                        "fetch": f"/v1/peers/{peer['name']}" + tail[len("/v1/export"):]})
        state["areas"] = len(adv.get("regions") or [])
        links.append(state)
    return out, links


def relay(root: Path, name: str, rest: list[str]) -> tuple[object, str]:
    """Fetch one thing from a peer, on behalf of a caller who never sees the credential.

    Returns what came and what it is. A table comes back as a dict with its addresses rewritten; a
    document body comes back as the text it is, untouched — there is nothing in a document to rewrite
    and re-encoding somebody else's prose as JSON would be this backbone editing it.
    """
    peer = next((p for p in declared(root) if p["name"] == name), None)
    if not peer: raise PeerError(f"no peer {name}", status=404, reachable=True)
    if not peer["token"]: raise PeerError(f"peer {name} has no token — set {peer['token_env']}", status=503)
    path = "/v1/export/" + "/".join(urllib.parse.quote(p, safe="") for p in rest)
    raw, ctype = _fetch(peer, path)
    if "json" not in ctype.lower():
        return raw.decode("utf-8", "replace"), ctype
    try:
        d = json.loads(raw or b"{}")
    except Exception as e:
        raise PeerError(f"peer {name} sent something this backbone could not read: {type(e).__name__}",
                        status=502, reachable=True) from e
    # Every address inside a relayed answer is one the peer prints on its own export surface, and
    # following one of those directly would need the credential this service is holding. They are
    # rewritten to point back here, which is also what makes the rule the tables state — "use the
    # address exactly as printed" — remain true across a link.
    return _rewrite(d, name), ctype


def _rewrite(value, name: str):
    if isinstance(value, dict):
        return {k: (f"/v1/peers/{name}{v[len('/v1/export'):]}"
                    if k == "fetch" and isinstance(v, str) and v.startswith("/v1/export/")
                    else _rewrite(v, name))
                for k, v in value.items()}
    if isinstance(value, list): return [_rewrite(v, name) for v in value]
    return value
