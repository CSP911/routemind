"""Writes — every mutation is: change the repo working tree → regenerate derived files → validate → git commit →
publish atomically. On validation failure the working tree is restored and nothing is published.

Publication layout (the volume Pi mounts read-only, SPEC-v2 §5):
  <publish>/<sha>/        complete checkout of one commit — write-once, never modified
  <publish>/current       symlink → <sha>/, replaced atomically (rename)
  <publish>/REVISION      the sha behind `current`, written after the swap
Pi may read through `current/` (fixed root) or pin to REVISION; both never see a half-applied state.
"""
from __future__ import annotations
import contextlib, os, re, shutil, subprocess, sys, tempfile, threading, time
from pathlib import Path
import yaml
from .store import Store, set_frontmatter, FM_RE
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
    to go and look at than a hand edit."""
    if fcntl is None or not (root / ".git").is_dir():
        yield; return
    with open(root / ".git" / "routemind-write.lock", "a+") as f:
        deadline = time.monotonic() + wait
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); break
            except OSError:
                if time.monotonic() >= deadline:
                    raise WriteError(503, f"another process is writing to {root} and has held it for more than "
                                          f"{wait:g}s — one writer per data directory. If nothing else should be "
                                          f"running, look for a second ontology on this mount.")
                time.sleep(0.05)
        try: yield
        finally: fcntl.flock(f, fcntl.LOCK_UN)


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
    """
    out = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                         capture_output=True, text=True, timeout=10).stdout
    if not out.strip(): return ""
    names = [l[3:].strip() for l in out.splitlines() if len(l) > 3]
    head = ", ".join(names[:3])
    return head + (f" and {len(names) - 3} more" if len(names) > 3 else "")


def _restore(root: Path):
    _git(root, "checkout", "--", ".", check=False); _git(root, "clean", "-fdq", check=False)


def _world_readable(top: Path) -> None:
    """Directories 0755, files 0644 — the published tree is read by iris-pi under a different uid."""
    os.chmod(top, 0o755)
    for d, dirs, files in os.walk(top):
        for x in dirs: os.chmod(Path(d) / x, 0o755)
        for x in files: os.chmod(Path(d) / x, 0o644)


def publish(root: Path, publish_dir: Path, sha: str | None = None, keep: set[str] | None = None) -> str:
    """Check out `sha` (default HEAD) into <publish>/<sha> and swap `current`. Idempotent.
    `keep`: revisions that must survive pruning — the Core revisions service fragments pin (`core_revision`).
    A fragment validates its references against the exact tree it was written for; prune that tree and the pin
    goes dead (found 2026-09-08: bsna's aca32cf was pruned after five later Core publishes)."""
    sha = sha or head(root)
    if not sha: raise WriteError(500, "repository has no HEAD")
    publish_dir.mkdir(parents=True, exist_ok=True)
    target = publish_dir / sha
    if not target.exists():
        tmp = Path(tempfile.mkdtemp(prefix=".stage-", dir=publish_dir))
        r = subprocess.run(["git", "-c", "safe.directory=*", "-C", str(root), "archive", "--format=tar", sha], capture_output=True)
        if r.returncode != 0: shutil.rmtree(tmp, ignore_errors=True); raise WriteError(500, "git archive failed: " + r.stderr.decode())
        subprocess.run(["tar", "-x", "-C", str(tmp)], input=r.stdout, check=True)
        (tmp / "REVISION").write_text(sha + "\n", encoding="utf-8")
        # Drafts never reach Pi: a machine-made node the human has not confirmed is removed from the checkout.
        # The echo the design guards against starts the moment Pi reads such a node.
        drafts, parent_of = set(), {}
        for f in tmp.glob("regions/*/*.md"):
            m = FM_RE.match(f.read_text(encoding="utf-8"))
            if not m: continue
            fm = m.group(1)
            par = re.search(r"^parent:\s*(\S+)\s*$", fm, re.M)
            if par: parent_of[f.stem] = par.group(1)
            if re.search(r"^status:\s*draft\s*$", fm, re.M): drafts.add(f.stem)
        # A draft takes what hangs under it. Under two types this came free — the draft was a
        # directory and its files went with it. One type makes containment a field, so a child left
        # behind would publish with a `parent` that resolves to nothing.
        changed = True
        while changed:
            changed = False
            for kid, par in parent_of.items():
                if par in drafts and kid not in drafts: drafts.add(kid); changed = True
        for f in tmp.glob("regions/*/*.md"):
            if f.stem in drafts: f.unlink(missing_ok=True)
        _world_readable(tmp)                                    # mkdtemp is 0700 and the host umask may be 0077 — Pi runs as another uid
        os.rename(tmp, target)                                  # write-once checkout appears atomically
    link_tmp = publish_dir / f".current-{sha[:8]}"
    if link_tmp.is_symlink() or link_tmp.exists(): link_tmp.unlink()
    os.symlink(sha, link_tmp); os.replace(link_tmp, publish_dir / "current")   # atomic swap
    (publish_dir / "REVISION").write_text(sha + "\n", encoding="utf-8"); os.chmod(publish_dir / "REVISION", 0o644); os.chmod(publish_dir, 0o755)
    # keep the last few checkouts only
    kept = sorted((p for p in publish_dir.iterdir() if p.is_dir() and not p.is_symlink() and re.fullmatch(r"[0-9a-f]{40}", p.name)), key=lambda p: p.stat().st_mtime)
    pinned = {k for k in (keep or set()) if k}
    for old in kept[:-5]:
        if any(old.name.startswith(k) for k in pinned): continue     # a fragment still points here
        shutil.rmtree(old, ignore_errors=True)
    return sha


