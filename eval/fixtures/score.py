#!/usr/bin/env python3
"""Q5a — score a continuity fixture. Stage 1: retrieval only, no generation.

`eval/fixtures/README.md` is the contract this implements, and it promises contributors two numbers
kept apart, because conflating them is the whole reason fixtures exist:

    found       is the operative document in the top-k at all
    operative   is it ranked **above its own distractors**

A system can score 1.00 on the first and 0.00 on the second. That is not a retrieval failure — every
document was found, all of them are true and relevant — it is a failure to distinguish *found the
material* from *established which material is operative*. Raised by GovKM on 2026-09-18 as F5, and
written into `eval/PREREGISTRATION.md` §Q5a as: "a reranker blind to dates has no reason to put July
above March."

    ./eval/fixtures/score.py eval/fixtures/supplier-selection.yaml
    ./eval/fixtures/score.py eval/fixtures/*.yaml --out eval/runs/2026-09-21-q5a.json

**The fixture's documents go into the retrieval pool; its `truth` and `questions` never do.** That is
rule 2 of the contract, and here it is mechanical rather than a promise: `pool()` reads `documents`
only, and the scorer reads `truth` only after the search has returned.

**The corpus is not modified.** The fixture is merged into the pool in memory. Writing four documents
into `bench/corpus/` would change the fingerprint every run record is stamped with, which is a high
price for a test that does not need it.

Q5 is specified to run first against `git tag baseline-pre-continuity` — the implementation before
any state, age or supersession field exists — so that a later continuity-aware change is a delta from
a preserved result rather than a test designed around the fix. The contributor asked for exactly that.

**That instruction cannot be followed literally, and saying so is part of honouring it.** The tag is
from 2026-09-18 19:07 and has no `bench/` directory at all: the retrieval harness was built after it,
so there is nothing at that commit to run a fixture through. What the tag actually marks is the
*service* before any continuity field. The intent is therefore checked mechanically at every run —
`baseline()` below diffs `ontology/service/` between the tag and HEAD and refuses to record a result
as baseline if anything there has changed. Today that diff is empty, so a run at HEAD *is* a baseline
run; the day it stops being empty, this stops claiming otherwise on its own.
"""
import argparse, json, os, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bench"))
if os.environ.get("BENCH_PYLIB"):
    sys.path.insert(0, os.environ["BENCH_PYLIB"])
import yaml
import run as runner
from retrieve import Hybrid
from rerank import LLMReranker
from agent import Agent


def pool(fixtures):
    """The corpus plus every fixture's documents. `truth` and `questions` are not read here."""
    texts, area, one_liner, children, has_body = runner.corpus()
    added = {}
    for fx in fixtures:
        for d in fx["documents"]:
            if d["id"] in texts:
                sys.exit(f"  {fx['id']}: document id {d['id']} already exists in the corpus")
            # Indexed exactly the way run.py indexes a corpus document, or the fixture would be
            # competing on a different footing from everything it is ranked against.
            texts[d["id"]] = f"{d.get('name','')}. {d.get('one_liner','')}\n\n{d['body'].strip()}"
            added[d["id"]] = fx["id"]
    return texts, added


def load_map(fx, path):
    """The frozen routing text beside a fixture — `<name>.map.yaml` — or the one named with --map.

    The map is the system under test (GovKM, PR #1, 2026-09-29): its current/replaced/history
    declarations are what the routing arm walks on, and they are read here exactly as frozen. The
    same agreement `check.py` enforces is re-checked, because a map that drifted from its fixture
    would have the walk reach documents the contributor did not mean.
    """
    mp = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
    if mp.get("fixture") != fx["id"]:
        sys.exit(f"  {path}: `fixture: {mp.get('fixture')!r}` does not name {fx['id']}")
    ids = {d["id"] for d in fx["documents"]}
    kids = (mp.get("node") or {}).get("children") or []
    named = [c["id"] for c in kids]
    if set(named) != ids or len(named) != len(ids):
        sys.exit(f"  {path}: map advertises {sorted(named)}, fixture holds {sorted(ids)}")
    return mp


