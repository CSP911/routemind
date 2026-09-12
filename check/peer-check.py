#!/usr/bin/env python3
"""What crosses a link between two backbones, and what must not.

    ./check/peer-check.py [port]

Starts its own backbones on throwaway repositories, because everything here is about what one
install lets another install see, and getting that wrong on somebody's real ontology is the whole
risk. Needs pyyaml on this python; see check/write-paths.sh for the same requirement.

The property under test is not "the token works". It is that **the export surface cannot serve an
area nobody decided to share** — no path through it, and no mistake in a token check, reaches one.
An area crosses a link by having `use_when_export` written on its representative, and by nothing
else. So the checks below are mostly negative: they name things that exist, are readable locally,
and must still come back 404 across the link.

docs/PEERING.md is the contract.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8171
TOKEN = "peer-check-token"
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results: print("\n".join(results))
    if results: print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="peer-check-")
repo = os.path.join(T, "repo")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
shutil.copytree(seed, repo)

sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

# One area is shared, by writing the line that shares it. Nothing else about the repository changes,
# which is the point: sharing is one field, and its absence is the default.
areas = sorted(d for d in os.listdir(os.path.join(repo, "regions"))
               if os.path.isdir(os.path.join(repo, "regions", d)))
SHARED, PRIVATE = areas[0], (areas[1] if len(areas) > 1 else None)
EXPORT_LINE = "what a partner may ask this office · the questions we answer for them"
rep_file = None
for f in sorted(os.listdir(os.path.join(repo, "regions", SHARED))):
    p = os.path.join(repo, "regions", SHARED, f)
    text = open(p, encoding="utf-8").read()
    if "\nrole: representative\n" in text and "\nparent:" not in text:
        open(p, "w", encoding="utf-8").write(
            text.replace("\nrole: representative\n", f"\nrole: representative\nuse_when_export: {EXPORT_LINE}\n", 1))
        rep_file = p; break
if not rep_file: raise SystemExit(f"no top representative in {SHARED} to share")
regenerate(Store(repo))
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=peer", "-c", "user.email=p@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)

env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT),
       "ONTOLOGY_PUBLISH": os.path.join(T, "publish"), "ONTOLOGY_PEER_TOKEN": TOKEN}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else: raise SystemExit(f"the backbone on {PORT} did not start")


def get(path, token=None):
    r = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1{path}")
    if token: r.add_header("X-Peer-Token", token)
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read()
        try: return e.code, json.loads(body or b"{}")
        except Exception: return e.code, {"raw": body.decode(errors="replace")[:120]}


# ── the door ──────────────────────────────────────────────────────────────────
check("no token is refused", get("/export/regions")[0] == 401)
check("a wrong token is refused", get("/export/regions", "not-the-token")[0] == 401)
st, adv = get("/export/regions", TOKEN)
check("the right token is let in", st == 200, str(st))

# ── what the peer sees ────────────────────────────────────────────────────────
rows = adv.get("regions") or []
check("only the shared area is advertised", [r["source"].replace("_", "-") for r in rows] == [SHARED],
      json.dumps([r["source"] for r in rows]))
# The whole reason use_when_export exists. An advertisement written for one backbone's hop 0 has no
# reason to be true in another's, so a peer must never be shown the local one by accident.
check("  and with the line written for a peer, not the local one",
      rows and rows[0]["use_when"] == EXPORT_LINE, rows[0]["use_when"] if rows else "")
local = next(r for r in get("/regions")[1]["regions"] if r["source"].replace("_", "-") == SHARED)
check("  which is not the line its own hop 0 shows", local["use_when"] != EXPORT_LINE)
# Staleness across a link needs no clock: git already numbers every state this repository has been in.
check("the advertisement says which revision it came from",
      len(str(adv.get("revision") or "")) == 40, str(adv.get("revision"))[:12])
check("the address it prints is on the export surface",
      rows and str(rows[0].get("fetch") or "").startswith("/v1/export/"), rows[0].get("fetch") if rows else "")

# ── what the peer must not see ────────────────────────────────────────────────
check("the shared area's own table crosses", get(f"/export/regions/{SHARED}", TOKEN)[0] == 200)
if PRIVATE:
    check("an area nobody shared does not", get(f"/export/regions/{PRIVATE}", TOKEN)[0] == 404)
    # 404 and not 403, deliberately: whether this backbone holds something it has not shared is itself
    # not the peer's business, so the two answers have to be indistinguishable.
    check("  and says 404, not 'exists but forbidden'",
          (get(f"/export/regions/{PRIVATE}", TOKEN)[1].get("error") or "").lower().count("forbid") == 0)

nodes = Store(repo).nodes()
shared_node = next((n["id"] for n in nodes if n.get("region") == SHARED.replace("-", "_")), None)
private_node = next((n["id"] for n in nodes if PRIVATE and n.get("region") == PRIVATE.replace("-", "_")), None)
if shared_node: check("a node inside the shared area crosses", get(f"/export/nodes/{shared_node}", TOKEN)[0] == 200)
if private_node:
    check("a node inside a private area does not", get(f"/export/nodes/{private_node}", TOKEN)[0] == 404,
          private_node)
    check("  though it reads perfectly well locally", get(f"/nodes/{private_node}")[0] == 200)

# ── a link is read-only ───────────────────────────────────────────────────────
# Not a limitation waiting to be lifted. Two ontologies that write to each other have been merged,
# and merging them is the thing a link exists to avoid.
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/export/regions", method="POST",
                             data=b"{}", headers={"Content-Type": "application/json", "X-Peer-Token": TOKEN})
try:
    urllib.request.urlopen(req, timeout=10); code = 200
except urllib.error.HTTPError as e: code = e.code
except Exception: code = 0
check("a write across the link is refused", code == 405, str(code))

# ── and the local install is untouched by any of it ───────────────────────────
check("the local hop 0 still lists every area",
      len(get("/regions")[1].get("regions") or []) == len(areas), str(len(areas)))

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
