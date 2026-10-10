#!/usr/bin/env python3
"""Flat or folded — does the shape of the tree change what a walking agent finds?

    ./eval/depth/run.py --pilot              6 questions, both trees: a cost and sanity check
    ./eval/depth/run.py                      all 73 questions, both trees
    ./eval/depth/run.py --report             the table, from what is on disk

The same documents, the same questions, the same agent (`bench/agent.py`), two trees:

    folded   the bench corpus as built — documents under section holders, up to five levels deep
    flat     every holder taken out and what it held lifted to the nearest ancestor that is not one,
             which is what `knowledge_place` produced before change sets: leaves under the first node
             a walk stopped at, and area tables a few hundred rows long

Nothing else differs: hop 0 is the same five frozen sentences, every document keeps its one-liner,
READ hands back the same text. See README.md for the predictions, written before the first walk.

Resumable: every walk is a file under `eval/runs/depth/<tree>/<question>.json`, and a walk already
on disk is not walked again.
"""
import argparse, concurrent.futures as cf, json, os, pathlib, sys, time
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bench"))
os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
import run as bench                    # noqa: E402  the bench's own corpus and hop 0
from agent import Agent                # noqa: E402

# A second run with another walker goes beside the first, never into it: DEPTH_RUN=cli-sonnet writes to
# eval/runs/depth-cli-sonnet/. The first run (claude-sonnet-5 through the API) stays where it is.
OUT = ROOT / "eval" / "runs" / ("depth" + (f"-{os.environ['DEPTH_RUN']}" if os.environ.get("DEPTH_RUN") else ""))
GOLD = ["eval/gold/pilot.yaml", "eval/gold/hard.yaml", "eval/gold/hard-temporal.yaml"]
PILOT = ["e1", "s1", "h-perdiem-000-i", "h-threshold-000-d", "t-accrual-01", "t-overtime-05"]


def questions():
    by = {q["id"]: q for f in GOLD for q in yaml.safe_load((ROOT / f).read_text(encoding="utf-8"))["questions"]}
    pilot = [q["id"] for q in yaml.safe_load((ROOT / GOLD[0]).read_text(encoding="utf-8"))["questions"]]
    sample = yaml.safe_load((ROOT / "eval/gold/walk-sample50.yaml").read_text(encoding="utf-8"))["questions"]
    return by, pilot + sample


def trees():
    texts, area, one_liner, children, has_body = bench.corpus()
    parent = {c: p for p, cs in children.items() for c in cs}
    holder = {i for i in one_liner if i.startswith("sec-")}
    def lift(i):
        p = parent.get(i)
        while p in holder: p = parent.get(p)
        return p
    flat = {}
    for i in one_liner:
        if i in holder: continue
        p = lift(i)
        if p and p != i: flat.setdefault(p, []).append(i)
    for k in flat: flat[k].sort()
    return texts, area, one_liner, has_body, {"folded": children, "flat": flat}, holder


def shape(children, roots):
    """Depth and width of a tree, from its five areas."""
    widths = [len(v) for v in children.values()]
    depth, stack = {}, [(r, 0) for r in roots]
    while stack:
        n, d = stack.pop(); depth[n] = d
        stack += [(c, d + 1) for c in children.get(n, [])]
    return {"entities": len(depth), "max_depth": max(depth.values()), "widest": max(widths),
            "area_rows": {r: len(children.get(r, [])) for r in sorted(roots)},
            "tables_over_25": sum(w > 25 for w in widths)}


def scored(q, walk):
    alt = q.get("D_alt") or {}
    got = set(walk["collected"])
    found = [d for d in q["D_true"] if d in got or set(alt.get(d, [])) & got]
    hit = bool(found) if q["needs"] == "any" else len(found) == len(q["D_true"])
    return {"hit": hit, "found": found, "collected": walk["collected"],
            "precision": (len([c for c in got if c in q["D_true"] or any(c in v for v in alt.values())]) / len(got)) if got else 0.0}


