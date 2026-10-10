"""Writes — every mutation is: change the repo working tree → regenerate derived files → validate → git commit.
On validation failure the working tree is restored and nothing is committed.

There is no publish step (retired 2026-10-07). A checkout of every commit was copied out for an agent
runtime that mounted it read-only; agents here read the repository through the API, so the copy had
no reader, and the screen's "agents are reading an older tree" warning built on it was not true.
"""
from __future__ import annotations
import contextlib, os, re, shutil, subprocess, threading, time
from pathlib import Path
import yaml
from .store import Store, FM_RE
from .store import file_lock
from .validate import validate, ID_RE, NAME_MAX, name_too_long
from .derive import regenerate, write_node_index, sync_region_node_lists, EDITABLE
from .romanize import romanize

# What a document may declare about itself, and what a write must therefore carry across rather
# than replace. `scope` is load-bearing: the validator refuses a `common` file that states a
# service's facts, so dropping it turns a refusal into a silent pass.
CONTENT_DECLARED = ("scope", "described_by")

_lock = threading.Lock()

try: import fcntl
except ImportError: fcntl = None                # not POSIX; the containers are, so this only relaxes checks run elsewhere

REPO_LOCK_WAIT = float(os.environ.get("ONTOLOGY_LOCK_WAIT") or 20.0)


@contextlib.contextmanager
def repo_lock(root: Path, wait: float = REPO_LOCK_WAIT):
    """One writer per data directory, across processes.

    `_lock` above is a threading lock, so it holds only inside one process — and the whole
    transaction below is a sequence of git commands on a shared working tree. Two processes on one
    data directory (`--scale ontology=2`, a second install pointed at the same mount, a stale
    container left behind by a rebuild) tear each other apart, and none of the damage looks like a
    race. Measured with twelve concurrent creates split across two processes:

      * eight were refused with "someone edited the repository by hand" — nobody had. The dirty-tree
        guard cannot tell another writer's half-finished transaction from a person's hand edit, so it
        sends the operator to `git status` looking for something that is not there.
      * two returned 500 from git's own index.lock.
      * two callers were told their write failed while it was committed anyway: `git add -A` stages
        the whole tree, so one process committed the other's files under its own message.
      * the run ended with the tree dirty and a file staged but never committed — a state in which
        *every* subsequent write is refused until a human runs git by hand. The service wedges itself.

    The worst of those is `_restore`: `git checkout -- . && git clean -fdq` on a failure throws away
    whatever is uncommitted, which includes the other process's in-flight write.

    The lock file lives in `.git/`, which is never part of the tree — nothing to commit, nothing to
    add to .gitignore, and no way for the lock itself to make the working tree dirty.

    It waits rather than refusing, because the thing on the other side is a transaction and those are
    short. But it waits with a bound: a writer wedged for good must not turn every later request into
    a hung connection. What comes back then says a process is holding it, which is a different thing
    to go and look at than a hand edit.

    Readers take this same lock **shared** (`Store.snapshot`), so a read never lands in the middle of
    a transaction. The primitive lives in store.py because both sides need it and write.py already
    imports store."""
    def _held():
        raise WriteError(503, f"another process is writing to {root} and has held it for more than "
                              f"{wait:g}s — one writer per data directory. If nothing else should be "
                              f"running, look for a second ontology on this mount.")
    with file_lock(root, exclusive=True, wait=wait, on_timeout=_held):
        yield


def name_from_file(stem: str) -> str:
    """A name for an entity created as a file: the file name itself.

    It used to be the description cut at 60 characters, which put a sentence ending mid-phrase on
    the map tile — "Courier SLA: delivery times for standard/express parcels and". **A name is an
    identity, not a summary.** The summary already exists and is carried whole as `one_liner`,
    directly under the name, so a truncated second copy of it gains nothing and loses the ending.

    It is returned as written, not title-cased. A file name is lowercase by rule, so there is no
    capitalisation left to recover and any would be invented: `courier-sla` becomes `Courier Sla`,
    which quietly unmakes an acronym the author wrote. The person can name it properly whenever they
    like — `name` is editable, and this is a starting value, not a verdict."""
    return stem


def slug_id(name: str) -> str | None:
    """The id a name gives on its own, or None when the name does not give one.

    It refuses rather than guesses, and that has not changed. **A partly-transliterated name is the
    trap**: `Ürün` reduced by dropping what was not understood gives `r-n`, which is not
    wrong-looking enough for anyone to catch, and an id cannot be renamed.

    What has changed is how much can be understood. It used to be "ASCII letters only", which meant a
    team writing in Korean, Japanese or Turkish typed an id by hand for every entity while an English
    team typed none — seventy-nine of them in the shipped example, and a different product depending
    on the language you work in. `romanize` handles what is mechanical (Latin with marks, hangul,
    kana) and refuses the rest (han characters, which need a dictionary of readings). The all-or-
    nothing rule is inside it: one unreadable letter and the whole name gives nothing.

    Punctuation and spacing are separators; they are not letters and do not disqualify a name."""
    raw = (name or "").strip()
    latin = romanize(raw)
    if latin is None: return None
    out = re.sub(r"[^a-z0-9]+", "-", latin.lower()).strip("-")[:48].strip("-")
    return out if out and ID_RE.match(out) else None


