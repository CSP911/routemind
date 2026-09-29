#!/usr/bin/env python3
"""Open an export and put it somewhere a person can decide about it.

    ./transfer/import.py partner.rmx --inspect          what is in it, without writing anything
    ./transfer/import.py partner.rmx --into ./incoming   unpacked as files, for review

**It does not write into an ontology, and that is the design rather than a stage that is missing.**
An export is somebody else's map. Deciding where a subject lives changes the routing table, and the
routing table is the text every search reads before it chooses anything — measured on this design's
own 700-question census, one row of it lay on the path of 39.7% of walks, and the single wrong
answer in all 700 came from one false sentence in such a row. Importing a stranger's areas straight
into a live backbone would be writing the map from a file that arrived in the post.

So this unpacks and shows. What comes out is ordinary Markdown with frontmatter — the same shape the
ontology stores — and a person moves what they want, the way they would move anything else. The same
rule `knowledge_write` follows: a machine writes notes, a person changes the map.

The ids are the hazard worth naming. A foreign `payroll` and a local `payroll` are different
subjects with the same name, and nothing in the file knows that. `--into` writes under one directory
named for the source so nothing lands on top of anything; `--inspect` lists what would collide.

The file format — magic, header, AEAD — is read from `transfer/bundle.py`, the one place that
defines it, so this and whatever wrote the file cannot drift apart.
"""
import argparse, getpass, json, os, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from transfer.bundle import MAGIC, BundleError, header_of, unseal


def write_out(payload: dict, root: pathlib.Path, source: str) -> int:
    """Unpacked as files, under one directory named for where it came from.

    Not merged, not renamed, not placed in areas. Whoever moves a document into an area is deciding
    that this subject lives there, which is a change to the map, and that decision is not one a file
    can carry with it.
    """
    base = root / source
    n = 0
    for node in payload.get("nodes") or []:
        nid = node.get("id")
        if not nid: continue
        fm = {k: node[k] for k in ("id", "name", "kind", "region", "one_liner", "parent")
              if node.get(k)}
        # `use_when_export` is what the sender wrote for an outside reader. It is kept under its own
        # name rather than promoted to `use_when`: the line that routes a local search has to be
        # written by whoever owns the local map.
        outward = node.get("use_when_export") or node.get("use_when")
        if outward: fm["use_when_export"] = outward
        out = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", ""]
        out.append((node.get("body") or "").strip())
        p = base / f"{nid}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
        n += 1
    (base / "_MANIFEST.json").write_text(
        json.dumps({k: v for k, v in payload.items() if k != "nodes"}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--inspect", action="store_true", help="say what is in it and write nothing")
    ap.add_argument("--into", help="directory to unpack into, for review")
    ap.add_argument("--against", help="a data/repo to list id collisions against")
    ap.add_argument("--passphrase-env", default="ROUTEMIND_EXPORT_PASSPHRASE")
    a = ap.parse_args()

    blob = pathlib.Path(a.file).read_bytes()
    try:
        h = header_of(blob)
    except BundleError as e:
        sys.exit(f"  {e}")
    print(f"  from {h.get('source', {}).get('api')} · revision {h.get('source', {}).get('revision')}\n"
          f"  made {h.get('created')} · {h.get('counts', {}).get('regions')} area(s), "
          f"{h.get('counts', {}).get('nodes')} node(s)", file=sys.stderr)
    if a.inspect and not a.into and not a.against:
        print("  (pass --into to unpack, or --against a repo to see id collisions)", file=sys.stderr)

    pw = os.environ.get(a.passphrase_env) or getpass.getpass("  passphrase: ")
    try:
        payload = unseal(blob, pw)
    except BundleError as e:
        sys.exit(f"  {e}")
    src = (payload.get("source", {}).get("api") or "unknown").split("//")[-1].replace(":", "-").replace("/", "-")

    ids = [n["id"] for n in (payload.get("nodes") or []) if n.get("id")]
    for r in (payload.get("regions") or []):
        # The surface hands the outward line over as `use_when`, because from the reader's side
        # that is what it is — the sender's own `use_when` never leaves their backbone.
        line = r.get("use_when") or r.get("use_when_export") or r.get("description") or ""
        print(f"    area  {r.get('source')}  —  {line[:90]}", file=sys.stderr)

    if a.against:
        have = {p.stem for p in pathlib.Path(a.against, "regions").rglob("*.md")}
        clash = sorted(set(ids) & have)
        print(f"\n  {len(clash)} id(s) already exist in {a.against}:", file=sys.stderr)
        for c in clash[:20]: print(f"    {c}", file=sys.stderr)
        if clash:
            print("  These are different subjects with the same name. Nothing was written; renaming "
                  "is a decision about which one owns the id.", file=sys.stderr)

    if a.into:
        n = write_out(payload, pathlib.Path(a.into), src)
        print(f"\n  {n} document(s) → {a.into}/{src}/\n"
              "  Nothing has been added to any ontology. Move what you want into an area yourself; "
              "that is the point at which it becomes part of your map.", file=sys.stderr)
    elif not a.against:
        print("\n  Nothing written. --into <dir> to unpack, --against <repo> to check ids.", file=sys.stderr)


if __name__ == "__main__":
    main()
