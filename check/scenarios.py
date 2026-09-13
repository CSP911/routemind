#!/usr/bin/env python3
"""The routing table over a whole lifetime — docs/SCENARIOS.md is the contract.

    ./check/scenarios.py [port]

Every other check asks whether one call answers correctly. This one asks whether what an agent reads
still tells the truth after the ontology has been lived in: areas created, advertised, emptied,
deleted, created again. Several of these delete everything, so it runs against a throwaway ontology
it starts itself — nothing here touches a live install.

Needs pyyaml, which the ontology image has and a host usually does not:

    docker cp check $(docker compose ps -q ontology):/tmp/check
    docker cp mcp   $(docker compose ps -q ontology):/tmp/mcp
    docker compose exec ontology python3 /tmp/check/scenarios.py
"""
import atexit, json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

# Two layouts, because this check runs in two places. From a checkout the service and the seed sit
# beside this file; copied into the ontology container they do not — the image keeps them at /app,
# flattened, with no `ontology/` above them. This used to be closed by a line of symlinks in the
# procedure above, which is a step that works perfectly and that the next person forgets, and the
# failure it produces ("the ontology on 8131 did not start") names none of it. Find them instead.
def _tree():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for server, seed in ((os.path.join(here, "ontology", "service", "server.py"), os.path.join(here, "seed")),
                         ("/app/service/server.py", "/app/seed")):
        if os.path.exists(server) and os.path.isdir(seed): return server, seed
    raise SystemExit("no ontology to run: looked beside this check and in /app")

SERVER, SEED = _tree()
# The package root for `import service.…` — the directory holding `service/`, which is `ontology/` in
# a checkout and `/app` in the image. ROOT stays what it always was, for the MCP server: that one is
# copied to /tmp/mcp beside /tmp/check, so it is in the same place in both layouts.
SERVICE_PARENT = os.path.dirname(os.path.dirname(SERVER))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8131
results, procs, notes = [], [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def note(name, what):
    """Behaviour worth recording that nobody has decided on yet. It prints, it never fails."""
    notes.append(f"--   {name}: {what}")


@atexit.register
def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results: print("\n".join(results))
    if notes: print("\n".join(notes))
    if results: print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


T = tempfile.mkdtemp(prefix="scenarios-")
repo = os.path.join(T, "repo")
shutil.copytree(SEED, repo)
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=seed", "-c", "user.email=s@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)

env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT),
       "ONTOLOGY_PUBLISH": os.path.join(T, "publish"),
       "ONTOLOGY_OVERLAYS": os.path.join(T, "overlays"),
       # The review queue is the only path that writes `use_when` (B2), so the curator has to exist.
       "ONTOLOGY_HARNESS": os.path.join(T, "harness")}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
procs.append(subprocess.Popen([sys.executable, SERVER],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
API = f"http://127.0.0.1:{PORT}/v1"
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else: raise SystemExit(f"the ontology on {PORT} did not start")


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Content-Type": "application/json", "X-Actor": "scenarios"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read()
        try: return e.code, json.loads(body or b"{}")
        except Exception: return e.code, {"raw": body.decode(errors="replace")[:200]}


class Mcp:
    """The rendered tables, because what an agent reads is text and not JSON."""
    def __init__(self):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   "--api", API, "--actor", "scenarios"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, bufsize=1)
        procs.append(self.p); self.n = 0
        self.rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                "clientInfo": {"name": "scenarios", "version": "0"}})

    def rpc(self, method, params=None):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}) + "\n")
        self.p.stdin.flush()
        return json.loads(self.p.stdout.readline() or "{}")

    def table(self, path=None):
        r = self.rpc("tools/call", {"name": "knowledge_table", "arguments": {"path": path} if path else {}})
        return ((r.get("result") or {}).get("content") or [{}])[0].get("text", "")


mcp = Mcp()
core = lambda: open(os.path.join(repo, "CORE.md"), encoding="utf-8").read()
regions = lambda: json.loads(open(os.path.join(repo, "regions.json"), encoding="utf-8").read())["regions"]


