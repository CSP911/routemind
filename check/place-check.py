#!/usr/bin/env python3
"""Placing a document by walking the table — the pure rules, then the whole walk through the MCP.

    ./check/place-check.py

Two halves. The first runs `service.place` on lines written here: which words of a document count,
which rows they land on, and the one rule that decides how far up a new document is advertised —
stop at the first ancestor whose line already covers it. The second starts an ontology on a copy of
the shipped corpus and drives `knowledge_place` over stdio the way an agent would: open, read hop 0,
step into the area the evidence points at, step again or stop, `here` — then reads back what was
written and what was queued, and checks that the two agree with the walk. A pick the table did not
print is refused; `none` at hop 0 writes nothing and asks for an area.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.place import terms, evidence, coverage, propagation           # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# ── 1. the words of a document ───────────────────────────────────────────────
doc = {"name": "Overseas vendor registration", "one_liner": "How to register a vendor based abroad with no Korean business number",
       "aliases": ["해외 거래처", {"name": "foreign supplier", "scope": "kr"}]}
t = terms(doc)
check("terms come from name, line and aliases", {"Overseas", "vendor", "registration", "register", "abroad"} <= set(t), str(t))
check("  stopwords are dropped", not ({"How", "to", "a", "with", "no"} & set(t)), str(t))
check("  an alias is kept whole, scoped or not", "해외 거래처" in t and "foreign supplier" in t, str(t))
check("  a Latin name wearing a Hangul particle is the name", "ATL" in terms({"name": "ATL에서 반납", "one_liner": ""}),
      str(terms({"name": "ATL에서 반납", "one_liner": ""})))
check("  one word once, whatever its case", [x.lower() for x in t].count("vendor") == 1, str(t))

# ── 2. evidence on a row ──────────────────────────────────────────────────────
ev = evidence(doc, "how far up this amount has to be approved · how to register a new vendor · how many quotes", ["procurement", "PROCUREMENT"])
check("evidence names the words found in the line", set(ev["terms"]) == {"vendor", "register"}, str(ev))
check("  and none in the names here", ev["names"] == [] and ev["hits"] == 2, str(ev))
ev = evidence(doc, "what counts as evidence for a spend", ["expense", "EXPENSE"])
check("  a row that shares nothing says so", ev["hits"] == 0, str(ev))
ev = evidence({"name": "x", "one_liner": "y", "aliases": ["foreign supplier"]}, "", ["vendor", "Foreign supplier"])
check("  an alias hitting a row's own name counts", ev["names"] == ["foreign supplier"] and ev["hits"] == 1, str(ev))

# ── 3. coverage, and how far up it goes ───────────────────────────────────────
c = coverage(doc, "how to register a new vendor")
check("a line with one of the words covers", c["covered"] and "vendor" in c["hits"], str(c))
check("  a line with none does not", not coverage(doc, "leave, parental leave, and time worked")["covered"])

anc = [{"scope": "entity", "id": "vendor-steps", "label": "Vendor steps", "line": "the steps, in order"},
       {"scope": "entity", "id": "vendor", "label": "Vendor", "line": "registering a vendor and keeping it registered"},
       {"scope": "bb", "id": "procurement", "label": "PROCUREMENT", "line": "how to register a new vendor"}]
p = propagation(doc, anc)
check("propagation stops at the first ancestor whose line covers it", p["stop_at"] and p["stop_at"]["label"] == "Vendor", str(p["stop_at"]))
check("  and proposes only for the ancestors below it", [q["label"] for q in p["proposals"]] == ["Vendor steps"], str(p["proposals"]))
check("  a node's proposal is scope entity, naming the node",
      p["proposals"][0]["scope"] == "entity" and p["proposals"][0]["entity"] == "vendor-steps", str(p["proposals"][0]))
check("  widened by the document's own line", p["proposals"][0]["after"] == "the steps, in order · " + doc["one_liner"], p["proposals"][0]["after"])
check("  and does not reach hop 0", not p["reaches_hop0"])

strange = {"name": "Zorbulant calibration", "one_liner": "Zorbulant units are recalibrated every quarter", "aliases": []}
p = propagation(strange, anc)
check("nothing covers it: every ancestor is proposed, up to the area", [q["scope"] for q in p["proposals"]] == ["entity", "entity", "bb"], str(p))
check("  the area's proposal is scope bb, naming the region", p["proposals"][-1]["region"] == "procurement")
check("  and it reaches hop 0", p["reaches_hop0"] and p["stop_at"] is None)
p = propagation(strange, [])
check("no ancestors: nothing proposed, nothing reached", p["proposals"] == [] and not p["reaches_hop0"])

# ── 4. the whole walk, through the MCP, on a copy of the shipped corpus ───────
PORT = int(os.environ.get("PLACE_CHECK_PORT") or 18120)
tmp = tempfile.mkdtemp(prefix="place-check-")
repo = os.path.join(tmp, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, symlinks=True)
subprocess.run(["git", "-C", repo, "config", "user.email", "check@routemind"], check=True)
subprocess.run(["git", "-C", repo, "config", "user.name", "place-check"], check=True)
# The proposal queue lives in the harness store; without it the queue answers 501 and `here` can
# place but not advertise. The check needs both halves, so it gives the server one.
os.makedirs(os.path.join(tmp, "harness"), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_HARNESS": os.path.join(tmp, "harness"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(tmp, "svc.log"), "w"), stderr=subprocess.STDOUT)


def _end():
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(tmp, ignore_errors=True)


def _log_tail():
    try:
        with open(os.path.join(tmp, "svc.log"), encoding="utf-8", errors="replace") as f:
            return "".join(f.readlines()[-25:])
    except Exception: return "(no server log)"


import atexit; atexit.register(_end)
for _ in range(80):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    # A server that never answered is the one failure the rest of this file cannot explain, and
    # its log is in a directory that is about to be removed. Print it before anything else fails.
    print("\n".join(results)); print(f"\nFAIL the ontology never answered on :{PORT} — its log:\n{_log_tail()}"); sys.exit(1)


def get(path):
    """A read, or the status it refused with — never an exception. A refused read should fail the
    assertion that needed it, with the code in the message, rather than end the run unexplained."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=20) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code} from {path}"}


