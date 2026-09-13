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


def hit(port, path, method="GET", token=None, header=None, value=None):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}",
                               data=b"{}" if method != "GET" else None, method=method)
    r.add_header("Content-Type", "application/json")
    if token: r.add_header("Authorization", f"Bearer {token}")
    if header: r.add_header(header, value or "")
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
