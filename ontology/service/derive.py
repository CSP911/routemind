"""Derived files — regenerated after every write, never edited by hand.

  regions.json           the area list hop 0 serves, one row per area, from its top representative
"""
from __future__ import annotations
import functools, json, re
from pathlib import Path
import yaml
from .store import Store
from .store import write as store_write

def region_label(d: str) -> str:
    """Area directory → its key (`back-office` → `BACK_OFFICE`), the `id` of its row."""
    return d.replace("-", "_").upper()


def regions_doc(store: Store) -> str:
    """What `regions.json` must contain, given the files — computed, not read.

    Split out of `regenerate` so something other than the writer can ask the question. `regions.json`
    is derived *and committed*, which means it can be committed stale: hand-edit an area's `.md`, push
    without regenerating, and hop 0 goes on advertising the old `title` and the old `use_when` for
    ever. `use_when` is the sentence an agent routes on, so that is a routing table quietly
    disagreeing with the repository it is supposed to be. The validator compares the two now, and it
    needs the answer without touching the tree.
    """
    # No `description` since 2026-10-07. It came from a row in CORE.md that no agent was ever shown —
    # hop 0 prints `use_when` — and creating an area required writing it anyway, a third sentence for
    # the one an agent reads.
    root = store.root
    nodes = store.nodes()
    regs = []
    for r in sorted(d.name for d in (root / "regions").iterdir() if d.is_dir()):
        # SPEC-v2 §1.1 — an area is a namespace. What it is, **its top representative advertises**.
        top = next((n for n in nodes if n["region"] == r and n.get("role") == "representative" and not n.get("parent")), None)
        # `source` is the directory name, as it is. It used to have its hyphens turned into underscores,
        # which gave every hyphenated area two spellings — and the export surface compared a node's
        # area (`back-office`) against the source (`back_office`), so every node of an exported area
        # with a hyphen in its name was a 404 to every peer while the area's own table read fine.
        # Reported by a user 2026-10-07. Readers still accept the old spelling (`dir_of`), because
        # committed tables and other backbones' answers carry it until they are regenerated.
        regs.append({"id": region_label(r), "source": r,
                     "title": (top["name"] if top else r),
                     "use_when": ((top.get("use_when") or "") if top else ""),
                     # Whether this area crosses a link. The line it crosses with is `use_when`
                     # above — there is one sentence (operator, 2026-09-29).
                     "export": bool(top.get("export")) if top else False,
                     "nodes": [n["id"] for n in nodes if n["region"] == r and n.get("status") != "draft"],
                     "representative": (top["id"] if top else None),
                     "fetch": f"/v1/regions/{r}"})
    return json.dumps({"schema": "iris-ontology-regions/v2", "regions": regs}, ensure_ascii=False, indent=1) + "\n"


def regenerate(store: Store) -> list[str]:
    """Rewrite derived files in place. Returns the relative paths touched."""
    touched = []
    p = store.root / "regions.json"; new = regions_doc(store)
    if not p.exists() or p.read_text(encoding="utf-8") != new: store_write(p, new); touched.append("regions.json")
    return touched


# Two lists hang off one field of a node's frontmatter — **is it serialised** (here) and **can the
# API change it** (write.update_node). On 2026-09-09 the two drifted: `use_when`, `parent` and
# `expands_in` were missing from the serialisation list, so writing a single file to a node silently
# dropped them. They come from one place now: a field absent here is not stored, and only a field
# that is here and in EDITABLE can be changed.
NODE_FIELDS = ("holds", "injected_by", "status", "role", "parent", "use_when", "export",
               "export_to", "expands_in", "aliases", "grafted_from")
EDITABLE = ("name", "kind", "one_liner", "holds", "status", "use_when", "export",
            "expands_in", "parent")


# What YAML would read as a line break or refuse outright, inside a double-quoted scalar that
# `json.dumps(ensure_ascii=False)` leaves raw: NEL and the two Unicode separators were folded into a
# space ("nel\x85x" came back "nel x"), and the C1 controls, a BOM and a lone surrogate make the
# whole file unreadable (audit, 2026-11-02).
_UNSAFE = re.compile(r"[\x7f-\x9f\u2028\u2029\ufeff\ufffe\uffff\ud800-\udfff]")


