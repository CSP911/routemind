#!/usr/bin/env python3
"""Give the generated corpus a tree — computed from the spec, not accumulated.

Every generated document was written as a direct child of its area's representative, because
`slot()` looked for an `under:` the spec did not carry. Two things broke: `expense` had 265 children
against a budget of 25, so the corpus did not validate; and arm A3 removes the hierarchy, which
means there has to be one.

**Idempotent by construction.** The first version named a section by looking at what was already on
disk, so a second run produced `domestic-trip-cases-cases`, sections parented under their own
siblings, and cycles in the tree. Section ids are now derived from the spec alone and the run
reconciles: keep what matches, delete what does not, write what is missing. Running it twice is the
same as running it once, on any state.

    ./bench/restructure.py --plan
    ./bench/restructure.py
"""
import argparse, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = ROOT / "corpus" / "regions"
SPEC = yaml.safe_load((ROOT / "spec.yaml").read_text(encoding="utf-8"))
MANIFEST = ROOT / "manifest.json"
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
MAX_CHILDREN, SPLIT_AT = 25, 20


# A section id is the cluster's slug behind a prefix no generated document uses. Without the prefix
# they collide: `slug("Supplier due diligence")` is `supplier-due-diligence`, and the generator had
# already written a document with exactly that id — so the section became its own parent and the tree
# had a cycle in it. The prefix also makes a stale section identifiable on disk, which matters because
# the manifest is not a reliable record of what was written.
SEC = "sec-"


def slug(t):
    return SEC + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:40]


