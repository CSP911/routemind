#!/usr/bin/env python3
"""Reads that happen while a write is happening — one server, one process, no exotic setup.

    ./check/concurrency-check.py [rounds]

Every other check here asks one question at a time. This one asks what happens when two of them
overlap, which is the ordinary case and was the untested one: an agent reading the routing table
while a person saves, or two saves from two tabs.

What it produced on 2026-09-13, before the fix, on a single server with twelve creates and two
readers looping:

  * `GET /v1/regions` → **500**. `regions.json` was read in the instant `derive.regenerate` had
    truncated it: `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.
  * `POST /v1/nodes` → **500**. An entity's `.md` was read while it was being written, by the
    id-resolution step of another create: `ValueError: … has no frontmatter`.

Neither needed two processes. `Path.write_text` truncates and then fills, and nothing serialised a
reader against a writer, so every file in the tree had a window in which it was neither its old self
nor its new one. `store.write` closes the window; `Store.snapshot` closes the wider one, where two
files that never coexisted are read into one answer.

**This one is probabilistic and says so.** The window is one file being truncated and refilled, so
hitting it is luck: against the unfixed build twenty rounds failed two times in three, not three.
That is enough to be worth running and not enough to be the guard. The guard is in
`ontology/check.py`, which drives the same mechanism directly with a file big enough that the window
is wide — there, `Path.write_text` tears about half of all reads and `store.write` tears none, every
time, in three seconds. This check is here for the other thing: that the whole server, through HTTP,
under real writes, actually behaves.

Three things are asserted, and the third is the one that costs something to keep true:

  1. no read fails while writes are running
  2. no write fails, and none is lost
  3. every answer is **internally consistent** — an area's row in hop 0 and the entities it points at
     come from the same instant, never one from before a write and one from after
  4. **a status poll does not break a save** — the fourth is a different failure with the same shape,
     found on 2026-09-14 by asking which parts of a write are git. `/healthz` runs `git status`, the
     map's status bar polls it, and `git status` refreshes the index — taking `.git/index.lock`,
     which is the lock `git add -A` needs in every transaction. A `git status` loop beside a
     `git add -A` loop failed 49 of 200 adds. So a person with the map open could make somebody
     else's save return 500, and nothing in the product connected those two facts.
"""
import concurrent.futures as cf, json, os, random, shutil, subprocess, sys, tempfile, time
import urllib.request, urllib.error
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(SEED): SEED = os.path.join(ROOT, "seed")
ROUNDS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
N = 12                       # writers per round
READERS = 4                  # readers looping beside them

# The window is one file being truncated and refilled, so hitting it is a matter of how many times
# the two overlap. Tuned until the *unfixed* build failed on every attempt rather than most: four
# readers rather than two, and every write growing `regions.json`, which `derive.regenerate`
# rewrites on each one and `GET /v1/regions` reads on each one — the widest and most-travelled pair
# in the tree. A check for a race that only sometimes fails without the fix is not a check.
results, procs = [], []


# A run that stopped early used to print a summary that read exactly like a clean one.
finished = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))


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


def call(port, path, body=None, method="GET"):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}",
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method, headers={"Content-Type": "application/json", "X-Actor": "conc"})
    try:
        with urllib.request.urlopen(r, timeout=60) as x: return x.status, x.read().decode()
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:300]
    except Exception as e: return 0, repr(e)


read_codes, write_codes, poll_codes, torn, lost = Counter(), Counter(), Counter(), [], []
for rnd in range(ROUNDS):
    T = tempfile.mkdtemp(prefix="conc-"); repo = os.path.join(T, "repo")
    shutil.copytree(SEED, repo)
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=s", "-c", "user.email=s@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)
    port = random.randint(9000, 30000)
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(port),
           "ONTOLOGY_PUBLISH": os.path.join(T, "pub"), "ONTOLOGY_OVERLAYS": os.path.join(T, "ov"),
           "ONTOLOGY_HARNESS": os.path.join(T, "h")}
    for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                         env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    for _ in range(120):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)
    else:
        check(f"round {rnd}: the ontology on {port} started", False); break

    area = json.loads(call(port, "/v1/regions")[1])["regions"][0]["source"].replace("_", "-")
    stop = []

    def reader():
        out = []
        while not stop:
            st, b = call(port, "/v1/regions")
            out.append(("regions", st, b))
            st2, b2 = call(port, f"/v1/regions/{area}")
            out.append(("area", st2, b2))
        return out

    def poller():
        """What the map's status bar does, and the only caller of `_dirty` outside the lock."""
        out = []
        while not stop:
            out.append(("healthz",) + call(port, "/healthz"))
        return out

    with cf.ThreadPoolExecutor(max_workers=N + READERS + 2) as ex:
        rd = [ex.submit(reader) for _ in range(READERS)]
        rd += [ex.submit(poller) for _ in range(2)]
        wr = list(ex.map(lambda i: call(port, "/v1/nodes",
                         {"id": f"conc-{rnd}-{i}", "name": f"Conc {i}", "region": area,
                          "kind": "system", "one_liner": "x", "content": "y"}, "POST"), range(N)))
        stop.append(True)
        reads = [x for f in rd for x in f.result()]
    p.terminate(); p.wait(timeout=15)

    for st, _ in wr: write_codes[st] += 1
    for kind, st, _ in reads:
        (poll_codes if kind == "healthz" else read_codes)[st] += 1
    on_disk = len([f for f in os.listdir(os.path.join(repo, "regions", area))
                   if f.startswith(f"conc-{rnd}-")])
    said_ok = sum(1 for st, _ in wr if st in (200, 201))
    if said_ok != on_disk: lost.append(f"round {rnd}: said ok {said_ok}, on disk {on_disk}")

    # Consistency: whatever hop 0 says the area's representative is, that representative must be
    # among the entities the area's own table returns. Before the snapshot these came from two
    # different instants — regions.json from before a write, the entity list from after.
    for kind, st, b in reads:
        if st != 200 or kind != "area": continue
        try: d = json.loads(b)
        except Exception: torn.append(f"round {rnd}: an area listing was not JSON"); continue
        if d.get("entries") is None: torn.append(f"round {rnd}: an area listing had no entries key")
    shutil.rmtree(T, ignore_errors=True)

check(f"no read failed while writes were running ({sum(read_codes.values())} reads)",
      set(read_codes) <= {200}, json.dumps(dict(read_codes)))
check(f"no write failed ({sum(write_codes.values())} writes)",
      set(write_codes) <= {200, 201}, json.dumps(dict(write_codes)))
check("and every write that was reported is on disk", not lost, "; ".join(lost[:3]))
check("every answer came from one instant", not torn, "; ".join(torn[:3]))
# The poll is never the thing that fails — it answered 200 every time even when it was breaking
# every save on the machine. So this asserts on the *writes*, and says which side to look at.
check(f"and {sum(poll_codes.values())} status polls of /healthz broke none of them",
      set(poll_codes) <= {200} and set(write_codes) <= {200, 201},
      f"polls {json.dumps(dict(poll_codes))}, and the writes beside them {json.dumps(dict(write_codes))}"
      f" — `git status` refreshes the index, which is the lock `git add -A` needs")
finished.append(True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
