"""Service-fragment store — reads the fragment repo (SPEC-service-fragment §3).

Layout, one directory per service id (the service path is the key, §2):
  <svc>/INDEX.md      generated: frontmatter · one-liner · `## Files`
  <svc>/<file>        operator-authored, free format — this module never parses them
"""
from __future__ import annotations
import os
from pathlib import Path
from .store import Store

SERVICE_RE = __import__("re").compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")   # Pi's SERVICE_RE
CONTENT_SUFFIXES = {".md", ".yaml", ".yml"}                                     # what Pi's source `include` admits


class ServiceStore:
    def __init__(self, root: str | os.PathLike):
        self.root = Path(root)

    def service_dirs(self):
        if not self.root.exists(): return
        for d in sorted(self.root.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and (d / "INDEX.md").exists(): yield d

    def services(self) -> list[dict]:
        out = []
        for d in self.service_dirs():
            idx = Store.parse_index((d / "INDEX.md").read_text(encoding="utf-8"))
            fm = idx["frontmatter"]
            out.append({
                "id": fm.get("service"), "dir": d.name,
                "core_revision": str(fm["core_revision"]) if fm.get("core_revision") is not None else None,
                "publisher": fm.get("publisher"), "game_line": fm.get("game_line"),
                "regions": [str(x) for x in (fm.get("regions") or [])],
                "updated": str(fm["updated"]) if fm.get("updated") is not None else None,   # YAML gives a date object; JSON cannot take one
                "one_liner": idx["one_liner"], "files": idx["files"], "path": str(d.relative_to(self.root)),
                "present_files": sorted(p.name for p in d.iterdir()
                                        if p.is_file() and p.name != "INDEX.md" and p.suffix.lower() in CONTENT_SUFFIXES),
            })
        return out

    def service(self, sid: str) -> dict | None:
        return next((s for s in self.services() if s["id"] == sid), None)

    def file(self, sid: str, name: str) -> str | None:
        s = self.service(sid)
        if not s or name not in [f["name"] for f in s["files"]]: return None   # not listed → does not exist for the API
        p = self.root / s["path"] / name
        return p.read_text(encoding="utf-8") if p.exists() else None
