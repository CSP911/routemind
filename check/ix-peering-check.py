#!/usr/bin/env python3
"""Two rooms that meet, and the third they do not carry for.

    ./check/ix-peering-check.py [port]

Three exchanges in a line — IX1 — IX2 — IX3 — each with one backbone of its own, on throwaway
repositories. Needs pyyaml on this python.

`exchange-check.py` covers backbones meeting at one exchange. This covers exchanges meeting each
other, which is the same contract used a second time — an exchange reads a neighbouring exchange with
exactly the member code it uses on a backbone — and two rules that only exist once there are two
rooms:

  * **Who may enrol whom.** The same two halves as everywhere else, with both of them now held by
    operators: each exchange names the other in its own `members.yaml`, one secret used in both
    directions, and neither room joins the other on its own say-so.
  * **No transit.** An exchange offers a neighbour its own backbones and never what a third exchange
    told it. HOME sees REMOTE and must not see FAR — not because FAR is secret, but because nobody at
    either end agreed to a relationship with the other, and the operator in the middle would be
    answering for two rooms that never met. It is also what bounds every path at one exchange-to-
    exchange hop, so a ring of exchanges cannot loop rather than merely being unlikely to.

The failure this is really watching for is the quiet one: transit that works. A row that arrives from
two exchanges away looks exactly like a row that arrived from one, and nothing at the reader can tell
the difference — so if the filter is wrong, everything keeps working and the boundary is simply gone.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8211
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

T = tempfile.mkdtemp(prefix="ix-peering-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

# One backbone per room, each sharing a different area, so a row anywhere names the room it came from.
BB = ["home", "remote", "far"]
IX = ["ix1", "ix2", "ix3"]
AT = {"home": "ix1", "remote": "ix2", "far": "ix3"}
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
               if os.path.isdir(os.path.join(seed, "regions", d)))[:3]
SHARE = dict(zip(BB, areas))
_need_areas(areas, 3, "the seed")
LINE = {n: f"what {n} answers for the others · questions that belong to {n}" for n in BB}
BB_PORT = {n: BASE + i for i, n in enumerate(BB)}
IX_PORT = {n: BASE + 10 + i for i, n in enumerate(IX)}

# One secret per link, used in both directions — the rule everywhere else, applied to a link whose
# two ends are both exchanges.
ADMIN = "operator-key"
TOK = {**{f"TOK_{n.upper()}": f"tok-{n}" for n in BB},
       "TOK_IX1_IX2": "tok-ix1-ix2", "TOK_IX2_IX3": "tok-ix2-ix3"}

for n in BB:
    repo = os.path.join(T, n); shutil.copytree(seed, repo)
    for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
        q = os.path.join(repo, "regions", SHARE[n], f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" in text and "\nparent:" not in text:
            open(q, "w", encoding="utf-8").write(
                text.replace("\nrole: representative\n",
                             f"\nrole: representative\nuse_when_export: {LINE[n]}\n", 1))
            break
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: {AT[n]}\n    label: {AT[n].upper()}\n"
        f"    url: http://127.0.0.1:{IX_PORT[AT[n]]}\n    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)
    e = {**os.environ, **TOK, "ONTOLOGY_DATA": repo, "PORT": str(BB_PORT[n]),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"),
         "ONTOLOGY_PEER_TOKEN": TOK[f"TOK_{n.upper()}"], "ONTOLOGY_PEER_TTL": "0"}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))


def member(name, label, port, token_env, kind="backbone"):
    return (f"  - name: {name}\n    label: {label}\n    url: http://127.0.0.1:{port}\n"
            f"    kind: {kind}\n    token_env: {token_env}\n")


# Both halves of every declaration, written out one room at a time. IX1 names IX2 and IX2 names IX1;
# neither entry alone is a link.
ROOMS = {
    "ix1": member("home", "HOME", BB_PORT["home"], "TOK_HOME")
         + member("ix2", "IX2", IX_PORT["ix2"], "TOK_IX1_IX2", "exchange"),
    "ix2": member("remote", "REMOTE", BB_PORT["remote"], "TOK_REMOTE")
         + member("ix1", "IX1", IX_PORT["ix1"], "TOK_IX1_IX2", "exchange")
         + member("ix3", "IX3", IX_PORT["ix3"], "TOK_IX2_IX3", "exchange"),
    "ix3": member("far", "FAR", BB_PORT["far"], "TOK_FAR")
         + member("ix2", "IX2", IX_PORT["ix2"], "TOK_IX2_IX3", "exchange"),
}
for n, body in ROOMS.items():
    f = os.path.join(T, f"members-{n}.yaml")
    open(f, "w", encoding="utf-8").write("members:\n" + body)
    e = {**os.environ, **TOK, "EXCHANGE_NAME": n, "PORT": str(IX_PORT[n]),
         "EXCHANGE_MEMBERS": f, "ONTOLOGY_PEER_TTL": "0", "EXCHANGE_ADMIN_TOKEN": ADMIN}
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

for port in [*BB_PORT.values(), *IX_PORT.values()]:
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def get(port, path, token=None, raw=False, kind=None):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
    if token: r.add_header("X-Peer-Token", token)
    if kind: r.add_header("X-Peer-Kind", kind)
    try:
        with urllib.request.urlopen(r, timeout=20) as x:
            b = x.read()
            return x.status, (b.decode("utf-8", "replace") if raw else json.loads(b or b"{}"))
    except urllib.error.HTTPError as e:
        b = e.read()
        if raw: return e.code, b.decode(errors="replace")
        try: return e.code, json.loads(b or b"{}")
        except Exception: return e.code, {"raw": b.decode(errors="replace")[:160]}
    except Exception as e: return 0, {"raw": type(e).__name__}


def origins(port, token, kind=None):
    st, d = get(port, "/v1/export/regions", token, kind=kind)
    return st, sorted({r.get("origin") for r in (d.get("regions") or [])}), d


# ── an exchange reads an exchange with the member contract, unchanged ─────────
st, seen, _ = origins(IX_PORT["ix1"], TOK["TOK_IX1_IX2"])
check("an exchange is let into another exchange by its member token", st == 200, str(st))
check("  and a wrong token is not", get(IX_PORT["ix1"], "/v1/export/regions", "nope")[0] == 401)
check("  nor a token that belongs on a different link",
      get(IX_PORT["ix1"], "/v1/export/regions", TOK["TOK_IX2_IX3"])[0] == 401)

# The first way two rooms break each other is not a wrong row, it is no row at all: IX1 asks IX2 what
# it is advertising, IX2 asks IX1 to find out, and neither ever answers. It ends in a timeout, so it
# reads as an outage on a link that is perfectly healthy.
t0 = time.monotonic()
st, _, _ = origins(IX_PORT["ix1"], TOK["TOK_IX1_IX2"])
dt = time.monotonic() - t0
check("a room answers a room without asking it back", st == 200 and dt < 2.0, f"{st} after {dt:.1f}s")

# ── one hop across: HOME sees REMOTE ─────────────────────────────────────────
st, seen, adv = origins(IX_PORT["ix1"], TOK["TOK_HOME"])
check("home's room offers it the backbone in the next room", seen == ["remote"], json.dumps(seen))
row = next((r for r in adv["regions"] if r["origin"] == "remote"), None)
check("  by the trail it travelled, nearest last", row and row["path"] == ["ix2", "remote"],
      json.dumps(row.get("path") if row else None))
check("  carrying the line remote wrote for a peer", row and row["use_when"] == LINE["remote"])
check("  and its address chains both rooms",
      row and str(row["fetch"]).startswith("/v1/export/peers/ix2/peers/remote/"),
      row["fetch"] if row else "")

# ── the rule that had to be decided: no transit ──────────────────────────────
check("and not the backbone two rooms away", "far" not in seen, json.dumps(seen))
st, seen3, _ = origins(IX_PORT["ix3"], TOK["TOK_FAR"])
check("  nor the other way round", seen3 == ["remote"], json.dumps(seen3))
st, seen2, _ = origins(IX_PORT["ix2"], TOK["TOK_REMOTE"])
check("while the room in the middle sees both of its neighbours",
      seen2 == ["far", "home"], json.dumps(seen2))
# The middle room is the one with something to pass on, so it is the one asked not to.
st, to_ix3, _ = origins(IX_PORT["ix2"], TOK["TOK_IX2_IX3"])
check("  and offers ix3 only its own backbone, not ix1's", to_ix3 == ["home"] or to_ix3 == ["remote"],
      json.dumps(to_ix3))
check("  specifically its own", to_ix3 == ["remote"], json.dumps(to_ix3))

# ── nothing comes back to where it started ───────────────────────────────────
st, to_ix1, _ = origins(IX_PORT["ix2"], TOK["TOK_IX1_IX2"])
check("nothing ix1 advertised is offered back to ix1", "home" not in to_ix1, json.dumps(to_ix1))
st, at_home, _ = origins(IX_PORT["ix1"], TOK["TOK_HOME"])
check("  and home is never offered its own area", "home" not in at_home, json.dumps(at_home))

# ── what the backbone makes of it ────────────────────────────────────────────
st, hop0 = get(BB_PORT["home"], "/v1/regions")
peer_rows = [r for r in (hop0.get("regions") or []) if r.get("peer")]
check("home's hop 0 carries the area from the next room", len(peer_rows) == 1,
      json.dumps([r.get("origin") for r in peer_rows]))
check("  named for where it came from, not for the room it came through",
      peer_rows and peer_rows[0]["origin"] == "remote", json.dumps(peer_rows[0].get("origin") if peer_rows else None))
check("  under home's own address, three prefixes deep",
      peer_rows and str(peer_rows[0]["fetch"]).startswith("/v1/peers/ix1/peers/ix2/peers/remote/"),
      peer_rows[0]["fetch"] if peer_rows else "")
check("  and its own areas are untouched",
      len([r for r in hop0["regions"] if not r.get("peer")]) == len(
          [d for d in os.listdir(os.path.join(T, "home", "regions"))
           if os.path.isdir(os.path.join(T, "home", "regions", d))]))

# ── and the document actually arrives, across two rooms ──────────────────────
if peer_rows:
    st, tbl = get(BB_PORT["home"], peer_rows[0]["fetch"])
    check("the area table two rooms away is readable", st == 200, json.dumps(tbl)[:140])
    check("  with its addresses moved onto home's surface",
          "/v1/export/" not in json.dumps(tbl), json.dumps(tbl)[:140])
    entry = next((e for e in (tbl.get("entries") or tbl.get("nodes") or []) if e.get("fetch")), None)
    if check("  and an entry in it to follow", bool(entry), json.dumps(sorted(tbl.keys()))):
        st, body = get(BB_PORT["home"], entry["fetch"], raw=True)
        check("    whose document comes back as the prose it is", st == 200 and isinstance(body, str)
              and len(body) > 0, f"{st} {str(body)[:80]}")

# ── a room the operator can see, and tell apart ──────────────────────────────
def admin(port, token):
    r = urllib.request.Request(f"http://127.0.0.1:{port}/admin/state")
    r.add_header("X-Admin-Token", token)
    try:
        with urllib.request.urlopen(r, timeout=15) as x: return x.status, json.loads(x.read() or b"{}")
    except Exception as e: return 0, {"raw": type(e).__name__}


st, state = admin(IX_PORT["ix2"], ADMIN)
check("the operator of the middle room is let in", st == 200, json.dumps(state)[:120])
kinds = {m["name"]: m.get("kind") for m in (state.get("members") or [])}
check("  and sees which of its members are rooms and which are backbones",
      kinds == {"ix1": "exchange", "ix3": "exchange", "remote": "backbone"}, json.dumps(kinds))
# A room member carries what is behind it, and the operator's number has to say so. Counting by the
# backbone that owns a row made every neighbouring room read "advertising 0" while it was carrying
# everything — the one number on that screen, wrong for exactly the members that matter most.
carrying = {m["name"]: m.get("advertising") for m in (state.get("members") or [])}
check("  and how much each member is carrying, rooms included",
      carrying.get("ix1") == 1 and carrying.get("remote") == 1, json.dumps(carrying))
check("    a room's number is what comes through it, not what it owns",
      carrying.get("ix1", 0) > 0, json.dumps(carrying))
check("  with every one of them answering",
      all(m["reachable"] for m in (state.get("members") or [])),
      json.dumps([(m["name"], m["reachable"], m["error"]) for m in (state.get("members") or [])]))
# The operator's door is health, never knowledge — the same rule as everywhere, restated here because
# a room that peers with rooms is the place somebody would be tempted to relax it.
check("  and still not one reflected row", "regions" not in state, json.dumps(sorted(state.keys())))
check("  nor the line any backbone wrote", not any(l in json.dumps(state) for l in LINE.values()))
st, d = get(IX_PORT["ix2"], "/healthz")
check("  and the room names everyone it can speak to",
      sorted(d.get("members") or []) == ["ix1", "ix3", "remote"], json.dumps(d.get("members")))

# ── a kind written wrong is caught by what the neighbour answers ─────────────
# `kind` is typed by hand, and the whole boundary rests on it. So the middle room is told that IX3 is
# an ordinary backbone — the one mistake that would silently turn it into a carrier for a room it
# never agreed to carry for.
open(os.path.join(T, "members-ix2.yaml"), "w", encoding="utf-8").write(
    "members:\n" + member("remote", "REMOTE", BB_PORT["remote"], "TOK_REMOTE")
    + member("ix1", "IX1", IX_PORT["ix1"], "TOK_IX1_IX2", "exchange")
    + member("ix3", "IX3", IX_PORT["ix3"], "TOK_IX2_IX3", "backbone"))
time.sleep(0.4)
st, leaked, _ = origins(IX_PORT["ix2"], TOK["TOK_IX1_IX2"])
check("a room mislabelled as a backbone still does not get carried", "far" not in leaked,
      json.dumps(leaked))
st, state = admin(IX_PORT["ix2"], ADMIN)
bad = next((m for m in (state.get("members") or []) if m["name"] == "ix3"), None)
check("  and the operator is told which line to fix",
      bad and "kind: exchange" in (bad.get("error") or ""), json.dumps(bad and bad.get("error")))
# And the other direction, which the label alone does not cover. IX2 now believes IX3 is an ordinary
# backbone, so nothing in its own file stops it handing IX3 what IX1 said — only IX3 announcing what
# it is does. This is the half a check that watched incoming rows would have missed entirely.
t0 = time.monotonic()
st, out3, _ = origins(IX_PORT["ix2"], TOK["TOK_IX2_IX3"], kind="exchange")
check("  nor is it handed a third room's knowledge on the way out", out3 == ["remote"],
      json.dumps(out3))
check("  and the mislabelled pair still answer each other", st == 200 and time.monotonic() - t0 < 2.0,
      f"{st} after {time.monotonic() - t0:.1f}s")
# Said plainly, because it is the shape of the guarantee and not a gap in it: with the label wrong
# *and* the caller saying nothing, there is nothing left to go on and the knowledge crosses. Two
# locks, and this is what one of them alone is worth — which is why `kind` is still the one that
# matters, and why the operator is told to fix it rather than reassured that it does not matter.
st, unsaid, _ = origins(IX_PORT["ix2"], TOK["TOK_IX2_IX3"])
check("  though a caller that says nothing, on a line labelled wrong, is taken at the label",
      unsaid == ["home", "remote"], json.dumps(unsaid))
st, seen3, _ = origins(IX_PORT["ix3"], TOK["TOK_FAR"])
check("  so far still sees one room across, and no more", seen3 == ["remote"], json.dumps(seen3))

shutil.rmtree(T, ignore_errors=True)
finished.append(True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
