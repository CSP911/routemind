"""Ontology v2 data store — reads the data directory (SPEC-v2 §1–3) into plain dicts.

Nothing here writes, except `write` below, which exists so that nothing anywhere writes a file a
reader can catch half-finished. Layout it understands:
  CORE.md · vocab.yaml · edges.yaml · regions.json · REVISION
  regions/<r>/INDEX.md · regions/<r>/<doc>.md · regions/<r>/edges.md (generated view)
  regions/<r>/nodes/<id>/INDEX.md (+ files)   core-nodes/<id>/INDEX.md (+ files)
"""
from __future__ import annotations
import contextlib, json, os, re, tempfile, threading, time
from pathlib import Path
import yaml

try: import fcntl
except ImportError: fcntl = None            # not POSIX; the containers are, so this only relaxes checks run elsewhere

LOCK_NAME = "routemind-write.lock"
READ_LOCK_WAIT = float(os.environ.get("ONTOLOGY_READ_LOCK_WAIT") or 10.0)


@contextlib.contextmanager
def file_lock(root: Path, *, exclusive: bool, wait: float, on_timeout):
    """The one lock this data directory has, taken shared or exclusive.

    It lives in `.git/`, which is never part of the tree — nothing to commit, nothing to add to
    .gitignore, and no way for the lock itself to make the working tree dirty. Writers take it
    exclusive (see `write.repo_lock`); readers take it shared, which is what makes a read see a tree
    no writer is in the middle of changing.

    `on_timeout` is called to raise, because what the two sides should say when they give up is not
    the same sentence: a writer waiting is one writer behind another, and a reader waiting is a read
    that a long write is holding up.
    """
    if fcntl is None or not (root / ".git").is_dir():
        yield; return
    with open(root / ".git" / LOCK_NAME, "a+") as f:
        deadline = time.monotonic() + wait
        flag = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        while True:
            try:
                fcntl.flock(f, flag | fcntl.LOCK_NB); break
            except OSError:
                if time.monotonic() >= deadline: on_timeout()
                time.sleep(0.05)
        try: yield
        finally: fcntl.flock(f, fcntl.LOCK_UN)


def write(path: Path, text: str) -> None:
    """Replace a file's contents so that a concurrent reader never sees them half-written.

    `Path.write_text` truncates and then fills, and reads here are not serialised against writes:
    a plain `GET` arriving inside that window gets an empty or partial file. Both failures were
    reproduced on 2026-09-13, on **one** server in **one** process, with ordinary reads running
    beside ordinary writes:

      * `regions.json` read while `derive.regenerate` had truncated it —
        `JSONDecodeError: Expecting value: line 1 column 1`, answered as 500 to `GET /v1/regions`.
      * an entity's `.md` read while it was being written — `ValueError: … has no frontmatter`,
        answered as 500 to the `POST` that was resolving an id at the time.

    Neither needed two processes, an exchange, or an unusual install. One person saving while another
    has the map open is the ordinary case, and it is the case that broke.

    Write beside the target and rename: `os.replace` is atomic on POSIX and on Windows, so a reader
    holding the old path sees the old bytes or the new bytes and never a mixture. The temp file goes
    in the same directory — the same filesystem, so the rename cannot become a copy — and is a
    dotfile ending in `.tmp`, so `entity_files`, which globs `*.md`, cannot see it.

    Its name is short and says nothing about the target's, which looks like a missed chance to make
    a leftover easy to trace and is not. An entity's id may be 252 characters — the longest that
    leaves room for `.md` under NAME_MAX, and two checks exist to hold that open. Prefixing the
    target's name onto a temp name puts every one of those over the limit, and the first version
    here did: `OSError: [Errno 63] File name too long`, on the two checks that guard the longest
    name a person may choose.
    """
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".rm-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush(); os.fsync(f.fileno())   # the rename is atomic; the contents being there is not
        os.replace(tmp, path)
    except BaseException:
        try: os.unlink(tmp)
        except OSError: pass
        raise

# Hand-written short keys, for areas whose derived key would be ugly or ambiguous. This table is
# NOT a registry of areas: an area that is not in it still works, it just gets the derived key. See
# docs/DOMAIN-NEUTRALITY.md — the copies of this table in the validators are less forgiving.
REGION_KEY: dict[str, str] = {}


