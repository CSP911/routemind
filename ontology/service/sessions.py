"""Six-hour session tokens for the export surface — what another RouteMind's circuit reads.

A circuit (`knowledge_circuit`, in the reader's MCP server) presents this backbone's **enrolment key**
once, to `POST /v1/peers/token`, and gets a session token good for six hours; every read on
`/v1/export/…` carries the session, not the key. The key is `ONTOLOGY_PEER_TOKEN`.

The secret used to be presented on every read, so it was in every request, every proxy log and every
transcript — and it never expired. Two leaked into a working session while this was being built, and
both stayed valid. Operator, 2026-09-29: six hours. The long-lived secret is then used about four
times a day per reader instead of on every request, and anything that leaks off the read path dies
by the end of the shift.

What this does **not** fix: a short-lived bearer token handed to an endpoint that is not who it
claims to be is still handed over. This shortens how long a leak is worth something; it does not prove
who is at the far end.

This was `peers.py` until 2026-10-08, which also held standing links between backbones (`peers.yaml`),
the exchange they met at, and the relay that fetched across them. Those were retired; a circuit is the
one way left to read another backbone, and this is all of the old module it needs.
"""
from __future__ import annotations

import hmac
import os
import secrets
import threading
import time

SESSION_TTL = float(os.environ.get("ONTOLOGY_PEER_SESSION_TTL") or 6 * 3600)
# In memory, so a restart revokes every session. That is a feature and the cheapest revocation there
# is: a circuit re-mints on a 401, so the cost of it is one extra round trip.
_SESSIONS: dict[str, float] = {}
_LOCK = threading.Lock()
# A ceiling, so a caller that mints in a loop cannot grow this without bound. Reaching it means
# something is wrong, and dropping the oldest is the failure that costs a round trip rather than memory.
MAX_SESSIONS = 512


def mint() -> tuple[str, int]:
    """A session token, and how many seconds it is good for."""
    now = time.time()
    token = secrets.token_urlsafe(32)
    with _LOCK:
        for k in [k for k, exp in _SESSIONS.items() if exp <= now]: _SESSIONS.pop(k, None)
        while len(_SESSIONS) >= MAX_SESSIONS:
            _SESSIONS.pop(min(_SESSIONS, key=_SESSIONS.get), None)
        _SESSIONS[token] = now + SESSION_TTL
    return token, int(SESSION_TTL)


def valid(token: str | None) -> bool:
    """Is this a live session? Expiry is checked here and nowhere else.

    Compared with `compare_digest` against each candidate rather than by dict lookup: a dict lookup on
    a secret is a hash-table probe whose timing depends on the key.
    """
    if not token: return False
    now = time.time()
    with _LOCK:
        rows = list(_SESSIONS.items())
    return any(exp > now and hmac.compare_digest(stored, token) for stored, exp in rows)


def drop_all() -> int:
    """Revoke every session — what "stop" looks like when it has to be now."""
    with _LOCK:
        n = len(_SESSIONS); _SESSIONS.clear()
    return n


def same_secret(given: str | None, expected: str | None) -> bool:
    """Compare two secrets without leaking how far the comparison got.

    `==` on strings stops at the first differing byte, so how long it takes says how much of a guess
    was right. An empty expected secret matches nothing: a backbone with no key configured is closed,
    never open to everyone.
    """
    if not given or not expected: return False
    return hmac.compare_digest(str(given), str(expected))


def tag(token: str) -> str | None:
    """A session as the access log names it: eight hex characters of a hash, which tells two readers
    apart without writing down anything that could be presented back. None for no token."""
    import hashlib
    t = str(token or "").strip()
    return ("s:" + hashlib.sha256(t.encode()).hexdigest()[:8]) if t else None
