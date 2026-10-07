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
import argparse, getpass, json, os, pathlib, shutil, sys

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
        # The sender's routing line, kept under a name of its own rather than promoted to
        # `use_when`. There is one sentence now and this is it — but whose table it routes is still
        # a decision, and unpacking for review is the stage before anyone has made it.
        outward = node.get("use_when")
        if outward: fm["use_when_from_source"] = outward
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


SAFE = __import__("re").compile(r"^[a-z0-9][a-z0-9-]*$")


def graft(payload: dict, repo: pathlib.Path, prefix: str) -> tuple[list[str], list[str]]:
    """Write the bundle into a repository, every id under one prefix.

    The prefix is the whole answer to the collision problem, and it is applied to *every* id rather
    than only the ones that clash. A prefix on the clashes alone would mean the same subject is
    called two different things depending on whether the receiving side happened to have that name
    already — so the same export, grafted into two repositories, would come out differently.

    Every reference moves with the ids, or the grafted tree points at the wrong documents: `parent`,
    the region a node belongs to, and `REGION/<id>.md` lines in a pointer node's body. A reference
    this cannot resolve inside the bundle is left alone and reported, because a half-rewritten
    pointer is worse than one that is obviously foreign.

    Returns (what was written, what could not be rewritten).
    """
    rename = {n["id"]: f"{prefix}-{n['id']}" for n in payload.get("nodes") or [] if n.get("id")}
    areas = {str(r.get("source")).replace("_", "-") for r in (payload.get("regions") or []) if r.get("source")}
    written, unresolved = [], []

    # A body line that addresses another area's document. None exist in the shipped corpus, so this
    # path is written from the validator's rule rather than from an example — which is exactly why
    # anything it cannot place is reported instead of guessed at.
    ref = __import__("re").compile(r"\b([A-Z_]+)/([a-z0-9-]+)\.md\b")

    def rewrite(body: str, where: str) -> str:
        def one(m):
            area, nid = m.group(1), m.group(2)
            if nid in rename:
                return f"{prefix.upper().replace('-', '_')}_{area}/{rename[nid]}.md"
            unresolved.append(f"{where}: {m.group(0)} — not in this bundle")
            return m.group(0)
        return ref.sub(one, body or "")

    for r in payload.get("regions") or []:
        # The directory, in either spelling: bundles made before 2026-10-07 carry underscores.
        src = str(r.get("source") or "").replace("_", "-")
        if not src: continue
        newsrc = f"{prefix}-{src}"
        d = repo / "regions" / newsrc
        d.mkdir(parents=True, exist_ok=True)
        for node in payload.get("nodes") or []:
            nid = node.get("id")
            if not nid or (node.get("region") or src) != src: continue
            # The name is suffixed as well as the id, because this repository requires both to be
            # unique: `validate` collects nodes by normalised name and errors on any name held by
            # more than one — identical spellings included, despite the message calling them
            # "spelling variants". Grafting a corpus that shares an ancestor produced 19 of them.
            # The marker goes after the name, not before, because the name is what a person scans.
            fm = {"id": rename[nid], "name": f"{node.get('name') or nid} ({prefix})"}
            for k in ("kind", "one_liner", "role", "status", "scope", "order"):
                if node.get(k): fm[k] = node[k]
            if node.get("parent"):
                fm["parent"] = rename.get(node["parent"], node["parent"])
                if node["parent"] not in rename:
                    unresolved.append(f"{nid}: parent {node['parent']} is not in this bundle")
            # The representative carries the area's routing line. The bundle hands over
            # The sender's own routing line becomes this repository's. Since 2026-09-29 there is one
            # sentence, so this is the line they route on rather than a summary written for
            # outsiders — but it is still written about their map, and the area it now routes is
            # yours. It is the thing to go and edit first; leaving it blank would hide the area.
            if (node.get("role") or "") == "representative" or nid == r.get("representative"):
                fm["role"] = "representative"
                line = (r.get("use_when") or "").strip()
                if line: fm["use_when"] = line
                # Where it came from, recorded rather than inferred. The prefix is a naming
                # convention — somebody renames, or uses `beta-` for an area of their own, and the
                # convention says the wrong thing with nothing to check it against. A reader
                # choosing between this row and one written here is choosing on whose answer it is,
                # so that fact belongs in the file.
                fm["grafted_from"] = str((payload.get("source") or {}).get("api") or "elsewhere")
            out = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", ""]
            out.append(rewrite((node.get("body") or "").strip(), nid))
            (d / f"{rename[nid]}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
            written.append(f"regions/{newsrc}/{rename[nid]}.md")


    # The links across the tree, with both ends renamed. Appended rather than merged: an edge this
    # brought is the sender's statement about their own documents, and it says nothing about anyone
    # else's. An edge naming something outside the bundle is dropped and reported — it can only mean
    # the file is older than this rule, and inventing the far end would be inventing a connection.
    edges = payload.get("edges") or []
    if edges:
        path = repo / "edges.yaml"
        keep, lost = [], 0
        for e in edges:
            f, t = e.get("from"), e.get("to")
            if f in rename and t in rename:
                keep.append({"from": rename[f], "rel": e.get("rel"), "to": rename[t]})
            else:
                lost += 1
        if lost: unresolved.append(f"{lost} edge(s) named a document not in this bundle, and were dropped")
        if keep:
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            if text and not text.endswith("\n"): text += "\n"
            text += f"\n# Grafted from {prefix}.\n"
            for e in keep:
                text += f"- from: {e['from']}\n  rel: {e['rel']}\n  to: {e['to']}\n"
            path.write_text(text, encoding="utf-8")
            written.append(f"edges.yaml (+{len(keep)})")
    return written, unresolved


def ungraft(repo: pathlib.Path, prefix: str) -> tuple[int, int]:
    """Take a graft back out: its documents, its area, and its links.

    The counterpart to `--graft`, and it exists because the graft was not reversible. Deleting the
    directory left every edge it had appended pointing at documents that were gone — four of them on
    the first repository this was tried against — and the repository stopped validating, which stops
    every write. A feature that cannot be undone is one people are right to be wary of using.

    Only what carries the prefix, so a graft never takes anything of yours with it. Returns
    (documents, links) removed.
    """
    gone, dropped = 0, 0
    for d in sorted((repo / "regions").iterdir()):
        if not d.is_dir() or not d.name.startswith(prefix + "-"): continue
        gone += len(list(d.glob("*.md")))
        shutil.rmtree(d)
    path = repo / "edges.yaml"
    if path.exists():
        keep, text = [], path.read_text(encoding="utf-8")
        # Line-wise on the flow this writes — three lines per edge, `from:` first. Read as YAML and
        # written back it would be reformatted whole, and edges.yaml is a file people edit.
        block, drop = [], False
        for line in text.splitlines(True):
            if line.startswith("- from:"):
                if block and not drop: keep.extend(block)
                elif block: dropped += 1
                block, drop = [line], f" {prefix}-" in line
            elif block:
                block.append(line)
                if line.strip().startswith("to:") and f" {prefix}-" in line: drop = True
            else:
                keep.append(line)
        if block and not drop: keep.extend(block)
        elif block: dropped += 1
        # The comment the graft left behind, once nothing under it remains.
        out = "".join(keep).replace(f"\n# Grafted from {prefix}.\n", "\n")
        path.write_text(out.rstrip("\n") + "\n", encoding="utf-8")
    return gone, dropped


def writer_for(repo: pathlib.Path):
    """The service's own `Writer`, or None with the reason.

    A graft is a write into somebody's ontology, and there is one way writes are made here:
    `Writer.transact` — refuse a dirty tree, mutate, regenerate, validate, **roll back on any
    failure**, commit. This used to do its own writing and its own regenerate, which is how it ended
    up with no rollback (files on disk after a failed validate, and "it is a git repository" offered
    as the undo), no commit (a dirty tree, in which every later API write is refused), and an edge
    list it appended to and could not take back — while `delete_region`, going through the writer,
    had cleaned edges correctly from the start.

    Operator, 2026-09-30: the same path. So when the service cannot be imported this does not fall
    back to the old way — a second discipline is the thing that produced the bugs. It says where to
    run instead.
    """
    root = pathlib.Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "ontology"))
    try:
        from service.write import Writer
        return Writer(repo), None
    except Exception as e:
        return None, (f"this python cannot import the service ({e}).\n"
                      f"  A graft is an ordinary write and goes through the same transaction as any "
                      f"other, which needs the service. Run it in the ontology container:\n"
                      f"    docker compose cp {repo} ontology:/tmp/graft-target   # if it is not already mounted\n"
                      f"    docker compose exec ontology python3 /app/transfer/import.py …\n"
                      f"  or from a checkout whose python has pyyaml.")
    return written, unresolved


