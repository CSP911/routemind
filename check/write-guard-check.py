#!/usr/bin/env python3
"""The write path keeps to its own files — the service audit of 2026-11-02.

    ./check/write-guard-check.py [port]

Every finding here was a write that reached somewhere it had no business reaching, or wrote
something that did not read back as what was sent:

  escape        DELETE /v1/regions/%2E%2E removed the whole data repository, .git and all; a node's
                `region` of `..` or `../.git`, and a file named `../../evil.md`, committed files outside
                regions/. The path rule is proved twice: through the API, and by asking the writer
                directly for every input a fuzzer can make — encoded, absolute, dotted, symlinked
  hand edits    a hand edit made while an API write ran was committed under the API's name, or wiped
                by its rollback (`reset --hard` + `clean -fd`); boot recovery wiped them the same way
  read-back     an id of `on`, `017` or `2024-01-01` was written bare and read back as a bool, 15 or a
                date; a kind with a newline in it wrote a second frontmatter line (`status: draft`); a
                hand-edited date took /v1/graph down; a file saved with a BOM "had no frontmatter"
  the rest      a create_only PUT replaced a document under a prefixed id; malformed bodies, an actor
                git refuses, a bad area name in a change set → 500; an unknown status stored as
                published; a no-op edit committed a reformat
"""
import json, os, random, shutil, subprocess, sys, tempfile, threading, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18440
sys.path.insert(0, os.path.join(ROOT, "ontology"))
results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:240]}"))
    return bool(cond)


T = tempfile.mkdtemp(prefix="write-guard-check-")
env0 = {**os.environ, "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
for k in [k for k in env0 if k.startswith("ONTOLOGY_LLM_")]: env0.pop(k)


def git(repo, *a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout.strip()


def repo_from(name, extra=None):
    r = os.path.join(T, name); shutil.copytree(os.path.join(ROOT, "examples", "back-office"), r)
    if extra: extra(r)
    for cmd in (["init", "-q"], ["config", "user.email", "g@g"], ["config", "user.name", "guard"], ["add", "-A"], ["commit", "-qm", "start"]):
        git(r, *cmd)
    return r


procs = []


def start(repo, port):
    h = os.path.join(T, f"harness-{port}"); os.makedirs(h, exist_ok=True)
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")],
                         env={**env0, "ONTOLOGY_DATA": repo, "PORT": str(port), "ONTOLOGY_HARNESS": h},
                         stdout=open(os.path.join(T, f"svc-{port}.log"), "w"), stderr=subprocess.STDOUT)
    procs.append(p)
    for _ in range(120):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); return p
        except Exception: time.sleep(0.25)
    sys.exit("the ontology never answered:\n" + open(os.path.join(T, f"svc-{port}.log")).read()[-1500:])


def stop(p):
    p.terminate()
    try: p.wait(5)
    except Exception: p.kill()


