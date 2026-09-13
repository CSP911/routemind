#!/usr/bin/env python3
"""The walk `check/install-check.sh` runs against the install it just made.

    ./check/install-walk.py <web-port> <web-b-port> <admin-port>

A separate file because it is a different question. The shell script asks whether a clean clone
installs; this asks whether the thing it installed does what the documents say — and it is the half
worth reading when something fails, so it does not live inside a heredoc.

It goes through the **web** API on the published ports and nothing else: the ontology API is not
published outside the compose network, so anything reachable only from in there is not a path a
person or an agent has. Two of the defects the first run of this found were on that boundary — a
scope the queue accepted and the proxy refused, and guidance the ontology wrote that the proxy
replaced with four words.
"""
import json
import sys
import time
import urllib.error
import urllib.request

WEB, WEB_B, ADMIN = (int(x) for x in sys.argv[1:4])
A = f"http://127.0.0.1:{WEB}/api/knowledge"
B = f"http://127.0.0.1:{WEB_B}/api/knowledge"
AD = f"http://127.0.0.1:{ADMIN}/api"
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def call(url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    if data is not None: r.add_header("Content-Type", "application/json")
    r.add_header("X-Knowledge-Actor", "install-check")
    try:
        with urllib.request.urlopen(r, timeout=120) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: return e.code, json.loads(raw or b"{}")
        except Exception: return e.code, {"error": raw.decode(errors="replace")[:200]}
    except Exception as e: return 0, {"error": type(e).__name__}


def hop0(base): return call(base + "/regions")[1]
def remote(base): return [(r.get("origin"), r.get("use_when")) for r in (hop0(base).get("regions") or [])
                          if r.get("peer")]


def queued(body, wait=2.0):
    """A routing decision, the only way a person can make one: submit, then accept. Both statuses are
    returned — an accept that could not be applied answered 200 once, which is how it went unnoticed."""
    st, p = call(B + "/proposals", "POST", body)
    if st not in (200, 201): return st, p
    st2, d = call(B + f"/proposals/{p['id']}/accept", "POST", {})
    time.sleep(wait)
    return st2, d


# ── the shipped shape ─────────────────────────────────────────────────────────
d = hop0(A)
own = [r for r in (d.get("regions") or []) if not r.get("peer")]
check("the worked example is on the map", len(own) == 5, json.dumps([r["source"] for r in own]))
check("  with an exchange up and reflecting nothing",
      [(l["name"], l["reachable"], l["areas"]) for l in d["links"]] == [("ix", True, 0)],
      json.dumps(d.get("links")))
# The one an install with a single backbone gets wrong most easily: being told about a link it has
# nothing across.
check("  and absence claimable, naming nobody",
      "may say something is absent" in (d.get("absence") or "")
      and "reaches through" not in (d.get("absence") or ""), (d.get("absence") or "")[:80])
check("  no link carries a note", all(not l.get("note") for l in d["links"]),
      json.dumps([l.get("note") for l in d["links"]]))
cfg = call(f"http://127.0.0.1:{WEB}/api/app-config")[1]
check("the running service says which door it has", cfg.get("auth") == "open", json.dumps(cfg)[:100])
check("  and that the name on a change is a signature", cfg.get("auth_names_the_actor") is False)

# ── the room ──────────────────────────────────────────────────────────────────
st, _ = call(AD + "/members", "POST",
             {"name": "branch", "label": "BRANCH", "url": "http://ontology-b:8100"})
check("the operator's screen registers the second backbone", st == 200, str(st))
time.sleep(3)
room = [(m["name"], m["kind"], m["reachable"]) for m in (call(AD + "/state")[1].get("members") or [])]
check("  and both are in the room, both answering",
      sorted(room) == [("branch", "backbone", True), ("home", "backbone", True)], json.dumps(room))

st, r = call(B + "/regions", "POST", {
    "source": "site-ops", "core_description": "Running the branch site day to day",
    "representative": {"name": "Site Operations", "id": "site-ops",
                       "one_liner": "Opening, closing, keys, and who to call when something breaks",
                       "use_when": "who opens the office · a key is lost · the lift is stuck"}})
check("the second backbone takes an area of its own", st == 200, json.dumps(r)[:110])

# ── the export decision, all three parts, through the queue ──────────────────
LINE = "who runs the branch site · keys, access, and the on-call for it"
FOR_HOME = "the branch site's own access and on-call, not the group's"

st, d = queued({"scope": "peer", "region": "site-ops", "after": LINE, "why": "head office asks"})
check("advertising it reaches the other backbone", st == 200 and remote(A) == [("branch", LINE)],
      f"{st} {json.dumps(remote(A))}")
check("  and the absence sentence starts naming the room",
      "reaches through" in (hop0(A).get("absence") or ""), (hop0(A).get("absence") or "")[:90])
row = next((r for r in hop0(A)["regions"] if r.get("peer")), None)
if check("  under an address of this backbone's own", row and str(row["fetch"]).startswith("/v1/peers/ix/"),
         json.dumps(row.get("fetch") if row else None)):
    # Followed exactly as printed, which is what every table tells an agent to do. A row that
    # arrives without its documents is a promise the link cannot keep.
    st, tbl = call(A + row["fetch"][len("/v1"):])
    check("  and what it points at is readable straight away", st == 200, f"{st} {json.dumps(tbl)[:90]}")
    check("    with its addresses moved onto this side", "/v1/export/" not in json.dumps(tbl))

st, _ = queued({"scope": "audience", "region": "site-ops", "after": "home", "why": "only head office"})
check("an audience naming the reader keeps it there", st == 200 and remote(A) == [("branch", LINE)],
      f"{st} {json.dumps(remote(A))}")
check("  and does not hand the reader the list", "export_to" not in json.dumps(hop0(A)))

st, _ = queued({"scope": "peer-line", "region": "site-ops", "peer": "home",
                "after": FOR_HOME, "why": "they have their own"})
# Immediately, not after a cache: the hint is what makes a narrower line narrow now rather than soon.
check("a line written for that reader is what it is shown, at once",
      st == 200 and remote(A) == [("branch", FOR_HOME)], f"{st} {json.dumps(remote(A))}")

st, e = queued({"scope": "audience", "region": "site-ops", "before": "home",
                "after": "someone-else", "why": "narrowing past the override"})
check("narrowing past the reader an override names is refused", st != 200, f"{st} {json.dumps(e)[:110]}")

st, d = queued({"scope": "peer", "region": "site-ops", "before": LINE, "after": "", "why": "stop"})
check("withdrawing it works", st == 200, f"{st} {json.dumps(d)[:150]}")
check("  and it goes from the other backbone's table", remote(A) == [], json.dumps(remote(A)))
reg = call(B + "/regions/site-ops")[1]
check("  taking the audience and the override with it",
      not reg.get("export_to") and not reg.get("use_when_export_for"),
      json.dumps({k: reg.get(k) for k in ("use_when_export", "export_to", "use_when_export_for")}))
d = hop0(A)
# Nothing here may read as an outage: a withdrawal is somebody's decision, and an outage is the one
# thing that stops a backbone claiming absence.
check("  with the link still up and unnoted",
      all(l["reachable"] and not l.get("note") for l in d["links"]), json.dumps(d.get("links")))
check("  and absence claimable again, naming nobody",
      "may say something is absent" in (d.get("absence") or "")
      and "reaches through" not in (d.get("absence") or ""), (d.get("absence") or "")[:80])

st, e = call(B + "/proposals", "POST", {"scope": "peer", "region": "site-ops", "after": ""})
check("an empty line against nothing is refused, and says how a withdrawal is filed",
      st == 422 and "before" in json.dumps(e), f"{st} {json.dumps(e)[:120]}")

print("\n".join(results))
print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
