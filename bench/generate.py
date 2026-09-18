#!/usr/bin/env python3
"""Expand bench/spec.yaml into documents, one cluster at a time.

The stratum never touches a document. It goes in bench/manifest.json, keyed by id — because the
frontmatter is part of what gets embedded, and a corpus that carries `stratum: S4` in its own text
would let the retriever read the answer sheet.

    ./bench/generate.py --pilot                 one cluster, printed, nothing written
    ./bench/generate.py --area expense --stratum S2
    ./bench/generate.py                          everything still missing from the manifest
"""
import argparse, json, os, pathlib, re, sys, time, urllib.request, urllib.error
from collections import Counter
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = ROOT / "corpus" / "regions"
SPEC = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
MANIFEST = ROOT / "manifest.json"
KINDS = ["topic", "rule", "procedure", "form", "table", "case", "system", "role", "deadline"]
MAX_CHILDREN = 25          # the vocabulary's own budget; exceeding it is a validation error
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)

PROVIDER = os.environ.get("BENCH_LLM_PROVIDER", "anthropic")
BASE = os.environ.get("BENCH_LLM_BASE_URL") or ("https://api.openai.com" if PROVIDER == "openai"
        else os.environ.get("ONTOLOGY_LLM_BASE_URL", "https://api.anthropic.com"))
KEY = (os.environ.get("BENCH_LLM_API_KEY") or (os.environ["EMBED_API_KEY"] if PROVIDER == "openai"
       else os.environ["ONTOLOGY_LLM_API_KEY"]))
# The install's own model is whatever the operator chose for the Suggest buttons — on this
# machine, Haiku. Generating 721 documents of prose is a different job, so this has its own
# setting and its own default.
MODEL = os.environ.get("BENCH_LLM_MODEL", "gpt-4o" if PROVIDER == "openai" else "claude-sonnet-5")


def existing():
    out = {}
    for p in CORPUS.rglob("*.md"):
        m = FM.match(p.read_text(encoding="utf-8"))
        fm = yaml.safe_load(m.group(1)) or {}
        out[fm.get("id") or p.stem] = {"area": p.parent.name, "parent": fm.get("parent"),
                                       "name": fm.get("name"), "one_liner": fm.get("one_liner"),
                                       "kind": fm.get("kind"), "path": p}
    return out


SYSTEM = """You write internal documentation for a Korean company's back office, in English.

You are extending a document set that already exists. Match it exactly: a markdown H1, then H2
sections, tables for anything with rates or bands, bold for the one trap a reader would otherwise
fall into, and a closing line that connects to a neighbouring subject. 900-1600 characters of body.

Rules that are not negotiable.
- Every amount, deadline and extension you use must be CONSISTENT WITH THE FACTS GIVEN. Do not invent
  a figure that contradicts one you were given. New figures for subjects not covered are fine.
- These are documents a person reads to do their job. They are NOT search-engine chunks: do not pad
  with keywords, do not restate the title, do not write "in this document we will".
- Write the trap. Real internal documentation earns its place by saying what goes wrong.
- Do not mention retrieval, search, embedding, or that this is an example or a corpus.
- **Sentence case for every title and heading**, never Title Case. The existing set reads
  "Entertainment caps and evidence" and "First-year days by joining month" — not "What the Travel
  Policy Actually Pays". Capitalisation that does not match is the one thing that makes a page look
  as though it came from somewhere else.

Answer in this format and nothing else. Markdown inside a JSON string breaks on the first newline,
so there is no JSON here — the delimiters are unambiguous and you must not vary them:

=== id: some-kebab-case-id
kind: rule
name: Short title
one_liner: one sentence, no trailing full stop
---
# The H1

...the body...

=== id: the-next-one
...

`id` must be unique, ASCII kebab-case, and must not collide with any id you were shown."""


