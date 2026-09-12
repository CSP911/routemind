"""Links to other backbones: reading what they advertise, and relaying what they hold.

A peer is another RouteMind, declared in `peers.yaml` in this repository. What crosses is its
**export advertisement** — the areas it wrote a `use_when_export` for — and, on request, the
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

**"The peer said no" and "I could not reach the peer" are different answers.** Only a backbone's own
hop 0 may say something is not there. A 404 relayed from a peer is that backbone speaking; a timeout
is nobody speaking, and must never be dressed as an absence. Everything below keeps them apart, and
`unreachable` is what makes hop 0 stop claiming absence at all.
"""
from __future__ import annotations

import json
import os
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
NAME_OK = __import__("re").compile(r"^[a-z][a-z0-9-]{0,30}$")


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
        out.append({"name": name, "url": url, "token_env": env,
                    "token": (os.environ.get(env) or "").strip(),
                    "label": str(row.get("label") or name)})
    return out


# name -> (when, advertisement or None, error). A failure is remembered for the same window as a
# success, and for the stronger reason: without it a peer that is down costs every request the full
# timeout, and hop 0 — which every run reads — becomes as slow as the slowest thing anyone linked to.
_cache: dict[str, tuple[float, dict | None, str]] = {}


def _fetch(peer: dict, path: str) -> dict:
    url = peer["url"] + path
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    if peer["token"]: req.add_header("X-Peer-Token", peer["token"])
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        # The peer answered. Whatever it said is its own answer and is carried through as one —
        # a 404 from over there means *that* backbone does not have it, which is a fact worth having.
        raise PeerError(f"peer {peer['name']} answered {e.code}", status=e.code, reachable=True) from e
    except Exception as e:
        raise PeerError(f"peer {peer['name']} is unreachable: {type(e).__name__}", status=504,
                        reachable=False) from e


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
        d = _fetch(peer, "/v1/export/regions")
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


def rows(root: Path) -> tuple[list[dict], list[dict]]:
    """Every peer's advertised areas, as hop-0 rows, and the state of each link.

    The rows carry **this** backbone's addresses, not the peer's: an agent follows `/v1/peers/hq/…`
    and this service does the fetching. The advertisement's own `fetch` is on the peer's export
    surface and is not something anyone here should hand out.
    """
    out, links = [], []
    for peer in declared(root):
        state = {"name": peer["name"], "label": peer["label"], "url": peer["url"],
                 "reachable": True, "revision": None, "areas": 0, "error": None}
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
        for r in (adv.get("regions") or []):
            src = str(r.get("source") or "").replace("_", "-")
            if not src: continue
            out.append({**{k: r.get(k) for k in ("id", "source", "title", "description", "use_when",
                                                 "representative")},
                        "peer": peer["name"], "peer_label": peer["label"],
                        "peer_revision": adv.get("revision"),
                        "fetch": f"/v1/peers/{peer['name']}/regions/{src}"})
        state["areas"] = len(adv.get("regions") or [])
        links.append(state)
    return out, links


def relay(root: Path, name: str, rest: list[str]) -> dict:
    """Fetch one thing from a peer, on behalf of a caller who never sees the credential."""
    peer = next((p for p in declared(root) if p["name"] == name), None)
    if not peer: raise PeerError(f"no peer {name}", status=404, reachable=True)
    if not peer["token"]: raise PeerError(f"peer {name} has no token — set {peer['token_env']}", status=503)
    path = "/v1/export/" + "/".join(urllib.parse.quote(p, safe="") for p in rest)
    d = _fetch(peer, path)
    # Every address inside a relayed answer is one the peer prints on its own export surface, and
    # following one of those directly would need the credential this service is holding. They are
    # rewritten to point back here, which is also what makes the rule the tables state — "use the
    # address exactly as printed" — remain true across a link.
    return _rewrite(d, name)


def _rewrite(value, name: str):
    if isinstance(value, dict):
        return {k: (f"/v1/peers/{name}{v[len('/v1/export'):]}"
                    if k == "fetch" and isinstance(v, str) and v.startswith("/v1/export/")
                    else _rewrite(v, name))
                for k, v in value.items()}
    if isinstance(value, list): return [_rewrite(v, name) for v in value]
    return value
