#!/usr/bin/env python3
"""The six-hour session tokens, and what the enrolment key is for now.

    ROUTEMIND_TOKEN=... ./check/session-check.py [ontology-url]

The secret in `.env` used to ride on every read across every link — in every request, every proxy
log, every transcript — and it never expired. Two of them leaked into a working session while this
was being built, and both stayed valid. Since 2026-09-29 it opens one thing, `/v1/peers/token`, and
what the read path carries is a session good for six hours.

Most of what is asserted here is about what must **not** work, because the whole value of the change
is in those: an enrolment key that still read, or a session that could mint another, would leave the
old permanent secret exactly where it was while everything looked different.
"""
import json, os, sys, time, urllib.error, urllib.request

API = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ROUTEMIND_API", "http://127.0.0.1:8100")).rstrip("/")
KEY = os.environ.get("ROUTEMIND_TOKEN", "")
results = []


def check(name, cond, detail=""):
    results.append(("ok  " if cond else "FAIL") + " " + name)
    if not cond and detail: results.append("     " + detail)
    return cond


def call(path, token, method="GET", data=None):
    r = urllib.request.Request(API + path, data=data, method=method,
                               headers={"X-Peer-Token": token} if token else {})
    try:
        with urllib.request.urlopen(r, timeout=15) as x:
            return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read().decode("utf-8", "replace")[:150]}
    except Exception as e:
        print(f"FAIL cannot reach {API}: {type(e).__name__}", file=sys.stderr); sys.exit(1)


if not KEY:
    print("FAIL ROUTEMIND_TOKEN is not set — this check needs the enrolment key the backbone accepts",
          file=sys.stderr)
    sys.exit(1)

# ---- the enrolment key opens one thing --------------------------------------------------------
st, _ = call("/v1/export/regions", KEY)
check("the enrolment key no longer reads", st == 401, f"HTTP {st} — it is still a read credential")

st, doc = call("/v1/peers/token", KEY, "POST", b"")
if not check("it does mint a session", st == 200, f"HTTP {st} {json.dumps(doc)[:100]}"):
    print("\n".join(results)); sys.exit(1)
session = doc["token"]
check(f"  which lasts six hours ({doc.get('expires_in')}s)", doc.get("expires_in") == 6 * 3600,
      str(doc.get("expires_in")))
check("  and is not the enrolment key with a new name", session != KEY)

# ---- the session reads, and cannot become a key -----------------------------------------------
check("the session reads", call("/v1/export/regions", session)[0] == 200)
# The one that decides whether six hours means anything. A session that can mint another renews
# itself for ever, and a leaked one is then as permanent as the thing this replaced.
check("a session cannot mint another", call("/v1/peers/token", session, "POST", b"")[0] == 401)

# ---- nothing else gets in ----------------------------------------------------------------------
for name, tok in [("no token", ""), ("a wrong one", "not-a-token"),
                  ("the session with a character changed", session[:-1] + ("x" if session[-1] != "x" else "y"))]:
    check(f"{name} is refused", call("/v1/export/regions", tok)[0] == 401)

# A refusal has to say what to do about it, or the first person to meet it reads "401" and starts
# checking the key they are already holding correctly.
st, body = call("/v1/export/regions", "not-a-token")
check("  and the refusal says where a session comes from", "/v1/peers/token" in json.dumps(body),
      json.dumps(body)[:120])

# ---- a second session is a second session ------------------------------------------------------
st, doc2 = call("/v1/peers/token", KEY, "POST", b"")
check("minting twice gives two different tokens", doc2.get("token") not in (None, session))
check("  and both work", call("/v1/export/regions", session)[0] == 200
      and call("/v1/export/regions", doc2["token"])[0] == 200)

print("\n".join(results))
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