def ask(prompt, max_tokens=12000):
    if PROVIDER == "anthropic":
        url, hdr = BASE.rstrip("/") + "/v1/messages", {"x-api-key": KEY, "anthropic-version": "2023-06-01"}
        # No `temperature`: the newer models reject it outright, and the variety wanted here comes
        # from the clusters being different subjects rather than from sampling.
        body = {"model": MODEL, "max_tokens": max_tokens, "system": SYSTEM,
                "messages": [{"role": "user", "content": prompt}]}
    else:
        url, hdr = BASE.rstrip("/") + "/v1/chat/completions", {"Authorization": f"Bearer {KEY}"}
        body = {"model": MODEL, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **hdr})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            if PROVIDER != "anthropic": return d["choices"][0]["message"]["content"]
            # Not `content[0]`: the first block is not always the answer — a model with extended
            # thinking on puts a `thinking` block in front of it, and indexing blindly raises
            # KeyError('text') on a response that is perfectly fine.
            text = "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
            if not text.strip():
                raise SystemExit("  the answer carried no text block: "
                                 + json.dumps([b.get("type") for b in d["content"]]))
            return text
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            if e.code in (429, 500, 502, 503, 529) and attempt < 5:
                time.sleep(5 * (attempt + 1)); continue
            raise SystemExit(f"  LLM {e.code}: {msg}")
        except Exception as e:
            # The run that died at 358 of 717 died here: `RemoteDisconnected`, which is not an
            # HTTPError and so fell straight past the retry above. Over a couple of hours of calls a
            # dropped connection is not an exceptional event, it is a certainty.
            if attempt < 5:
                print(f"      {type(e).__name__}: {e} — retrying", flush=True)
                time.sleep(5 * (attempt + 1)); continue
            raise SystemExit(f"  giving up after 6 attempts: {type(e).__name__}: {e}")


def facts(area, docs):
    """The figures already in this area, so the model cannot contradict them."""
    out = []
    for i, d in docs.items():
        if d["area"] != area: continue
        body = FM.match(d["path"].read_text(encoding="utf-8")).group(2)
        for line in body.splitlines():
            if re.search(r"\d[\d,]*\s?(KRW|USD|%)|\b\d+ (working days|days|years|months)\b", line):
                out.append(line.strip()[:150])
    return out[:40]


def prompt_for(area, stratum, cluster, docs, parent_id):
    here = {i: d for i, d in docs.items() if d["area"] == area}
    return f"""Write {cluster['n']} documents for the area `{area}`, all as children of `{parent_id}`.

SUBJECT: {cluster['topic']}
COVERING: {cluster['detail']}

Documents already in this area (id — one-liner). Do not duplicate these subjects, and do not reuse
an id:
""" + "\n".join(f"  {i} — {d['one_liner']}" for i, d in sorted(here.items())) + f"""

Figures already established in this area. Anything you write must be consistent with them:
""" + "\n".join(f"  {f}" for f in facts(area, docs)) + f"""

KINDS available: {', '.join(KINDS)}

Write {cluster['n']} documents. Vary the kind to suit the subject. They are siblings covering
different parts of the subject — not {cluster['n']} restatements of it."""


SEC = "sec-"


def slot(area, cluster, docs, made):
    """Where this cluster's documents hang.

    Its own section page if one exists — `bench/restructure.py` builds them, and a document written
    straight onto the area representative is how `expense` ended up with 265 children against a
    budget of 25. Falling back to the representative is correct only before the sections exist;
    running restructure afterwards moves them.
    """
    import re
    base = SEC + re.sub(r"[^a-z0-9]+", "-", cluster["topic"].lower()).strip("-")[:40]
    # A split cluster has sec-x-1, sec-x-2 …; the last one is the one still being filled.
    parts = sorted(i for i in docs if i.startswith(base))
    if base in docs and not any(i.startswith(base + "-") and i[len(base) + 1:].isdigit() for i in parts):
        return base
    numbered = [i for i in parts if i[len(base) + 1:].isdigit()]
    if numbered: return max(numbered, key=lambda i: int(i[len(base) + 1:]))
    rep = next(i for i, d in docs.items() if d["area"] == area and not d["parent"])
    want = cluster.get("under")
    return want if want in docs else rep


def write(doc, area, parent, stratum, cluster):
    p = CORPUS / area / f"{doc['id']}.md"
    fm = [f"id: {doc['id']}", f"name: {json.dumps(doc['name'], ensure_ascii=False)}",
          f"kind: {doc['kind']}", f"one_liner: {json.dumps(doc['one_liner'], ensure_ascii=False)}",
          f"parent: {parent}"]
    p.write_text("---\n" + "\n".join(fm) + "\n---\n" + doc["body"].strip() + "\n", encoding="utf-8")
    return {"id": doc["id"], "area": area, "parent": parent, "stratum": stratum,
            "cluster": cluster["topic"], "pair": cluster.get("pair")}