# Whatever ends this run early, the assertions that already ran are the evidence; print them.
atexit.register(lambda: print("\n".join(results)) if results and not getattr(sys, "_place_check_done", False) else None)


class Mcp:
    """One MCP process over stdio, one call at a time."""
    def __init__(self):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "place-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.n = 0
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "place-check", "version": "0"}}})
        self._recv()
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    def _id(self): self.n += 1; return self.n
    def _send(self, m): self.p.stdin.write(json.dumps(m) + "\n"); self.p.stdin.flush()
    def _recv(self): return json.loads(self.p.stdout.readline())
    def call(self, name, args):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/call", "params": {"name": name, "arguments": args}})
        m = self._recv()
        r = m.get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


m = Mcp()
atexit.register(m.close)
tools_text, _ = m.call("knowledge_place", {"op": "list"})
check("the tool answers", "No placement is open" in tools_text, tools_text[:80])

# A document about vendors, which PROCUREMENT's sentence already covers.
text, err = m.call("knowledge_place", {"op": "open", "name": doc["name"], "one_liner": doc["one_liner"],
                                       "aliases": ["해외 거래처"], "content": "# Overseas vendor registration\n\nWritten 1 October 2026.\n"})
check("open prints hop 0", not err and "/v1/regions/procurement" in text and "/v1/regions/expense" in text, text[:200])
pid = text.split("[", 1)[1].split("]", 1)[0] if "[" in text else ""
check("  with a placement id", pid.startswith("p"), pid)
row = next((l for l in text.splitlines() if "/v1/regions/procurement" in l), "")
check("  and the procurement row shows the shared words", "vendor" in row and "register" in row, row)
# Not "every other row shares nothing": ATTENDANCE and EXPENSE both say "business trip", and the
# document says "business number", so they honestly share one word. The property is that the
# right area shares strictly more than any other — the evidence points, it does not just exist.
def _shares(line):
    cells = [c for c in line.split("  ") if c.strip()]
    return 0 if len(cells) < 2 or cells[1].strip() == "—" else len(cells[1].split(","))
hop0 = {l.split()[0]: _shares(l) for l in text.splitlines() if l.strip().startswith("/v1/regions/")}
check("  and procurement shares strictly more than any other area",
      hop0.get("/v1/regions/procurement", 0) > max(v for k, v in hop0.items() if k != "/v1/regions/procurement"), str(hop0))

text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/payroll/../procurement"})
check("a pick the table did not print is refused", err and "not an address the last table printed" in text, text[:120])
text, err = m.call("knowledge_place", {"op": "here", "id": pid})
check("`here` at hop 0 is refused", err and "hop 0" in text, text[:120])