def _line_map(value) -> dict:
    """Peer name to the line that peer is shown. Anything that is not a mapping of text to text is
    nothing, and an empty line removes that peer's override rather than writing a blank one."""
    if not isinstance(value, dict): return {}
    return {str(k).strip(): str(v).strip() for k, v in value.items()
            if str(k).strip() and str(v).strip()}


def _name_list(value) -> list[str]:
    """Peer names off the wire: a list, or one name, or a comma-separated string. Normalised in one
    place so that what is stored does not depend on which of those a caller sent."""
    if value is None: return []
    if isinstance(value, str): value = [v for v in re.split(r"[,\s]+", value) if v]
    if not isinstance(value, list): return []
    return sorted({str(v).strip() for v in value if str(v).strip()})


class Writer:
    describe_configured = None   # () -> bool. "not configured" (503) and "could not generate" (422) are different facts
    suggest_id = None            # (name, kind, one_liner, region, taken) -> id. Absent → id is required
    suggest_id_configured = None
    suggest_kind = None          # (name, one_liner, region, content) -> a kind from the vocabulary. Absent → kind is required
    describe = None          # (name, content) -> one line. The server wires the LLM in. Absent → a new file must carry a description

    def __init__(self, root: Path, publish_dir: Path | None, fragments_dir: Path | None, keep_provider=None):
        self.root, self.publish_dir, self.fragments_dir = root, publish_dir, fragments_dir
        self.keep_provider = keep_provider          # () -> set of Core revisions fragments pin; publish() will not prune them
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
        # `default_kind` in vocab.yaml, when there is no LLM to choose. In the default configuration
        # nothing reads a kind — it is in no prompt and in no table an agent receives, and `edge_rules`
        # ships empty — so requiring a person to pick one was a field with no effect but a refusal.
        # The response still reports `kind_generated`, so a domain that later declares edge_rules can
        # see which kinds were never actually chosen.
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
        prefixed with the parent — the same rule the migration used, kept in one place."""
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

    def transact(self, message: str, actor: str, mutate) -> dict:
        with _lock, repo_lock(self.root):
            if not (self.root / ".git").exists(): raise WriteError(500, "data directory is not a git repository")
            if (dirty := _dirty(self.root)):
                raise WriteError(409, "working tree is dirty — someone edited the repository by hand; commit or revert it first",
                                 code="tree_dirty", data={"files": dirty})
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
                _git(self.root, "-c", f"user.name={actor}", "-c", f"user.email={actor}@iris.local", "commit", "-q", "-m", message)
            except WriteError:
                _restore(self.root); raise
            except Exception as e:
                _restore(self.root); raise WriteError(500, f"{type(e).__name__}: {e}")
            sha = head(self.root)
            # **Publishing is downstream of the write, so its failure is not the write's failure.**
            # The commit above is already in the repository and every read here serves the repository,
            # not the checkout — the entity exists and answers the moment this returns. This used to
            # propagate, so a publish that could not write (a full disk, a read-only mount, a checkout
            # directory owned by another uid) answered `500 internal error` for a write that had fully
            # succeeded. An agent told that retries and gets `409 exists`; a person presses Submit
            # again. Both are then acting on a lie about what is in the ontology, which is the one
            # thing this codebase cannot afford to be wrong about.
            #
            # It is a warning rather than a silence because the checkout really is behind, and it
            # catches up on its own: the next successful write publishes the new HEAD, which carries
            # this commit, and a restart republishes. Nothing is lost and nothing needs undoing — but
            # anything reading the published tree is stale until then, and only this can say so.
            warnings = list(res["warnings"])
            if self.publish_dir:
                try:
                    publish(self.root, self.publish_dir, sha, keep=(self.keep_provider() if self.keep_provider else None))
                except Exception as e:
                    sys.stderr.write(f"publish failed after committing {sha}: {type(e).__name__}: {e}\n")
                    warnings.append(f"committed as {sha[:8]}, but the published checkout could not be written "
                                    f"({type(e).__name__}: {e}) and is still behind. The write itself is safe: "
                                    f"the next successful write, or a restart, publishes it.")
            return {"ok": True, "revision": sha, "message": message, "warnings": warnings, "stats": res["stats"]}

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
        new_edges = body.get("edges") or []          # a node must relate to something — create it with its first edge(s)
        for e in new_edges:
            for k in ("from", "rel", "to"):
                if not e.get(k): raise WriteError(400, f"edges[]: {k} is required")
            if nid not in (e["from"], e["to"]): raise WriteError(400, "edges[] must involve the new node")
        def mutate():
            base.parent.mkdir(parents=True, exist_ok=True)
            write_node_index(self.store, {"id": nid, "name": body["name"], "kind": kind, "region": region, "holds": holds, "injected_by": body.get("injected_by"), "status": body.get("status"),
                                          "parent": body.get("parent"), "aliases": body.get("aliases") or [],
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
            if new_edges:
                edges = self.store.edges()
                for e in new_edges:
                    ne = {"from": e["from"], "rel": e["rel"], "to": e["to"]}
                    if e.get("note"): ne["note"] = e["note"]
                    if e.get("source"): ne["source"] = e["source"]
                    edges.append(ne)
                self._save_edges(edges)
        res = self.transact(f"node {nid}: create" + (f" (+{len(new_edges)} edge)" if new_edges else ""), actor, mutate)
        return {**res, "id": nid, "id_generated": id_generated, "kind": kind, "kind_generated": kind_generated}

    def update_node(self, nid: str, body: dict, actor: str) -> dict:
        """Edit an entity's fields. Setting `parent` to something in another area **moves it there**,
        with everything under it, in this same transaction.

        The area is not a field anyone sets; it is the directory the file sits in, and which
        directory that is follows from the parent. So "move to another area" is not a second
        operation with its own endpoint — it is what this one already means, once it stops refusing.

        The rule that used to refuse it stays true and is the reason this works: a parent in another
        area is still an error, because after the move there is no such thing. The entity is in the
        parent's area. Nothing about the check had to be relaxed to let the move happen — which is
        the difference between a move and an exception to a rule.

        ids, bodies and edges do not change. An edge that used to sit inside one area now crosses
        two, which is what an edge is for."""
        n = self.store.node(nid)
        if not n: raise WriteError(404, f"node {nid} not found")
        if "id" in body and body["id"] != nid: raise WriteError(400, "renaming a node is not supported — create the new one, move edges, delete the old")
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
            # An audience is a list wherever it is stored and arrives as whatever the caller had:
            # a list from the API, one comma-separated line from the review queue, which carries a
            # sentence and not a structure. Normalised here rather than at each door, because the
            # cost of getting it wrong is silent — `", ".join("branch")` is `b, r, a, n, c, h`.
            if "export_to" in body: n["export_to"] = _name_list(body["export_to"])
            if "use_when_export_for" in body:
                n["use_when_export_for"] = _line_map(body["use_when_export_for"])
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
        return self.transact(f"node {nid}: update{where}{extra}", actor, mutate)

    def _plan_move(self, n: dict, new_parent: str | None) -> list:
        """Where every file goes when `n` is re-parented. Empty when the area does not change.

        A move takes the whole subtree, because `parent` is the only thing that says an entity is in
        an area at all: leave a child behind and it is in area A naming a parent in area B, which is
        the very state the validator calls an error."""
        if new_parent is None: return []
        tgt = self.store.node(new_parent)
        if not tgt: raise WriteError(400, f"parent {new_parent} does not exist")
        # A loop is checked before the area is, because it is not a fact about areas. Dropping an
        # entity onto its own child inside one area is the same mistake and has to be refused the
        # same way — `validate` would catch it, but only as "nothing was written", which tells the
        # person who just dragged something nothing about what they did.
        family = [n["id"], *self.descendants(n["id"])]
        if new_parent in family:
            raise WriteError(409, f"parent {new_parent} is inside {n['id']} — an entity cannot hang under itself")
        if tgt["region"] == n["region"]: return []
        # An area's face cannot leave it — the area would have nothing speaking for it, and
        # `validate` refuses that state rather than inventing a new speaker.
        if n.get("role") == "representative" and not n.get("parent"):
            raise WriteError(409, f"{n['id']} is what speaks for area {n['region']} — moving it would leave that area with no representative")
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
        edges = self.store.edges(); refs = [e for e in edges if e["from"] in gone or e["to"] in gone]
        by_id = {x["id"]: x for x in self.store.nodes()}
        # a node cannot exist without an edge and an edge cannot exist without its nodes, so the node and its
        # edges go in one transaction — the same way create_node takes its first edges
        def mutate():
            for eid in gone:
                t = self.root / by_id[eid]["path"]
                shutil.rmtree(t) if t.is_dir() else t.unlink(missing_ok=True)
            if refs: self._save_edges([e for e in edges if e not in refs])
        res = self.transact(f"node {nid}: delete" + (f" (+{len(kids)} child)" if kids else "") + (f" (-{len(refs)} edge)" if refs else ""), actor, mutate)
        res["removed_edges"] = [f"{e['from']} {e['rel']} {e['to']}" for e in refs]
        res["removed_children"] = sorted(kids); return res

    # ---- node files ----
    def put_file(self, nid: str, name: str, body: dict, actor: str) -> dict:
        """When no `description` is given:
             existing file → **keep the one it has.** Rewriting the routing line on every content
                             edit changes a sentence nobody touched, silently.
             new file      → **read the body and write one** (operator, 2026-09-10). That line is the
                             routing signal an agent picks the file on, so it is not left to whatever
                             tone the author happened to use. If it cannot be written, **refuse** —
                             an empty description is a row nobody has a reason to choose."""
        n = self.store.node(nid)
        if not n: raise WriteError(404, f"node {nid} not found")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*\.md", name) or name == "INDEX.md": raise WriteError(400, "file name must be <ascii-kebab>.md and not INDEX.md")
        if (why := name_too_long(name)):
            raise WriteError(400, f"file name: {why}", code="name_too_long",
                             data={"field": "file_name", "n": len(name.encode()), "max": NAME_MAX})
        if "content" not in body: raise WriteError(400, "content is required")
        desc = (body.get("description") or "").strip()
        existing = next((f["description"] for f in n["files"] if f["name"] == name), None)
        content = body["content"].rstrip("\n") + "\n"
        generated = False
        if not desc and existing is None:                       # a new file with no description
            if not (self.describe_configured and self.describe_configured()):
                raise WriteError(503, "description is required — no LLM is configured to write one (ONTOLOGY_LLM_*)",
                                 code="no_llm", data={"field": "description"})
            desc = (self.describe(name, content) or "").strip()
            if not desc: raise WriteError(422, "description could not be generated — nothing could be drawn from the body. Supply one, or write the body")
            generated = True
        line = desc or existing or ""
        if not line: raise WriteError(400, "description is required — it is the line an agent chooses this on")
        # A file is an entity that declares a `parent`. Writing one is writing an entity, so this is
        # `create_node`/`update_node` under an older name; the endpoint stays while the screen still
        # speaks in files.
        cur = next((x for x in self.store.nodes() if x.get("parent") == nid and f"{x['id']}.md" == name), None)
        cid = cur["id"] if cur else self.child_id(nid, name[:-3])
        cp = self.entity_path(n["region"], cid)
        def mutate():
            text = set_frontmatter(content, "described_by", "knowledge") if generated else content
            m = FM_RE.match(text)
            # The supplied content may declare things **about itself** — `scope` says which service's
            # facts it states, and the validator refuses a common file that names one. Writing the
            # entity replaces the frontmatter wholesale, so anything the author declared has to be
            # carried across or it disappears with no error and no sign on the screen.
            declared = (yaml.safe_load(m.group(1)) or {}) if m else {}
            write_node_index(self.store, {**(cur or {}), **{k: declared[k] for k in CONTENT_DECLARED if k in declared},
                                          "id": cid, "name": (cur or {}).get("name") or name_from_file(cid),
                                          "kind": (cur or {}).get("kind") or n["kind"], "region": n["region"],
                                          "parent": nid, "holds": "content", "one_liner": line,
                                          "body": (m.group(2) if m else text),
                                          "described_by": "knowledge" if generated else (declared.get("described_by") or (cur or {}).get("described_by")),
                                          "path": str(cp.relative_to(self.root))})
        return self.transact(f"node {nid}: file {name}" + (" (description generated)" if generated else ""), actor, mutate)

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

        The problem is hop 0. A new area has no row in CORE.md, so its `description` is empty, and a
        representative with no `use_when` leaves that empty too — **a row with a title and nothing
        else**, which an agent will never choose. An empty slot left to be filled later does not get
        filled, so **both are required**."""
        src = str(body.get("source") or "").strip()
        if not re.fullmatch(r"[a-z][a-z0-9-]*", src or ""): raise WriteError(400, "source must be lowercase ascii-kebab (it is the area directory name)")
        if (why := name_too_long(src)):
            raise WriteError(400, f"source: {why}", code="name_too_long",
                             data={"field": "source", "n": len(src.encode()), "max": NAME_MAX})
        if (self.root / "regions" / src).exists(): raise WriteError(409, f"region {src} exists")
        rep = body.get("representative") or {}
        for k in ("name", "one_liner", "use_when"):
            if not str(rep.get(k) or "").strip():
                raise WriteError(400, f"representative.{k} is required — {'it is the condition for choosing this area at hop 0' if k == 'use_when' else 'it is how the representative describes itself'}")
        core_desc = str(body.get("core_description") or "").strip()
        if not core_desc: raise WriteError(400, "core_description is required — with no CORE.md row, hop 0 goes out with an empty description")
        if "|" in core_desc or "\n" in core_desc: raise WriteError(400, "this is one table cell — `|` and newlines are not allowed")
        label = src.replace("-", "_").upper()
        kind, kind_generated = self._resolve_kind(rep.get("kind"), name=rep["name"], one_liner=rep["one_liner"], region=src)
        nid, id_generated = self._resolve_id(rep.get("id"), name=rep["name"], kind=kind, one_liner=rep["one_liner"], region=src)
        core = self.root / "CORE.md"
        if not core.exists(): raise WriteError(404, "CORE.md not found")
        text = core.read_text(encoding="utf-8")
        if re.search(r"^\| `" + re.escape(label) + r"` \| ", text, re.M): raise WriteError(409, f"CORE.md already has a `{label}` row")
        # Append after the table's last row. When there are no rows — **which is exactly what a
        # freshly installed ontology looks like** — the separator line is the last thing. Anchoring on
        # rows alone makes the first area impossible forever: there is no row, so it cannot be created,
        # so there is never a row.
        rows = list(re.finditer(r"^\| `[A-Z_]+` \| .+ \|$", text, re.M))
        anchor = rows[-1] if rows else re.search(r"^\|[ \t]*:?-+:?[ \t]*\|[ \t]*:?-+:?[ \t]*\|[ \t]*$", text, re.M)
        if anchor is None:
            raise WriteError(500, "CORE.md has no area table — it needs a header and a separator (`| --- | --- |`)")
        base = self.entity_path(src, nid)
        new_edges = body.get("edges") or []          # known relations go in the same transaction
        for e in new_edges:
            for k in ("from", "rel", "to"):
                if not e.get(k): raise WriteError(400, f"edges[]: {k} is required")
            if nid not in (e["from"], e["to"]): raise WriteError(400, "edges[] must involve the new representative")

        def mutate():
            base.parent.mkdir(parents=True, exist_ok=True)
            write_node_index(self.store, {"id": nid, "name": rep["name"], "kind": kind, "region": src,
                                          "holds": "content", "injected_by": None, "status": None,
                                          "role": "representative", "use_when": rep["use_when"],
                                          # Optional, and absent means this area crosses no link. Export
                                          # is opt-in per area and in writing — see docs/PEERING.md.
                                          "use_when_export": (rep.get("use_when_export") or "").strip() or None,
                                          # And who, when it is not everybody. Validation refuses an
                                          # audience without a line above it, so the two arrive or
                                          # neither does.
                                          "export_to": _name_list(rep.get("export_to")),
                                          "use_when_export_for": _line_map(rep.get("use_when_export_for")),
                                          "aliases": [], "one_liner": rep["one_liner"], "body": "",
                                          "path": str(base.relative_to(self.root))})
            end = anchor.end()
            core.write_text(text[:end] + f"\n| `{label}` | {core_desc} |" + text[end:], encoding="utf-8")
            if new_edges:
                edges = self.store.edges()
                for e in new_edges:
                    ne = {"from": e["from"], "rel": e["rel"], "to": e["to"]}
                    if e.get("note"): ne["note"] = e["note"]
                    edges.append(ne)
                self._save_edges(edges)

        res = self.transact(f"region {src}: create (representative {nid} · CORE row)", actor, mutate)
        return {**res, "source": src, "key": label, "representative": nid,
                "id_generated": id_generated, "kind": kind, "kind_generated": kind_generated}

    def delete_region(self, src: str, actor: str) -> dict:
        """Delete an area — **directory, nodes, edges and the CORE row in one transaction.**

        Being able to create but not delete is half a feature. And deleting in pieces leaves
        intermediate states that do not validate: delete the representative first and it is refused
        with "no node speaks for this area"; delete the directory first and the CORE row survives with
        nothing behind it. So it goes at once.

        **Only when empty.** Any node besides the representative and this refuses — a person has to
        know what they are about to lose."""
        d = self.root / "regions" / src
        if not d.is_dir(): raise WriteError(404, f"region {src} not found")
        mine = [n for n in self.store.nodes() if n["region"] == src]
        others = [n["id"] for n in mine if n.get("parent") or n.get("role") != "representative"]
        if others: raise WriteError(409, f"region {src}: nodes remain {others} — delete them first")
        ids = {n["id"] for n in mine}
        label = src.replace("-", "_").upper()
        core = self.root / "CORE.md"
        text = core.read_text(encoding="utf-8") if core.exists() else ""
        row = re.search(r"^\| `" + re.escape(label) + r"` \| .+ \|$\n?", text, re.M)

        def mutate():
            shutil.rmtree(d)
            edges = [e for e in self.store.edges() if e["from"] not in ids and e["to"] not in ids]
            self._save_edges(edges)
            if row: core.write_text(text[:row.start()] + text[row.end():], encoding="utf-8")

        res = self.transact(f"region {src}: delete ({len(ids)} nodes · CORE row)", actor, mutate)
        return {**res, "source": src, "removed_nodes": sorted(ids), "core_row_removed": bool(row)}

    def put_core_row(self, key: str, description: str, actor: str) -> dict:
        """Change **one row's description cell** in the CORE.md area table.

        That cell is the source of `regions.json.description` and it goes out at hop 0. But CORE.md is
        a narrative carried **whole** into every prompt, so editing one row moves its context with it.
        Hence **row replacement only — no whole-document write.** That is something a person does in
        the repository."""
        desc = (description or "").strip()
        if not desc: raise WriteError(400, "description is required")
        if "|" in desc or "\n" in desc: raise WriteError(400, "this is one table cell — `|` and newlines are not allowed")
        core = self.root / "CORE.md"
        if not core.exists(): raise WriteError(404, "CORE.md not found")
        pat = re.compile(r"^(\| `" + re.escape(key) + r"` \| )(.+?)( \|)$", re.M)
        text = core.read_text(encoding="utf-8")
        m = pat.search(text)
        if not m: raise WriteError(404, f"CORE.md area table has no `{key}` row")
        before = m.group(2)
        if before == desc: raise WriteError(200, "no change")
        def mutate():
            core.write_text(pat.sub(lambda mm: mm.group(1) + desc + mm.group(3), text, count=1), encoding="utf-8")
        res = self.transact(f"core: region {key} description", actor, mutate)
        return {**res, "key": key, "before": before, "after": desc}

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
        makes cheap: the old version created a new id and had to carry the edges across, because the
        file could not keep an identity it never had. Nothing points anywhere new here, so no edge
        moves.

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
                                          "aliases": body.get("aliases") or [],
                                          "one_liner": body["one_liner"], "body": "",
                                          "path": str(dest.relative_to(self.root))})
            # The child moves under it. Its id does not change, so every edge pointing at it still
            # resolves — the old promotion could not say that.
            write_node_index(self.store, {**child, "parent": new_id})

        res = self.transact(f"promote {child['id']} under new {new_id}", actor, mutate)
        return {**res, "id": new_id, "promoted": child["id"], "id_generated": id_generated,
                "kind": kind, "kind_generated": kind_generated}

    # ---- edges ----
    def _save_edges(self, edges: list[dict]):
        head_comment = "# Edges. `from` and `to` are node ids; `rel` must be one of the relations in vocab.yaml.\n\n"
        (self.root / "edges.yaml").write_text(head_comment + yaml.safe_dump(edges, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")

    def add_edge(self, body: dict, actor: str) -> dict:
        for k in ("from", "rel", "to"):
            if not body.get(k): raise WriteError(400, f"{k} is required")
        edges = self.store.edges()
        if any(e["from"] == body["from"] and e["rel"] == body["rel"] and e["to"] == body["to"] for e in edges): raise WriteError(409, "edge exists")
        new = {"from": body["from"], "rel": body["rel"], "to": body["to"]}
        if body.get("note"): new["note"] = body["note"]
        if body.get("source"): new["source"] = body["source"]
        def mutate(): self._save_edges(edges + [new])
        return self.transact(f"edge {body['from']} {body['rel']} {body['to']}: add", actor, mutate)

    def update_edge(self, f: str, rel: str, t: str, body: dict, actor: str) -> dict:
        edges = self.store.edges(); hit = [e for e in edges if e["from"] == f and e["rel"] == rel and e["to"] == t]
        if not hit: raise WriteError(404, "edge not found")
        def mutate():
            for k in ("note", "source"):
                if k in body:
                    if body[k]: hit[0][k] = body[k]
                    else: hit[0].pop(k, None)
            self._save_edges(edges)
        return self.transact(f"edge {f} {rel} {t}: update", actor, mutate)

    def delete_edge(self, f: str, rel: str, t: str, actor: str) -> dict:
        edges = self.store.edges(); rest = [e for e in edges if not (e["from"] == f and e["rel"] == rel and e["to"] == t)]
        if len(rest) == len(edges): raise WriteError(404, "edge not found")
        def mutate(): self._save_edges(rest)
        return self.transact(f"edge {f} {rel} {t}: delete", actor, mutate)

    # ---- service fragments (owner channel) — no validation, no git ----
    def fragment_path(self, svc: str, name: str) -> Path:
        if not self.fragments_dir: raise WriteError(501, "ONTOLOGY_FRAGMENTS is not configured")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", svc) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(md|yaml|yml)", name): raise WriteError(400, "bad service or file name")
        return self.fragments_dir / svc / name

    def put_fragment(self, svc: str, name: str, content: str) -> dict:
        p = self.fragment_path(svc, name); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")
        return {"ok": True, "path": str(p)}