def region_key(d: str) -> str:
    """The short display key. A hand-written abbreviation wins where there is one; otherwise it is
    derived from the directory name, so that a new area gets a key rather than `None` and vanishing
    from the graph."""
    return REGION_KEY.get(d) or d.replace("-", "_").upper()
FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def file_scope(text: str):
    """A content file may open with a frontmatter carrying `scope`. Absent → common.
    Values: "common" | "<service>" | ["svc", ...] | "mixed" (facts of several services — awaiting migration)."""
    m = FM_RE.match(text)
    if not m: return "common"
    fm = yaml.safe_load(m.group(1)) or {}
    v = fm.get("scope", "common")
    return [str(x) for x in v] if isinstance(v, list) else str(v)


def described_by(text: str) -> str | None:
    """**Who wrote** this file's one-line description. Absent means a person did.

    That line is a routing signal: an agent picks the file on the strength of it and nothing else.
    Since 2026-09-10 a new file's description is written by Knowledge from the document itself, so
    **human-written and machine-written lines now sit in the same table** — and a person deciding
    whether to correct one has to be able to tell which is which."""
    m = FM_RE.match(text)
    if not m: return None
    return ((yaml.safe_load(m.group(1)) or {}).get("described_by")) or None


def set_frontmatter(text: str, key: str, value: str) -> str:
    """Set one key in a document's frontmatter, creating the block if there is none and replacing
    only that key if there is."""
    m = FM_RE.match(text)
    line = f"{key}: {value}"
    if not m: return f"---\n{line}\n---\n{text.lstrip()}"
    fm = m.group(1)
    kept = [l for l in fm.splitlines() if not l.startswith(f"{key}:")]
    return "---\n" + "\n".join(kept + [line]) + "\n---\n" + m.group(2).lstrip("\n")


def alias_names(aliases) -> list[str]:
    """Aliases are strings or {name, scope} — a game's own name for a common node. Names either way."""
    return [a["name"] if isinstance(a, dict) else str(a) for a in (aliases or [])]


def _lines(value) -> dict:
    """A peer name to the line that peer is shown, from frontmatter. Anything that is not a mapping of
    text to text is nothing: the field is read on every export and a half-formed one would put a
    fragment of somebody's YAML into another backbone's routing table."""
    if not isinstance(value, dict): return {}
    return {str(k).strip(): str(v).strip() for k, v in value.items()
            if str(k).strip() and str(v).strip()}


def _names(value) -> list[str]:
    """A frontmatter list of peer names, normalised. A single name written bare is a list of one —
    the field is read far more often than it is written, and half of the ways a person writes one
    name are not a YAML list."""
    if value is None: return []
    if isinstance(value, str): value = [v for v in re.split(r"[,\s]+", value) if v]
    if not isinstance(value, list): return []
    return sorted({str(v).strip() for v in value if str(v).strip()})


