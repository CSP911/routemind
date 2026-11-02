#!/usr/bin/env python3
"""The MCP server against what a client, a `.env` and a far end can hand it — no Docker.

    ./check/mcp-edge-check.py [port]

Starts an ontology on a copy of the shipped repository (one area exported, a circuit key set) and a
few fake far ends that are not RouteMind, then drives the MCP server over stdio the way a client does.
Every assertion is a defect an outside audit found on 2026-11-02 (MC-n in its findings), each of which
either ended the process, answered from somewhere else than the agent was told, or reported a failure
as a result:

  the stream     a JSON-RPC batch or any JSON that is not an object (MC-1), one byte that is not
                 UTF-8 (MC-2) — each ended the process, and with it every tool of the session.
                 `initialize` echoed any protocolVersion it was sent (MC-3)
  the far end    a circuit to something that is not RouteMind was a JSON-RPC internal error and stayed
                 listed on hop 0 (MC-4); --api at such a thing failed `initialize` itself (MC-6); one that
                 accepts and never answers cost 30 s per fetch, initialize included (MC-19)
  .env           not UTF-8 crashed the start (MC-7); a BOM, or a WEB_PORT that is not a port, sent the
                 agent to 8080 — on a machine with a second install, another backbone (MC-8)
  circuits       a node's own document was never printed (MC-5), area sentences were cut (MC-11),
                 refusals came back as results (MC-13), a failed re-open dropped a working circuit (MC-12)
  the tools      ids reused (MC-9), refusals without their reasons (MC-10), odd arguments as internal
                 errors (MC-14), knowledge_read as a GET over all of /v1 (MC-15), a `why` that cannot be
                 encoded silently dropping its step from the footprint (MC-18), a TTL that is not a
                 number (MC-17), and a walk cut off while it was still walking
"""
import http.server, json, os, select, shutil, socket, subprocess, sys, tempfile, threading, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18310
KEY = "edge-check-circuit-key"
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:240]}"))
    return bool(cond)


# ── far ends that are not RouteMind: PORT+1 … PORT+4 ───────────────────────────
def _serve(port, body, ctype):
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _go(self):
            self.send_response(200); self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        do_GET = do_POST = _go
    s = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=s.serve_forever, daemon=True).start()


def _raw(port, banner):
    """Accepts, and either says something that is not HTTP and hangs up, or says nothing at all."""
    ls = socket.socket(); ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); ls.bind(("127.0.0.1", port)); ls.listen()
    held = []
    def run():
        while True:
            c, _ = ls.accept()
            if banner is None: held.append(c); continue
            try: c.recv(4096); c.sendall(banner)
            finally: c.close()
    threading.Thread(target=run, daemon=True).start()


HTML, JLIST, SSH, SILENT = PORT + 1, PORT + 2, PORT + 3, PORT + 4
_serve(HTML, b"<html>hello, not routemind</html>", "text/html")
_serve(JLIST, b"[1, 2, 3]", "application/json")
_raw(SSH, b"SSH-2.0-OpenSSH_9.0\r\n")
_raw(SILENT, None)


# ── the MCP server, as a client drives it ─────────────────────────────────────
class Mcp:
    def __init__(self, api=None, env=None, script=None, init=True):
        e = {k: v for k, v in os.environ.items() if not k.startswith("KNOWLEDGE_")}
        e.update(env or {})
        self.err = tempfile.TemporaryFile()
        self.p = subprocess.Popen([sys.executable, script or os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   *(["--api", api] if api else []), "--actor", "edge-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.err, env=e)
        self.n = 0
        self.init_reply = self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                                  "clientInfo": {"name": "edge-check", "version": "0"}}) if init else None
    def raw(self, line, timeout=40):
        try: self.p.stdin.write((line if isinstance(line, bytes) else line.encode()) + b"\n"); self.p.stdin.flush()
        except (BrokenPipeError, OSError): return {"_": f"the server is gone (rc={self.p.poll()})"}
        r, _, _ = select.select([self.p.stdout], [], [], timeout)
        if not r: return {"_": "no reply"}
        l = self.p.stdout.readline()
        return json.loads(l) if l else {"_": f"the server died (rc={self.p.poll()})"}
    def rpc(self, method, params=None, timeout=40):
        self.n += 1
        return self.raw(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}), timeout)
    def call(self, name, args):
        r = self.rpc("tools/call", {"name": name, "arguments": args})
        if "result" not in r: return f"(not a tool result: {json.dumps(r, ensure_ascii=False)[:200]})", None
        res = r["result"]
        return (res.get("content") or [{}])[0].get("text", ""), bool(res.get("isError"))
    def alive(self):
        return "result" in self.rpc("ping", timeout=10)
    def stderr(self):
        self.err.seek(0); return self.err.read().decode("utf-8", "replace")
    def close(self):
        try: self.p.stdin.close(); self.p.wait(10)
        except Exception: self.p.kill()
        return self.stderr()


