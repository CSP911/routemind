"""How long each route has been there, and when the document behind it last moved.

Two different times, and the difference is the whole point. A route laid down in 2023 whose document
was rewritten last week is **fresh**; the same route whose document has not moved in three years is
the one worth asking about. One number cannot say both, so both are kept.

**Read from git, not stored.** Every one of these facts is already in the history — a field carrying
them would be a second copy that drifts, and a wrong date here is worse than none: it is a reason to
trust the wrong row. Nothing to migrate, nothing to keep in sync, and true by construction.

    route_since   the most recent commit that *added* this file
    changed       the most recent commit that touched it at all

`route_since` is the most recent addition rather than the first ever, so a subject deleted and
re-created reads as new — because it is. The question the number answers is "how long has this path
been here unbroken", and an unbroken run restarts when the path does.

One pass over the log per revision, cached on the commit id the store already tracks. Measured on the
shipped repository: 677 commits, 82 documents, 0.34s — fine once, far too slow per request.
"""
from __future__ import annotations

import subprocess
import threading
from pathlib import Path

_CACHE: dict[str, dict] = {}
_LOCK = threading.Lock()
# A repository that has never been committed, or a checkout without git, has no history to read. That
# is not an error and must not be one: a backbone whose ages are unknown still routes correctly, and
# refusing to answer over a missing timestamp would make git a dependency of reading a document.
UNKNOWN: dict = {}


def _log(root: Path, *extra: str) -> list[tuple[str, list[str]]]:
    """(when, paths) per commit, newest first. Empty on any failure, deliberately."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%x00%cI", "--name-only", *extra,
             "--", "regions"],
            capture_output=True, text=True, timeout=30)
    except Exception:
        return []
    if out.returncode != 0: return []
    rows = []
    for chunk in out.stdout.split("\0"):
        lines = [l for l in chunk.splitlines() if l.strip()]
        if not lines: continue
        rows.append((lines[0].strip(), [l for l in lines[1:] if l.endswith(".md")]))
    return rows


def _node_id(path: str) -> str | None:
    """`regions/<area>/<id>.md` → `<id>`. Anything else is not a node and is skipped."""
    parts = path.split("/")
    if len(parts) != 3 or parts[0] != "regions" or not parts[2].endswith(".md"): return None
    return parts[2][:-3]


def of(root, revision: str | None = None) -> dict:
    """`{node_id: {"route_since": iso, "changed": iso}}` for this revision.

    Keyed on the revision so it is computed once per commit rather than once per request. A
    repository with no history answers `{}`, and every caller treats a missing entry as "not known"
    rather than as "new" — a document whose age cannot be read must not look like a fresh one.
    """
    root = Path(root)
    key = revision or "HEAD"
    with _LOCK:
        hit = _CACHE.get(key)
    if hit is not None: return hit

    changed: dict[str, str] = {}
    for when, paths in _log(root):
        for p in paths:
            nid = _node_id(p)
            # Newest first, so the first time a path is seen is its most recent change.
            if nid and nid not in changed: changed[nid] = when
    added: dict[str, str] = {}
    for when, paths in _log(root, "--diff-filter=A"):
        for p in paths:
            nid = _node_id(p)
            if nid and nid not in added: added[nid] = when

    out = {nid: {"route_since": added.get(nid), "changed": changed.get(nid)}
           for nid in set(changed) | set(added)}
    with _LOCK:
        # Only this revision's answer is kept. The history behind a commit does not change, so a
        # stale entry is impossible; holding every revision ever asked for is the leak.
        _CACHE.clear()
        _CACHE[key] = out
    return out
