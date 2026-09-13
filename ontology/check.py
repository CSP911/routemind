#!/usr/bin/env python3
"""The Knowledge unit's invariants — whether the data model holds itself together.

The four suites in `check/` drive an install from the outside: the API, the screen, the protocol.
This one calls the modules directly and watches what must never happen.

It exists because on 2026-09-11 `set_frontmatter` was destroying the body of every document it
touched and all four suites passed. The transaction committed, the API returned 201, and only the
file was empty. **A check that measures success cannot see a loss that is quiet.** So each thing
here is stated as an absence — the body that must still be there, the draft that must not be
published, the entity that must not be stranded.

Every one of them is proved both ways: reverting the fix makes it fail. A check nobody has watched
fail is a check nobody knows the meaning of.

    python3 ontology/check.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from service.store import set_frontmatter, file_scope, described_by, FM_RE, Store

fails = []


def eq(label, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {label:<52} {got!r}" + ("" if ok else f"  <- expected {want!r}"))
    if not ok: fails.append(label)


# ── frontmatter round-trip: is what was written what comes back ──────────────
BODY = "# Heading\n\nThe body has to survive.\n"
eq("a key added to a document with no frontmatter keeps the body",
   BODY in set_frontmatter(BODY, "described_by", "knowledge"), True)
eq("a key added to a document that has frontmatter keeps the body",
   BODY.strip() in set_frontmatter("---\nscope: common\n---\n" + BODY, "described_by", "knowledge"), True)
eq("writing the same key twice leaves one",
   set_frontmatter(set_frontmatter(BODY, "k", "a"), "k", "b").count("k:"), 1)
eq("the value written reads back",
   described_by(set_frontmatter(BODY, "described_by", "knowledge")), "knowledge")
eq("the key beside it survives",
   file_scope(set_frontmatter("---\nscope: [a1]\n---\n" + BODY, "described_by", "x")), ["a1"])

# ── does everything using FM_RE take the body from group(2) ──────────────────
m = FM_RE.match("---\na: 1\n---\nbody\n")
eq("FM_RE.end() is end-of-file, not where the body starts", "---\na: 1\n---\nbody\n"[m.end():], "")
eq("the body is group(2)", m.group(2), "body\n")

for src in sorted(pathlib.Path(__file__).resolve().parent.joinpath("service").glob("*.py")):
    for i, ln in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        if "m.end()" in ln and "FM_RE" not in ln and not ln.strip().startswith("#"):
            fails.append(f"{src.name}:{i}")
            print(f"FAIL {src.name}:{i:<46} slices the body at m.end() — it is group(2)")

# ── does publishing hold drafts back ─────────────────────────────────────────
# A draft is machine-made and unconfirmed. The moment the agent reads one back as fact, the echo
# the design guards against has started. Under two types this came free: a draft was a directory
# and its files went with it. One type makes containment a field, so the children have to be
# collected — otherwise a child publishes with a `parent` that resolves to nothing.
def _publish_drops_drafts():
    import subprocess, tempfile
    from service.write import publish
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-publish-"))
    repo, pub = t / "repo", t / "pub"
    (repo / "regions" / "alpha").mkdir(parents=True); pub.mkdir()
    (repo / "CORE.md").write_text("| key | description |\n| --- | --- |\n", encoding="utf-8")
    (repo / "vocab.yaml").write_text("budgets: {}\n", encoding="utf-8")
    (repo / "edges.yaml").write_text("[]\n", encoding="utf-8")
    for eid, extra in (("keep", "role: representative"), ("hidden", "status: draft"), ("kid", "parent: hidden")):
        (repo / "regions" / "alpha" / f"{eid}.md").write_text(
            f"---\nid: {eid}\n{extra}\n---\nbody of {eid}\n", encoding="utf-8")
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q)
    subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    publish(repo, pub)
    return {e: (pub / "current" / "regions" / "alpha" / f"{e}.md").exists() for e in ("keep", "hidden", "kid")}


try:
    got = _publish_drops_drafts()
    eq("a draft is not published", got["hidden"], False)
    eq("nor is what hangs under it", got["kid"], False)
    eq("what is not a draft is published", got["keep"], True)
except Exception as e:
    fails.append("publish"); print(f"FAIL {'the publish check could not run':<52} {e}")

# ── does promotion insert a parent ───────────────────────────────────────────
# Promotion is not about identity; it makes room for a sibling (operator, 2026-09-11). There was
# one AWX document. Continua arrives, so the person names the thing that holds them both and AWX
# moves under it. The entity being promoted keeps its id, its name and its body — which is why
# nothing pointing at it has to move. The old promotion minted a new id and had to carry the edges.
def _promote_interposes():
    import shutil, subprocess, tempfile
    from service.write import Writer
    here = pathlib.Path(__file__).resolve().parent.parent
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-promote-"))
    repo, pub = t / "repo", t / "pub"
    shutil.copytree(here / "seed", repo); pub.mkdir()
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q); subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    w = Writer(repo, pub, None)
    # The shape the operator described: one document under an area, and then a second one arrives.
    w.create_region({"source": "lib", "core_description": "l",
                     "representative": {"id": "top", "name": "Top", "kind": "tool",
                                        "one_liner": "the area", "use_when": "when"}}, "c")
    w.create_node({"id": "awx", "name": "AWX", "kind": "tool", "region": "lib", "parent": "top",
                   "one_liner": "what AWX is", "content": "what AWX is for",
                   "edges": [{"from": "top", "rel": "CONSISTS_OF", "to": "awx"}]}, "c")
    w.promote_file("top", "awx.md", {"name": "Orchestration", "one_liner": "holds them",
                                     "id": "orch", "kind": "tool"}, "c")
    after = {n["id"]: n for n in w.store.nodes()}
    edges = w.store.edges()
    return {"holder made": "orch" in after,
            "promoted kept its id": "awx" in after,
            "it moved under the holder": after.get("awx", {}).get("parent"),
            "its body survived": (after.get("awx", {}).get("body") or "").strip(),
            "the holder sits where it did": after.get("orch", {}).get("parent"),
            "the edge still resolves": all(e["from"] in after and e["to"] in after for e in edges)}


try:
    g = _promote_interposes()
    eq("promotion makes the holder", g["holder made"], True)
    eq("the promoted entity keeps its id", g["promoted kept its id"], True)
    eq("it moves under the holder", g["it moved under the holder"], "orch")
    eq("its body survives", g["its body survived"], "what AWX is for")
    eq("the holder stands where it stood", g["the holder sits where it did"], "top")
    eq("the edge that pointed at it still resolves", g["the edge still resolves"], True)
except Exception as e:
    fails.append("promote"); print(f"FAIL {'the promote check could not run':<52} {e}")

# ── does a re-parent across areas move the entity there ──────────────────────
# The operator drags an entity onto a parent in another area. The area is not a field anyone sets —
# it is the directory the file sits in — so the move follows the parent, and the whole subtree goes.
# Leave one child behind and it sits in area A naming a parent in area B, which is the state the
# validator calls an error.
def _move_across():
    import shutil, subprocess, tempfile
    from service.write import Writer, WriteError
    from service.validate import validate
    here = pathlib.Path(__file__).resolve().parent.parent
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-move-"))
    repo, pub = t / "repo", t / "pub"
    shutil.copytree(here / "seed", repo); pub.mkdir()
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q); subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    w = Writer(repo, pub, None)
    for src, nm in (("alpha", "A"), ("beta", "B")):
        w.create_region({"source": src, "core_description": nm,
                         "representative": {"id": f"{src}-top", "name": nm, "kind": "tool",
                                            "one_liner": "the area", "use_when": "when"}}, "c")
    w.create_node({"id": "mover", "name": "Mover", "kind": "tool", "region": "alpha", "parent": "alpha-top",
                   "one_liner": "moves", "content": "the body of mover",
                   "edges": [{"from": "alpha-top", "rel": "CONSISTS_OF", "to": "mover"}]}, "c")
    w.create_node({"id": "carried", "name": "Carried", "kind": "tool", "region": "alpha", "parent": "mover",
                   "one_liner": "carried along", "content": "the body of carried",
                   "edges": [{"from": "mover", "rel": "CONSISTS_OF", "to": "carried"}]}, "c")
    w.update_node("mover", {"parent": "beta-top"}, "c")
    after = {n["id"]: n for n in w.store.nodes()}
    edges = w.store.edges()
    left = sorted(f.stem for f in (repo / "regions" / "alpha").glob("*.md"))
    refusals = {}
    for label, call in (("the area's face", lambda: w.update_node("beta-top", {"parent": "alpha-top"}, "c")),
                        ("a loop", lambda: w.update_node("mover", {"parent": "carried"}, "c")),
                        ("an area set by hand", lambda: w.update_node("carried", {"region": "alpha"}, "c"))):
        try: call(); refusals[label] = "accepted"
        except WriteError as e: refusals[label] = e.status
    return {"moved": after["mover"]["region"], "subtree": after["carried"]["region"],
            "parent": after["mover"]["parent"], "body": after["carried"]["body"].strip(),
            "left behind": left, "edges": len(edges),
            "edges resolve": all(e["from"] in after and e["to"] in after for e in edges),
            "valid": validate(w.store)["ok"], "refusals": refusals}


try:
    g = _move_across()
    eq("the entity lands in the new area", g["moved"], "beta")
    eq("what hung under it comes too", g["subtree"], "beta")
    eq("its parent is what it was dropped on", g["parent"], "beta-top")
    eq("the body travels intact", g["body"], "the body of carried")
    eq("nothing is left behind in the old area", g["left behind"], ["alpha-top"])
    eq("every edge still resolves", g["edges resolve"], True)
    eq("the edge count is unchanged", g["edges"], 2)
    eq("and the tree validates", g["valid"], True)
    eq("moving an area's face is refused", g["refusals"]["the area's face"], 409)
    eq("moving an entity under itself is refused", g["refusals"]["a loop"], 409)
    eq("setting an area by hand is refused", g["refusals"]["an area set by hand"], 400)
except Exception as e:
    fails.append("move"); print(f"FAIL {'the move check could not run':<52} {e!r}")

# ── does deleting refuse to take a branch with it ────────────────────────────
# A document under an entity is part of it and goes with it. A branch someone built is not, and
# losing it to one click is the harm the operator asked to prevent (2026-09-11).
def _delete_refuses_branches():
    import shutil, subprocess, tempfile
    from service.write import Writer, WriteError
    here = pathlib.Path(__file__).resolve().parent.parent
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-del-"))
    repo, pub = t / "repo", t / "pub"
    shutil.copytree(here / "seed", repo); pub.mkdir()
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q); subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    w = Writer(repo, pub, None)
    w.create_region({"source": "a", "core_description": "A",
                     "representative": {"id": "top", "name": "T", "kind": "tool",
                                        "one_liner": "the area", "use_when": "when"}}, "c")
    # `hollow` is what "+ New node" leaves behind: made, not written. On the map it is an area you
    # open, not a document you read, so it blocks its parent's delete exactly as `mid` does.
    for eid, par, body in (("branch", "top", "body of branch"), ("mid", "branch", "body of mid"),
                           ("leaf", "mid", "body of leaf"), ("plain", "top", "body of plain"),
                           ("doc", "plain", "body of doc"), ("keeper", "top", "body of keeper"),
                           ("hollow", "keeper", "")):
        w.create_node({"id": eid, "name": eid, "kind": "tool", "region": "a", "parent": par,
                       "one_liner": f"what {eid} is", "content": body,
                       "edges": [{"from": par, "rel": "CONSISTS_OF", "to": eid}]}, "c")
    out = {}
    for label, target in (("a branch", "branch"), ("an empty child", "keeper")):
        try: w.delete_node(target, "c"); out[label] = "deleted"
        except WriteError as e: out[label] = e.status
    # `plain` holds one document and nothing that holds anything — it goes, and takes the document.
    w.delete_node("plain", "c")
    ids = {n["id"] for n in w.store.nodes()}
    out["the entity went"] = "plain" not in ids
    out["its document went too"] = "doc" not in ids
    out["the branch is still there"] = {"branch", "mid", "leaf", "keeper", "hollow"} <= ids
    out["edges resolve"] = all(e["from"] in ids and e["to"] in ids for e in w.store.edges())
    return out


try:
    g = _delete_refuses_branches()
    eq("deleting something that holds a branch is refused", g["a branch"], 409)
    eq("an unwritten child blocks it too — made, not absent", g["an empty child"], 409)
    eq("an entity holding only documents is deleted", g["the entity went"], True)
    eq("and its document goes with it", g["its document went too"], True)
    eq("the branch it refused is untouched", g["the branch is still there"], True)
    eq("no edge is left pointing at nothing", g["edges resolve"], True)
except Exception as e:
    fails.append("delete"); print(f"FAIL {'the delete check could not run':<52} {e!r}")

# ── an entity's own routing line goes through the queue ──────────────────────
# The line an entity shows in its parent's table is edited like an area's advertisement: drafted,
# settled by a person, queued, applied on accept. There is deliberately no immediate-apply path.
def _entity_line_through_queue():
    from service.curator import submit_route, ROUTE_SCOPES, SCOPE_ALIAS
    out = {"scope is known": "entity" in ROUTE_SCOPES,
           "and it edits one_liner": ROUTE_SCOPES.get("entity")}

    class Fake:                       # the queue, reduced to what submit_route touches
        def __init__(self): self.rows = []
        def append(self, row): self.rows.append(row)

    q = Fake()
    r = submit_route(q, {"scope": "entity", "entity": "mover", "after": "what a reader comes here for",
                         "before": "moves", "why": "it said nothing"}, "c")
    row = q.rows[-1]
    out["it is queued, not applied"] = r["status"]
    out["the row names the entity"] = row["entity"]
    out["its evidence points at the entity"] = row["evidence"]
    for label, body in (("no entity", {"scope": "entity", "after": "x"}),
                        ("a field that is not the line", {"scope": "entity", "entity": "m", "after": "x", "field": "use_when"}),
                        ("a field nobody knows", {"scope": "entity", "entity": "m", "after": "x", "nonsense": 1})):
        try: submit_route(Fake(), body, "c"); out[label] = "accepted"
        except ValueError as e: out[label] = "refused"
    # an area proposal still needs its region — the entity scope did not loosen the others
    try: submit_route(Fake(), {"scope": "as", "after": "x"}, "c"); out["an area with no region"] = "accepted"
    except ValueError: out["an area with no region"] = "refused"
    return out


try:
    g = _entity_line_through_queue()
    eq("`entity` is a scope the queue knows", g["scope is known"], True)
    eq("and what it edits is the routing line", g["and it edits one_liner"], "one_liner")
    eq("a submitted line is queued, not applied", g["it is queued, not applied"], "pending")
    eq("the queued row names the entity", g["the row names the entity"], "mover")
    eq("its evidence points at the entity", g["its evidence points at the entity"], ["node:mover"])
    eq("scope entity with no entity is refused", g["no entity"], "refused")
    eq("editing any other field at this scope is refused", g["a field that is not the line"], "refused")
    eq("an unknown field is refused", g["a field nobody knows"], "refused")
    eq("an area proposal still needs its region", g["an area with no region"], "refused")
except Exception as e:
    fails.append("entity-line"); print(f"FAIL {'the entity-line check could not run':<52} {e!r}")

# ── a name is not asked about, and not summarised ────────────────────────────
# Two things the live run turned up, both about a value a person has to live with. An id cannot be
# renamed and a name is what the map tile shows.
from service.write import slug_id, name_from_file

# `Parcels` came back from the model as `tracking-system`: apt, and matching nothing anyone typed.
# The model is there for names a regex cannot reduce — and only those.
for nm, want in (("Parcels", "parcels"), ("Courier SLA", "courier-sla"), ("US4 Maker", "us4-maker"),
                 ("CDN — Edge", "cdn-edge"), ("3rd party", "3rd-party")):
    eq(f"{nm!r} names its own id", slug_id(nm), want)
# The trap the translator exists for: a name that is *partly* ASCII reduces to a fragment that looks
# deliberate, and there is no rename path. What counts as "a regex cannot take it" narrowed on
# 2026-09-12, when hangul, kana and Latin-with-marks became mechanical — see ontology/service/
# romanize.py. Han characters did not: there is no rule, only a dictionary of readings, and for
# Japanese the reading depends on the compound. Those still go to the model, and so does a name with
# one of them anywhere in it.
for nm, want in (("소포 추적", "sopo-chujeog"), ("Ürün", "urun"), ("한글 CDN", "hangeul-cdn"),
                 ("けいひ", "keihi")):
    eq(f"{nm!r} names its own id now, with no model", slug_id(nm), want)
for nm in ("小包", "小包 tracking", "束", "   "):
    eq(f"{nm!r} is sent to the translator, not guessed at", slug_id(nm), None)

# A description cut at 60 characters was becoming the name: "Courier SLA: delivery times for
# standard/express parcels and". The summary is already carried whole, right under it.
eq("a file names itself, and is not title-cased", name_from_file("courier-sla"), "courier-sla")


# And the point of all that: with an ASCII name the model is **not consulted at all**. A `Writer`
# with no LLM refused every id before; now it only refuses the names a regex genuinely cannot take.
def _id_without_an_llm():
    import shutil, subprocess, tempfile
    from service.write import Writer, WriteError
    here = pathlib.Path(__file__).resolve().parent.parent
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-id-"))
    repo, pub = t / "repo", t / "pub"
    shutil.copytree(here / "seed", repo); pub.mkdir()
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q); subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    w = Writer(repo, pub, None)                     # no LLM of any kind is wired to this
    r = w.create_region({"source": "p", "core_description": "P",
                         "representative": {"name": "Parcels", "kind": "tool",
                                            "one_liner": "Where a parcel is and who carries it",
                                            "use_when": "tracking a parcel"}}, "c")
    out = {"id": r["representative"], "said it generated one": r["id_generated"]}
    try:
        w.create_node({"name": "小包", "kind": "tool", "region": "p", "parent": r["representative"],
                       "one_liner": "a parcel"}, "c")
        out["a name a regex cannot take"] = "accepted"
    except WriteError as e:
        out["a name a regex cannot take"] = e.status
    return out


try:
    g = _id_without_an_llm()
    eq("an ASCII name gets its id with no LLM at all", g["id"], "parcels")
    eq("and it is not reported as generated", g["said it generated one"], False)
    eq("a name needing translation still asks for one", g["a name a regex cannot take"], 503)
except Exception as e:
    fails.append("id-no-llm"); print(f"FAIL {'the id check could not run':<52} {e!r}")

# ── a suggestion must be what the write would do ─────────────────────────────
# The screen shows a drafted id and the person agrees to it. If the save then resolves a different
# one, the button was worse than no button — an id is permanent and cannot be taken back. So the
# draft endpoint calls the same resolution the write calls, and this holds the two together.
def _suggestion_matches_the_write():
    import shutil, subprocess, tempfile
    from service.write import Writer, WriteError
    here = pathlib.Path(__file__).resolve().parent.parent
    t = pathlib.Path(tempfile.mkdtemp(prefix="check-sugg-"))
    repo, pub = t / "repo", t / "pub"
    shutil.copytree(here / "seed", repo); pub.mkdir()
    q = dict(capture_output=True, cwd=repo)
    subprocess.run(["git", "init", "-q"], **q); subprocess.run(["git", "add", "-A"], **q)
    subprocess.run(["git", "-c", "user.name=c", "-c", "user.email=c@l", "commit", "-qm", "t"], **q)
    w = Writer(repo, pub, None)                       # no LLM anywhere
    w.create_region({"source": "a", "core_description": "A",
                     "representative": {"id": "top", "name": "T", "kind": "tool",
                                        "one_liner": "the area", "use_when": "when"}}, "c")
    out = {}
    drafted, generated = w._resolve_id(None, name="Parcel Tracking", kind="", one_liner="", region="a")
    out["the draft"] = drafted
    out["it did not need a model"] = generated
    r = w.create_node({"name": "Parcel Tracking", "region": "a", "parent": "top",
                       "one_liner": "where a parcel is"}, "c")
    out["what the write used"] = r["id"]
    # No kind sent and no LLM: `default_kind` from the vocabulary decides, and the answer says so.
    out["kind came from the vocabulary"] = (r["kind"], r["kind_generated"])

    def refuse(label, fn):
        try: fn(); out[label] = "accepted"
        except WriteError as e: out[label] = (e.status, str(e))
    # Two reasons reach the same place and they have different fixes. Calling a name collision
    # "no LLM is configured" sends the reader somewhere a model would not have helped.
    refuse("a name whose id is taken", lambda: w._resolve_id(None, name="Parcel Tracking", kind="", one_liner="", region="a"))
    refuse("a name a regex cannot take", lambda: w._resolve_id(None, name="小包", kind="", one_liner="", region="a"))

    # Now with a model wired. A collision must be refused **before it is asked** — told "must not
    # collide", a model answers `books-2`, which is the one thing this method's own rule forbids.
    asked = []
    w.suggest_id_configured = lambda: True
    w.suggest_id = lambda **kw: (asked.append(kw.get("name")), "parcel-tracking-2")[1]
    refuse("a taken name while a model is available", lambda: w._resolve_id(None, name="Parcel Tracking", kind="", one_liner="", region="a"))
    out["was the model asked"] = list(asked)
    # It is still asked for the case it exists for.
    w.suggest_id = lambda **kw: (asked.append(kw.get("name")), "parcel")[1]
    out["a translated name"] = w._resolve_id(None, name="小包", kind="", one_liner="", region="a")
    return out


try:
    g = _suggestion_matches_the_write()
    eq("the suggested id is the one the write uses", g["the draft"], g["what the write used"])
    eq("and an ASCII name needed no model", g["it did not need a model"], False)
    eq("no kind and no LLM takes the vocabulary's default", g["kind came from the vocabulary"], ("system", True))
    eq("a taken name is refused as a collision", g["a name whose id is taken"][0], 409)
    eq("and it says so, not 'no LLM'", "taken" in g["a name whose id is taken"][1], True)
    eq("a name needing translation still asks for an LLM", g["a name a regex cannot take"][0], 503)
    eq("a taken name is refused even with a model", g["a taken name while a model is available"][0], 409)
    eq("and the model is never asked — it would answer `x-2`", g["was the model asked"], [])
    eq("a name needing translation does reach the model", g["a translated name"], ("parcel", True))
except Exception as e:
    fails.append("suggest"); print(f"FAIL {'the suggestion check could not run':<52} {e!r}")

# ── an overlay is one question's working set, and never an inventory ─────────
# The rule everything else rests on: an overlay narrows **where to look**, never what exists. So the
# refusals matter more than the happy path — a table that silently stops early would make "not here"
# read as "not anywhere", which is the one failure this feature must not have.
def _overlay_life():
    import tempfile
    from service.overlays import OverlayStore, OverlayError
    served = {"/v1/regions/a": 30, "/v1/nodes/big": 100, "/v1/nodes/small": 2, "/v1/nodes/doc/body": 1}
    resolve = lambda a: a in served
    rows_of = lambda a: served.get(a, 0)
    st = OverlayStore(pathlib.Path(tempfile.mkdtemp(prefix="check-ov-")),
                      members_max=3, rows_max=40, open_hours=24, keep_days=30)
    who = {"kind": "agent", "name": "c"}
    out = {}

    def refuse(label, fn):
        try: fn(); out[label] = "accepted"
        except OverlayError as e: out[label] = e.status

    ov = st.create("why is it late", [{"address": "/v1/regions/a", "why": "the area"}], who, resolve, rows_of)
    out["it opens"] = ov["state"]
    out["the trail starts with the reason"] = ov["trail"][0]["why"]
    refuse("an address that resolves to nothing", lambda: st.amend(ov["id"], "/v1/nodes/invented", None, "assembled", resolve, rows_of))
    refuse("an add with no why", lambda: st.amend(ov["id"], "/v1/nodes/small", None, "  ", resolve, rows_of))
    refuse("the same member twice", lambda: st.amend(ov["id"], "/v1/regions/a", None, "again", resolve, rows_of))
    refuse("both add and remove at once", lambda: st.amend(ov["id"], "/v1/nodes/small", "/v1/regions/a", "?", resolve, rows_of))
    refuse("over the row limit", lambda: st.amend(ov["id"], "/v1/nodes/big", None, "everything", resolve, rows_of))
    # The refusal must not have written anything: a create-then-delete or an add-then-roll-back is a
    # half-succeeded state, and the record is the thing being protected here.
    out["a refused add left no trace"] = [t["op"] for t in st.get(ov["id"])["trail"]]
    st.amend(ov["id"], "/v1/nodes/small", None, "narrower", resolve, rows_of)
    st.amend(ov["id"], "/v1/nodes/doc/body", None, "the document", resolve, rows_of)
    refuse("over the member limit", lambda: st.amend(ov["id"], "/v1/nodes/big", None, "one more", resolve, rows_of))
    st.amend(ov["id"], None, "/v1/nodes/small", "too coarse after all", resolve, rows_of)
    closed = st.close(ov["id"], "answered",
                      ["/v1/nodes/doc/body", "/v1/nodes/small", "/v1/regions/a", "/v1/nodes/big"], resolve)
    out["how each used address is labelled"] = [u["how"] for u in closed["used"]]
    refuse("a change after close", lambda: st.amend(ov["id"], "/v1/nodes/big", None, "late", resolve, rows_of))
    refuse("closing twice", lambda: st.close(ov["id"], "answered", [], resolve))
    refuse("an outcome nobody defined", lambda: st.close(st.create("q", [{"address": "/v1/nodes/small", "why": "w"}], who, resolve, rows_of)["id"], "maybe", [], resolve))
    refuse("a question nobody asked", lambda: st.create("   ", [{"address": "/v1/nodes/small", "why": "w"}], who, resolve, rows_of))
    refuse("an overlay with nothing in it", lambda: st.create("q", [], who, resolve, rows_of))

    # Expiry is decided when someone looks — no thread, no scheduler.
    stale = st.create("left behind", [{"address": "/v1/nodes/small", "why": "w"}], who, resolve, rows_of)
    st._write({**stale, "touched_at": "2020-01-01T00:00:00Z"})
    out["an untouched overlay is settled on the next read"] = st.get(stale["id"])["state"]
    gone = st.create("long over", [{"address": "/v1/nodes/small", "why": "w"}], who, resolve, rows_of)
    st._write({**gone, "state": "answered", "closed_at": "2020-01-01T00:00:00Z"})
    refuse("a record past its keeping is forgotten", lambda: st.get(gone["id"]))
    return out


try:
    g = _overlay_life()
    eq("an overlay opens", g["it opens"], "open")
    eq("the trail starts with the reason", g["the trail starts with the reason"], "the area")
    eq("an address that resolves to nothing is refused", g["an address that resolves to nothing"], 422)
    eq("an add with no why is refused", g["an add with no why"], 400)
    eq("the same member twice is refused", g["the same member twice"], 409)
    eq("add and remove at once is refused", g["both add and remove at once"], 400)
    eq("over the row limit is refused", g["over the row limit"], 409)
    eq("over the member limit is refused", g["over the member limit"], 409)
    eq("a refused add wrote nothing", g["a refused add left no trace"], ["create"])
    # `reached` is the one that matters: answering from something never added is the normal case, and
    # the spec's first draft refused it. It says the overlay was drawn a level too coarse.
    eq("used says how each address was reached", g["how each used address is labelled"], ["member", "removed", "member", "reached"])
    eq("a change after close is refused", g["a change after close"], 409)
    eq("closing twice is refused", g["closing twice"], 409)
    eq("an outcome nobody defined is refused", g["an outcome nobody defined"], 400)
    eq("a question nobody asked is refused", g["a question nobody asked"], 400)
    eq("an overlay with nothing in it is refused", g["an overlay with nothing in it"], 400)
    eq("an untouched overlay settles when read", g["an untouched overlay is settled on the next read"], "abandoned")
    eq("a record past its keeping is forgotten", g["a record past its keeping is forgotten"], 404)
except Exception as e:
    fails.append("overlay"); print(f"FAIL {'the overlay check could not run':<52} {e!r}")

# ── what actually goes out to each of the three providers ────────────────────
# A fake server, so the wire itself is what is read. The three differ in four places at once —
# path, auth header, where `system` goes, and the shape of the answer. Get any one wrong and
# "OpenAI-compatible" is true of the name and of nothing else. No real provider is called.
def _wire(provider, *, json_object=False, status=200, body=None, fail_first=None):
    import http.server, json as _j, threading
    from service.curator import chat_client
    seen = []

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            got = _j.loads(self.rfile.read(n) or b"{}")
            seen.append({"path": self.path, "body": got,
                         "headers": {k.lower(): v for k, v in self.headers.items()}})
            if fail_first and len(seen) == 1:
                out = _j.dumps({"error": {"message": fail_first}}).encode()
                self.send_response(400)
            else:
                self.send_response(status)
                out = _j.dumps(body if body is not None else (
                    {"content": [{"type": "text", "text": "ANSWER"}]} if provider == "anthropic"
                    else {"choices": [{"message": {"content": "ANSWER"}}]})).encode()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out))); self.end_headers(); self.wfile.write(out)

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        c = chat_client(provider, f"http://127.0.0.1:{srv.server_address[1]}", "KEY", "M",
                        max_tokens=77, temperature=0.25)
        try: out = c("sys prompt", "user prompt", json_object=json_object)
        except Exception as e: out = e
    finally:
        srv.shutdown()
    return out, seen


for prov, path, auth in (("litellm", "/v1/chat/completions", "authorization"),
                         ("openai", "/v1/chat/completions", "authorization"),
                         ("anthropic", "/v1/messages", "x-api-key")):
    out, seen = _wire(prov)
    r = seen[0]
    eq(f"{prov}: path", r["path"], path)
    eq(f"{prov}: the key goes out on the auth header", r["headers"].get(auth, "").endswith("KEY"), True)
    eq(f"{prov}: the answer is read out", out, "ANSWER")
    eq(f"{prov}: max_tokens is sent", r["body"].get("max_tokens"), 77)
    eq(f"{prov}: temperature is sent", r["body"].get("temperature"), 0.25)

# `system` sits somewhere else on Anthropic: a top-level field, not the first message
_, seen = _wire("openai")
eq("openai: system is the first message", seen[0]["body"]["messages"][0]["role"], "system")
_, seen = _wire("anthropic")
eq("anthropic: system is top-level", seen[0]["body"].get("system"), "sys prompt")
eq("anthropic: the version header rides along", seen[0]["headers"].get("anthropic-version"), "2023-06-01")
eq("anthropic: the only message is the user one", [m["role"] for m in seen[0]["body"]["messages"]], ["user"])

# `response_format` is the call site's decision, and Anthropic has no such field at all
_, seen = _wire("openai", json_object=True)
eq("openai: asking for JSON sends response_format", seen[0]["body"].get("response_format"), {"type": "json_object"})
_, seen = _wire("openai", json_object=False)
eq("openai: not asking sends nothing", "response_format" in seen[0]["body"], False)
_, seen = _wire("anthropic", json_object=True)
eq("anthropic: response_format is never sent", "response_format" in seen[0]["body"], False)

# The argument over the parameter name is settled by asking, not by guessing from a model name
out, seen = _wire("openai", fail_first="Unsupported parameter: 'max_tokens'. Use 'max_completion_tokens'.")
eq("a refusal that names the parameter is retried under that name", seen[-1]["body"].get("max_completion_tokens"), 77)
eq("and the answer arrives", out, "ANSWER")

# A refusal arrives carrying the provider's own words
out, _ = _wire("openai", status=401, body={"error": {"message": "invalid api key"}}, fail_first=None)
eq("a refusal carries what the provider said", "invalid api key" in str(out), True)
eq("and it is an LLMError", type(out).__name__, "LLMError")

try:
    from service.curator import chat_client as _cc
    _cc("gemini", "http://x", "k", "m", max_tokens=1, temperature=0)
    eq("an unknown provider is refused", "it was accepted", "ValueError")
except ValueError as e:
    eq("an unknown provider is refused", "gemini" in str(e), True)

# ── a reader must never see a file half-written ──────────────────────────────
# The end-to-end version of this is check/concurrency-check.py, driving a real server; it reproduces
# the failure but only usually, because the window is one file being truncated and refilled and
# hitting it is luck. This one is the mechanism on its own, where the window can be made as wide as
# it needs to be — a big file, rewritten in a loop, read in a loop — so it answers the same question
# every time.
#
# Both directions are measured. `Path.write_text`, which is what every writer here used until
# 2026-09-13, is shown failing: that is the evidence the fix is for something. `store.write` is shown
# not failing under the same pressure.
import threading as _th, tempfile as _tf, shutil as _sh
from service.store import write as _atomic

def _torn_reads(writer, seconds=1.5):
    """Rewrite one file over and over with `writer`, read it over and over, count the bad reads."""
    d = _tf.mkdtemp(prefix="torn-"); f = pathlib.Path(d) / "x.json"
    a = json.dumps({"v": "a" * 60000}); b = json.dumps({"v": "b" * 60000})
    f.write_text(a, encoding="utf-8")
    stop, bad, reads = [], [], [0]
    def write_loop():
        i = 0
        while not stop:
            writer(f, a if i % 2 else b); i += 1
    def read_loop():
        while not stop:
            try:
                json.loads(f.read_text(encoding="utf-8")); reads[0] += 1
            except FileNotFoundError: bad.append("vanished")
            except Exception as e: bad.append(type(e).__name__)
    ts = [_th.Thread(target=write_loop), _th.Thread(target=read_loop), _th.Thread(target=read_loop)]
    for t in ts: t.start()
    time.sleep(seconds); stop.append(True)
    for t in ts: t.join()
    _sh.rmtree(d, ignore_errors=True)
    return bad, reads[0]

import json, time                                                          # noqa: E402
_bad, _n = _torn_reads(lambda p, t: p.write_text(t, encoding="utf-8"))
eq("write_text: a reader does catch it half-written", len(_bad) > 0, True)
print(f"     ({len(_bad)} torn reads of {_n + len(_bad)} — this is the failure, reproduced)")
_bad, _n = _torn_reads(_atomic)
eq("store.write: a reader never does", _bad[:3], [])
eq(f"  and it really was reading ({_n} clean reads)", _n > 100, True)


# ── what ships has to validate as shipped ────────────────────────────────────
# `examples/back-office` is what the README tells a new person to copy over `data/repo` before the
# first boot, and `seed/` is what the entrypoint lays down when they do not. Both are committed
# ontologies with a committed `regions.json`, and neither was ever validated *as committed* — every
# check that used them called `regenerate` first, so a stale file in the repository was invisible to
# all of them.
#
# It went stale the moment the export fields were added: `use_when_export`, `export_to` and
# `use_when_export_for` were simply absent from the shipped table. Nothing noticed until the drift
# rule started comparing the text — and then the very first thing a new install did was report five
# validation errors about a file nobody had touched. A worked example that does not validate teaches
# the wrong lesson on page one.
for _ship in ("examples/back-office", "seed"):
    _src = pathlib.Path(_ship)
    if not (_src / "regions.json").exists(): continue
    import shutil as _sh, tempfile as _tf, subprocess as _sp
    from service.validate import validate as _v
    from service.derive import regenerate as _rg
    _T = _tf.mkdtemp(prefix="shipped-"); _r = pathlib.Path(_T) / "r"
    _sh.copytree(_src, _r); _sp.run(["git", "-C", str(_r), "init", "-q"], check=True)
    _st = Store(_r)
    _res = _v(_st)
    eq(f"{_ship} validates as shipped", _res["ok"], True)
    if not _res["ok"]: print("     " + "\n     ".join(e[:120] for e in _res["errors"][:5]))
    eq(f"  and its derived table needs no regenerating", _rg(_st), [])
    _sh.rmtree(_T, ignore_errors=True)


# ── a derived file that is also committed can be committed stale ─────────────
# `regions.json` is generated from the areas' `.md` files and the CORE.md table, and it is versioned
# alongside them, which is the combination that lets the two drift: edit an area's file in an editor,
# commit, restart, and nothing regenerates. Measured 2026-09-13 on a copy of the live repository —
# `title` and `use_when` changed by hand, `validate` returned ok with no errors and no warnings, and
# hop 0 went on advertising the old wording. `use_when` is the sentence an agent routes on, so what
# was quietly wrong was the routing table itself.
#
# Stated as an absence, like everything else here: the loss is that nobody is told.
if (pathlib.Path("data/repo") / "regions").is_dir():
    import shutil, tempfile, subprocess, json as _json
    from service.validate import validate as _validate
    from service.derive import regenerate as _regen
    _T = tempfile.mkdtemp(prefix="derived-drift-")
    _repo = pathlib.Path(_T) / "repo"
    shutil.copytree("data/repo", _repo, ignore=shutil.ignore_patterns(".git"))
    subprocess.run(["git", "-C", str(_repo), "init", "-q"], check=True)
    _st = Store(_repo)
    eq("the copy starts in sync", _regen(_st), [])
    eq("  and validates", _validate(_st)["ok"], True)

    _area = sorted(d.name for d in (_repo / "regions").iterdir() if d.is_dir())[0]
    _md = _repo / "regions" / _area / f"{_area}.md"
    _before = _md.read_text(encoding="utf-8")
    _md.write_text(_before.replace("use_when:", "use_when: EDITED BY HAND ·", 1), encoding="utf-8")
    _v = _validate(_st)
    eq("a hand-edited area file is caught", _v["ok"], False)
    eq("  and the error names the file, the area and the field",
       any(f"regions.json {_area}" in e and "use_when" in e for e in _v["errors"]), True)
    eq("  and does not blame a field that did not move",
       any("export_to" in e for e in _v["errors"]), False)
    eq("  regenerating is what fixes it", _regen(_st), ["regions.json"])
    eq("  and then it validates again", _validate(_st)["ok"], True)

    # The other direction, which is the one that would make this check worthless: an untouched tree
    # must not fail. A drift check that fires on a clean repository would be turned off within a day.
    _md.write_text(_before, encoding="utf-8"); _regen(_st)
    eq("an untouched tree still passes", _validate(_st)["ok"], True)
    shutil.rmtree(_T, ignore_errors=True)

# ── if a tree is there, does every entity read ───────────────────────────────
root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("data/repo")
if (root / "regions").is_dir():
    ns = Store(root).nodes()
    empty = [n["id"] for n in ns if not n.get("files") and not (n.get("body") or "").strip()]
    print(f"\n{root}: {len(ns)} entities, {len(empty)} with nothing in them" + (f" {empty[:6]}" if empty else ""))

print()
print("all pass" if not fails else f"FAIL {len(fails)}: {fails}")
sys.exit(1 if fails else 0)
