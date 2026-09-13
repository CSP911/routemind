#!/usr/bin/env python3
"""What crosses a domain boundary, and who is recorded having read it.

    ./check/domain-check.py [port]

A **domain** is one exchange and the backbones around it. Two of them here — two rooms, a backbone in
each — because the questions only sharpen once the reader is not somebody you share an operator with.
Needs pyyaml.

Two things, and they are two halves of one decision: nothing crosses that was not allowed, and
somebody can say afterwards what did.

  * **Allow and deny by kind.** `vocab.yaml` says what a kind *is*; it now also says whether that
    sort of thing leaves. One decision per kind rather than one per entity — twelve, not
    seventy-nine — and a deny list rather than an allow list, because the area-level
    `use_when_export` is already the opt-in and making it a twelve-part act would mean the part
    everybody skips is the one that matters.
  * **A record at the owner.** A relayed document is held for one request and discarded, which is the
    point of a link rather than a merge — and it means nothing anywhere remembers unless the owner
    writes a line. With a physical copy there is at least an artefact; memory-only removes even that.
    The HTTP access line said `172.20.0.2 "GET /v1/export/nodes/x"`, and every read through an
    exchange comes from the same container, so they were all identically anonymous.

The failure worth naming: refusing the fetch and leaving the address in the listing. An address that
is printed and then refused reads as an outage, and following one is exactly what the tables tell an
agent to do. Listing and fetch have to agree, and they are asserted together.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8351
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# A run that stopped early used to print a summary that read exactly like a clean one. The results
# list holds what ran, `_end` is an atexit handler so it prints whatever crashed the script, and
# "0 failed of 29" is then true of the 29 that ran and silent about the 40 that did not. The exit
# code was 1, so nothing automated was fooled — but the line a person reads said the run passed, and
# that is the one place a check must not be wrong about itself. Appended to on the last line.
finished = []


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results:
        print("\n".join(results))
        n = sum(r.startswith("FAIL") for r in results)
        print(f"\n{n} failed of {len(results)}" if finished else
              f"\n{n} failed of the {len(results)} that ran — but THE RUN STOPPED EARLY and the rest "
              f"never ran, so this is not a pass. What stopped it is printed above these results.")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="domain-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402
from service import access                                               # noqa: E402


def _need_areas(names, n, what):
    if len(names) >= n: return names
    print(f"this check needs a seed with at least {n} area{'s' if n > 1 else ''} to share between "
          f"backbones, and {what} has {len(names)}.\nRun it on the host, where examples/back-office "
          f"is — the ontology image ships an empty seed on purpose.")
    raise SystemExit(2)


areas = sorted(d for d in os.listdir(os.path.join(seed, "regions"))
               if os.path.isdir(os.path.join(seed, "regions", d)))
_need_areas(areas, 2, "the seed")

# Two domains: one backbone in each room, the rooms peering. HOME reads across both.
BB = {"home": BASE, "far": BASE + 1}
IX = {"ix1": BASE + 10, "ix2": BASE + 11}
AT = {"home": "ix1", "far": "ix2"}
SHARE = {"home": areas[0], "far": areas[1]}
TOK = {"TOK_HOME": "t-home", "TOK_FAR": "t-far", "TOK_IX": "t-ix1-ix2"}
ACCESS = {n: os.path.join(T, f"access-{n}") for n in BB}
repos = {}
DENIED_KIND = None
DENIED_ID = None
KEPT_ID = None

for n in BB:
    repo = os.path.join(T, n); shutil.copytree(seed, repo); repos[n] = repo
    for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
        q = os.path.join(repo, "regions", SHARE[n], f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" in t and "\nparent:" not in t:
            open(q, "w", encoding="utf-8").write(t.replace(
                "\nrole: representative\n", f"\nrole: representative\nuse_when_export: what {n} answers\n", 1))
            break
    if n == "far":
        # A sentence that exists in this domain and nowhere else, so "the reader kept no copy" can be
        # looked for rather than assumed. Both backbones are seeded from the same example, and a
        # needle that is in both proves nothing.
        for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
            q = os.path.join(repo, "regions", SHARE[n], f)
            t = open(q, encoding="utf-8").read()
            if "\nrole: representative\n" in t: continue
            open(q, "w", encoding="utf-8").write(t.replace(
                'one_liner: "', 'one_liner: "ONLY-IN-THE-FAR-DOMAIN-8351 · ', 1))
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: {AT[n]}\n    label: {AT[n].upper()}\n"
        f"    url: http://127.0.0.1:{IX[AT[n]]}\n    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)

# A kind to deny, chosen from the table a peer is actually handed rather than from the files on
# disk: an area's table lists the representative's own children, and picking a grandchild would test
# the policy against a row nobody was ever offered.


def deny_kind(who, kind=None):
    """`export: no` on a kind, in that backbone's own vocabulary — committed, like every other thing
    this backbone is."""
    v = os.path.join(repos[who], "vocab.yaml")
    lines = [l for l in open(v, encoding="utf-8").read().splitlines(True)]
    out, hit = [], False
    for l in lines:
        if l.startswith("  export: "): continue             # take any previous answer out first
        out.append(l)
        # A kinds entry is `- id: x` at column 0 with `  desc:` under it, so the flag sits at two
        # spaces beside desc. Four put it inside the description and the policy did nothing.
        if kind and l.strip() == f"- id: {kind}": hit = True
        elif hit and l.startswith("  desc:"):
            out.append("  export: no\n"); hit = False
    open(v, "w", encoding="utf-8").write("".join(out))
    subprocess.run(["git", "-C", repos[who], "add", "-A"], check=True)
    subprocess.run(["git", "-C", repos[who], "-c", "user.name=x", "-c", "user.email=x@l",
                    "commit", "-q", "--allow-empty", "-m", f"export policy {kind}"], check=True)


for n, port in BB.items():
    e = {**os.environ, **TOK, "ONTOLOGY_DATA": repos[n], "PORT": str(port),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"), "ONTOLOGY_ACCESS": ACCESS[n],
         "ONTOLOGY_PEER_TOKEN": TOK[f"TOK_{n.upper()}"], "ONTOLOGY_PEER_TTL": "0"}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

ROOMS = {
    "ix1": [("home", BB["home"], "TOK_HOME", "backbone"), ("ix2", IX["ix2"], "TOK_IX", "exchange")],
    "ix2": [("far", BB["far"], "TOK_FAR", "backbone"), ("ix1", IX["ix1"], "TOK_IX", "exchange")],
}
for name, members in ROOMS.items():
    f = os.path.join(T, f"members-{name}.yaml")
    open(f, "w", encoding="utf-8").write("members:\n" + "".join(
        f"  - name: {m}\n    label: {m.upper()}\n    url: http://127.0.0.1:{p}\n"
        f"    kind: {k}\n    token_env: {tv}\n" for m, p, tv, k in members))
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                                  env={**os.environ, **TOK, "EXCHANGE_NAME": name, "PORT": str(IX[name]),
                                       "EXCHANGE_MEMBERS": f, "ONTOLOGY_PEER_TTL": "0"},
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

for port in [*BB.values(), *IX.values()]:
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def get(port, path, raw=False):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=25) as x:
            b = x.read()
            return x.status, (b.decode("utf-8", "replace") if raw else json.loads(b or b"{}"))
    except urllib.error.HTTPError as e: return e.code, {}
    except Exception as e: return 0, {"raw": type(e).__name__}


def far_area_at_home():
    row = next((r for r in (get(BB["home"], "/v1/regions")[1].get("regions") or []) if r.get("peer")), None)
    return row


# The far area's table, read at its owner, is what says which kinds are on offer.
st, own_tbl = get(BB["far"], f"/v1/regions/{SHARE['far']}")
by_kind = {}
for e in (own_tbl.get("entries") or []):
    by_kind.setdefault(str(e.get("kind") or ""), []).append(e["id"])
check("the far area offers more than one kind of thing", len(by_kind) > 1, json.dumps(
    {k: v for k, v in by_kind.items()}))
# Not the kind the area's **face** is: denying that stops the whole area crossing, which is right and
# is a different assertion, made below on its own.
FACE_KIND = str((get(BB["far"], f"/v1/nodes/{own_tbl['representative']}")[1] or {}).get("kind") or "")
pickable = {k: v for k, v in by_kind.items() if k != FACE_KIND}
check("  and more than one that is not the kind its face is", len(pickable) > 1,
      json.dumps({"face": FACE_KIND, "rest": sorted(pickable)}))
DENIED_KIND = sorted(pickable, key=lambda k: (-len(pickable[k]), k))[0]
DENIED_ID = pickable[DENIED_KIND][0]
KEPT_ID = next(i for k, v in sorted(pickable.items()) if k != DENIED_KIND for i in v)

row = far_area_at_home()
check("a domain away, the other one's area is on the table", bool(row),
      json.dumps([r.get("origin") for r in (get(BB["home"], "/v1/regions")[1].get("regions") or [])]))
if not row: raise SystemExit(1)
TBL = row["fetch"]
st, tbl = get(BB["home"], TBL)
before = [e.get("id") for e in (tbl.get("entries") or [])]
check("  and its entries with it", DENIED_ID in before and KEPT_ID in before, json.dumps(before))
check("  each of them readable", get(BB["home"], TBL.rsplit("/regions/", 1)[0] + f"/nodes/{DENIED_ID}")[0] == 200)

# ── the policy ────────────────────────────────────────────────────────────────
deny_kind("far", DENIED_KIND)
time.sleep(0.5)
st, tbl = get(BB["home"], TBL)
after = [e.get("id") for e in (tbl.get("entries") or [])]
check(f"with `export: no` on kind `{DENIED_KIND}`, it is out of the table a domain away",
      DENIED_ID not in after, json.dumps(after))
check("  and the kinds that still cross are still there", KEPT_ID in after, json.dumps(after))
NODES = TBL.rsplit("/regions/", 1)[0] + "/nodes/"
st_denied, _ = get(BB["home"], NODES + DENIED_ID)
check("  and the address a reader already had stops working", st_denied == 404, str(st_denied))
st_none, _ = get(BB["home"], NODES + "no-such-entity-anywhere")
check("    with the same answer as something that was never there", st_denied == st_none,
      f"{st_denied} vs {st_none}")
check("  while the ones that cross still read", get(BB["home"], NODES + KEPT_ID)[0] == 200)
# The owner keeps everything. A policy about what leaves is not a policy about what it holds.
check("  and the owner still reads it at home", get(BB["far"], f"/v1/nodes/{DENIED_ID}")[0] == 200)

# The area's own face. Denying that kind is denying the area: every row of its table is under the
# representative, so offering it would offer a table nothing in which can be read.
deny_kind("far", FACE_KIND)
time.sleep(0.5)
check(f"denying the kind an area's face is (`{FACE_KIND}`) stops the whole area crossing",
      far_area_at_home() is None, json.dumps(far_area_at_home()))
check("  rather than offering a table with nothing readable in it",
      get(BB["home"], TBL)[0] in (404, 502), str(get(BB["home"], TBL)[0]))
check("  while the owner still has all of it", get(BB["far"], f"/v1/regions/{SHARE['far']}")[0] == 200)

deny_kind("far", None)
time.sleep(0.5)
check("taking the policy away lets it cross again",
      DENIED_ID in [e.get("id") for e in (get(BB["home"], TBL)[1].get("entries") or [])])
check("  and its address works again", get(BB["home"], NODES + DENIED_ID)[0] == 200)

# ── the record ────────────────────────────────────────────────────────────────
rows = access.read(ACCESS["far"])
check("every read across the boundary is recorded at the owner", len(rows) > 0, str(len(rows)))
served = [r for r in rows if r["outcome"] == "served"]
refused = [r for r in rows if r["outcome"] == "refused"]
check("  served reads among them", len(served) > 0, str(len(served)))
# The one that matters: somebody following an address they should not have.
check("  and the refusals, which are the ones worth having", len(refused) > 0, str(len(refused)))
check("    naming what was asked for",
      any(DENIED_ID in r["path"] for r in refused), json.dumps([r["path"] for r in refused][-3:]))
# Two names, two questions: which link carried it, and who was at the far end.
check("  with the link it came in on", all(r["peer"] == "ix2" for r in rows),
      json.dumps(sorted({r["peer"] for r in rows})))
# Two readers, and both are right. `ix1` is a member of the room FAR meets in, reading through it;
# `ix2` is that room itself, reading FAR's advertisement so it can filter for its members. The
# record has to tell those apart, because only the first is somebody else's traffic.
check("  and who it was for", {r["reader"] for r in rows} <= {"ix1", "ix2"},
      json.dumps(sorted({r["reader"] for r in rows})))
check("    including the room reading for itself, which is not the same act",
      "ix2" in {r["reader"] for r in rows} and "ix1" in {r["reader"] for r in rows},
      json.dumps(sorted({r["reader"] for r in rows})))
check("  each one stamped and sized",
      all(r.get("at") and isinstance(r.get("size"), int) for r in rows), json.dumps(rows[:1]))
# A domain two rooms out is not in the record, and that is what no-transit means rather than a gap.
check("  and the backbone two rooms away is not named — it has no relationship here",
      not any(r["reader"] == "home" for r in rows), json.dumps(sorted({r["reader"] for r in rows})))

# A wrong token is a read too, and the only signal there is that a link is being probed.
r = urllib.request.Request(f"http://127.0.0.1:{BB['far']}/v1/export/regions")
r.add_header("X-Peer-Token", "not-the-secret")
try: urllib.request.urlopen(r, timeout=15)
except Exception: pass
time.sleep(0.3)
rows = access.read(ACCESS["far"])
bad = [x for x in rows if x["outcome"] == "refused" and x.get("peer") == "?"]
check("a wrong token is recorded, before the door", len(bad) > 0, json.dumps(rows[-1:]))
check("  as a refusal with a reason", bad and "token" in (bad[-1].get("reason") or ""),
      json.dumps(bad[-1] if bad else None))

# ── and nothing of it is kept ─────────────────────────────────────────────────
# The record is the only account there is, and this is why: read a document across the boundary, then
# look for any trace of it on the reader's disk. Memory only is what the relay has always done; it is
# asserted here because it is now load-bearing for accountability rather than only for tidiness.
MARK = "ONLY-IN-THE-FAR-DOMAIN-8351"
marked = next((e["id"] for e in (own_tbl.get("entries") or []) if MARK in json.dumps(e)), None)
st, doc = get(BB["home"], NODES + (marked or KEPT_ID))
needle = MARK
check("a document only the far domain has is readable across the boundary",
      st == 200 and MARK in json.dumps(doc), f"{st} {json.dumps(doc)[:110]}")
found = []
for base, _dirs, files in os.walk(repos["home"]):
    if ".git" in base: continue
    for f in files:
        try: t = open(os.path.join(base, f), encoding="utf-8", errors="ignore").read()
        except Exception: continue
        if needle and needle in t: found.append(os.path.relpath(os.path.join(base, f), repos["home"]))
check("  and the reader keeps no copy of it, anywhere", not found, json.dumps(found[:3]))
for base, _dirs, files in os.walk(os.path.join(T, "pub-home")):
    for f in files:
        try: t = open(os.path.join(base, f), encoding="utf-8", errors="ignore").read()
        except Exception: continue
        if needle and needle in t: found.append(f)
check("    nor in what it publishes", not found, json.dumps(found[:3]))
# Its own record is about what **it** served, never about what it read. Two domains, two accounts,
# and neither is the other's.
here = access.read(ACCESS["home"])
check("  and its own record is of what it served, not of what it read",
      all(x["path"].startswith("/v1/export") for x in here) and
      not any(DENIED_ID in x["path"] or KEPT_ID in x["path"] for x in here),
      json.dumps(here[-2:]))

shutil.rmtree(T, ignore_errors=True)
finished.append(True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
