#!/usr/bin/env python3
"""The operator's door on an exchange, and everything it must not open.

    ./check/admin-check.py [port]

Starts an exchange and one backbone on throwaway repositories. Needs pyyaml on this python.

An admin surface is where a careful design usually springs a leak: it is the screen with the most
buttons, written last, and the one place where "just let the operator see everything" sounds
reasonable. So most of what is asserted here is what it **cannot** do.

  * It answers membership and health, and **never a reflected row**. What each backbone shares is
    between the members; an operator learns that BRANCH is attached and advertising two areas, not
    what they are.
  * It cannot make an area cross. Nothing here writes `use_when_export`, which is the only thing that
    shares an area and which lives in that backbone's own repository, behind its own review queue.
  * Its door is not the members' door. A member token does not open `/admin`, and the admin token
    does not read the reflection — two doors, two keys, and neither is a spare for the other.
  * With no token configured it is not a door at all.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8151
IX_PORT, BB_PORT = BASE + 10, BASE
MEMBER_TOKEN, ADMIN_TOKEN = "member-key", "operator-key"
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results: print("\n".join(results))
    if results: print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="admin-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
repo = os.path.join(T, "repo"); shutil.copytree(seed, repo)

sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

AREA = sorted(d for d in os.listdir(os.path.join(repo, "regions"))
              if os.path.isdir(os.path.join(repo, "regions", d)))[0]
SECRET_LINE = "the line only the members are meant to read"
for f in sorted(os.listdir(os.path.join(repo, "regions", AREA))):
    q = os.path.join(repo, "regions", AREA, f)
    text = open(q, encoding="utf-8").read()
    if "\nrole: representative\n" in text and "\nparent:" not in text:
        open(q, "w", encoding="utf-8").write(
            text.replace("\nrole: representative\n",
                         f"\nrole: representative\nuse_when_export: {SECRET_LINE}\n", 1))
        break
regenerate(Store(repo))
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)

MEMBERS = os.path.join(T, "members.yaml")
open(MEMBERS, "w", encoding="utf-8").write(
    f"members:\n  - name: solo\n    label: SOLO\n    url: http://127.0.0.1:{BB_PORT}\n"
    f"    token_env: TOK_SOLO\n")

env = {**os.environ, "TOK_SOLO": MEMBER_TOKEN, "ONTOLOGY_DATA": repo, "PORT": str(BB_PORT),
       "ONTOLOGY_PUBLISH": os.path.join(T, "pub"), "ONTOLOGY_PEER_TOKEN": MEMBER_TOKEN,
       "ONTOLOGY_PEER_TTL": "0"}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))


def start_exchange(admin_token: str | None):
    e = {**os.environ, "TOK_SOLO": MEMBER_TOKEN, "EXCHANGE_NAME": "ix", "PORT": str(IX_PORT),
         "EXCHANGE_MEMBERS": MEMBERS, "ONTOLOGY_PEER_TTL": "0"}
    if admin_token: e["EXCHANGE_ADMIN_TOKEN"] = admin_token
    else: e.pop("EXCHANGE_ADMIN_TOKEN", None)
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                         env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{IX_PORT}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    return p


def call(path, token=None, header="X-Admin-Token", method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"http://127.0.0.1:{IX_PORT}{path}", data=data, method=method,
                               headers={"Content-Type": "application/json"})
    if token: r.add_header(header, token)
    try:
        with urllib.request.urlopen(r, timeout=15) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: return e.code, json.loads(raw or b"{}")
        except Exception: return e.code, {"error": raw.decode(errors="replace")[:120]}
    except Exception as e: return 0, {"error": type(e).__name__}


for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{BB_PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)

# ── with no token configured, there is no door ────────────────────────────────
ix = start_exchange(None)
check("with no admin token there is no operator door", call("/admin/state")[0] == 501)
check("  and the members' door is unaffected",
      call("/v1/export/regions", MEMBER_TOKEN, "X-Peer-Token")[0] == 200)
ix.terminate(); time.sleep(0.6)

# ── with one, it is a door and only for the right key ─────────────────────────
ix = start_exchange(ADMIN_TOKEN)
check("no token is refused", call("/admin/state")[0] == 401)
check("a wrong token is refused", call("/admin/state", "nope")[0] == 401)
# Two doors, two keys. A member holding its own secret must not be able to read the operator's view,
# and the operator must not be able to read the members' — neither key is a spare for the other.
check("a member's token does not open the operator's door",
      call("/admin/state", MEMBER_TOKEN)[0] == 401)
check("the operator's token does not open the members' door",
      call("/v1/export/regions", ADMIN_TOKEN, "X-Peer-Token")[0] == 401)

st, state = call("/admin/state", ADMIN_TOKEN)
check("the operator's token is let in", st == 200, str(st))

# ── it sees the plumbing, never the knowledge ─────────────────────────────────
blob = json.dumps(state, ensure_ascii=False)
check("it answers membership and health", [m["name"] for m in (state.get("members") or [])] == ["solo"],
      json.dumps([m.get("name") for m in (state.get("members") or [])]))
check("  with whether each is answering", (state.get("members") or [{}])[0].get("reachable") is True)
check("  and how many areas each advertises", (state.get("members") or [{}])[0].get("advertising") == 1)
check("but not one reflected row", "regions" not in state, json.dumps(sorted(state.keys())))
# The strongest form of it: the line the member wrote for its peers is knowledge, and this door has
# no business carrying it.
check("  and not the line a member advertises", SECRET_LINE not in blob)
check("  nor any area's name", AREA not in blob, blob[:120])

# ── membership is the exchange's own state, so it can be edited ───────────────
st, r = call("/admin/members", ADMIN_TOKEN, method="POST",
             body={"name": "second", "label": "SECOND", "url": "http://127.0.0.1:9"})
check("a backbone can be registered", st == 200 and "second" in (r.get("members") or []), json.dumps(r)[:90])
check("  and it lands in members.yaml", "second" in open(MEMBERS, encoding="utf-8").read())
check("  with no secret written into the file", MEMBER_TOKEN not in open(MEMBERS, encoding="utf-8").read())
st, state2 = call("/admin/state", ADMIN_TOKEN)
check("  and shows as unreachable, named, with the reason",
      any(m["name"] == "second" and not m["reachable"] and m["error"] for m in state2.get("members") or []),
      json.dumps([(m["name"], m["reachable"]) for m in state2.get("members") or []]))

st, r = call("/admin/members", ADMIN_TOKEN, method="DELETE", body={"name": "second"})
check("and removed again", st == 200 and "second" not in (r.get("members") or []))
check("  leaving the one that was already there", "solo" in (r.get("members") or []))
check("  and its ontology untouched — it simply stops meeting here",
      urllib.request.urlopen(f"http://127.0.0.1:{BB_PORT}/healthz", timeout=5).status == 200)

# ── a name that could not be an address is refused ────────────────────────────
for bad in ["../etc", "Has Caps", "", "x" * 40]:
    st, _ = call("/admin/members", ADMIN_TOKEN, method="POST",
                 body={"name": bad, "url": "http://127.0.0.1:9"})
    check(f"a member named {bad[:12]!r} is refused", st == 400, str(st))
st, _ = call("/admin/members", ADMIN_TOKEN, method="POST", body={"name": "ok-name", "url": "file:///etc"})
check("and so is an address that is not http", st == 400, str(st))

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
