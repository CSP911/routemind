"""A change set — several decisions about the tree, applied as one commit, with what they do to the
routing lines above them computed rather than guessed (docs/CHANGE.md).

A set is **decisions, not a script**: at most one decision per (entity, aspect), and the order of
application is fixed here — creates, moves, rewordings and body edits, deletes — so the same set in
any order makes the same tree. What a set does to the lines above it is the **impact**: an entity is
impacted when its table (its children's ids and lines) differs before and after, and every impacted
line must be decided in the set, `reword` or `keep`. The cascade climbs exactly as far as the
rewording goes: keep a line and its parent's table is unchanged.

The preview is the apply with the commit left out — one code path, so the two cannot disagree.
"""
from __future__ import annotations
import os, re, shutil, subprocess
from pathlib import Path
from .write import WriteError, Writer, _git, _yesno, name_from_file
from .derive import write_node_index

MAX_DECISIONS = int(os.environ.get("KNOWLEDGE_CHANGE_MAX") or 20)
REF_RE = re.compile(r"^\$[a-z0-9][a-z0-9-]*$")
LINE_FIELDS = ("one_liner", "use_when", "name")
OPS = ("create", "move", "reword", "write", "keep", "delete")
HOP0 = "@hop0"


def _top(n: dict) -> bool:
    return n.get("role") == "representative" and not n.get("parent")


def _line_field(n: dict) -> str:
    """The routing line an entity has: an area's face routes on `use_when` (hop 0 prints it); every
    other entity on `one_liner` (its parent's table prints it)."""
    return "use_when" if _top(n) else "one_liner"


def tables(nodes: list[dict]) -> dict[str, list[tuple[str, str]]]:
    """Every table the tree serves, by its owner: hop 0 (one row per area), and each entity's (one row
    per child, drafts left out as `advertised` leaves them out)."""
    out: dict[str, list] = {HOP0: []}
    tops = {}
    for n in nodes:
        out.setdefault(n["id"], [])
        if _top(n): tops[n["region"]] = n
    for r in sorted(tops):
        out[HOP0].append((r, (tops[r].get("use_when") or "").strip()))
    for n in nodes:
        if n.get("status") == "draft": continue
        # An empty `parent` on something other than the face means the face holds it — the map's
        # "+ New node" on an area writes that, and `store.children_of` reads it so. Counted the same
        # here, or the area's table would change with no line over it impacted.
        owner = n.get("parent") or (tops[n["region"]]["id"] if not _top(n) and n["region"] in tops else None)
        if owner and owner != n["id"]:
            out.setdefault(owner, []).append((n["id"], (n.get("one_liner") or "").strip()))
    for k in out: out[k].sort()
    return out


def stale_lines(before: list[dict], after: list[dict]) -> list[dict]:
    """The lines a write may have left behind: every entity, present before and after, whose table
    changed — the parent of what was added, moved or deleted, and the parent of a line that was
    reworded. Hop 0 has no line of its own. What a single write hands back beside its result, so the
    screen can say "these may be stale" rather than nobody noticing."""
    tb, ta = tables(before), tables(after)
    by_after = {n["id"]: n for n in after}
    out = []
    for owner in sorted(set(tb) & set(ta)):
        if owner == HOP0 or tb[owner] == ta[owner] or owner not in by_after: continue
        n = by_after[owner]
        rb, ra = dict(tb[owner]), dict(ta[owner])
        because = sorted(k for k in set(rb) | set(ra) if rb.get(k) != ra.get(k))
        f = _line_field(n)
        out.append({"id": owner, "field": f, "text": (n.get(f) or "").strip(), "because": because})
    return out


