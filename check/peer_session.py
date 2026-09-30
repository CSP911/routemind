"""A session token for reading a backbone's export surface, for the checks.

The enrolment key in the environment opens `/v1/peers/token` and nothing else since 2026-09-29;
reads carry a six-hour session. Every check that reads a link is a client of that, so they share
this rather than each growing its own copy — and going through the real mint is the point, since a
check that presented the enrolment key directly would be testing a path no client uses.

Cached per (base, key) and re-minted on demand, exactly as the relay does it.
"""
import json, urllib.error, urllib.request

_HELD = {}


def session(base, key, timeout=20):
    """Mint or reuse a session token for `base` (e.g. "http://127.0.0.1:8100"), or return "" ."""
    if not key: return ""
    ident = (base.rstrip("/"), key)
    if ident in _HELD: return _HELD[ident]
    r = urllib.request.Request(base.rstrip("/") + "/v1/peers/token", data=b"", method="POST",
                               headers={"X-Peer-Token": key})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as x:
            tok = str(json.loads(x.read() or b"{}").get("token") or "")
    except urllib.error.HTTPError:
        # Handed back unchanged so the caller's own assertion sees the refusal it was testing for —
        # a check that probes with a wrong key must get its 401 from the surface, not from here.
        return key
    except Exception:
        return key
    if tok: _HELD[ident] = tok
    return tok or key


def forget(base=None, key=None):
    """Drop held tokens, so the next read mints again. All of them when called bare."""
    if base is None: _HELD.clear(); return
    _HELD.pop((base.rstrip("/"), key), None)