def read(p):
    m = FM.match(p.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def set_parent(p, parent):
    fm, body = FM.match(p.read_text(encoding="utf-8")).groups()
    keep = [l for l in fm.split("\n") if not l.startswith("parent:")]
    p.write_text("---\n" + "\n".join(keep) + f"\nparent: {parent}\n---\n" + body, encoding="utf-8")


def intended(man, on_disk):
    """The tree the spec asks for. Depends on nothing that is already on disk."""
    members = {}
    for i, m in man.items():
        if m.get("section"): continue                      # a section is not a member of its cluster
        members.setdefault((m["area"], m["cluster"]), []).append(i)

    sections, parent_of = {}, {}
    for area in SPEC:
        rep = next(i for i, p in on_disk.items()
                   if p.parent.name == area and not read(p)[0].get("parent") and i not in man)
        for stratum in ("S1", "S2", "S3", "S4"):
            for c in SPEC[area][stratum]:
                ids = sorted(members.get((area, c["topic"]), []))
                if not ids: continue
                under = c["under"] if c.get("under") in on_disk else rep
                base = slug(c["topic"])
                k = max(1, -(-len(ids) // SPLIT_AT))
                size = -(-len(ids) // k)
                groups = [ids[i:i + size] for i in range(0, len(ids), size)]
                meta = dict(area=area, cluster=c["topic"], stratum=stratum, detail=c["detail"])
                if len(groups) == 1:
                    sections[base] = {**meta, "parent": under, "n": len(groups[0])}
                    for i in groups[0]: parent_of[i] = base
                else:
                    sections[base] = {**meta, "parent": under, "n": 0}
                    for n, g in enumerate(groups, 1):
                        sid = f"{base}-{n}"
                        sections[sid] = {**meta, "parent": base, "n": len(g)}
                        for i in g: parent_of[i] = sid
    return sections, parent_of


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--plan", action="store_true"); a = ap.parse_args()
    man = json.loads(MANIFEST.read_text())
    on_disk = {}
    for p in CORPUS.rglob("*.md"):
        fm, _ = read(p)
        on_disk[fm.get("id") or p.stem] = p

    sections, parent_of = intended(man, on_disk)
    # Three ways a file can be stale, and the third is the one that hurt: a section written by an
    # earlier, broken run, never recorded in the manifest and named nothing like the current scheme.
    # Nineteen of those survived two rounds of cleanup because every check consulted the manifest,
    # which did not know about them. The file system is the fact here — anything in the corpus that
    # is neither in the manifest nor in the worked example it grew from was left behind.
    seed = {(read(q)[0].get("id") or q.stem)
            for q in (ROOT.parent / "examples" / "back-office" / "regions").rglob("*.md")}
    stale = sorted({i for i in on_disk if i.startswith(SEC) and i not in sections}
                   | {i for i, m in man.items() if m.get("section") and i not in sections}
                   | {i for i in on_disk if i not in man and i not in seed})
    missing = [s for s in sections if s not in on_disk]

    fan = {}
    for s, m in sections.items(): fan[m["parent"]] = fan.get(m["parent"], 0) + 1
    for i, s in parent_of.items(): fan[s] = fan.get(s, 0) + 1
    for i, p in on_disk.items():
        if i in man or i in sections: continue
        fm, _ = read(p)
        if fm.get("parent"): fan[fm["parent"]] = fan.get(fm["parent"], 0) + 1
    over = {k: v for k, v in fan.items() if v > MAX_CHILDREN}

    print(f"  {len(sections)} sections intended · {len(parent_of)} documents beneath them")
    print(f"  on disk: {len(missing)} to write, {len(stale)} stale to remove")
    print(f"  worst fan-out after: {max(fan.values())}   over budget: {over or 'none'}")
    if a.plan:
        for s in sorted(missing)[:5]: print(f"      write   {s}")
        for s in sorted(stale)[:5]: print(f"      remove  {s}")
        return

    for i in stale:
        p = on_disk.get(i)
        if p and p.exists(): p.unlink()
        man.pop(i, None); on_disk.pop(i, None)
    if stale: print(f"  removed {len(stale)} stale section pages")

    if missing:
        sys.path.insert(0, str(ROOT))
        from generate import ask, parse, KINDS
        for area in SPEC:
            want = {s: sections[s] for s in missing if sections[s]["area"] == area and s not in on_disk}
            # One call per area is one answer with nineteen documents in it, and the tail gets
            # truncated. Six at a time: small enough to arrive whole, large enough that a section
            # still knows what its siblings cover.
            todo = sorted(want)
            for i in range(0, len(todo), 6):
                batch = {s: want[s] for s in todo[i:i + 6]}
                taken = sorted({read(q)[0].get("name", "") for q in on_disk.values()})
                listing = "\n".join(
                    f"  {s} — {m['cluster']}: {m['detail'][:120]}"
                    + (f"  (holds {m['n']} pages)" if m["n"] else "  (holds the sub-sections below it)")
                    for s, m in sorted(batch.items()))
                out = parse(ask(
                    f"Write the section pages for the area `{area}`. Each opens a part of the area and "
                    f"points at the detail beneath it — what this part covers, the common case, the one "
                    f"thing that goes wrong. **Do not restate figures that live in the pages below**: a "
                    f"section page says the shape, the pages under it say the numbers.\n\n"
                    f"Use exactly these ids, one document each:\n{listing}\n\n"
                    f"KINDS available: {', '.join(KINDS)}. A section page is usually `topic`.\n\n"
                    f"**Every `name` must be distinct from all of these**, which are already in use:\n"
                    + "\n".join(f"  {t}" for t in taken),
                    max_tokens=9000))
                for d in out:
                    if d["id"] not in batch: print(f"      unexpected id {d['id']}"); continue
                    m = batch[d["id"]]
                    fm = [f"id: {d['id']}", f"name: {json.dumps(d['name'], ensure_ascii=False)}",
                          f"kind: {d['kind'] if d['kind'] in KINDS else 'topic'}",
                          f"one_liner: {json.dumps(d['one_liner'], ensure_ascii=False)}",
                          f"parent: {m['parent']}"]
                    p = CORPUS / area / f"{d['id']}.md"
                    p.write_text("---\n" + "\n".join(fm) + "\n---\n" + d["body"].strip() + "\n", encoding="utf-8")
                    on_disk[d["id"]] = p
                    man[d["id"]] = {"id": d["id"], "area": area, "parent": m["parent"],
                                    "stratum": m["stratum"], "cluster": m["cluster"],
                                    "pair": None, "section": True}
                print(f"      {area}: {sum(1 for s in sections if s in on_disk)}/{len(sections)} sections exist")

    absent = [s for s in sections if s not in on_disk]
    if absent:
        MANIFEST.write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  {len(absent)} sections still missing — nothing re-parented. Run again: {absent[:4]}")
        return

    # A section can exist on disk and not in the manifest: the earlier, non-idempotent version wrote
    # files and saved the manifest at different moments, and a crash between the two left exactly
    # that. Adopt it rather than fail — the file is the fact, the manifest is the record of it.
    for s, m in sections.items():
        if s not in man:
            man[s] = {"id": s, "area": m["area"], "parent": m["parent"], "stratum": m["stratum"],
                      "cluster": m["cluster"], "pair": None, "section": True}
        set_parent(on_disk[s], m["parent"]); man[s]["parent"] = m["parent"]
    for i, s in parent_of.items():
        set_parent(on_disk[i], s); man[i]["parent"] = s
    MANIFEST.write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(sections)} sections and {len(parent_of)} documents re-parented")


if __name__ == "__main__":
    main()