HEAD = re.compile(r"^=== id:\s*(\S+)\s*$", re.M)


def parse(text):
    """Split on the `=== id:` delimiter. Nothing here can be broken by the body's own content."""
    t = text.strip()
    if t.startswith("```"): t = re.sub(r"\A```[a-z]*\n|\n```\Z", "", t)
    marks = list(HEAD.finditer(t))
    if not marks: raise SystemExit("  no `=== id:` blocks in the answer:\n" + t[:400])
    out = []
    for m, nxt in zip(marks, marks[1:] + [None]):
        chunk = t[m.end():(nxt.start() if nxt else len(t))]
        head, _, body = chunk.partition("\n---\n")
        fields = {"id": m.group(1)}
        for line in head.strip().splitlines():
            k, _, v = line.partition(":")
            if k.strip() in ("kind", "name", "one_liner"): fields[k.strip()] = v.strip()
        if not body.strip() or not fields.get("name") or not fields.get("one_liner"):
            print(f"      skip {fields['id']}: incomplete block"); continue
        fields["body"] = body.strip()
        out.append(fields)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--area"); ap.add_argument("--stratum"); ap.add_argument("--limit", type=int)
    a = ap.parse_args()

    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    docs = existing()
    # How many of each cluster already exist, so a run that stopped part-way through one finishes it
    # rather than skipping it. The first version asked whether the cluster had *any* document and
    # moved on if it did — which, after the connection dropped mid-cluster, would have left that
    # cluster permanently short and the stratum counts quietly wrong.
    done = Counter((m["area"], m["cluster"]) for m in man.values())
    jobs = []
    for area in SPEC:
        for s in ("S1", "S2", "S3", "S4"):
            for c in SPEC[area][s]:
                if a.area and area != a.area: continue
                if a.stratum and s != a.stratum: continue
                left = c["n"] - done.get((area, c["topic"]), 0)
                if left > 0: jobs.append((area, s, {**c, "n": left}))
    if a.pilot: jobs = jobs[:1]
    if a.limit: jobs = jobs[:a.limit]
    print(f"  {len(jobs)} cluster(s), {sum(c['n'] for _, _, c in jobs)} documents, model {MODEL}")

    # Asked for in batches rather than a cluster at a time. A single call for twenty-four full
    # documents is thirty thousand characters of output: it risks being truncated mid-document, it
    # shows no progress for minutes, and one failure loses the lot. Eight is small enough to be quick
    # and large enough that the model still writes them as siblings rather than as eight separate
    # answers to the same brief.
    BATCH = 8
    for area, stratum, cluster in jobs:
        parent = slot(area, cluster, docs, man)
        print(f"\n  {area}/{stratum}  {cluster['topic']}  ×{cluster['n']}  under {parent}", flush=True)
        made = 0
        while made < cluster["n"]:
            want = min(BATCH, cluster["n"] - made)
            sub = {**cluster, "n": want}
            out = parse(ask(prompt_for(area, stratum, sub, docs, parent)))
            if a.pilot:
                for d in out: print(f"\n{'─'*80}\n{d['id']}  [{d['kind']}]  {d['name']}\n  {d['one_liner']}\n\n{d['body'][:600]}")
                print(f"\n  PILOT — {len(out)} documents, nothing written")
                return
            wrote = 0
            for d in out:
                if d["id"] in docs or d["id"] in man: print(f"      skip duplicate id {d['id']}", flush=True); continue
                if d["kind"] not in KINDS: d["kind"] = "topic"
                man[d["id"]] = write(d, area, parent, stratum, cluster)
                docs[d["id"]] = {"area": area, "parent": parent, "name": d["name"],
                                 "one_liner": d["one_liner"], "kind": d["kind"],
                                 "path": CORPUS / area / f"{d['id']}.md"}
                wrote += 1
            MANIFEST.write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
            made += wrote
            print(f"      +{wrote}  ({made}/{cluster['n']} in this cluster, {len(man)} written overall)", flush=True)
            if wrote == 0:
                print("      nothing new came back; moving on rather than looping", flush=True); break


if __name__ == "__main__":
    main()
