"""Where a new document goes, decided by walking the routing table — the same walk a question takes.

A question is routed by reading one line per area at hop 0, choosing, then reading one line per
node on the way down. A document that is being added should find its place the same way: read the
lines, choose the row whose sentence covers it, descend, until the table you are looking at is the
one it belongs in. Not "scan the corpus and pick a likely spot" — that is retrieval wearing a
different hat, and it puts a document wherever the words happened to land. The walk puts it where
the map *says* such things go, and records every hop it took to get there, so the placement can be
read back and argued with.

Two outcomes at the top. Either a row at hop 0 covers it, and the walk goes down; or none does, and
the honest answer is "no area advertises this" — which is a request for a new area, not a place to
hide the document. Deeper down, "none of these" is ordinary: the document becomes a child of the
node whose table you are reading.

Then the second decision, which is the one a filing system does not have. The map advertises. Each
area's sentence at hop 0 is what the whole backbone — and, if exported, every peer — reads to decide
whether to come here. A new document may be something that sentence does not say. So after placing,
walk back **up** and ask at each ancestor: does your line already cover this? The first one that
does is where propagation stops — the same rule as route aggregation, where a prefix already inside
an advertised aggregate is not announced again. Every ancestor below that point gets a proposal to
widen its line. If nothing covers it all the way to hop 0, the area's own sentence is proposed, and
whether the area is exported is reported beside it — that last step is a separate decision and is
never taken here.

Every judgement in this file is a literal string found or not found, and every result names the
strings. "Covered" means a word from the document's name, line or aliases appears in the ancestor's
line. That is deliberately crude and deliberately visible: a person reading "vendor — found in the
area's sentence" can agree or not in a second, and a wrong call is corrected by editing one line.

Pure. The service hands it rows and lines; it touches nothing.
"""
import re

from service.resolve import _find

# Words that are in every sentence and say nothing about which one. Short on purpose: a term that
# should have been dropped shows up in the evidence where somebody can see it, which is better than a
# long list that quietly drops a word somebody meant.
STOP = {
    "the", "a", "an", "of", "to", "and", "or", "for", "in", "on", "at", "by", "is", "are", "be",
    "it", "its", "this", "that", "with", "from", "as", "was", "were", "what", "how", "when", "who",
    "which", "where", "whether", "not", "no", "yes", "do", "does", "did", "can", "may", "has", "have",
    "및", "또는", "그리고", "에서", "에게", "의", "를", "을", "는", "은", "이", "가", "와", "과", "에", "로",
    "으로", "하는", "한", "것", "수", "등", "때", "뭐", "무엇", "어떻게", "언제", "누가", "누구",
}
_SPLIT = re.compile(r"[\s,.;:·()\[\]\"'/|—–!?]+")
# "ATL에서" is one token to a split and two things to a reader: a Latin name and a Hangul particle.
# The name is what matches a line; the particle never does.
_LATIN_THEN_HANGUL = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_-]*)[가-힣]+$")


def _alias_names(aliases) -> list[str]:
    return [a["name"] if isinstance(a, dict) else str(a) for a in (aliases or [])]


def terms(doc: dict) -> list[str]:
    """The words of the document that could match a line: its name, its one_liner, its aliases.

    Not the body. A body is long and says many things; the name and the line are what the author
    chose to say it *is*, and that is what a routing sentence would mention. Aliases are included
    whole as well as split, because an alias is a name somebody actually uses.
    """
    out, seen = [], set()
    def add(s):
        s = s.strip()
        if len(s) < 2 or s.lower() in STOP or s.lower() in seen: return
        seen.add(s.lower()); out.append(s)
    for a in _alias_names(doc.get("aliases")): add(a)
    for field in ("name", "one_liner"):
        for tok in _SPLIT.split(str(doc.get(field) or "")):
            m = _LATIN_THEN_HANGUL.match(tok)
            add(m.group(1) if m else tok)
    return out


def evidence(doc: dict, line: str, names: list[str]) -> dict:
    """Which of the document's words appear in a row's line, and which name one of them is."""
    ts = terms(doc)
    in_line = [t for t in ts if line and _find(t, line)]
    in_names = [t for t in ts if any(_find(t, n) for n in names if n)]
    return {"terms": in_line, "names": in_names, "hits": len(set(in_line) | set(in_names))}


def table(doc: dict, rows: list[dict]) -> list[dict]:
    """The rows of one table, each with the evidence for choosing it. Order is the table's own —
    this is a table with a column added, not a ranking; every row is there to be read."""
    return [{**r, "evidence": evidence(doc, r.get("line") or "", r.get("names") or [])} for r in rows]


def coverage(doc: dict, line: str) -> dict:
    """Does an ancestor's line already say this? One word of the document's name, line or aliases
    found in it is enough to say yes — the line already brings a reader here for such things."""
    hits = [t for t in terms(doc) if line and _find(t, line)]
    return {"line": line or "", "hits": hits, "covered": bool(hits)}


def propagation(doc: dict, ancestors: list[dict]) -> dict:
    """How far up the new document has to be advertised.

    `ancestors` is innermost first: the node the document was placed under, then its parent, up to
    the area. Each is {"scope": "entity" | "bb", "id", "label", "line"}. The walk up stops at the
    first ancestor whose line covers the document — aggregation — and every ancestor below that gets
    a proposal to widen its line by the document's own one_liner, which is the sentence its author
    wrote for exactly this purpose. Proposals, not writes: a routing sentence changes through the
    queue, where somebody reads it.
    """
    proposals, stop = [], None
    for a in ancestors:
        c = coverage(doc, a.get("line") or "")
        if c["covered"]:
            stop = {"label": a["label"], "hits": c["hits"]}
            break
        after = (a.get("line") or "").strip()
        add = str(doc.get("one_liner") or doc.get("name") or "").strip()
        after = f"{after} · {add}" if after else add
        proposals.append({"scope": a["scope"], **({"entity": a["id"]} if a["scope"] == "entity" else {"region": a["id"]}),
                          "label": a["label"], "before": a.get("line") or "", "after": after,
                          "why": f"{doc.get('name')} was placed beneath this and the line did not say it"})
    return {"stop_at": stop, "proposals": proposals,
            "reaches_hop0": stop is None and any(a["scope"] == "bb" for a in ancestors)}
