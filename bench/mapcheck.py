#!/usr/bin/env python3
"""Is the routing table a fair description of the corpus it sits over? A precondition, not a result.

The study tests whether a **well-kept** routing layer earns its upkeep. A table that has gone stale
is a different thing to measure, and measuring it by accident is how three runs were thrown away:
two families sat in areas where this corpus does not keep those subjects, a new section's one-liner
read as an index rather than as the current table, and every supersession notice was filed inside the
section a mistaken walk never reaches. All three were found by watching walks fail, which is the
expensive way and also the wrong way — a walk failing cannot tell you whether the map or the model
was at fault.

So the map is checked before the arms run, the way `PREREGISTRATION.md` §2 checks the corpus.

**The rules are written from a principle, not from a score.** A person holding this map must be able
to (1) find the area a subject lives in, (2) tell a current table from one it replaced, and (3) get
out of an area whose subject has moved. Each rule below is a property of the table against the
corpus, decidable without running anything and without knowing any result. That matters: "it was a
precondition, not tuning" is exactly what someone would say after fitting to their own questions, and
the only thing that separates the two is whether the rule could have been written in advance and
applied where it hurts.

    ./bench/mapcheck.py
"""
import json, os, re, sys
import yaml

ROOT = __import__("pathlib").Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main():
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    import run as runner
    import crowd
    texts, area, one, kids, has_body = runner.corpus()
    rows = runner.rows()
    man = json.loads((ROOT / "crowd-manifest.json").read_text())

    fails, notes = [], []

    def check(ok, rule, detail):
        (notes if ok else fails).append((rule, detail))

    # R1 — a family sits in the area where this corpus already keeps that subject. The corpus decides
    # where a subject lives; a new table on an old subject that lands somewhere else is not a routing
    # problem for the walker to solve, it is a filing error.
    for fam in crowd.FAMILIES:
        homes = {area[i] for i, _ in fam["supersedes"] if i in area}
        check(fam["area"] in homes or not homes, "R1 family is filed where the subject lives",
              f"{fam['key']}: table in {fam['area']}, superseded pages in {sorted(homes)}")

    # R2 — every subject with a section under an area is named in that area's hop-0 sentence. A walk
    # chooses an area from that sentence alone; a subject the sentence never mentions is a subject
    # the walk has no reason to look for here.
    for a, sent in rows.items():
        low = sent.lower()
        for k in kids.get(a, []):
            if not k.startswith("sec-hard-"): continue
            subj = next((f["subject"] for f in crowd.FAMILIES if f"sec-hard-{f['key']}" == k), "")
            head = subj.split()[0].lower() if subj else ""
            check(head and head in low, "R2 hop 0 names what the area holds",
                  f"{a}: '{subj}' — hop 0 {'mentions' if head in low else 'never mentions'} it")

    # R3 — a section that supersedes another says so in its one-liner, because the one-liner is the
    # only line a walk sees when it chooses between them.
    for fam in crowd.FAMILIES:
        sec = f"sec-hard-{fam['key']}"
        ol = one.get(sec, "")
        check(("current" in ol.lower()) and re.search(r"\d{4}-\d{2}-\d{2}", ol),
              "R3 a replacing section says it is current, where the walker sees it",
              f"{sec}: {'ok' if 'current' in ol.lower() else 'one-liner reads as an index'}")

    # R4 — every area holding a superseded page holds a notice about it, at the area itself. A notice
    # filed inside the section that replaced it is invisible to the walk that went to the old one.
    sup_by_area = {}
    for fam in crowd.FAMILIES:
        for i, _ in fam["supersedes"]:
            if i in area: sup_by_area.setdefault(area[i], set()).add(fam["key"])
    for a, fams in sorted(sup_by_area.items()):
        at_area = {man.get(k, {}).get("family") for k in kids.get(a, [])
                   if man.get(k, {}).get("legend") in ("revision", "moved")}
        for f in sorted(fams):
            check(f in at_area, "R4 a superseded subject is flagged in its own area",
                  f"{a}: {f} — {'notice present' if f in at_area else 'NO notice at this area'}")

    # R5 — nothing claims to supersede a document about a different subject. An over-claim scores a
    # correct retrieval as a stale answer, which is a labelling error wearing a result's clothes.
    for fam in crowd.FAMILIES:
        for i, name in fam["supersedes"]:
            check(i in texts or i in area, "R5 supersession targets exist",
                  f"{fam['key']} -> {i}")

    print(f"\n  routing table vs corpus — {len(notes)} pass, {len(fails)} fail\n")
    for rule, detail in notes:
        if detail: print(f"    ok    {rule[:4]}  {detail}")
    for rule, detail in fails:
        print(f"    FAIL  {rule}\n          {detail}")
    if fails:
        print(f"\n  The table does not describe this corpus. Measuring an arm against it measures the")
        print(f"  map's condition, not the routing idea. Fix, then run.\n")
        sys.exit(1)
    print("\n  The table describes the corpus. This is the condition the arms are measured under,")
    print("  and it is recorded with the run rather than assumed.\n")


if __name__ == "__main__":
    main()
