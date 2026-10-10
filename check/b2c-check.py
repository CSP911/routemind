#!/usr/bin/env python3
"""What a non-expert meets on the screen, against a real ontology — the 2026-10-10 B2C pass.

    ./check/b2c-check.py [port]

Each of these was a person stuck, or data lost, found by walking the screen's own calls:

  size        the 121st entity and the 26th child were refused ("budget exceeded", in English); a
              budget is a warning now, and the write goes through
  names       one name anywhere in the tree: a second "Overview" under another desk was refused; the
              rule holds among siblings only
  overwrite   "new data" used the edit PUT, so a taken name replaced that document; create_only refuses
  the queue   a conflict read "apply failed", a gone target likewise; a proposal for nothing was filed;
              a rejection replaced the proposer's reason
  refusals    the common ones carry a reason the screen translates, instead of English
  stale sets  a set rewording a line applied although the table under it had changed since its base
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18270
results = []
def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:220]}"))

T = tempfile.mkdtemp(prefix="b2c-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "examples", "back-office"), repo)
def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()
for cmd in (["init", "-q"], ["config", "user.email", "b@r"], ["config", "user.name", "b2c"], ["add", "-A"], ["commit", "-qm", "example"]):
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
                               method=method, headers={"Content-Type": "application/json", "X-Knowledge-Actor": "b2c"})
    try:
        with urllib.request.urlopen(r, timeout=60) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}

try:
    # ── size: past the budget, a warning and the write ────────────────────────
    st, v = call("GET", "/v1/validate"); n0 = v["stats"]["nodes"]
    vocab = open(os.path.join(repo, "vocab.yaml"), encoding="utf-8").read()
    cap = int([l for l in vocab.splitlines() if l.strip().startswith("entities:")][0].split(":")[1])
    st, d = call("POST", "/v1/nodes", {"name": "Bulk", "one_liner": "where the check fills", "region": "expense", "parent": "expense"})
    for i in range(max(0, cap - n0) + 1):
        st, d = call("PUT", f"/v1/nodes/bulk/files/b{i}.md", {"content": f"# B{i}\n\nbody\n", "description": f"bulk document {i}"})
        if st >= 300: break
    st, v = call("GET", "/v1/validate")
    check("past the entity budget, a write still goes through — the budget is a warning", st == 200 and v["stats"]["nodes"] > cap and v["ok"]
          and any("budget exceeded: entities" in w for w in v["warnings"]), f"nodes {v['stats']['nodes']} cap {cap} ok {v['ok']}")
    check("  and so does a child past the per-table budget", any("budget exceeded: children of bulk" in w for w in v["warnings"]) or v["stats"]["nodes"] - n0 < 27,
          [w for w in v["warnings"] if "children" in w][:2])

    # ── names: siblings, not the tree ─────────────────────────────────────────
    st, a = call("POST", "/v1/nodes", {"id": "ovw-a", "name": "Overview", "one_liner": "this desk's overview", "region": "expense", "parent": "expense"})
    st2, b = call("POST", "/v1/nodes", {"id": "ovw-b", "name": "Overview", "one_liner": "another desk's overview", "region": "payroll", "parent": "payroll"})
    check("the same name under two different holders is allowed", st == 201 and st2 == 201, f"{st} {st2} {json.dumps(b)[:160]}")
    st3, c = call("POST", "/v1/nodes", {"id": "ovw-c", "name": "overview", "one_liner": "a sibling spelled the same", "region": "expense", "parent": "expense"})
    check("  while two siblings spelled alike are refused", st3 == 422, f"{st3} {json.dumps(c)[:160]}")

    # ── overwrite: a new document never replaces one ──────────────────────────
    st, d = call("PUT", "/v1/nodes/bulk/files/b0.md", {"content": "# OVERWRITE\n", "description": "new upload", "create_only": True})
    body = call("GET", "/v1/nodes/b0")[1].get("body") or ""
    check("a new document under a taken name is refused, and the old one is untouched", st == 409 and d.get("reason") == "file_exists"
          and "OVERWRITE" not in body, f"{st} {json.dumps(d)[:160]}")
    st, d = call("PUT", "/v1/nodes/bulk/files/fresh.md", {"content": "# Fresh\n\nbody\n", "description": "a fresh one", "create_only": True, "name": "Fresh one"})
    check("  a new name goes through, keeps its typed name, and the answer says the id it got", st == 200 and d.get("id") == "fresh"
          and call("GET", "/v1/nodes/fresh")[1].get("name") == "Fresh one", json.dumps(d)[:160])

    # ── the queue says what happened ──────────────────────────────────────────
    cur = call("GET", "/v1/regions/expense")[1]["use_when"]
    st, p1 = call("POST", "/v1/curator/proposals", {"scope": "bb", "region": "expense", "before": cur, "after": "receipts · cards · trips — first wording", "why": "one"})
    st, p2 = call("POST", "/v1/curator/proposals", {"scope": "bb", "region": "expense", "before": cur, "after": "receipts · cards · trips — second wording", "why": "two"})
    call("POST", f"/v1/curator/proposals/{p1['id']}/accept", {"why": "ok"})
    st, d = call("POST", f"/v1/curator/proposals/{p2['id']}/accept", {"why": "ok"})
    check("accepting a proposal whose line moved meanwhile is a named conflict that shows the current line", st == 409
          and d.get("reason") == "conflict" and "first wording" in json.dumps(d), f"{st} {json.dumps(d)[:200]}")
    st, d = call("POST", f"/v1/curator/proposals/{p1['id']}/accept", {"why": "again"})
    check("  accepting one already decided says so, by name", st == 409 and d.get("reason") == "already_decided", f"{st} {json.dumps(d)[:160]}")
    st, d = call("POST", "/v1/curator/proposals", {"scope": "entity", "entity": "never-existed", "after": "x", "why": "x"})
    check("  a proposal for something that does not exist is refused when filed", st == 404 and d.get("reason") == "target_missing", f"{st} {json.dumps(d)[:160]}")
    st, p3 = call("POST", "/v1/curator/proposals", {"scope": "entity", "entity": "ovw-a", "after": "rewritten", "why": "proposer's own reason"})
    call("DELETE", "/v1/nodes/ovw-a")
    st, d = call("POST", f"/v1/curator/proposals/{p3['id']}/accept", {"why": "ok"})
    check("  accepting one whose target was deleted says the target is gone", st == 409 and d.get("reason") == "target_missing", f"{st} {json.dumps(d)[:160]}")
    st, p4 = call("POST", "/v1/curator/proposals", {"scope": "entity", "entity": "ovw-b", "after": "rewritten", "why": "the proposer's reason"})
    call("POST", f"/v1/curator/proposals/{p4['id']}/reject", {"why": "the reviewer's reason"})
    got = next((x for x in call("GET", "/v1/curator/proposals?status=rejected")[1]["proposals"] if x["id"] == p4["id"]), {})
    check("  a rejection keeps the proposer's reason and records the reviewer's beside it", got.get("why") == "the proposer's reason"
          and got.get("decided_why") == "the reviewer's reason", json.dumps(got)[:200])

    # ── refusals carry a reason the screen translates ─────────────────────────
    named = {
        "region_exists": call("POST", "/v1/regions", {"source": "expense", "representative": {"name": "E", "one_liner": "e", "use_when": "e"}}),
        "bad_area_name": call("POST", "/v1/regions", {"source": "it-", "representative": {"name": "E", "one_liner": "e", "use_when": "e"}}),
        "region_not_empty": call("DELETE", "/v1/regions/payroll"),
        "move_into_itself": call("PUT", "/v1/nodes/expense-overview" if call("GET", "/v1/nodes/expense-overview")[0] == 200 else "/v1/nodes/bulk", {"parent": "b1"}),
        "parent_missing": call("PUT", "/v1/nodes/bulk", {"parent": "no-such-holder"}),
    }
    for want, (st, d) in named.items():
        if want == "move_into_itself" and d.get("reason") != want:
            st, d = call("PUT", "/v1/nodes/bulk", {"parent": "b1"})
        check(f"refusal named: {want}", st >= 400 and d.get("reason") == want, f"{st} {json.dumps(d)[:160]}")

    # ── a set rewording a line is stale when the table under it changed ───────
    base = git("rev-parse", "HEAD")
    call("POST", "/v1/nodes", {"name": "Came later", "one_liner": "a child added after the base", "region": "expense", "parent": "bulk"})
    st, d = call("POST", "/v1/changes", {"why": "on an old table", "base": base, "decisions": [
        {"op": "reword", "id": "bulk", "field": "one_liner", "after": "where the check fills — reworded"},
        {"op": "keep", "id": "expense", "field": "use_when"}]})
    check("a set rewording a line whose table gained a child since its base is stale", st == 409 and d.get("reason") == "stale", f"{st} {json.dumps(d)[:200]}")
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
