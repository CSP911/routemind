"""Generated INDEX.md for a service fragment (SPEC-service-fragment §3).

The operator supplies a file and one line describing it; this writes the index. Never hand-maintained —
a hand-kept file list is wrong by the second file, which is why Core generates its node indexes too.
"""
from __future__ import annotations
import json
from .service_store import ServiceStore

FM_ORDER = ["service", "core_revision", "publisher", "game_line", "regions", "updated"]


def write_service_index(store: ServiceStore, svc: dict) -> None:
    fm = []
    for k in FM_ORDER:
        v = svc.get(k)
        if v in (None, "", []): continue
        fm.append(f"{k}: [" + ", ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]" if isinstance(v, list)
                  else f"{k}: {v}")
    files = svc.get("files") or []
    body = "---\n" + "\n".join(fm) + "\n---\n" + (svc.get("one_liner") or "").strip() + "\n\n## Files\n"
    body += "".join(f"- {f['name']} : {f['description']}\n" for f in files) if files else \
            "(none — this service's fragment is still empty)\n"
    (store.root / svc["dir"] / "INDEX.md").write_text(body, encoding="utf-8")


def regenerate(store: ServiceStore) -> list[str]:
    """Rewrite every service index from the directory's actual contents. Returns paths touched."""
    touched = []
    for svc in store.services():
        listed = {f["name"]: f["description"] for f in svc["files"]}
        files = [{"name": n, "description": listed.get(n, "(no description — the owner has to write one line)")}
                 for n in svc["present_files"]]
        if files == svc["files"]: continue
        before = (store.root / svc["dir"] / "INDEX.md").read_text(encoding="utf-8")
        write_service_index(store, {**svc, "files": files})
        if (store.root / svc["dir"] / "INDEX.md").read_text(encoding="utf-8") != before:
            touched.append(f"{svc['dir']}/INDEX.md")
    return touched
