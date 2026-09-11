"""Service-fragment validator — SPEC-service-fragment §6, as code.

validate_services(store, core_publish_dir) -> {"ok", "errors", "warnings", "stats"}
Every write through the API must pass this before it is committed.

Core references are Region+file paths (§4), never symbolic ids: a fragment that says
"SVN/sync-check.md" is checked against the published Core tree at the revision the fragment
declares. That is the whole resolution mechanism — no registry, no resolver.
"""
from __future__ import annotations
import re
from pathlib import Path
from .service_store import ServiceStore, SERVICE_RE

# Region label → published directory. Same six labels Pi routes by.
REGION_DIR = {"SVN": "svn", "ORCHESTRATION": "orchestration", "UPDATE_SYSTEM": "update-system",
              "CDN": "cdn", "CHANNELS": "channels", "GAME_SERVER": "game-server", "LEARNED": "learned"}
REF_RE = re.compile(r"\b(" + "|".join(REGION_DIR) + r")/([A-Za-z0-9][A-Za-z0-9._/-]*\.md)\b")
# Structure belongs to Core (§1) — a fragment that redefines it has crossed the line.
STRUCTURE_KEYS = re.compile(r"^\s*(nodes|edges|kinds|vocab|relations)\s*:", re.M)
# §4 — the symbolic id namespace was never built; a leftover `proc_*`/`ref_*` value points at nothing
# and REF_RE cannot see it, so it would pass silently. Catch it explicitly.
SYMBOLIC_RE = re.compile(r"^\s*(?:-\s*)?(?:[a-z_]+):\s*(proc_[a-z0-9_]+|ref_[a-z0-9_]+)\s*(?:#.*)?$", re.M)


def _core_tree(core_publish_dir: Path | None, revision: str | None) -> Path | None:
    """The published Core checkout a fragment pins to. Full or abbreviated sha; `current` is the last resort,
    because a short sha must keep resolving after `current` has moved on."""
    if not core_publish_dir or not revision: return None
    exact = core_publish_dir / revision
    if exact.is_dir() and (exact / "regions").is_dir(): return exact
    hits = sorted(d for d in core_publish_dir.glob(f"{revision}*") if d.is_dir() and not d.is_symlink() and (d / "regions").is_dir())
    if len(hits) == 1: return hits[0]
    if len(hits) > 1: return None                                  # ambiguous abbreviation — refuse rather than guess
    cur = core_publish_dir / "current"
    if cur.exists() and (cur / "regions").is_dir():
        rev = (cur / "REVISION").read_text(encoding="utf-8").strip() if (cur / "REVISION").exists() else ""
        if rev.startswith(revision): return cur
    return None


def resolve_ref(tree: Path, label: str, rest: str) -> bool:
    """A reference resolves if it names a Region doc, a node file, or a core-node file."""
    r = REGION_DIR[label]
    return any((tree / c).exists() for c in (f"regions/{r}/{rest}", f"regions/{r}/nodes/{rest}", f"core-nodes/{rest}"))


def validate_services(store: ServiceStore, core_publish_dir: Path | None = None) -> dict:
    errors, warnings, refs_checked = [], [], 0
    services = store.services()
    seen = {}
    for s in services:
        sid, d = s["id"], s["dir"]
        # 1 · 7 — identity
        if not sid: errors.append(f"service {d}: `service` frontmatter missing"); continue
        if sid != d: errors.append(f"service {d}: `service` {sid!r} ≠ directory name {d!r}")
        if not SERVICE_RE.match(sid): errors.append(f"service {sid}: id does not match Pi's SERVICE_RE")
        if sid in seen: errors.append(f"service id declared twice: {sid}")
        seen[sid] = d
        # 6 — one-liner
        if not s["one_liner"]: errors.append(f"service {sid}: one-liner (first paragraph) missing")
        # 3 · 4 — the index and the directory agree, both ways
        listed = [f["name"] for f in s["files"]]
        for f in listed:
            if f not in s["present_files"]: errors.append(f"service {sid}: `## Files` lists {f} but it is not in the directory")
        for f in s["present_files"]:
            if f not in listed: warnings.append(f"service {sid}: {f} is in the directory but not in `## Files` — the API ignores it")
        for f in s["files"]:
            if not f["description"].strip() or f["description"].startswith("(no description"):
                warnings.append(f"service {sid}: {f['name']} has no one-line description — the agent cannot tell what it holds")
        # 2 · 5 — the Core binding and every reference into it
        rev = s["core_revision"]
        if not rev:
            errors.append(f"service {sid}: `core_revision` missing — references into Core cannot be checked")
            tree = None
        else:
            tree = _core_tree(core_publish_dir, str(rev))
            if core_publish_dir and tree is None:
                # The pinned tree is gone (pruned before publish() learned to keep pins). References are then
                # checked against `current`: if they all resolve the fragment is sound *now* and only needs
                # re-pinning — a warning, not a block. If any fails, that is an error below as usual.
                cur = core_publish_dir / "current"
                if cur.exists() and (cur / "regions").is_dir():
                    tree = cur
                    cur_rev = (cur / "REVISION").read_text(encoding="utf-8").strip() if (cur / "REVISION").exists() else "?"
                    warnings.append(f"service {sid}: core_revision {rev} is no longer published — validated against current {cur_rev[:12]}; re-pin")
                else:
                    errors.append(f"service {sid}: core_revision {rev} is not a published Core revision and no current tree exists")
        body = "".join((store.root / d / n).read_text(encoding="utf-8", errors="replace") for n in s["present_files"])
        for label, rest in REF_RE.findall(body):
            refs_checked += 1
            if tree is not None and not resolve_ref(tree, label, rest):
                errors.append(f"service {sid}: reference {label}/{rest} does not exist in Core {rev}")
        # 9 — no symbolic Core references
        for sym in sorted(set(SYMBOLIC_RE.findall(body))):
            errors.append(f"service {sid}: symbolic reference {sym!r} — Core references are Region+file paths "
                          f'(e.g. "SVN/sync-check.md"), there is no id namespace')
        # 8 — a fragment states decisions, not structure
        if STRUCTURE_KEYS.search(body):
            warnings.append(f"service {sid}: a file declares nodes/edges/kinds — structure belongs to Core, not to a fragment")
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "stats": {"services": len(services), "files": sum(len(s["present_files"]) for s in services),
                      "refs_checked": refs_checked}}
