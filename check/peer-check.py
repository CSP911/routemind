#!/usr/bin/env python3
"""What crosses a link between two backbones, and what must not.

    ./check/peer-check.py [port]

Starts its own backbones on throwaway repositories, because everything here is about what one
install lets another install see, and getting that wrong on somebody's real ontology is the whole
risk. Needs pyyaml on this python; see check/write-paths.sh for the same requirement.

The property under test is not "the token works". It is that **the export surface cannot serve an
area nobody decided to share** — no path through it, and no mistake in a token check, reaches one.
An area crosses a link by having `use_when_export` written on its representative, and by nothing
else. So the checks below are mostly negative: they name things that exist, are readable locally,
and must still come back 404 across the link.

docs/PEERING.md is the contract.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8171
TOKEN = "peer-check-token"
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results: print("\n".join(results))
    if results: print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")


import atexit; atexit.register(_end)

T = tempfile.mkdtemp(prefix="peer-check-")
repo = os.path.join(T, "repo")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
shutil.copytree(seed, repo)

sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

# One area is shared, by writing the line that shares it. Nothing else about the repository changes,
# which is the point: sharing is one field, and its absence is the default.
def _need_areas(names, n, what):
    """This check shares an area between two backbones, so it needs a seed with at least `n`.

    The ontology image ships `seed/` with no areas and no `examples/`, which is right — an install
    starts empty — and means running this inside a container ends in `IndexError: list index out of
    range`. A refusal that names neither the mistake nor the fix is the thing this repository keeps
    finding in its own code; it should not be in the checks that find it.
    """
    if len(names) >= n: return names
    print(f"this check needs a seed with at least {n} area{'s' if n > 1 else ''} to share between "
          f"backbones, and {what} "
          f"has {len(names)}.\nRun it on the host, where examples/back-office is — the ontology image "
          f"ships an empty seed on purpose.")
    raise SystemExit(2)


areas = sorted(d for d in os.listdir(os.path.join(repo, "regions"))
               if os.path.isdir(os.path.join(repo, "regions", d)))
_need_areas(areas, 1, "the seed")
SHARED, PRIVATE = areas[0], (areas[1] if len(areas) > 1 else None)
EXPORT_LINE = "what a partner may ask this office · the questions we answer for them"
rep_file = None
for f in sorted(os.listdir(os.path.join(repo, "regions", SHARED))):
    p = os.path.join(repo, "regions", SHARED, f)
    text = open(p, encoding="utf-8").read()
    if "\nrole: representative\n" in text and "\nparent:" not in text:
        open(p, "w", encoding="utf-8").write(
            text.replace("\nrole: representative\n", f"\nrole: representative\nuse_when_export: {EXPORT_LINE}\n", 1))
        rep_file = p; break
if not rep_file: raise SystemExit(f"no top representative in {SHARED} to share")
regenerate(Store(repo))
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=peer", "-c", "user.email=p@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)

env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT),
       "ONTOLOGY_PUBLISH": os.path.join(T, "publish"), "ONTOLOGY_PEER_TOKEN": TOKEN}
for k in [k for k in env if k.startswith("ONTOLOGY_LLM_")]: env.pop(k)
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
else: raise SystemExit(f"the backbone on {PORT} did not start")


def get(path, token=None):
    r = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1{path}")
    if token: r.add_header("X-Peer-Token", token)
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read()
        try: return e.code, json.loads(body or b"{}")
        except Exception: return e.code, {"raw": body.decode(errors="replace")[:120]}


# ── the door ──────────────────────────────────────────────────────────────────
check("no token is refused", get("/export/regions")[0] == 401)
check("a wrong token is refused", get("/export/regions", "not-the-token")[0] == 401)
st, adv = get("/export/regions", TOKEN)
check("the right token is let in", st == 200, str(st))

# ── what the peer sees ────────────────────────────────────────────────────────
rows = adv.get("regions") or []
check("only the shared area is advertised", [r["source"].replace("_", "-") for r in rows] == [SHARED],
      json.dumps([r["source"] for r in rows]))
# The whole reason use_when_export exists. An advertisement written for one backbone's hop 0 has no
# reason to be true in another's, so a peer must never be shown the local one by accident.
check("  and with the line written for a peer, not the local one",
      rows and rows[0]["use_when"] == EXPORT_LINE, rows[0]["use_when"] if rows else "")
local = next(r for r in get("/regions")[1]["regions"] if r["source"].replace("_", "-") == SHARED)
check("  which is not the line its own hop 0 shows", local["use_when"] != EXPORT_LINE)
# Staleness across a link needs no clock: git already numbers every state this repository has been in.
check("the advertisement says which revision it came from",
      len(str(adv.get("revision") or "")) == 40, str(adv.get("revision"))[:12])
check("the address it prints is on the export surface",
      rows and str(rows[0].get("fetch") or "").startswith("/v1/export/"), rows[0].get("fetch") if rows else "")

# ── what the peer must not see ────────────────────────────────────────────────
check("the shared area's own table crosses", get(f"/export/regions/{SHARED}", TOKEN)[0] == 200)
if PRIVATE:
    check("an area nobody shared does not", get(f"/export/regions/{PRIVATE}", TOKEN)[0] == 404)
    # 404 and not 403, deliberately: whether this backbone holds something it has not shared is itself
    # not the peer's business, so the two answers have to be indistinguishable.
    check("  and says 404, not 'exists but forbidden'",
          (get(f"/export/regions/{PRIVATE}", TOKEN)[1].get("error") or "").lower().count("forbid") == 0)

nodes = Store(repo).nodes()
shared_node = next((n["id"] for n in nodes if n.get("region") == SHARED.replace("-", "_")), None)
private_node = next((n["id"] for n in nodes if PRIVATE and n.get("region") == PRIVATE.replace("-", "_")), None)
if shared_node: check("a node inside the shared area crosses", get(f"/export/nodes/{shared_node}", TOKEN)[0] == 200)
if private_node:
    check("a node inside a private area does not", get(f"/export/nodes/{private_node}", TOKEN)[0] == 404,
          private_node)
    check("  though it reads perfectly well locally", get(f"/nodes/{private_node}")[0] == 200)

# ── a link is read-only ───────────────────────────────────────────────────────
# Not a limitation waiting to be lifted. Two ontologies that write to each other have been merged,
# and merging them is the thing a link exists to avoid.
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/export/regions", method="POST",
                             data=b"{}", headers={"Content-Type": "application/json", "X-Peer-Token": TOKEN})
try:
    urllib.request.urlopen(req, timeout=10); code = 200
except urllib.error.HTTPError as e: code = e.code
except Exception: code = 0
check("a write across the link is refused", code == 405, str(code))

# ── and the local install is untouched by any of it ───────────────────────────
check("the local hop 0 still lists every area",
      len(get("/regions")[1].get("regions") or []) == len(areas), str(len(areas)))


# ══ two backbones, linked both ways ═══════════════════════════════════════════
# Everything above is one install deciding what to show. This is the link itself: what an agent at A
# sees of B, and — the part that matters — what A is entitled to say when B cannot be reached.
PORT_B = PORT + 1
TOKEN_B = "peer-check-token-b"
repo_b = os.path.join(T, "repo-b")
shutil.copytree(seed, repo_b)

# B shares a different area, so a row appearing at A can only have come across the link.
areas_b = sorted(d for d in os.listdir(os.path.join(repo_b, "regions"))
                 if os.path.isdir(os.path.join(repo_b, "regions", d)))
_need_areas(areas_b, 1, "the seed")
SHARED_B = areas_b[-1] if areas_b[-1] != SHARED else areas_b[0]
EXPORT_B = "what the other office may ask us · the questions we answer for them"
for f in sorted(os.listdir(os.path.join(repo_b, "regions", SHARED_B))):
    q = os.path.join(repo_b, "regions", SHARED_B, f)
    text = open(q, encoding="utf-8").read()
    if "\nrole: representative\n" in text and "\nparent:" not in text:
        open(q, "w", encoding="utf-8").write(
            text.replace("\nrole: representative\n", f"\nrole: representative\nuse_when_export: {EXPORT_B}\n", 1))
        break

# Each declares the other. `peers.yaml` lives in the repository because who a backbone is linked to
# is part of what it is; the token comes from the environment, the way the LLM key does.
def link(where, name, port, token_env):
    open(os.path.join(where, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: {name}\n    label: {name.upper()}\n"
        f"    url: http://127.0.0.1:{port}\n    token_env: {token_env}\n")

link(repo, "bee", PORT_B, "PEERTOK_B")
link(repo_b, "ay", PORT, "PEERTOK_A")
regenerate(Store(repo_b))
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=peer", "-c", "user.email=p@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo_b, *a], check=True)
subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
subprocess.run(["git", "-C", repo, "-c", "user.name=peer", "-c", "user.email=p@l", "commit", "-qm", "link"], check=True)

tokens = {"PEERTOK_A": TOKEN, "PEERTOK_B": TOKEN_B}
env_b = {**os.environ, **tokens, "ONTOLOGY_DATA": repo_b, "PORT": str(PORT_B),
         "ONTOLOGY_PUBLISH": os.path.join(T, "publish-b"), "ONTOLOGY_PEER_TOKEN": TOKEN_B,
         "ONTOLOGY_PEER_TTL": "0"}
for k in [k for k in env_b if k.startswith("ONTOLOGY_LLM_")]: env_b.pop(k)
b = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                     env=env_b, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
procs.append(b)

# A is restarted so it reads the peers.yaml it now has, and with the token B expects.
procs[0].terminate(); time.sleep(0.6)
env_a = {**env, **tokens, "ONTOLOGY_PEER_TTL": "0"}
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                              env=env_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for port in (PORT, PORT_B):
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def text_at(port, path):
    """A body, as bytes and type. `at` parses JSON and would report a Markdown answer as a failure —
    which is the exact mistake this pair of assertions exists to catch."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1{path}", timeout=20) as x:
            return x.read().decode("utf-8", "replace"), (x.headers.get("Content-Type") or ""), x.status
    except urllib.error.HTTPError as e: return e.read().decode(errors="replace"), "", e.code
    except Exception as e: return f"{type(e).__name__}", "", 0


