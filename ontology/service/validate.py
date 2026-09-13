"""Ontology v2 validator — the rules of ontology/CLAUDE.md and SPEC-v2, as code.

validate(store) -> {"ok": bool, "errors": [...], "warnings": [...], "stats": {...}}
Every write through the API must pass this before it is committed.
"""
from __future__ import annotations
from collections import Counter
import re
from .store import Store, alias_names, file_scope, region_key, FM_RE

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# An id is not only an address: it is the file name `<id>.md`, and an area name is a directory name.
# Every filesystem this runs on stops one path component at 255 bytes, and the write path had no bound
# of its own — so a 300-character id passed the kebab-case check above, passed validation, and died
# inside the transaction on `OSError: [Errno 36] File name too long`, which the API could only report
# as `502 internal error`. Probing every malformed input the API accepts, that was the only one that
# came back without a reason. The number is the filesystem's and not a matter of taste; there is
# nothing here to tune.
PEER_NAME = re.compile(r"^[a-z][a-z0-9-]{0,30}$")
NAME_MAX = 255
ID_MAX = NAME_MAX - len(".md")


def name_too_long(value: str, *, suffix: str = "") -> str | None:
    """The refusal for a name that cannot become a file, or None when it can.

    Bytes rather than characters, because the limit is the filesystem's. Ids are ASCII so the two
    agree, but an area name or an attached file name reaches here before anything has promised that.
    """
    n = len(str(value).encode("utf-8")) + len(suffix)
    if n <= NAME_MAX: return None
    return (f"that is {n} bytes as the file name and a path component holds at most {NAME_MAX} — "
            f"{'an id becomes ' + repr(str(value)[:24] + '….md') if suffix else 'shorten it'}")


def edge_rules(vocab: dict) -> list[dict]:
    """Domain rules about which edges are wrong, declared in `vocab.yaml` rather than written here.

    These used to be four constants — kind names from one particular domain — compared against one
    particular area name. In any other domain neither side ever matched, so the rules could not fire
    and validation quietly ran three checks short while looking complete. A rule that cannot fire is
    worse than no rule: it reads as coverage.

    If the vocabulary is the domain, the judgments attached to the vocabulary are the domain too.
    Shape, all keys optional except `error`:

        edge_rules:
        - from_kind: task          # the source node's kind
          to_region: config-store  # the target node's area directory
          error: "a task pointing at the store is a step, not structure"
    """
    out = []
    for r in (vocab.get("edge_rules") or []):
        if isinstance(r, dict) and str(r.get("error") or "").strip(): out.append(r)
    return out


EXPANDS_IN = {"service_fragment", "inventory"}   # where the concrete detail lives

def _ref_exists(store: Store, ref: str) -> bool:
    """Does a cross-area reference like `AREA_KEY/file.md` point at something that exists?

    The key→directory table used to be a constant holding one domain's areas, which meant a reference
    into any area created afterwards was refused as non-existent — including every area in a new
    domain. It is derived from the areas that are actually there.
    """
    m = re.match(r"^([A-Z_]+)/(.+\.md)$", ref)
    if not m: return False
    dirs = {region_key(d["dir"]): d["dir"] for d in store.regions()}
    r = dirs.get(m.group(1))
    if r is None: return False
    return any((store.root / c).exists() for c in (f"regions/{r}/{m.group(2)}", f"regions/{r}/nodes/{m.group(2)}"))


def export_kinds(vocab: dict) -> set[str]:
    """The kinds that do not cross a link, declared on the kind itself in `vocab.yaml`.

        kinds:
          - id: table
            desc: a table of values — amounts, caps, rates, day counts
            export: no          # this kind stays inside this backbone

    On the kind and not somewhere else because the vocabulary is already where a kind is *defined*,
    reviewed and committed — "this sort of thing does not leave" is a sentence about the sort of
    thing, and putting it beside the definition means one decision per kind rather than one per
    entity. Twelve, not seventy-nine.

    A deny list rather than an allow list. The area-level decision is already the opt-in: an area
    crosses because somebody wrote `use_when_export` for it. Requiring every kind to be named again
    would make exporting one area a twelve-part act, and the part everybody would skip is the one
    that matters.
    """
    out = set()
    for k in (vocab.get("kinds") or []):
        if not isinstance(k, dict): continue
        v = k.get("export")
        # `no` in YAML is already False; a string is what somebody writes by hand.
        if v is False or (isinstance(v, str) and v.strip().lower() in ("no", "false", "never")):
            out.add(str(k.get("id") or "").strip())
    return {k for k in out if k}