def walk_one(tree, q, agent_args):
    path = OUT / tree / f"{q['id']}.json"
    if path.exists(): return json.loads(path.read_text())
    ag = Agent(**agent_args)
    t0 = time.time()
    try:
        w = ag.walk(q["q"])
    except Exception as e:
        return {"id": q["id"], "tree": tree, "error": str(e)[:300]}
    rec = {"id": q["id"], "tree": tree, "q": q["q"], "needs": q["needs"], "lever": q.get("lever") or "pilot",
           "family": q.get("family") or "", **scored(q, w), "turns": w["turns"], "opens": w["opens"],
           "returns": w["returns"], "exhausted": w["exhausted"], "read_chars": w["read_chars"],
           "usage": ag.usage, "seconds": round(time.time() - t0, 1), "model": ag.model, "log": w["log"]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def cost(u):
    # What the CLI reported when the walker was `claude -p`; otherwise Sonnet-class list prices per
    # million tokens — an estimate, said so wherever it is printed.
    if "cost_usd" in u: return float(u["cost_usd"])
    return (u["in"] * 3 + u["cache_write"] * 3.75 + u["cache_read"] * 0.3 + u["out"] * 15) / 1e6


def report():
    by, ids = questions()
    rows = {t: {} for t in ("folded", "flat")}
    for t in rows:
        for f in (OUT / t).glob("*.json"):
            r = json.loads(f.read_text())
            if "error" not in r: rows[t][r["id"]] = r
    both = sorted(set(rows["folded"]) & set(rows["flat"]))
    if not both: print("nothing walked on both trees yet"); return
    def line(name, sel):
        out = [f"  {name:<22}"]
        for t in ("folded", "flat"):
            rs = [rows[t][i] for i in sel]
            n = len(rs)
            out.append(f"{t}: hit {sum(r['hit'] for r in rs)}/{n} ({sum(r['hit'] for r in rs)/n:.0%})  "
                       f"turns {sum(r['turns'] for r in rs)/n:.1f}  opens {sum(r['opens'] for r in rs)/n:.1f}  "
                       f"back {sum(r['returns'] for r in rs)/n:.1f}  ${sum(cost(r['usage']) for r in rs)/n:.3f}/walk")
        return "   ".join(out)
    groups = {"all": both}
    for i in both:
        g = rows["folded"][i]["lever"]
        g = "pilot" if g == "pilot" else ("indirect" if g == "indirect" else "direct" if g == "direct" else "temporal")
        groups.setdefault(g, []).append(i)
    print(f"  {len(both)} questions walked on both trees")
    for g, sel in groups.items(): print(line(f"{g} ({len(sel)})", sel))
    b = sum(1 for i in both if rows["folded"][i]["hit"] and not rows["flat"][i]["hit"])
    c = sum(1 for i in both if rows["flat"][i]["hit"] and not rows["folded"][i]["hit"])
    from math import comb
    n = b + c
    p = min(1.0, 2 * sum(comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n) if n else 1.0
    print(f"  discordant: folded only {b}, flat only {c} — exact McNemar p = {p:.3f}")
    ex = {t: sum(rows[t][i]["exhausted"] for i in both) for t in rows}
    print(f"  ran out of turns: folded {ex['folded']}, flat {ex['flat']}")
    tot = {t: sum(cost(rows[t][i]["usage"]) for i in both) for t in rows}
    print(f"  estimated spend: folded ${tot['folded']:.2f}, flat ${tot['flat']:.2f} (Sonnet-class list prices)")
    return rows, both


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--parallel", type=int, default=6)
    ap.add_argument("--steps", type=int, default=30)
    a = ap.parse_args()
    if a.report: report(); return
    by, ids = questions()
    if a.pilot: ids = PILOT
    texts, area, one_liner, has_body, tr, holder = trees()
    rows = bench.rows()
    for t, ch in tr.items():
        print(f"  {t:<7} {json.dumps(shape(ch, rows.keys()))}")
    jobs = []
    for t, ch in tr.items():
        args = dict(rows=rows, children=ch, one_liner=one_liner, has_body=has_body, steps=a.steps, body=texts)
        jobs += [(t, by[i], args) for i in ids]
    print(f"  {len(jobs)} walks · model {os.environ.get('ROUTER_MODEL', 'claude-opus-5')} · {a.parallel} at a time", flush=True)
    done = 0
    with cf.ThreadPoolExecutor(a.parallel) as ex:
        for r in cf.as_completed([ex.submit(walk_one, *j) for j in jobs]):
            r = r.result(); done += 1
            if "error" in r: print(f"  [{done}/{len(jobs)}] {r['tree']:<6} {r['id']:<22} ERROR {r['error'][:120]}", flush=True); continue
            print(f"  [{done}/{len(jobs)}] {r['tree']:<6} {r['id']:<22} {'HIT ' if r['hit'] else 'miss'} "
                  f"turns {r['turns']:>2} opens {r['opens']:>2} back {r['returns']} ${cost(r['usage']):.3f}", flush=True)
    report()


if __name__ == "__main__":
    main()
