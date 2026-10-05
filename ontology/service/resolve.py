"""A question in a person's words, resolved into the map's own names — before anything is routed.

This is the DNS in front of the routing table. A person types a name the way their team says it;
the map holds a different, canonical name for the same thing; and routing on the wrong one goes to
the wrong place. On 2026-09-30 a person asked for "the most recent work on BNS", an agent read the
word "work", opened one area (ops), found nothing, and said so. The record was four levels down in
a different area, under a node called `neo` that shares a VPC with `bns` — a fact the map already
held as an edge. Nothing translated "BNS" into the two nodes it meant, and nothing turned "most
recent" into the one column built to answer it.

So this does three things a resolver does, and nothing a search engine does:

  CNAME   a name somebody said → the node the map calls it. Sources: every node's id, its name and
          its `aliases` (the field that already exists for this), plus one hop along the map's own
          edges — because the thing you asked about is usually next to the thing you meant.
  TYPE    what is being asked *about* that name — most recent, when, who, how, whether — read from
          plain words. This is common sense, not domain vocabulary, and it is a fixed table here.
  NXDOMAIN when no name in the question is one the map knows, it says so — and still hands over the
          area list, because that list is the only place absence may be claimed from.

**The one thing this is not:** a ranking. Every match is a literal string found in the question,
and every result names the string it matched on. A person can read why "BNS" became `neo` and say
that it is wrong. That is the difference from an embedding, and the reason the front of this
pipeline is allowed to be this simple.

**What always comes back with the answer:** the area list — hop 0. A resolution is per-question, so
it cannot be served from memory, and it arrives with the list every search must start from. That is
how "start at hop 0" stops being a request in a tool description.

**What may be cached, and for how long:** a resolution is good while the map's revision is the one
it was made against, and not a moment longer. An absence is never cached — the one failure DNS spent
years learning to name (RFC 2308) is a "does not exist" that outlives the moment it was true.

Pure. Takes the map as arguments and touches nothing; the service wraps it and the check runs it
without a server.
"""
import re

# ── what is being asked ──────────────────────────────────────────────────────
# Order is priority: the first kind whose words appear wins. "가장 최근" contains "최근" and both are
# `latest`, so containment across rows was checked when the table was written; a new word goes in
# the row it belongs to and nowhere else.
#
# Latin words match on their own boundaries so `how` does not fire inside `show`; Hangul and CJK
# match as substrings because those scripts put no space between a word and its particle — "BNS에서"
# is one token to a regex and two to a person.
ASKS = [
    ("latest",  ["가장 최근", "최근", "최신", "마지막", "가장 나중", "요즘",
                 # Inflections are listed, not derived: `recent` on its own edges does not match
                 # `recently`, and loosening the edge to catch it is how `last` catches `blast`.
                 "latest", "most recently", "most recent", "recently", "recent", "newest", "last"],
     "가장 최근에 바뀐 기록", "the most recently changed record",
     "read the AGE column — the row whose `changed` is newest"),
    ("when",    ["언제", "몇 월", "며칠", "날짜", "기한", "마감",
                 "when", "what date", "deadline", "by when", "due"],
     "언제인지", "when",
     "look for a date or a deadline row"),
    ("who",     ["누구", "누가", "담당", "책임", "담당자",
                 "who", "whom", "owner", "responsible", "in charge"],
     "누가 맡는지", "who is responsible",
     "look for a role or a desk"),
    ("how",     ["어떻게", "방법", "절차", "순서",
                 "how", "steps", "procedure", "process"],
     "어떻게 하는지", "how it is done",
     "look for a procedure"),
    ("whether", ["되나", "돼?", "돼요", "가능", "할 수 있", "해도 되", "허용", "되는지",
                 "can i", "may i", "allowed", "is it ok", "whether", "permitted"],
     "해도 되는지", "whether it is allowed",
     "look for a rule"),
    ("what",    [], "무엇인지", "what it is", ""),
]

_HANGUL = re.compile(r"[가-힣ㄱ-ㆎ]")
_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힣]")
_ABSENCE = ("Nothing outside this list exists in RouteMind. This list is the grounds on which you may say "
            "something is absent — no smaller table is.")


def _pattern(term: str) -> re.Pattern:
    """How a term is found in a question. Latin on its own edges, CJK anywhere."""
    t = re.escape(term.strip())
    if _CJK.search(term): return re.compile(t, re.I)
    return re.compile(rf"(?<![A-Za-z0-9]){t}(?![A-Za-z0-9])", re.I)


def _find(term: str, q: str):
    m = _pattern(term).search(q)
    return m.group(0) if m else None


