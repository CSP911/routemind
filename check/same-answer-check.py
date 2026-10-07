#!/usr/bin/env python3
"""Invariant 4: every reader of one fact gets the same answer.

    ./check/same-answer-check.py [port]

Not a feature check. A table: each **fact** the repository holds — an area's routing sentence, whether
it is exported, who speaks for it; a node's name, line, kind, parent, aliases, body; the edges; the
core — against every **path** that reads it: the file (the one home, invariant 3), the API's listing
and detail, the parent's table, the export surface a peer reads, the placement walk,
and what the MCP prints to an agent. Every pair must agree. A disagreement is a bug by definition,
whichever side is "right", because a reader cannot tell which side it is on.

Measured 2026-10-05 before this existed: `store.regions()` read the files and `store.regions_json()`
read a committed table, and after a hand edit the two answered the same question differently — hop 0
showed one thing, the export surface another, and nothing compared them. This compares them, on a
clean tree and then again with an uncommitted hand edit in it, where the two homes are furthest
apart.

What the MCP prints is compared by prefix: the table clips a long line with `…`, and a clipped line
is the same fact, shortened, not a different one. The clip itself is noted in the output, because
an agent is a reader too and the length it is shown is a fact about this system.
"""
import json, os, re, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
import yaml                                                              # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18200
TOKEN = "same-answer-enrolment-key"
results, mismatches = [], []
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def same(fact, a_name, a, b_name, b, prefix=False):
    """One cell of the table. `prefix`: b may be a clipped rendering of a."""
    if prefix:
        bb = str(b or "").rstrip("…").strip()
        ok = str(a or "").strip().startswith(bb) if bb else not str(a or "").strip()
    else:
        ok = a == b
    if not ok: mismatches.append((fact, a_name, a, b_name, b))
    return ok


def get(path, token=None, raw=False):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", headers={"X-Peer-Token": token} if token else {})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            return r.status, (body.decode("utf-8") if raw else json.loads(body or b"{}"))
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


def post(path, body):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "X-Knowledge-Actor": "same-answer"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())


def session():
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/peers/token", data=b"", method="POST", headers={"X-Peer-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read())["token"]


class Mcp:
    def __init__(self):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "same-answer"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.n = 0
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "same-answer", "version": "0"}}})
        self._recv(); self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    def _id(self): self.n += 1; return self.n
    def _send(self, m): self.p.stdin.write(json.dumps(m) + "\n"); self.p.stdin.flush()
    def _recv(self): return json.loads(self.p.stdout.readline())
    def call(self, name, args):
        self._send({"jsonrpc": "2.0", "id": self._id(), "method": "tools/call", "params": {"name": name, "arguments": args}})
        r = self._recv().get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    def close(self):
        try: self.p.stdin.close(); self.p.wait(5)
        except Exception: self.p.kill()


def files(repo):
    """The one home: every node's frontmatter and body, straight from disk."""
    out = {}
    for root, _, names in os.walk(os.path.join(repo, "regions")):
        for n in names:
            if not n.endswith(".md"): continue
            p = os.path.join(root, n)
            m = FM.match(open(p, encoding="utf-8").read())
            if not m: continue
            fm = yaml.safe_load(m.group(1)) or {}
            fm["_body"] = m.group(2); fm["_area"] = os.path.relpath(root, os.path.join(repo, "regions")).split(os.sep)[0]
            out[fm.get("id") or n[:-3]] = fm
    return out


def yesno(v):
    return v if isinstance(v, bool) else (str(v).strip().lower() in ("yes", "true") if v is not None else False)


def table_rows(text):
    """`address → why` as the MCP printed them, with the ADDRESS/WHY columns of a table."""
    rows = {}
    for l in text.splitlines():
        parts = l.split()
        if len(parts) >= 2 and parts[0] in ("table", "file", "empty") and parts[1].startswith("/v1/"):
            # why is everything after the age column; find it by locating the address and the
            # age token, then taking the rest
            rest = l.split(parts[1], 1)[1].strip()
            rest = re.sub(r"^\S+ / \S+\s+", "", rest)      # the AGE column, `3y / 2d`
            rest = re.sub(r"^(ours|copied|theirs)\s+", "", rest)
            rows[parts[1]] = rest.strip()
    return rows


