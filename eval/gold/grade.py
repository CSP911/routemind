#!/usr/bin/env python3
"""Grade a gold set: measure A, take B from the label, read C/D/E, compute the band.

A is *measured*, not trusted. A question written to be a paraphrase can share more vocabulary with
its answer than intended, and the intent is only a record of what was attempted — eval/DIFFICULTY.md
defines A as a fraction of the question's content tokens that appear in the answer document, and
that is what is computed here.

    ./eval/gold/grade.py eval/gold/pilot.yaml
    ./eval/gold/grade.py eval/gold/pilot.yaml --csv
"""
import argparse, csv, pathlib, re, sys
from collections import Counter
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
STOP = set("a an and are as at be by for for from has have how i in into is it its me my of on or "
           "that the them they this to was we what when where which who will with you your not no "
           "do does did can may might would should there here if then than so but".split())
# A: fraction of the question's content tokens present in the answer document (DIFFICULTY.md §A)
A_CUTS = (0.75, 0.50, 0.25)
BANDS = (("easy", 0, 2), ("moderate", 3, 5), ("hard", 6, 9), ("severe", 10, 15))


def toks(t):
    return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 2}


def corpus():
    out = {}
    for p in (ROOT / "bench" / "corpus" / "regions").rglob("*.md"):
        m = FM.match(p.read_text(encoding="utf-8"))
        fm = yaml.safe_load(m.group(1)) or {}
        out[fm.get("id") or p.stem] = f"{fm.get('name','')} {fm.get('one_liner','')} {m.group(2)}"
    return out


def factors():
    path = ROOT / "bench" / "factors.csv"
    return {r["id"]: r for r in csv.DictReader(l for l in open(path) if not l.startswith("#"))}


def grade(q, docs, fac):
    qt = toks(q["q"])
    # Measured against the union of the answer documents: any of them answering is an answer.
    dt = set().union(*(toks(docs[d]) for d in q["D_true"] if d in docs)) if q["D_true"] else set()
    share = len(qt & dt) / len(qt) if qt else 0.0
    A = next((n for n, c in enumerate(A_CUTS) if share >= c), 3)
    B = q["intent_B"]
    # C, D, E come from the answer document. Where there are several, the hardest governs: the
    # question is only as easy as the easiest way to reach an answer, and the easiest way is the one
    # with the *lowest* factor sum.
    rows = [fac[d] for d in q["D_true"] if d in fac]
    if rows:
        best = min(rows, key=lambda r: int(r["CDE"]))
        C, D, E = int(best["C"]), int(best["D"]), int(best["E"])
    else:
        C = D = E = 0
    total = A + B + C + D + E
    band = next(n for n, lo, hi in BANDS if lo <= total <= hi)
    return {"id": q["id"], "A": A, "B": B, "C": C, "D": D, "E": E, "sum": total,
            "band": band, "share": share, "intent_A": q["intent_A"],
            "areas": len(q["A_true"]), "needs": q["needs"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("--csv", action="store_true")
    a = ap.parse_args()
    g = yaml.safe_load(pathlib.Path(a.path).read_text(encoding="utf-8"))
    docs, fac = corpus(), factors()
    missing = [d for q in g["questions"] for d in q["D_true"] if d not in docs]
    if missing: sys.exit(f"  D_true names documents not in the corpus: {missing}")
    out = [grade(q, docs, fac) for q in g["questions"]]
    if a.csv:
        print("id,A,B,C,D,E,sum,band,lexical_share,intent_A,areas,needs")
        for r in out:
            print(f"{r['id']},{r['A']},{r['B']},{r['C']},{r['D']},{r['E']},{r['sum']},{r['band']},"
                  f"{r['share']:.3f},{r['intent_A']},{r['areas']},{r['needs']}")
        return
    print(f"  {len(out)} questions\n")
    print("  id    A B C D E   sum  band        lexical  intent_A")
    for r in out:
        flag = "" if r["A"] == r["intent_A"] else f"  <- wrote for A{r['intent_A']}"
        print(f"  {r['id']:<5} {r['A']} {r['B']} {r['C']} {r['D']} {r['E']}   {r['sum']:>3}  "
              f"{r['band']:<10}  {r['share']:.2f}     {r['intent_A']}{flag}")
    print(f"\n  bands: {dict(Counter(r['band'] for r in out))}")
    agree = sum(1 for r in out if r["A"] == r["intent_A"])
    print(f"  measured A matched intent: {agree}/{len(out)}")


if __name__ == "__main__":
    main()
