#!/usr/bin/env python3
"""The door on the screen's side — three modes, and what each one is worth.

    docker cp check $(docker compose ps -q web):/tmp/check
    docker compose exec web python3 /tmp/check/auth-check.py

Needs fastapi and uvicorn, which the web image has and a host usually does not — the same shape as
`scenarios.py` needing pyyaml. It starts `web/app.py` itself on spare ports, with no ontology behind
it: the gate answers **before** anything is proxied, so "401 or not 401" is the whole question and a
missing backend cannot confuse it. Every non-401 below is a request that got past the door and then
failed for the honest reason that there is nothing behind it.

Until 2026-09-13 the only thing that said this build had no authentication was the README, which is
the one place a running system cannot be read from. Three of these assertions are about that: the log
says it, `/healthz` says it, and a mode that cannot be safe does not start.

The one worth reading twice is the trusted source. A header naming the user is what every
authenticating reverse proxy offers, and believing it from anywhere is **worse than no
authentication**: anybody can send one, and now the record says a person who was not there did it. So
`proxy` without `KNOWLEDGE_AUTH_TRUSTED_PROXY` refuses to start rather than coming up looking guarded.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = next((p for p in (os.environ.get("KNOWLEDGE_APP"), "/app/app.py",
                        os.path.join(ROOT, "web", "app.py")) if p and os.path.isfile(p)), None)
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8391
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# A run that stopped early used to print a summary that read exactly like a clean one. The results
# list holds what ran, `_end` is an atexit handler so it prints whatever crashed the script, and
# "0 failed of 29" is then true of the 29 that ran and silent about the 40 that did not. The exit
# code was 1, so nothing automated was fooled — but the line a person reads said the run passed, and
# that is the one place a check must not be wrong about itself. Appended to on the last line.
finished = []


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

if not APP:
    print("FAIL web/app.py not found"); sys.exit(1)
try:
    import fastapi, uvicorn                                              # noqa: F401
except Exception as e:
    print(f"auth-check needs fastapi and uvicorn ({type(e).__name__}). Run it in the web container:\n"
          f"  docker cp check $(docker compose ps -q web):/tmp/check\n"
          f"  docker compose exec web python3 /tmp/check/auth-check.py")
    sys.exit(2)

port_seq = iter(range(BASE, BASE + 40))


def start(**env):
    """One web process, on its own port, with nothing behind it."""
    port = next(port_seq)
    e = {**os.environ, "PORT": str(port), "KNOWLEDGE_API_URL": "http://127.0.0.1:1"}
    for k in ("KNOWLEDGE_AUTH", "KNOWLEDGE_TOKEN", "KNOWLEDGE_AUTH_HEADER",
              "KNOWLEDGE_AUTH_TRUSTED_PROXY", "KNOWLEDGE_AUTH_READS"):
        e.pop(k, None)
    e.update({k: str(v) for k, v in env.items()})
    p = subprocess.Popen([sys.executable, APP], env=e, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
    procs.append(p)
    for _ in range(120):
        if p.poll() is not None: return None, port, p
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/app-config", timeout=1)
            return p, port, p
        except urllib.error.HTTPError:
            return p, port, p
        except Exception: time.sleep(0.25)
    return p, port, p


def hit(port, path, method="GET", token=None, header=None, value=None, extra=None):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}",
                               data=b"{}" if method != "GET" else None, method=method)
    r.add_header("Content-Type", "application/json")
    if token: r.add_header("Authorization", f"Bearer {token}")
    if header: r.add_header(header, value or "")
    for k, v in (extra or {}).items(): r.add_header(k, v)
    def low(h): return {k.lower(): v for k, v in dict(h).items()}   # HTTP header names are not case
    try:
        with urllib.request.urlopen(r, timeout=10) as x: return x.status, low(x.headers), x.read()
    except urllib.error.HTTPError as e: return e.code, low(e.headers), e.read()
    except Exception as e: return 0, {}, str(e).encode()


WRITE = "/api/knowledge/nodes"
READ = "/api/knowledge/regions"

# ── open: what every install has been, and now says so ───────────────────────
p, port, _ = start()
check("open: the service starts", p and p.poll() is None)
st, _, _ = hit(port, WRITE, "POST")
check("  and a write is not refused at the door", st != 401, str(st))
st, _, b = hit(port, "/api/app-config")
cfg = json.loads(b or b"{}")
check("  and the running service says which door it has", cfg.get("auth") == "open", json.dumps(cfg)[:120])
check("    and that the name on a commit is a signature, not an identity",
      cfg.get("auth_names_the_actor") is False)
p.terminate(); time.sleep(0.4)
log = p.stdout.read() if p.stdout else ""
check("  and says it out loud at startup, where an operator will see it",
      "auth=open" in log and "anyone who can reach this port" in log, log[-160:])

# ── a mode that cannot be safe does not start ────────────────────────────────
# Both of these used to be impossible to get wrong only because neither existed. An operator who sets
# a mode has decided the thing is meant to be closed; coming up open instead turns that decision into
# a surprise, and into the kind nobody finds until somebody else does.
_, _, dead = start(KNOWLEDGE_AUTH="token")
dead.wait(timeout=20)
out = dead.stdout.read() if dead.stdout else ""
check("token with no secret refuses to start", dead.returncode == 2, str(dead.returncode))
check("  and names the variable to set", "KNOWLEDGE_TOKEN" in out, out[:160])
_, _, dead = start(KNOWLEDGE_AUTH="proxy")
dead.wait(timeout=20)
out = dead.stdout.read() if dead.stdout else ""
check("proxy with no trusted source refuses to start", dead.returncode == 2, str(dead.returncode))
check("  and says why believing the header from anywhere is worse than nothing",
      "KNOWLEDGE_AUTH_TRUSTED_PROXY" in out and "anybody can send the header" in out, out[:200])
_, _, dead = start(KNOWLEDGE_AUTH="sso")
dead.wait(timeout=20)
check("a mode nobody implemented refuses to start", dead.returncode == 2, str(dead.returncode))

# ── token: may you write, and nothing about who you are ──────────────────────
SECRET = "s3cret-token-value"
p, port, _ = start(KNOWLEDGE_AUTH="token", KNOWLEDGE_TOKEN=SECRET)
check("token: the service starts", p and p.poll() is None)
st, h, _ = hit(port, WRITE, "POST")
check("  a write with no secret is refused", st == 401, str(st))
check("    and says what to present rather than leaving them guessing",
      h.get("www-authenticate") == "Bearer", json.dumps(h.get("www-authenticate")))
check("  a write with the wrong secret is refused", hit(port, WRITE, "POST", token="nope")[0] == 401)
check("  a write with the secret gets past the door", hit(port, WRITE, "POST", token=SECRET)[0] != 401)
# Reads are what an agent does through the MCP, which has no session and did not ask for one. Closing
# them by default would make turning authentication on mean turning the agent off, and the hole the
# README warns about is a write hole.
check("  a read is open, because that is where the agent is", hit(port, READ)[0] != 401)
st, _, b = hit(port, "/api/app-config")
check("  and it still answers what the door is", json.loads(b or b"{}").get("auth") == "token")
check("  which is a lock and not a name",
      json.loads(b or b"{}").get("auth_names_the_actor") is False)
p.terminate(); time.sleep(0.3)

p, port, _ = start(KNOWLEDGE_AUTH="token", KNOWLEDGE_TOKEN=SECRET, KNOWLEDGE_AUTH_READS="1")
check("  and with reads guarded too, asked for explicitly", hit(port, READ)[0] == 401)
check("    while the secret still opens them", hit(port, READ, token=SECRET)[0] != 401)
# A health check that needs a credential is a health check nobody wires up, and the image's own
# HEALTHCHECK calls this one.
check("    and the health endpoint is never behind it", hit(port, "/api/app-config")[0] == 200)
p.terminate(); time.sleep(0.3)

# /healthz on the web port is never behind the door either — but with reads guarded, an anonymous
# caller gets the state without the detail: the full answer names the data path, uncommitted files
# and validation errors that quote the map's own sentences (2026-10-10).
import http.server, threading                                            # noqa: E402
class _Fake(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        body = json.dumps({"ok": True, "valid": False, "writable": True, "writing": False, "data": "/data/repo",
                           "uncommitted": "regions/hr/secret-plan.md", "errors": ["use_when no longer matches: 'the merger'"]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
_srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Fake); threading.Thread(target=_srv.serve_forever, daemon=True).start()
p, port, _ = start(KNOWLEDGE_AUTH="token", KNOWLEDGE_TOKEN=SECRET, KNOWLEDGE_AUTH_READS="1",
                   KNOWLEDGE_API_URL=f"http://127.0.0.1:{_srv.server_address[1]}")
st, _, b = hit(port, "/healthz"); anon = json.loads(b or b"{}")
check("  /healthz answers without the secret, and says only whether it is well",
      st == 200 and anon.get("valid") is False and "errors" not in anon and "uncommitted" not in anon and "data" not in anon, anon)
st, _, b = hit(port, "/healthz", token=SECRET)
check("    and in full to whoever holds it", st == 200 and "errors" in json.loads(b or b"{}"))
p.terminate(); time.sleep(0.3); _srv.shutdown()

# ── what the relay carries across, with a fake ontology behind it ─────────────
# Each of these is the web app being wrong about the ontology's answer — what it passed on, what it
# dropped, what it let through — so the far end records what reached it and answers on cue.
SEEN = {}
class _Far(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _answer(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        SEEN[self.path] = dict(self.headers)
        if self.path == "/v1/nodes/doc/body":
            body = b"the document\n"
            self.send_response(200); self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.send_header("X-Revision", "a" * 40)
            self.send_header("X-Source", "regions/hr/doc.md"); self.end_headers(); self.wfile.write(body); return
        if self.path.endswith("/body"):
            return self._answer(404, {"error": "node shelf has no document yet — it is listed as `type: empty`"})
        body = json.dumps({"regions": []}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.send_header("X-Revision", "b" * 40)
        self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        # The connection dropped mid-answer, as a paused or restarting ontology does.
        self.close_connection = True; self.connection.close()
    def do_PUT(self):
        SEEN[self.path] = {"length": self.headers.get("Content-Length")}
        self.rfile.read(int(self.headers.get("Content-Length") or 0)); self._answer(200, {"ok": True})
_far = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Far); threading.Thread(target=_far.serve_forever, daemon=True).start()
FAR = f"http://127.0.0.1:{_far.server_address[1]}"
p, port, _ = start(KNOWLEDGE_API_URL=FAR)

# The reader in the owner's access log is the socket's address. The relay appended it to whatever
# X-Forwarded-For the caller sent, and the log records the first entry — so a reader could write
# itself down as anybody (web audit WB-2, 2026-11-02).
hit(port, "/v1/export/regions", extra={"X-Forwarded-For": "8.8.8.8"})
xff = {k.lower(): v for k, v in (SEEN.get("/v1/export/regions") or {}).items()}.get("x-forwarded-for")
check("relay: the export reader is recorded as the socket's address, not one it claimed",
      xff == "127.0.0.1", repr(xff))
# A far end that drops the connection is the JSON 502 the export read gives, not a plain-text 500
# (web audit WB-3: the token POST, with the ontology paused).
st, h, b = hit(port, "/v1/peers/token", "POST")
check("  a token request the ontology drops is a JSON 502", st == 502 and "json" in (h.get("content-type") or ""),
      f"{st} {b[:80]!r}")
# The API's own reason for a 404, not "RouteMind API returned HTTP 404." — "nobody has written this
# yet" and "no such address" are different answers, as the route's docstring says (web audit WB-5).
st, _, b = hit(port, "/api/knowledge/nodes/shelf/body")
check("  a document's 404 carries the API's reason", st == 404 and b"no document yet" in b, f"{st} {b[:120]!r}")

# Which commit, and which file, a read was served from. The relay rebuilt every answer and dropped
# both, so an agent behind the web port recorded walks that said where it went and not what it read
# (2026-11-02).
for path in ("/api/knowledge/nodes/doc/body", "/api/knowledge/v1/nodes/doc/body"):
    st, h, b = hit(port, path)
    check(f"  {path} carries the revision and the file it was read from",
          st == 200 and h.get("x-revision") == "a" * 40 and h.get("x-source") == "regions/hr/doc.md", f"{st} {h}")
st, h, b = hit(port, "/api/knowledge/regions")
check("  and a table carries its revision", st == 200 and h.get("x-revision") == "b" * 40, f"{st} {h}")

# A document is bounded. 50 MB went through and was committed, and the popup then served all of it
# (web audit WB-7, 2026-11-02). Refused here, before it is sent, with a sentence and the setting.
big = json.dumps({"content": "x" * 1_200_000, "description": "big"}).encode()
def put_big(port):
    r = urllib.request.Request(f"http://127.0.0.1:{port}/api/knowledge/nodes/shelf/files/big.md", data=big,
                               method="PUT", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, x.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
SEEN.pop("/v1/nodes/shelf/files/big.md", None)
st, b = put_big(port)
check("  a 1.2 MB document is refused with 413 and why", st == 413 and b"KNOWLEDGE_MAX_DOCUMENT_BYTES" in b, f"{st} {b[:160]!r}")
check("    and nothing reached the ontology", "/v1/nodes/shelf/files/big.md" not in SEEN)
p.terminate(); time.sleep(0.3)
p, port, _ = start(KNOWLEDGE_API_URL=FAR, KNOWLEDGE_MAX_DOCUMENT_BYTES="2000000")
check("  and the limit is a setting", put_big(port)[0] == 200)
p.terminate(); time.sleep(0.3); _far.shutdown()

# ── proxy: the only mode that produces an actor worth the name ───────────────
HEAD = "X-Forwarded-Email"
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="any")
check("proxy: the service starts once a source is declared", p and p.poll() is None)
check("  a write with no header is refused", hit(port, WRITE, "POST")[0] == 401)
check("    and does not offer a token that does not exist",
      hit(port, WRITE, "POST")[1].get("www-authenticate") is None)
check("  a write with one gets past the door",
      hit(port, WRITE, "POST", header=HEAD, value="someone@example.com")[0] != 401)
check("  an empty header is not a person", hit(port, WRITE, "POST", header=HEAD, value="")[0] == 401)
st, _, b = hit(port, "/api/app-config")
check("  and this is the one door that names the actor",
      json.loads(b or b"{}").get("auth_names_the_actor") is True)
p.terminate(); time.sleep(0.3)

# Declared as one address, arriving from another. This is the assertion the whole mode rests on.
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="10.9.9.9")
check("  a header from an address that was not declared is not believed",
      hit(port, WRITE, "POST", header=HEAD, value="someone@example.com")[0] == 401, "from 127.0.0.1")
p.terminate(); time.sleep(0.3)
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="127.0.0.0/8")
check("  and one from a declared range is", 
      hit(port, WRITE, "POST", header=HEAD, value="someone@example.com")[0] != 401)
p.terminate(); time.sleep(0.3)

# The address judged is the socket's, never X-Forwarded-For. uvicorn's default replaced the client
# address with that header's for anything arriving from 127.0.0.1, so a same-host proxy that adds it
# (oauth2-proxy, nginx and Caddy all do) was never believed, and any local process could name a
# trusted address in it and be whoever it liked (web audit WB-1, 2026-11-02).
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="127.0.0.1")
check("  a declared proxy that adds X-Forwarded-For is still believed",
      hit(port, WRITE, "POST", header=HEAD, value="someone@example.com",
          extra={"X-Forwarded-For": "203.0.113.5"})[0] != 401)
p.terminate(); time.sleep(0.3)
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="10.255.255.1")
check("  and X-Forwarded-For naming the declared address does not make a caller it",
      hit(port, WRITE, "POST", header=HEAD, value="ceo@example.com",
          extra={"X-Forwarded-For": "10.255.255.1"})[0] == 401, "from 127.0.0.1")
p.terminate(); time.sleep(0.3)

# An identity longer than a commit's name holds is refused, and says so. It was cut to 64 characters
# without a word, so two long addresses sharing a prefix signed as one person (web audit WB-6).
p, port, _ = start(KNOWLEDGE_AUTH="proxy", KNOWLEDGE_AUTH_TRUSTED_PROXY="any")
st, _, b = hit(port, WRITE, "POST", header=HEAD, value="x" * 70 + "@example.com")
check("  an identity too long to sign with is refused, with the reason",
      st == 401 and b"64" in b, f"{st} {b[:160]!r}")
# Only where something is signed: the same check on every request locked that person out of the map
# itself, reads included, with reads not guarded at all (verification pass, 2026-11-02).
st, _, b = hit(port, READ, "GET", header=HEAD, value="x" * 70 + "@example.com")
check("  but may still read when reads are not guarded", st != 401, f"{st} {b[:160]!r}")
p.terminate(); time.sleep(0.3)

# ── and the actor itself ─────────────────────────────────────────────────────
# Read out of the module rather than over the wire: what a commit is signed with is decided here, and
# the comment above the proxy calls used to claim it was "the signed-in username, never a
# client-supplied value" while it was exactly that.
sys.path.insert(0, os.path.dirname(APP))
os.environ.update({"KNOWLEDGE_AUTH": "proxy", "KNOWLEDGE_AUTH_TRUSTED_PROXY": "any",
                   "KNOWLEDGE_API_URL": "http://127.0.0.1:1"})
import importlib                                                          # noqa: E402
appmod = importlib.import_module(os.path.basename(APP)[:-3])


class _Req:
    def __init__(self, headers): self.headers = headers; self.client = type("C", (), {"host": "127.0.0.1"})()


who = appmod._request_user(_Req({HEAD: "real@example.com", "X-Knowledge-Actor": "somebody-else"}))
check("in proxy mode the proxy names the actor", who.get("username") == "real@example.com", json.dumps(who))
check("  and the client does not get a vote", "somebody-else" not in json.dumps(who))
check("  with no header, there is no actor to record", appmod._request_user(_Req({})) == {})

finished.append(True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