def area_rules(vocab: dict) -> dict:
    """Per-area rules, declared in `vocab.yaml`. Absent means the area has no special role.

    These were written against one area named `learned`. Naming an area in code makes the rule apply
    to anyone who happens to use that word and to nobody else — it is a role, not a name.

        area_rules:
          learned:
            drafts: true       # this area may hold status: draft
            pointers: true     # every node but the representative must hold pointers
    """
    out = {}
    for k, v in (vocab.get("area_rules") or {}).items():
        if isinstance(v, dict): out[str(k)] = v
    return out


def _norm(name: str) -> str:
    return re.sub(r"[\s·/()\-]", "", name or "").lower()


def validate(store: Store) -> dict:
    errors, warnings = [], []
    vocab = store.vocab(); budgets = vocab.get("budgets", {})
    kinds = {k["id"] for k in vocab.get("kinds", [])}
    # `export` on a kind decides whether that sort of thing crosses a link. Anything but a plain no
    # is refused rather than read as one: a policy that silently means the opposite of what somebody
    # typed is the worst shape this file can take, and `export: maybe` would read as caution.
    for k in (vocab.get("kinds") or []):
        v = k.get("export") if isinstance(k, dict) else None
        if v is None: continue
        if not (v is False or v is True or (isinstance(v, str) and v.strip().lower()
                                            in ("no", "false", "never", "yes", "true"))):
            errors.append(f"vocab kinds[{k.get('id')}]: export must be yes or no, got {v!r} — "
                          f"anything else would be read as one of them and it is not obvious which")
    groups = {g["group"]: [(r["id"] if isinstance(r, dict) else r) for r in g["rels"]] for g in vocab.get("relations", [])}
    rels = {r for rs in groups.values() for r in rs}
    domain_rules = edge_rules(vocab); areas = area_rules(vocab)
    nodes = store.nodes(); edges = store.edges(); regions = {r["dir"] for r in store.regions()}
    by_id = {}

    # ---- nodes ----
    for n in nodes:
        nid = n["id"]
        if not nid or not ID_RE.match(nid): errors.append(f"node {n['path']}: id {nid!r} is not ASCII kebab-case")
        if nid != n["dir"]: errors.append(f"node {n['path']}: id {nid!r} ≠ directory name {n['dir']!r}")
        if nid in by_id: errors.append(f"node id declared twice: {nid}")
        by_id[nid] = n
        if not n["name"]: errors.append(f"node {nid}: no name")
        if n["kind"] not in kinds: errors.append(f"node {nid}: kind {n['kind']!r} not in vocab")
        if n["region"] is None: errors.append(f"node {nid}: every Data area lives in a Region — core-nodes/ was retired 2026-09-08")
        # expands_in — "below this point is outside the ontology". It lets a reader tell, from the
        # listing alone, whether a childless representative is **empty** or is a **boundary**. If that
        # fact lives only in a document body, no consumer can act on it.
        if n.get("expands_in") and n["expands_in"] not in EXPANDS_IN:
            errors.append(f"node {nid}: expands_in {n['expands_in']!r} — must be one of {sorted(EXPANDS_IN)}")
        if n["holds"] not in ("content", "pointers"): errors.append(f"node {nid}: holds must be content | pointers, got {n['holds']!r}")
        if n["status"] not in ("draft", "published"): errors.append(f"node {nid}: status must be draft | published")
        rule = areas.get(n["region"] or "", {})
        if n["status"] == "draft" and not rule.get("drafts"):
            errors.append(f"node {nid}: this area does not take drafts — structure is never drafted by a machine "
                          f"(open it with area_rules.{n['region']}.drafts in vocab.yaml)")
        # An area whose nodes only point: what is learned points at content elsewhere, it never carries
        # its own. **The representative is the exception** (SPEC-v2 §1.1): it has to advertise what the
        # area is, which is a statement about the area rather than a thing learned. Without that, there
        # is nowhere left to say what the area is.
        if rule.get("pointers") and n["holds"] != "pointers" and n.get("role") != "representative":
            errors.append(f"node {nid}: this area holds only pointer nodes — its content lives elsewhere and is pointed at")
        if n["region"] and n["region"] not in regions: errors.append(f"node {nid}: region {n['region']!r} has no directory")
        if not n["one_liner"]: errors.append(f"node {nid}: one-liner (first paragraph) missing")
        listed = [f["name"] for f in n["files"]]
        # A name listed twice puts the same row in the table twice, and a model reads that as **two
        # different files**. One was created during a migration on 2026-09-09 and nothing stopped it.
        for f in {x for x in listed if listed.count(x) > 1}:
            errors.append(f"node {nid}: `## Files` lists {f} twice — two identical rows read as two different files")
        for f in listed:
            if f not in n["present_files"]: errors.append(f"node {nid}: `## Files` lists {f} but the file is not in the directory")
        for f in n["present_files"]:
            if f not in listed: warnings.append(f"node {nid}: {f} is in the directory but not in `## Files` — the API ignores it")
    # A pointer node's files are pointer files: every meaningful line is a reference — a node id, or
    # REGION/path.md — and every reference must resolve. Prose here would be content, and a pointer node has
    # none. Second pass: `by_id` must be complete before a reference to a later Region's node can resolve.
    for n in nodes:
        if n["holds"] != "pointers": continue
        for f in n["present_files"]:
            for ln in (store.root / n["path"] / f).read_text(encoding="utf-8", errors="replace").splitlines():
                ref = ln.strip().lstrip("-").strip()
                if not ref or ref.startswith("#") or ref in by_id or _ref_exists(store, ref): continue
                errors.append(f"pointer node {n['id']}: {f} line {ref[:60]!r} is not a reference that resolves (node id or REGION/path.md)")
    # aliases: unique, never a node id/name
    names = {n["name"] for n in nodes}; seen_alias = {}
    for n in nodes:
        for a in alias_names(n["aliases"]):
            if a in names or a in by_id: errors.append(f"node {n['id']}: alias {a!r} is also a node name/id")
            if a in seen_alias and seen_alias[a] != n["id"]: errors.append(f"alias {a!r} on two nodes: {seen_alias[a]}, {n['id']}")
            seen_alias[a] = n["id"]
    # spelling variants
    norm = {}
    for n in nodes: norm.setdefault(_norm(n["name"]), []).append(n["name"])
    for v in norm.values():
        if len(v) > 1: errors.append(f"node name spelling variants: {v}")

    # ---- scope (operator decision 2026-09-08): a common file states no service's facts ----
    # Game-specific facts are a service's own — they live in that service's fragment. Until a service has a
    # fragment they may sit in Core only inside a file that declares `scope: <svc>` (or a list), so nothing
    # game-specific hides inside what every run reads as common. `scope: mixed` marks a file still to migrate.
    known = [str(s) for s in (vocab.get("known_services") or [])]
    svc_re = re.compile(r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(s) for s in sorted(known, key=len, reverse=True)) + r")(?![A-Za-z0-9_-])") if known else None
    def scan(label: str, text: str, scope):
        if not svc_re: return
        # The frontmatter is not prose. `aliases: [{name: L2UpdateServer, scope: l2a}]` is the
        # sanctioned way to say a service-specific name, and `scope: l2a` names the service in its
        # own declaration — reading either as a claim about a service makes the rule contradict the
        # mechanism it exists to enforce. Under two types this hid: INDEX.md was never scanned.
        m = FM_RE.match(text)
        if m: text = m.group(2)
        if scope == "mixed": warnings.append(f"scope: {label} is `mixed` — several services' facts in one file; migrate them to their fragments"); return
        allowed = set(scope) if isinstance(scope, list) else ({scope} if scope != "common" else set())
        hits = sorted(set(svc_re.findall(text)) - allowed)
        if hits: errors.append(f"scope: {label} is {scope!r} but names service(s) {hits} — a common file states no service's facts; move the rows to that service's fragment or declare `scope:`")
    # An entity's content is its own file, and the loop below reads every `regions/<area>/*.md`.
    for r in regions:
        for p in sorted((store.root / "regions" / r).glob("*.md")):
            if p.name in ("INDEX.md", "edges.md"): continue
            t = p.read_text(encoding="utf-8", errors="replace"); scan(f"regions/{r}/{p.name}", t, file_scope(t))
    for n in nodes:
        for a in n["aliases"]:
            if isinstance(a, dict) and a.get("scope") and a["scope"] not in known: errors.append(f"node {n['id']}: alias {a.get('name')!r} scope {a['scope']!r} is not a known service")

    # ---- representatives — SPEC-v2 §1.1 ----
    # **Exactly one representative with no `parent` per area.** That one is the area's face, and what
    # the outside points at. Below it there may be any number — a representative can contain others.
    tops = {}
    for n in nodes:
        if n.get("role") not in (None, "representative"): errors.append(f"node {n['id']}: role must be representative or absent")
        if n.get("role") == "representative":
            if n["status"] == "draft": errors.append(f"node {n['id']}: a draft cannot represent a Region")
            # The advertisement is a table (name · type · address); `use_when` is the one line that
            # answers "should I come here". Empty goes out as empty — before 2026-09-09 it was filled
            # by copying the representative's one_liner, which put a description where a routing
            # signal belongs. The two being identical means that copy has come back.
            if n.get("parent"):
                pass                                  # an inner representative — not used to decide entry into the area
            elif not (n.get("use_when") or "").strip():
                warnings.append(f"node {n['id']}: a representative with no use_when — the advertisement's 'should I come here' goes out blank")
            elif (n.get("use_when") or "").strip() == (n.get("one_liner") or "").strip():
                errors.append(f"node {n['id']}: use_when is identical to one_liner — a description is not a 'when to come here'")
            # `use_when_export` is the same sentence written for a *different* backbone's hop 0 — see
            # docs/PEERING.md. It is checked, not required: an area with none is simply not advertised
            # across a link, which is how export stays opt-in and in writing rather than a default.
            #
            # Identical to `use_when` is fine and will be the common case between backbones of one
            # organisation. Identical to `one_liner` is the same mistake as above, arriving by the same
            # route — someone filled the field by copying the description.
            exp = (n.get("use_when_export") or "").strip()
            if exp:
                if n.get("parent"):
                    errors.append(f"node {n['id']}: only an area's top representative can carry use_when_export — "
                                  f"an inner node is not what a peer chooses")
                if exp == (n.get("one_liner") or "").strip():
                    errors.append(f"node {n['id']}: use_when_export is identical to one_liner — a description is not a 'when to come here'")
                # It becomes one cell of another backbone's routing table, exactly like use_when.
                if "|" in exp or "\n" in exp:
                    errors.append(f"node {n['id']}: use_when_export is one table cell — `|` and newlines are not allowed")
            # `export_to` narrows who that line reaches. It can only ever narrow: an area with no
            # `use_when_export` crosses to nobody, and naming an audience for it changes nothing at
            # all — which is precisely the shape of mistake that looks like it worked. So it is an
            # error and not a warning.
            aud = n.get("export_to") or []
            if aud:
                if not exp:
                    errors.append(f"node {n['id']}: export_to without use_when_export — an audience "
                                  f"for an area that crosses to nobody. Write the line, or take the "
                                  f"audience away too if you are withdrawing it")
                if n.get("parent"):
                    errors.append(f"node {n['id']}: only an area's top representative can carry export_to")
                for a in aud:
                    # Matched against a peer's name at whoever enforces it — this backbone's own
                    # peers.yaml for a direct link, the exchange's members.yaml behind one. Held to
                    # the same shape either way, because a name that cannot be a member is an
                    # audience of nobody and would read as a working restriction.
                    if not PEER_NAME.match(a):
                        errors.append(f"node {n['id']}: export_to names {a!r}, which is not a peer name "
                                      f"— ASCII kebab-case, starting with a letter")
            # A line written for one named reader instead of the one everybody else gets. Every rule
            # the default line has applies to each of these, because each becomes exactly the same
            # cell in exactly the same kind of table — just somebody else's.
            per = n.get("use_when_export_for") or {}
            if per:
                if not exp:
                    errors.append(f"node {n['id']}: use_when_export_for without use_when_export — a "
                                  f"line for one peer and nothing for the rest. Write the line, or "
                                  f"take the override away too if you are withdrawing it")
                if n.get("parent"):
                    errors.append(f"node {n['id']}: only an area's top representative can carry use_when_export_for")
                for who, line in sorted(per.items()):
                    if not PEER_NAME.match(who):
                        errors.append(f"node {n['id']}: use_when_export_for names {who!r}, which is not a "
                                      f"peer name — ASCII kebab-case, starting with a letter")
                    if "|" in line or "\n" in line:
                        errors.append(f"node {n['id']}: use_when_export_for[{who}] is one table cell — "
                                      f"`|` and newlines are not allowed")
                    if line.strip() == (n.get("one_liner") or "").strip():
                        errors.append(f"node {n['id']}: use_when_export_for[{who}] is identical to one_liner "
                                      f"— a description is not a 'when to come here'")
                    if line.strip() == exp:
                        # Not a warning. It reads as a decision to say something different to that
                        # peer, and says the same thing — so the day the default changes, one reader
                        # silently keeps the old sentence and nobody is looking there.
                        errors.append(f"node {n['id']}: use_when_export_for[{who}] is identical to "
                                      f"use_when_export — an override that overrides nothing")
                    if aud and who not in aud:
                        errors.append(f"node {n['id']}: use_when_export_for[{who}] writes a line for a peer "
                                      f"that export_to leaves out — it would never be read")
            if not n.get("parent"):
                if n["region"] in tops:
                    errors.append(f"region {n['region']}: two top representatives ({tops[n['region']]}, {n['id']}) — an area has one face. Give one of them a parent")
                tops[n["region"]] = n["id"]
        elif (n.get("use_when_export") or "").strip():
            errors.append(f"node {n['id']}: use_when_export on a node that does not represent an area — "
                          f"a peer chooses areas, not nodes")
        elif n.get("export_to"):
            errors.append(f"node {n['id']}: export_to on a node that does not represent an area — "
                          f"an audience is something an area has")
        elif n.get("use_when_export_for"):
            errors.append(f"node {n['id']}: use_when_export_for on a node that does not represent an "
                          f"area — a peer chooses areas, not nodes")
    # A representative that carries nothing and has no expands_in cannot be told apart, from the
    # listing alone, as **empty** or as a **boundary**. If that distinction lives only in a document
    # body, neither the screen nor an agent can use it — and both will state something they cannot know.
    has_kid = set()
    for n in nodes:
        if n.get("parent"): has_kid.add(n["parent"])
    for n in nodes:
        if n.get("role") == "representative" and n.get("parent") and n["id"] not in has_kid and not n.get("expands_in"):
            warnings.append(f"node {n['id']}: a representative that carries nothing and has no expands_in — the listing cannot say whether it is empty or a boundary")

    # An entity with no document and nothing under it is advertised as `type: empty`. That is
    # honest, but it is also a row an agent can only ever bounce off — someone made it and never
    # wrote it. The warning is how it gets finished instead of quietly accumulating. Advertising a
    # node with nothing behind it sends a model on a round trip that ends with it answering from the
    # one line in the row (core-05, 2026-09-09).
    #
    # A second rule used to say the same thing further down, written before flattening and asking
    # `n["files"] or n["id"] in _kids`. Both halves of that test are the same question — `files` is
    # derived from the children (store.py) — and neither half is `body`, so it fired on every leaf
    # document in the ontology: the thing that has a document is the thing it called documentless. Its
    # only unique coverage was that false positive, so it is gone rather than made body-aware, which
    # would have made it a duplicate of this one.
    for n in nodes:
        if not (n.get("body") or "").strip() and not any(x.get("parent") == n["id"] for x in nodes):
            warnings.append(f"node {n['id']}: no document and nothing under it — it advertises as `empty`, which is a row with nothing behind it")

    for rdir in regions:
        if rdir not in tops: errors.append(f"region {rdir}: no top representative — no node says what this area is (SPEC-v2 §1.1)")

    # ---- parent (nested representatives) ----
    for n in nodes:
        par = n.get("parent")
        if not par: continue
        tgt = by_id.get(par)
        if not tgt: errors.append(f"node {n['id']}: parent {par!r} does not exist"); continue
        if tgt["region"] != n["region"]: errors.append(f"node {n['id']}: parent {par} is in another area ({tgt['region']}) — a relation across areas is an edge")
        # "only representatives carry nodes" was the two-type containment rule: a file could not hold
        # anything, so anything holding had to be a node, and a node under a node had to be a
        # representative. One type drops that — holding others is a property, not a class. What still
        # has to hold is that the chain ends: every entity reaches its area's top representative.
        # What remains is that the chain ends. Requiring it to end **at a representative** would be a
        # new rule, not a translation of the old one: `beta` can sit at the top of an area without
        # speaking for it, and holding something does not change that.
        seen, cur = {n["id"]}, tgt
        while cur is not None and cur.get("parent"):
            if cur["id"] in seen: errors.append(f"node {n['id']}: parent chain loops at {cur['id']}"); break
            seen.add(cur["id"]); cur = by_id.get(cur["parent"])
    # cycles
    for n in nodes:
        seen, cur = set(), n
        while cur and cur.get("parent"):
            if cur["id"] in seen: errors.append(f"node {n['id']}: parent chain is a cycle"); break
            seen.add(cur["id"]); cur = by_id.get(cur["parent"])

    # ---- edges ----
    seen = set(); degree = {nid: 0 for nid in by_id}
    max_note = int(budgets.get("edge_note_max_lines", 6))
    for e in edges:
        s, r, t = e.get("from"), e.get("rel"), e.get("to")
        if s not in by_id: errors.append(f"edge {s}-{r}->{t}: unknown from-node {s!r}"); continue
        if t not in by_id: errors.append(f"edge {s}-{r}->{t}: unknown to-node {t!r}"); continue
        if r not in rels: errors.append(f"edge {s}-{r}->{t}: relation {r!r} not in vocab")
        if (s, r, t) in seen: errors.append(f"edge {s}-{r}->{t}: declared twice")
        seen.add((s, r, t)); degree[s] += 1; degree[t] += 1
        note = e.get("note") or ""
        if len([l for l in note.splitlines() if l.strip()]) > max_note:
            errors.append(f"edge {s}-{r}->{t}: note exceeds {max_note} lines — move it to a node file or a Region doc")
        src = e.get("source")
        # `source` is the entity the relation was read off. It used to be a path, because a file was
        # not addressable; one type gives it an id, so it is named the same way `from` and `to` are.
        # The path form is still accepted while trees in the old layout are still readable.
        if src and src not in by_id and not (store.root / src).exists():
            errors.append(f"edge {s}-{r}->{t}: source {src} is neither an entity id nor a path that exists")
        sk, tk = by_id[s]["kind"], by_id[t]["kind"]
        for rule in domain_rules:
            if "from_kind" in rule and sk != rule["from_kind"]: continue
            if "to_kind" in rule and tk != rule["to_kind"]: continue
            if "rel" in rule and r != rule["rel"]: continue
            if "from_region" in rule and by_id[s]["region"] != rule["from_region"]: continue
            if "to_region" in rule and by_id[t]["region"] != rule["to_region"]: continue
            errors.append(f"edge {s}-{r}->{t}: {rule['error']}")
    for nid, n in by_id.items():
        if degree[nid]: continue
        warnings.append(f"node {nid}: no relations — nothing points at this node except containment (its area and representative)"
                        + (" (it is a top representative — normal for a new area, an island if it stays that way)"
                           if n.get("role") == "representative" and not n.get("parent") else ""))

    # ---- budgets ----
    def budget(label, n, cap):
        if n > cap: errors.append(f"budget exceeded: {label} {n} > {cap}")
        elif n >= cap * 0.8: warnings.append(f"budget {label} at {n}/{cap}")
    budget("kinds", len(kinds), int(budgets.get("kinds", 12)))
    # `nodes: 70` counted the addressable things, and under two types a file was not one. Flattening
    # made 32 files addressable without adding any knowledge, so the count moved for a reason that
    # has nothing to do with the ontology growing — the unit changed, and the cap is restated in the
    # new unit rather than raised in the old one. `nodes` is still read so an unconverted tree keeps
    # its cap.
    budget("entities", len(nodes), int(budgets.get("entities", budgets.get("nodes", 70))))
    # What one person reads at once is one listing, not the whole map. The old budget could not see
    # this at all: a representative with 16 files counted as 1.
    for par, kids in Counter(n["parent"] for n in nodes if n.get("parent")).items():
        budget(f"children of {par}", kids, int(budgets.get("children_per_entity", 25)))
    for g, rs in groups.items(): budget(f"relations in {g!r}", len(rs), int(budgets.get("relations_per_group", 8)))
    used_rels = {e.get("rel") for e in edges}
    for r in rels - used_rels: warnings.append(f"relation {r} is in vocab but unused")
    used_kinds = {n["kind"] for n in nodes}
    for k in kinds - used_kinds: warnings.append(f"kind {k!r} is in vocab but unused")

    # seeds.yaml retired (2026-09-09). It fed a taught initial spreading-activation pass, and the
    # spreading is gone. A validator that keeps enforcing a setting nothing reads makes it look alive.
    #
    # ---- empty slots that look alive ----
    # A field that is empty in every record is either dead or used by nobody. From outside, both look
    # like "a slot you may fill", and that is where the next person puts something. This happened twice
    # in one day (2026-09-09): `see_region` — which the validator forbids a value for while the API
    # kept emitting it as null — actually misled a consumer, and `index` (permanently "" after the area
    # INDEX.md was retired) was created hours after the same person deleted the first one. **A comment
    # cannot prevent this, which is why the rule is here.**
    #
    # Two things this rule does not see (confirmed 2026-09-09):
    #  1. **Empty right now is not the same as dead.** `status` is absent from every node and is not
    #     dead — the curator writes it on drafts, and there are no drafts pending. Code that writes it
    #     means it is alive.
    #  2. **All-the-same is also dead.** `data_kind` and `authority` were: one literal at the emit site
    #     stamped the same value on every row. They are not empty, so the rule below misses them; they
    #     were found by hand. Widening it to "warn when every value is identical" would wrongly catch
    #     `status` from (1). What separates the two is not in the data — it is **whether any code ever
    #     writes something other than the default** — and that cannot be seen from here.

    for label, records in (("node", nodes), ("region", store.regions())):
        if not records: continue
        for k in sorted(set().union(*(r.keys() for r in records))):
            if all(r.get(k) in (None, "", [], {}) for r in records):
                warnings.append(f"{label}.{k}: empty in all {len(records)} records — a dead field, or a slot nobody uses. From outside it looks like one you may fill")

    # ---- regions.json vs directories ----
    # `dir` is derived from `source`. Putting a `path` in regions.json publishes it, and once it is
    # published someone builds an address out of it. One value has no reason to exist under two names.
    rj = {r["source"].replace("_", "-"): r for r in store.regions_json().get("regions", [])}
    for d in regions:
        if d not in rj: errors.append(f"regions.json: missing entry for regions/{d}")
        else:
            declared = set(rj[d].get("nodes", [])); actual = {n["id"] for n in nodes if n["region"] == d and n["status"] != "draft"}
            if declared != actual: errors.append(f"regions.json {d}: nodes {sorted(declared ^ actual)} differ from directory")
            if rj[d].get("source") != d.replace("-", "_"): errors.append(f"regions.json {d}: source must be {d.replace('-', '_')!r}")
    for d in rj:
        if d not in regions: errors.append(f"regions.json: entry {d} has no directory")
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "stats": {"nodes": len(nodes), "edges": len(edges), "kinds": len(kinds), "relations": len(rels), "regions": len(regions),
                      "revision": store.revision()}}