# ── the set ───────────────────────────────────────────────────────────────────
def parse(body: dict, store) -> dict:
    """The set, checked for shape before anything is locked. Every refusal is collected, so one
    answer names everything wrong with it rather than the first thing."""
    if not isinstance(body, dict): raise WriteError(400, "body must be a JSON object")
    raw = body.get("decisions")
    if not isinstance(raw, list) or not raw: raise WriteError(400, "decisions is required — a list of at least one")
    if len(raw) > MAX_DECISIONS:
        raise WriteError(422, f"{len(raw)} decisions — a set holds at most {MAX_DECISIONS}, the size one person can check",
                         code="too_many", data={"n": len(raw), "max": MAX_DECISIONS})
    why = str(body.get("why") or "").strip()
    if not why: raise WriteError(400, "why is required — one line on what this set is for; it becomes the commit")
    nodes = {n["id"]: n for n in store.nodes()}
    areas = {n["region"] for n in nodes.values()} | {d.name for d in (store.root / "regions").iterdir() if d.is_dir()}
    refs: dict[str, dict] = {}
    seen: dict[tuple, int] = {}
    problems: list[str] = []
    decs: list[dict] = []
    # Every ref first: a move may name a holder the set creates further down. Order says nothing.
    known = {str(d.get("ref") or "").strip() for d in raw if isinstance(d, dict) and d.get("op") == "create"}

    def aspect(key, i):
        if key in seen: problems.append(f"decision {i}: a second decision on {key[0]}.{key[1]} (decision {seen[key]} already has it) — one decision per aspect")
        else: seen[key] = i

    for i, d in enumerate(raw, 1):
        if not isinstance(d, dict): problems.append(f"decision {i}: not an object"); continue
        op = str(d.get("op") or "").strip()
        if op not in OPS: problems.append(f"decision {i}: op must be one of {', '.join(OPS)} (got {op!r})"); continue
        d = {**d, "op": op}
        tid = str(d.get("id") or "").strip()
        if op == "create":
            ref = str(d.get("ref") or "").strip()
            if not REF_RE.match(ref): problems.append(f"decision {i}: create needs a ref like $holder — the set's own name for it"); continue
            if ref in refs: problems.append(f"decision {i}: ref {ref} is used twice"); continue
            for k in ("name", "one_liner"):
                if not str(d.get(k) or "").strip(): problems.append(f"decision {i} ({ref}): {k} is required")
            parent = d.get("parent")
            if parent is None:
                src = str(d.get("area") or "").strip()
                if not re.fullmatch(r"[a-z][a-z0-9-]*", src): problems.append(f"decision {i} ({ref}): with no parent this is a new area's face — `area` (its directory name, lowercase kebab) is required")
                elif src in areas: problems.append(f"decision {i} ({ref}): area {src} exists — place it under that area's face instead")
                if not str(d.get("use_when") or "").strip(): problems.append(f"decision {i} ({ref}): a new area needs `use_when` — the sentence hop 0 prints for it")
            else:
                parent = str(parent).strip()
                if parent.startswith("$"):
                    if parent not in known: problems.append(f"decision {i} ({ref}): parent {parent} is not a ref the set creates")
                    elif parent == ref: problems.append(f"decision {i} ({ref}): its own parent")
                elif parent not in nodes: problems.append(f"decision {i} ({ref}): parent {parent} does not exist")
                if d.get("use_when"): problems.append(f"decision {i} ({ref}): use_when belongs to an area's face only — this one has a parent")
            d["parent"] = parent
            refs[ref] = d; aspect((ref, "exists"), i); decs.append(d); continue
        if tid.startswith("$"):
            problems.append(f"decision {i}: {op} on {tid} — a thing made in this set is complete as created; say it in the create"); continue
        if tid not in nodes: problems.append(f"decision {i}: {op} — {tid or '(no id)'} does not exist"); continue
        n = nodes[tid]
        if op == "move":
            parent = str(d.get("parent") or "").strip()
            if not parent: problems.append(f"decision {i}: move {tid} needs a parent")
            elif parent.startswith("$"):
                if parent not in known: problems.append(f"decision {i}: parent {parent} is not a ref the set creates")
            elif parent not in nodes: problems.append(f"decision {i}: parent {parent} does not exist")
            if _top(n): problems.append(f"decision {i}: {tid} is what speaks for area {n['region']} — it cannot move")
            d["parent"] = parent; aspect((tid, "parent"), i)
        elif op in ("reword", "keep"):
            f = str(d.get("field") or "").strip()
            if f not in LINE_FIELDS: problems.append(f"decision {i}: field must be one of {', '.join(LINE_FIELDS)} (got {f!r})")
            elif f == "use_when" and not _top(n): problems.append(f"decision {i}: use_when is an area's sentence, and {tid} is not an area's face — its line is one_liner")
            if op == "reword" and not str(d.get("after") or "").strip(): problems.append(f"decision {i}: reword {tid}.{f} needs `after`")
            d["field"] = f; aspect((tid, f), i)
        elif op == "write":
            if "content" not in d: problems.append(f"decision {i}: write {tid} needs content")
            aspect((tid, "body"), i)
        elif op == "delete":
            if _top(n): problems.append(f"decision {i}: {tid} is what speaks for area {n['region']} — delete the area instead, once it is empty")
            aspect((tid, "exists"), i)
        d["id"] = tid; decs.append(d)
    expose = body.get("expose") or []
    if not isinstance(expose, list): problems.append("expose must be a list of ids or refs")
    if problems:
        raise WriteError(422, "the set cannot be applied as written — nothing was written", problems,
                         code="refused", data={"n": len(problems)})
    return {"why": why, "base": (str(body.get("base") or "").strip() or None), "decisions": decs,
            "expose": [str(x) for x in expose], "refs": refs}


