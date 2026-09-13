"""Derived files — regenerated after every write, never edited by hand.

  regions/<r>/edges.md   the Region's edge view (Pi's Region sources carry relation knowledge through this)
  regions.json           catalog descriptors (Pi reads these instead of code-embedded ones)
"""
from __future__ import annotations
import json, re
from pathlib import Path
from .store import Store

def region_label(d: str) -> str:
    """Area directory → the key in the CORE.md table. This used to be a hard-coded list; every entry
    in it came out of this rule anyway, and leaving it meant editing code to add an area."""
    return d.replace("-", "_").upper()
VIEW_NOTE = "- edges.md : relations this area's nodes take part in (generated — edges.yaml is the source)"


def regenerate(store: Store) -> list[str]:
    """Rewrite derived files in place. Returns the relative paths touched."""
    root, touched = store.root, []
    nodes = store.nodes(); edges = store.edges()
    region_of = {n["id"]: n["region"] for n in nodes}
    name_of = {n["id"]: n["name"] for n in nodes}
    templates = {(r["id"] if isinstance(r, dict) else r): (r.get("template") if isinstance(r, dict) else None) for g in store.vocab().get("relations", []) for r in g["rels"]}
    # edges.md retired (2026-09-09). A relation view was generated per area and **nothing read it** —
    # agents use the API, the map draws the graph. edges.yaml is the source and `/v1/edges` and
    # `/v1/graph` serve it. What was left was code that wrote the file and a validator that warned
    # when it was missing.
    # ---- regions.json ----
    core = store.core(); core_rows = {m.group(1): m.group(2).strip() for m in re.finditer(r"^\| `([A-Z_]+)` \| (.+?) \|$", core, re.M)}
    regs = []
    for r in sorted(d.name for d in (root / "regions").iterdir() if d.is_dir()):
        # SPEC-v2 §1.1 — an area is a namespace. What it is, **its top representative advertises**.
        top = next((n for n in nodes if n["region"] == r and n.get("role") == "representative" and not n.get("parent")), None)
        regs.append({"id": region_label(r), "source": r.replace("-", "_"),
                     "title": (top["name"] if top else r), "description": core_rows.get(region_label(r), ""),
                     "use_when": ((top.get("use_when") or "") if top else ""),
                     # Empty is not the same as absent here: "" means this area is not exported.
                     "use_when_export": ((top.get("use_when_export") or "") if top else ""),
                     "export_to": ((top.get("export_to") or []) if top else []),
                     "use_when_export_for": ((top.get("use_when_export_for") or {}) if top else {}),
                     "nodes": [n["id"] for n in nodes if n["region"] == r and n.get("status") != "draft"],
                     "representative": (top["id"] if top else None),
                     "fetch": f"/v1/regions/{r}"})
    p = root / "regions.json"; new = json.dumps({"schema": "iris-ontology-regions/v2", "regions": regs}, ensure_ascii=False, indent=1) + "\n"
    if not p.exists() or p.read_text(encoding="utf-8") != new: p.write_text(new, encoding="utf-8"); touched.append("regions.json")
    return touched


# Two lists hang off one field of a node's frontmatter — **is it serialised** (here) and **can the
# API change it** (write.update_node). On 2026-09-09 the two drifted: `use_when`, `parent` and
# `expands_in` were missing from the serialisation list, so writing a single file to a node silently
# dropped them. They come from one place now: a field absent here is not stored, and only a field
# that is here and in EDITABLE can be changed.
NODE_FIELDS = ("holds", "injected_by", "status", "role", "parent", "use_when", "use_when_export",
               "export_to", "use_when_export_for", "expands_in", "aliases")
EDITABLE = ("name", "kind", "one_liner", "aliases", "holds", "status", "use_when", "use_when_export",
            "export_to", "use_when_export_for", "expands_in", "parent")


def write_node_index(store: Store, node: dict) -> None:
    """Serialize an entity from its dict: frontmatter, then its own body.

    `region` is not written — the directory the file sits in already says it, and anything derivable
    that is also stored is a second copy free to drift from the first. Children are not written
    either: each declares its own `parent`, so a list and the tree cannot disagree."""
    fm = [f"id: {node['id']}", f"name: {json.dumps(node['name'], ensure_ascii=False)}",
          f"kind: {node['kind']}", f"one_liner: {json.dumps((node.get('one_liner') or '').strip(), ensure_ascii=False)}"]
    if node.get("holds") == "pointers": fm.append("holds: pointers")
    if node.get("injected_by"): fm.append(f"injected_by: {node['injected_by']}")
    if node.get("status") == "draft": fm.append("status: draft")
    if node.get("role") == "representative": fm.append("role: representative")
    if node.get("parent"): fm.append(f"parent: {node['parent']}")
    if node.get("use_when"): fm.append(f"use_when: {node['use_when']}")
    if node.get("use_when_export"): fm.append(f"use_when_export: {node['use_when_export']}")
    # Who may see it, when that is not everybody. A list, written flow-style so the file stays one
    # frontmatter line per fact. Absent is the common case and means the area crosses to every peer
    # it is exported to at all — the audience narrows what `use_when_export` opened, and can never
    # open anything on its own.
    if node.get("export_to"):
        fm.append("export_to: [" + ", ".join(sorted(node["export_to"])) + "]")
    # One line per fact stays one line: a flow mapping, values JSON-quoted so a sentence with a colon,
    # a brace or a `·` in it cannot end the mapping early. Only for the peers that get something other
    # than the line above — a map that repeated the default for everybody would be two places to
    # change it and one of them would fall behind.
    if node.get("use_when_export_for"):
        fm.append("use_when_export_for: {" + ", ".join(
            f"{k}: {json.dumps(v, ensure_ascii=False)}"
            for k, v in sorted(node["use_when_export_for"].items())) + "}")
    if node.get("expands_in"): fm.append(f"expands_in: {node['expands_in']}")
    if node.get("aliases"):
        fm.append("aliases: [" + ", ".join(
            (f'{{name: {json.dumps(a["name"], ensure_ascii=False)}, scope: {a["scope"]}}}' if isinstance(a, dict) else json.dumps(a, ensure_ascii=False))
            for a in node["aliases"]) + "]")
    if node.get("scope") and node["scope"] != "common":
        fm.append(f"scope: {json.dumps(node['scope'], ensure_ascii=False) if isinstance(node['scope'], list) else node['scope']}")
    if node.get("described_by"): fm.append(f"described_by: {node['described_by']}")
    body = "---\n" + "\n".join(fm) + "\n---\n" + (node.get("body") or "").strip() + "\n"
    (store.root / node["path"]).write_text(body, encoding="utf-8")


def sync_region_node_lists(store: Store) -> list[str]:
    """SPEC-v2 §1.1 — the area `INDEX.md` is gone; the routing table lists the nodes. The write paths
    still call this, so the name stays and does nothing."""
    return []


