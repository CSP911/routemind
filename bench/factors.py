#!/usr/bin/env python3
"""The document side of the difficulty scale — C, D and E for every document.

eval/DIFFICULTY.md defines five factors. Two of them are properties of a (question, answer) pair and
cannot exist before the questions do:

    A  lexical bridge   how much vocabulary the question shares with its answer
    B  area spread      how many areas the answer needs

The other three are properties of a document and its place in the corpus, and they are what decides
which band a document can *support*. A question written against a document with C+D+E = 1 cannot be
severe however it is phrased; one with C+D+E = 7 cannot be easy.

    C  depth            hops from hop 0 to the document
    D  routing margin   gap between the best-matching area description and the second
    E  crowding         documents within 0.70 cosine

    ./bench/factors.py              the distribution, and what each band can draw on
    ./bench/factors.py --csv        id,area,stratum,depth,margin,crowd,C,D,E,CDE — for choosing documents

**The model is pinned to `text-embedding-3-large` and printed with every result.** It was meant to be
a different model from the one the arms use, and measuring showed that cannot be had for free: across
`3-large` and `ada-002`, D agreed on 27% of documents, E on 8%, and 79% changed band. Absolute
thresholds do not carry between embeddings. Quantile thresholds would carry, and would also make the
79-vs-800 scale comparison vacuous by fixing the share of hard documents. So the cuts stay absolute,
the model is pinned, and the cost is written down. DIFFICULTY.md has the numbers.
"""
import argparse, itertools, json, os, pathlib, re, sys
from collections import Counter
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from retrieve import Dense
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)

# The cuts are the corpus's own quartiles, measured 2026-09-18 and recorded in DIFFICULTY.md so a
# later corpus is compared against them rather than re-quartiled into agreement.
DEPTH_CUTS  = (1, 2, 4)          # 0: ≤1 · 1: 2 · 2: 3–4 · 3: 5+
MARGIN_CUTS = (0.129, 0.072, 0.034)   # 0: > .129 · 1: > .072 · 2: > .034 · 3: ≤ .034
CROWD_CUTS  = (0, 2, 5)          # 0: 0 · 1: 1–2 · 2: 3–5 · 3: 6+
NEIGHBOUR   = 0.70               # chosen because it discriminates: at 0.80, 74% have no neighbour


def band(v, cuts, descending=False):
    if descending:
        for n, c in enumerate(cuts):
            if v > c: return n
        return len(cuts)
    for n, c in enumerate(cuts):
        if v <= c: return n
    return len(cuts)


def load():
    man = json.loads((ROOT / "manifest.json").read_text())
    spec = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
    clauses = {a: [c.strip() for c in spec[a]["frozen_use_when"].split("·")] for a in spec}
    texts, parent = {}, {}
    for p in (ROOT / "corpus" / "regions").rglob("*.md"):
        m = FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
        i = fm.get("id") or p.stem
        parent[i] = fm.get("parent")
        if i in man and not man[i].get("section"):
            texts[i] = f"{fm.get('name','')}. {fm.get('one_liner','')}\n\n{m.group(2).strip()}"
    return man, clauses, texts, parent


def measure():
    man, clauses, texts, parent = load()
    # Pinned, not inherited from EMBED_MODEL: the cuts below are that model's quartiles and mean
    # nothing under another. FACTOR_EMBED_MODEL overrides it for the sensitivity check only.
    model = os.environ.get("FACTOR_EMBED_MODEL", "text-embedding-3-large")
    d = Dense(cache=ROOT / f"embeddings-factors.json")
    d.model = model
    flat = [(a, c) for a, cs in clauses.items() for c in cs]
    cv = dict(zip(flat, d.embed([c for _, c in flat])))
    ids = list(texts)
    dv = dict(zip(ids, d.embed([texts[i] for i in ids])))
    cos = lambda u, v: sum(x * y for x, y in zip(u, v))

    def depth(i, n=0):
        par = parent.get(i)
        return n if not par or n > 8 else depth(par, n + 1)

    nb = Counter()
    for a, b in itertools.combinations(ids, 2):
        if cos(dv[a], dv[b]) > NEIGHBOUR: nb[a] += 1; nb[b] += 1

    out = {}
    for i in ids:
        sc = sorted((max(cos(dv[i], cv[(a, c)]) for c in clauses[a]) for a in clauses), reverse=True)
        margin = sc[0] - sc[1]
        dep = depth(i)
        out[i] = {"area": man[i]["area"], "stratum": man[i]["stratum"], "cluster": man[i]["cluster"],
                  "depth": dep, "margin": margin, "crowd": nb[i],
                  "C": band(dep, DEPTH_CUTS), "D": band(margin, MARGIN_CUTS, descending=True),
                  "E": band(nb[i], CROWD_CUTS)}
        out[i]["CDE"] = out[i]["C"] + out[i]["D"] + out[i]["E"]
    return out, model


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--csv", action="store_true"); a = ap.parse_args()
    out, model = measure()
    if a.csv:
        print(f"# D and E computed with {model}")
        print("id,area,stratum,depth,margin,crowd,C,D,E,CDE")
        for i, r in sorted(out.items(), key=lambda kv: -kv[1]["CDE"]):
            print(f"{i},{r['area']},{r['stratum']},{r['depth']},{r['margin']:.4f},{r['crowd']},"
                  f"{r['C']},{r['D']},{r['E']},{r['CDE']}")
        return
    print(f"  {len(out)} documents · D and E computed with {model}\n")
    for name, k in (("C depth", "C"), ("D margin", "D"), ("E crowding", "E")):
        c = Counter(r[k] for r in out.values())
        print(f"  {name:<12} " + "   ".join(f"{lv}:{c.get(lv,0):>4}" for lv in range(4)))
    cde = Counter(r["CDE"] for r in out.values())
    print(f"\n  C+D+E (0–9)   " + "  ".join(f"{k}:{v}" for k, v in sorted(cde.items())))
    # A question adds A and B, each 0–3. So a document with C+D+E = s reaches bands [s, s+6].
    print(f"\n  what each band can be built on (a question adds A+B, 0–6):")
    for label, lo, hi in (("쉬움 easy", 0, 2), ("보통 moderate", 3, 5), ("어려움 hard", 6, 9), ("극악 severe", 10, 15)):
        n = sum(v for s, v in cde.items() if s <= hi and s + 6 >= lo)
        print(f"      {label:<16} {n:>4} documents   (need C+D+E between {max(0, lo-6)} and {hi})")


if __name__ == "__main__":
    main()