class Store:
    _snap = threading.local()

    def __init__(self, root: str | os.PathLike):
        self.root = Path(root)

    # ---- one consistent view, for the length of one request ----
    @contextlib.contextmanager
    def snapshot(self):
        """Read the whole tree once, under a shared lock, and serve this thread from that.

        Atomic writes stop a reader seeing half a file. They do not stop it seeing half a
        *transaction*: `regions.json` as it was before the write and an entity's `.md` as it is
        after, in one answer, which is a routing table that never existed. A write here is
        mutate → regenerate → validate → commit, and every one of those steps changes files a reader
        is walking.

        So the reader takes the writers' lock **shared** — several readers at once, no reader while a
        writer holds it — loads everything the tree can offer, and lets go. The lock is held for the
        load and nothing else: `/v1/regions` goes on to ask every peer what it is advertising, and a
        peer that is down would otherwise hold this lock for the whole timeout and stall every write
        on this backbone behind a machine somebody else owns.

        Nested use is a no-op, so a handler that opens one inside another still sees a single view,
        and no code path can take the lock twice and wait on itself.
        """
        if getattr(Store._snap, "data", None) is not None:
            yield; return
        def _late():
            raise TimeoutError(f"a write to {self.root} has held the repository for more than "
                               f"{READ_LOCK_WAIT:g}s; this read gave up rather than hang")
        # **Bytes under the lock, parsing outside it.** Every read used to take what it needed and
        # no more, and `/v1/core` was one small file: 0.19 ms. Loading and *parsing* the whole tree
        # for every request made it 6.37 ms, almost all of it `yaml.safe_load` on vocab.yaml and
        # edges.yaml — 2.5 ms each, and `safe_load` is the pure-python loader even where libyaml is
        # installed. Neither file is touched by most requests.
        #
        # Reading them is what has to happen at one instant; turning them into objects does not. So
        # the lock covers four small reads and a stat of each entity, and a parse happens on first
        # use, once, if it happens at all.
        with file_lock(self.root, exclusive=False, wait=READ_LOCK_WAIT, on_timeout=_late):
            data = {"raw": {n: self._read(n) for n in ("CORE.md", "vocab.yaml", "edges.yaml",
                                                       "regions.json", "REVISION")},
                    # The node cache is keyed on every entity's mtime, so a hit here is not a guess:
                    # it is the same content, and the stat that proved it happened under this lock.
                    "nodes": self.nodes(), "parsed": {}}
        Store._snap.data = data
        try: yield
        finally: Store._snap.data = None

    def _read(self, name: str) -> str | None:
        try: return (self.root / name).read_text(encoding="utf-8")
        except FileNotFoundError: return None

    @classmethod
    def _lazy(cls, name, parse, fallback):
        """The parsed form of one file in the open snapshot, or None when there is no snapshot."""
        d = getattr(cls._snap, "data", None)
        if d is None: return None, False
        if name not in d["parsed"]:
            raw = d["raw"][name]
            d["parsed"][name] = fallback if raw is None else parse(raw)
        return d["parsed"][name], True

    # ---- raw files ----
    # Each serves the open snapshot, and reads the tree directly when there is none — so a write
    # path, which is deliberately outside any snapshot, still sees the tree as it is right now.
    def core(self) -> str:
        v, ok = self._lazy("CORE.md", lambda t: t, "")
        return v if ok else self._core()

    def revision(self) -> str | None:
        v, ok = self._lazy("REVISION", lambda t: t.strip(), None)
        return v if ok else self._revision()

    def vocab(self) -> dict:
        v, ok = self._lazy("vocab.yaml", lambda t: yaml.safe_load(t) or {}, {})
        return v if ok else self._vocab()

    def edges(self) -> list[dict]:
        v, ok = self._lazy("edges.yaml", lambda t: yaml.safe_load(t) or [], [])
        return v if ok else self._edges()

    def regions_json(self) -> dict:
        v, ok = self._lazy("regions.json", json.loads, {"regions": []})
        return v if ok else self._regions_json()

    def _core(self) -> str:
        return (self.root / "CORE.md").read_text(encoding="utf-8")

    def _revision(self) -> str | None:
        p = self.root / "REVISION"
        return p.read_text(encoding="utf-8").strip() if p.exists() else None

    def _vocab(self) -> dict:
        return yaml.safe_load((self.root / "vocab.yaml").read_text(encoding="utf-8")) or {}

    def _edges(self) -> list[dict]:
        return yaml.safe_load((self.root / "edges.yaml").read_text(encoding="utf-8")) or []

    def _regions_json(self) -> dict:
        p = self.root / "regions.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"regions": []}

    # ---- nodes ----
    def entity_files(self):
        """An entity is one `.md`: `regions/<area>/<id>.md`.

        A node and a file are **the same kind of thing** — what differs is what each declares.
        Three independent properties (addressable · readable · holds others) had been forced into
        two shapes, so anything readable that needed an address had to be dressed as a node holding
        exactly one file. As one type each property is a field that is present or absent."""
        for f in sorted((self.root / "regions").glob("*/*.md")):
            yield f.parent.name, f
        # core-nodes/ retired 2026-09-08 — every Data area lives in a Region (interface inheritance: a pointer node
        # is the same kind of thing as a content node, so it takes the same path)

    @staticmethod
    def parse_index(text: str) -> dict:
        """Parse a **service fragment** `INDEX.md`: frontmatter, a one-liner, and a `## Files` list.

        This is no longer how the ontology is stored — an entity is one file and its children
        declare themselves. Fragments are a separate tree, written by whoever owns the service, and
        they still have this shape, so the parser stays for them and says so.

        The Korean `## ...` spelling an early version of this format wrote is not read any more. Nothing
        produces it, and this product's data starts empty, so the only thing keeping it alive was
        that it was already written down."""
        m = FM_RE.match(text)
        if not m: raise ValueError("INDEX.md without frontmatter")
        fm = yaml.safe_load(m.group(1)) or {}
        body = m.group(2)
        one = ""
        for para in re.split(r"\n\s*\n", body.split("\n## ", 1)[0].strip()):
            if para.strip(): one = " ".join(para.split()); break
        files = []
        head = "\n## Files\n" if "\n## Files\n" in "\n" + body else None
        if head:
            sec = ("\n" + body).split(head, 1)[1].split("\n## ", 1)[0]
            for l in sec.splitlines():
                mm = re.match(r"^- ([^\s:][^:]*?) : (.+)$", l.strip())
                if mm: files.append({"name": mm.group(1).strip(), "description": mm.group(2).strip()})
        return {"frontmatter": fm, "one_liner": one, "files": files, "body": body}

    _nodes_cache: tuple | None = None          # (key, list)
    _nodes_lock = __import__("threading").Lock()

    def _nodes_key(self):
        # Same two-step, same answer: a file that vanishes between the glob and the stat leaves the
        # key without it, which is what the next read will find too.
        out = []
        for _, f in self.entity_files():
            try: out.append((str(f), f.stat().st_mtime_ns))
            except FileNotFoundError: pass
        return tuple(out)

    def nodes(self) -> list[dict]:
        import copy
        d = getattr(Store._snap, "data", None)
        # Inside a snapshot this is the list loaded under the lock. Deep-copied on the way out for
        # the same reason the cache is: callers annotate what they are handed.
        if d is not None: return copy.deepcopy(d["nodes"])
        key = self._nodes_key()
        with self._nodes_lock:
            if self._nodes_cache and self._nodes_cache[0] == key:
                return copy.deepcopy(self._nodes_cache[1])
        out = self._read_nodes()
        with self._nodes_lock: self._nodes_cache = (key, copy.deepcopy(out))
        return out

    def _read_nodes(self) -> list[dict]:
        out = []
        for order, (region, f) in enumerate(self.entity_files()):
            # Not `parse_index`: that reads a `## Files` list out of the body, and an entity's body
            # is a document, which may legitimately have a heading by that name.
            #
            # The listing and the read are two steps, and a writer can delete a file between them —
            # a rename, a delete, or `_restore` rolling a failed transaction back. `store.write`
            # closes the *torn* read; it cannot close this one, because there is no content to see.
            # A file that is gone by the time we reach it was not in the tree we are describing, so
            # it is skipped rather than raised: the alternative is a 500 on an ordinary `GET` for a
            # deletion that succeeded.
            try: text = f.read_text(encoding="utf-8")
            except FileNotFoundError: continue
            m = FM_RE.match(text)
            if not m: raise ValueError(f"{f} has no frontmatter — an entity declares its id there")
            fm = yaml.safe_load(m.group(1)) or {}
            # The routing line is `one_liner:` in the frontmatter, because the body is the entity's
            # own content rather than a list of what sits under it. Children are not listed here —
            # each declares its own `parent`, so a list and the tree cannot disagree.
            out.append({
                "id": fm.get("id") or f.stem, "dir": f.stem, "name": fm.get("name"),
                "kind": fm.get("kind"), "region": region, "aliases": fm.get("aliases") or [],
                "holds": fm.get("holds") or "content", "injected_by": fm.get("injected_by"),
                "status": fm.get("status") or "published", "use_when": fm.get("use_when"),
                # What this area says about itself to *another backbone*. Absent means it is not
                # advertised across a link at all — export is opt-in, per area, in writing.
                "use_when_export": fm.get("use_when_export"),
                "export_to": _names(fm.get("export_to")),
                "use_when_export_for": _lines(fm.get("use_when_export_for")),
                "role": fm.get("role"), "parent": fm.get("parent"),
                "expands_in": fm.get("expands_in"), "one_liner": fm.get("one_liner") or "",
                "order": order, "path": str(f.relative_to(self.root)), "body": m.group(2),
                "scope": fm.get("scope", "common"), "described_by": fm.get("described_by"),
            })
        # `files` and `present_files` are derived from the children, not stored. A flat entity's
        # children are the entities that name it as `parent`, and a child's file is `<id>.md` —
        # one identity, one name. Callers that still speak in files keep working through the
        # conversion without a stored list that can disagree with the tree.
        for n in out:
            kids = [k for k in out if k.get("parent") == n["id"]]
            n["files"] = [{"name": f"{k['id']}.md", "description": k["one_liner"]} for k in kids]
            n["present_files"] = sorted(f["name"] for f in n["files"])
            n["file_scopes"] = {f"{k['id']}.md": k.get("scope", "common") for k in kids}
        return out

    def node(self, node_id: str) -> dict | None:
        for n in self.nodes():
            if n["id"] == node_id: return n
        return None

    def node_file(self, node_id: str, name: str) -> str | None:
        n = self.node(node_id)
        if not n or name not in [f["name"] for f in n["files"]]: return None    # not listed → does not exist for the API
        # A file is a child entity, and its document is that entity's own file — the address
        # `nodes/<parent>/files/<name>.md` is the old spelling of `nodes/<name>`, kept while the
        # screen and the agent prompt still use it.
        kid = next((k for k in self.nodes() if k.get("parent") == node_id and f"{k['id']}.md" == name), None)
        if not kid: return None
        p = self.root / kid["path"]
        return p.read_text(encoding="utf-8") if p.exists() else None

    # ---- regions ----
    def regions(self) -> list[dict]:
        """SPEC-v2 §1.1 — **an area is a namespace.** It has no entry document; what it is, its
        representative advertises. It exists because `nodes/` exists, and its face is the
        representative with no `parent`."""
        nodes = self.nodes()
        out = []
        for d in sorted((self.root / "regions").iterdir()):
            if not d.is_dir(): continue
            mine = [n for n in nodes if n["region"] == d.name]
            top = next((n for n in mine if n.get("role") == "representative" and not n.get("parent")), None)
            # `index` was dropped (2026-09-09). The area INDEX.md had been retired, so the field was
            # permanently the empty string — the same shape as `see_region`, which misled a consumer
            # on the same day: **an empty slot pretending to be alive**.
            #
            # With no representative, `advertises` is not emitted as "". An empty string reads as
            # "this area says nothing about itself", when the truth is "this area has nobody to speak
            # for it" — different facts. The validator refuses this state, but **refusing it and being
            # loud about it are not the same thing.**
            out.append({"dir": d.name, "key": region_key(d.name),
                        "representative": top["id"] if top else None,
                        "advertises": top["one_liner"] if top else None,
                        "use_when": (top.get("use_when") if top else None),
                        "use_when_export": (top.get("use_when_export") if top else None),
                        "export_to": (top.get("export_to") if top else []),
                        "use_when_export_for": (top.get("use_when_export_for") if top else {}),
                        "nodes": [n["id"] for n in mine]})
        return out

    def children_of(self, node_id: str) -> list[dict]:
        """The nodes this representative carries. An empty `parent` means the area's top
        representative (SPEC-v2 §1.1)."""
        nodes = self.nodes()
        me = next((n for n in nodes if n["id"] == node_id), None)
        if not me: return []
        tops = {r["dir"]: r["representative"] for r in self.regions()}
        return [n for n in nodes if n["id"] != node_id and
                (n.get("parent") or (tops.get(n["region"]) if n["region"] != n["id"] else None)) == node_id]

    # ---- graph for the 2D/3D pages (same shape the pages already consume) ----
    def graph(self) -> dict:
        vocab = self.vocab(); group_of = {(r["id"] if isinstance(r, dict) else r): g["group"] for g in vocab.get("relations", []) for r in g["rels"]}
        N = [{"id": n["id"], "name": n["name"], "kind": n["kind"], "region": (region_key(n["region"]) if n["region"] else None),
              "region_dir": n["region"], "core": False, "holds": n["holds"], "file": (n["path"] + "/INDEX.md"), "desc": n["one_liner"],
              "order": n["order"], "aliases": alias_names(n["aliases"]), "alias_scopes": [a for a in n["aliases"] if isinstance(a, dict)],
              "file_scopes": n["file_scopes"], "status": n["status"], "injected_by": n.get("injected_by"), "role": n.get("role")} for n in self.nodes()]
        E = [{"s": e["from"], "t": e["to"], "rel": e["rel"], "group": group_of.get(e["rel"], ""), "note": e.get("note", "") or "",
              "file": e.get("source", "")} for e in self.edges()]
        return {"revision": self.revision(), "nodes": N, "edges": E}