def _order(decs: list[dict]) -> list[dict]:
    """Creates first — new areas, then by parent reference so a holder is written before what hangs
    under it — then moves, then rewordings and bodies, then deletes."""
    creates = [d for d in decs if d["op"] == "create"]
    done, out = set(), []
    while creates:
        ready = [d for d in creates if d["parent"] is None or not str(d["parent"]).startswith("$") or d["parent"] in done]
        if not ready: raise WriteError(422, "creates refer to each other in a loop")
        for d in ready: out.append(d); done.add(d["ref"])
        creates = [d for d in creates if d not in ready]
    out += [d for d in decs if d["op"] == "move"]
    out += [d for d in decs if d["op"] in ("reword", "write")]
    out += [d for d in decs if d["op"] == "delete"]
    return out


def _region_of(d: dict, refs: dict, nodes: dict) -> str:
    if d["parent"] is None: return d["area"]
    p = d["parent"]
    return _region_of(refs[p], refs, nodes) if p.startswith("$") else nodes[p]["region"]


def _descendants(nodes: list[dict], eid: str) -> list[str]:
    out, frontier = [], [eid]
    while frontier:
        cur = frontier.pop()
        kids = [n["id"] for n in nodes if n.get("parent") == cur]
        out += kids; frontier += kids
    return out


def _ancestors(by_id: dict, eid: str) -> list[str]:
    """Up to the area's face — which holds a parentless entity too, as `tables` counts it."""
    tops = {n["region"]: n["id"] for n in by_id.values() if _top(n)}
    out, cur, guard = [], by_id.get(eid), 0
    while cur and guard < 64:
        up = cur.get("parent") or (tops.get(cur["region"]) if not _top(cur) else None)
        if not up or up == cur["id"]: break
        out.append(up); cur = by_id.get(up); guard += 1
    return out


def _area_export(nodes: list[dict]) -> dict[str, bool]:
    return {n["region"]: bool(n.get("export")) for n in nodes if _top(n)}


def impact(before: list[dict], after: list[dict], cs: dict, ids: dict) -> dict:
    """What the set does beyond what it says: the tables it changes, the lines over them and whether
    each is decided, what newly crosses a circuit, what a move carried along."""
    decided = {}
    for d in cs["decisions"]:
        if d["op"] in ("reword", "keep"): decided[(d["id"], d["field"])] = d["op"]
    made = set(ids.values())
    tb, ta = tables(before), tables(after)
    by_b, by_a = {n["id"]: n for n in before}, {n["id"]: n for n in after}
    out_tables, lines = [], []
    for owner in sorted(set(tb) | set(ta)):
        if owner in made or (owner != HOP0 and owner not in by_a) or tb.get(owner, []) == ta.get(owner, []): continue
        out_tables.append({"owner": owner,
                           "before": [{"id": k, "line": v} for k, v in tb.get(owner, [])],
                           "after": [{"id": k, "line": v} for k, v in ta.get(owner, [])]})
        if owner == HOP0 or owner not in by_b: continue
        n = by_a[owner]; f = _line_field(n)
        rb, ra = dict(tb.get(owner, [])), dict(ta.get(owner, []))
        lines.append({"id": owner, "field": f, "text": (n.get(f) or "").strip(),
                      **({"was": (by_b[owner].get(f) or "").strip()} if decided.get((owner, f)) == "reword" else {}),
                      "decided": decided.get((owner, f)),
                      "because": sorted(k for k in set(rb) | set(ra) if rb.get(k) != ra.get(k))})
    idle = sorted(f"{i}.{f}" for (i, f), op in decided.items() if op == "keep" and not any(l["id"] == i and l["field"] == f for l in lines))
    xb, xa = _area_export(before), _area_export(after)
    exposure = []
    for n in after:
        was = bool(xb.get(by_b[n["id"]]["region"])) if n["id"] in by_b else False
        now = bool(xa.get(n["region"]))
        if was != now: exposure.append({"id": n["id"], "from": was, "to": now})
    acked = {ids.get(x, x) for x in cs["expose"]}
    carried = []
    for d in cs["decisions"]:
        if d["op"] == "move":
            for k in _descendants(before, d["id"]): carried.append({"id": k, "under": d["id"]})
    carried.sort(key=lambda c: (c["under"], c["id"]))
    return {"tables": out_tables, "lines": lines, "exposure": exposure, "carried": carried,
            "undecided": [f"{l['id']}.{l['field']}" for l in lines if not l["decided"]],
            "unacknowledged": sorted(e["id"] for e in exposure if e["to"] and e["id"] not in acked),
            "idle_keeps": idle}


