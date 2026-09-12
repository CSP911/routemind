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
    docker compose exec ontology sh -c 'mkdir -p /tmp/ontology && ln -sfn /app/service /tmp/ontology/service && ln -sfn /app/seed /tmp/seed'
    docker compose exec ontology python3 /tmp/check/scenarios.py
"""
import atexit, json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

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
shutil.copytree(os.path.join(ROOT, "seed"), repo)
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=seed", "-c", "user.email=s@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)

env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT),
       "ONTOLOGY_PUBLISH": os.path.join(T, "publish"),
       "ONTOLOGY_OVERLAYS": os.path.join(T, "overlays"),
       # The review queue is the only path that writes `use_when` (B2), so the curator has to exist.
       "ONTOLOGY_HARNESS": os.path.join(T, "harness")}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
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
sys.path.insert(0, os.path.join(ROOT, "ontology"))
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

sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