def compare(repo, label):
    """The whole table once, for the repository as it stands now."""
    F = files(repo)
    areas = sorted(d for d in os.listdir(os.path.join(repo, "regions")) if os.path.isdir(os.path.join(repo, "regions", d)))
    rep_of = {a: next((i for i, f in F.items() if f["_area"] == a and f.get("role") == "representative" and not f.get("parent")), None) for a in areas}
    n_cells = 0

    # ── area facts ────────────────────────────────────────────────────────────
    st, listing = get("/v1/regions"); rows = {r["source"].replace("_", "-"): r for r in listing.get("regions", []) if not r.get("peer")}
    st, exported = get("/v1/export/regions", session()); ex = {r["source"].replace("_", "-"): r for r in exported.get("regions", [])}
    placed = post("/v1/place", {"at": "/v1/regions", "doc": {"name": "x", "one_liner": "x"}, "path": []}); pl = {r["id"]: r for r in placed.get("rows", [])}
    m = Mcp(); hop0, _ = m.call("knowledge_table", {}); printed = table_rows(hop0)
    for a in areas:
        rep = rep_of[a]; f = F.get(rep, {})
        st, detail = get(f"/v1/regions/{a}")
        use_when = (f.get("use_when") or "").strip()
        for name, val, pre in [("listing", rows.get(a, {}).get("use_when"), False), ("detail", detail.get("use_when"), False),
                               ("place", pl.get(a, {}).get("line"), False),
                               ("mcp hop0", printed.get(f"/v1/regions/{a}"), True)]:
            n_cells += 1; same(f"area {a} use_when", "file", use_when, name, (val or "").strip() if val is not None else val, prefix=pre)
        if yesno(f.get("export")):
            n_cells += 1; same(f"area {a} use_when", "file", use_when, "export surface", (ex.get(a, {}).get("use_when") or "").strip())
            n_cells += 1; same(f"area {a} crosses", "file", True, "export surface", a in ex)
        else:
            n_cells += 1; same(f"area {a} crosses", "file", False, "export surface", a in ex)
        n_cells += 1; same(f"area {a} export", "file", yesno(f.get("export")), "detail", bool(detail.get("export")))
        n_cells += 1; same(f"area {a} representative", "file", rep, "listing", rows.get(a, {}).get("representative"))
        n_cells += 1; same(f"area {a} representative", "file", rep, "detail", detail.get("representative"))
        n_cells += 1; same(f"area {a} title", "file", f.get("name"), "listing", rows.get(a, {}).get("title"))

    # ── node facts ────────────────────────────────────────────────────────────
    st, nodes = get("/v1/nodes"); N = {n["id"]: n for n in nodes.get("nodes", [])}
    n_cells += 1; same("the set of nodes", "files", sorted(F), "listing", sorted(N))
    sample = sorted(F)[:: max(1, len(F) // 24)]          # two dozen spread across the tree, plus every representative
    sample = sorted(set(sample) | {r for r in rep_of.values() if r})
    for i in sample:
        f = F[i]; st, d = get(f"/v1/nodes/{i}")
        for fact, fv, key in [("name", f.get("name"), "name"), ("one_liner", f.get("one_liner"), "one_liner"),
                              ("kind", f.get("kind"), "kind"), ("parent", f.get("parent"), "parent")]:
            n_cells += 1; same(f"node {i} {fact}", "file", fv, "listing", N.get(i, {}).get(key))
            if key in d: n_cells += 1; same(f"node {i} {fact}", "file", fv, "detail", d.get(key))
        aliases = [x["name"] if isinstance(x, dict) else str(x) for x in (f.get("aliases") or [])]
        n_cells += 1; same(f"node {i} aliases", "file", aliases, "listing", [x["name"] if isinstance(x, dict) else str(x) for x in (N.get(i, {}).get("aliases") or [])])
        # the row this node is, in its parent's table — the line an agent reads
        par = f.get("parent")
        if par:
            st, pd = get(f"/v1/nodes/{par}")
            row = next((c for c in (pd.get("children") or []) if c.get("id") == i), None)
            if row is not None:
                n_cells += 1; same(f"node {i} one_liner", "file", f.get("one_liner"), "parent's table", row.get("one_liner"))
            placed = post("/v1/place", {"at": f"/v1/nodes/{par}", "doc": {"name": "x", "one_liner": "x"}, "path": [f"/v1/nodes/{par}"]})
            prow = next((r for r in placed.get("rows", []) if r["id"] == i), None)
            if prow is not None:
                n_cells += 1; same(f"node {i} one_liner", "file", f.get("one_liner"), "place rows", prow.get("line"))
            t, err = m.call("knowledge_table", {"path": f"/v1/nodes/{par}", "why": "the check walks here"})
            pr = table_rows(t)
            addr = next((k for k in pr if k.rstrip("/body").endswith(f"/v1/nodes/{i}") or k == f"/v1/nodes/{i}/body" or k == f"/v1/nodes/{i}"), None)
            if addr:
                n_cells += 1; same(f"node {i} one_liner", "file", f.get("one_liner"), "mcp table", pr[addr].split(" — ", 1)[-1] if " — " in pr[addr] else pr[addr], prefix=True)
        body = (f.get("_body") or "").strip()
        if body:
            st, api_body = get(f"/v1/nodes/{i}/body", raw=True)
            n_cells += 1; same(f"node {i} body", "file", body, "api body", (api_body or "").strip())
            t, err = m.call("knowledge_read", {"path": f"/v1/nodes/{i}/body", "why": "the check walks here"})
            n_cells += 1; same(f"node {i} body", "file", body, "mcp read", (t or "").strip()[:len(body)], prefix=True)
    m.close()

    # ── edges and core ────────────────────────────────────────────────────────
    ef = yaml.safe_load(open(os.path.join(repo, "edges.yaml"), encoding="utf-8")) or []
    st, ea = get("/v1/edges"); st, g = get("/v1/graph")
    # The graph names its ends `s` and `t`; the fact is the triple, not the field names.
    key = lambda e: (e.get("from", e.get("s")), e.get("rel"), e.get("to", e.get("t")))
    n_cells += 1; same("edges", "file", sorted(map(key, ef)), "api edges", sorted(map(key, ea.get("edges", []))))
    n_cells += 1; same("edges", "file", sorted(map(key, ef)), "graph", sorted(map(key, g.get("edges", []))))
    st, core = get("/v1/core", raw=True)
    n_cells += 1; same("core", "file", open(os.path.join(repo, "CORE.md"), encoding="utf-8").read(), "api core", core)
    return n_cells


T = tempfile.mkdtemp(prefix="same-answer-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
for cmd in (["init", "-q"], ["config", "user.email", "same@routemind"], ["config", "user.name", "same-answer"], ["add", "-A"], ["commit", "-qm", "as shipped"]):
    subprocess.run(["git", "-C", repo, *cmd], check=True, capture_output=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": TOKEN,
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env, stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    svc.kill(); sys.exit("  the ontology never answered — log:\n" + open(os.path.join(T, "svc.log")).read()[-1500:])

try:
    n1 = compare(repo, "clean"); m1 = list(mismatches)
    check(f"clean tree: every reader agrees ({n1} cells)", not m1)
    # The state where the two homes are furthest apart: a hand edit nobody committed. Nothing may
    # regenerate (the tree is dirty) and every reader must still agree — with the file.
    area = sorted(d for d in os.listdir(os.path.join(repo, "regions")) if os.path.isdir(os.path.join(repo, "regions", d)))[0]
    md = os.path.join(repo, "regions", area, f"{area}.md")
    text = open(md, encoding="utf-8").read()
    open(md, "w", encoding="utf-8").write(text.replace("use_when:", "use_when: EDITED BY HAND ·", 1)
                                           .replace("\nexport: no\n", "\nexport: yes\n", 1) if "\nexport: no\n" in text
                                           else text.replace("use_when:", "use_when: EDITED BY HAND ·", 1))
    mismatches.clear()
    n2 = compare(repo, "hand-edited"); m2 = list(mismatches)
    check(f"with an uncommitted hand edit: every reader still agrees with the file ({n2} cells)", not m2)
    for fact, an, a, bn, b in (m1 + m2)[:12]:
        results.append(f"       {fact}: {an}={str(a)[:60]!r}  vs  {bn}={str(b)[:60]!r}")
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {sum(1 for r in results if r[:4] in ('ok  ', 'FAIL'))}")
sys.exit(1 if n else 0)