def _check_base(root: Path, base: str, paths: set[str]) -> None:
    """The decisions were made against `base`; a file they read or change that moved since is a
    decision made about something that is no longer there. Unrelated files moving is fine."""
    r = subprocess.run(["git", "-c", "safe.directory=*", "-C", str(root), "merge-base", "--is-ancestor", base, "HEAD"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise WriteError(409, f"base {base[:10]} is not a revision this repository has — read the tables again",
                         code="stale", data={"base": base, "files": []})
    changed = set(_git(root, "diff", "--name-only", base, "HEAD").splitlines())
    hit = sorted(changed & paths)
    if hit:
        raise WriteError(409, f"{len(hit)} of the files these decisions rest on changed since {base[:10]} — read them again: {', '.join(hit[:4])}",
                         hit, code="stale", data={"base": base, "files": hit})


def apply(writer: Writer, body: dict, actor: str, *, dry_run: bool = False) -> dict:
    """One set, one commit — or, dry, the same transaction with the commit left out."""
    store = writer.store
    cs = parse(body, store)
    nodes0 = {n["id"]: n for n in store.nodes()}
    # ids for what is created, before the lock (the id may come from a model), and checked again
    # inside it, as create_node does.
    ids: dict[str, str] = {}
    kinds: dict[str, str] = {}
    taken = set(nodes0)
    for d in _order(cs["decisions"]):
        if d["op"] != "create": continue
        region = _region_of(d, cs["refs"], nodes0)
        kind, _ = writer._resolve_kind(d.get("kind"), name=d["name"], one_liner=d["one_liner"], region=region,
                                       content=str(d.get("content") or "")[:3000])
        nid, _ = writer._resolve_id(d.get("id"), name=d["name"], kind=kind, one_liner=d["one_liner"], region=region)
        if nid in taken: raise WriteError(409, f"{d['ref']}: id {nid} is taken (by another decision in this set, or the tree)", code="id_taken", data={"id": nid})
        taken.add(nid); ids[d["ref"]] = nid; kinds[d["ref"]] = kind
    rid = lambda x: ids[x] if isinstance(x, str) and x.startswith("$") else x
    # The files the decisions rest on: what they touch, the parents they name, and every line on the
    # way up from those — the tables the walk read.
    rest = set()
    for d in cs["decisions"]:
        for x in (d.get("id"), d.get("parent")):
            if x and not str(x).startswith("$") and x in nodes0:
                rest.add(nodes0[x]["path"])
                for a in _ancestors(nodes0, x): rest.add(nodes0[a]["path"])
    state: dict = {}

    def mutate():
        if cs["base"]: _check_base(writer.root, cs["base"], rest)
        for d in _order(cs["decisions"]):
            op = d["op"]
            if op == "create":
                nid, region = ids[d["ref"]], _region_of(d, cs["refs"], nodes0)
                path = writer.entity_path(region, nid)
                if path.exists(): raise WriteError(409, f"entity {nid} exists", code="id_taken", data={"id": nid})
                path.parent.mkdir(parents=True, exist_ok=True)
                write_node_index(store, {"id": nid, "name": d["name"], "kind": kinds[d["ref"]], "region": region,
                                         "holds": "content", "injected_by": None, "status": None,
                                         "role": "representative" if d["parent"] is None else None,
                                         "use_when": d.get("use_when") if d["parent"] is None else None,
                                         "export": False, "parent": rid(d["parent"]),
                                         "one_liner": d["one_liner"], "body": str(d.get("content") or ""),
                                         "path": str(path.relative_to(writer.root))})
            elif op == "move":
                n = store.node(d["id"]); new_parent = rid(d["parent"])
                moves = writer._plan_move(n, new_parent)
                n["parent"] = new_parent
                by_id = {x["id"]: x for x in store.nodes()}
                for eid, src, dst in moves:
                    ent = n if eid == n["id"] else by_id[eid]
                    ent["path"] = str(dst.relative_to(writer.root))
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    write_node_index(store, ent)
                    if src != dst: src.unlink(missing_ok=True)
                if not moves: write_node_index(store, n)
            elif op == "reword":
                n = store.node(d["id"]); f = d["field"]
                cur = (n.get(f) or "").strip()
                if d.get("before") is not None and str(d["before"]).strip() != cur:
                    raise WriteError(409, f"{d['id']}.{f} is not what the decision says it was — it reads {cur!r} now",
                                     code="conflict", data={"id": d["id"], "field": f, "current": cur})
                n[f] = str(d["after"]).strip(); write_node_index(store, n)
            elif op == "write":
                n = store.node(d["id"]); n["body"] = str(d["content"] or ""); write_node_index(store, n)
            elif op == "delete":
                all_nodes = store.nodes(); n = next(x for x in all_nodes if x["id"] == d["id"])
                holds = {x["parent"] for x in all_nodes if x.get("parent")}
                blockers = sorted(x["id"] for x in all_nodes if x.get("parent") == n["id"] and (x["id"] in holds or not (x.get("body") or "").strip()))
                if blockers:
                    raise WriteError(409, f"{n['id']} holds {', '.join(blockers)} — nodes, not documents; move or delete them in the set first",
                                     code="holds_children", data={"id": n["id"], "held": ", ".join(blockers)})
                by_id = {x["id"]: x for x in all_nodes}
                for eid in [n["id"], *_descendants(all_nodes, n["id"])]:
                    t = writer.root / by_id[eid]["path"]
                    shutil.rmtree(t) if t.is_dir() else t.unlink(missing_ok=True)

    def after(before, now):
        imp = impact(before, now, cs, ids)
        state["impact"] = imp
        # A dry run is for seeing this. Only the write is refused on it.
        if dry_run: return {"impact": imp, "ids": ids, "impacted": [], "applies": not (imp["undecided"] or imp["unacknowledged"])}
        if imp["undecided"]:
            raise WriteError(409, f"{len(imp['undecided'])} line(s) over the change are not decided — reword or keep each: {', '.join(imp['undecided'])}",
                             imp["undecided"], code="undecided", data={"impact": imp, "ids": ids})
        if imp["unacknowledged"]:
            raise WriteError(409, f"this would make {', '.join(imp['unacknowledged'])} readable through a circuit (an exported area) — say so with `expose`",
                             imp["unacknowledged"], code="exposure", data={"impact": imp, "ids": ids})
        return {"impact": imp, "ids": ids, "impacted": []}

    def message():
        imp = state.get("impact") or {}
        head = f"change: {cs['why']}"
        trail = []
        for d in cs["decisions"]:
            if d["op"] == "create": trail.append(f"Create: {ids[d['ref']]} under {rid(d['parent']) or ('area ' + d['area'])}")
            elif d["op"] == "move": trail.append(f"Move: {d['id']} -> {rid(d['parent'])}")
            elif d["op"] == "reword": trail.append(f"Reword: {d['id']}.{d['field']}")
            elif d["op"] == "keep": trail.append(f"Keep: {d['id']}.{d['field']}" + (f" — {d['why']}" if d.get("why") else ""))
            elif d["op"] == "write": trail.append(f"Write: {d['id']}")
            elif d["op"] == "delete": trail.append(f"Delete: {d['id']}")
        for e in imp.get("exposure", []):
            trail.append(f"{'Expose' if e['to'] else 'Withdraw'}: {e['id']}")
        if cs["base"]: trail.append(f"Base: {cs['base']}")
        return head + "\n\n" + "\n".join(trail) + "\n"

    return writer.transact(message, actor, mutate, dry_run=dry_run, after=after)