def tree(fixtures, maps):
    """The tree the walk reads, with each fixture grafted in **by its map**, not by its documents.

    Two views, and they are kept apart on purpose. The retrieval arms index each document's own
    name, one_liner and body (`pool()`), and nothing here touches that. The walk reads *lines*: the
    map's node under the parent the map names, and under it one row per document carrying the
    map's line for it — the current/replaced/history sentence — not the document's own one_liner.
    That is the whole arrangement being tested: the continuity statement lives in the routing text
    and nowhere in the corpus, and the question is whether a walk that reads it beats retrieval
    that reads the documents.
    """
    _, _, one_liner, children, has_body = runner.corpus()
    one_liner, children, has_body = dict(one_liner), {k: list(v) for k, v in children.items()}, dict(has_body)
    for fx, mp in zip(fixtures, maps):
        node = mp["node"]
        if node["parent"] not in one_liner:
            sys.exit(f"  {fx['id']}: the map's parent {node['parent']!r} is not in the tree the walk reads")
        if node["id"] in one_liner:
            sys.exit(f"  {fx['id']}: the map's node {node['id']!r} already exists in the tree")
        one_liner[node["id"]] = " ".join(str(node.get("one_liner") or "").split())
        has_body[node["id"]] = False
        children.setdefault(node["parent"], []).append(node["id"])
        children[node["parent"]].sort()
        # Map order, not sorted: the map is a table somebody wrote, and the order its rows are in is
        # part of what was written.
        children[node["id"]] = [c["id"] for c in node["children"]]
        for c in node["children"]:
            one_liner[c["id"]] = " ".join(str(c.get("one_liner") or "").split())
            has_body[c["id"]] = True
    return one_liner, children, has_body


sys.path.insert(0, str(ROOT / "ontology"))
from service.resolve import resolve as resolve_names   # noqa: E402

# Strings the discovery block must never contain: the words the map uses to say which record
# governs, and the answers. Checked on every block, in --dry-run and before every walk.
FORBIDDEN = ("current", "replaced", "history", "in force", "supersed", "withdrawn", "operative")


def corpus_names():
    """id → name, from frontmatter, for every document in the tree the walk reads. `runner.corpus()`
    keeps one_liners and parents but not names, and names are what a person says."""
    import re as _re
    out = {}
    roots = [ROOT / "bench" / "corpus" / "regions"]
    extra = os.environ.get("BENCH_EXTRA_CORPUS")
    if extra:
        ex = pathlib.Path(extra)
        if not ex.is_absolute(): ex = ROOT / ex
        roots.append(ex / "regions")
    for r in roots:
        for p in r.rglob("*.md"):
            m = runner.FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
            out[fm.get("id") or p.stem] = fm.get("name") or p.stem
    return out


def load_names(fx, path):
    """`<fixture>.names.yaml` — the subject names the discovery mechanism may know. Optional; a
    fixture with none gets a mechanism that resolves nothing, which is itself a result."""
    p = pathlib.Path(path)
    if not p.exists(): return {}
    mp = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if mp.get("fixture") != fx["id"]: sys.exit(f"  {path}: `fixture:` does not name {fx['id']}")
    return {k: [str(a) for a in (v or [])] for k, v in (mp.get("names") or {}).items()}