def _said(e: Exception) -> str:
    """A WriteError's own sentence, which is the repository explaining itself, or the exception.

    `transact` refuses a dirty tree and refuses a graft that would not validate, and both come back
    as a `WriteError` carrying the sentence a person needs. Printing `WriteError(409, ...)` instead
    would be this file paraphrasing an answer it did not write.
    """
    detail = getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
    rows = getattr(e, "details", None) or []
    return str(detail) + ("\n" + "\n".join(f"    · {r}" for r in rows[:8]) if rows else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", nargs="?", help="the .rmx to open; not needed with --ungraft")
    ap.add_argument("--inspect", action="store_true", help="say what is in it and write nothing")
    ap.add_argument("--into", help="directory to unpack into, for review")
    ap.add_argument("--against", help="a data/repo to list id collisions against")
    ap.add_argument("--graft", metavar="REPO",
                    help="write the bundle into this repository, every id under --prefix")
    ap.add_argument("--prefix", help="the prefix every grafted id takes; defaults to the source host")
    ap.add_argument("--ungraft", metavar="REPO",
                    help="remove a graft from this repository — its documents, its area and its "
                         "links. Needs --prefix, and touches nothing else")
    ap.add_argument("--passphrase-env", default="ROUTEMIND_EXPORT_PASSPHRASE")
    ap.add_argument("--actor", default=os.environ.get("KNOWLEDGE_ACTOR") or "graft",
                    help="the name on the commit this makes, like any other write")
    a = ap.parse_args()

    # Before the file is even read: removing a graft needs the prefix and the repository, not the
    # bundle it came from — which may be long gone, and requiring it would make the undo depend on
    # keeping a copy of the thing you are undoing.
    if a.ungraft:
        repo = pathlib.Path(a.ungraft)
        if not (repo / "regions.json").is_file():
            sys.exit(f"  {a.ungraft} is not a RouteMind repository — no regions.json in it")
        if not a.prefix or not SAFE.match(a.prefix):
            sys.exit("  --ungraft needs --prefix, in ascii kebab-case — it is what says which graft")
        writer, why = writer_for(repo)
        if not writer: sys.exit(f"  {why}")
        counted = {}
        try:
            res = writer.transact(f"ungraft: remove everything under `{a.prefix}-`",
                                  a.actor, lambda: counted.update(
                                      zip(("gone", "dropped"), ungraft(repo, a.prefix))))
        except Exception as e:
            sys.exit(f"  {_said(e)}")
        if not counted.get("gone"):
            sys.exit(f"  nothing under `{a.prefix}-` in {a.ungraft}. Nothing was removed.")
        print(f"  {counted['gone']} document(s) and {counted['dropped']} link(s) removed, "
              f"validated, and committed as {str(res.get('revision') or '')[:8]}.", file=sys.stderr)
        return

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
        line = r.get("use_when") or r.get("description") or ""
        print(f"    area  {r.get('source')}  —  {line[:90]}", file=sys.stderr)

    if a.against:
        have = {p.stem for p in pathlib.Path(a.against, "regions").rglob("*.md")}
        clash = sorted(set(ids) & have)
        print(f"\n  {len(clash)} id(s) already exist in {a.against}:", file=sys.stderr)
        for c in clash[:20]: print(f"    {c}", file=sys.stderr)
        if clash:
            print("  These are different subjects with the same name. Nothing was written; renaming "
                  "is a decision about which one owns the id.", file=sys.stderr)

    if a.graft:
        repo = pathlib.Path(a.graft)
        if not (repo / "regions.json").is_file():
            sys.exit(f"  {a.graft} is not a RouteMind repository — no regions.json in it")
        prefix = (a.prefix or src.split("-")[0] or "incoming").lower()
        if not SAFE.match(prefix):
            sys.exit(f"  --prefix must be ascii kebab-case, got {prefix!r}")

        have = {p.stem for p in (repo / "regions").rglob("*.md")}
        still = sorted({f"{prefix}-{i}" for i in ids} & have)
        if still:
            # The prefix is supposed to make this impossible. If it has not, grafting anyway would
            # overwrite documents that are already somebody's, so it stops here rather than deciding.
            sys.exit(f"  {len(still)} id(s) would still collide under `{prefix}-`: "
                     + ", ".join(still[:5]) + "\n  Pick another --prefix.")

        writer, why = writer_for(repo)
        if not writer: sys.exit(f"  {why}")
        held = {}
        try:
            # One transaction, the same one every other write here uses: a dirty tree is refused up
            # front, and anything that fails after this point puts the repository back as it was
            # rather than leaving half a graft on disk.
            res = writer.transact(f"graft: {len(ids)} document(s) from {src} under `{prefix}-`",
                                  a.actor, lambda: held.update(
                                      zip(("written", "unresolved"), graft(payload, repo, prefix))))
        except Exception as e:
            sys.exit(f"  {_said(e)}\n  Nothing was written — the repository is as it was.")
        written, unresolved = held.get("written") or [], held.get("unresolved") or []
        docs = sum(1 for w in written if w.endswith(".md"))
        # A transaction, so there is no half-done state left to describe. The two paragraphs that
        # used to be here — one for "the index was not rebuilt", one for "this was not validated" —
        # were both about states `transact` cannot leave behind: it regenerates, validates, and puts
        # the repository back on any failure before this line is reached.
        print(f"\n  {docs} document(s) written under `{prefix}-`, validated, and committed as "
              f"{str(res.get('revision') or '')[:8]}.\n"
              f"  To take it back out:  ./transfer/import.py --ungraft {a.graft} --prefix {prefix}",
              file=sys.stderr)
        for u in unresolved[:10]:
            print(f"    unresolved reference — {u}", file=sys.stderr)

        print("\n  What the graft could not bring:\n"
              "    · Names for kinds and relations. Every document has a kind, and every link has a\n"
              "      relation name; both belong to the sender's vocabulary. If yours has never heard\n"
              "      of one, validate says which — nothing here writes into your vocab.yaml.\n"
              "\n  And the one thing to look at first: the sender's outward line is now this area's\n"
              "  routing line in your table. It was written to introduce the area to an outsider,\n"
              "  not to route your people's searches. One sentence, and it is the one that decides\n"
              "  where a search goes.", file=sys.stderr)
    elif a.into:
        n = write_out(payload, pathlib.Path(a.into), src)
        print(f"\n  {n} document(s) → {a.into}/{src}/\n"
              "  Nothing has been added to any ontology. Move what you want into an area yourself; "
              "that is the point at which it becomes part of your map.", file=sys.stderr)
    elif not a.against:
        print("\n  Nothing written. --into <dir> to unpack, --graft <repo> to write it in, "
              "--against <repo> to check ids.", file=sys.stderr)


if __name__ == "__main__":
    main()
