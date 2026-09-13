#!/usr/bin/env python3
"""The room over a lifetime — docs/SCENARIOS.md, sections L, M and N.

    ./check/room-check.py [port]

Two backbones and an exchange on throwaway repositories. Needs pyyaml.

The other peering checks ask whether a room answers correctly once it is up. This asks what happens
while it changes, and it exists because the default install changed underneath those questions: an
exchange is now there from the first `docker compose up`, which means **every link in every install
runs through one process nobody had yet switched off on purpose.**

  * **L — membership.** A backbone is registered, advertises, is removed at the exchange, and comes
    back. Removing one is the operator action with the widest blast radius on this screen, and what
    it must *not* touch — the removed backbone's own ontology — is as much of the scenario as what it
    must.
  * **M — the room itself goes away.** Not a member: the exchange. Each backbone must keep answering
    its own areas, must drop the rows it can no longer stand behind, must **stop claiming absence**,
    and must name what failed. Then it must recover with nobody pressing anything. A backbone that
    stayed cautious for ever after one blip is as wrong as one that never noticed and much harder to
    see, because everything still works.
  * **N — an audience over a lifetime.** Written, narrowed, widened, and pointed at somebody who is
    not in the room. The last is the quiet one: a name nobody has means an area advertised to nobody,
    and nothing anywhere errors.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8271
A_PORT, B_PORT, IX_PORT = BASE, BASE + 1, BASE + 10
ADMIN = "operator-key"
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results:
        print("\n".join(results))
        print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="room-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

TOK = {"TOK_AY": "tok-ay", "TOK_BEE": "tok-bee"}
LINE = {"ay": "what ay answers for the others", "bee": "what bee answers for the others"}
areas = sorted(d for d in os.listdir(os.path.join(seed, "regions"))
               if os.path.isdir(os.path.join(seed, "regions", d)))
SHARE = {"ay": areas[0], "bee": areas[1]}
PORT = {"ay": A_PORT, "bee": B_PORT}
repos, envs = {}, {}
MEMBERS = os.path.join(T, "members.yaml")


def write_members(names):
    open(MEMBERS, "w", encoding="utf-8").write("members:\n" + "".join(
        f"  - name: {n}\n    label: {n.upper()}\n    url: http://127.0.0.1:{PORT[n]}\n"
        f"    token_env: TOK_{n.upper()}\n" for n in names))


def set_export(who, line=None, audience=None):
    """The frontmatter, the derived file, a commit — the three steps a person's edit takes. No API,
    so nothing announces: every transition here has to be found by looking, not by being told."""
    repo, area = repos[who], SHARE[who]
    for f in sorted(os.listdir(os.path.join(repo, "regions", area))):
        q = os.path.join(repo, "regions", area, f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in t or "\nparent:" in t: continue
        out = [l for l in t.splitlines(True)
               if not l.startswith(("use_when_export:", "export_to:"))]
        at = next(i for i, l in enumerate(out) if l.strip() == "role: representative") + 1
        if audience: out.insert(at, "export_to: [" + ", ".join(audience) + "]\n")
        if line: out.insert(at, f"use_when_export: {line}\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(repo))
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=x", "-c", "user.email=x@l",
                    "commit", "-q", "--allow-empty", "-m", "export"], check=True)


for n in ("ay", "bee"):
    repo = os.path.join(T, n); shutil.copytree(seed, repo); repos[n] = repo
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: ix\n    label: EXCHANGE\n    url: http://127.0.0.1:{IX_PORT}\n"
        f"    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)
    e = {**os.environ, **TOK, "ONTOLOGY_DATA": repo, "PORT": str(PORT[n]),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"),
         "ONTOLOGY_PEER_TOKEN": TOK[f"TOK_{n.upper()}"], "ONTOLOGY_PEER_TTL": "0"}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    envs[n] = e
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

IX_ENV = {**os.environ, **TOK, "EXCHANGE_NAME": "ix", "PORT": str(IX_PORT),
          "EXCHANGE_MEMBERS": MEMBERS, "ONTOLOGY_PEER_TTL": "0",
          "EXCHANGE_ADMIN_TOKEN": ADMIN}


def start_ix():
    write_members(["ay", "bee"]) if not os.path.exists(MEMBERS) else None
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                         env=IX_ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{IX_PORT}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    return p


def get(port, path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=20) as x:
            return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e: return e.code, {}
    except Exception as e: return 0, {"raw": type(e).__name__}


def admin(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"http://127.0.0.1:{IX_PORT}{path}", data=data, method=method,
                               headers={"Content-Type": "application/json", "X-Admin-Token": ADMIN})
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e: e.read(); return e.code, {}
    except Exception as e: return 0, {"raw": type(e).__name__}


def export_of(who):
    """What a backbone offers across a link, read the way a peer reads it. `/v1/regions` does not
    print `use_when_export` — it is the line for somebody else's hop 0, not for this one — so asking
    hop 0 whether an area is still shared asks the wrong table."""
    r = urllib.request.Request(f"http://127.0.0.1:{PORT[who]}/v1/export/regions")
    r.add_header("X-Peer-Token", TOK[f"TOK_{who.upper()}"])
    try:
        with urllib.request.urlopen(r, timeout=20) as x:
            return sorted(q["source"] for q in (json.loads(x.read() or b"{}").get("regions") or []))
    except Exception: return None


def hop0(who):
    return get(PORT[who], "/v1/regions")[1]


def remote(who):
    return sorted(str(r.get("origin") or r.get("peer")) for r in (hop0(who).get("regions") or [])
                  if r.get("peer"))


def mine(who):
    return len([r for r in (hop0(who).get("regions") or []) if not r.get("peer")])


write_members(["ay"])                    # one member: the shape a default install ships in
start_ix()
for port in (A_PORT, B_PORT, IX_PORT):
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)

# ── L — membership ───────────────────────────────────────────────────────────
# The shipped shape first: one backbone, one exchange, nothing to reflect. It has to read exactly as
# it would with no exchange at all, or every single-backbone install is being told about a link.
own = mine("ay")
check("L1 one backbone and an empty room: hop 0 carries only its own areas", remote("ay") == [] and own > 0,
      json.dumps(remote("ay")))
check("   and absence may be claimed, with nothing named",
      "may say something is absent" in (hop0("ay").get("absence") or "")
      and "reaches through" not in (hop0("ay").get("absence") or ""),
      (hop0("ay").get("absence") or "")[:90])
check("   while the link itself reads as up",
      all(l["reachable"] for l in (hop0("ay").get("links") or [])),
      json.dumps(hop0("ay").get("links")))

st, r = admin("POST", "/admin/members",
              {"name": "bee", "label": "BEE", "url": f"http://127.0.0.1:{B_PORT}",
               "token_env": "TOK_BEE"})
check("L2 a second backbone is registered", st == 200 and "bee" in (r.get("members") or []), str(st))
time.sleep(0.4)
check("   and advertising nothing, it changes nothing at hop 0", remote("ay") == [],
      json.dumps(remote("ay")))
check("   and absence is still claimable", "may say something is absent" in (hop0("ay").get("absence") or ""))

set_export("bee", LINE["bee"])
time.sleep(0.4)
check("L3 once it advertises, the row arrives with nothing restarted", remote("ay") == ["bee"],
      json.dumps(remote("ay")))
addr = next((r["fetch"] for r in hop0("ay")["regions"] if r.get("peer")), None)
check("   and what it points at is readable straight away",
      bool(addr) and get(A_PORT, addr)[0] == 200, str(addr))
check("   and the sentence now names the room it comes through",
      "reaches through" in (hop0("ay").get("absence") or ""), (hop0("ay").get("absence") or "")[:100])

st, r = admin("DELETE", "/admin/members", {"name": "bee"})
check("L4 removing it at the exchange is accepted", st == 200 and "bee" not in (r.get("members") or []))
time.sleep(0.4)
check("   and its rows go from the other backbone", remote("ay") == [], json.dumps(remote("ay")))
check("   and the address goes with them", get(A_PORT, addr)[0] in (404, 502, 503), str(get(A_PORT, addr)[0]))
# The widest-blast-radius button on the operator's screen. What it must not touch:
check("   while its own ontology is untouched — it simply stops meeting here",
      mine("bee") > 0 and export_of("bee") == [SHARE["bee"]],
      f'{mine("bee")} own, exporting {json.dumps(export_of("bee"))}')
check("   and the remaining member is not disturbed", mine("ay") == own)
check("   and absence is claimable again, with nobody named",
      "may say something is absent" in (hop0("ay").get("absence") or "")
      and "reaches through" not in (hop0("ay").get("absence") or ""))

admin("POST", "/admin/members", {"name": "bee", "label": "BEE", "url": f"http://127.0.0.1:{B_PORT}",
               "token_env": "TOK_BEE"})
time.sleep(0.4)
check("L5 registering it again brings the row back", remote("ay") == ["bee"], json.dumps(remote("ay")))

# ── M — the room itself goes away ────────────────────────────────────────────
# Not a member. The exchange is in every install now, so it is on every path, and nobody had switched
# it off on purpose before this.
ix = [p for p in procs if p.poll() is None][-1]
ix.terminate(); time.sleep(1.0)
d = hop0("ay")
check("M1 with the room gone, a backbone still answers", bool(d.get("regions")), json.dumps(d)[:80])
check("   and still serves its own areas", mine("ay") == own, str(mine("ay")))
check("   and drops the rows it can no longer stand behind", remote("ay") == [], json.dumps(remote("ay")))
check("   and says the list is incomplete", "incomplete" in (d.get("absence") or "").lower(),
      (d.get("absence") or "")[:90])
check("   and forbids claiming absence", "may say something is absent" not in (d.get("absence") or ""))
check("   and names what failed, and why",
      any(not l["reachable"] and l["error"] for l in (d.get("links") or [])),
      json.dumps(d.get("links")))
st, _ = get(A_PORT, addr)
check("   while a read across it is not a 404", st != 404, str(st))
check("   and the other backbone is equally unaffected in its own areas", mine("bee") > 0)

start_ix()
time.sleep(1.0)
d = hop0("ay")
check("M2 the room comes back and is used again, unprompted", remote("ay") == ["bee"],
      json.dumps(remote("ay")))
check("   and absence may be claimed over both backbones again",
      "may say something is absent" in (d.get("absence") or "")
      and "incomplete" not in (d.get("absence") or "").lower(), (d.get("absence") or "")[:90])
check("   and a read across it works again", get(A_PORT, addr)[0] == 200)

# ── N — an audience over a lifetime ──────────────────────────────────────────
set_export("bee", LINE["bee"], audience=["ay"])
time.sleep(0.4)
check("N1 an audience naming the only other member changes nothing for it", remote("ay") == ["bee"],
      json.dumps(remote("ay")))
check("   and does not hand it the list", "export_to" not in json.dumps(hop0("ay")))

set_export("bee", LINE["bee"], audience=["somebody-else"])
time.sleep(0.4)
check("N2 an audience naming somebody who is not in the room leaves everyone out",
      remote("ay") == [], json.dumps(remote("ay")))
check("   and nothing errors anywhere — the link is up, not broken",
      all(l["reachable"] for l in (hop0("ay").get("links") or [])), json.dumps(hop0("ay").get("links")))
check("   and the address stops working, not just the row",
      get(A_PORT, addr)[0] in (404, 502), str(get(A_PORT, addr)[0]))
check("   while bee still holds it locally", mine("bee") > 0)
# The room's own view is health, not policy: the operator sees a member advertising an area, whoever
# it is for. Anything else would make an audience visible to the one party it does not restrict.
st, state = admin("GET", "/admin/state")
check("   and the operator still sees it advertising",
      any(m["name"] == "bee" and m["advertising"] == 1 for m in (state.get("members") or [])),
      json.dumps([(m["name"], m.get("advertising")) for m in (state.get("members") or [])]))

set_export("bee", LINE["bee"])
time.sleep(0.4)
check("N3 taking the audience away puts it back", remote("ay") == ["bee"], json.dumps(remote("ay")))
check("   and the address with it", get(A_PORT, addr)[0] == 200)

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
