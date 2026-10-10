#!/usr/bin/env python3
"""Where each walk was lost: the area, or the document inside it — and the public claims, rechecked.

    ./bench/attribution.py --out eval/runs/<date>-attribution.json

Issue #2 asks for per-query records an outside auditor can attribute failures with. The answer
there mapped their fields onto the files as they stand and said `selected_area_id` "is not a field,
but readable from each walk's report". This reads it, so nobody has to: an area counts as entered
when a command in the walk names `/v1/regions/<area>` — `table` it, or (the overlay arm) make it an
overlay `--member`. Then each walk is one of

    found       cited a gold document
    area        never entered any gold area — the hop-0 choice lost it
    document    entered a gold area and still cited none of the gold documents

No model, no network: only the census and gold files. It also re-derives the numbers that answer
quoted (the reranker-never-fired split, the scoped ceiling), so a claim made in public is one this
script fails on if the files stop saying it.
"""
import argparse, collections, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bench"))
import yaml

RUNS = ROOT / "eval" / "runs"
AREA = re.compile(r"/v1/regions/([a-z0-9-]+)")


def gold():
    out = {}
    for f in ("hard.yaml", "hard-temporal.yaml"):
        for q in yaml.safe_load((ROOT / "eval" / "gold" / f).read_text())["questions"]:
            out[q["id"]] = q
    return out


def attribute(walk, q):
    # The commands section only — the answer and sources below it may name an area it never entered.
    commands = (walk.get("report") or "").split("**Answer**", 1)[0]
    entered = list(dict.fromkeys(AREA.findall(commands)))
    a_true = set(q.get("A_true") or [])
    if walk["hit"]:
        stage = "found"
    elif not a_true & set(entered):
        stage = "area"
    else:
        stage = "document"
    return {"id": walk["id"], "arm": walk["arm"], "lever": q.get("lever"), "family": q.get("family"),
            "A_true": sorted(a_true), "entered": entered, "no_matching_area": not entered,
            "hit": walk["hit"], "stage": stage}


def claims(census):
    """The numbers the issue #2 answer stated, recomputed. Each is (what, expected, found)."""
    out = []
    hard = json.loads((RUNS / "2026-09-20b-retrieval-hard.json").read_text())
    temp = json.loads((RUNS / "2026-09-20b-retrieval-temporal.json").read_text())
    rr = [r for r in hard["results"] + temp["results"] if r["arm"] != "rag"]
    never = [r for r in rr if not r["reranked"]]
    ind = sum(1 for r in never if r["id"].endswith("-i"))
    out.append(("reranker never fired", 310, len(never)))
    out.append(("… of them indirect", 287, ind))
    out.append(("… of them temporal", 23, sum(1 for r in never if r["id"].startswith("t-"))))
    out.append(("… all inside retrieval failures", 0, sum(1 for r in never if r["retrieval_hit"])))
    out.append(("ranked ids saved per query, at most", 10, max(len(r["top"]) for r in rr)))
    out.append(("census walks", 1400, len(census["walks"])))
    out.append(("census fingerprint", "a84ac6cf463a1a6d", census["meta"]["fingerprint"]))
    out.append(("retrieval fingerprint", "a84ac6cf463a1a6d", hard["fingerprint"]))
    s = json.loads((RUNS / "2026-10-01-scoped-ceiling.json").read_text())["table"]["indirect"]
    out.append(("indirect recall@20, whole corpus", 0.103, round(s["full@20"], 3)))
    out.append(("indirect recall@20, gold area handed over", 0.134, round(s["scoped@20"], 3)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    census = json.loads((RUNS / "2026-09-20-census.json").read_text())
    g = gold()
    rows = [attribute(w, g[w["id"]]) for w in census["walks"]]
    table = collections.defaultdict(collections.Counter)
    for r in rows:
        table[r["arm"]][r["stage"]] += 1
    for arm, c in sorted(table.items()):
        print(f"{arm:18} " + "  ".join(f"{k} {c[k]}" for k in ("found", "area", "document")))
    for r in rows:
        if r["stage"] != "found":
            print(f"  lost  {r['arm']:16} {r['id']:22} {r['stage']:8} entered={r['entered']} gold={r['A_true']}")
    bad = 0
    for what, want, got in claims(census):
        ok = want == got
        bad += not ok
        print(f"  {'ok ' if ok else 'BAD'}  {what}: stated {want}, files say {got}")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps({
            "fingerprint": census["meta"]["fingerprint"], "source": "eval/runs/2026-09-20-census.json",
            "rule": "entered = areas a command in the walk names as /v1/regions/<area> (table, or overlay --member)",
            "summary": {k: dict(v) for k, v in table.items()},
            "claims": [{"what": w, "stated": s, "files": f} for w, s, f in claims(census)],
            "walks": rows}, indent=1, ensure_ascii=False) + "\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