def discovery_block(question, *, one_liner, children, areas, names, aliases, maps):
    """What the continuity-discovery arm shows the walker, and nothing else.

    The mechanism is `service.resolve` — the resolver in front of hop 0 in the product: names said
    in the question matched against the names the map knows, one hop along the map's own edges,
    and what kind of thing is being asked. From its answer this renders only **where** each named
    thing is recorded: the node, whether it is a table or a document, and the path down to it from
    its area. Not the node's line. Not a date. Not which of two records governs. The walker still
    has to open the table and read the lines, exactly as the control does; the block changes only
    whether it knows which table to open.
    """
    parent = {c: p for p, cs in children.items() for c in cs}
    region_of = dict(areas)
    for mp in maps:
        region_of[mp["node"]["id"]] = mp["area"]
        for c in mp["node"]["children"]: region_of[c["id"]] = mp["area"]
    nodes = [{"id": i, "name": names.get(i, i), "region": region_of.get(i), "aliases": aliases.get(i, []),
              "one_liner": ""} for i in one_liner]
    regions = [{"dir": a, "key": a.upper(), "representative": a, "use_when": ""} for a in sorted(set(region_of.values()) - {None})]
    edges = []
    try: edges = yaml.safe_load((ROOT / "bench" / "corpus" / "edges.yaml").read_text(encoding="utf-8")) or []
    except Exception: pass
    r = resolve_names(question, nodes=nodes, edges=edges if isinstance(edges, list) else [], regions=regions, ages={}, revision="")

    def path_to(i):
        chain, cur = [], parent.get(i)
        while cur and cur not in chain and cur != region_of.get(i):
            chain.append(cur); cur = parent.get(cur)
        return " › ".join(reversed(chain))

    if not r["names"]:
        lines = ["Names in this question that the map knows: none."]
    else:
        lines = ["Names in this question that the map knows, and where each is recorded:"]
        for n in r["names"]:
            kind = "table" if children.get(n["is"]) else "document"
            where = path_to(n["is"])
            lines.append(f"  \"{n['said']}\"  →  {n['is']} ({kind}) — in {n['area']}" + (f", under {where}" if where else "") + f"  [{n['via']}]")
    a = r["ask"]
    lines.append(f"Asking: {a['kind']}" + (f" (said \"{a['said']}\")" if a.get("said") else ""))
    block = "\n".join(lines)
    low = block.lower()
    bad = [w for w in FORBIDDEN if w in low]
    if bad: sys.exit(f"  discovery block for {question!r} contains forbidden words {bad}:\n{block}")
    for mp in maps:
        for c in mp["node"]["children"]:
            if " ".join(str(c.get("one_liner") or "").split())[:40].lower() in low:
                sys.exit(f"  discovery block for {question!r} contains a map line")
    return block


BASE_TAG = "baseline-pre-continuity"