def make_area(src, name, use_when, core_desc):
    return call("POST", "/regions", {"source": src, "core_description": core_desc,
                                     "representative": {"id": src, "name": name, "kind": "system",
                                                        "one_liner": f"{name} — what it holds",
                                                        "use_when": use_when}})


# ── A. the routing table over a lifetime ──────────────────────────────────────
empty_top = mcp.table()
check("A1 an empty ontology still prints hop 0", "KNOWLEDGE" in empty_top or "ROUTEMIND" in empty_top)
check("A1   and says it holds nothing", "(nothing here)" in empty_top)
check("A1   and still carries the absence rule", "grounds on which you may say" in empty_top)

st, _ = make_area("alpha", "Alpha", "an alpha question · something alpha", "the alpha area")
check("A2 an area is created", st in (200, 201), str(st))
top = mcp.table()
check("A2   it reaches hop 0", "/v1/regions/alpha" in top)
check("A2   with the sentence it is chosen by", "an alpha question" in top)

make_area("beta", "Beta", "a beta question · something beta", "the beta area")
top = mcp.table()
check("A3 both areas are advertised", "/v1/regions/alpha" in top and "/v1/regions/beta" in top)
check("A3   and hop 0 is ordered, not creation-ordered",
      top.index("/v1/regions/alpha") < top.index("/v1/regions/beta"))

st, body = call("DELETE", "/regions/alpha")
check("A4 an area is deleted", st == 200, json.dumps(body)[:120])
top = mcp.table()
check("A4   it leaves hop 0", "/v1/regions/alpha" not in top)
check("A4   and its CORE row goes with it", "`ALPHA`" not in core())
check("A4   while the other stays", "/v1/regions/beta" in top)

call("DELETE", "/regions/beta")
top = mcp.table()
check("A5 with everything deleted, hop 0 is what it was when empty", top.strip() == empty_top.strip())
check("A5   regions.json holds nothing", regions() == [])
check("A5   the CORE table keeps its header, so the next area can be written into it",
      "| Area | What it holds |" in core() and "|---|---|" in core())
check("A5   and no area directory is left behind",
      sorted(p for p in os.listdir(os.path.join(repo, "regions")) if not p.startswith(".")) == [])

# ── B. what an area advertises ────────────────────────────────────────────────
st, body = make_area("mute", "Mute", "", "an area with nothing to pick it by")
if st in (200, 201):
    top = mcp.table()
    row = next((l for l in top.splitlines() if "/v1/regions/mute" in l), "")
    note("B1", "an area with an empty use_when is accepted, and hop 0 carries the row: "
               + (repr(row.strip()) if row else "…but the row is not printed"))
    call("DELETE", "/regions/mute")
else:
    check("B1 an area with nothing to pick it by is refused", st in (400, 422), str(st))

make_area("gamma", "Gamma", "a gamma question", "the gamma area")
st, prop = call("POST", "/curator/proposals",
                {"scope": "bb", "region": "gamma", "before": "a gamma question",
                 "after": "a gamma question · and another one", "why": "the second one belongs here"})
if check("B2 a change to use_when can be proposed", st in (200, 201), json.dumps(prop)[:120]):
    st, out = call("POST", f"/curator/proposals/{prop['id']}/accept", {})
    check("B2   accepting it applies", st == 200 and (out.get("result") or {}).get("ok") is not False,
          json.dumps(out)[:140])
    check("B2   and hop 0 says the new sentence", "and another one" in mcp.table())

top = mcp.table()
check("B3 hop 0 lists areas and nothing else",
      all("/v1/nodes/" not in l for l in top.splitlines()))

# ── C. created, but not advertised ────────────────────────────────────────────
st, _ = call("POST", "/nodes", {"id": "seen", "name": "Seen", "kind": "system", "region": "gamma",
                                "one_liner": "a node anyone may route to"})