text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/procurement"})
check("step into procurement prints its table", not err and "child of procurement in procurement" in text, text[:300])
addrs = [l.split()[0] for l in text.splitlines() if l.strip().startswith("/v1/nodes/")]
check("  with node addresses to descend into", len(addrs) > 0, str(addrs[:5]))
check("  and says PROCUREMENT already covers it", "already covers it" in text and "vendor" in text, text[-300:])
# Descend one more hop if a row shares a word; otherwise place under the representative.
shared = [l.split()[0] for l in text.splitlines() if l.strip().startswith("/v1/nodes/") and "vendor" in l.lower()]
if shared:
    text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": shared[0]})
    check(f"step into {shared[0]} works", not err and "child of" in text, text[:200])
walked_to = shared[0] if shared else "/v1/regions/procurement"

before = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
text, err = m.call("knowledge_place", {"op": "here", "id": pid})
check("`here` places it", not err and text.startswith("PLACED"), text[:200])
nid = text.split(" as ", 1)[1].split(",", 1)[0] if " as " in text else ""
node = get(f"/v1/nodes/{nid}") if nid else {}
check("  the node exists afterwards", bool(node.get("id")), str(node)[:120])
parent_expected = walked_to.rsplit("/", 1)[1] if walked_to.startswith("/v1/nodes/") else "procurement"
check("  under the parent the walk reached", node.get("parent") == parent_expected, f"parent={node.get('parent')!r} expected {parent_expected!r}")
check("  carrying the alias people use", "해외 거래처" in json.dumps(node, ensure_ascii=False))
after = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
check("  no bb proposal: the area's sentence already said vendor", not any("PROCUREMENT (bb)" in l for l in text.splitlines()), text)
check("  the walk is on record", "walked  :" in text and "/v1/regions/procurement" in text)
check("  and the placement is closed", "No placement is open" in m.call("knowledge_place", {"op": "list"})[0])

# A document nothing advertises: placed, and proposals climb to hop 0.
text, err = m.call("knowledge_place", {"op": "open", "name": strange["name"], "one_liner": strange["one_liner"],
                                       "content": "# Zorbulant\n\nWritten 1 October 2026.\n"})
pid = text.split("[", 1)[1].split("]", 1)[0]
check("a document no sentence covers: every row shares nothing", all("—" in l for l in text.splitlines() if l.strip().startswith("/v1/regions/")), text[:400])
text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/procurement"})
check("  inside the area it says nothing above covers it", "nothing above covers it" in text and "reaches hop 0" in text, text[-300:])
check("  and reports export: no, unchanged", "export: no" in text, text[-200:])
before = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
text, err = m.call("knowledge_place", {"op": "here", "id": pid})
check("  placed under the representative", not err and "child of procurement" in text, text[:200])
after = {q["id"] for q in get("/v1/curator/proposals").get("proposals") or []}
new = after - before
check("  one proposal queued — the area's hop-0 sentence", len(new) == 1 and "PROCUREMENT (bb)" in text, text)
q = next((q for q in get("/v1/curator/proposals").get("proposals") or [] if q["id"] in new), {})
check("  scope bb on procurement, widened by the document's line",
      q.get("scope") == "bb" and q.get("region") == "procurement" and str(q.get("after", "")).endswith(strange["one_liner"]), str(q)[:200])
check("  and not applied: the sentence at hop 0 is unchanged",
      not str(next(r for r in get("/v1/regions")["regions"] if r["source"] == "procurement")["use_when"]).endswith(strange["one_liner"]))
check("  export was not touched", not next(r for r in get("/v1/regions")["regions"] if r["source"] == "procurement").get("export"))

# `none` at hop 0: nothing written, an area asked for.
text, err = m.call("knowledge_place", {"op": "open", "name": "Pigeon loft rota", "one_liner": "Who feeds the pigeons on which day"})
pid = text.split("[", 1)[1].split("]", 1)[0]
n_before = len(get("/v1/nodes")["nodes"])
text, err = m.call("knowledge_place", {"op": "step", "id": pid, "pick": "none"})
check("`none` at hop 0 asks for a new area and writes nothing",
      not err and "new area" in text and "Nothing was written" in text and len(get("/v1/nodes")["nodes"]) == n_before, text[:200])
check("  offering the document's own line as the sentence", "Who feeds the pigeons" in text)

sys._place_check_done = True
print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
