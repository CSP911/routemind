#!/usr/bin/env python3
"""Three backbones meeting at one exchange.

    ./check/exchange-check.py [port]

Starts three backbones and an exchange on throwaway repositories. Needs pyyaml on this python; see
check/write-paths.sh for the same requirement.

check/peer-check.py covers one link. This covers what a room full of them has to get right, and every
one of these has a way of looking fine while being wrong:

  * **The arithmetic.** Three backbones that all want to see each other need three links through here
    and six without. That is the only reason an exchange exists.
  * **Split horizon.** A member must never be handed back what it advertised. Without it every
    backbone sees its own areas twice under two addresses, and the second copy looks like somebody
    else's.
  * **The path.** Knowledge two hops away arrives as `/v1/peers/ix/peers/branch/…`, and everything
    that reads an address has to peel *every* prefix, not one.
  * **The exchange is not a backbone.** No areas, no hop 0, no `/v1/regions`. If it ever grows one,
    the absence rule has a third kind of thing to be wrong about.

docs/PEERING.md is the contract.
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = int(sys.argv[1]) if len(sys.argv) > 1 else 8181
IX_PORT = BASE + 10
IX = "ix"
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

T = tempfile.mkdtemp(prefix="exchange-check-")
seed = os.path.join(ROOT, "examples", "back-office")
if not os.path.isdir(seed): seed = os.path.join(ROOT, "seed")
sys.path.insert(0, os.path.join(ROOT, "ontology"))
from service.store import Store                                          # noqa: E402
from service.derive import regenerate                                    # noqa: E402

# Three backbones, each sharing one area, each a different one — so a row arriving anywhere can only
# have come across the link that carries it.
NAMES = ["alpha", "beta", "gamma"]
def _need_areas(names, n, what):
    """These checks share areas between backbones, so they need a seed with at least `n` of them.

    The ontology image ships `seed/` with no areas and no `examples/`, which is right — an install
    starts empty — and means running this inside a container ends in `IndexError: list index out of
    range` from the slice below. A refusal that names neither the mistake nor the fix is the thing
    this repository keeps finding in its own code; it should not be in the checks that find it.
    """
    if len(names) >= n: return names
    print(f"this check needs a seed with at least {n} area{'s' if n > 1 else ''} to share between "
          f"backbones, and {what} "
          f"has {len(names)}.\nRun it on the host, where examples/back-office is — the ontology image "
          f"ships an empty seed on purpose.")
    raise SystemExit(2)

areas_all = sorted(d for d in os.listdir(os.path.join(seed, "regions"))
                   if os.path.isdir(os.path.join(seed, "regions", d)))
_need_areas(areas_all, 3, "the seed")
SHARE = dict(zip(NAMES, areas_all))
LINE = {n: f"what {n} answers for the others · questions that belong to {n}" for n in NAMES}
PORTS = {n: BASE + i for i, n in enumerate(NAMES)}
TOKENS = {n: f"tok-{n}" for n in NAMES}
repos = {}

for n in NAMES:
    repo = os.path.join(T, n); shutil.copytree(seed, repo); repos[n] = repo
    for f in sorted(os.listdir(os.path.join(repo, "regions", SHARE[n]))):
        q = os.path.join(repo, "regions", SHARE[n], f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" in text and "\nparent:" not in text:
            open(q, "w", encoding="utf-8").write(
                text.replace("\nrole: representative\n",
                             f"\nrole: representative\nuse_when_export: {LINE[n]}\n", 1))
            break
    # One entry, not two. That is the arithmetic: everybody names the exchange and nobody names
    # anybody else. Six links become three, and adding a fourth backbone costs one more, not three.
    open(os.path.join(repo, "peers.yaml"), "w", encoding="utf-8").write(
        f"peers:\n  - name: {IX}\n    label: EXCHANGE\n"
        f"    url: http://127.0.0.1:{IX_PORT}\n    kind: exchange\n    token_env: TOK_{n.upper()}\n")
    regenerate(Store(repo))
    for a in (["init", "-q"], ["add", "-A"],
              ["-c", "user.name=x", "-c", "user.email=x@l", "commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", repo, *a], check=True)

env_tokens = {f"TOK_{n.upper()}": TOKENS[n] for n in NAMES}

open(os.path.join(T, "members.yaml"), "w", encoding="utf-8").write(
    "members:\n" + "".join(
        f"  - name: {n}\n    label: {n.upper()}\n    url: http://127.0.0.1:{PORTS[n]}\n"
        f"    token_env: TOK_{n.upper()}\n" for n in NAMES))

for n in NAMES:
    e = {**os.environ, **env_tokens, "ONTOLOGY_DATA": repos[n], "PORT": str(PORTS[n]),
         "ONTOLOGY_PUBLISH": os.path.join(T, f"pub-{n}"),
         "ONTOLOGY_PEER_TOKEN": TOKENS[n], "ONTOLOGY_PEER_TTL": "0"}
    for k in [k for k in e if k.startswith("ONTOLOGY_LLM_")]: e.pop(k)
    procs.append(subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                                  env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

ix_env = {**os.environ, **env_tokens, "EXCHANGE_NAME": IX, "PORT": str(IX_PORT),
          "EXCHANGE_MEMBERS": os.path.join(T, "members.yaml"), "ONTOLOGY_PEER_TTL": "0"}
ix = subprocess.Popen([sys.executable, os.path.join(ROOT, "exchange", "server.py")],
                      env=ix_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
procs.append(ix)

for port in [*PORTS.values(), IX_PORT]:
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)


def get(port, path, token=None, raw=False):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
    if token: r.add_header("X-Peer-Token", token)
    try:
        with urllib.request.urlopen(r, timeout=20) as x:
            body = x.read()
            return x.status, (body.decode("utf-8", "replace") if raw else json.loads(body or b"{}"))
    except urllib.error.HTTPError as e:
        body = e.read()
        if raw: return e.code, body.decode(errors="replace")
        try: return e.code, json.loads(body or b"{}")
        except Exception: return e.code, {"raw": body.decode(errors="replace")[:120]}
    except Exception as e: return 0, {"raw": type(e).__name__}


# ── the exchange is not a backbone ────────────────────────────────────────────
check("an exchange has no hop 0", get(IX_PORT, "/v1/regions", TOKENS["alpha"])[0] == 404)
check("  nor a repository to publish", get(IX_PORT, "/v1/core", TOKENS["alpha"])[0] == 404)
def post(port, path, token):
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=b"{}", method="POST",
                               headers={"Content-Type": "application/json", "X-Peer-Token": token})
    try:
        urllib.request.urlopen(r, timeout=10); return 200
    except urllib.error.HTTPError as e: e.read(); return e.code
    except Exception: return 0


check("  and refuses a write", post(IX_PORT, "/v1/export/regions", TOKENS["alpha"]) == 405,
      str(post(IX_PORT, "/v1/export/regions", TOKENS["alpha"])))

# ── the door ──────────────────────────────────────────────────────────────────
check("an unknown token is refused", get(IX_PORT, "/v1/export/regions", "nope")[0] == 401)
check("no token is refused", get(IX_PORT, "/v1/export/regions")[0] == 401)
st, adv = get(IX_PORT, "/v1/export/regions", TOKENS["alpha"])
check("a member's own token is let in", st == 200, str(st))

# ── split horizon ─────────────────────────────────────────────────────────────
origins = sorted({r["origin"] for r in (adv.get("regions") or [])})
check("alpha is offered the other two, and not itself", origins == ["beta", "gamma"],
      json.dumps(origins))
st, adv_b = get(IX_PORT, "/v1/export/regions", TOKENS["beta"])
check("  and beta the other two, and not itself",
      sorted({r["origin"] for r in (adv_b.get("regions") or [])}) == ["alpha", "gamma"])

# ── the path ──────────────────────────────────────────────────────────────────
row = next((r for r in (adv.get("regions") or []) if r["origin"] == "gamma"), None)
check("a reflected row says where it came from", row and row.get("path") == ["gamma"],
      json.dumps(row.get("path") if row else None))
check("  and carries the line gamma wrote for a peer", row and row["use_when"] == LINE["gamma"])
check("  and its address goes through the exchange",
      row and str(row["fetch"]).startswith("/v1/export/peers/gamma/"), row["fetch"] if row else "")
check("  and keeps the origin's own revision, not the exchange's digest",
      row and len(str(row.get("origin_revision") or "")) == 40 and row["origin_revision"] != adv["revision"])

# ── an area that crosses to one of them and not the other ────────────────────
# `use_when_export` opens a door; `export_to` says who is on the list. It can only ever narrow, and
# the interesting failure is not that the wrong backbone sees the row — it is that the wrong backbone
# sees the row's *address* and follows it, which nothing in the listing would show.
def set_audience(where, area, names):
    for f in sorted(os.listdir(os.path.join(where, "regions", area))):
        q = os.path.join(where, "regions", area, f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in text or "\nparent:" in text: continue
        out = [l for l in text.splitlines(True) if not l.startswith("export_to:")]
        if names:
            at_i = next(i for i, l in enumerate(out) if l.startswith("use_when_export:"))
            out.insert(at_i + 1, "export_to: [" + ", ".join(names) + "]\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(where))
    subprocess.run(["git", "-C", where, "add", "-A"], check=True)
    subprocess.run(["git", "-C", where, "-c", "user.name=x", "-c", "user.email=x@l",
                    # --allow-empty: setting an audience that is already set is a no-op, and a
                    # helper that dies on one would make the order of the checks load-bearing.
                    "commit", "-q", "--allow-empty", "-m", f"audience {area}"], check=True)


addr = None
row_b = next((r for r in (adv_b.get("regions") or []) if r["origin"] == "alpha"), None)
if row_b: addr = row_b["fetch"]
set_audience(repos["alpha"], SHARE["alpha"], ["beta"])
time.sleep(0.4)

st, to_b = get(IX_PORT, "/v1/export/regions", TOKENS["beta"])
st, to_g = get(IX_PORT, "/v1/export/regions", TOKENS["gamma"])
check("an area named for beta reaches beta",
      "alpha" in {r["origin"] for r in (to_b.get("regions") or [])},
      json.dumps(sorted({r["origin"] for r in (to_b.get("regions") or [])})))
check("  and does not reach gamma",
      "alpha" not in {r["origin"] for r in (to_g.get("regions") or [])},
      json.dumps(sorted({r["origin"] for r in (to_g.get("regions") or [])})))
check("  while gamma's own area still reaches beta",
      "gamma" in {r["origin"] for r in (to_b.get("regions") or [])})
# Who else was on the list is not beta's business. The audience is the room's to apply and nobody
# else's to read.
check("  and beta is not told who else was considered",
      "export_to" not in json.dumps(to_b), json.dumps(to_b)[:160])

# The address is the half a listing filter would miss. gamma knew it a moment ago.
if check("gamma still holds the address from before", bool(addr), str(addr)):
    st, _ = get(IX_PORT, addr, TOKENS["gamma"])
    check("  and following it now gets nothing", st == 404, str(st))
    st, still = get(IX_PORT, addr, TOKENS["beta"])
    check("  while beta still reads it", still if st == 200 else False, str(st))
    # 404 and not 403: whether alpha holds something it has not shared with gamma is itself
    # something gamma has no business learning, and the two answers must be indistinguishable.
    st_unshared, _ = get(IX_PORT, "/v1/export/peers/alpha/regions/nothing-like-this", TOKENS["gamma"])
    check("  the same answer an area that was never shared gives", st_unshared == 404, str(st_unshared))

# Health is not policy: the operator sees what alpha is advertising, not who it chose.
st, opstate = get(IX_PORT, "/v1/export/regions", TOKENS["beta"])
set_audience(repos["alpha"], SHARE["alpha"], [])
time.sleep(0.4)
st, back = get(IX_PORT, "/v1/export/regions", TOKENS["gamma"])
check("taking the audience away puts it back in front of gamma",
      "alpha" in {r["origin"] for r in (back.get("regions") or [])},
      json.dumps(sorted({r["origin"] for r in (back.get("regions") or [])})))

# ── what a backbone makes of it ───────────────────────────────────────────────
st, hop0 = get(PORTS["alpha"], "/v1/regions")
remote = [r for r in (hop0.get("regions") or []) if r.get("peer")]
check("alpha's hop 0 carries both of the others", len(remote) == 2, json.dumps([r["source"] for r in remote]))
check("  under alpha's own addresses, two hops deep",
      all(str(r["fetch"]).startswith("/v1/peers/ix/peers/") for r in remote),
      json.dumps([r["fetch"] for r in remote]))
check("  and its own areas are untouched",
      len([r for r in hop0["regions"] if not r.get("peer")]) == len(areas_all))

# ── and can read across two hops ──────────────────────────────────────────────
if remote:
    st, tbl = get(PORTS["alpha"], remote[0]["fetch"])
    check("a table two backbones away is readable", st == 200, str(st))
    ent = (tbl.get("entries") or [])
    check("  and its rows still point back through the exchange",
          ent and all(str(e.get("fetch") or "/v1/peers/ix/").startswith("/v1/peers/ix/peers/") for e in ent),
          json.dumps([e.get("fetch") for e in ent[:2]]))
    body = next((e["fetch"] for e in ent if str(e.get("fetch") or "").endswith("/body")), None)
    if body:
        st, text = get(PORTS["alpha"], body, raw=True)
        check("  and a document two backbones away arrives as text", st == 200 and len(text) > 0,
              f"{st} {len(text)}b")

# ── the client half of the path ───────────────────────────────────────────────
sys.path.insert(0, os.path.join(ROOT, "mcp"))
import importlib.util as _u                                              # noqa: E402
_spec = _u.spec_from_file_location("kmcp", os.path.join(ROOT, "mcp", "knowledge_mcp.py"))
_m = _u.module_from_spec(_spec); _spec.loader.exec_module(_m)
check("the client peels every hop off an address, not one",
      _m._local("/v1/peers/ix/peers/gamma/regions/payroll") == "/v1/regions/payroll",
      _m._local("/v1/peers/ix/peers/gamma/regions/payroll"))

# ── a member goes quiet ───────────────────────────────────────────────────────
# The exchange must report it rather than answer for it, and alpha must stop claiming absence — the
# rows it can no longer stand behind are two backbones away, and no closer to being its to vouch for.
gamma_proc = procs[NAMES.index("gamma")]
gamma_proc.terminate(); time.sleep(1.0)
st, adv2 = get(IX_PORT, "/v1/export/regions", TOKENS["alpha"])
check("a member that has gone is named, not answered for",
      any(not m["reachable"] and m["name"] == "gamma" for m in (adv2.get("members") or [])),
      json.dumps([(m["name"], m["reachable"]) for m in (adv2.get("members") or [])]))
check("  and its rows are not offered", all(r["origin"] != "gamma" for r in (adv2.get("regions") or [])))
st, hop2 = get(PORTS["alpha"], "/v1/regions")
check("  while alpha still answers, with beta still reachable",
      st == 200 and len([r for r in hop2.get("regions") or [] if r.get("peer")]) == 1, str(st))

# ── advertising through the exchange, and withdrawing again ───────────────────
# The same transition as a direct link, one hop further. It is worth its own assertions because an
# exchange holds a cache and a split-horizon rule between the two backbones, and either could turn a
# withdrawal into something that stays visible — the failure that looks exactly like everything
# working.
def set_export(where, area, line):
    for f in sorted(os.listdir(os.path.join(where, "regions", area))):
        q = os.path.join(where, "regions", area, f)
        text = open(q, encoding="utf-8").read()
        if "\nrole: representative\n" not in text or "\nparent:" in text: continue
        out = [l for l in text.splitlines(True) if not l.startswith("use_when_export:")]
        if line:
            at_i = next(i for i, l in enumerate(out) if l.strip() == "role: representative")
            out.insert(at_i + 1, f"use_when_export: {line}\n")
        open(q, "w", encoding="utf-8").write("".join(out))
        break
    regenerate(Store(where))
    subprocess.run(["git", "-C", where, "add", "-A"], check=True)
    subprocess.run(["git", "-C", where, "-c", "user.name=x", "-c", "user.email=x@l",
                    "commit", "-qm", "flip"], check=True)


def at_alpha():
    return {str(r["source"]).replace("_", "-"): r
            for r in (get(PORTS["alpha"], "/v1/regions")[1].get("regions") or []) if r.get("peer")}


SECOND_B = next((a for a in areas_all if a != SHARE["beta"]), None)
if SECOND_B:
    check("before beta advertises it, alpha does not see it", SECOND_B not in at_alpha())
    set_export(repos["beta"], SECOND_B, "beta's second area, now open to the others")
    time.sleep(0.5)
    now = at_alpha()
    check("an area advertised at beta reaches alpha through the exchange", SECOND_B in now,
          json.dumps(sorted(now)))
    check("  still named as beta's, not the exchange's",
          SECOND_B in now and now[SECOND_B].get("origin") == "beta",
          (now.get(SECOND_B) or {}).get("origin"))
    check("  and readable two hops away",
          SECOND_B in now and get(PORTS["alpha"], now[SECOND_B]["fetch"])[0] == 200)
    # And it must not come back to the one that sent it, cache or no cache. By **origin**, not by
    # name: alpha shares an area with the same name, so a row called that is legitimately at beta —
    # it is alpha's. Asserting on the name made split horizon look broken when it was working, which
    # is a good illustration of why the two backbones in this check share different areas by default.
    beta_sees = get(IX_PORT, "/v1/export/regions", TOKENS["beta"])[1].get("regions") or []
    check("  and nothing of beta's own is offered back to beta",
          all(r.get("origin") != "beta" for r in beta_sees),
          json.dumps([(r.get("source"), r.get("origin")) for r in beta_sees]))

    gone = now.get(SECOND_B, {}).get("fetch")
    set_export(repos["beta"], SECOND_B, None)
    time.sleep(0.5)
    check("withdrawing it removes it from alpha", SECOND_B not in at_alpha())
    if gone:
        st, body = get(PORTS["alpha"], gone)
        check("  and it stops being readable through the exchange", st == 404, str(st))
        check("    as somebody saying no, not as a link that failed",
              body.get("reason") == "peer_said_no", json.dumps(body)[:80])
    check("  and what beta never stopped advertising is untouched",
          SHARE["beta"] in at_alpha())

shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