check("C  a plain node is created", st in (200, 201), str(st))
draft_body = {"id": "hidden", "name": "Hidden", "kind": "system", "region": "gamma",
              "one_liner": "a node the agent should not be sent to yet", "status": "draft"}
st, body = call("POST", "/nodes", dict(draft_body))
check("C0 a draft is refused in an area that has not asked for them", st == 422, str(st))
check("C0   and the refusal names the rule",
      "draft" in json.dumps(body).lower(), json.dumps(body)[:140])

# Drafts are opt-in per area (`area_rules` in vocab.yaml), so the area has to say so first. The file
# is edited and committed the way a person would, because an uncommitted repository blocks writes.
vocab = os.path.join(repo, "vocab.yaml")
with open(vocab, "a", encoding="utf-8") as f:
    f.write("\narea_rules:\n  gamma:\n    drafts: true\n")
subprocess.run(["git", "-C", repo, "-c", "user.name=seed", "-c", "user.email=s@l",
                "commit", "-qam", "gamma may hold drafts"], check=True)

st, body = call("POST", "/nodes", dict(draft_body))
check("C1 a draft node is created once the area allows it", st in (200, 201), json.dumps(body)[:140])
listed = next((r["nodes"] for r in regions() if r["source"] == "gamma"), [])
check("C1   it is not in the area's advertised nodes", "hidden" not in listed and "seen" in listed,
      str(listed))
area_table = mcp.table("/v1/regions/gamma")
check("C1   and not in the area's rendered table", "/v1/nodes/hidden" not in area_table)

# Where the line is drawn, written down so it is a decision rather than an accident: a draft is
# never *advertised* — no listing an agent is handed carries its address — but fetching it directly
# still answers. An agent is told never to build an address and is only ever given ones a table
# printed, so it cannot reach this; and the review screen, when it lands, has to be able to read the
# thing a person is being asked to accept.
st, _ = call("GET", "/nodes/hidden")
check("C2 a draft is unlisted, not sealed — a direct fetch still answers", st == 200, str(st))
check("C2   but no advertised listing anywhere carries its address",
      "/v1/nodes/hidden" not in mcp.table("/v1/regions/gamma") + mcp.table())

st, body = call("PUT", "/nodes/hidden", {"status": "published"})
listed = next((r["nodes"] for r in regions() if r["source"] == "gamma"), [])
check("C3 publishing the draft advertises it", st == 200 and "hidden" in listed,
      f"PUT answered {st}, list {listed}")
check("C3   and the rendered table now offers it", "/v1/nodes/hidden" in mcp.table("/v1/regions/gamma"))

# ── F. a VRF while the tree moves under it ────────────────────────────────────
st, ov = call("POST", "/overlays", {"question": "does an overlay survive its area being deleted",
                                    "by": {"kind": "agent", "name": "scenarios"},
                                    "members": [{"address": "/v1/regions/gamma", "why": "the whole area"}]})
if check("F  an overlay is created over an area", st in (200, 201), json.dumps(ov)[:120]):
    oid = ov["id"]
    st, before = call("GET", f"/overlays/{oid}")
    rows_before = before.get("rows")
    call("POST", "/nodes", {"id": "later", "name": "Later", "kind": "system", "region": "gamma",
                            "one_liner": "added after the overlay was drawn"})
    st, after = call("GET", f"/overlays/{oid}")
    check("F2 an overlay's rows are read now, not frozen when it was drawn",
          (after.get("rows") or 0) > (rows_before or 0), f"{rows_before} → {after.get('rows')}")

    for nid in ("seen", "hidden", "later"): call("DELETE", f"/nodes/{nid}")
    st, body = call("DELETE", "/regions/gamma")
    check("F1 the area an overlay names can be deleted", st == 200, json.dumps(body)[:140])
    st, gone = call("GET", f"/overlays/{oid}")
    check("F1   reading the overlay afterwards does not crash", st < 500, f"answered {st}")
    if st == 200:
        printed = json.dumps(gone.get("sections") or [], ensure_ascii=False)
        check("F1   and it does not still list what the deleted area held",
              "/v1/nodes/seen" not in printed, printed[:140])
        note("F1", f"the overlay still answers {st}, state={gone.get('state')}, rows={gone.get('rows')}")
    else:
        note("F1", f"the overlay answers {st} once its only member is gone")