def names_of(nodes: list[dict], regions: list[dict]) -> list[tuple[str, dict]]:
    """The CNAME table: every string the map answers to, and what it stands for.

    Longest first, so "neo-us-east-1" is tried before "neo" and a question about the host is not
    read as a question about the service. Names under two characters are left out: a one-letter
    alias matches everything and resolves nothing.
    """
    out = []
    for n in nodes:
        seen = set()
        for s in [n.get("id"), n.get("name"), *_alias_names(n.get("aliases"))]:
            s = (s or "").strip()
            if len(s) < 2 or s.lower() in seen: continue
            seen.add(s.lower())
            out.append((s, {"kind": "node", "id": n["id"], "name": n.get("name") or n["id"],
                            "area": n.get("region"), "one_liner": n.get("one_liner") or ""}))
    for r in regions:
        for s in [r.get("dir"), r.get("key")]:
            s = (s or "").strip()
            if len(s) < 2: continue
            out.append((s, {"kind": "area", "id": r["dir"], "name": r.get("key") or r["dir"],
                            "area": r["dir"], "one_liner": r.get("use_when") or ""}))
    out.sort(key=lambda p: -len(p[0]))
    return out


def _alias_names(aliases) -> list[str]:
    return [a["name"] if isinstance(a, dict) else str(a) for a in (aliases or [])]


def ask_of(q: str) -> dict:
    """What the question wants about the thing it names. First kind whose word is present wins."""
    for kind, words, ko, en, hint in ASKS:
        for w in words:
            hit = _find(w, q)
            if hit: return {"kind": kind, "said": hit, "ko": ko, "en": en, "hint": hint}
    kind, _, ko, en, hint = ASKS[-1]
    return {"kind": kind, "said": None, "ko": ko, "en": en, "hint": hint}


def resolve(q: str, *, nodes: list[dict], edges: list[dict], regions: list[dict],
            ages: dict, revision: str, absence: str | None = None) -> dict:
    """The question, resolved. See the module docstring for what each part is and is not."""
    q = (q or "").strip()
    ko = bool(_HANGUL.search(q))
    by_id = {n["id"]: n for n in nodes}
    table = names_of(nodes, regions)

    # CNAME — literal matches, longest first, one entry per node. A node reached by two of its names
    # is still one node; the first (longest) string that found it is the one reported.
    found: dict[str, dict] = {}
    for term, what in table:
        if what["kind"] != "node": continue
        hit = _find(term, q)
        if not hit or what["id"] in found: continue
        found[what["id"]] = {"said": hit, "is": what["id"], "name": what["name"], "area": what["area"],
                             "via": "name" if hit.lower() == what["id"].lower() or hit.lower() == what["name"].lower() else "alias",
                             "one_liner": what["one_liner"]}
    # One hop along the map's own edges. The 2026-09-30 miss was exactly one hop: `bns` was named,
    # `neo` held the record, and an edge between them said so. Two hops is a graph walk, not a
    # resolution, and it would pull in half the map for any well-connected node.
    direct = list(found)
    for e in edges:
        a, b = e.get("from"), e.get("to")
        for src, dst in ((a, b), (b, a)):
            if src in direct and dst in by_id and dst not in found:
                n = by_id[dst]
                found[dst] = {"said": found[src]["said"], "is": dst, "name": n.get("name") or dst,
                              "area": n.get("region"), "via": f"edge {e.get('rel') or ''} from {src}".strip(),
                              "one_liner": n.get("one_liner") or ""}
    for r in found.values():
        r["fetch"] = f"/v1/nodes/{r['is']}"
        r["changed"] = (ages.get(r["is"]) or {}).get("changed")

    ask = ask_of(q)

    # Where to go first. For `latest` the newest `changed` leads, which is the whole reason the
    # column exists; otherwise what was named outranks what was reached by an edge.
    rows = list(found.values())
    if ask["kind"] == "latest":
        rows.sort(key=lambda r: (r.get("changed") or ""), reverse=True)
    else:
        rows.sort(key=lambda r: (r["via"] != "name" and r["via"] != "alias", r["is"]))

    # Hop 0, always. The one table absence may be claimed from, sent with every resolution so a
    # resolution cannot be had without it.
    areas = []
    for r in regions:
        rep = r.get("representative")
        a = ages.get(rep) or {}
        areas.append({"id": r.get("key") or r["dir"], "area": r["dir"], "use_when": r.get("use_when") or "",
                      "fetch": f"/v1/regions/{r['dir']}",
                      "route_since": a.get("route_since"), "changed": a.get("changed")})

    # The restatement: the question in the map's words, one line, for a person to disagree with.
    area_names = []
    for r in rows:
        if r["area"] and r["area"] not in area_names: area_names.append(r["area"])
    if rows:
        head = (", ".join(area_names) + (" 영역 — " if ko else " — ")) if area_names else ""
        restated = head + ", ".join(r["name"] for r in rows) + ": " + (ask["ko"] if ko else ask["en"])
    else:
        restated = ("맵이 아는 이름이 질문에 없음 — 영역 목록의 문장으로 고르거나, 여기에 없음" if ko else
                    "no name in this question is one the map knows — choose from the area list by its sentences, or it is not here")

    return {
        "q": q,
        "revision": revision,
        "resolved": bool(rows),
        "names": rows,
        "ask": ask,
        "restated": restated,
        "start": [r["fetch"] for r in rows],
        "areas": areas,
        "absence": absence or _ABSENCE,
        # TTL. A name resolution is good while the map is the map it was made against. An absence is
        # good for as long as it took to read it.
        "valid_while": revision,
        "cache": {"names": "while `revision` is unchanged", "absence": "never"},
    }