class WriteError(Exception):
    """A refusal, with a reason. `code` and `data` make that reason readable in another language.

    The message stays the whole sentence in English and stays the thing that is sent: it is what an
    agent gets, what a `curl` gets, and what the screen falls back to for anything it does not
    recognise. `code` is a stable name for *which* refusal this is, and `data` the values inside it.

    They are separate because half these sentences interpolate — `node {nid} exists` — so a code alone
    would leave the screen unable to say which node. And a translation must be able to put the value
    somewhere else in the sentence, which slicing the English apart would never allow.

    Only the refusals a person actually meets carry one. The rest are for agents and for `curl`, which
    read English, and inventing a code for each of the seventy-seven would be a dictionary nobody
    reads. check/i18n-check.mjs holds the two halves together: a code emitted here with no string on
    the screen is an error that stays English forever, and it fails on that.
    """

    def __init__(self, status: int, message: str, details=None, *, code: str | None = None, data=None):
        super().__init__(message)
        self.status, self.details = status, details or []
        self.code, self.data = code, data or {}


def _git(root: Path, *args, check=True) -> str:
    r = subprocess.run(["git", "-c", "safe.directory=*", "-C", str(root), *args], capture_output=True, text=True)   # bind-mounted repo, arbitrary uid
    if check and r.returncode != 0: raise WriteError(500, f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def head(root: Path) -> str | None:
    """HEAD's commit. Read from the files git keeps it in when they are plain — HEAD naming a branch,
    the branch a loose ref or a line in packed-refs — because this is asked once per row of a table,
    and a `git rev-parse` per row was a second of a 200-row table (2026-10-10). Anything unusual (a
    detached HEAD is fine; a worktree or an odd ref is not) goes to git itself."""
    try:
        g = Path(root) / ".git"
        ref = (g / "HEAD").read_text(encoding="utf-8").strip()
        if not ref.startswith("ref: "):
            return ref if len(ref) == 40 else _git(root, "rev-parse", "HEAD")
        name = ref[5:].strip()
        loose = g / name
        if loose.exists(): return loose.read_text(encoding="utf-8").strip()
        packed = g / "packed-refs"
        if packed.exists():
            for line in packed.read_text(encoding="utf-8").splitlines():
                if line.endswith(" " + name): return line.split(" ", 1)[0]
        return _git(root, "rev-parse", "HEAD")
    except (OSError, WriteError):
        try: return _git(root, "rev-parse", "HEAD")
        except WriteError: return None


def _dirty(root) -> str:
    """The uncommitted paths in the data repository, as one short line, or "" when it is clean.

    Lives here rather than in server.py because the refusal that reports it is raised here, and a
    second copy over there would be the two drifting apart. The screen's read-only banner and this
    refusal now say the same thing because they are the same function.

    Not `.stdout.strip()`: porcelain puts two status columns and a space before the path, so the path
    begins at index 3 — and stripping the whole output eats the leading space of the *first* line
    only. Every path after it survived; the first one always arrived a character short, and with one
    file dirty, which is the usual case, the screen named a file that does not exist.

    **`--no-optional-locks`, and it is not a micro-optimisation.** `git status` refreshes the index
    while it looks, and to do that it takes `.git/index.lock` — the same lock `git add -A` needs one
    line further down in every transaction. This function is called from two places: inside the
    transaction, under the exclusive lock, where nothing else is running; and from `/healthz`, under
    no lock at all, which the map's status bar polls. So a person with the map open was periodically
    taking the index lock, and a save that landed on top of that came back **500** — `fatal: Unable
    to create '.git/index.lock': File exists`. Measured 2026-09-14: a `git status` loop beside a
    `git add -A` loop failed 49 of 200 adds. With this flag, 0 of 200. The flag is exactly for this;
    the answer is the same, git simply does not write while producing it.

    Two more things this line was getting wrong, both of which fail *open*. It did not pass
    `safe.directory` the way `_git` does, so in a container whose repository is owned by another uid
    git refuses with "dubious ownership" — and the return code was never looked at, so any failure
    became empty output, which reads as **clean**. The guard whose whole job is to refuse writes onto
    a hand-edited tree would have quietly allowed them.
    """
    r = subprocess.run(["git", "--no-optional-locks", "-c", "safe.directory=*", "-C", str(root),
                        "status", "--porcelain"], capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        raise WriteError(500, f"cannot tell whether {root} has uncommitted changes: "
                              f"{r.stderr.strip() or 'git status failed'}")
    out = r.stdout
    if not out.strip(): return ""
    names = [l[3:].strip() for l in out.splitlines() if len(l) > 3]
    head = ", ".join(names[:3])
    return head + (f" and {len(names) - 3} more" if len(names) > 3 else "")


TXN_MARKER = "routemind-transaction"


def recover_interrupted(root: Path) -> str:
    """At boot: roll back a transaction the last process did not finish, and nothing else.

    Only when the marker is there — a dirty tree without it is somebody's hand edit and stays
    exactly as it is, refused for writes until it is committed. With it, the dirt is ours: a stale
    index lock is removed and the tree goes back to its last commit. Returns what was done, or ""."""
    marker = root / ".git" / TXN_MARKER
    if not marker.exists(): return ""
    what = ""
    try: what = marker.read_text(encoding="utf-8")[:120]
    except OSError: pass
    lock = root / ".git" / "index.lock"
    if lock.exists():
        try: lock.unlink()
        except OSError: pass
    _restore(root)
    try: marker.unlink()
    except OSError: pass
    return what or "a write"


def _restore(root: Path):
    """Back to HEAD, whatever the transaction did — including what it had already staged. A dry run
    restores after `git add`, and `checkout -- .` restores the *index*, which by then holds the
    change; `reset --hard` restores the commit. The tree was clean when the transaction opened (it
    refuses otherwise), so there is nothing of anybody's to lose."""
    _git(root, "reset", "-q", "--hard", check=False); _git(root, "clean", "-fdq", check=False)


def _yesno(value) -> bool:
    """yes / no, from a boolean or from the word the review queue carries.

    Anything it does not recognise is False, because the field decides whether an area leaves the
    building and the safe reading of an unrecognised value is "do not".
    """
    if isinstance(value, bool): return value
    return str(value or "").strip().lower() in ("yes", "true", "on", "1")


class Writer:
    suggest_id = None            # (name, kind, one_liner, region, taken) -> id. Absent → id is required
    suggest_id_configured = None
    suggest_kind = None          # (name, one_liner, region, content) -> a kind from the vocabulary. Absent → kind is required

    def __init__(self, root: Path):
        self.root = root
        self.store = Store(root)

    def _resolve_id(self, given: str | None, *, name: str, kind: str, one_liner: str, region: str) -> tuple[str, bool]:
        """Make an id when none was given. **Never auto-increments** — something like `x-2` is a
        permanent address that means nothing."""
        nid = (given or "").strip()
        if nid:
            if not ID_RE.match(nid): raise WriteError(400, "id must be ASCII kebab-case")
            if (why := name_too_long(nid, suffix=".md")):
                raise WriteError(400, f"id: {why}", code="name_too_long",
                                 data={"field": "id", "n": len(nid.encode()) + 3, "max": NAME_MAX})
            if self.store.node(nid):
                raise WriteError(409, f"node {nid} exists", code="id_taken", data={"id": nid})
            return nid, False
        # **Do not ask a model a question the name already answers.** The reason an LLM is here at
        # all is that a non-Latin name cannot be slugged by a regex — it yields "" or, worse,
        # something wrong but plausible. That reason does not apply to a name that slugs cleanly.
        # Asking anyway invites the model to characterise instead of translate: "Parcels" came back
        # as `tracking-system`, a permanent address matching nothing the person typed.
        slug = slug_id(name)
        if slug and (why := name_too_long(slug, suffix=".md")):
            # The name is the caller's, so the refusal names the name and not the slug it made.
            raise WriteError(400, f"the name {name!r} gives an id of {len(slug)} characters — {why}",
                             code="name_too_long", data={"field": "name", "n": len(slug) + 3, "max": NAME_MAX})
        if slug:
            if not self.store.node(slug): return slug, False
            # **The collision is refused before any model is asked, configured or not.** Asking one
            # here produced `books-2` — the model was told "must not collide", and that instruction
            # has exactly one cheap answer. It is also the answer this method's own rule forbids: a
            # numbered id is a permanent address that means nothing.
            #
            # The deeper reason is that a model cannot solve this. The name collides, so there is no
            # id for it to find — only a disguise for one. The person has called a thing what another
            # thing is already called, and only they can settle that.
            raise WriteError(409, f"the name {name!r} gives the id {slug}, which is taken — choose another name, or supply an id",
                             code="name_taken", data={"name": name, "id": slug})
        if not (self.suggest_id_configured and self.suggest_id_configured()):
            raise WriteError(503, "id is required — this name gives none on its own and no LLM is configured to translate it (ONTOLOGY_LLM_*)",
                             code="no_llm", data={"field": "id"})
        taken = [n["id"] for n in self.store.nodes()]
        nid = (self.suggest_id(name=name, kind=kind, one_liner=one_liner, region=region, taken=taken) or "").strip()
        if not nid or not ID_RE.match(nid):
            raise WriteError(422, f"id could not be generated ({nid!r}) — supply one")
        if (why := name_too_long(nid, suffix=".md")):
            raise WriteError(422, f"the suggested id is {len(nid)} characters — {why}. Supply one")
        if self.store.node(nid):
            raise WriteError(409, f"the suggested id {nid} already exists — supply one (this never auto-increments)")
        return nid, True

    def _resolve_kind(self, given: str | None, *, name: str, one_liner: str, region: str, content: str = "") -> tuple[str, bool]:
        """Decide a kind when none was given. **Never invents one outside the vocabulary** — if it
        is not in the list, this fails."""
        k = (given or "").strip()
        if k: return k, False
        if self.suggest_id_configured and self.suggest_id_configured():
            k = (self.suggest_kind(name=name, one_liner=one_liner, region=region, content=content) or "").strip()
            if k: return k, True
        # `default_kind` in vocab.yaml, when there is no LLM to choose. A kind is in no prompt and in
        # no table an agent receives; its one reader is `export: no` on a kind in vocab.yaml, which
        # keeps that sort of thing from crossing a link. Requiring a person to pick one was a field
        # with no effect but a refusal. The response still reports `kind_generated`, so a domain that
        # relies on that rule can see which kinds were never actually chosen.
        fallback = str((self.store.vocab().get("default_kind") or "")).strip()
        if fallback: return fallback, True
        raise WriteError(503, "kind is required — no LLM is configured to decide one (ONTOLOGY_LLM_*), "
                              "and vocab.yaml declares no default_kind", code="no_llm", data={"field": "kind"})

    # ---- the one write path ----
    def entity_path(self, region: str, eid: str) -> Path:
        """Where an entity lives. One type, one shape: `regions/<area>/<id>.md`.

        The bound is repeated here on purpose. Every caller above refuses an over-long name with a
        message about the field the caller actually typed, which is the useful error; this one is
        the floor under all of them, because `child_id` composes `<parent>-<stem>` and a route that
        never asked a person for the id can still arrive with one too long to write. A crash inside
        the transaction is the one outcome this must not have."""
        if (why := name_too_long(eid, suffix=".md")): raise WriteError(400, f"id {eid[:24]}…: {why}")
        return self.root / "regions" / region / f"{eid}.md"

    def child_id(self, parent: str, stem: str) -> str:
        """An id for a child named `<stem>.md`. Ids are global, so a stem already taken elsewhere is
        prefixed with the parent — the same rule the migration used, kept in one place.

        Which means **whoever gets there first keeps the short id**: a `note.md` on a minor node
        takes the global `note`, and a real node wanting that id later gets 409. It also makes the id
        depend on what the repository already held, so building the same content in a different order
        names some children differently. Both are consequences of ids being global and of matching
        what the migration wrote; neither can be fixed here without renaming every child on disk.
        """
        taken = {n["id"] for n in self.store.nodes()}
        return stem if stem not in taken else f"{parent}-{stem}"

    def descendants(self, eid: str) -> list[str]:
        """Everything that hangs under an entity. Deleting an entity takes its children with it —
        the old shape deleted a directory, and a child left with a `parent` that resolves to
        nothing is the orphan that shape made impossible."""
        out, frontier = [], [eid]
        while frontier:
            cur = frontier.pop()
            kids = [n["id"] for n in self.store.nodes() if n.get("parent") == cur]
            out += kids; frontier += kids
        return out

    def transact(self, message, actor: str, mutate, *, dry_run: bool = False, after=None) -> dict:
        """mutate → regenerate → validate → commit, or nothing.

        `after(before, now)` runs once the tree validates and before the commit, with the tree as it
        was and as it is: a change set decides there whether the lines over it are all decided, and
        anything it raises rolls the write back like a validation failure. What it returns goes into
        the result. `message` may be a callable, for a commit message that names what `after` found.

        `dry_run` is the same transaction with the commit left out — the one way a preview cannot
        disagree with the write it previews.

        Every result carries `impacted`: the lines whose tables this write changed — the parent of
        what was added, moved or deleted, the parent of a line reworded. Nobody has to act on it; the
        screen shows it so a line going stale is seen by somebody."""
        from .change import stale_lines
        with _lock, repo_lock(self.root):
            if not (self.root / ".git").exists(): raise WriteError(500, "data directory is not a git repository")
            # Boot always leaves a commit. No HEAD means the directory was swapped under this process
            # (a backup restored while running), and every write then failed as "node … not found" or
            # "region … does not exist" — true of the dead mount, and no help (operator QA, 2026-10-10).
            if head(self.root) is None:
                raise WriteError(503, "the data directory has no git history — if it was replaced while this was "
                                      "running, restart it: docker compose restart ontology", code="repo_replaced")
            if (dirty := _dirty(self.root)):
                raise WriteError(409, "working tree is dirty — someone edited the repository by hand; commit or revert it first",
                                 code="tree_dirty", data={"files": dirty})
            before = self.store.nodes()
            # A marker for the length of the transaction, under .git where it is never part of the
            # tree. A process killed between `mutate` and the commit left a dirty tree and an index
            # lock, and every write after it was refused as "someone edited the repository by hand"
            # (2026-10-10). The marker is what tells the next boot that the dirt is an interrupted
            # write of its own — safe to roll back — and not a person's edit, which is never touched.
            marker = self.root / ".git" / TXN_MARKER
            try: marker.write_text(str(message) if not callable(message) else "change set", encoding="utf-8")
            except OSError: pass
            try:
                mutate()
                sync_region_node_lists(self.store); regenerate(self.store)
                res = validate(self.store)
                if not res["ok"]:
                    # The details stay English: they are 52 different diagnostics for someone fixing
                    # data, and a dictionary of those is one nobody would read or keep current.
                    raise WriteError(422, "validation failed — nothing was written", res["errors"],
                                     code="validation_failed", data={"n": len(res["errors"])})
                _git(self.root, "add", "-A")
                if not _git(self.root, "status", "--porcelain"): raise WriteError(200, "no change")
                now = self.store.nodes()
                extra = after(before, now) if after else {}
                impacted = stale_lines(before, now)
                msg = message() if callable(message) else message
                if dry_run:
                    _restore(self.root)
                    return {"ok": True, "dry_run": True, "revision": None, "message": msg, "warnings": list(res["warnings"]),
                            "stats": res["stats"], "impacted": impacted, **extra}
                _git(self.root, "-c", f"user.name={actor}", "-c", f"user.email={actor}@routemind.local", "commit", "-q", "-m", msg)
            except WriteError:
                _restore(self.root); raise
            except PermissionError as e:
                # The data directory is not this container's to write: the uid, or a read-only mount.
                # It surfaced as "502 PermissionError: …" with a temp file's path in it (2026-10-10).
                _restore(self.root)
                raise WriteError(503, f"cannot write to the data directory — check that data/repo is owned by KNOWLEDGE_UID "
                                      f"and not read-only ({e.filename})", code="repo_unwritable")
            except Exception as e:
                _restore(self.root); raise WriteError(500, f"{type(e).__name__}: {e}")
            finally:
                try: marker.unlink()
                except OSError: pass
            sha = head(self.root)
            warnings = list(res["warnings"])
            return {"ok": True, "revision": sha, "message": msg, "warnings": warnings, "stats": res["stats"],
                    "impacted": impacted, **extra}

    # ---- nodes ----
    def create_node(self, body: dict, actor: str) -> dict:
        region = body.get("region")
        if not region: raise WriteError(400, "region is required — every Data area lives in a Region (core-nodes/ was retired 2026-09-08)")
        if not (self.root / "regions" / region).is_dir():   # SPEC-v2 §1.1 — an area exists because nodes/ does
            raise WriteError(400, f"region {region} does not exist", code="region_missing", data={"region": region})
        holds = body.get("holds") or "content"
        if holds not in ("content", "pointers"): raise WriteError(400, "holds must be content | pointers")
        files = body.get("files") or []                      # [{name, description, content}] — pointer files for a pointer node
        for f in files:
            for k in ("name", "description", "content"):
                if not f.get(k): raise WriteError(400, f"files[]: {k} is required")
        for k in ("name", "one_liner"):
            if not body.get(k): raise WriteError(400, f"{k} is required")
        kind, kind_generated = self._resolve_kind(body.get("kind"), name=body["name"],
                                                  one_liner=body["one_liner"], region=region,
                                                  content="\n\n".join(f.get("content", "") for f in files)[:3000])
        nid, id_generated = self._resolve_id(body.get("id"), name=body["name"], kind=kind,
                                             one_liner=body["one_liner"], region=region)
        base = self.entity_path(region, nid)
        if base.exists(): raise WriteError(409, f"entity {nid} exists", code="id_taken", data={"id": nid})
        def mutate():
            # Asked twice on purpose. The check above runs before the lock — it has to, because the
            # id may still have to be made from the name, and that can call a model — so between it
            # and here another writer can have taken the id. Unlocked, the answer was "free" for
            # both of them and the second silently overwrote the first. This one is inside the
            # transaction, where the answer cannot change under it.
            if base.exists(): raise WriteError(409, f"entity {nid} exists", code="id_taken", data={"id": nid})
            base.parent.mkdir(parents=True, exist_ok=True)
            write_node_index(self.store, {"id": nid, "name": body["name"], "kind": kind, "region": region, "holds": holds, "injected_by": body.get("injected_by"), "status": body.get("status"),
                                          "parent": body.get("parent"),
                                          "one_liner": body["one_liner"], "body": body.get("content") or "",
                                          "path": str(base.relative_to(self.root))})
            # `files` on a create are children, not contents. Each is the same kind of thing as its
            # parent and is written the same way — the only difference is that it declares a `parent`.
            for f in files:
                cid = self.child_id(nid, f["name"][:-3] if f["name"].endswith(".md") else f["name"])
                cp = self.entity_path(region, cid)
                write_node_index(self.store, {"id": cid, "name": name_from_file(cid), "kind": kind,
                                              "region": region, "parent": nid, "holds": "content",
                                              "one_liner": f["description"], "body": f["content"],
                                              "path": str(cp.relative_to(self.root))})
        res = self.transact(f"node {nid}: create", actor, mutate)
        return {**res, "id": nid, "id_generated": id_generated, "kind": kind, "kind_generated": kind_generated}

    def update_node(self, nid: str, body: dict, actor: str, note: str = "") -> dict:
        """Edit an entity's fields. Setting `parent` to something in another area **moves it there**,
        with everything under it, in this same transaction.

        The area is not a field anyone sets; it is the directory the file sits in, and which
        directory that is follows from the parent. So "move to another area" is not a second
        operation with its own endpoint — it is what this one already means, once it stops refusing.

        The rule that used to refuse it stays true and is the reason this works: a parent in another
        area is still an error, because after the move there is no such thing. The entity is in the
        parent's area. Nothing about the check had to be relaxed to let the move happen — which is
        the difference between a move and an exception to a rule.

        ids and bodies do not change."""
        n = self.store.node(nid)
        if not n: raise WriteError(404, f"node {nid} not found")
        if "id" in body and body["id"] != nid: raise WriteError(400, "renaming a node is not supported — create the new one, delete the old")
        moves: list[tuple[str, Path, Path]] = []
        if "parent" in body and (body.get("parent") or None) != (n.get("parent") or None):
            moves = self._plan_move(n, body.get("parent") or None)
        if "region" in body and body["region"] != (moves[0][2].parent.name if moves else n["region"]):
            raise WriteError(400, "an area is not set directly — it is where the parent is, so move the entity by its `parent`")

        def mutate():
            unknown = sorted(set(body) - set(EDITABLE) - {"id", "region", "content"})
            if unknown: raise WriteError(400, f"not editable: {unknown} — editable fields are {sorted(EDITABLE) + ['content']}")
            for k in EDITABLE:
                if k in body: n[k] = body[k]
            # yes/no, and it arrives as a boolean from the API or as a word from the review queue,
            # which carries sentences. `bool("no")` is True, so it cannot go through `bool()` — that
            # is a withdrawal that silently turns export on.
            if "export" in body: n["export"] = _yesno(body["export"])
            # One type: an entity's content is its own field, not a file underneath it. Editing the
            # body and editing the routing line are the same call on the same thing.
            if "content" in body: n["body"] = body["content"]
            by_id = {x["id"]: x for x in self.store.nodes()}
            for eid, src, dst in moves:
                # The moved entity is `n` itself, already carrying this call's edits; the rest are
                # read as they are on disk. Written first, unlinked after, so nothing is ever gone
                # from both places — and the whole thing is one commit either way.
                ent = n if eid == nid else by_id[eid]
                ent["path"] = str(dst.relative_to(self.root))
                dst.parent.mkdir(parents=True, exist_ok=True)
                write_node_index(self.store, ent)
                if src != dst: src.unlink(missing_ok=True)
            if not moves: write_node_index(self.store, n)

        where = f" -> {moves[0][2].parent.name}" if moves else ""
        extra = f" (+{len(moves) - 1} under it)" if len(moves) > 1 else ""
        # `note` says what the update was for, when the caller knows: an export accepted from the
        # review queue read "node expense: update" — the same as its withdrawal (2026-10-10).
        return self.transact(f"node {nid}: update{where}{extra}" + (f" — {note}" if note else ""), actor, mutate)

    def _plan_move(self, n: dict, new_parent: str | None) -> list:
        """Where every file goes when `n` is re-parented. Empty when the area does not change.

        A move takes the whole subtree, because `parent` is the only thing that says an entity is in
        an area at all: leave a child behind and it is in area A naming a parent in area B, which is
        the very state the validator calls an error."""
        if new_parent is None: return []
        tgt = self.store.node(new_parent)
        if not tgt: raise WriteError(400, f"parent {new_parent} does not exist", code="parent_missing", data={"id": new_parent})
        # A loop is checked before the area is, because it is not a fact about areas. Dropping an
        # entity onto its own child inside one area is the same mistake and has to be refused the
        # same way — `validate` would catch it, but only as "nothing was written", which tells the
        # person who just dragged something nothing about what they did.
        family = [n["id"], *self.descendants(n["id"])]
        if new_parent in family:
            raise WriteError(409, f"parent {new_parent} is inside {n['id']} — an entity cannot hang under itself",
                             code="move_into_itself", data={"id": n["id"]})
        if tgt["region"] == n["region"]: return []
        # An area's face cannot leave it — the area would have nothing speaking for it, and
        # `validate` refuses that state rather than inventing a new speaker.
        if n.get("role") == "representative" and not n.get("parent"):
            raise WriteError(409, f"{n['id']} is what speaks for area {n['region']} — moving it would leave that area with no representative",
                             code="face_cannot_move", data={"id": n["id"], "region": n["region"]})
        by_id = {x["id"]: x for x in self.store.nodes()}
        out = []
        for eid in family:
            dst = self.entity_path(tgt["region"], eid)
            if dst.exists() and dst != (self.root / by_id[eid]["path"]):
                raise WriteError(409, f"area {tgt['region']} already holds {eid}")
            out.append((eid, self.root / by_id[eid]["path"], dst))
        return out

    def delete_node(self, nid: str, actor: str) -> dict:
        n = self.store.node(nid)
        if not n: raise WriteError(404, f"node {nid} not found")
        kids = self.descendants(nid)
        # Operator, 2026-09-11: "하위에 AS가 더 있는데 상위를 지우려하면 지우지못하게 해" — if there is an
        # area under it, the parent must not be deletable. One type has no separate class of "node",
        # but the screen draws the line the operator means, and it is the advertised `type`: a
        # document (`data`) is something you read, and it is part of its parent the way a file inside
        # a node's directory always was, so it goes along. Anything else is a thing someone made and
        # opens like an area — including an empty one, which is exactly what "+ New node" leaves
        # behind. **Empty is not the same as absent**; it is a node nobody has written yet, and
        # losing it to one click is the harm. Same stance `delete_region` has always taken.
        all_nodes = self.store.nodes()
        holds = {x["parent"] for x in all_nodes if x.get("parent")}
        blockers = sorted(x["id"] for x in all_nodes if x.get("parent") == nid
                          and (x["id"] in holds or not (x.get("body") or "").strip()))
        if blockers:
            raise WriteError(409, f"{nid} holds {', '.join(blockers)} — "
                                  f"{'these are nodes' if len(blockers) > 1 else 'that is a node'}, not a document. "
                                  f"Move or delete {'them' if len(blockers) > 1 else 'it'} first",
                             code="holds_children", data={"id": nid, "n": len(blockers), "held": ", ".join(blockers)})
        gone = {nid, *kids}
        by_id = {x["id"]: x for x in self.store.nodes()}
        def mutate():
            for eid in gone:
                t = self.root / by_id[eid]["path"]
                shutil.rmtree(t) if t.is_dir() else t.unlink(missing_ok=True)
        res = self.transact(f"node {nid}: delete" + (f" (+{len(kids)} child)" if kids else ""), actor, mutate)
        res["removed_children"] = sorted(kids); return res

    # ---- node files ----
    def put_file(self, nid: str, name: str, body: dict, actor: str) -> dict:
        """When no `description` is given:
             existing file → **keep the one it has.** Rewriting the routing line on every content
                             edit changes a sentence nobody touched, silently.
             new file      → **refuse.** That line is the routing signal an agent picks the file on,
                             and every routing line is a person's (operator, 2026-09-11: the LLM is a
                             button). It used to be written here by the LLM when left out; nothing on
                             the screen ever left it out, so that path only reached raw API callers
                             (removed 2026-10-07). The ✨ Suggest button drafts one to edit."""
        n = self.store.node(nid)
        if not n: raise WriteError(404, f"node {nid} not found")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*\.md", name) or name == "INDEX.md": raise WriteError(400, "file name must be <ascii-kebab>.md and not INDEX.md")
        if (why := name_too_long(name)):
            raise WriteError(400, f"file name: {why}", code="name_too_long",
                             data={"field": "file_name", "n": len(name.encode()), "max": NAME_MAX})
        if "content" not in body: raise WriteError(400, "content is required")
        # A new document never replaces one silently. The screen's "new data" form and an upload use
        # the same PUT as an edit, so a name already taken under this node overwrote that document
        # with no warning (2026-10-10). `create_only` says "this is new": an existing one is refused.
        if body.get("create_only") and any(f["name"] == name for f in n["files"]):
            raise WriteError(409, f"{nid} already holds {name}", code="file_exists", data={"name": name[:-3]})
        desc = (body.get("description") or "").strip()
        existing = next((f["description"] for f in n["files"] if f["name"] == name), None)
        content = body["content"].rstrip("\n") + "\n"
        line = desc or existing or ""
        if not line: raise WriteError(400, "description is required — it is the line an agent chooses this on", code="description_required")
        # A file is an entity that declares a `parent`. Writing one is writing an entity, so this is
        # `create_node`/`update_node` under an older name; the endpoint stays while the screen still
        # speaks in files.
        cur = next((x for x in self.store.nodes() if x.get("parent") == nid and f"{x['id']}.md" == name), None)
        cid = cur["id"] if cur else self.child_id(nid, name[:-3])
        cp = self.entity_path(n["region"], cid)
        def mutate():
            text = content
            m = FM_RE.match(text)
            # The supplied content may declare things **about itself** — `scope` says which service's
            # facts it states, and the validator refuses a common file that names one. Writing the
            # entity replaces the frontmatter wholesale, so anything the author declared has to be
            # carried across or it disappears with no error and no sign on the screen.
            declared = (yaml.safe_load(m.group(1)) or {}) if m else {}
            write_node_index(self.store, {**(cur or {}), **{k: declared[k] for k in CONTENT_DECLARED if k in declared},
                                          # The name the person typed, when they typed one: a document
                                          # filed as "출장비 기준" is called that on the map, not by the
                                          # address its name was romanised into (2026-10-10).
                                          "id": cid, "name": (cur or {}).get("name") or str(body.get("name") or "").strip() or name_from_file(cid),
                                          "kind": (cur or {}).get("kind") or n["kind"], "region": n["region"],
                                          "parent": nid, "holds": "content", "one_liner": line,
                                          "body": (m.group(2) if m else text),
                                          "described_by": declared.get("described_by") or (cur or {}).get("described_by"),
                                          "path": str(cp.relative_to(self.root))})
        # The id it was written under, which is not always the name: a stem taken elsewhere gets the
        # holder's prefix (`laptops-swelling`), and the screen had said `/v1/nodes/swelling`.
        res = self.transact(f"node {nid}: file {cid}", actor, mutate)
        return {**res, "id": cid}

    def delete_file(self, nid: str, name: str, actor: str) -> dict:
        n = self.store.node(nid)
        if not n or name not in [f["name"] for f in n["files"]]: raise WriteError(404, "file not listed on this node")
        child = next((x for x in self.store.nodes() if x.get("parent") == nid and f"{x['id']}.md" == name), None)
        if not child: raise WriteError(404, "file not listed on this node")
        return self.delete_node(child["id"], actor)

    def create_region(self, body: dict, actor: str) -> dict:
        """Create a new area — **in one transaction, carrying everything hop 0 needs.**

        An area is not like a node. `regions.json` is derived and an area exists because its `nodes/`
        directory does (SPEC-v2 §1.1), so "create an area" is really **create a representative node
        in a new namespace**.

        The problem is hop 0. A representative with no `use_when` is **a row with a title and nothing
        else**, which an agent will never choose. An empty slot left to be filled later does not get
        filled, so it is required. It is the one sentence: a CORE.md row was a second one, required
        here until 2026-10-07 though no agent was ever shown it."""
        src = str(body.get("source") or "").strip()
        # No trailing hyphen and no double one: `it-` and `it--support` were accepted (2026-10-10).
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", src or ""):
            raise WriteError(400, "source must be lowercase ascii-kebab (it is the area directory name)", code="bad_area_name", data={"region": src})
        if (why := name_too_long(src)):
            raise WriteError(400, f"source: {why}", code="name_too_long",
                             data={"field": "source", "n": len(src.encode()), "max": NAME_MAX})
        if (self.root / "regions" / src).exists(): raise WriteError(409, f"region {src} exists", code="region_exists", data={"region": src})
        rep = body.get("representative") or {}
        for k in ("name", "one_liner", "use_when"):
            if not str(rep.get(k) or "").strip():
                raise WriteError(400, f"representative.{k} is required — {'it is the condition for choosing this area at hop 0' if k == 'use_when' else 'it is how the representative describes itself'}")
        label = src.replace("-", "_").upper()
        kind, kind_generated = self._resolve_kind(rep.get("kind"), name=rep["name"], one_liner=rep["one_liner"], region=src)
        nid, id_generated = self._resolve_id(rep.get("id"), name=rep["name"], kind=kind, one_liner=rep["one_liner"], region=src)
        base = self.entity_path(src, nid)

        def mutate():
            base.parent.mkdir(parents=True, exist_ok=True)
            write_node_index(self.store, {"id": nid, "name": rep["name"], "kind": kind, "region": src,
                                          "holds": "content", "injected_by": None, "status": None,
                                          "role": "representative", "use_when": rep["use_when"],
                                          # Off unless somebody says otherwise: export is opt-in per
                                          # area and in writing — see docs/CIRCUIT.md. The line it
                                          # crosses with is `use_when` above; there is one sentence.
                                          "export": _yesno(rep.get("export")),
                                          "one_liner": rep["one_liner"], "body": "",
                                          "path": str(base.relative_to(self.root))})

        res = self.transact(f"region {src}: create (representative {nid})", actor, mutate)
        return {**res, "source": src, "key": label, "representative": nid,
                "id_generated": id_generated, "kind": kind, "kind_generated": kind_generated}

    def delete_region(self, src: str, actor: str) -> dict:
        """Delete an area — **directory and representative in one transaction.**

        Being able to create but not delete is half a feature. And deleting in pieces leaves
        intermediate states that do not validate: delete the representative first and it is refused
        with "no node speaks for this area". So it goes at once.

        **Only when empty.** Any node besides the representative and this refuses — a person has to
        know what they are about to lose."""
        d = self.root / "regions" / src
        if not d.is_dir(): raise WriteError(404, f"region {src} not found")
        mine = [n for n in self.store.nodes() if n["region"] == src]
        others = [n["id"] for n in mine if n.get("parent") or n.get("role") != "representative"]
        if others: raise WriteError(409, f"region {src}: nodes remain {others} — delete them first",
                                    code="region_not_empty", data={"region": src, "n": len(others)})
        ids = {n["id"] for n in mine}

        def mutate():
            shutil.rmtree(d)

        res = self.transact(f"region {src}: delete ({len(ids)} nodes)", actor, mutate)
        return {**res, "source": src, "removed_nodes": sorted(ids)}

    def promote_file(self, nid: str, name: str, body: dict, actor: str) -> dict:
        """Promote — **insert a named parent above this entity, in one transaction.**

        I had this wrong. Reading the old code, promotion looked like it was about identity: a file
        had no address, so being promoted was how it got one, and under one type it already has one,
        so I reduced this to editing fields. That translated what the old code *did* and lost what
        it was *for*.

        What it is for (operator, 2026-09-11): there was one AWX document under `catalog`. Continua
        arrives, and now two things belong together with nothing to hold them. Promote makes that
        holder — the person names it — and AWX moves under it, so Continua can be added beside AWX
        rather than beside `catalog`. **It makes room for a sibling.** Under two types that
        coincided with lifting a file into a node of its own; under one type it does not, and the
        screen's card has been promising the right thing while this did the other.

        The entity being promoted keeps its id, its name and its body. That is the part one type
        makes cheap: the old version created a new id, because the file could not keep an identity it
        never had.

        Two writes that must not half-happen — a new parent with nothing under it is exactly the
        stranded state the old version's transaction existed to prevent."""
        parent = self.store.node(nid)
        if not parent: raise WriteError(404, f"node {nid} not found")
        child = next((x for x in self.store.nodes() if x.get("parent") == nid and f"{x['id']}.md" == name), None)
        if not child: raise WriteError(404, "file not listed on this node")
        if body.get("region") and body["region"] != child["region"]:
            raise WriteError(400, "moving an entity between Regions is not supported")
        for k in ("name", "one_liner"):
            if not str(body.get(k) or "").strip():
                raise WriteError(400, f"{k} is required — it names the holder being made, not the thing being moved into it")
        region = child["region"]
        kind, kind_generated = self._resolve_kind(body.get("kind"), name=body["name"],
                                                  one_liner=body["one_liner"], region=region)
        new_id, id_generated = self._resolve_id(body.get("id"), name=body["name"], kind=kind,
                                                one_liner=body["one_liner"], region=region)
        if new_id == child["id"]: raise WriteError(409, f"{new_id} is the entity being promoted — the holder needs a name of its own")
        dest = self.entity_path(region, new_id)
        if dest.exists(): raise WriteError(409, f"entity {new_id} exists")

        def mutate():
            write_node_index(self.store, {"id": new_id, "name": body["name"], "kind": kind,
                                          "region": region, "holds": "content", "injected_by": None,
                                          "status": None, "parent": child.get("parent"),
                                          "one_liner": body["one_liner"], "body": "",
                                          "path": str(dest.relative_to(self.root))})
            # The child moves under it. Its id does not change, so every address to it still resolves —
            # the old promotion could not say that.
            write_node_index(self.store, {**child, "parent": new_id})

        res = self.transact(f"promote {child['id']} under new {new_id}", actor, mutate)
        return {**res, "id": new_id, "promoted": child["id"], "id_generated": id_generated,
                "kind": kind, "kind_generated": kind_generated}