# ── G. the repository edited by hand ──────────────────────────────────────────
# README tells you to edit `vocab.yaml` and commit, so a dirty working tree is a state real people
# reach. Writes are refused there, and the screen names the files — which it did a character short:
# the porcelain path starts at column 3, and stripping the whole output ate the leading space of the
# first line only, so with one file dirty, the usual case, it named a file that does not exist.
# F deleted the last area, and a write into an area that does not exist is refused before the dirty
# check ever runs — so there has to be somewhere for the blocked write to aim at.
make_area("delta", "Delta", "a delta question", "the delta area")
open(os.path.join(repo, "vocab.yaml"), "a", encoding="utf-8").write("\n# edited by hand\n")
st, body = call("POST", "/nodes", {"id": "zz-blocked", "name": "Blocked", "kind": "system",
                                   "region": "delta", "one_liner": "must not be created"})
check("G1 a hand-edited repository refuses writes", st == 409, str(st))
check("G1   and says why, in words", "dirty" in json.dumps(body).lower(), json.dumps(body)[:120])
import urllib.request as _u2
with _u2.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=5) as r: health = json.load(r)
check("G2 it names the file, whole", health.get("uncommitted") == "vocab.yaml",
      repr(health.get("uncommitted")))
open(os.path.join(repo, "CORE.md"), "a", encoding="utf-8").write("\n")
with _u2.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=5) as r: health = json.load(r)
check("G2   and every file when there are several", health.get("uncommitted") == "CORE.md, vocab.yaml",
      repr(health.get("uncommitted")))
subprocess.run(["git", "-C", repo, "checkout", "--", "vocab.yaml", "CORE.md"], check=True)
with _u2.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=5) as r: health = json.load(r)
check("G3 reverting makes it writable again", health.get("writable") is True and not health.get("uncommitted"),
      repr(health.get("uncommitted")))

# ── H. the clock the expiry runs on ───────────────────────────────────────────
# Overlay stamps are UTC, and the age of one must not depend on where the service happens to run.
# It did: `time.mktime(...) - time.timezone` mixes a standard offset with a value that carries DST,
# and the two cancel only outside summer time — an hour out in Europe/London and America/New_York,
# exactly right in Asia/Seoul, which is the signature. The containers run UTC, so this was invisible
# in deployment and visible only to whoever ran these checks on their own machine in July.
sys.path.insert(0, SERVICE_PARENT)
from service.overlays import _age_hours as _age                     # noqa: E402
_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 10 * 3600))
_was = os.environ.get("TZ")
_ages = {}
for _tz in ("UTC", "Asia/Seoul", "Europe/London", "America/New_York", "Australia/Sydney"):
    os.environ["TZ"] = _tz; time.tzset()
    _ages[_tz] = round(_age(_stamp), 2)
if _was is None: os.environ.pop("TZ", None)
else: os.environ["TZ"] = _was
time.tzset()
check("H  a stamp is the same age in every timezone", len(set(_ages.values())) == 1, json.dumps(_ages))
check("H    and that age is right", all(abs(v - 10) < 0.05 for v in _ages.values()), json.dumps(_ages))

