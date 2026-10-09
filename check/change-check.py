#!/usr/bin/env python3
"""A change set: several decisions, one commit, the lines over them decided (docs/CHANGE.md).

    ./check/change-check.py [port]

Against a real ontology on a copy of the shipped repository. What has to hold:

  one commit or none      a set lands as exactly one commit; a set refused anywhere — a line left
                          undecided, a conflict on `before`, a stale base — leaves no commit and a
                          clean tree, even when earlier decisions in it had already written files
  the preview is the write  a dry run returns the same impact and ids and moves nothing
  the cascade is computed   adding under P impacts P's line and nothing above; rewording P's line
                          impacts P's parent; keeping it stops there
  a move impacts both ends  the parent it left and the one it joined; cross-area, both areas' faces,
                          and what newly crosses a circuit must be acknowledged
  decisions, not a script   the same set in another order makes the same impact and the same ids;
                          two decisions on one aspect are refused by name
  the base holds            a file the decisions rest on that moved since `base` is a stale set, and
                          the file is named; unrelated movement is not
  every write nudges        a plain create's result names the line its parent now has over it
  the queue takes a set     with a review queue, a set rewording an area's sentence waits there whole
  the agent's door          through the MCP: a `here` with undecided lines is refused with the lines,
                          and the same `here` with them decided places the document
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18260
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:220]}"))
    return bool(cond)


T = tempfile.mkdtemp(prefix="change-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()
for cmd in (["init", "-q"], ["config", "user.email", "c@r"], ["config", "user.name", "change-check"], ["add", "-A"], ["commit", "-qm", "as shipped"]):
    git(*cmd)
os.makedirs(os.path.join(T, "harness"), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_HARNESS": os.path.join(T, "harness"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    svc.kill(); sys.exit("  the ontology never answered — " + open(os.path.join(T, "svc.log")).read()[-1200:])


def call(method, path, body=None):
    r = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(body).encode() if body is not None else None,
                               method=method, headers={"Content-Type": "application/json", "X-Knowledge-Actor": "change-check"})
    try:
        with urllib.request.urlopen(r, timeout=60) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}


def head(): return git("rev-parse", "HEAD")
def clean(): return git("status", "--porcelain") == ""
def commits_since(h): return int(git("rev-list", "--count", f"{h}..HEAD"))
def change(body, **kw): return call("POST", "/v1/changes", {**body, **kw})
def lines(d): return {f"{l['id']}.{l['field']}": l["decided"] for l in ((d.get("values") or d).get("impact") or {}).get("lines", [])}
def trailer(): return git("log", "-1", "--format=%B")


try:
    # The shipped example: procurement's face holds purchase-request, which holds approval-threshold.
    st, pr = call("GET", "/v1/nodes/purchase-request")
    assert st == 200 and pr.get("parent") == "procurement", pr
    DOC = {"op": "create", "ref": "$doc", "name": "Late-night taxi receipts", "one_liner": "whether a taxi receipt is enough on its own after 22:00",
           "content": "# Taxi receipts\n\nAfter 22:00 a receipt alone is enough.\n", "parent": "purchase-request"}

    # ── one commit or none ────────────────────────────────────────────────────
    h0 = head()
    st, d = change({"why": "taxi receipts", "decisions": [DOC]}, dry_run=True)
    check("a dry run answers 200 with the impact, and moves nothing", st == 200 and d.get("dry_run") is True and commits_since(h0) == 0 and clean()
          and lines(d) == {"purchase-request.one_liner": None} and d.get("applies") is False, f"{st} {json.dumps(d)[:200]}")
    check("  and already names the id the document would get", d.get("ids", {}).get("$doc") == "late-night-taxi-receipts", d.get("ids"))
    st, d = change({"why": "taxi receipts", "decisions": [DOC]})
    check("the same set applied: refused — the line over it is not decided, by name", st == 409 and d.get("reason") == "undecided"
          and "purchase-request.one_liner" in d.get("details", []) and commits_since(h0) == 0 and clean(), f"{st} {json.dumps(d)[:200]}")
    st, d = change({"why": "taxi receipts", "decisions": [DOC, {"op": "keep", "id": "purchase-request", "field": "one_liner", "why": "its line already covers evidence"}]})
    check("with the line kept: one commit, clean tree, the id in the answer", st == 201 and commits_since(h0) == 1 and clean()
          and d.get("revision") == head() and d["ids"]["$doc"] == "late-night-taxi-receipts", f"{st} {json.dumps(d)[:200]}")
    check("  the cascade stopped at the kept line: nothing above it is impacted", lines(d) == {"purchase-request.one_liner": "keep"}, lines(d))
    check("  the decision is in the commit, as a trailer", "Keep: purchase-request.one_liner — its line already covers evidence" in trailer()
          and "Create: late-night-taxi-receipts under purchase-request" in trailer(), trailer())
    check("  and nothing of the set's own is left in the answer as stale", d.get("impacted") == [], d.get("impacted"))

    # ── the cascade climbs as far as the rewording ────────────────────────────
    h0 = head()
    st, d = change({"why": "say receipts", "decisions": [{"op": "reword", "id": "purchase-request", "field": "one_liner",
                                                            "after": "the request, its amount bands, and what counts as evidence — receipts included"}]})
    check("rewording a line impacts its parent's table: the area's face, by its use_when", st == 409 and lines(d) == {"procurement.use_when": None} and commits_since(h0) == 0, f"{st} {lines(d)}")
    st, d = change({"why": "say receipts", "decisions": [{"op": "reword", "id": "purchase-request", "field": "one_liner",
                                                            "after": "the request, its amount bands, and what counts as evidence — receipts included",
                                                            "before": pr["one_liner"]},
                                                           {"op": "keep", "id": "procurement", "field": "use_when"}]})
    check("  kept there, it applies; `before` matched what the line said", st == 201 and commits_since(h0) == 1 and lines(d) == {"procurement.use_when": "keep"}, f"{st} {lines(d)}")
    st, d = change({"why": "say receipts again", "decisions": [{"op": "reword", "id": "purchase-request", "field": "one_liner", "after": "x", "before": pr["one_liner"]},
                                                                 {"op": "keep", "id": "procurement", "field": "use_when"}]})
    check("  a `before` that no longer matches is a conflict, not an overwrite", st == 409 and d.get("reason") == "conflict" and commits_since(h0) == 1, f"{st} {json.dumps(d)[:160]}")

    # ── folding siblings into a holder, and a move impacts both ends ──────────
    st, tbl = call("POST", "/v1/place", {"at": "/v1/regions/procurement"})
    sibs = [r["id"] for r in tbl["rows"] if r["id"] != "purchase-request"][:2]
    h0 = head()
    fold = {"why": "fold the vendor side", "decisions": [
        {"op": "create", "ref": "$h", "name": "Vendors", "one_liner": "everything about the vendor side — custody, registration", "parent": "procurement"},
        {"op": "move", "id": sibs[0], "parent": "$h"}, {"op": "move", "id": sibs[1], "parent": "$h"},
        {"op": "keep", "id": "procurement", "field": "use_when"}]}
    st, d = change(fold, dry_run=True)
    st2, d2 = change({**fold, "decisions": list(reversed(fold["decisions"]))}, dry_run=True)
    diff = [k for k in set(d.get("impact", {})) | set(d2.get("impact", {})) if d.get("impact", {}).get(k) != d2.get("impact", {}).get(k)]
    check("a set is decisions, not a script: in another order, the same impact and the same ids", st == 200 and st2 == 200
          and not diff and d["ids"] == d2["ids"], f"{st} {st2} differ in {diff}: {json.dumps({k: [d['impact'].get(k), d2['impact'].get(k)] for k in diff})[:300]}")
    st, d = change(fold)
    tab = next((t for t in d.get("impact", {}).get("tables", []) if t["owner"] == "procurement"), {})
    check("folding two siblings under a new holder: one commit; the face's table lost two rows and gained the holder", st == 201 and commits_since(h0) == 1
          and {r["id"] for r in tab.get("before", [])} - {r["id"] for r in tab.get("after", [])} == set(sibs)
          and d["ids"]["$h"] in {r["id"] for r in tab.get("after", [])}, f"{st} {json.dumps(tab)[:200]}")
    holder = d.get("ids", {}).get("$h", "?")
    st, n = call("GET", f"/v1/nodes/{sibs[0]}")
    check("  the moved entity keeps its address and now names the holder", st == 200 and n.get("parent") == holder, n.get("parent"))

    # ── two decisions on one aspect ───────────────────────────────────────────
    st, d = change({"why": "twice", "decisions": [{"op": "move", "id": sibs[0], "parent": "procurement"}, {"op": "move", "id": sibs[0], "parent": "purchase-request"}]})
    check("two decisions on one aspect are refused by name, before anything is locked", st == 422 and d.get("reason") == "refused"
          and any(f"{sibs[0]}.parent" in x for x in d.get("details", [])), f"{st} {d.get('details')}")

    # ── cross-area, into an exported area ─────────────────────────────────────
    st, ex = call("PUT", "/v1/nodes/expense", {"export": True})
    assert 200 <= st < 300, ex
    h0 = head()
    mv = {"why": "receipts are an expense matter", "decisions": [
        {"op": "move", "id": "late-night-taxi-receipts", "parent": "expense"},
        {"op": "keep", "id": "purchase-request", "field": "one_liner"}, {"op": "keep", "id": "expense", "field": "use_when"}]}
    st, d = change(mv)
    check("a move into an exported area is refused until the exposure is acknowledged", st == 409 and d.get("reason") == "exposure"
          and d.get("details") == ["late-night-taxi-receipts"] and commits_since(h0) == 0, f"{st} {json.dumps(d)[:160]}")
    st, d = change({**mv, "expose": ["late-night-taxi-receipts"]})
    check("  acknowledged, it applies; both ends' lines were decided; the exposure is in the commit", st == 201 and commits_since(h0) == 1
          and set(lines(d)) == {"purchase-request.one_liner", "expense.use_when"} and "Expose: late-night-taxi-receipts" in trailer(), f"{st} {lines(d)}")
    st, n = call("GET", "/v1/nodes/late-night-taxi-receipts")
    check("  and the entity is in the other area, under its face", st == 200 and n.get("region") == "expense" and n.get("parent") == "expense", f"{n.get('region')} {n.get('parent')}")

    # ── the base ──────────────────────────────────────────────────────────────
    base = head()
    call("PUT", "/v1/nodes/expense", {"use_when": "expenses, receipts and per-diems — now also taxi receipts"})
    st, d = change({"why": "on a stale table", "base": base, "decisions": [
        {"op": "create", "ref": "$x", "name": "Per-diem Tokyo", "one_liner": "the per-diem for Tokyo", "parent": "expense"},
        {"op": "keep", "id": "expense", "field": "use_when"}]})
    check("a set whose base is behind a change to a line it rests on is stale, and the file is named", st == 409 and d.get("reason") == "stale"
          and d.get("details") == ["regions/expense/expense.md"], f"{st} {json.dumps(d)[:160]}")
    h0 = head()
    st, d = change({"why": "elsewhere", "base": base, "decisions": [
        {"op": "create", "ref": "$x", "name": "Per-diem Tokyo", "one_liner": "the per-diem for Tokyo", "parent": "purchase-request"},
        {"op": "keep", "id": "purchase-request", "field": "one_liner"}]})
    check("  while a base behind unrelated movement is fine", st == 201 and commits_since(h0) == 1, f"{st} {json.dumps(d)[:160]}")

    # ── a new area from hop 0, and a delete ───────────────────────────────────
    h0 = head()
    st, d = change({"why": "nothing at hop 0 covers travel", "decisions": [
        {"op": "create", "ref": "$area", "name": "Travel", "one_liner": "travel: booking, per-diems, what to keep", "parent": None, "area": "travel",
         "use_when": "when the question is about a trip — booking it, what it pays, what to keep from it"},
        {"op": "create", "ref": "$doc", "name": "Booking a flight", "one_liner": "how a flight is booked and by whom", "parent": "$area", "content": "# Booking\n\nThrough the desk.\n"}]})
    st2, regs = call("GET", "/v1/regions")
    check("a new area from hop 0, with its first document, in one commit; hop 0 lists it", st == 201 and commits_since(h0) == 1
          and any(r.get("source") == "travel" or r.get("dir") == "travel" for r in regs.get("regions", [])), f"{st} {json.dumps(d)[:160]}")
    st, v = call("GET", "/v1/validate")
    check("  and the repository validates — regions.json was regenerated with it", v.get("ok") is True, (v.get("errors") or [])[:2])
    st, d = change({"why": "drop the holder", "decisions": [{"op": "delete", "id": d["ids"]["$area"]}]})
    check("deleting an area's face through a set is refused", st == 422, f"{st}")
    st, d = change({"why": "drop the folded holder", "decisions": [{"op": "delete", "id": holder}, {"op": "keep", "id": "procurement", "field": "use_when"}]})
    check("deleting a holder that holds nodes is refused and names them", st == 409 and d.get("reason") == "holds_children", f"{st} {json.dumps(d)[:160]}")

    # ── atomicity: files written early in a set are gone when a late decision fails ──
    h0 = head()
    st, d = change({"why": "half of it fails", "decisions": [
        {"op": "create", "ref": "$a", "name": "Half A", "one_liner": "a", "parent": "purchase-request"},
        {"op": "keep", "id": "purchase-request", "field": "one_liner"},
        {"op": "reword", "id": "expense", "field": "use_when", "after": "y", "before": "not what it says"}]})
    check("a set whose last decision fails leaves no commit and no file — the creates before it are gone", st == 409 and commits_since(h0) == 0 and clean()
          and not os.path.exists(os.path.join(repo, "regions", "procurement", "half-a.md")), f"{st} {json.dumps(d)[:120]}")

    # ── every write nudges ────────────────────────────────────────────────────
    st, d = call("POST", "/v1/nodes", {"name": "Plain create", "one_liner": "made with the ordinary call", "region": "procurement", "parent": "purchase-request"})
    check("an ordinary create's result names the line its parent now has over it", st == 201 and [x["id"] for x in d.get("impacted", [])] == ["purchase-request"]
          and d["impacted"][0]["because"] == ["plain-create"], json.dumps(d.get("impacted"))[:200])
    st, d = call("POST", "/v1/nodes", {"name": "Top of the area", "one_liner": "made with no parent, the way the map's + New node does", "region": "procurement"})
    check("  a create with no parent sits under the area's face, so it is the face's line that is nudged", st == 201
          and [x["id"] for x in d.get("impacted", [])] == ["procurement"] and d["impacted"][0]["field"] == "use_when", json.dumps(d.get("impacted"))[:200])
    st, d = call("PUT", "/v1/nodes/plain-create", {"content": "# Plain\n\nA body only.\n"})
    check("  a body-only edit changes no table, so it nudges nothing", st == 200 and d.get("impacted") == [], d.get("impacted"))

    # ── the review queue takes a set whole ────────────────────────────────────
    h0 = head()
    st, d = change({"why": "hop 0 should say receipts", "decisions": [
        {"op": "reword", "id": "procurement", "field": "use_when", "after": "purchases, their approval bands, vendors — and what a request must carry as evidence"}]})
    pid = d.get("queued")
    check("with a review queue, a set rewording an area's sentence is queued whole, not committed", st == 202 and bool(pid) and commits_since(h0) == 0, f"{st} {json.dumps(d)[:160]}")
    st, d = call("POST", f"/v1/curator/proposals/{pid}/accept", {"why": "yes"})
    check("  accepting it applies it as one commit", 200 <= st < 300 and commits_since(h0) == 1 and (d.get("result") or {}).get("revision") == head(), f"{st} {json.dumps(d)[:160]}")

    # ── a queued set accepted after the tree moved is stale, and says so (2026-10-10) ──
    h0 = head()
    st, d = change({"why": "a reword that waits", "decisions": [
        {"op": "create", "ref": "$q", "name": "Queued note", "one_liner": "filed while the sentence waits for review", "parent": "expense",
         "content": "# Queued\n\nbody\n"},
        {"op": "reword", "id": "expense", "field": "use_when", "after": "expenses, receipts, per-diems — and notes filed while a sentence waits"}]})
    qid = d.get("queued")
    call("PUT", "/v1/nodes/expense", {"one_liner": "the expense area, moved on while the set waited"})
    st, d = call("POST", f"/v1/curator/proposals/{qid}/accept", {"why": "late"})
    det = d.get("detail") or {}
    check("a queued set accepted after a file it rests on moved is refused as stale, not as a taken name",
          st == 409 and (det.get("code") == "stale" or "stale" in json.dumps(d) or "changed since" in json.dumps(d)) and "taken" not in json.dumps(d),
          f"{st} {json.dumps(d)[:200]}")

    # ── a document takes its documented siblings' kind; a typed name is kept ──
    st, kids = call("GET", "/v1/nodes/purchase-request")
    sib = [c for c in (kids.get("entries") or []) if c.get("type") != "node"]
    st, d = change({"why": "kind from siblings", "decisions": [
        {"op": "create", "ref": "$k", "name": "Kind probe", "one_liner": "what kind a document gets with none given", "parent": "purchase-request",
         "content": "# Kind\n\nbody\n"}, {"op": "keep", "id": "purchase-request", "field": "one_liner"}]})
    st2, made = call("GET", f"/v1/nodes/{(d.get('ids') or {}).get('$k', 'x')}")
    wanted = {}
    for f in os.listdir(os.path.join(repo, "regions", "procurement")):
        t = open(os.path.join(repo, "regions", "procurement", f), encoding="utf-8").read()
        if "\nparent: purchase-request\n" in t and t.split("---", 2)[2].strip() and "kind-probe" not in f:
            k = [l.split(":", 1)[1].strip() for l in t.splitlines() if l.startswith("kind:")][0]; wanted[k] = wanted.get(k, 0) + 1
    check("a placed document with no kind takes the kind its documented siblings mostly have", st == 201 and wanted
          and wanted.get(made.get("kind"), 0) == max(wanted.values()), f"{made.get('kind')} vs {wanted}")
    st, d = call("PUT", "/v1/nodes/purchase-request/files/gyeonjeok-bigyopyo.md", {"content": "# 견적 비교표\n\n세 곳.\n", "description": "견적을 몇 곳에서 받는지", "name": "견적 비교표"})
    st2, n = call("GET", "/v1/nodes/gyeonjeok-bigyopyo")
    check("a document written with a name keeps it, rather than being called by its address", 200 <= st < 300 and n.get("name") == "견적 비교표", f"{st} {n.get('name')} {json.dumps(d)[:160]}")

    # ── the agent's door ──────────────────────────────────────────────────────
    m = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "agent-c"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    nn = [0]
    def rpc(method, params=None):
        nn[0] += 1; m.stdin.write(json.dumps({"jsonrpc": "2.0", "id": nn[0], "method": method, "params": params or {}}) + "\n"); m.stdin.flush()
        return json.loads(m.stdout.readline())
    def tool(name, a):
        r = rpc("tools/call", {"name": name, "arguments": a}).get("result") or {}
        return (r.get("content") or [{}])[0].get("text", ""), bool(r.get("isError"))
    rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "change-check", "version": "0"}})
    m.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); m.stdin.flush()
    t, err = tool("knowledge_place", {"op": "open", "name": "Vendor onboarding checklist", "one_liner": "the steps before a new vendor may be paid", "content": "# Onboarding\n\n1. W-9.\n"})
    pid = t.split("[", 1)[1].split("]", 1)[0] if "[" in t else ""
    check("mcp: open prints hop 0 and a placement id", not err and pid.startswith("p") and "/v1/regions/procurement" in t, t[:200])
    t, err = tool("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/procurement"})
    check("  step prints the area's table and how `here` works", not err and "a decision for each line over it" in t, t[-300:])
    h0 = head()
    t, err = tool("knowledge_place", {"op": "here", "id": pid, "why": "vendors need a checklist"})
    check("  `here` with the line over it undecided: not written, and the refusal prints the table and the line", not err and t.startswith("NOT WRITTEN")
          and "table of procurement:" in t and "+ vendor-onboarding-checklist" in t and "line procurement.use_when: UNDECIDED" in t and commits_since(h0) == 0, t[:400])
    t, err = tool("knowledge_place", {"op": "here", "id": pid, "why": "vendors need a checklist", "dry_run": True,
                                      "decisions": [{"op": "keep", "id": "procurement", "field": "use_when", "why": "vendors are purchases"}]})
    check("  a dry run with the decision says it applies, and writes nothing", not err and t.startswith("DRY RUN") and "It applies as it is." in t and commits_since(h0) == 0, t[:300])
    t, err = tool("knowledge_place", {"op": "here", "id": pid, "why": "vendors need a checklist",
                                      "decisions": [{"op": "keep", "id": "procurement", "field": "use_when", "why": "vendors are purchases"}]})
    check("  the same `here` with the line decided places it: one commit, the id printed, the decision in the trailer", not err and t.startswith("PLACED")
          and "vendor-onboarding-checklist" in t and commits_since(h0) == 1 and "Keep: procurement.use_when — vendors are purchases" in trailer(), t[:300])
    t, err = tool("knowledge_place", {"op": "list"})
    check("  and the placement is closed", "No placement is open" in t, t)
    # hop 0 says none: the area is made in the same commit as the document
    t, err = tool("knowledge_place", {"op": "open", "name": "Office plants", "one_liner": "who waters the plants and when"})
    pid = t.split("[", 1)[1].split("]", 1)[0]
    t, err = tool("knowledge_place", {"op": "step", "id": pid, "pick": "none"})
    check("  `none` at hop 0 offers to make the area rather than ending the walk", not err and "here {" in t and "area:" in t, t[:300])
    h0 = head()
    t, err = tool("knowledge_place", {"op": "here", "id": pid, "why": "nothing covers the office itself",
                                      "area": {"source": "office", "name": "Office", "one_liner": "the office itself — plants, keys, the kitchen", "use_when": "when the question is about the office as a place: plants, keys, the kitchen"}})
    check("  `here` with `area` makes the area, its sentence and the document in one commit", not err and t.startswith("PLACED") and "$area = office" in t and commits_since(h0) == 1, t[:300])
    # a set the queue takes ends the placement: the agent is not invited to file it again another way
    t, err = tool("knowledge_place", {"op": "open", "name": "Queue probe", "one_liner": "a document whose area sentence is reworded"})
    pid = t.split("[", 1)[1].split("]", 1)[0]
    tool("knowledge_place", {"op": "step", "id": pid, "pick": "/v1/regions/attendance"})
    t, err = tool("knowledge_place", {"op": "here", "id": pid, "why": "probe", "decisions": [
        {"op": "reword", "id": "attendance", "field": "use_when", "after": "leave, attendance and the queue probe"}]})
    t2, _ = tool("knowledge_place", {"op": "list"})
    check("  a set the review queue takes ends the placement and says not to file it again", t.startswith("QUEUED") and "do not file the document again" in t
          and "No placement is open" in t2, t[:300])
    m.stdin.close(); m.wait(5)
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
