#!/usr/bin/env python3
"""Where the new configuration meets the old — docs/SCENARIOS.md, section P.

    ./check/cross-check.py [port]

Two backbones and an exchange on throwaway repositories, with the features that were built before
links existed switched on beside them: drafts, a hand-edited tree, overlays, deletion, an id at the
length limit. Needs pyyaml.

Everything else about peering was written by asking "does a link work". These ask the question that
only appears once a link is there at all: **which of the promises this ontology already makes are
still true when the reader is another backbone?** Each of these was a settled answer for a local
reader and a different question for a remote one, and three of them were wrong:

  * A **draft** is hidden from a listing and answers by address, which is right for the owner and was
    the whole of the access control across a link.
  * An **overlay** refused a peer address by telling the person they had assembled it — when hop 0
    had printed it and the tables say to follow one exactly as printed.
  * A malformed overlay **member** came back `500 internal error`, naming neither the mistake nor
    the fix. (Found by making it, while writing this.)

The two that were already right are here because nothing said so: a hand-edited tree must not take a
link down, and an audience must never look like an outage.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8331
A_PORT, B_PORT, IX_PORT = BASE, BASE + 1, BASE + 10
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results:
        print("\n".join(results))
        print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="cross-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

TOK = {"TOK_AY": "t-ay", "TOK_BEE": "t-bee"}
def _need_areas(names, n, what):
    """These checks share areas between backbones, so they need a seed with at least `n` of them.

    The ontology image ships `seed/` with no areas and no `examples/`, which is right — an install
    starts empty — and means running this inside a container ends in `IndexError: list index out of
    range` from the slice below. A refusal that names neither the mistake nor the fix is the thing
    this repository keeps finding in its own code; it should not be in the checks that find it.
    """
    if len(names) >= n: return names
    print(f"this check needs a seed with at least {n} area{'s' if n > 1 else ''} to share between "
          f"backbones, and {what} "
          f"has {len(names)}.\nRun it on the host, where examples/back-office is — the ontology image "
          f"ships an empty seed on purpose.")
    raise SystemExit(2)

areas = sorted(d for d in os.listdir(os.path.join(seed, "regions"))
               if os.path.isdir(os.path.join(seed, "regions", d)))
_need_areas(areas, 2, "the seed")
SHARE = {"ay": areas[0], "bee": areas[1]}
PORT = {"ay": A_PORT, "bee": B_PORT}
repos = {}
DRAFT = None

for n in ("ay", "bee"):
    repo = os.path.join(T, n); shutil.copytree(seed, repo); repos[n] = repo
    for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
        q = os.path.join(repo, "regions", SHARE[n], f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" in t and "\nparent:" not in t:
            open(q, "w", encoding="utf-8").write(t.replace(
                "\nrole: representative\n", f"\nrole: representative\nuse_when_export: what {n} answers\n", 1))
            break
    if n == "bee":
        # The seed declares no area that takes drafts, so this copy declares one. `area_rules` is
        # where that lives — a role an area is given in its own vocabulary, never a name in code.
        v = os.path.join(repo, "vocab.yaml")
        open(v, "a", encoding="utf-8").write(
            f"\narea_rules:\n  {SHARE['bee']}:\n    drafts: true\n")
        # One entity in the shared area, unfinished. Locally that means "hidden from the table"; the
        # question is what it means to somebody on the other side of a link.
        for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
            q = os.path.join(repo, "regions", SHARE[n], f)
            t = open(q, encoding="utf-8").read()
            if "\nrole: representative\n" in t: continue
            DRAFT = next(l.split(":", 1)[1].strip() for l in t.splitlines() if l.startswith("id:"))
            lines = t.splitlines(True)
            lines.insert(next(i for i, l in enumerate(lines) if l.startswith("kind:")) + 1, "status: draft\n")
            open(q, "w", encoding="utf-8").write("".join(lines))
            break
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: ix\n    label: EXCHANGE\n    url: http://127.0.0.1:{IX_PORT}\n"
        f"    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)
    e = {**os.environ, **TOK, "ONTOLOGY_DATA": repo, "PORT": str(PORT[n]),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"), "ONTOLOGY_OVERLAYS": os.path.join(T, f"ov-{n}"),
         "ONTOLOGY_PEER_TOKEN": TOK[f"TOK_{n.upper()}"], "ONTOLOGY_PEER_TTL": "0"}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

MEMBERS = os.path.join(T, "members.yaml")
open(MEMBERS, "w", encoding="utf-8").write("members:\n" + "".join(
    f"  - name: {n}\n    label: {n.upper()}\n    url: http://127.0.0.1:{PORT[n]}\n"
    f"    token_env: TOK_{n.upper()}\n" for n in ("ay", "bee")))
IX_ENV = {**os.environ, **TOK, "EXCHANGE_NAME": "ix", "PORT": str(IX_PORT),
          "EXCHANGE_MEMBERS": MEMBERS, "ONTOLOGY_PEER_TTL": "0"}


def start_ix():
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                         env=IX_ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{IX_PORT}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    return p


ix = start_ix()
for port in (A_PORT, B_PORT):
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def call(port, path, method="GET", body=None, token=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method)
    if data is not None: r.add_header("Content-Type", "application/json")
    if token: r.add_header("X-Peer-Token", token)
    r.add_header("X-Actor", "cross-check")
    try:
        with urllib.request.urlopen(r, timeout=30) as x:
            b = x.read()
            return x.status, (b.decode("utf-8", "replace") if raw else json.loads(b or b"{}"))
    except urllib.error.HTTPError as e:
        b = e.read()
        if raw: return e.code, b.decode(errors="replace")
        try: return e.code, json.loads(b or b"{}")
        except Exception: return e.code, {"error": b.decode(errors="replace")[:200]}
    except Exception as e: return 0, {"error": type(e).__name__}


def hop0(who): return call(PORT[who], "/v1/regions")[1]
def peer_rows(who): return [r for r in (hop0(who).get("regions") or []) if r.get("peer")]


addr = next((r["fetch"] for r in peer_rows("ay")), None)
check("the room is up and ay can see bee", bool(addr), json.dumps([r.get("origin") for r in peer_rows("ay")]))

# ── P1 a draft, across a link ────────────────────────────────────────────────
# Locally this is settled and stays settled: hidden from the table, served by address, because the
# reader is the owner and "draft" means unfinished rather than secret. Across a link the listing is
# the *only* access control there is, so the same answer is a hole — anybody who kept yesterday's
# address keeps reading a thing that has been taken off the table.
st, local = call(B_PORT, f"/v1/regions/{SHARE['bee']}")
check("P1 a draft is not in its area's table", DRAFT not in json.dumps(local), str(DRAFT))
check("   and locally it still answers by address", call(B_PORT, f"/v1/nodes/{DRAFT}")[0] == 200)
st, across = call(B_PORT, f"/v1/export/regions/{SHARE['bee']}", token=TOK["TOK_BEE"])
check("   and it is not in the table a peer is given", DRAFT not in json.dumps(across), str(st))
st, _ = call(B_PORT, f"/v1/export/nodes/{DRAFT}", token=TOK["TOK_BEE"])
check("   and a peer following its address gets nothing", st == 404, str(st))
st, _ = call(A_PORT, f"/v1/peers/ix/peers/bee/nodes/{DRAFT}")
check("   the same across the room, as bee saying no", st == 404, str(st))
# Indistinguishable from a node that was never there, on purpose.
st2, _ = call(B_PORT, "/v1/export/nodes/no-such-entity-at-all", token=TOK["TOK_BEE"])
check("   and it is the same answer as a node that does not exist", st2 == 404, str(st2))

# ── P2 a hand-edited tree, and a peer reading ────────────────────────────────
# Writes are refused there and that is deliberate. Nothing said what it does to a link, and the
# tempting-but-wrong answer is "stop serving until somebody tidies up": a peer would see an outage,
# stop claiming absence, and none of it would be true.
open(os.path.join(repos["bee"], "SOMEBODY-EDITED-THIS.md"), "w", encoding="utf-8").write("by hand\n")
time.sleep(0.3)
check("P2 a hand-edited tree is not writable", call(B_PORT, "/healthz")[1].get("writable") is False)
st, _ = call(B_PORT, "/v1/nodes", "POST",
             {"name": "X", "kind": "rule", "region": SHARE["bee"], "one_liner": "y"})
check("   and a write says so", st == 409, str(st))
st, adv = call(B_PORT, "/v1/export/regions", token=TOK["TOK_BEE"])
check("   while a peer still reads the advertisement", st == 200 and len(adv.get("regions") or []) == 1, str(st))
check("   and the row is still on the other backbone's table", len(peer_rows("ay")) == 1)
check("   and the link reads as up, because it is",
      all(l["reachable"] for l in (hop0("ay").get("links") or [])))
check("   and absence may still be claimed", "may say something is absent" in (hop0("ay").get("absence") or ""))
os.remove(os.path.join(repos["bee"], "SOMEBODY-EDITED-THIS.md"))

# ── P3 an overlay, and an address across a link ──────────────────────────────
# The refusal is right — an overlay narrows this backbone's own tree — and its *reason* was not. It
# said the address had been assembled, when hop 0 had printed it and every table says to follow one
# exactly as printed. A refusal that blames the reader for doing the documented thing is worse than
# no refusal, because the person goes looking for a mistake they did not make.
st, r = call(A_PORT, "/v1/overlays", "POST",
             {"question": "who pays for a trip", "by": {"kind": "person", "name": "p"},
              "members": [{"address": addr, "why": "the other office holds it"}]})
check("P3 an overlay refuses an address across a link", st == 422, str(st))
check("   and says what an overlay is, not that the address was made up",
      "across a link" in json.dumps(r) and "assembling" not in json.dumps(r), json.dumps(r)[:190])
st, ok = call(A_PORT, "/v1/overlays", "POST",
              {"question": "who pays for a trip", "by": {"kind": "person", "name": "p"},
               "members": [{"address": f"/v1/regions/{SHARE['ay']}", "why": "mine"}]})
check("   while a local area is taken", st == 201, json.dumps(ok)[:120])
check("   and an overlay is not on the export surface at all",
      call(B_PORT, "/v1/export/overlays", token=TOK["TOK_BEE"])[0] == 404)
# Found while writing this: a member that is not an object was `500 internal error`, which names
# neither the mistake nor the fix — the exact class of bug scenario I was written for.
st, r = call(A_PORT, "/v1/overlays", "POST",
             {"question": "q", "by": {"kind": "person", "name": "p"}, "members": [f"/v1/regions/{SHARE['ay']}"]})
check("   and a member that is not an object is refused with a reason", st == 400, str(st))
check("     naming what one is", "address" in json.dumps(r) and "why" in json.dumps(r), json.dumps(r)[:150])

# ── P4 an audience, while the link is down ───────────────────────────────────
# Two reasons a row is missing, and only one of them is an outage. If "you are not on the list" ever
# reads as "I could not see", a backbone stops claiming absence over a link that is working perfectly
# — and every answer downstream gets weaker than the data supports.
def set_audience(who, names):
    repo, area = repos[who], SHARE[who]
    for f in sorted(os.listdir(os.path.join(repo, "regions", area))):
        q = os.path.join(repo, "regions", area, f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in t or "\nparent:" in t: continue
        out = [l for l in t.splitlines(True) if not l.startswith("export_to:")]
        if names:
            i = next(j for j, l in enumerate(out) if l.startswith("use_when_export:"))
            out.insert(i + 1, "export_to: [" + ", ".join(names) + "]\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(repo))
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=x", "-c", "user.email=x@l",
                    "commit", "-q", "--allow-empty", "-m", "audience"], check=True)


set_audience("bee", ["nobody-here"])
time.sleep(0.4)
d = hop0("ay")
check("P4 left off the list, the row goes", len(peer_rows("ay")) == 0)
check("   and absence may still be claimed — it is a policy, not an outage",
      "may say something is absent" in (d.get("absence") or "")
      and "incomplete" not in (d.get("absence") or "").lower(), (d.get("absence") or "")[:80])
ix.terminate(); time.sleep(1.0)
d = hop0("ay")
check("   and when the link then drops, the outage is what is reported",
      "incomplete" in (d.get("absence") or "").lower(), (d.get("absence") or "")[:80])
check("     with absence no longer claimable", "may say something is absent" not in (d.get("absence") or ""))
ix = start_ix(); time.sleep(1.0)
check("   and when it comes back, the policy is what remains", len(peer_rows("ay")) == 0
      and "may say something is absent" in (hop0("ay").get("absence") or ""),
      (hop0("ay").get("absence") or "")[:80])
set_audience("bee", [])
time.sleep(0.4)
check("   until the list is taken away", len(peer_rows("ay")) == 1)

# ── P5 a name at the length limit, three prefixes deep ───────────────────────
# 252 characters is the longest id there is: `.md` makes it exactly 255. An address across a room is
# that plus three prefixes, and nothing between here and there may shorten it.
LONG = "a" + "x" * 251
st, r = call(B_PORT, "/v1/regions", "POST",
             {"source": "long-one", "core_description": "an area with the longest name there is",
              "representative": {"name": "L" * 40, "one_liner": "the longest id there is",
                                 "use_when": "when the id is as long as it can be",
                                 "use_when_export": "the longest id there is, across a link",
                                 "id": LONG}})
if check("P5 an area whose representative has a 252-character id is created", st in (200, 201), json.dumps(r)[:140]):
    time.sleep(0.5)
    row = next((x for x in peer_rows("ay") if "long-one" in str(x.get("fetch"))), None)
    check("   and it crosses the room whole",
          bool(row) and row["fetch"] == "/v1/peers/ix/peers/bee/regions/long-one",
          json.dumps(row.get("fetch") if row else [x.get("fetch") for x in peer_rows("ay")]))
    if row:
        st, tbl = call(A_PORT, row["fetch"])
        check("   and its table reads back", st == 200, json.dumps(tbl)[:120])
        check("     with the id intact, not truncated", LONG in json.dumps(tbl),
              json.dumps(tbl)[:150])

# ── P6 deleting an exported area ─────────────────────────────────────────────
# Withdrawing is checked elsewhere. Deleting is the other way an area stops crossing, and the rule
# that guards it was written before links existed: an area with anything in it is refused.
st, r = call(B_PORT, f"/v1/regions/{SHARE['bee']}", "DELETE")
check("P6 an exported area with entities in it is refused", st == 409, str(st))
check("   and says what is still in it", "nodes remain" in json.dumps(r), json.dumps(r)[:120])
check("   and it is still crossing, untouched by the attempt", len(peer_rows("ay")) >= 1)
st, r = call(B_PORT, "/v1/regions/long-one", "DELETE")
if check("   while an area holding only its representative goes", st == 200, json.dumps(r)[:140]):
    time.sleep(0.5)
    check("   and the row goes with it", not any("long-one" in str(x.get("fetch")) for x in peer_rows("ay")),
          json.dumps([x.get("fetch") for x in peer_rows("ay")]))
    check("     and so does the address", call(A_PORT, "/v1/peers/ix/peers/bee/regions/long-one")[0] == 404)
    check("     as bee saying no, not a link that failed",
          all(l["reachable"] for l in (hop0("ay").get("links") or [])))

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