def at(port, path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1{path}", timeout=20) as x:
            return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read()
        try: return e.code, json.loads(body or b"{}")
        except Exception: return e.code, {"raw": body.decode(errors="replace")[:120]}
    except Exception as e: return 0, {"raw": f"{type(e).__name__}"}


st, hop0 = at(PORT, "/regions")
remote = [r for r in (hop0.get("regions") or []) if r.get("peer")]
check("A's hop 0 carries B's shared area", len(remote) == 1, json.dumps([r.get("source") for r in remote]))
check("  under an address of A's own, not B's",
      remote and str(remote[0]["fetch"]).startswith("/v1/peers/bee/"), remote[0]["fetch"] if remote else "")
check("  with the line B wrote for a peer", remote and remote[0]["use_when"] == EXPORT_B)
check("  and B's revision, so staleness is visible",
      remote and len(str(remote[0].get("peer_revision") or "")) == 40)
check("A's own areas are all still there",
      len([r for r in hop0["regions"] if not r.get("peer")]) == len(areas))

# The document itself, fetched by A on the agent's behalf. The agent never holds B's credential.
if remote:
    st, tbl = at(PORT, remote[0]["fetch"][3:])
    check("A relays B's area table", st == 200, str(st))
    ent = (tbl.get("entries") or [])
    check("  and rewrites the addresses inside it back to A",
          ent and all(str(e.get("fetch") or "/v1/peers/bee").startswith("/v1/peers/bee/") for e in ent),
          json.dumps([e.get("fetch") for e in ent[:2]]))
    # A document body is Markdown, not JSON, on both sides of a link. This module assumed JSON, so
    # every remote document came back as "peer is unreachable" — while the peer was answering 200.
    # Worse than the outage it invented: `reachable` is the flag hop 0 stops claiming absence on, so a
    # parser bug in here was suspending the absence rule and blaming the other backbone for it.
    body = next((e["fetch"] for e in ent if str(e.get("fetch") or "").endswith("/body")), None)
    if body:
        raw, ctype, code = text_at(PORT, body[3:])
        check("  and relays a document as the text it is", code == 200 and len(raw) > 0, f"{code} {len(raw)}b")
        check("    with the type it has on the other side", "markdown" in ctype or "text/" in ctype, ctype)
    if ent:
        st, doc = at(PORT, ent[0]["fetch"][3:])
        check("  and relays a document behind it", st == 200, str(st))

# Both ways. A link that only works in the direction it was built is not a link.
st, hop0b = at(PORT_B, "/regions")
check("B's hop 0 carries A's shared area",
      len([r for r in (hop0b.get("regions") or []) if r.get("peer")]) == 1)

# ── the sentence ──────────────────────────────────────────────────────────────
check("with the link up, absence is claimed over both backbones",
      "BEE" in (hop0.get("absence") or "") and "may say something is absent" in (hop0.get("absence") or ""),
      (hop0.get("absence") or "")[:80])

# ── advertising and withdrawing while everything is running ───────────────────
# Everything above is a steady state that was arranged before anything started. This is the part that
# makes it dynamic routing rather than a static file: an area that begins to advertise appears at the
# far end without anyone restarting anything, and one that stops advertising **goes**, including the
# documents behind it. A withdraw that only hides the row would leave every address still readable —
# which is not a withdraw, it is a missing menu item.
def set_export(where, area, line):
    """Give an area an export line, or take it away. Written the way a person's edit lands: the
    frontmatter, then the derived file, then a commit — the same three steps the API does."""
    for f in sorted(os.listdir(os.path.join(where, "regions", area))):
        q = os.path.join(where, "regions", area, f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in text or "\nparent:" in text: continue
        out = [l for l in text.splitlines(True) if not l.startswith("use_when_export:")]
        if line:
            at = next(i for i, l in enumerate(out) if l.strip() == "role: representative")
            out.insert(at + 1, f"use_when_export: {line}\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(where))
    subprocess.run(["git", "-C", where, "add", "-A"], check=True)
    subprocess.run(["git", "-C", where, "-c", "user.name=peer", "-c", "user.email=p@l",
                    "commit", "-qm", f"{'advertise' if line else 'withdraw'} {area}"], check=True)


def remote_at_a():
    return {str(r["source"]).replace("_", "-"): r
            for r in (at(PORT, "/regions")[1].get("regions") or []) if r.get("peer")}


SECOND = next((a for a in areas_b if a != SHARED_B), None)
if SECOND:
    check("before it advertises, B's second area is not at A", SECOND not in remote_at_a())
    set_export(repo_b, SECOND, "the second area, now speaking to the other office")
    time.sleep(0.4)
    now = remote_at_a()
    check("an area that starts advertising reaches A with no restart", SECOND in now,
          json.dumps(sorted(now)))
    check("  carrying the line it just wrote",
          SECOND in now and "second area" in (now[SECOND]["use_when"] or ""))
    # It is not enough for the row to appear: what it points at has to be readable, or the
    # advertisement is a promise the link cannot keep.
    if SECOND in now:
        check("  and what it points at is readable straight away",
              at(PORT, now[SECOND]["fetch"][3:])[0] == 200)

    # Withdraw. The row goes — and so does the reach. An export surface built from the shared set
    # cannot serve what is no longer in it, which is what makes this a real withdrawal and not a
    # hidden menu entry.
    gone_fetch = now.get(SECOND, {}).get("fetch")
    set_export(repo_b, SECOND, None)
    time.sleep(0.4)
    after = remote_at_a()
    check("an area that stops advertising leaves A's hop 0", SECOND not in after,
          json.dumps(sorted(after)))
    check("  and the area it shared is still there at B, locally",
          at(PORT_B, f"/regions/{SECOND}")[0] == 200)
    if gone_fetch:
        st, body = at(PORT, gone_fetch[3:])
        check("  but is no longer readable across the link", st == 404, str(st))
        check("    and that 404 is B saying no, not a link that failed",
              body.get("reason") == "peer_said_no", json.dumps(body)[:90])
    check("  while everything B never stopped advertising is untouched", SHARED_B in after)

# ── a link that is up and carrying nothing ────────────────────────────────────
# The state every fresh install is in: an exchange is wired from the first `docker compose up` and has
# nothing to reflect yet. A link that brings no rows adds nothing to the world, so the plain sentence
# is not merely acceptable — it is the accurate one. Naming the link would promise rows that are not
# coming, and on a one-backbone install it announced "the backbones it is linked to (EXCHANGE)",
# calling a backbone the one thing that is careful not to be one.
_had = {}
for a in areas_b:
    for f in sorted(os.listdir(os.path.join(repo_b, "regions", a))):
        t = open(os.path.join(repo_b, "regions", a, f), encoding="utf-8").read()
        if "\nrole: representative\n" not in t or "\nparent:" in t: continue
        line = next((l.split(":", 1)[1].strip() for l in t.splitlines()
                     if l.startswith("use_when_export:")), None)
        if line: _had[a] = line
        break
for a in _had: set_export(repo_b, a, None)
time.sleep(0.4)
st, bare = at(PORT, "/regions")
check("a link carrying nothing leaves the plain sentence alone",
      "linked to" not in (bare.get("absence") or "") and "reaches through" not in (bare.get("absence") or ""),
      (bare.get("absence") or "")[:80])
check("  and absence may still be claimed", "may say something is absent" in (bare.get("absence") or ""))
check("  while the link itself still reads as up",
      all(l["reachable"] for l in (bare.get("links") or [])))
for a, line in _had.items(): set_export(repo_b, a, line)
time.sleep(0.4)
check("  and it comes back when something is advertised again",
      "reaches through" in (at(PORT, "/regions")[1].get("absence") or ""))

# ── and with it down ──────────────────────────────────────────────────────────
# The whole design rests on "only hop 0 may say something is not here", and that is true because hop
# 0 is the whole world. A link that cannot be read makes it false. There is no smaller honest claim.
b.terminate(); time.sleep(0.8)
st, down = at(PORT, "/regions")
check("with the link down, A still answers", st == 200, str(st))
check("  and still serves its own areas",
      len([r for r in (down.get("regions") or []) if not r.get("peer")]) == len(areas))
check("  and drops the rows it can no longer stand behind",
      len([r for r in (down.get("regions") or []) if r.get("peer")]) == 0)
check("  and says the list is incomplete", "incomplete" in (down.get("absence") or "").lower(),
      (down.get("absence") or "")[:70])
check("  and forbids claiming absence", "do not say anything is absent" in (down.get("absence") or ""))
check("  and names which link, and why",
      any(not l["reachable"] and l["error"] for l in (down.get("links") or [])),
      json.dumps([(l["name"], l["error"]) for l in (down.get("links") or [])])[:100])

# A relayed read now fails as unreachable — which is nobody's claim, and must not read as a 404.
if remote:
    st, err = at(PORT, remote[0]["fetch"][3:])
    check("a read across a dead link is not a 404", st != 404, str(st))
    check("  and says the peer could not be reached, not that it said no",
          err.get("reason") == "peer_unreachable", json.dumps(err)[:90])

# ── and back up ───────────────────────────────────────────────────────────────
# A link that comes back has to come back on its own. Nothing restarts A, nobody presses anything, and
# the claim it stopped making has to return — a backbone that stayed cautious for ever after one blip
# would be as wrong as one that never noticed, and the second failure is the harder one to see because
# everything still works.
procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                              env=env_b, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for _ in range(80):
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT_B}/healthz", timeout=1); break
    except Exception: time.sleep(0.25)
time.sleep(0.5)
st, back = at(PORT, "/regions")
check("a link that comes back is used again, unprompted",
      len([r for r in (back.get("regions") or []) if r.get("peer")]) == 1,
      json.dumps([r.get("source") for r in (back.get("regions") or []) if r.get("peer")]))
check("  and the link reads as up", all(l["reachable"] for l in (back.get("links") or [])))
# The one that matters. Refusing to claim absence is right while a link is down and wrong once it is
# back: a table that is whole again is the grounds for saying something is missing, and staying quiet
# would leave every later answer weaker than the data supports.
check("  and absence may be claimed over both backbones again",
      "may say something is absent" in (back.get("absence") or "")
      and "incomplete" not in (back.get("absence") or "").lower(),
      (back.get("absence") or "")[:80])
check("  and a read across it works again",
      at(PORT, [r for r in back["regions"] if r.get("peer")][0]["fetch"][3:])[0] == 200
      if any(r.get("peer") for r in back.get("regions") or []) else False)

# ── an audience, on a link with no exchange in it ─────────────────────────────
# `use_when_export` opens the door and `export_to` says who is on the list. On a direct link the
# backbone that owns the area does the filtering itself, which it can only do if it can put a name to
# whoever is calling — and a name comes from **one secret per link, used in both directions**. That
# rule is written down in docs/PEERING.md and until now nothing checked what it buys. It buys this.
def set_audience(where, area, names):
    for f in sorted(os.listdir(os.path.join(where, "regions", area))):
        q = os.path.join(where, "regions", area, f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in text or "\nparent:" in text: continue
        out = [l for l in text.splitlines(True) if not l.startswith("export_to:")]
        if names:
            i = next(j for j, l in enumerate(out) if l.startswith("use_when_export:"))
            out.insert(i + 1, "export_to: [" + ", ".join(names) + "]\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(where))
    subprocess.run(["git", "-C", where, "add", "-A"], check=True)
    subprocess.run(["git", "-C", where, "-c", "user.name=peer", "-c", "user.email=p@l",
                    # --allow-empty: setting an audience that is already set is a no-op, and a
                    # helper that dies on one would make the order of the checks load-bearing.
                    "commit", "-q", "--allow-empty", "-m", f"audience {area}"], check=True)


# ── and the rules that stop an audience being written as decoration ──────────
# Read straight out of the validator on a copy, because every one of these is a state a person can
# reach by typing and none of them is visibly wrong in the file. The worst of them is the first: an
# audience on an area that crosses to nobody restricts nothing at all, and reads exactly like a
# restriction that is working.
from service.validate import validate                                    # noqa: E402


def rep_of(where, area):
    for f in sorted(os.listdir(os.path.join(where, "regions", area))):
        q = os.path.join(where, "regions", area, f)
        t = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" in t and "\nparent:" not in t: return q, t
    raise AssertionError(area)


def errors_with(lines, area=None, path=None):
    """Validate a copy of B with those frontmatter lines added to an area's representative."""
    tmp = os.path.join(T, "vcheck"); shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(repo_b, tmp)
    q, t = rep_of(tmp, area or SHARED_B) if path is None else (os.path.join(tmp, path), None)
    if t is None: t = open(q, encoding="utf-8").read()
    at_i = t.index("\nrole: representative\n") + len("\nrole: representative\n") if "\nrole: representative\n" in t \
        else t.index("\n---\n", 4) + 1
    open(q, "w", encoding="utf-8").write(t[:at_i] + "".join(l + "\n" for l in lines) + t[at_i:])
    return validate(Store(tmp)).get("errors") or []


# An area that crosses to nobody. Naming an audience on it restricts nothing, and it is the one of
# these that reads like a working restriction.
UNSHARED_B = next(d for d in sorted(os.listdir(os.path.join(repo_b, "regions")))
                  if os.path.isdir(os.path.join(repo_b, "regions", d)) and d != SHARED_B)
e = errors_with(["export_to: [ay]"], area=UNSHARED_B)
check("an audience with no export line is refused",
      any("export_to without use_when_export" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", "export_to: [Not A Name]"])
check("  and so is a name that could never be a peer's",
      any("not a peer name" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", "export_to: [ay, warehouse]"])
check("while two names are ordinary", not any("export_to" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", "export_to: ay"])
check("  and one name written bare is a list of one", not any("export_to" in x for x in e),
      json.dumps(e[:2]))

# A line written for one named reader. Each of these is dead text that reads like a decision, which
# is why none of them is a warning: the file looks exactly the way somebody meant it to look.
OV = 'use_when_export_for: {ay: "a line only ay is shown"}'
e = errors_with([OV], area=UNSHARED_B)
check("a line for one peer with no line for the rest is refused",
      any("use_when_export_for without use_when_export" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", f'use_when_export_for: {{ay: "{EXPORT_B}"}}'])
check("  and one that repeats the default is refused",
      any("overrides nothing" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", "export_to: [somebody-else]", OV])
check("  and one written for a peer the audience leaves out",
      any("would never be read" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", 'use_when_export_for: {Not A Name: "x"}'])
check("  and one addressed to something that is not a peer name",
      any("not a peer name" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", 'use_when_export_for: {ay: "a | b"}'])
check("  and one carrying a pipe, which is a table cell ending early",
      any("one table cell" in x for x in e), json.dumps(e[:2]))
e = errors_with([f"use_when_export: {EXPORT_B}", "export_to: [ay]", OV])
check("while a line for a peer that is on the list is ordinary",
      not any("use_when_export_for" in x for x in e), json.dumps(e[:2]))

# This pair was set up with a secret each way rather than one between them, which is legal and is
# what most people would write first. Its cost has been invisible until there was something to name.
set_audience(repo_b, SHARED_B, ["ay"])
time.sleep(0.4)
st, closed = at(PORT, "/regions")
check("an audience is closed to a caller that cannot be named",
      not any(r.get("peer") for r in (closed.get("regions") or [])),
      json.dumps([r.get("source") for r in (closed.get("regions") or []) if r.get("peer")]))
# And it is closed properly, not merely unlisted: A still has yesterday's address.
check("  and the address it already had stops working",
      at(PORT, "/peers/bee/regions/" + SHARED_B.replace("_", "-"))[0] == 404)
# The link itself is fine. Nothing here may look like an outage — an outage suspends the absence
# rule, and "you are not on the list" is not a reason to stop knowing what exists.
check("  while the link still reads as up", all(l["reachable"] for l in (closed.get("links") or [])),
      json.dumps(closed.get("links")))
check("  and absence may still be claimed", "may say something is absent" in (closed.get("absence") or ""))

# One secret for the link, in both directions — B now looks A up by the same token A presents.
open(os.path.join(repo_b, "peers.yaml"), "w", encoding="utf-8").write(
    f"peers:\n  - name: ay\n    label: AY\n"
    f"    url: http://127.0.0.1:{PORT}\n    token_env: PEERTOK_B\n")
time.sleep(0.4)
st, named = at(PORT, "/regions")
check("with one secret between them the caller has a name, and is on the list",
      len([r for r in (named.get("regions") or []) if r.get("peer")]) == 1,
      json.dumps([r.get("source") for r in (named.get("regions") or []) if r.get("peer")]))
check("  and the audience is not handed to it",
      "export_to" not in json.dumps(named), json.dumps(named)[:120])
check("  and the document behind it reads",
      at(PORT, [r for r in named["regions"] if r.get("peer")][0]["fetch"][3:])[0] == 200
      if any(r.get("peer") for r in named.get("regions") or []) else False)

# A name that is not ours is not ours, even with the link working perfectly.
set_audience(repo_b, SHARED_B, ["somebody-else"])
time.sleep(0.4)
st, other = at(PORT, "/regions")
check("an audience naming someone else leaves us out",
      not any(r.get("peer") for r in (other.get("regions") or [])),
      json.dumps([r.get("source") for r in (other.get("regions") or []) if r.get("peer")]))
set_audience(repo_b, SHARED_B, [])
time.sleep(0.4)
check("and taking it away puts the area back",
      len([r for r in (at(PORT, "/regions")[1].get("regions") or []) if r.get("peer")]) == 1)

# ── the secret itself: comparing it, rotating it, and where it may travel ────
# One shared secret per link is the whole of a link's authentication, so the three things that can be
# wrong with a shared secret are the three things worth pinning. None of them is visible from a test
# that only asks whether the right token works.
from service.peers import same_secret, public_address, declared                # noqa: E402

check("a secret matches itself", same_secret("abc123", "abc123"))
check("  and nothing else", not same_secret("abc123", "abc124"))
# `==` stops at the first differing byte, so how long it takes says how much of a guess was right.
# Between two organisations that is a way in that needs no bug and nobody's mistake, only patience.
check("  in constant time, not with ==", "compare_digest" in
      open(os.path.join(ROOT, "ontology", "service", "peers.py"), encoding="utf-8").read())
# The empty case is the one that turns a closed link into an open one: a peer with no token
# configured must match nobody, never everybody.
for a, b in ((None, "x"), ("x", None), ("", ""), (None, None), ("", "x"), ("x", "")):
    check(f"  and an empty secret matches nothing ({a!r}, {b!r})", not same_secret(a, b))

# Rotation. Without a second accepted secret the only way to change one is to stop both ends at the
# same moment, which is why nobody does it — and a room makes that worse, because every member's
# link stops at once.
open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
    f"peers:\n  - name: bee\n    label: BEE\n    url: http://127.0.0.1:{PORT_B}\n"
    f"    token_env: PEERTOK_B\n    also_accept_env: PEERTOK_A\n")
os.environ["PEERTOK_A"], os.environ["PEERTOK_B"] = TOKEN, TOKEN_B
d = next(x for x in declared(repo) if x["name"] == "bee")
check("a link presents one secret", d["token"] == TOKEN_B)
check("  and accepts the one being retired beside it", sorted(d["accept"]) == sorted({TOKEN, TOKEN_B}),
      json.dumps(sorted(d["accept"])))
open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
    f"peers:\n  - name: bee\n    label: BEE\n    url: http://127.0.0.1:{PORT_B}\n"
    f"    token_env: PEERTOK_B\n")
d = next(x for x in declared(repo) if x["name"] == "bee")
check("  and with nothing being retired, exactly one", d["accept"] == [TOKEN_B], json.dumps(d["accept"]))

# Where a secret may travel. `http://` inside a compose network or a VPN is the ordinary shape and
# must stay out of the way; `http://` to a public address is a bearer token in clear text on the wire.
for url in ("http://ontology:8100", "http://127.0.0.1:8100", "http://10.1.2.3:8110",
            "http://192.168.0.9", "http://172.16.4.1", "https://ix.partner.example",
            "http://a-name-that-does-not-resolve.invalid"):
    check(f"  {url} is not treated as public", not public_address(url))
# A name that does resolve outside every private range. `example.com` is reserved for this.
check("while http:// to a public address is", public_address("http://example.com"))
check("  and https:// to the same place is not", not public_address("https://example.com"))

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