# ── I. a name that has to become a file ───────────────────────────────────────
# Three inputs are written straight into a path: a node id becomes `<id>.md`, an area name becomes the
# directory, and an attached file name is the file. None of them was bounded, and every filesystem
# stops one path component at 255 bytes — so each of the three passed its kebab-case check, passed
# validation, and died inside the transaction on `OSError: [Errno 36] File name too long`. The API
# could only answer `502 internal error`. Probing every malformed input the surface accepts — broken
# JSON, no Content-Type, wrong method, an unknown path, an array for a body — these three were the
# only ones that came back with no reason, and a caller given `internal error` has nothing to fix.
#
# The boundary is asserted from both sides. A bound nobody has watched permit the longest legal name
# is a bound that drifts down to whatever the first refusal happened to be.
LONG = "z" * 300
make_area("names", "Names", "a question about names · nothing real", "the area section I writes into")
st, b = call("POST", "/nodes", {"id": LONG, "name": "P", "region": "names", "kind": "system",
                                "one_liner": "p", "content": "x"})
check("I1 an over-long id is refused, not a crash", st == 400, f"{st} {b}")
check("I1   and the refusal says why", "255" in str(b.get("error", "")), repr(b.get("error"))[:120])

st, b = call("POST", "/regions", {"source": LONG, "core_description": "p",
                                  "representative": {"name": "P", "kind": "system",
                                                     "one_liner": "p", "use_when": "never"}})
check("I2 an over-long area name is refused", st == 400, f"{st} {b}")

st, b = call("PUT", f"/nodes/names/files/{LONG}.md", {"content": "x", "description": "p"})
check("I3 an over-long attached file name is refused", st == 400, f"{st} {b}")

# 252 + len(".md") is exactly 255. Both sides, so the limit stays where the filesystem put it.
_at = "y" * 252
st, _ = call("POST", "/nodes", {"id": _at, "name": "At", "region": "names", "kind": "system",
                                "one_liner": "p", "content": "x"})
_file = os.path.join(repo, "regions", "names", _at + ".md")
check("I4 the longest name that fits is written", st in (200, 201) and os.path.exists(_file),
      f"{st} exists={os.path.exists(_file)}")
check("I4   and it is exactly the filesystem's limit", len(os.path.basename(_file).encode()) == 255)
call("DELETE", f"/nodes/{_at}")
st, _ = call("POST", "/nodes", {"id": "y" * 253, "name": "Over", "region": "names", "kind": "system",
                                "one_liner": "p", "content": "x"})
check("I5 one byte over is refused", st == 400, str(st))

# ── J. the publish that fails after the commit ────────────────────────────────
# The commit is inside the transaction; publishing is after it, and publishing can fail on its own —
# a full disk, a read-only mount, a checkout directory owned by another uid. It used to propagate, so
# a write that had fully succeeded answered `500 internal error`. An agent told that retries and gets
# `409 exists`; a person presses Submit again. Both then act on a lie about what is in the ontology.
#
# The state was never in danger, and that is the point: publishing is downstream, every read here
# serves the repository, and the next successful write publishes a HEAD that carries this commit. Only
# the report was wrong, which is the kind of bug no amount of checking the data will find.
_pub = os.path.join(T, "publish")
# `geteuid` is POSIX-only; on a platform without it there is no root to be, so nobody is.
if getattr(os, "geteuid", lambda: 1)() == 0:
    note("J", "skipped — running as root, which walks through the directory permission this needs")
else:
    _before = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    os.chmod(_pub, 0o555)
    try:
        st, b = call("POST", "/nodes", {"id": "pubfail", "name": "Pub Fail", "region": "names",
                                        "kind": "system", "one_liner": "x", "content": "y"})
        _after = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        check("J1 a write whose publish fails is not reported as failed", st in (200, 201), f"{st} {b}")
        check("J1   and it says the checkout is behind",
              any("behind" in str(w) for w in (b.get("warnings") or [])),
              json.dumps(b.get("warnings") or [])[-160:])
        check("J2 the commit stands", _after != _before, f"{_before[:8]} -> {_after[:8]}")
        check("J2   and the entity reads back straight away", call("GET", "/nodes/pubfail")[0] == 200)
        with _u2.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=5) as r: _h = json.load(r)
        # The one operator-facing signal: the screen's bar reads exactly this comparison.
        check("J3 healthz shows the published tree behind the repository",
              _h.get("head") and _h.get("head") != _h.get("published"),
              f"head={str(_h.get('head'))[:8]} published={str(_h.get('published'))[:8]}")
    finally:
        os.chmod(_pub, 0o755)
    call("POST", "/nodes", {"id": "pubok", "name": "Pub Ok", "region": "names",
                            "kind": "system", "one_liner": "x", "content": "y"})
    with _u2.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=5) as r: _h = json.load(r)
    check("J4 the next successful write catches the checkout up",
          _h.get("head") == _h.get("published"),
          f"head={str(_h.get('head'))[:8]} published={str(_h.get('published'))[:8]}")