def instructions(m):
    return ((m.init_reply or {}).get("result") or {}).get("instructions", "")


# ── an ontology with `expense` exported and a circuit key ──────────────────────
T = tempfile.mkdtemp(prefix="mcp-edge-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
face = os.path.join(repo, "regions", "expense", "expense.md")
src = open(face, encoding="utf-8").read()
open(face, "w", encoding="utf-8").write(src.replace("\nrole: representative\n", "\nrole: representative\nexport: yes\n", 1))
for cmd in (["init", "-q"], ["config", "user.email", "e@r"], ["config", "user.name", "edge"], ["add", "-A"], ["commit", "-qm", "expense exported"]):
    subprocess.run(["git", "-C", repo, *cmd], check=True, capture_output=True)
for d in ("walks", "overlays", "harness"): os.makedirs(os.path.join(T, d), exist_ok=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_PEER_TOKEN": KEY,
       "ONTOLOGY_WALKS": os.path.join(T, "walks"), "ONTOLOGY_OVERLAYS": os.path.join(T, "overlays"),
       "ONTOLOGY_HARNESS": os.path.join(T, "harness"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else:
    svc.kill(); sys.exit("  the ontology never answered — log:\n" + open(os.path.join(T, "svc.log")).read()[-1500:])
API = f"http://127.0.0.1:{PORT}/v1"
SELF = f"http://127.0.0.1:{PORT}"


def get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=10) as r: return json.loads(r.read())


try:
    # ── the stream (MC-1, MC-2, MC-3) ─────────────────────────────────────────
    # One server per kind of line: each of these ended the process, and the next would then be
    # measuring a dead one.
    for line, what in (('[{"jsonrpc":"2.0","id":2,"method":"ping"}]', "a batch"), ("42", "a number"),
                       ('"x"', "a string"), ("null", "null"),
                       (b'{"jsonrpc":"2.0","id":77,"method":"ping","x":"\xff\xfe"}', "a byte that is not UTF-8")):
        m = Mcp(API)
        r = m.raw(line)
        check(f"{what} on the stream is answered, and the server is still there",
              ("error" in r or "result" in r) and m.alive(), r)
        if not isinstance(line, bytes):
            check("  as Invalid Request", (r.get("error") or {}).get("code") == -32600, r)
        m.close()
    m = Mcp(API)
    for asked in ("2099-12-31", "1999-01-01", "garbage"):
        v = (m.rpc("initialize", {"protocolVersion": asked}).get("result") or {}).get("protocolVersion")
        check(f"initialize asked for {asked!r} answers a version this server speaks", v and v != asked and v[:2] == "20", v)
    for asked in ("2024-11-05", "2025-06-18"):
        v = (m.rpc("initialize", {"protocolVersion": asked}).get("result") or {}).get("protocolVersion")
        check(f"  and {asked}, which it speaks, is answered as asked", v == asked, v)

    # ── odd arguments are tool errors (MC-14) ─────────────────────────────────
    for args in ([1], "x"):
        r = m.rpc("tools/call", {"name": "knowledge_table", "arguments": args})
        check(f"arguments {args!r} come back as a tool error", (r.get("result") or {}).get("isError") is True, r)
    m.call("knowledge_table", {"question": "edge"})
    for tool, p in (("knowledge_table", "/v1/nodes/a b"), ("knowledge_table", "/v1/nodes/한글"), ("knowledge_read", "/v1/nodes/é/body")):
        t, err = m.call(tool, {"path": p, "why": "odd"})
        check(f"{tool} {p!r} is a tool error that names the address", err is True and "address" in t, t)

    # ── what knowledge_read reads (MC-15) ─────────────────────────────────────
    t, err = m.call("knowledge_read", {"path": "/v1/walks", "why": "history"})
    check("knowledge_read does not read the walk history", err is True and '"walks"' not in t and "question" not in t, t)
    t, err = m.call("knowledge_read", {"path": "/v1/vocab", "why": "vocab"})
    check("  nor any other part of /v1 that is not a document", err is True and "/v1/nodes/<id>/body" in t, t)
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body", "why": "the evidence list"})
    check("  and still reads a document", err is False and "Qualifying evidence" in t, t[:120])

    # ── a step whose reason cannot be encoded is still recorded (MC-18) ───────
    m.call("knowledge_table", {"question": "surrogate-probe"})
    m.call("knowledge_table", {"path": "/v1/regions/expense", "why": "receipts"})
    t, err = m.call("knowledge_read", {"path": "/v1/nodes/qualified-list/body", "why": "list \ud800 here"})
    walk = next((w for w in get("/v1/walks?limit=20").get("walks", []) if w.get("question") == "surrogate-probe"), {})
    steps = [s.get("address") for s in get(f"/v1/walks/{walk.get('id')}").get("steps", [])] if walk else []
    check("a `why` with a lone surrogate: the read answers and the step is on the record",
          err is False and "/v1/nodes/qualified-list/body" in steps and "step not recorded" not in m.stderr(), steps)

    # ── circuits to things that are not RouteMind (MC-4, MC-13) ───────────────
    for url, what in ((f"http://127.0.0.1:{HTML}", "an HTML page"), (f"http://127.0.0.1:{JLIST}", "a JSON array"),
                      (f"http://127.0.0.1:{SSH}", "an SSH banner"), ("not a url", "not a url"),
                      (f"ftp://127.0.0.1:{PORT}", "ftp")):
        t, err = m.call("knowledge_circuit", {"op": "open", "url": url, "token": "k", "name": "bad"})
        check(f"a circuit to {what} is refused as a tool error, saying why",
              err is True and ("Nothing was kept" in t or "http:// or https://" in t), t)
    t, _ = m.call("knowledge_circuit", {"op": "list"})
    check("  and none of them is kept", "No circuits are open" in t, t)
    t, _ = m.call("knowledge_table", {"question": "after bad circuits"})
    check("  nor listed on hop 0", "/v1/circuits/" not in t, t[-300:])
    t, err = m.call("knowledge_circuit", {"op": "close", "name": "nothing-here"})
    check("closing a circuit that is not open is a tool error", err is True, t)
    t, err = m.call("knowledge_circuit", {"op": "bogus"})
    check("an op that does not exist is a tool error", err is True and "op must be" in t, t)
    t, err = m.call("knowledge_place", {"op": "bogus"})
    check("knowledge_place with an op that does not exist says what op must be", err is True and "op must be" in t, t)

    # ── a circuit to a real far end (MC-5, MC-11, MC-12) ──────────────────────
    t, err = m.call("knowledge_circuit", {"op": "open", "url": SELF, "token": KEY, "name": "self"})
    check("a circuit to a RouteMind opens", err is False and "CIRCUIT self open" in t, t)
    t, err = m.call("knowledge_circuit", {"op": "open", "url": SELF, "token": "typo", "name": "self"})
    t2, _ = m.call("knowledge_circuit", {"op": "list"})
    check("a second open under the same name is refused, and the open one stays", err is True and "self" in t2 and SELF in t2, t + " | " + t2)
    m.call("knowledge_table", {"question": "circuit walk"})
    t, err = m.call("knowledge_table", {"path": "/v1/circuits/self/regions", "why": "what they share"})
    whole = next((r["use_when"] for r in get("/v1/regions")["regions"] if r.get("source") == "expense"), "")
    check("an area's sentence through a circuit is whole, not cut at 100 characters",
          " ".join(whole.split()) in t and "…" not in t, t)
    t, err = m.call("knowledge_table", {"path": "/v1/circuits/self/nodes/corp-card", "why": "the card"})
    check("a node with a document and children prints its own document through a circuit",
          "/v1/circuits/self/nodes/corp-card/body" in t, t)
    t, err = m.call("knowledge_read", {"path": "/v1/circuits/self/nodes/corp-card/body", "why": "its own document"})
    check("  and that address reads it", err is False and len(t) > 50, t[:120])
    t, err = m.call("knowledge_read", {"path": "/v1/circuits/self/regions", "why": "raw"})
    check("knowledge_read does not hand back a circuit's raw table with its unrewritten addresses",
          err is True and "/v1/export/" not in t, t)

    # ── placements (MC-9, MC-10, MC-14) ───────────────────────────────────────
    ids = []
    for name in ("Doc One", "Doc Two"):
        t, _ = m.call("knowledge_place", {"op": "open", "name": name, "one_liner": f"what {name} is for"})
        ids.append(t.split("[", 1)[1].split("]", 1)[0] if "[" in t else "")
    m.call("knowledge_place", {"op": "close", "id": ids[0]})
    t, _ = m.call("knowledge_place", {"op": "open", "name": "Doc Three", "one_liner": "what Doc Three is for"})
    third = t.split("[", 1)[1].split("]", 1)[0] if "[" in t else ""
    t, _ = m.call("knowledge_place", {"op": "list"})
    check("a placement id is never reused: closing one does not let the next overwrite another",
          third not in ids and "Doc Two" in t and "Doc Three" in t, f"{ids} {third} | {t}")
    m.call("knowledge_place", {"op": "step", "id": third, "pick": "/v1/regions/expense"})
    t, err = m.call("knowledge_place", {"op": "here", "id": third, "decisions": 5})
    check("decisions that are not a list are a tool error", err is True and m.alive(), t)
    t, err = m.call("knowledge_place", {"op": "open", "name": "Gym", "one_liner": "the gym", "kind": "nonexistent-kind"})
    check("a kind this backbone does not have is refused at open, naming the kinds it has",
          err is True and "nonexistent-kind" in t and "rule" in t, t)
    t, _ = m.call("knowledge_place", {"op": "open", "name": "Bad Area Doc", "one_liner": "a doc for a bad area"})
    pid = t.split("[", 1)[1].split("]", 1)[0] if "[" in t else ""
    t, err = m.call("knowledge_place", {"op": "here", "id": pid, "why": "new area",
                                        "area": {"source": "Bad Source", "name": "Bad", "one_liner": "x", "use_when": "y"}})
    check("a refused change says what the service said was wrong with it", err is True and "kebab" in t, t)
    m.close()

    # ── the far end at --api is not RouteMind (MC-6, MC-19) ───────────────────
    for port, what in ((SSH, "speaks something that is not HTTP"), (JLIST, "answers a JSON array"), (HTML, "answers HTML")):
        mx = Mcp(f"http://127.0.0.1:{port}/v1")
        ok = "result" in (mx.init_reply or {}) and "not reachable" in instructions(mx)
        tl = mx.rpc("tools/list")
        check(f"--api at something that {what}: initialize and tools/list still answer, saying so",
              ok and len((tl.get("result") or {}).get("tools") or []) == 4, f"{mx.init_reply} {str(tl)[:200]}")
        mx.close()
    t0 = time.time(); mx = Mcp(f"http://127.0.0.1:{SILENT}/v1"); t_init = time.time() - t0
    t0 = time.time(); tl = mx.rpc("tools/list"); t_tools = time.time() - t0
    check("--api at a host that never answers: initialize within 10 s, tools/list within 15 s",
          "result" in (mx.init_reply or {}) and t_init < 10 and "result" in tl and t_tools < 15, f"{t_init:.1f}s {t_tools:.1f}s")
    mx.close()

    # ── .env (MC-7, MC-8) ─────────────────────────────────────────────────────
    # Started without `initialize` unless the address is known to be one this check owns: the failure
    # tested here is the server pointing at 8080, and on a machine with an install there, that is
    # somebody's backbone (the audit's own walk landed on one). The address is on stderr at start.
    def with_env(raw, env=None, init=False):
        d = tempfile.mkdtemp(dir=T); os.makedirs(os.path.join(d, "mcp"))
        shutil.copy(os.path.join(ROOT, "mcp", "knowledge_mcp.py"), os.path.join(d, "mcp"))
        open(os.path.join(d, ".env"), "wb").write(raw)
        mx = Mcp(None, env=env, script=os.path.join(d, "mcp", "knowledge_mcp.py"), init=False)
        for _ in range(40):
            if "api=" in mx.stderr() or mx.p.poll() is not None: break
            time.sleep(0.1)
        if init and ":8080" not in mx.stderr():
            mx.init_reply = mx.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                                  "clientInfo": {"name": "edge-check", "version": "0"}})
        return mx, mx.close()
    mx, err = with_env(b"# caf\xe9 (saved in latin-1)\nWEB_PORT=9449\n")
    check("a .env that is not UTF-8 does not stop the server, and its WEB_PORT is read",
          "localhost:9449/" in err and "Traceback" not in err, err[-300:])
    mx, err = with_env(b"# caf\xe9\nWEB_PORT=9449\n", {"KNOWLEDGE_API": API}, init=True)
    check("  nor every call after it, when the address comes from KNOWLEDGE_API",
          "ROUTEMIND" in instructions(mx), (mx.init_reply or {}))
    mx, err = with_env(b"\xef\xbb\xbfWEB_PORT=9449\nKNOWLEDGE_ACTOR=x\n")
    check("a .env with a byte-order mark: WEB_PORT is read, not 8080", "localhost:9449/" in err and ":8080" not in err, err[-300:])
    mx, err = with_env(b"\xff\xfe" + "WEB_PORT=9449\r\n".encode("utf-16-le"))
    check("a .env saved as UTF-16 (Notepad's \"Unicode\"): WEB_PORT is read", "localhost:9449/" in err, err[-300:])
    mx, err = with_env(b"WEB_PORT=9449   # the map\n")
    check("a WEB_PORT with a comment after it is read", "localhost:9449/" in err, err[-300:])
    mx, err = with_env(b"WEB_PORT=94x9\n", init=True)
    check("a WEB_PORT that is not a port: no silent 8080, and the agent is told why",
          ":8080" not in err and "WEB_PORT" in instructions(mx) and "WEB_PORT" in err, err[-300:] + " | " + instructions(mx)[:200])
    mx, err = with_env(b"COMPOSE_PROJECT_NAME=x\n")
    check("  while a .env with no WEB_PORT at all is compose's own 8080", "localhost:8080/" in err, err[-300:])

    # ── settings that are not numbers, and a walk still walking (MC-17) ───────
    mx = Mcp(API, env={"KNOWLEDGE_WALK_TTL": "10m"})
    check("KNOWLEDGE_WALK_TTL=10m: the server starts, and says what it used", "result" in (mx.init_reply or {}) and "KNOWLEDGE_WALK_TTL" in mx.close())
    mx = Mcp(API, env={"KNOWLEDGE_WALK_TTL": "2"})
    mx.call("knowledge_table", {"question": "a long walk"})
    errs = []
    for _ in range(3):
        time.sleep(1.2)
        errs.append(mx.call("knowledge_table", {"path": "/v1/regions/expense", "why": "still walking"})[1])
    check("a walk that keeps stepping is not cut off at the TTL — it expires when left alone", errs == [False] * 3, errs)
    time.sleep(2.5)
    t, err = mx.call("knowledge_table", {"path": "/v1/regions/expense", "why": "after a pause"})
    check("  and left alone longer than the TTL, it expires", err is True and "expired" in t, t)
    mx.close()

    # ── the circuit prompt reads KNOWLEDGE_CIRCUIT_KEYS like the tool does; overlay asks for no walk ──
    mx = Mcp(API, env={"KNOWLEDGE_CIRCUIT_KEYS": f"{SELF}={KEY}", "KNOWLEDGE_TOOLS_EXTRA": "overlay"})
    pl = (mx.rpc("prompts/list").get("result") or {}).get("prompts", [])
    tok = next((a for p in pl if p["name"] == "circuit" for a in p.get("arguments", []) if a["name"] == "token"), {})
    check("the circuit prompt does not require a token", tok.get("required") is False, tok)
    r = mx.rpc("prompts/get", {"name": "circuit", "arguments": {"url": SELF, "name": "kept"}})
    text = (((r.get("result") or {}).get("messages") or [{}])[0].get("content") or {}).get("text", "")
    check("  and opens by address alone when KNOWLEDGE_CIRCUIT_KEYS holds the key, never printing it",
          "CIRCUIT kept open" in text and KEY not in text, text[:200])
    ov = next((t for t in (mx.rpc("tools/list").get("result") or {}).get("tools", []) if t["name"] == "knowledge_overlay"), None)
    check("the overlay tool asks for no walk id hop 0 never prints",
          ov is not None and "walk" not in ov["inputSchema"]["properties"], ov and sorted(ov["inputSchema"]["properties"]))
    mx.close()
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
