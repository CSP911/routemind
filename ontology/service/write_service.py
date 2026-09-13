"""Service-fragment writes — the same transaction Core uses (SPEC-service-fragment §5).

  change the working tree → regenerate every INDEX.md → validate → git commit → publish atomically

On validation failure the tree is restored and nothing is published. Atomicity matters more here than
for Core: a half-applied state where the index points at a file that is not there yet would reach Pi
directly, so the publish swaps a whole write-once tree behind one symlink rename.
"""
from __future__ import annotations
from pathlib import Path
from .service_store import ServiceStore, SERVICE_RE, CONTENT_SUFFIXES
from .store import write as store_write
from .derive_service import write_service_index, regenerate
from .validate_service import validate_services
from .write import WriteError, _git, _dirty, _restore, _lock, repo_lock, head, publish

FRONTMATTER_FIELDS = ("core_revision", "publisher", "game_line", "regions", "updated")


def _safe_name(name: str) -> str:
    n = str(name or "").strip()
    if not n or "/" in n or "\\" in n or n.startswith(".") or n == "INDEX.md":
        raise WriteError(400, "file name must be a plain name, not INDEX.md, no path separators")
    if Path(n).suffix.lower() not in CONTENT_SUFFIXES:
        raise WriteError(400, f"file must be one of {sorted(CONTENT_SUFFIXES)} — Pi's source reads only those")
    return n


class ServiceWriter:
    def __init__(self, root: Path, publish_dir: Path | None, core_publish_dir: Path | None):
        self.root, self.publish_dir, self.core_publish_dir = Path(root), publish_dir, core_publish_dir
        self.store = ServiceStore(root)

    # ---- the one write path ----
    def transact(self, message: str, actor: str, mutate) -> dict:
        # Its own repository, so its own lock — see repo_lock in write.py.
        with _lock, repo_lock(self.root):
            if not (self.root / ".git").exists(): raise WriteError(500, "fragment directory is not a git repository")
            if (dirty := _dirty(self.root)):
                raise WriteError(409, "working tree is dirty — someone edited the repository by hand; commit or revert it first",
                                 code="tree_dirty", data={"files": dirty})
            try:
                mutate()
                regenerate(self.store)
                res = validate_services(self.store, self.core_publish_dir)
                if not res["ok"]:
                    raise WriteError(422, "validation failed — nothing was written", res["errors"],
                                     code="validation_failed", data={"n": len(res["errors"])})
                _git(self.root, "add", "-A")
                if not _git(self.root, "status", "--porcelain"): raise WriteError(200, "no change")
                _git(self.root, "-c", f"user.name={actor}", "-c", f"user.email={actor}@iris.local", "commit", "-q", "-m", message)
            except WriteError:
                _restore(self.root); raise
            except Exception as e:
                _restore(self.root); raise WriteError(500, f"{type(e).__name__}: {e}")
            sha = head(self.root)
            if self.publish_dir: publish(self.root, self.publish_dir, sha)
            return {"ok": True, "revision": sha, "message": message, "warnings": res["warnings"], "stats": res["stats"]}

    # ---- services ----
    def create_service(self, body: dict, actor: str) -> dict:
        sid = str(body.get("service") or "").strip()
        if not SERVICE_RE.match(sid): raise WriteError(400, "service id must match Pi's SERVICE_RE")
        if (self.root / sid).exists(): raise WriteError(409, f"service {sid} exists")
        if not body.get("one_liner"): raise WriteError(400, "one_liner is required")
        if not body.get("core_revision"): raise WriteError(400, "core_revision is required — it is what makes references checkable")
        def mutate():
            (self.root / sid).mkdir(parents=True)
            write_service_index(self.store, {"id": sid, "dir": sid, "one_liner": body["one_liner"], "files": [],
                                             **{k: body.get(k) for k in FRONTMATTER_FIELDS}, "service": sid})
        return self.transact(f"fragment create: {sid}", actor, mutate)

    def update_service(self, sid: str, body: dict, actor: str) -> dict:
        svc = self.store.service(sid)
        if not svc: raise WriteError(404, f"no such service fragment: {sid}")
        def mutate():
            merged = {**svc, "service": sid,
                      "one_liner": body.get("one_liner", svc["one_liner"]),
                      **{k: (body[k] if k in body else svc.get(k)) for k in FRONTMATTER_FIELDS}}
            write_service_index(self.store, merged)
        return self.transact(f"fragment update: {sid}", actor, mutate)

    def delete_service(self, sid: str, actor: str) -> dict:
        svc = self.store.service(sid)
        if not svc: raise WriteError(404, f"no such service fragment: {sid}")
        import shutil
        def mutate(): shutil.rmtree(self.root / svc["dir"])
        return self.transact(f"fragment delete: {sid}", actor, mutate)

    # ---- files (the operator channel) ----
    def put_file(self, sid: str, name: str, content: str, description: str, actor: str) -> dict:
        svc = self.store.service(sid)
        if not svc: raise WriteError(404, f"no such service fragment: {sid}")
        name = _safe_name(name)
        if not str(description or "").strip(): raise WriteError(400, "description is required — one line saying what this file holds")
        def mutate():
            store_write(self.root / svc["dir"] / name, content)
            files = [f for f in svc["files"] if f["name"] != name] + [{"name": name, "description": description.strip()}]
            write_service_index(self.store, {**svc, "service": sid, "files": sorted(files, key=lambda f: f["name"])})
        return self.transact(f"fragment file: {sid}/{name}", actor, mutate)

    def delete_file(self, sid: str, name: str, actor: str) -> dict:
        svc = self.store.service(sid)
        if not svc: raise WriteError(404, f"no such service fragment: {sid}")
        name = _safe_name(name)
        p = self.root / svc["dir"] / name
        if not p.exists(): raise WriteError(404, f"no such file: {sid}/{name}")
        def mutate():
            p.unlink()
            write_service_index(self.store, {**svc, "service": sid, "files": [f for f in svc["files"] if f["name"] != name]})
        return self.transact(f"fragment file delete: {sid}/{name}", actor, mutate)

    def publish_head(self) -> str | None:
        if not self.publish_dir: return None
        return publish(self.root, self.publish_dir, head(self.root))