# ── K. two processes on one data directory ────────────────────────────────────
# The writer's lock was a threading lock, so it held only inside one process, while the transaction it
# guards is a sequence of git commands on a shared working tree. Twelve concurrent creates split
# across two processes, before: eight refused as "someone edited the repository by hand" (nobody had —
# the dirty-tree guard cannot tell another writer's half-finished transaction from a hand edit), two
# 500s from git's own index.lock, two callers told their write failed while `git add -A` committed it
# under the other process's message, and the tree left dirty with a file staged and never committed —
# a state in which every later write is refused until a human runs git. The service wedges itself.
#
# Nobody is meant to run two. They will: `--scale ontology=2`, a second install on the same mount, a
# container left behind by a rebuild. None of the damage above looks like a race from the outside.
import concurrent.futures as _cf                                          # noqa: E402
from collections import Counter as _Counter                               # noqa: E402

_P2 = PORT + 1
_env2 = {**env, "PORT": str(_P2), "ONTOLOGY_PUBLISH": os.path.join(T, "publish2")}
procs.append(subprocess.Popen([sys.executable, SERVER],
                              env=_env2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for _ in range(80):
    try: _u2.urlopen(f"http://127.0.0.1:{_P2}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)


def _call_on(port, body):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/nodes", data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json",
                                                         "X-Actor": f"p{port}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return r.status
    except urllib.error.HTTPError as e: e.read(); return e.code
    except Exception: return 0


_N = 12
with _cf.ThreadPoolExecutor(max_workers=_N) as _ex:
    _out = list(_ex.map(lambda i: _call_on(PORT if i % 2 == 0 else _P2,
                                           {"id": f"race-{i}", "name": f"Race {i}", "region": "names",
                                            "kind": "system", "one_liner": "x", "content": "y"}), range(_N)))
_said_ok = sum(1 for st in _out if st in (200, 201))
_on_disk = len([f for f in os.listdir(os.path.join(repo, "regions", "names")) if f.startswith("race-")])
_dirty = subprocess.run(["git", "-C", repo, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
check("K1 every write across two processes succeeds", _said_ok == _N, f"{dict(_Counter(_out))}")
# The one that matters. A caller told "failed" for a write that was committed is the same lie as the
# publish case, and here it was the *other* process's `git add -A` that committed it.
check("K1   and what was reported matches what is on disk", _said_ok == _on_disk,
      f"said ok {_said_ok}, on disk {_on_disk}")
check("K2 the tree is not left dirty", _dirty == "", _dirty[:80])
check("K2   and the repository is still valid", call("POST", "/validate", {})[1].get("ok") is True)

# Waiting is bounded: a writer wedged for good must not turn every later request into a hung socket.
sys.path.insert(0, SERVICE_PARENT)
from service.write import repo_lock, WriteError as _WE                    # noqa: E402
with repo_lock(__import__("pathlib").Path(repo)):
    _t0 = time.monotonic()
    try:
        with repo_lock(__import__("pathlib").Path(repo), wait=0.5): _msg = None
    except _WE as e: _msg = str(e)
    _took = time.monotonic() - _t0
check("K3 a held lock gives up rather than hanging", _msg is not None and _took < 5, f"{_took:.2f}s")
check("K3   and says a process is holding it, not that someone edited by hand",
      _msg and "another process" in _msg, repr(_msg)[:100])

sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