def _quoted(value) -> str:
    """A double-quoted YAML scalar that reads back as exactly `value`. JSON's string syntax is YAML's
    double-quoted one, less what YAML treats as a break."""
    return _UNSAFE.sub(lambda m: f"\\u{ord(m.group()):04x}", json.dumps(str(value), ensure_ascii=False))


def _scalar(value) -> str:
    # A list or a mapping is carried across as one (a hand-written alias scope); JSON is YAML's flow style.
    if isinstance(value, (list, dict)): return json.dumps(value, ensure_ascii=False)
    return _scalar_text(str(value))


@functools.lru_cache(maxsize=8192)
def _scalar_text(value: str) -> str:
    """A field written bare when it reads back as itself, and quoted when it does not.

    `id`, `kind`, `parent` and `injected_by` were written bare. A bare scalar is YAML's to interpret:
    an id of `on` read back as True, `017` as 15, `0x1a` as 26, `2024-01-01` as a date that took the
    write down with a 500; a kind of "rule\\nstatus: draft" wrote a second line and made the node a
    draft; an injected_by of `a: b` did not parse (audit, 2026-11-02). Ids romanised from Korean land on
    these words (온 → on, 노 → no). Bare is kept for everything that survives the round trip, which is
    every ordinary value, so a file the writer re-saves does not change shape under its author."""
    s = str(value)
    if _BARE.fullmatch(s):
        try:
            if yaml.safe_load(f"k: {s}") == {"k": s}: return s
        except yaml.YAMLError: pass
    return _quoted(s)


_BARE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def write_node_index(store: Store, node: dict) -> None:
    """Serialize an entity from its dict: frontmatter, then its own body.

    `region` is not written — the directory the file sits in already says it, and anything derivable
    that is also stored is a second copy free to drift from the first. Children are not written
    either: each declares its own `parent`, so a list and the tree cannot disagree."""
    fm = [f"id: {_scalar(node['id'])}", f"name: {_quoted(node['name'])}",
          f"kind: {_scalar(node['kind'])}", f"one_liner: {_quoted((node.get('one_liner') or '').strip())}"]
    if node.get("holds") == "pointers": fm.append("holds: pointers")
    if node.get("injected_by"): fm.append(f"injected_by: {_scalar(node['injected_by'])}")
    if node.get("status") == "draft": fm.append("status: draft")
    if node.get("role") == "representative": fm.append("role: representative")
    if node.get("parent"): fm.append(f"parent: {_scalar(node['parent'])}")
    # Quoted, like the name and the line: a sentence with a colon in it ("when the question is
    # about the office: plants, keys") was written bare and no file with it could be read back.
    if node.get("use_when"): fm.append(f"use_when: {_quoted(str(node['use_when']).strip())}")
    # Written only when true. `export: no` and no line at all mean the same thing, and a file that
    # says both would be two spellings of one fact.
    if node.get("export"): fm.append("export: yes")
    if node.get("grafted_from"): fm.append(f"grafted_from: {_scalar(node['grafted_from'])}")
    # Two fields from retired features, written back only so a file that has them keeps them across
    # an edit: `grafted_from` (transfer bundles) and `export_to` (audiences of named peers). Nothing
    # reads either since 2026-10-08.
    if node.get("export_to"):
        fm.append("export_to: [" + ", ".join(_scalar(x) for x in sorted(node["export_to"])) + "]")
    if node.get("expands_in"): fm.append(f"expands_in: {_scalar(node['expands_in'])}")
    if node.get("aliases"):
        fm.append("aliases: [" + ", ".join(
            (f'{{name: {_quoted(a["name"])}, scope: {_scalar(a["scope"])}}}' if isinstance(a, dict) else _quoted(a))
            for a in node["aliases"]) + "]")
    if node.get("scope") and node["scope"] != "common":
        fm.append(f"scope: {json.dumps(node['scope'], ensure_ascii=False) if isinstance(node['scope'], list) else _scalar(node['scope'])}")
    if node.get("described_by"): fm.append(f"described_by: {_scalar(node['described_by'])}")
    body = "---\n" + "\n".join(fm) + "\n---\n" + (node.get("body") or "").strip() + "\n"
    store_write(store.root / node["path"], body)


def sync_region_node_lists(store: Store) -> list[str]:
    """SPEC-v2 §1.1 — the area `INDEX.md` is gone; the routing table lists the nodes. The write paths
    still call this, so the name stays and does nothing."""
    return []


