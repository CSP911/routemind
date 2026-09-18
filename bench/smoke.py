#!/usr/bin/env python3
"""Retrieve + rerank, end to end, on whatever is in the corpus right now.

Not the experiment — the experiment needs the questions and they are not written yet. This is here
so the two halves are known to work together before they are load-bearing.
"""
import json, pathlib, re, sys, yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from retrieve import Hybrid
from rerank import LLMReranker

ROOT = pathlib.Path(__file__).resolve().parent
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)

docs = {}
for p in sorted((ROOT / "corpus" / "regions").rglob("*.md")):
    m = FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
    i = fm.get("id") or p.stem
    docs[i] = {"area": p.parent.name, "name": fm.get("name", ""), "one_liner": fm.get("one_liner", ""),
               "body": m.group(2).strip()}

# What is indexed: the document, without `use_when`. `use_when` is the routing line the table is made
# of — the arm that runs without a table must not be fed it, or the comparison is over before it runs.
texts = {i: f"{d['name']}. {d['one_liner']}\n\n{d['body']}" for i, d in docs.items()}
print(f"  {len(texts)} documents indexed")

h = Hybrid(texts).warm()
rr = LLMReranker()

QS = ["what do I do if I lose the receipt for something I paid for in cash abroad",
      "who has to approve buying something that costs four million won"]
for q in QS:
    top = h.search(q, n=8)
    print(f"\n  Q: {q}")
    print("     retrieved:")
    for n, i in enumerate(top[:5], 1): print(f"       {n}. [{docs[i]['area']:<11}] {i}")
    ranked = rr.rank(q, top, texts)
    print("     reranked:")
    for n, i in enumerate(ranked[:5], 1): print(f"       {n}. [{docs[i]['area']:<11}] {i}")
