#!/usr/bin/env python3
"""Invariant 11: every walk is recorded, and the screen and the agent read the same record.

    ./check/footprint-check.py [port]

Three parts, smallest first.

  the store     `walks.WalkStore` on its own: a step without a reason is refused; two walks
                interleaved come back by cursor in order with none lost and none twice; the counter
                survives a new store on the same directory (a restart); an open walk untouched past
                its hour is closed `abandoned`, a closed one is gone after its six hours; HEAT counts
                walks, not steps; the hot path names the tables walks opened.
  the service   the same through HTTP — POST to open, step and close, GET since=N — and HEAT on the
                tables an agent reads.
  the MCP       an agent's walk through the real MCP server: hop 0 opens a walk on the record, a
                table without `why` is refused, every table and read it makes appears on the record
                in order with its reason, the overlay's close closes the walk, and a second walk
                touching the same name is shown the first one as history.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service import walks                                                # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18280
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


T = tempfile.mkdtemp(prefix="footprint-check-")
try:
    # ── the store ─────────────────────────────────────────────────────────────
    d = Path(T) / "walks"
    st = walks.WalkStore(d)
    a = st.open("how many quotes for 6 million", "knowledge_resolve", {"kind": "agent", "name": "a"})
    b = st.open("who signs a trip request", "knowledge_resolve", {"kind": "agent", "name": "b"})
    try: st.step(a["id"], "table", "/v1/regions/procurement", ""); refused = False
    except walks.WalkError as e: refused = e.status == 400 and "why" in str(e)
    check("a step without a reason is refused", refused)
    st.step(a["id"], "table", "/v1/regions/procurement", "quotes are in its sentence")
    st.step(b["id"], "table", "/v1/regions/attendance", "trips are approved before they start")
    st.step(a["id"], "table", "/v1/nodes/approval-threshold", "the band table")
    st.step(a["id"], "read", "/v1/nodes/threshold-table/body", "the numbers")
    st.step(b["id"], "read", "/v1/nodes/trip-request-form/body", "the form names the approver")
    rows = st.since(0)["steps"]
    ns = [r["n"] for r in rows]
    check("every step comes back by cursor, in order, each once", ns == sorted(ns) and len(ns) == len(set(ns)) == 7, str(ns))
    check("  interleaved walks keep their own steps", [r["walk"] for r in rows if r["op"] != "open"] == [a["id"], b["id"], a["id"], a["id"], b["id"]],
          str([(r["n"], r["walk"][-6:], r["op"]) for r in rows]))
    mid = ns[3]
    later = [r["n"] for r in st.since(mid)["steps"]]
    check("asking from the middle returns exactly what came after", later == ns[4:], f"{later} vs {ns[4:]}")
    st2 = walks.WalkStore(d)
    s = st2.step(b["id"], "table", "/v1/regions/expense", "the allowance side")
    check("a new store on the same directory continues the counter (a restart)", s["n"] == ns[-1] + 1, f"{s['n']} after {ns[-1]}")
    st2.close(a["id"], "answered", "found the band")
    try: st2.step(a["id"], "table", "/v1/regions/expense", "late"); late = False
    except walks.WalkError as e: late = e.status == 409
    check("a closed walk takes no more steps", late)
    h = st2.heat()
    check("HEAT counts walks per row", h.get("procurement") == {"walked": 1, "answered": 1} and h.get("attendance") == {"walked": 1, "answered": 0}, json.dumps(h)[:200])
    st2.step(b["id"], "table", "/v1/regions/attendance", "back again")
    check("  a walk that opened a row twice was there once", st2.heat().get("attendance", {}).get("walked") == 1)
    hot = st2.hot(["threshold-table"])
    check("the hot path names the tables earlier walks opened", hot["walks"] == 1 and hot["paths"][0]["path"] == ["/v1/regions/procurement", "/v1/nodes/approval-threshold"],
          json.dumps(hot))
    # expiry: an open walk an hour stale, a closed one six hours stale
    w = st2.get(b["id"]); w["touched_at"] = "2020-01-01T00:00:00Z"; st2._write(w)
    check("an open walk untouched past its hour is closed abandoned", st2.get(b["id"])["outcome"] == "abandoned")
    w = st2.get(a["id"]); w["closed_at"] = "2020-01-01T00:00:00Z"; st2._write(w)
    gone = False
    try: st2.get(a["id"])
    except walks.WalkError: gone = True
    check("a closed walk is gone after its six hours", gone)

    # ── the service ───────────────────────────────────────────────────────────
    repo = os.path.join(T, "repo")
    shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
    for cmd in (["init", "-q"], ["config", "user.email", "f@r"], ["config", "user.name", "f"], ["add", "-A"], ["commit", "-qm", "as shipped"]):
        subprocess.run(["git", "-C", repo, *cmd], check=True, capture_output=True)
    os.makedirs(os.path.join(T, "ov"), exist_ok=True)
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_WALKS": os.path.join(T, "svc-walks"),
           "ONTOLOGY_OVERLAYS": os.path.join(T, "ov"),
           "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
    svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                           stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)
    else:
        sys.exit("  the ontology never answered — " + open(os.path.join(T, "svc.log")).read()[-1200:])

    def call(method, path, body=None):
        r = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(body).encode() if body is not None else None,
                                   method=method, headers={"Content-Type": "application/json", "X-Knowledge-Actor": "footprint-check"})
        try:
            with urllib.request.urlopen(r, timeout=30) as x: return x.status, json.loads(x.read() or b"{}")
        except urllib.error.HTTPError as e:
            try: return e.code, json.loads(e.read() or b"{}")
            except Exception: return e.code, {}

    try:
        code, o = call("POST", "/v1/walks", {"question": "what counts as a receipt", "how": "check"})
        wid = o.get("id", "")
        check("service: POST opens a walk", code == 201 and wid.startswith("wk_"), f"{code} {o}")
        code, e = call("POST", f"/v1/walks/{wid}/steps", {"op": "table", "address": "/v1/regions/expense"})
        check("  a step without why is refused over HTTP", code == 400 and "why" in e.get("error", ""), f"{code} {e}")
        call("POST", f"/v1/walks/{wid}/steps", {"op": "table", "address": "/v1/regions/expense", "why": "receipts are in its sentence"})
        call("POST", f"/v1/walks/{wid}/steps", {"op": "read", "address": "/v1/nodes/qualified-list/body", "why": "the evidence list"})
        code, r = call("GET", "/v1/walks?since=0")
        ops = [x["op"] for x in r.get("steps", []) if x["walk"] == wid]
        check("  GET since=0 returns the walk's steps in order", ops == ["open", "table", "read"], str(ops))
        code, one = call("GET", f"/v1/walks/{wid}")
        check("  GET one walk returns it whole, for a replay", code == 200 and len(one.get("steps", [])) == 3 and one["steps"][1]["why"] == "receipts are in its sentence")
        call("POST", f"/v1/walks/{wid}/close", {"outcome": "answered"})
        code, area = call("GET", "/v1/regions/expense")
        row = next((x for x in area.get("entries", []) if x["id"] == "qualified-evidence"), None) or {}
        code, top = call("GET", "/v1/regions")
        exp = next((x for x in top.get("regions", []) if x["source"] == "expense"), {})
        check("  HEAT rides on hop 0", exp.get("heat") == {"walked": 1, "answered": 1}, json.dumps(exp.get("heat")))

        # ── the MCP ───────────────────────────────────────────────────────────
        class Mcp:
            def __init__(self):
                self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"), "--api", f"http://127.0.0.1:{PORT}/v1", "--actor", "agent-a"],
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                self.n = 0
                self._send({"jsonrpc": "2.0", "id": self._id(), "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "fp", "version": "0"}}})
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

        def walk_of(text):
            return next((l.split(":", 1)[1].strip().split()[0] for l in text.splitlines() if l.strip().startswith("walk")), "")

        m = Mcp()
        code, before = call("GET", "/v1/walks?since=0"); cursor = before.get("seq", 0)
        t, err = m.call("knowledge_resolve", {"q": "how far up does a purchase have to be approved"})
        w1 = walk_of(t)
        check("mcp: hop 0 opens a walk on the record", w1.startswith("wk_"), w1)
        t, err = m.call("knowledge_table", {"path": "/v1/regions/procurement", "walk": w1})
        check("  a table without why is refused, and says why it wants one", err and "why" in t, t[:140])
        m.call("knowledge_table", {"path": "/v1/regions/procurement", "walk": w1, "why": "approval bands are in its sentence"})
        m.call("knowledge_table", {"path": "/v1/nodes/approval-threshold", "walk": w1, "why": "the band table"})
        m.call("knowledge_read", {"path": "/v1/nodes/threshold-table/body", "walk": w1, "why": "the numbers themselves"})
        code, after = call("GET", f"/v1/walks?since={cursor}")
        mine = [(x["op"], x["address"], x["why"]) for x in after.get("steps", []) if x["walk"] == w1]
        check("  every step it made is on the record, in order, with its reason",
              [x[0] for x in mine] == ["open", "table", "table", "read"] and mine[1][2] == "approval bands are in its sentence", json.dumps(mine)[:300])
        t, err = m.call("knowledge_overlay", {"op": "create", "question": "approval bands", "members": [{"address": "/v1/regions/procurement", "why": "w"}]})
        import re as _re
        oid = (_re.search(r"OVERLAY (ov_[A-Za-z0-9_-]+)", t) or [None, ""])[1]
        m.call("knowledge_overlay", {"op": "close", "id": oid, "outcome": "answered", "used": ["/v1/nodes/threshold-table/body"], "walk": w1})
        code, one = call("GET", f"/v1/walks/{w1}")
        check("  closing the overlay closes the walk on the record", one.get("state") == "closed" and one.get("outcome") == "answered", json.dumps({k: one.get(k) for k in ("state", "outcome")}))
        t, err = m.call("knowledge_resolve", {"q": "the threshold-table for a purchase"})
        w2 = walk_of(t)
        check("  a second walk touching the same name is shown the first as history", "earlier walks touching these names" in t and "procurement" in t, t[:600])
        # HEAT is on the row that was walked, in the table that lists it: approval-threshold is a
        # row of purchase-request, threshold-table a row of approval-threshold.
        t, err = m.call("knowledge_table", {"path": "/v1/nodes/approval-threshold", "walk": walk_of(t), "why": "again"})
        heat_line = next((l for l in t.splitlines() if "threshold-table" in l), "")
        check("  and the table that lists a walked row shows its HEAT", "HEAT" in t and "1/1" in heat_line, (heat_line or t[:300]))
        # A walk the agent never closes is closed by the next question, on the record too.
        m.call("knowledge_resolve", {"q": "who approves a purchase"})
        code, two = call("GET", f"/v1/walks/{w2}")
        check("  an unclosed walk is closed abandoned when the next question starts",
              two.get("state") == "closed" and two.get("outcome") == "abandoned", json.dumps({k: two.get(k) for k in ("state", "outcome")}))
        m.close()
    finally:
        svc.terminate()
        try: svc.wait(5)
        except Exception: svc.kill()
finally:
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
