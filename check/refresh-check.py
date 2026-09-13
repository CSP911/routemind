#!/usr/bin/env python3
"""Taking an advertisement back, and how long it stays on somebody else's table.

    ./check/refresh-check.py [port]

Two backbones and an exchange, on throwaway repositories, with a **long** cache — thirty seconds
rather than the five a real install uses. Every other peering check runs with the cache off, which is
right for asking whether a row is correct and useless for asking when it goes away. Needs pyyaml.

Advertising something a few seconds late is a delay. Withdrawing something a few seconds late is the
withdrawn thing still sitting on somebody else's table, and narrowing an audience is a withdrawal for
whoever just left the list. So a backbone whose export set changes says so, and this is the difference
that says makes.

  * **A control first**, because otherwise this checks nothing: the same withdrawal made behind the
    server's back stays visible, which is what the cache is for and what the hint is shortening.
  * **It crosses a room.** A withdrawal that reaches the exchange and stops there is a withdrawal that
    sits on every member's table for the length of their own cache.
  * **It is a hint, not a protocol.** `ADVERT_TTL` remains the guarantee: a peer that is down while
    the hint goes out still reads the new set on its own, and nothing fails because a poke did not
    land.
  * **It terminates.** A hint carries no path to check itself against, so it carries a budget that
    only goes down.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8241
A_PORT, B_PORT, IX_PORT = BASE, BASE + 1, BASE + 10
TTL = "30"                      # long enough that a stale answer cannot be mistaken for a fresh one
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

T = tempfile.mkdtemp(prefix="refresh-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

TOK = {"TOK_A": "tok-a", "TOK_B": "tok-b"}
LINE = "what the other office may ask us · the questions we answer for them"
SHARED = sorted(d for d in os.listdir(os.path.join(seed, "regions"))
                if os.path.isdir(os.path.join(seed, "regions", d)))[0]
repos = {}

for n, port in (("a", A_PORT), ("b", B_PORT)):
    repo = os.path.join(T, n); shutil.copytree(seed, repo); repos[n] = repo
    if n == "b":
        for f in sorted(os.listdir(os.path.join(repo, "regions", SHARED))):
            q = os.path.join(repo, "regions", SHARED, f)
            t = open(q, encoding="utf-8").read()
            if "\nrole: representative\n" in t and "\nparent:" not in t:
                open(q, "w", encoding="utf-8").write(
                    t.replace("\nrole: representative\n",
                              f"\nrole: representative\nuse_when_export: {LINE}\n", 1))
                break
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: ix\n    label: EXCHANGE\n    url: http://127.0.0.1:{IX_PORT}\n"
        f"    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)
    e = {**os.environ, **TOK, "ONTOLOGY_DATA": repo, "PORT": str(port),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"),
         "ONTOLOGY_PEER_TOKEN": TOK[f"TOK_{n.upper()}"], "ONTOLOGY_PEER_TTL": TTL}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

MEMBERS = os.path.join(T, "members.yaml")
open(MEMBERS, "w", encoding="utf-8").write(
    "members:\n"
    f"  - name: ay\n    label: AY\n    url: http://127.0.0.1:{A_PORT}\n    token_env: TOK_A\n"
    f"  - name: bee\n    label: BEE\n    url: http://127.0.0.1:{B_PORT}\n    token_env: TOK_B\n")
procs.append(subprocess.Popen(
    [sys.executable, os.path.join(ROOT, "exchange", "server.py")],
    env={**os.environ, **TOK, "EXCHANGE_NAME": "ix", "PORT": str(IX_PORT),
         "EXCHANGE_MEMBERS": MEMBERS, "ONTOLOGY_PEER_TTL": TTL},
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

for port in (A_PORT, B_PORT, IX_PORT):
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def get(port, path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=20) as x:
            return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e: return e.code, {}
    except Exception as e: return 0, {"raw": type(e).__name__}


def refresh(port, token, hops=None):
    r = urllib.request.Request(f"http://127.0.0.1:{port}/v1/export/refresh", data=b"", method="POST")
    if token: r.add_header("X-Peer-Token", token)
    if hops is not None: r.add_header("X-Refresh-Hops", str(hops))
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e: e.read(); return e.code, {}
    except Exception as e: return 0, {"raw": type(e).__name__}


def at_a():
    return [r for r in (get(A_PORT, "/v1/regions")[1].get("regions") or []) if r.get("peer")]


def withdraw_quietly():
    """Behind the server's back: the frontmatter, the derived file, a commit — and no API call, so
    nothing announces anything. This is the control."""
    for f in sorted(os.listdir(os.path.join(repos["b"], "regions", SHARED))):
        q = os.path.join(repos["b"], "regions", SHARED, f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in t or "\nparent:" in t: continue
        open(q, "w", encoding="utf-8").write(
            "".join(l for l in t.splitlines(True) if not l.startswith("use_when_export:")))
        break
    regenerate(Store(repos["b"]))
    subprocess.run(["git", "-C", repos["b"], "add", "-A"], check=True)
    subprocess.run(["git", "-C", repos["b"], "-c", "user.name=x", "-c", "user.email=x@l",
                    "commit", "-q", "--allow-empty", "-m", "withdraw"], check=True)


# ── the row is there, and both caches are now warm ───────────────────────────
check("a sees the area b advertises", len(at_a()) == 1, json.dumps([r.get("source") for r in at_a()]))
check("  and b is still serving it", get(B_PORT, "/v1/regions")[0] == 200)

# ── the control: withdrawn quietly, so nobody was told ───────────────────────
withdraw_quietly()
time.sleep(0.6)
check("withdrawn behind the server's back, it stays on a's table",
      len(at_a()) == 1, json.dumps([r.get("source") for r in at_a()]))
check("  which is the cache, not a bug — the row is genuinely gone at b",
      not any(r.get("use_when_export") for r in (get(B_PORT, "/v1/regions")[1].get("regions") or [])))

# ── the hint, sent by hand, crossing the room ────────────────────────────────
# b tells the room; the room tells a. Two hops, and the second is the one that would be missed by
# anything that only forgot what it was told about directly.
st, r = refresh(IX_PORT, TOK["TOK_B"])
check("the room takes the hint", st == 200 and r.get("forgot") == "bee", f"{st} {json.dumps(r)}")
time.sleep(1.0)
check("  and the row goes from a's table without waiting out the cache",
      len(at_a()) == 0, json.dumps([r.get("source") for r in at_a()]))
check("  while a's own areas are untouched",
      len(get(A_PORT, "/v1/regions")[1].get("regions") or []) > 0)
check("  and the link still reads as up, because nothing broke",
      all(l["reachable"] for l in (get(A_PORT, "/v1/regions")[1].get("links") or [])))

# ── the door ─────────────────────────────────────────────────────────────────
check("a hint with no token is refused", refresh(IX_PORT, None)[0] == 401)
check("  and one with a wrong token is refused", refresh(IX_PORT, "nope")[0] == 401)
# A backbone will not take one on the shared token either: forgetting is per peer, and a caller with
# no name says which peer to forget no better than a stranger does.
check("  and a backbone wants a name, not just a key",
      refresh(A_PORT, "nope")[0] == 401)
check("  while a peer it can name is taken", refresh(A_PORT, TOK["TOK_A"])[0] == 200)

# ── it stops ─────────────────────────────────────────────────────────────────
# A hint carries no path, so it carries a budget. Nothing here should still be running in a second.
t0 = time.monotonic()
st, _ = refresh(IX_PORT, TOK["TOK_B"], hops=0)
check("a hint with nothing left to spend is taken and passed nowhere", st == 200, str(st))
st, _ = refresh(IX_PORT, TOK["TOK_B"], hops=9)
check("  and a large budget still answers at once",
      st == 200 and time.monotonic() - t0 < 6.0, f"{st} after {time.monotonic() - t0:.1f}s")
check("  with every service still answering afterwards",
      all(get(p, "/healthz")[0] == 200 for p in (A_PORT, B_PORT, IX_PORT)))

# ── and a write through the API announces on its own ─────────────────────────
# The whole point: nobody should have to remember to send one.
for f in sorted(os.listdir(os.path.join(repos["b"], "regions", SHARED))):
    q = os.path.join(repos["b"], "regions", SHARED, f)
    t = open(q, encoding="utf-8").read()
    if "\nrole: representative\n" not in t or "\nparent:" in t: continue
    node_id = next(l.split(":", 1)[1].strip() for l in t.splitlines() if l.startswith("id:"))
    break
body = json.dumps({"use_when_export": LINE}).encode()
req = urllib.request.Request(f"http://127.0.0.1:{B_PORT}/v1/nodes/{node_id}", data=body,
                             method="PUT", headers={"Content-Type": "application/json",
                                                      "X-Actor": "refresh-check"})
try:
    with urllib.request.urlopen(req, timeout=25) as x: wrote = x.status
except urllib.error.HTTPError as e: wrote = f"{e.code} {e.read().decode(errors='replace')[:120]}"
except Exception as e: wrote = type(e).__name__
if check("advertising it again through the API works", wrote == 200, str(wrote)):
    time.sleep(1.5)
    check("  and it is back on a's table, with nobody having sent a hint",
          len(at_a()) == 1, json.dumps([r.get("source") for r in at_a()]))

# ── every field a peer can see, or the hint is not a hint ────────────────────
# The fingerprint that decides whether to send one listed the areas, the line and the audience, and
# was written before a line could be addressed to one reader by name. So writing that line changed
# what that reader is shown and sent nothing: the row sat stale for a cache at each hop while the
# change looked done — and a line written for one reader is usually the narrower one, which is the
# single case this whole mechanism exists for.
rep_id = None
for f in sorted(os.listdir(os.path.join(repos["b"], "regions", SHARED))):
    t = open(os.path.join(repos["b"], "regions", SHARED, f), encoding="utf-8").read()
    if "\nrole: representative\n" in t and "\nparent:" not in t:
        rep_id = next(l.split(":", 1)[1].strip() for l in t.splitlines() if l.startswith("id:"))
        break
FOR_A = "what b tells a in particular, and nobody else"
body = json.dumps({"use_when_export": LINE, "use_when_export_for": {"ay": FOR_A}}).encode()
req = urllib.request.Request(f"http://127.0.0.1:{B_PORT}/v1/nodes/{rep_id}", data=body, method="PUT",
                             headers={"Content-Type": "application/json", "X-Actor": "refresh-check"})
try:
    with urllib.request.urlopen(req, timeout=30) as x: wrote = x.status
except urllib.error.HTTPError as e: wrote = f"{e.code} {e.read().decode(errors='replace')[:120]}"
except Exception as e: wrote = type(e).__name__
if check("a line written for one named reader is a write a peer can see", wrote == 200, str(wrote)):
    time.sleep(1.5)
    rows = at_a()
    check("  and the row is still on a's table", len(rows) == 1,
          json.dumps([r.get("source") for r in rows]))
    # The whole assertion in one line: with a thirty-second cache at each hop, a's table already
    # carries the sentence written for a. Without the field in the fingerprint no hint goes out and
    # this is the old line for the next half-minute, with everything looking done.
    check("  carrying the line written for it, with no cache waited out",
          rows and rows[0].get("use_when") == FOR_A,
          json.dumps(rows[0].get("use_when") if rows else None))

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