def baseline():
    """Is this still the implementation the fixtures are supposed to measure first?

    Not a promise in prose — a diff. If `ontology/service/` has changed since the tag, something
    continuity-aware may have been added and a result recorded here is no longer a baseline result.
    """
    r = subprocess.run(["git", "diff", "--stat", BASE_TAG, "HEAD", "--", "ontology/service/"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"cannot compare against {BASE_TAG}: {r.stderr.strip()[:80]}"
    changed = r.stdout.strip()
    if changed:
        return False, f"ontology/service/ has changed since {BASE_TAG}:\n{changed}"
    return True, f"ontology/service/ is unchanged since {BASE_TAG}"


def rank_of(ids, doc):
    return ids.index(doc) + 1 if doc in ids else None


def score_question(q, ids, k):
    """Two numbers, kept apart. `found` is about the pool; `operative` is about the order."""
    op = q["operative"]
    r_op = rank_of(ids, op)
    found = r_op is not None and r_op <= k
    ranks = {d: rank_of(ids, d) for d in q.get("distractors") or []}
    # A distractor that was not retrieved cannot outrank anything, so it does not count against the
    # operative document. Treating "absent" as "beaten" is the reading that flatters the system; it
    # is also the correct one — the question is whether a wrong document was *preferred*.
    above = [d for d, r in ranks.items() if r is not None and r_op is not None and r < r_op]
    beats = found and not above
    return dict(q=q["q"], operative=op, rank=r_op, found=found,
                distractor_ranks=ranks, outranked_by=above, beats_distractors=beats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixtures", nargs="+")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--n", type=int, default=20, help="candidates fused before any reranking")
    ap.add_argument("--no-rerank", action="store_true")
    # Opt-in, so every invocation that existed before this flag still does exactly what it did.
    ap.add_argument("--routing", action="store_true",
                    help="also walk: the pilot's walker (bench/agent.py) over the tree with each fixture's map grafted in")
    ap.add_argument("--map", action="append", default=[],
                    help="routing: the map for the fixture in the same position; default <fixture>.map.yaml beside it")
    ap.add_argument("--steps", type=int, default=30, help="routing: the walk's turn ceiling, as in the pilot")
    # The continuity-discovery arm (PR #1, proposed by GovKM 2026-10-02): the control's walker, the
    # control's map, the control's ceiling, plus one block before hop 0 saying where the names in the
    # question are recorded. --dry-run prints that block for every question and exits before any
    # model is called — the block is what GovKM reviews, so it has to be seen before it is used.
    ap.add_argument("--discovery", action="store_true", help="also walk with the discovery block (implies --routing)")
    ap.add_argument("--names", action="append", default=[],
                    help="discovery: the names file for the fixture in the same position; default <fixture>.names.yaml")
    ap.add_argument("--dry-run", action="store_true", help="discovery: print each question's block verbatim and stop; no model call")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.discovery: a.routing = True

    fixtures = [yaml.safe_load(pathlib.Path(f).read_text(encoding="utf-8")) for f in a.fixtures]
    maps = None
    if a.routing:
        paths = [a.map[i] if i < len(a.map) else str(pathlib.Path(f).with_suffix("")) + ".map.yaml"
                 for i, f in enumerate(a.fixtures)]
        maps = [load_map(fx, p) for fx, p in zip(fixtures, paths)]
    texts, added = pool(fixtures)
    print(f"  {len(texts)} documents ({len(added)} from {len(fixtures)} fixture(s)) · k={a.k}",
          file=sys.stderr)

    blocks = {}
    if a.discovery:
        one_liner, children, has_body = tree(fixtures, maps)
        _, areas, _, _, _ = runner.corpus()
        cnames = corpus_names()
        for fx, mp in zip(fixtures, maps):
            cnames[mp["node"]["id"]] = mp["node"].get("name") or mp["node"]["id"]
            for d in fx["documents"]: cnames[d["id"]] = d.get("name") or d["id"]
        aliases = {}
        for i, f in enumerate(a.fixtures):
            npath = a.names[i] if i < len(a.names) else str(pathlib.Path(f).with_suffix("")) + ".names.yaml"
            aliases.update(load_names(fixtures[i], npath))
        for fx in fixtures:
            for q in fx["questions"]:
                blocks[q["q"]] = discovery_block(q["q"], one_liner=one_liner, children=children, areas=areas,
                                                 names=cnames, aliases=aliases, maps=maps)
        if a.dry_run:
            # Before any model exists in this process. The control's first turn is asserted to be
            # byte-identical to the pre-discovery format, so the control is the control.
            probe = Agent.__new__(Agent); probe.rows = runner.rows()
            for fx in fixtures:
                for q in fx["questions"]:
                    assert probe.first_turn(q["q"], "") == f"Question: {q['q']}\n\n{probe._hop0()}", "control first turn changed"
            print("  control first turn: unchanged (asserted)\n")
            for fx in fixtures:
                for n, q in enumerate(fx["questions"], 1):
                    print(f"=== Q{n}: {q['q']}\n{blocks[q['q']]}\n")
            print("  (dry run — no model was called, nothing was scored)")
            return

    tag = subprocess.run(["git", "describe", "--tags", "--always"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    is_base, why = baseline()
    print(f"  baseline: {'yes' if is_base else 'NO'} — {why}", file=sys.stderr)
    h = Hybrid(texts).warm()
    rr = None if a.no_rerank else LLMReranker()

    out, rows = [], []
    for fx in fixtures:
        for q in fx["questions"]:
            ids = h.search(q["q"], n=a.n)          # fused candidates, best-first
            rows.append(("rag", fx["id"], score_question(q, ids, a.k)))
            if rr:
                rows.append(("rag+rerank", fx["id"],
                             score_question(q, rr.rank(q["q"], ids, texts), a.k)))

    # The routing arm. The pilot's walker — bench/agent.py, OPEN/READ/BACK/DONE over tables — on the
    # tree with each fixture grafted in by its map. Not the `claude -p` census walker: this one runs
    # in-process and writes down every turn, which is what a run that may happen once has to do.
    #
    # What is ranked is what the walk READ, in the order it read it. `found` is whether the
    # operative document was read at all; `operative` is whether it was read before any distractor
    # — the same two numbers, through the same `score_question`, so the three arms are compared on
    # one definition. A walk that reads the review first and the September decision second has found
    # the answer and preferred the wrong document, exactly as a retrieval list would have.
    walker = None
    if a.routing:
        one_liner, children, has_body = tree(fixtures, maps)
        walker = Agent(runner.rows(), children, one_liner, has_body, steps=a.steps, body=texts)
        print(f"  routing: {walker.provider} {walker.model} · steps={a.steps} · use_when="
              f"{os.environ.get('BENCH_USE_WHEN', 'frozen')}", file=sys.stderr)
        for fx, mp in zip(fixtures, maps):
            for q in fx["questions"]:
                before = dict(walker.usage)
                w = walker.walk(q["q"])
                got = [i for i in w["collected"] if i in texts]
                r = score_question(q, got, a.k)
                r.update(read=got, visited=w["visited"], hops=w["hops"], opens=w["opens"],
                         returns=w["returns"], turns=w["turns"], exhausted=w["exhausted"],
                         read_chars=w["read_chars"], log=w["log"],
                         usage={k: walker.usage[k] - before[k] for k in walker.usage})
                rows.append(("routing", fx["id"], r))
                print(f"    routing  {q['q'][:50]:<50} read {got}  hops {w['hops']}"
                      f"{'  EXHAUSTED' if w['exhausted'] else ''}", file=sys.stderr)
        # The discovery arm: the same walker, map and ceiling, differing only in the block before
        # hop 0. The block is recorded on the result as `exposed`, verbatim, because what the walker
        # was shown is the experiment.
        if a.discovery:
            for fx, mp in zip(fixtures, maps):
                for q in fx["questions"]:
                    before = dict(walker.usage)
                    w = walker.walk(q["q"], preface=blocks[q["q"]])
                    got = [i for i in w["collected"] if i in texts]
                    r = score_question(q, got, a.k)
                    r.update(read=got, visited=w["visited"], hops=w["hops"], opens=w["opens"],
                             returns=w["returns"], turns=w["turns"], exhausted=w["exhausted"],
                             read_chars=w["read_chars"], log=w["log"], exposed=blocks[q["q"]],
                             usage={k: walker.usage[k] - before[k] for k in walker.usage})
                    rows.append(("routing+discovery", fx["id"], r))
                    print(f"    discov.  {q['q'][:50]:<50} read {got}  hops {w['hops']}"
                          f"{'  EXHAUSTED' if w['exhausted'] else ''}", file=sys.stderr)

    print()
    for arm in ["rag", "rag+rerank", "routing", "routing+discovery"]:
        rs = [r for a_, _, r in rows if a_ == arm]
        if not rs: continue
        f = sum(r["found"] for r in rs) / len(rs)
        b = sum(r["beats_distractors"] for r in rs) / len(rs)
        print(f"  {arm:<12} found {f:.3f}   operative {b:.3f}   n={len(rs)}")
    print()
    for arm, fid, r in rows:
        mark = "ok  " if r["beats_distractors"] else ("ORDER" if r["found"] else "MISS ")
        print(f"  {mark} {arm:<12} rank {str(r['rank']):>4}   {r['q'][:58]}")
        if r["outranked_by"]:
            for d in r["outranked_by"]:
                print(f"         outranked by {d} at {r['distractor_ranks'][d]}")

    out = {"tag": tag, "k": a.k, "n": a.n,
           "baseline": {"is": is_base, "why": why},
           **({"routing": {"walker": "bench/agent.py Agent — the pilot's in-process walker (OPEN/READ/BACK/DONE), "
                                      "not the claude -p census walker",
                           "provider": walker.provider, "model": walker.model, "steps": a.steps,
                           "use_when": os.environ.get("BENCH_USE_WHEN", "frozen"),
                           # The map as walked, verbatim: the lines are the system under test.
                           "maps": [{"fixture": fx["id"], "node": mp["node"]} for fx, mp in zip(fixtures, maps)]}}
              if walker else {}),
           # The discovery arm's whole difference from the control, verbatim, per question.
           **({"discovery": {"mechanism": "ontology/service/resolve.py over the grafted tree; names from "
                                          "<fixture>.names.yaml; block rendered by score.discovery_block",
                             "exposed": blocks}} if blocks else {}),
           "fixtures": [f["id"] for f in fixtures],
           "contributed_by": [f.get("contributed_by") for f in fixtures],
           "documents_in_pool": len(texts), "from_fixtures": added,
           "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "results": [dict(arm=a_, fixture=fid, **r) for a_, fid, r in rows]}
    if a.out:
        p = ROOT / a.out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