def call(port, method, path, body=None, raw=None, headers=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    h = {"Content-Type": "application/json"}; h.update(headers or {})
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        t = e.read()
        try: return e.code, json.loads(t or b"{}")
        except Exception: return e.code, {"raw": t[:200].decode("utf-8", "replace")}


def tracked(repo): return set(git(repo, "ls-files").splitlines())


try:
    # ── the path rule, asked of the writer directly ────────────────────────────
    from service.write import Writer, WriteError
    r0 = repo_from("unit")
    outside = os.path.join(T, "outside"); os.makedirs(outside)
    os.symlink(outside, os.path.join(r0, "regions", "linked"))           # a directory under regions/ that leads out
    os.symlink(os.path.join(r0, "regions", "expense"), os.path.join(r0, "regions", "alias"))
    w = Writer(Path(r0)); regions = (Path(r0) / "regions").resolve()
    rng = random.Random(20261102)
    toks = [".", "..", "/", "\\", "%2E", "%2F", "%2e%2e", "a", "expense", "linked", "alias", "\0", "~", " ", "\n",
            "é", ".git", "regions", "*", "C:", "//", "-", "x" * 300]
    inputs = ["..", ".", "../.git", "/tmp", "/", "", "expense/..", "expense/../..", "linked", "alias", ".git",
              "%2E%2E", "..%2F", "expense\0", " expense", "regions/../..", "\\..\\..", str(Path(r0)), "x" * 300]
    inputs += ["".join(rng.choice(toks) for _ in range(rng.randint(1, 5))) for _ in range(3000)]
    inputs += [urllib.parse.unquote(s) for s in inputs]
    escaped, refused, allowed = [], 0, 0
    for s in inputs:
        for new in (False, True):
            try: d = w.area_dir(s, new=new)
            except WriteError as e:
                refused += 1
                if e.status >= 500: escaped.append((s, new, f"{e.status} {e}"))
                continue
            except Exception as e:
                escaped.append((s, new, f"raised {type(e).__name__}: {e}")); continue
            allowed += 1
            if not (d.parent == Path(r0) / "regions" and d.resolve().parent == regions and not d.is_symlink()
                    and d.name == s and "/" not in s and s not in (".", "..")):
                escaped.append((s, new, str(d)))
            # and the file inside it is a direct child of that directory, for every id the fuzzer makes
            for eid in ("ok-id", "..", "../../evil", "/abs", "a/b", s):
                try: p = w.entity_path(s, eid)
                except WriteError as e:
                    if e.status >= 500: escaped.append((s, eid, f"{e.status} {e}"))
                    continue
                if not (p.parent == d and p.resolve().parent.parent == regions and p.name == f"{eid}.md"):
                    escaped.append((s, eid, str(p)))
    check(f"the writer's area rule: {len(inputs) * 2} inputs (encoded, absolute, dotted, symlinked), "
          f"none resolves outside regions/ or to anything but a direct child of it ({allowed} allowed, {refused} refused)",
          not escaped and refused > 0 and allowed > 0, escaped[:4])
    for s in ("linked", "alias"):
        try: w.area_dir(s); ok = False
        except WriteError: ok = True
        except Exception: ok = False
        check(f"  a symlink under regions/ ({s}) is not an area anything is written into or deleted", ok)

    # ── through the API ──────────────────────────────────────────────────────
    repo = repo_from("api")
    P = PORT; svc = start(repo, P)
    h0 = git(repo, "rev-parse", "HEAD"); files0 = tracked(repo)

    def intact(label):
        ok = (os.path.isdir(os.path.join(repo, ".git")) and git(repo, "rev-parse", "HEAD") == h0
              and git(repo, "status", "--porcelain") == "" and tracked(repo) == files0)
        check(f"  {label}: no commit, the tree is clean, every file is where it was", ok,
              f"head moved {git(repo, 'rev-parse', 'HEAD') != h0}, status {git(repo, 'status', '--porcelain')[:120]!r}")

    for raw in ("%2E%2E", "%2E", "..%2F..", ".git", "%2Fetc", "expense%2F..%2F..", "%2E%2E%2F.git"):
        st, d = call(P, "DELETE", f"/v1/regions/{raw}")
        check(f"DELETE /v1/regions/{raw} is refused as a request, not a 500", 400 <= st < 500, f"{st} {d}")
        intact(f"DELETE {raw}")
    for reg in (".", "..", "../.git", "/tmp", "expense/../..", "expense/."):
        st, d = call(P, "POST", "/v1/nodes", {"name": "trav", "id": "trav-x", "one_liner": "x", "region": reg, "kind": "rule"})
        check(f"POST /v1/nodes with region {reg!r} is refused, 4xx", 400 <= st < 500, f"{st} {str(d)[:160]}")
        intact(f"region {reg!r}")
    for name in ("../../evil.md", "/abs.md", "a/b.md", "..md", "INDEX.md", "../.git/x.md"):
        st, d = call(P, "POST", "/v1/nodes", {"name": "Evil host", "id": "evil-host", "one_liner": "x", "region": "expense",
                                              "parent": "expense", "kind": "rule",
                                              "files": [{"name": name, "description": "d", "content": "c"}]})
        check(f"files[].name {name!r} on a create is refused, 4xx", 400 <= st < 500, f"{st} {str(d)[:160]}")
        intact(f"files[] {name!r}")
    check("  and nothing named evil.md exists anywhere in the data directory",
          not any("evil" in f for _, _, fs in os.walk(repo) for f in fs))

    # ── read-back: what is written reads back as what was sent ─────────────
    for nid in ("on", "off", "yes", "true", "null", "017", "0x1a", "2024-01-01", "1e3"):
        st, d = call(P, "POST", "/v1/nodes", {"name": f"Read back {nid}", "id": nid, "one_liner": "an id YAML would misread",
                                              "region": "expense", "parent": "expense", "kind": "rule"})
        gst, g = call(P, "GET", f"/v1/nodes/{nid}")
        check(f"an id of {nid!r} is created and reads back as the string {nid!r}", st == 201 and gst == 200 and g.get("id") == nid,
              f"{st} {str(d)[:140]} / {gst} {str(g)[:80]}")
    st, d = call(P, "POST", "/v1/nodes", {"name": "Kind inject", "id": "kind-inject", "one_liner": "x", "region": "expense",
                                          "parent": "expense", "kind": "rule\nstatus: draft"})
    gst, g = call(P, "GET", "/v1/nodes/kind-inject")
    check("a kind with a newline does not write a second frontmatter line (it is refused, or stored as typed)",
          (400 <= st < 500) or (gst == 200 and g.get("status") != "draft" and g.get("kind") == "rule\nstatus: draft"),
          f"{st} {str(d)[:140]} / {gst} {str(g)[:120]}")
    st, d = call(P, "POST", "/v1/nodes", {"name": "Face inject", "id": "face-inject", "one_liner": "x", "region": "expense",
                                          "parent": "expense", "kind": "rule", "injected_by": "x\nrole: representative"})
    gst, g = call(P, "GET", "/v1/nodes/face-inject")
    check("injected_by with a newline does not make a second face",
          (400 <= st < 500) or (gst == 200 and g.get("role") != "representative"), f"{st} {str(d)[:120]} / {str(g)[:120]}")
    st, d = call(P, "POST", "/v1/nodes", {"name": "Colon by", "id": "colon-by", "one_liner": "x", "region": "expense",
                                          "parent": "expense", "kind": "rule", "injected_by": "a: b"})
    gst, g = call(P, "GET", "/v1/nodes/colon-by")
    check("injected_by of `a: b` is stored as typed", st == 201 and g.get("injected_by") == "a: b", f"{st} {str(d)[:120]} / {str(g)[:120]}")
    st, d = call(P, "POST", "/v1/nodes", {"name": "nel\x85x", "id": "nel-name", "one_liner": "line\u2028sep", "region": "expense",
                                          "parent": "expense", "kind": "rule"})
    gst, g = call(P, "GET", "/v1/nodes/nel-name")
    check("a name with NEL and a line with U+2028 read back as sent", st == 201 and g.get("name") == "nel\x85x"
          and g.get("one_liner") == "line\u2028sep", f"{st} {str(d)[:120]} / {g.get('name')!r} {g.get('one_liner')!r}")
    st, d = call(P, "POST", "/v1/nodes", {"name": "Bogus status", "id": "bogus-status", "one_liner": "x", "region": "expense",
                                          "parent": "expense", "kind": "rule", "status": "bogus"})
    check("a status that is neither draft nor published is refused, not stored as published", 400 <= st < 500, f"{st} {str(d)[:120]}")

    # ── a document under a prefixed id is that document (create_only never replaces) ──
    st1, d1 = call(P, "PUT", "/v1/nodes/corp-card/files/evidence.md", {"content": "# One\n", "description": "first", "create_only": True})
    st2, d2 = call(P, "PUT", "/v1/nodes/corp-card/files/evidence.md", {"content": "# Two\n", "description": "second", "create_only": True})
    gst, g = call(P, "GET", f"/v1/nodes/{d1.get('id')}")
    check("create_only on a stem taken elsewhere: the first is made under the holder's prefix", st1 == 200 and d1.get("id") == "corp-card-evidence", f"{st1} {str(d1)[:120]}")
    check("  and a second create_only of the same name is refused, not written over it", st2 == 409 and "One" in (g.get("body") or ""),
          f"{st2} {str(d2)[:120]} / body {str(g.get('body'))[:40]!r}")
    st3, d3 = call(P, "PUT", "/v1/nodes/corp-card/files/evidence.md", {"content": "# Three\n"})
    gst, g = call(P, "GET", "/v1/nodes/corp-card-evidence")
    check("  an edit of evidence.md on corp-card edits that document, and keeps its line",
          st3 == 200 and d3.get("id") == "corp-card-evidence" and "Three" in (g.get("body") or "") and g.get("one_liner") == "first",
          f"{st3} {str(d3)[:120]}")
    dst, dd = call(P, "DELETE", "/v1/nodes/corp-card/files/evidence.md")
    check("  and DELETE …/files/evidence.md removes it", dst == 200 and call(P, "GET", "/v1/nodes/corp-card-evidence")[0] == 404, f"{dst} {str(dd)[:120]}")
    check("  the global `evidence` is untouched throughout", call(P, "GET", "/v1/nodes/evidence")[1].get("parent") != "corp-card")

    # ── malformed bodies are the caller's mistake: 400, nothing written ───
    h1 = git(repo, "rev-parse", "HEAD")
    bad = [("POST", "/v1/nodes", b"[1,2]"), ("POST", "/v1/nodes", b'"x"'), ("POST", "/v1/nodes", b"\xff\xfe{"),
           ("POST", "/v1/nodes", json.dumps({"name": ["a"], "one_liner": "x", "region": "expense", "kind": "rule"}).encode()),
           ("POST", "/v1/nodes", json.dumps({"name": 7, "one_liner": "x", "region": "expense", "kind": "rule"}).encode()),
           ("POST", "/v1/nodes", json.dumps({"name": "N", "one_liner": {"a": 1}, "region": "expense", "kind": "rule"}).encode()),
           ("POST", "/v1/nodes", json.dumps({"name": "N", "one_liner": "x", "region": "expense", "kind": "rule", "content": 5}).encode()),
           ("POST", "/v1/nodes", json.dumps({"name": "N", "one_liner": "x", "region": "expense", "kind": "rule", "files": "abc"}).encode()),
           ("POST", "/v1/nodes", b'{"name": NaN, "one_liner": "x", "region": "expense", "kind": "rule"}'),
           ("PUT", "/v1/nodes/corp-card", json.dumps({"one_liner": 5}).encode()),
           ("PUT", "/v1/nodes/corp-card/files/x.md", json.dumps({"content": {"a": 1}, "description": "d"}).encode()),
           ("PUT", "/v1/nodes/corp-card/files/x.md", json.dumps({"content": "---\n: : [\n---\nbody\n", "description": "d"}).encode()),
           ("POST", "/v1/regions", json.dumps({"source": "zz", "representative": {"name": ["n"], "one_liner": "o", "use_when": "u"}}).encode()),
           ("POST", "/v1/regions", b"[]")]
    for m, path, raw in bad:
        st, d = call(P, m, path, raw=raw)
        check(f"{m} {path} {raw[:40]!r} → 400", st == 400, f"{st} {str(d)[:140]}")
    check("  none of them committed anything, and the tree is clean", git(repo, "rev-parse", "HEAD") == h1 and git(repo, "status", "--porcelain") == "")

    # ── an actor git would refuse is a name, not a 500 ─────────────────────
    for i, a in enumerate(("%3C%3E", "%2C", "%00x", "a%0Ab", "%3Cevil%40x%3E")):
        st, d = call(P, "POST", "/v1/nodes", {"name": f"Actor {i}", "id": f"actor-{i}", "one_liner": "x", "region": "expense",
                                              "parent": "expense", "kind": "rule"}, headers={"X-Actor": a})
        author = git(repo, "log", "-1", "--format=%an <%ae>") if st == 201 else ""
        check(f"X-Actor {a} → the write succeeds and the author is one plain line", st == 201 and "\n" not in author
              and author.count("<") == 1 and author.count(">") == 1, f"{st} {str(d)[:120]} {author!r}")

    # ── change sets: an area name create_region refuses is refused here too ───
    for area in ("it-", "it--x", "a" * 300, "../x", "Upper"):
        st, d = call(P, "POST", "/v1/changes", {"why": "t", "dry_run": True, "decisions": [
            {"op": "create", "ref": "$a", "name": "Area", "one_liner": "an area", "parent": None, "area": area, "use_when": "when"}]})
        check(f"a change set making area {area[:12]!r}… is refused, 4xx", 400 <= st < 500, f"{st} {str(d)[:140]}")
    st, d = call(P, "POST", "/v1/changes", {"why": "t", "dry_run": True, "decisions": [{"op": "write", "id": "corp-card", "content": {"a": 1}}]})
    check("a change set writing content that is not text is refused, 4xx", 400 <= st < 500, f"{st} {str(d)[:140]}")

    # ── a no-op edit is no change ─────────────────────────────────────────
    h2 = git(repo, "rev-parse", "HEAD")
    st, d = call(P, "PUT", "/v1/nodes/expense", {"parent": None})
    st2, d2 = call(P, "PUT", "/v1/nodes/corp-card", {"one_liner": call(P, "GET", "/v1/nodes/corp-card")[1].get("one_liner", "")})
    check("PUT {parent: null} on a face, and a line set to what it already says: no commit",
          st == 200 and st2 == 200 and git(repo, "rev-parse", "HEAD") == h2, f"{st} {str(d)[:100]} / {st2} {str(d2)[:100]}")
    stop(svc)

    # ── hand-edited values YAML reads as something else, and a BOM ────────
    def hand(r):
        p = os.path.join(r, "regions", "expense", "card-loss.md")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write("\ufeff" + t)                 # PowerShell 5's Set-Content -Encoding UTF8
        p = os.path.join(r, "regions", "expense", "2024-01-01.md")
        open(p, "w", encoding="utf-8").write("---\nid: 2024-01-01\nname: \"A dated rule\"\nkind: rule\none_liner: \"x\"\nparent: expense\n---\nbody\n")
    repo = repo_from("hand", hand)
    svc = start(repo, P + 1)
    st, g = call(P + 1, "GET", "/v1/nodes/2024-01-01")
    check("a hand-written `id: 2024-01-01` reads back as that id", st == 200 and g.get("id") == "2024-01-01", f"{st} {str(g)[:160]}")
    st, g = call(P + 1, "GET", "/v1/graph"); check("  and /v1/graph answers", st == 200, f"{st} {str(g)[:160]}")
    st, g = call(P + 1, "GET", "/v1/nodes/card-loss")
    check("a file saved with a UTF-8 BOM is read as having frontmatter", st == 200 and g.get("id") == "card-loss", f"{st} {str(g)[:160]}")
    st, v = call(P + 1, "POST", "/v1/validate")
    check("  and the repository validates with both", st == 200, f"{st} {str(v)[:300]}")
    stop(svc)

    # ── a hand edit made while a write runs is neither committed nor wiped ──
    def bulk(r):
        for i in range(3000):
            open(os.path.join(r, "regions", "expense", f"bulk-{i}.md"), "w", encoding="utf-8").write(
                f"---\nid: bulk-{i}\nname: \"Bulk {i}\"\nkind: rule\none_liner: \"bulk {i}\"\nparent: corp-card\n---\nbody {i}\n")
    repo = repo_from("race", bulk)
    svc = start(repo, P + 2)
    marker = os.path.join(repo, ".git", "routemind-transaction")

    def during(method, path, body, edit):
        """Run one write; make `edit` the moment its transaction is open; return the write's answer."""
        out = {}
        t = threading.Thread(target=lambda: out.update(r=call(P + 2, method, path, body))); t.start()
        for _ in range(4000):
            if os.path.exists(marker): break
            time.sleep(0.001)
        seen = os.path.exists(marker); edit(); t.join()
        return seen, out["r"]

    hand_md = os.path.join(repo, "regions", "expense", "hand-50.md")
    seen, (st, d) = during("PUT", "/v1/nodes/bulk-3", {"one_liner": "bulk three, edited"}, lambda: open(hand_md, "w", encoding="utf-8").write(
        "---\nid: hand-50\nname: \"Hand\"\nkind: rule\none_liner: \"by hand\"\nparent: corp-card\n---\nhand\n"))
    check("a hand edit landed inside the write's transaction (the race this guards was reached)", seen)
    check("  the API write did not commit the hand-made file", "regions/expense/hand-50.md" not in tracked(repo), f"{st} {str(d)[:140]}")
    check("  and the hand-made file is still on disk", os.path.exists(hand_md))
    os.remove(hand_md); git(repo, "checkout", "--", ".")
    # A create makes its area's directory with exist_ok — the area is not the transaction's to claim.
    seen, (st, d) = during("POST", "/v1/nodes", {"name": "Raced create", "id": "raced-create", "one_liner": "x", "region": "expense",
                                                 "parent": "corp-card", "kind": "rule"}, lambda: open(hand_md, "w", encoding="utf-8").write(
        "---\nid: hand-50\nname: \"Hand\"\nkind: rule\none_liner: \"by hand\"\nparent: corp-card\n---\nhand\n"))
    check("a create in the area a person is saving into does not commit their file", seen and "regions/expense/hand-50.md" not in tracked(repo)
          and os.path.exists(hand_md), f"{seen} {st} {str(d)[:140]}")
    os.remove(hand_md); git(repo, "checkout", "--", ".")
    h3 =git(repo, "rev-parse", "HEAD")
    b10 = os.path.join(repo, "regions", "expense", "bulk-10.md"); notes = os.path.join(repo, "notes.txt")
    seen, (st, d) = during("PUT", "/v1/nodes/bulk-3", {"kind": "no-such-kind"},
                           lambda: (open(b10, "a", encoding="utf-8").write("appended by hand\n"), open(notes, "w").write("mine\n")))
    check("a failing write while a person edits: the write is refused", seen and st >= 400 and git(repo, "rev-parse", "HEAD") == h3, f"{seen} {st} {str(d)[:120]}")
    check("  and its rollback leaves both of the person's edits as they were",
          os.path.exists(notes) and "appended by hand" in open(b10, encoding="utf-8").read())
    stop(svc)

    # ── boot recovery rolls back the interrupted write's own files, and only those ──
    repo = repo_from("boot")
    mine = os.path.join(repo, "regions", "expense", "corp-card.md"); theirs = os.path.join(repo, "regions", "payroll", "payroll.md")
    open(mine, "a", encoding="utf-8").write("half a transaction\n")
    open(theirs, "a", encoding="utf-8").write("a person's edit\n")
    open(os.path.join(repo, ".git", "routemind-transaction"), "w", encoding="utf-8").write(
        "routemind-transaction v2\nnode corp-card: update\nregions/expense/corp-card.md\nregions.json\n")
    svc = start(repo, P + 3)
    check("boot recovery rolls back the file the interrupted write had touched", "half a transaction" not in open(mine, encoding="utf-8").read())
    check("  and leaves a hand edit it never touched as it is", "a person's edit" in open(theirs, encoding="utf-8").read())
    stop(svc)
    # ── what an operating system leaves behind is nobody's edit ───────────────
    # Opening data/repo in Finder leaves .DS_Store; every write was then refused as "edited by hand",
    # and the map stopped saving (verification pass, 2026-11-02). Never committed either.
    repo = repo_from("litter")
    for f in (".DS_Store", "regions/expense/.DS_Store", "regions/._corp-card.md", "Thumbs.db"):
        open(os.path.join(repo, f), "w").write("x")
    svc = start(repo, P + 4)
    st, b = call(P + 4, "PUT", "/v1/nodes/corp-card", {"one_liner": "Corporate card rules, with Finder open"})
    check("a .DS_Store, an AppleDouble file or a Thumbs.db does not refuse a write", st == 200, f"{st} {b}")
    check("  and none of them is committed", not any(f in tracked(repo) for f in (".DS_Store", "regions/expense/.DS_Store", "Thumbs.db")))
    open(os.path.join(repo, "regions", "expense", "notes.txt"), "w").write("a person's file")
    st, b = call(P + 4, "PUT", "/v1/nodes/corp-card", {"one_liner": "Corporate card rules, again"})
    check("  while a real stray file still does", st == 409 and b.get("reason") == "tree_dirty", f"{st} {b}")
    stop(svc)
finally:
    for p in procs:
        if p.poll() is None: stop(p)
    shutil.rmtree(T, ignore_errors=True)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
