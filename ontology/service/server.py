"""iris-ontology — HTTP API over the v2 data repository (SPEC-v2 §4).

  ONTOLOGY_DATA       the data git repository (default /data)
  ONTOLOGY_HARNESS    the review queue for routing changes (default: none → 501)
  ONTOLOGY_LLM_BASE_URL / ONTOLOGY_LLM_API_KEY / ONTOLOGY_LLM_MODEL  the ✨ Suggest buttons (absent → disabled)
  PORT                listen port (default 8100)

Reads serve the repository working tree. Writes go through Writer.transact: mutate → regenerate derived files →
validate → git commit. Vocabulary and kinds are not writable here — changing them is a Knowledge-approved change
to vocab.yaml (operator decision, 2026-09-07).

Retired 2026-10-07, all without a reader: the publish step (a checkout per commit for an agent runtime that
mounted it; agents here read this API), service fragments (`ONTOLOGY_SERVICES`, set by no install), the
legacy fragment directory, and the curator's sleep and observations (no caller anywhere).
"""
from __future__ import annotations
import datetime, json, os, re, sys, time, traceback, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.store import Store        # noqa: E402
from service.validate import validate, export_kinds  # noqa: E402
from service import ages  # noqa: E402
from service import derive as deriving  # noqa: E402
from service.write import Writer, WriteError, head, _dirty   # noqa: E402
from service import sessions                                 # noqa: E402
from service import overlays                                # noqa: E402
from service import walks                                   # noqa: E402
from service import curator                                 # noqa: E402
from service import change                                  # noqa: E402
from service import access                                  # noqa: E402

DATA = Path(os.environ.get("ONTOLOGY_DATA", "/data"))
# The enrolment key another RouteMind's circuit presents, once, to get a six-hour session for reading
# /v1/export. Unset means that whole surface answers 501 — which is the right default: letting another
# backbone read this one is a decision, not something an install drifts into. See docs/CIRCUIT.md.
PEER_TOKEN = (os.environ.get("ONTOLOGY_PEER_TOKEN") or "").strip()
# Where the record of cross-domain reads is kept. Unset means stderr only, which every install has
# without configuring anything — and stderr rotates away, and an audit that rotates away is not one.
ACCESS = (os.environ.get("ONTOLOGY_ACCESS") or "").strip() or None
OVERLAYS = Path(os.environ["ONTOLOGY_OVERLAYS"]) if os.environ.get("ONTOLOGY_OVERLAYS") else None
# The footprint — every walk, as it is walked (docs/FOOTPRINT.md). Unset → 501, like overlays.
WALKS = Path(os.environ["ONTOLOGY_WALKS"]) if os.environ.get("ONTOLOGY_WALKS") else None
PORT = int(os.environ.get("PORT", "8100"))
store = Store(DATA); writer = Writer(DATA)


def describe_file(name: str, content: str) -> str | None:
    """Write a new file's one-line description **by reading its body** (operator, 2026-09-10).

    That line goes into the routing table and is the only thing an agent sees when choosing the
    file. Left to whoever created it, the table fills with a dozen different registers. On failure it
    returns **None — it never invents one.**"""
    c = llm_client()
    if not c: return None
    SYSTEM = (
        "You read one document and write **the single line that will appear in a routing table**.\n"
        "A reader decides 'should I open this file' from that line and nothing else.\n"
        "Rules:\n"
        "- One line. No trailing period. Under 80 characters.\n"
        "- Say **what it contains**, not what it claims about itself.\n"
        "- Write nothing that is not in the body. If unsure, carry over its headings only.\n"
        "- Do not repeat the file name.\n"
        "- Output that one line only — no preamble, no greeting, no quotes."
    )
    try:
        out = c(SYSTEM, f"file name: {name}\n\n---\n{content[:8000]}")
    except Exception as e:
        _llm_failed(e); return None
    line = (out or "").strip().splitlines()[0].strip().strip('"').strip("'") if (out or "").strip() else ""
    return line[:200] or None


def suggest_node_id(name: str, kind: str, one_liner: str, region: str, taken: list[str]) -> str | None:
    """Make a node id from its name (operator, 2026-09-10).

    **An id is a permanent address** — agents call `/v1/nodes/<id>`,
    it is embedded in file addresses, and **there is no rename path.** It is also the one value a
    screen cannot produce: slugging a non-Latin name with a regex yields "" or, worse, something
    wrong but plausible — a name whose only ASCII is an embedded acronym slugs down to that acronym
    alone. **A wrong value is produced silently and cannot be undone.** Good ids are translations,
    and translation is not a job for a regex."""
    c = llm_client()
    if not c: return None
    SYSTEM = (
        "You render a name as an ASCII address. Once set it cannot change.\n"
        "**You are translating a name, not describing a thing.** A reader who knows the name must\n"
        "recognise the address as that same name.\n"
        "Rules:\n"
        "- Lowercase ASCII kebab-case, under 48 characters, digits allowed.\n"
        "- Carry the **name** across. Translate it where it is not Latin; keep it where it is.\n"
        "- Do **not** substitute what the thing does for what it is called. A node named `Parcels`\n"
        "  is `parcels`, never `tracking-system` — the second may be apt and is still the wrong\n"
        "  answer, because nobody typed it.\n"
        "- Do not repeat the area name. A node in the `cdn` area need not start with `cdn-`.\n"
        "- Use only widely understood abbreviations (db · svn · ui).\n"
        "- It must not collide with an id already taken.\n"
        "- Output the id alone — no explanation, no quotes."
    )
    # The one-liner is context for disambiguating a name, not material to build an id from; `kind` is
    # not sent at all, because a kind is a category and categories are what produced `tracking-system`.
    ask = (f"name: {name}\narea: {region}\nwhat it is (context only, do not name it after this): {one_liner}\n\n"
           f"ids already taken (must not collide):\n" + ", ".join(sorted(taken)))
    try: out = c(SYSTEM, ask)
    except Exception as e: _llm_failed(e); return None
    v = (out or "").strip().splitlines()[0].strip().strip('"').strip("'").lower() if (out or "").strip() else ""
    return v[:48] or None


def suggest_use_when(name: str, one_liner: str) -> str:
    """Draft the one line that decides whether an agent comes to this area at all.

    Of everything a person types when opening an area, this is the line that decides whether the area
    works. It is not a description — it is the condition under which a question belongs here, and the
    difference is invisible until an agent has seven areas to choose between and picks by it. People
    write a description here by default, because that is what every other field on the form is.

    Drafted, never applied: it comes back into an editable box. A sentence nobody read should not be
    the thing an agent routes on.
    """
    c = llm_client()
    if not c: raise WriteError(503, "drafting needs an LLM (ONTOLOGY_LLM_*)")
    SYSTEM = (
        "You write the one line that tells an agent when to choose an area of an ontology.\n"
        "It appears in a list of areas, and the agent picks exactly one by reading these lines.\n\n"
        "Rules:\n"
        "- Write the CONDITION, not a description. Not what the area is — what someone would be\n"
        "  asking when the answer is in here.\n"
        "- Concrete triggers, not categories: the questions themselves, separated by ' · '.\n"
        "- One line, under 120 characters, no trailing period.\n"
        "- Use only what the input says. Invent no capability the area has not claimed.\n"
        "- Output that line alone — no quotes, no preamble."
    )
    # A brand-new area has nothing written yet — the form that opens one asks for two things and
    # derives the rest. Handing the model an empty field next to
    # "invent no capability the area has not claimed" left it nothing to do but ask the caller for the
    # missing context, so say what is missing and what to do about it.
    known = [f"area name: {name}"]
    if one_liner and one_liner != name: known.append(f"what it is: {one_liner}")
    if len(known) == 1:
        known.append("Nothing else is known yet — this area is being opened now. Write the line from the "
                     "name alone: the questions someone with that name over the door would be asked.")
    ask = "\n".join(known)
    # 422 means "the model answered and the answer was unusable". A provider that refused is a
    # different fact with a different fix, so it does not borrow that code.
    try: out = (c(SYSTEM, ask) or "").strip().strip('"').splitlines()
    except Exception as e: raise WriteError(502, f"could not draft a line: {e}")
    # The prompt says "output that line alone — no quotes, no preamble", so more than one line back is
    # the model disobeying, and taking the first of them is how a preamble became the answer.
    lines = [l.strip() for l in out if l.strip()]
    line = lines[0] if lines else ""
    # An answer is not a draft just because it came back. The prompt asks for one line, under 120
    # characters, no trailing period — and forbids inventing anything the input did not claim. Given a
    # brand-new area, where the only input is a slug and the architecture row does not exist yet, a
    # good model obeys that last rule and asks the caller for the missing context instead. The screen
    # then wrote *"I need the architecture document content… Could you provide the row that describes
    # what it-support covers?"* straight into the field an agent routes on, and pressing Create would
    # have made that sentence the area's advertisement.
    #
    # So the shape the prompt asked for is checked, not just the presence of text. Refusing reaches
    # the person as "write the line yourself", which is the honest outcome when there was nothing to
    # draft from.
    if not line or len(lines) != 1 or line.endswith(("?", ":")) or len(line) > 240:
        raise WriteError(422, "nothing could be drafted from that — write the line yourself")
    return line[:300]


def route_draft(region: str, scope: str, changed: list | None) -> dict:
    """Compare **what this area holds** against **what its advertisement says**, and draft a change.

    `changed[]` is only a hint — the screen knows what was just made, not three things made
    yesterday and raised today. Working out what is missing is Knowledge's job.

    **If nothing is missing, the draft is empty.** Producing a proposal when nothing needs to change
    turns the queue into noise, and then nobody reads the queue."""
    r = next((x for x in store.regions() if x["dir"] == region or x["key"] == region.upper()), None)
    if not r: raise WriteError(404, f"region {region} not found")
    rep = store.node(r["representative"]) if r.get("representative") else None
    if not rep: raise WriteError(409, f"region {region}: no top representative, so there is nothing to advertise")
    scope = curator.SCOPE_ALIAS.get(scope, scope)
    field = curator.ROUTE_SCOPES.get(scope)
    if not field: raise WriteError(400, "scope must be as | bb")
    if scope not in DRAFTABLE:
        # Guarded on the scope, not on the field, because the prompt is chosen by scope: `peer` has a
        # field this recognised and no prompt, so it reached `WHAT[scope]` and came back as
        # `500 internal error`. And these three genuinely are not drafted. The other scopes revise a
        # sentence about what an area holds, which is in the ontology and can be read; who may see it
        # and what one named organisation should be told are decisions about people who are not.
        raise WriteError(400, f"scope {scope} is not drafted — the model can read what an area holds, "
                              f"not who is reading and what they should be told. Write it yourself")
    before = rep.get(field) or ""

    # What this area holds right now — the material to compare the advertisement against
    holds = [f"file {f['name']} — {f['description']}" for f in rep["files"]]
    holds += [f"node {c['name']} ({c['kind']}) — {c['one_liner']}" for c in store.children_of(rep["id"])]
    c = llm_client()
    if not c:
        raise WriteError(503, "route-draft needs an LLM (ONTOLOGY_LLM_*)")
    WHAT = DRAFT_PROMPTS[scope]
    SYSTEM = (
        f"You revise an area's advertisement. What you are editing is {WHAT}.\n"
        "The input is (1) the current sentence and (2) a list of what the area actually holds.\n"
        "Do this:\n"
        "1. Split what it holds into **what the sentence already says** and **what it does not**.\n"
        "2. If nothing is unsaid, leave `after` as the **empty string**. Do not edit for its own sake.\n"
        "3. Otherwise revise the sentence as little as possible to cover it, matching its register\n"
        "   and its length.\n"
        "4. Invent no facts. Use only words that appear in the list.\n\n"
        'Output exactly one JSON object: {"covered": [...], "uncovered": [...], "after": "...", "why": "..."}\n'
        "covered/uncovered hold only the names of things it holds. `why` is one or two lines on what was added."
    )
    ask = (f"area: {r['key']}\ncurrent sentence:\n{before or '(empty)'}\n\n"
           f"what it holds:\n" + "\n".join("- " + h for h in holds)
           + (f"\n\njust changed (hint): {', '.join(changed)}" if changed else ""))
    # This one parses JSON out of the answer, so it asks for JSON where the provider can be told.
    # Anthropic has no such field; its prompt already asks, which is the only mechanism there is.
    try: out = c(SYSTEM, ask, json_object=True)
    # The provider's own words, not just the exception class — "HTTP 401 invalid x-api-key" is the
    # whole answer, and a bare `LLMError` sends the reader looking in the wrong place.
    except Exception as e: raise WriteError(502, f"could not produce a draft: {e}")
    m = re.search(r"\{.*\}", out or "", re.S)
    if not m: raise WriteError(422, "the draft was not JSON")
    try: d = json.loads(m.group(0))
    except Exception: raise WriteError(422, "the draft JSON could not be parsed")
    after = str(d.get("after") or "").strip()
    return {"region": r["dir"], "scope": scope, "field": field, "before": before,
            "after_draft": after, "why": str(d.get("why") or "").strip(),
            "covered": [str(x) for x in (d.get("covered") or [])],
            "uncovered": [str(x) for x in (d.get("uncovered") or [])],
            "nothing_to_do": not after}


def one_liner_draft(nid: str) -> dict:
    """Draft the line an entity's **own row** shows in its parent's table.

    A different question from `route_draft`, which asks what an *area* should advertise by comparing
    the area's holdings against its representative's sentence. This one reads one entity's body and
    asks what makes it worth opening — and reads its **siblings' lines** as well, because a routing
    line is chosen from a list. A sentence that is accurate but says what the row above it already
    says has not helped anyone choose; being distinguishable is the whole job.

    Draft only. It never writes — the line goes through the queue, the same way an area's does
    (operator: no immediate-apply path for a routing line)."""
    n = store.node(nid)
    if not n: raise WriteError(404, f"node {nid} not found")
    body = (n.get("body") or "").strip()
    kids = store.children_of(nid)
    if not body and not kids:
        # Nothing to read it off. Inventing a line for an entity nobody has written is exactly the
        # noise the queue must not fill with.
        raise WriteError(409, f"{nid} has no document and holds nothing — write it first, then the line can describe it")
    parent = store.node(n["parent"]) if n.get("parent") else None
    siblings = [c for c in (store.children_of(parent["id"]) if parent else []) if c["id"] != nid]
    c = llm_client()
    if not c: raise WriteError(503, "one-liner-draft needs an LLM (ONTOLOGY_LLM_*)")
    SYSTEM = (
        "You write the one line that appears beside an entry in a routing table. A reader scans the\n"
        "table and picks one row. Your line is how they decide this row is the one.\n"
        "The input is (1) the current line, (2) what this entry actually says, (3) what it holds, and\n"
        "(4) the lines on the rows beside it.\n"
        "Do this:\n"
        "1. Say what a reader would come to this entry **for**, in its own words.\n"
        "2. Make it **distinguishable from the rows beside it**. If the current line already does\n"
        "   both, leave `after` as the empty string. Do not edit for its own sake.\n"
        "3. One line. No trailing period. Match the register and length of the neighbouring lines.\n"
        "4. Invent no facts. Use only what the input says.\n\n"
        'Output exactly one JSON object: {"after": "...", "why": "...", "distinguishes_from": [...]}\n'
        "`distinguishes_from` holds the ids of the neighbours the line is meant to be told apart from."
    )
    ask = (f"entry: {n['name']} ({n['kind']})\ncurrent line:\n{n.get('one_liner') or '(empty)'}\n\n"
           f"what it says:\n{body[:6000] or '(no document — it holds other entries)'}\n\n"
           + (f"what it holds:\n" + "\n".join(f"- {k['name']} — {k['one_liner']}" for k in kids) + "\n\n" if kids else "")
           + (f"rows beside it:\n" + "\n".join(f"- {sb['id']}: {sb['one_liner']}" for sb in siblings) if siblings
              else "rows beside it: (none — it is the only entry here)"))
    try: out = c(SYSTEM, ask, json_object=True)
    except Exception as e: raise WriteError(502, f"could not produce a draft: {e}")
    m = re.search(r"\{.*\}", out or "", re.S)
    if not m: raise WriteError(422, "the draft was not JSON")
    try: d = json.loads(m.group(0))
    except Exception: raise WriteError(422, "the draft JSON could not be parsed")
    after = str(d.get("after") or "").strip()
    return {"entity": nid, "region": n["region"], "scope": "entity", "field": "one_liner",
            "before": n.get("one_liner") or "", "after_draft": after,
            "why": str(d.get("why") or "").strip(),
            "distinguishes_from": [str(x) for x in (d.get("distinguishes_from") or [])],
            "nothing_to_do": not after}


def suggest_node_kind(name: str, one_liner: str, region: str, content: str = "") -> str | None:
    """Decide a node's `kind` (operator, 2026-09-10: "what relations may hold is the curator's job").

    `kind` is **never seen by an agent** — it does not go into a prompt. What uses it is **the
    validator's edge rules** (`edge_rules` in vocab.yaml). So what a kind decides is "which relations
    this node may take part in", and relations are the curator's territory.

    Unlike `id` it **can be corrected later** (it is in update_node's allow list). But getting it
    wrong is quiet: someone drawing a relation months later is refused, and nothing at that moment
    points back at this node's kind. So the response carries `kind_generated` — **a chance to fix it
    right after it was made**."""
    c = llm_client()
    if not c: return None
    kinds = store.vocab().get("kinds") or []
    table = "\n".join(f"- {k['id'] if isinstance(k, dict) else k}: "
                      f"{(k.get('desc', '') if isinstance(k, dict) else '')}" for k in kinds)
    SYSTEM = (
        "You pick one **kind** for an ontology node, from the list below.\n"
        "A kind decides which relations the node may take part in — it is a **classification**, not a\n"
        "description.\n\n"
        f"These are the only choices:\n{table}\n\n"
        "Rules:\n"
        "- Output exactly one value from the list, verbatim. Never invent one.\n"
        "- That value alone — no explanation, no quotes, nothing around it.\n"
        "- If unsure, follow the **primary nature** described by the one-liner."
    )
    ask = f"name: {name}\narea: {region}\none-liner: {one_liner}" + (f"\n\ndocument:\n{content[:3000]}" if content else "")
    try: out = c(SYSTEM, ask)
    except Exception as e: _llm_failed(e); return None
    v = (out or "").strip().splitlines()[0].strip().strip('"').strip("'") if (out or "").strip() else ""
    valid = {(k["id"] if isinstance(k, dict) else k) for k in kinds}
    return v if v in valid else None          # outside the list is a failure — it never invents one


# `llm_configured()`, not `all(LLM.values())`. They differ on one case and it matters: a provider
# this build does not know leaves the three values set, so the old test said "there is an LLM", the
# call then found no client and returned None, and the writer reported 422 — "nothing could be drawn
# from the body" — for what is a misconfiguration. Same three values, two answers, and the wrong one
# sent the reader to look at their document.
writer.suggest_kind = lambda **kw: suggest_node_kind(**kw) if llm_configured() else None
writer.suggest_id = lambda **kw: suggest_node_id(**kw) if llm_configured() else None
writer.suggest_id_configured = lambda: llm_configured()


HARNESS = Path(os.environ["ONTOLOGY_HARNESS"]) if os.environ.get("ONTOLOGY_HARNESS") else None


LLM = {k: os.environ.get(f"ONTOLOGY_LLM_{k}") for k in ("BASE_URL", "API_KEY", "MODEL")}
# `litellm` keeps what an existing install already does, so an upgrade changes nothing until someone
# asks it to. The two numbers are the operator's; `response_format` is not — see `chat_client`.
LLM_PROVIDER = (os.environ.get("ONTOLOGY_LLM_PROVIDER") or "litellm").strip().lower()


def _llm_number(name, default, cast):
    raw = os.environ.get(f"ONTOLOGY_LLM_{name}")
    try: return cast(raw) if raw not in (None, "") else default
    except ValueError:
        # A number nobody can parse is not a reason to run with a silent default — say it once, at
        # startup, where the person who set it will see it.
        print(f"ONTOLOGY_LLM_{name}={raw!r} is not a number — using {default}", flush=True)
        return default


LLM_MAX_TOKENS = _llm_number("MAX_TOKENS", 1024, int)
LLM_TEMPERATURE = _llm_number("TEMPERATURE", 0.0, float)


def _llm_failed(e: Exception) -> None:
    """These callers answer `None`, and the writer turns that into "could not be generated —
    nothing could be drawn from the body". A wrong key or a provider mismatch is a different fact
    and deserves a different answer; that conflation is older than three providers and is not fixed
    here. What is fixed is that the reason stops disappearing — it goes to the log, where the person
    who just changed a setting will look."""
    print(f"LLM call failed: {e}", flush=True)


def llm_configured() -> bool:
    return all(LLM.values()) and LLM_PROVIDER in curator.PROVIDERS


def llm_client():
    if not llm_configured(): return None
    return curator.chat_client(LLM_PROVIDER, LLM["BASE_URL"], LLM["API_KEY"], LLM["MODEL"],
                               max_tokens=LLM_MAX_TOKENS, temperature=LLM_TEMPERATURE)


def cstore():
    if not HARNESS: raise WriteError(501, "ONTOLOGY_HARNESS is not configured")
    return curator.CuratorStore(HARNESS / "curator")


def apply_proposal(p: dict, actor: str):
    """Accepting a proposal runs the ordinary write path — never a side door.

    Only routing changes a person filed (`route`) are applied. The machine-made kinds — `promote`,
    `repin` and the rest — came from the curator's sleep, retired 2026-10-07 with no caller; one still
    sitting in a queue is refused here with a sentence, and can be rejected."""
    if p["type"] == "change":
        # A change set queued whole (docs/CHANGE.md). Its `base` check still holds at accept: what
        # moved under it since is handed back as stale, not overwritten.
        return change.apply(writer, p.get("set") or {}, actor, proposed_by=p.get("submitted_by") or "")
    if p["type"] != "route":
        return {"ok": False, "error": f"a {p['type']!r} proposal came from the retired curator sleep and is no longer applied — reject it"}
    if p["type"] == "route":
        # Approval happens later than drafting. If the value moved in between, this does not overwrite
        # it — it **hands the current value back**.
        scope, region = p["scope"], p["region"]
        if scope == "entity":
            # The same conflict rule as an area's line, for the same reason: approval happens later
            # than drafting, and if the sentence moved in between this hands the current one back
            # rather than overwriting what someone else decided.
            n = store.node(p.get("entity") or "")
            if not n: return {"ok": False, "error": f"{p.get('entity')} no longer exists", "reason": "target_missing", "code": 409}
            cur = n.get("one_liner") or ""
            if p.get("before") and cur != p["before"]:
                return {"ok": False, "error": "conflict", "code": 409, "field": "one_liner",
                        "current": cur, "submitted_before": p["before"]}
            return writer.update_node(n["id"], {"one_liner": p["after"]}, actor,
                                      note=f"one_liner, proposal {p['id']}" + (f": {p['why']}" if p.get("why") else ""))
        if scope == "audience":
            # Who an area crossed to, by name — named peers went with standing links on 2026-10-08.
            return {"ok": False, "error": "an `audience` proposal names peers, which no longer exist — reject it"}
        if scope == "core":
            # CORE.md is no longer read (2026-10-07); a proposal to change one of its rows that is
            # still queued has nothing to change.
            return {"ok": False, "error": "a `core` proposal changes a CORE.md row, which is no longer read — reject it"}
        r = next((x for x in store.regions() if x["dir"] == region or x["key"] == region.upper()), None)
        if not r or not r.get("representative"): return {"ok": False, "error": f"area {region} no longer exists", "reason": "target_missing", "code": 409}
        rep = store.node(r["representative"])
        # From the table, not from a two-way if. It read `"one_liner" if scope == "as" else "use_when"`,
        # which is correct for exactly the two scopes that existed and writes the wrong field for any
        # third — a `peer` proposal would have silently overwritten the area's own `use_when`.
        field = curator.ROUTE_SCOPES.get(curator.SCOPE_ALIAS.get(scope, scope))
        if not field: return {"ok": False, "error": f"unknown route scope {scope!r}"}
        # A queue proposal carries a sentence, and one of these fields is a list. Rendered the same
        # way on both sides of the comparison, or an audience would conflict with itself the moment
        # anybody submitted a second one.
        # A mapping field is edited one key at a time: the proposal names the peer, and what it
        # replaces is that peer's line and nobody else's. Comparing against the whole map would make
        # every override conflict with every other one, which is having no conflict check at all once
        # two people are working. Which fields those are is declared in curator.MAPPING_FIELDS and not
        # read off the current value — an empty mapping and an unset field look identical from here,
        # and deciding by the value means the *first* override of an area silently writes nothing.
        if field in curator.MAPPING_FIELDS:
            merged = dict(rep.get(field) or {})
            cur = merged.get(p.get("peer") or "", "")
            if p["after"]: merged[p["peer"]] = p["after"]
            else: merged.pop(p.get("peer") or "", None)
            after = merged
        else:
            cur, after = (rep.get(field) or ""), p["after"]
            if isinstance(cur, list): cur = ", ".join(cur)
            # A yes/no field against a proposal, which carries sentences. The stored value is a
            # boolean and `before` is the word somebody saw on screen; comparing them directly is a
            # conflict on every withdrawal, because `"yes" != True` always. Both sides become the
            # word here, so the comparison is between what was shown and what is there.
            if isinstance(rep.get(field), bool) or field in curator.BOOL_FIELDS:
                cur = "yes" if rep.get(field) else "no"
                after = "yes" if str(p["after"]).strip().lower() in ("yes", "true", "on", "1") else "no"
        if p.get("before") and cur != p["before"]:
            return {"ok": False, "error": "conflict", "code": 409, "field": field,
                    "current": cur, "submitted_before": p["before"]}
        what = (f"export {after}" if field == "export" else field)
        return writer.update_node(rep["id"], {field: after}, actor,
                                  note=f"{what}, proposal {p['id']}" + (f": {p['why']}" if p.get("why") else ""))
    return None


# `_advert_file` retired (2026-09-11). It advertised a file at `/v1/nodes/<id>/files/<name>` — a
# second address for something that now has its own. Every row goes through `_advert_child`.


# Internal bookkeeping, kept out of responses. `path` is the repository path itself; `present_files`
# are file names the API does not serve; `file_scopes` is a map of names with no addresses — scope
# moved onto the file's own row. On a node, `dir` is a character-for-character duplicate of `id`. An
# area's `dir` is different: that one is a name, and consumers read it.
_NODE_INTERNAL = ("path", "dir", "present_files", "file_scopes", "holds", "files")


_overlay_store = None


_walk_store = None


def wstore():
    """The walk record, when `ONTOLOGY_WALKS` is set. Settings mirror the overlay store's."""
    global _walk_store
    if not WALKS: raise WriteError(501, "ONTOLOGY_WALKS is not configured — the footprint is off")
    if _walk_store is None:
        _walk_store = walks.WalkStore(WALKS,
                                      keep_hours=float(os.environ.get("ONTOLOGY_WALK_KEEP_HOURS", "6")),
                                      open_hours=float(os.environ.get("ONTOLOGY_WALK_OPEN_HOURS", "1")))
    return _walk_store


def ostore():
    global _overlay_store
    if _overlay_store is None:
        _overlay_store = overlays.OverlayStore(
            OVERLAYS,
            members_max=int(os.environ.get("ONTOLOGY_OVERLAY_MEMBERS", "8")),
            rows_max=int(os.environ.get("ONTOLOGY_OVERLAY_ROWS", "120")),
            open_hours=float(os.environ.get("ONTOLOGY_OVERLAY_OPEN_HOURS", "24")),
            keep_days=float(os.environ.get("ONTOLOGY_OVERLAY_KEEP_DAYS", "30")))
    return _overlay_store


def overlay_resolve(addr: str):
    """What an overlay address points at, or None.

    **This checks that the address resolves, not that the ontology ever printed it.** Nothing records
    what was printed, so a guard phrased that way would claim more than it can do — and "never
    printed" and "does not resolve" are different facts that must not end up as one value. What this
    buys is still worth having: an assembled address that points at nothing is refused, with the
    sentence that says where addresses come from."""
    parts = [x for x in str(addr or "").strip("/").split("/") if x]
    if parts[:1] != ["v1"]: return None
    parts = parts[1:]
    if len(parts) == 2 and parts[0] == "regions":
        r = next((x for x in store.regions() if x["dir"] == parts[1]), None)
        return {"kind": "area", "region": r} if r else None
    if len(parts) == 2 and parts[0] == "nodes":
        n = store.node(parts[1])
        return {"kind": "entity", "node": n} if n else None
    if len(parts) == 3 and parts[0] == "nodes" and parts[2] == "body":
        n = store.node(parts[1])
        # A document address for an entity nobody has written points at a 404. Letting it into an
        # overlay would put a row in the table that cannot be read.
        return {"kind": "document", "node": n} if n and (n.get("body") or "").strip() else None
    return None


def overlay_rows_of(addr: str) -> int:
    """How many rows one member would bring. The store owns both caps and asks this for the one it
    cannot count on its own — how big an address is, is a question about the ontology."""
    got = overlay_resolve(addr)
    if not got: return 0
    if got["kind"] == "document": return 1
    if got["kind"] == "entity": return len(store.children_of(got["node"]["id"]))
    r = got["region"]
    return len(store.children_of(r["representative"])) if r.get("representative") else 0


def overlay_table(ov: dict) -> list[dict]:
    """The overlay's table: each member's own rows, one level down, under its own heading.

    One level, not the subtree — an overlay is where to look next, and an agent that asked to narrow
    should not be handed everything. A document contributes **itself** as a row, because there is
    nothing under it and the row is what an agent picks.

    Rows are returned, never rendered. `_table()` in the MCP is the renderer and the absence footer
    lives there; a second renderer here would drift from it the first time either changed."""
    out = []
    for m in ov["members"]:
        got = overlay_resolve(m["address"])
        if not got:
            # The ontology moved under a live overlay. Say so as a section rather than dropping it:
            # a member that quietly vanishes makes the table read as if it was never chosen.
            out.append({"member": m["address"], "why": m["why"], "title": m["address"],
                        "gone": True, "rows": []})
            continue
        if got["kind"] == "area":
            r = got["region"]; rep = store.node(r["representative"]) if r.get("representative") else None
            rows = [_advert_child(c) for c in advertised(r["representative"])] if rep else []
            out.append({"member": m["address"], "why": m["why"], "title": r.get("title") or r["dir"], "rows": rows})
        elif got["kind"] == "entity":
            n = got["node"]
            out.append({"member": m["address"], "why": m["why"], "title": n["name"],
                        "rows": [_advert_child(c) for c in advertised(n["id"])]})
        else:
            n = got["node"]
            out.append({"member": m["address"], "why": m["why"], "title": n["name"],
                        "rows": [_advert_child(n)]})
    return out


def overlay_out(ov: dict) -> dict:
    sections = overlay_table(ov)
    return {**ov, "sections": sections, "rows": sum(len(x["rows"]) for x in sections),
            # The renderer decides how to print it; what it must not do is leave it off. An overlay
            # read as an inventory is the one way this feature becomes a lie.
            "absence": "Not finding it here means go back to hop 0 — it does not mean it does not exist."}


def advertised(node_id: str) -> list[dict]:
    """What a caller is told this thing holds — its children, minus the drafts.

    `status: draft` was how the curator's sleep wrote something a person had not accepted yet —
    visible to people, invisible to an agent. The sleep is retired (2026-10-07) and nothing writes a
    draft now, but a repository may still hold one, and it must stay out of an agent's table.

    That promise was once not kept. `derive.py` drops drafts from `regions.json`, but every advertised listing here
    was built straight from `store.children_of`, which filters nothing — so a draft appeared in the
    area table an agent is handed, and the curator's unreviewed writing came back as evidence, which
    is the one thing the invariant exists to prevent.

    Filtering belongs here rather than in `store.children_of`: deletion walks the children to take a
    subtree with it, and validation counts them against the budget. Both have to see a draft.
    """
    return [c for c in store.children_of(node_id) if c.get("status") != "draft"]


def _advert_child(c: dict) -> dict:
    """The type comes from **what you get when you call it**, not from where it sits.

    When `type` was introduced, a constant was written here instead — which only restated "it is in
    children[]", the very thing the field was meant to replace. Not one of the 41 children had two
    files or any children of its own, so all 41 were falsely typed as something to descend into. The
    model was told 41 times to go deeper, and each time found a one-row table.

    The version after that guessed from counts — one file and no children meant a leaf — because the
    two questions that decide it were not fields. They are now, and there are **three** answers, not
    two: a table to descend into, a document to read, and an entity nobody has written yet. Forcing
    the third into `data` advertises a document that is not there, which is the same error as
    before, pointed the other way."""
    kids = store.children_of(c["id"])
    has_body = bool((c.get("body") or "").strip())
    kind = "dr" if kids else ("data" if has_body else "empty")
    # Two times, because they answer different questions and one number cannot do both. A route laid
    # down in 2023 whose document was rewritten last week is fresh; the same route whose document has
    # not moved in three years is the one worth asking about. Read from git rather than stored — see
    # ages.py. Absent when there is no history to read, and absent means *not known*, never new.
    age = ages.of(DATA, head(DATA)).get(c["id"]) or {}
    row = {"id": c["id"], "name": c["name"], "kind": c["kind"], "one_liner": c["one_liner"],
           "type": kind, "has_body": has_body, "children": len(kids),
           **({"route_since": age["route_since"]} if age.get("route_since") else {}),
           **({"changed": age["changed"]} if age.get("changed") else {}),
           # The row carries the call that answers it. A document is not read at the address that
           # lists a table — the two verbs need two addresses, or "read" has to call "table".
           "fetch": f"/v1/nodes/{c['id']}/body" if kind == "data" else f"/v1/nodes/{c['id']}"}
    if kids: row.update({"representative": c.get("role") == "representative",
                         "expands_in": c.get("expands_in")})
    return row


class Handler(BaseHTTPRequestHandler):
    server_version = "iris-ontology/0.3"

    # ---- plumbing ----
    # Set for the duration of an export read. `_export` answers the last two of its paths by
    # delegating to the ordinary reader, which is what keeps one shape of answer on both surfaces —
    # but that reader prints local addresses (`/v1/nodes/x`), and a peer following one of those
    # resolves it against **its own** ontology. With ids that collide it does not even fail: it
    # silently reads a different node with the same name. So every address leaving on this surface is
    # moved onto it, once, here, where nothing can route around it.
    _as_peer = False
    # Set for the length of one read of the export surface, and cleared by the answer. Recording in
    # `_send` rather than at each `return` covers the exits this function has today and the ones
    # somebody adds next year — the same argument that made the export surface a separate surface
    # instead of the ordinary one behind a check.
    _access = None

    def _send(self, code: int, payload, ctype="application/json; charset=utf-8"):
        if self._access is not None:
            a, self._access = self._access, None
            why = None
            if code >= 400 and isinstance(payload, dict):
                why = payload.get("reason") or (payload.get("error") or "")[:120]
            access.record(ACCESS, path=a["path"], peer=a.get("peer"), reader=a.get("reader"),
                          outcome=("served" if 200 <= code < 300 else "refused"), reason=why,
                          size=(len(json.dumps(payload, ensure_ascii=False)) if isinstance(payload, (dict, list))
                                else len(payload or "")))
        if self._as_peer and isinstance(payload, dict):
            # One place, for both of the things a peer's answer needs doing to it. Doing either of
            # them at the call sites would mean being right at every call site, and the export
            # surface has four; the argument is the same one that made it a separate surface rather
            # than the ordinary one behind a check.
            payload = _drop_kinds(payload, _denied_kinds())
            payload = _to_export(payload)
        body = payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=1).encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*"); self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Actor"); self.end_headers(); self.wfile.write(body)

    def _err(self, status, msg, details=None, reason=None, data=None):
        """`error` is the sentence; `reason` and `values` are the same refusal as something a screen
        can translate. The sentence is always sent and is always the whole answer on its own — an
        agent, a `curl` and any client that does not know a reason read exactly what they read
        before. Only refusals a person meets carry one; see WriteError in write.py.

        The parameter was called `code`, which was the HTTP status. Adding a second, different thing
        also called a code to the same function is how the wrong one ends up in the wrong field."""
        self._send(status, {"error": msg,
                            **({"details": details} if details else {}),
                            **({"reason": reason} if reason else {}),
                            **({"values": data} if data else {})})

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if not raw: return {}
        if self.headers.get("Content-Type", "").startswith("text/"): return {"content": raw.decode("utf-8")}
        try: return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError: raise WriteError(400, "body must be JSON")

    def _actor(self):
        """The name that goes on the commit. Percent-decoded: HTTP headers are latin-1, so a name that
        is not ASCII cannot be sent raw — it arrives as mojibake or the send fails outright. Decoding
        is backward-compatible: a plain ASCII name has nothing to decode."""
        raw = (self.headers.get("X-Actor") or "").strip()
        try: name = unquote(raw, errors="strict").strip()
        except Exception: name = ""
        return name[:64] or "web"

    def log_message(self, fmt, *args): sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    def _route(self, method):
        p = unquote(urlparse(self.path).path).rstrip("/") or "/"
        parts = [x for x in p.split("/") if x]
        try:
            if method == "OPTIONS": return self._send(204, "")
            # `llm` says whether this install can derive an id, a kind and a description from a name.
            # Without it those must be typed, and a screen that does not know which mode it is in either
            # asks for fields nobody should fill or hides fields without which nothing can be created.
            if p == "/healthz":
                # `writable` is the state where everything still reads and nothing can be written: the
                # data repository has uncommitted changes, so every write is refused to avoid committing
                # someone's half-finished hand edit along with it. That is correct and it is invisible —
                # a person meets it as one failed save, with a sentence about git. The screen shows it.
                # While a write holds the repository its files are mid-change by design: that is not
                # "uncommitted changes, commit or revert them", which the screen said during every write
                # on a large map (2026-10-10). Busy is reported as busy, and the tree is judged after.
                dirty, writing = "", False
                from service.write import _lock as _wlock
                if _wlock.acquire(blocking=False):
                    try: dirty = _dirty(DATA)
                    except Exception: dirty = ""
                    finally: _wlock.release()
                else:
                    writing = True
                # A data directory this process cannot write is not writable, whatever git says.
                can_write = os.access(DATA, os.W_OK) and os.access(DATA / "regions", os.W_OK)
                why_not = "the data directory cannot be written by this container — check KNOWLEDGE_UID and the mount"
                # Boot always leaves a commit, so no HEAD means the directory was swapped underneath a
                # running service — a backup restored with `rm -rf data/repo; cp -a …` — and the mount
                # still points at the deleted one. That answered `writable: true` (QA, 2026-10-10).
                hd = head(DATA)
                if hd is None:
                    can_write = False
                    why_not = ("the data directory has no git history — if it was replaced while this was running, "
                               "restart it: docker compose restart ontology")
                return self._send(200, {"ok": True, "data": str(DATA), "head": hd,
                                        # `llm` said only "something is configured". With three
                                        # providers that is not enough: a build that does not know
                                        # the provider a person set would ignore it silently, and
                                        # the setting would be dead with nothing to show for it.
                                        # `llm_provider` is what this build will actually use, and
                                        # it is null when the configured one is not one it knows.
                                        "llm": llm_configured(),
                                        "llm_provider": LLM_PROVIDER if LLM_PROVIDER in curator.PROVIDERS else None,
                                        "llm_providers": list(curator.PROVIDERS),
                                        "llm_max_tokens": LLM_MAX_TOKENS, "llm_temperature": LLM_TEMPERATURE,
                                        "writable": (not dirty) and can_write, "uncommitted": dirty, "writing": writing,
                                        **({} if can_write else {"unwritable": why_not}),
                                        # Whether the repository validates, and the first reasons it
                                        # does not. Before this the only place that fact existed was
                                        # one line in the startup log, and a server that had just
                                        # said `valid=False` answered every health check "ok".
                                        **_health_valid()})
            if parts[:1] != ["v1"]: return self._err(404, "unknown path")
            parts = parts[1:]
            # Before anything else, and read-only. A circuit reads; writes go to the backbone that owns
            # the area, through its own screen and its own review queue.
            if parts[:1] == ["export"]:
                if method != "GET": return self._err(405, "the export surface is read-only — write to the backbone that owns it")
                return self._export(parts[1:])
            # Not a write and not a read: the caller trades the enrolment key for a session to read
            # with. It changes nothing anybody can read — only for how long the caller may keep reading.
            if parts == ["peers", "token"]:
                if method != "POST": return self._err(405, "POST the enrolment key to get a session")
                return self._peer_token()
            # One consistent view of the tree per read. Without it a single answer could carry
            # `regions.json` from before a write and an entity from after it — a routing table that
            # never existed. The lock is held only while the snapshot loads, so the peer fetches
            # further down this path cannot stall a write behind somebody else's machine.
            if method == "GET":
                try:
                    with store.snapshot(): return self._get(parts)
                except TimeoutError as e:
                    return self._err(503, str(e), reason="repository_busy")
            return self._write(method, parts)
        except WriteError as e:
            if e.status == 200: return self._send(200, {"ok": True, "message": str(e)})
            return self._err(e.status, str(e), e.details, reason=e.code, data=e.data)
        except FileNotFoundError as e: return self._err(404, str(e))
        except Exception:
            traceback.print_exc(); return self._err(500, "internal error")

    def do_GET(self): self._route("GET")
    def do_POST(self): self._route("POST")
    def do_PUT(self): self._route("PUT")
    def do_PATCH(self): self._route("PATCH")
    def do_DELETE(self): self._route("DELETE")
    def do_OPTIONS(self): self._route("OPTIONS")

    def _reader(self) -> str:
        """Where a circuit's request came from: the first address the web relay forwarded, else the
        socket's own (which, behind the relay, is the relay)."""
        fwd = (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
        return fwd or (self.client_address[0] if self.client_address else "?")

    def _peer_token(self):
        """Trade the enrolment key for a session token. The only thing the enrolment key opens.

        The secret in `.env` used to be presented on every read, so it was in every request, every
        proxy log and every transcript, and it never expired. Now it buys six hours and nothing else
        — so the long-lived secret is used about four times a day per link instead of thousands, and
        what does leak off the read path stops being worth anything by the end of the shift.

        A session is in memory, so a restart revokes every one of them. Clients re-mint on a 401,
        which makes that the cheapest revocation there is.
        """
        token = self.headers.get("X-Peer-Token") or ""
        # Recorded like a read, refusals above all: a wrong key tried here is the probe that matters
        # most, and it reached only the HTTP log until 2026-10-10.
        self._access = {"path": "/v1/peers/token", "peer": None, "reader": self._reader()}
        if not PEER_TOKEN:
            return self._err(501, "this backbone lets nobody read it — set KNOWLEDGE_CIRCUIT_TOKEN in its .env (ONTOLOGY_PEER_TOKEN inside the container) to allow a circuit")
        # The enrolment key only. A session token cannot mint another: a leaked session would
        # otherwise renew itself for ever and the six hours would bound nothing.
        if not sessions.same_secret(token, PEER_TOKEN):
            return self._err(401, "enrolment key missing or wrong")
        session, ttl = sessions.mint()
        return self._send(200, {"token": session, "expires_in": ttl, "token_type": "session"})

    # ---- what crosses a link ----
    def _export(self, parts):
        """The only surface another backbone can read — through a circuit. See docs/CIRCUIT.md.

        **It is a separate surface, not the ordinary one behind a check.** An area crosses only by
        somebody setting `export` on it, and every handler here starts from that set — so there is no
        path through this code, and no bug in a token check, that can serve an area nobody decided to
        share. A filter applied on the way out would have to be right every time; a surface built from
        the exported set is right by construction.

        The line a reader sees is `use_when` — the same one this backbone routes on (operator,
        2026-09-29: one sentence). What crosses is still a decision — `export` — and it still goes
        through the review queue.

        Until 2026-10-08 an area could also name an audience (`export_to`) — the named peers of
        `peers.yaml` it would cross to. Named peers went with standing links; every reader now presents
        the one enrolment key, so an audience could name nobody it could tell apart, and it is ignored.
        """
        # Before the door, so a wrong token is recorded too. A refused read is the one that matters:
        # a run of refusals is the only signal there is that the surface is being probed.
        # Who: the address the request came from (the web relay forwards it) and which session it
        # carried, as a short hash — every reader holds the same key, so the session is the one thing
        # that tells two of them apart. "?" for both until 2026-10-10.
        self._access = {"path": urlparse(self.path).path, "reader": self._reader(),
                        "peer": sessions.tag(self.headers.get("X-Peer-Token") or "")}
        if not PEER_TOKEN:
            return self._err(501, "this backbone lets nobody read it — set KNOWLEDGE_CIRCUIT_TOKEN in its .env (ONTOLOGY_PEER_TOKEN inside the container) to allow a circuit")
        # A session token, and not the enrolment key. The enrolment key opens `/v1/peers/token` and
        # nothing else — if it still worked here, the read path would still carry a secret that never
        # expires and the six hours would be decoration.
        if not sessions.valid(self.headers.get("X-Peer-Token") or ""):
            return self._err(401, "session token missing, wrong or expired — POST /v1/peers/token "
                                  "with the enrolment key to get one (they last six hours)")

        rj = _regions_live()
        shared = {r["source"].replace("_", "-"): r for r in rj.get("regions", []) if r.get("export")}
        # An area whose **face** is of a kind that does not cross, does not cross. Its entries are
        # that representative's children, so offering the area would offer a table every row of which
        # is refused — and an empty table is the one answer a listing must never give, because it
        # reads as "there is nothing here" rather than "you may not see it".
        _denied = _denied_kinds()
        if _denied:
            def _face_crosses(r):
                rep = store.node(r.get("representative") or "")
                return not rep or str(rep.get("kind") or "") not in _denied
            shared = {k: r for k, r in shared.items() if _face_crosses(r)}
        # The revision the reader is told about. It is what makes staleness visible on the other side:
        # git already numbers every state this repository has been in, so nobody needs a clock.
        rev = head(DATA)

        if parts == ["regions"]:
            return self._send(200, {"revision": rev, "schema": rj.get("schema"), "regions": [
                {"id": r["id"], "source": r["source"], "title": r["title"],
                 "use_when": (r.get("use_when") or "").strip(), "representative": r.get("representative"),
                 "fetch": f"/v1/export/regions/{src}"}
                for src, r in sorted(shared.items())]})

        if len(parts) == 2 and parts[0] == "regions":
            if parts[1] not in shared: return self._err(404, f"no exported area {parts[1]}")
            self._as_peer = True
            return self._get(["regions", parts[1]])

        if len(parts) >= 2 and parts[0] == "nodes":
            n = store.node(parts[1])
            # 404 and not 403: whether this backbone holds a thing it has not shared is itself
            # something the reader has no business learning. The two answers must be indistinguishable.
            if not n or (n.get("region") or "") not in {dir_of(r["source"]) for r in shared.values()}:
                return self._err(404, f"no exported node {parts[1]}")
            # A draft is not in the area's advertised list, and across a circuit that list is the only
            # access control there is. Locally the same node answers by address on purpose — the
            # reader there is the owner — but a reader elsewhere cannot be told "this is hidden" and
            # then be served it by anyone who kept yesterday's address.
            if _draft_anywhere(n):
                return self._err(404, f"no exported node {parts[1]}")
            # And the kind. `vocab.yaml` says which sorts of thing stay inside this backbone, and an
            # entity under one that does not cross does not cross either. Same 404 as everything else.
            if _kind_denied_anywhere(n, _denied_kinds()):
                return self._err(404, f"no exported node {parts[1]}")
            self._as_peer = True
            return self._get(parts)

        return self._err(404, "unknown export path")

    # ---- reads ----
    def _get(self, parts):
        if parts == ["revision"]: return self._send(200, {"head": head(DATA)})
        if parts == ["vocab"]: return self._send(200, store.vocab())
        if parts == ["graph"]: g = store.graph(); g["revision"] = head(DATA); return self._send(200, g)
        if parts == ["regions"]:
            # A listing is an advertisement too. `path` and `nodes` stay in regions.json but are
            # **not emitted**: publish a path and someone builds an address out of it (someone did),
            # and `nodes` is internal bookkeeping the validator uses to catch drift against the
            # directory, not something a caller should act on. There is one way to go: `fetch`.
            rj = _regions_live()
            # An area's age is its representative's: that node is the area's face, and its two
            # times are what somebody choosing between areas at hop 0 is actually choosing on.
            _ages = ages.of(DATA, head(DATA))
            def _area_age(rep_id):
                return {k: v for k, v in (_ages.get(rep_id) or {}).items() if v}
            mine = [
                {"id": r["id"], "source": r["source"], "title": r["title"],
                 "use_when": r.get("use_when", ""), "representative": r.get("representative"),
                 **_area_age(r.get("representative")),
                 "fetch": f"/v1/regions/{r['source'].replace('_', '-')}"}
                for r in rj.get("regions", [])]
            return self._send(200, {"revision": head(DATA), "schema": rj.get("schema"), "regions": mine})
        if len(parts) == 2 and parts[0] == "regions":
            # SPEC-v2 §1.1 — an area is a namespace. The substance of this response is **what the
            # representative advertises**: what it is (advertises), the data it holds (files), and what
            # it carries (children). There is no entry document.
            for r in store.regions():
                if r["dir"] != parts[1] and r["key"] != parts[1].upper(): continue
                rep = next((n for n in store.nodes() if n["id"] == r["representative"]), None)
                if not rep:
                    # With no representative this does not return an empty list. An empty list reads
                    # as "it holds nothing", when the truth is "no node speaks for this area" — and a
                    # caller has to be able to tell those apart.
                    return self._err(409, f"region {r['dir']}: no top representative, so there is nothing to advertise — this area is not ready to speak yet")
                return self._send(200, {
                    "dir": r["dir"], "key": r["key"], "representative": r["representative"],
                    "use_when": r.get("use_when") or "",     # should I come here — the same value the listing gave
                    "advertises": r["advertises"],           # how the representative describes itself (one_liner)
                    # Whether a circuit from another backbone may read this area. Not on the export
                    # surface — this is the **owner's** view of its own decision, and the screen
                    # shows it so a person can make it.
                    "export": bool(r.get("export")),
                    "entries": [_advert_child(c) for c in advertised(r["representative"])],
})
                    # `path`, `data_kind`, `authority`, `nodes` and `docs` are kept out of the
                    # advertisement. A path invites someone to build an address from it — someone did.
                    # `data_kind` and `authority` held the same value in every area, so they separated
                    # nothing. `children` covers `nodes`, and `files` covers `docs`.
            return self._err(404, f"region {parts[1]} not found")
        # GET /v1/regions/{dir}/files/{name} retired (2026-09-09). It was opened to serve documents
        # sitting directly under an area; a day later those documents moved under the representative
        # and edges.md was retired too, so **there was nothing left to serve**. Leaving it is the
        # "slot that looks usable" failure again. Files come from nodes.
        if parts == ["nodes"]:
            # A listing is an index: what exists and where to go. The detail response holds the rest.
            # Emitting the internal record wholesale with `{**n}` ships `path`, `dir` and an
            # address-less `files[]`, and the receiver glues them into a path. The same projection the
            # area listing gets is applied here.
            return self._send(200, {"revision": head(DATA), "nodes": [
                {"id": n["id"], "name": n["name"], "kind": n["kind"], "region": n["region"],
                 "one_liner": n["one_liner"], "role": n.get("role"), "parent": n.get("parent"),
                 "expands_in": n.get("expands_in"),
                 "status": n["status"], "injected_by": n.get("injected_by"), "order": n["order"],
                 "fetch": f"/v1/nodes/{n['id']}"} for n in store.nodes()]})
        if len(parts) == 2 and parts[0] == "nodes":
            n = store.node(parts[1])
            if not n: return self._err(404, f"node {parts[1]} not found")
            # A representative may contain other representatives (SPEC-v2 §1.1) — what it carries comes with it
            # Under one type a file IS a child: one row per entity, carrying its own address.
            # Listing `files` as well would advertise everything twice, at two addresses, for one
            # thing — which is what made a single-file node draw itself as a node on the map.
            # Its own two times, beside its children's. A node's table lists its entries *and*, when
            # it has a body, a first row that is the node itself — and that row had no age while
            # every row under it did, so the one document a reader is most likely to quote was the
            # one the page said nothing about.
            own = {k: v for k, v in (ages.of(DATA, head(DATA)).get(parts[1]) or {}).items() if v}
            return self._send(200, {**{k: v for k, v in n.items() if k not in _NODE_INTERNAL}, **own,
                                    "entries": [_advert_child(c) for c in advertised(parts[1])],
                                    "body": n.get("body") or ""})
        if len(parts) == 3 and parts[0] == "nodes" and parts[2] == "body":
            # One entity, two things you can ask for: what it holds (a table) and what it says (a
            # document). They are different verbs, so they are different addresses — reading a
            # document must never require calling the tool that lists tables.
            n = store.node(parts[1])
            if not n: return self._err(404, f"node {parts[1]} not found")
            body = (n.get("body") or "").strip()
            if not body:
                # Not the same as "it does not exist". A caller has to be able to tell an entity
                # nobody has written yet from an address that is wrong.
                return self._err(404, f"node {parts[1]} has no document yet — it is listed as `type: empty`")
            return self._send(200, body + "\n", "text/markdown; charset=utf-8")
        if len(parts) == 4 and parts[0] == "nodes" and parts[2] == "files":
            t = store.node_file(parts[1], parts[3])
            return self._send(200, t, "text/markdown; charset=utf-8") if t is not None else self._err(404, "file not listed in the node's `## Files`")
        if parts[:1] == ["overlays"]:
            if not OVERLAYS: return self._err(501, "ONTOLOGY_OVERLAYS is not configured")
            if len(parts) == 1:
                q = dict(x.split("=", 1) for x in urlparse(self.path).query.split("&") if "=" in x)
                want = q.get("state")
                # Reading is also when expiry is decided — `all()` settles each record on the way past.
                rows = [o for o in ostore().all() if not want or o["state"] == want]
                return self._send(200, {"overlays": [overlay_out(o) for o in rows]})
            if len(parts) == 2:
                try: return self._send(200, overlay_out(ostore().get(parts[1])))
                except overlays.OverlayError as e: return self._err(e.status, str(e))
            return self._err(404, "unknown path")
        if parts[:1] == ["walks"]:
            # The footprint, read: everything after a cursor for the screen's live view, or one walk
            # whole for a replay. Reading is also when expiry is decided.
            if not WALKS: return self._err(501, "ONTOLOGY_WALKS is not configured — the footprint is off")
            try:
                if len(parts) == 1:
                    q = dict(x.split("=", 1) for x in urlparse(self.path).query.split("&") if "=" in x)
                    if "since" in q:
                        try: n = int(q.get("since") or 0)
                        except ValueError: return self._err(400, "since must be a step number")
                        return self._send(200, wstore().since(n, checks=q.get("checks") == "1"))
                    want = q.get("state") or None
                    # The history: newest first, a page at a time when `limit` is given — six hours of
                    # walks is hundreds of rows on a busy install, and the screen shows ten. Each row
                    # carries what the history table prints, so a page costs one request, not eleven.
                    try:
                        limit = int(q["limit"]) if q.get("limit") else None
                        offset = int(q.get("offset") or 0)
                    except ValueError: return self._err(400, "limit and offset must be numbers")
                    if (limit is not None and not 1 <= limit <= 200) or offset < 0:
                        return self._err(400, "limit is 1 to 200, and offset is not negative")
                    # By the opening step's number, not `at`: that is to the second, and walks opened in
                    # the same second would come back in an order that changes between pages.
                    rows = sorted((w for w in wstore().all(want) if q.get("checks") == "1" or not w.get("check")), key=lambda w: ((w.get("steps") or [{}])[0].get("n") or 0, w.get("at") or ""), reverse=True)
                    page = rows[offset:offset + limit] if limit is not None else rows
                    return self._send(200, {"seq": wstore().seq(), "total": len(rows), "offset": offset,
                                            "walks": [_walk_row(w) for w in page]})
                if len(parts) == 2: return self._send(200, wstore().get(parts[1]))
            except walks.WalkError as e: return self._err(e.status, str(e))
            return self._err(404, "unknown path")
        if parts == ["validate"]: return self._send(200, validate(store))
        if len(parts) == 2 and parts[0] == "curator":
            q = dict(x.split("=", 1) for x in urlparse(self.path).query.split("&") if "=" in x)
            if parts[1] == "proposals": return self._send(200, {"proposals": cstore().proposals(q.get("status"))})
        return self._err(404, "unknown path")

    # ---- writes ----
    def _write(self, method, parts):
        actor = self._actor(); body = self._body()
        # Before any lookup: a write into a directory swapped under this process failed as "node … not
        # found" — true of the dead mount, and no help. Boot always leaves a commit (operator QA).
        if parts[:1] in (["nodes"], ["regions"], ["changes"]) and head(DATA) is None:
            raise WriteError(503, "the data directory has no git history — if it was replaced while this was "
                                  "running, restart it: docker compose restart ontology", code="repo_replaced")
        if parts == ["place"] and method == "POST":
            # One hop of the placement walk, stateless: the table at `at`, and where the document would
            # land if the walk stopped here. A POST that writes nothing; the walk's state is the
            # caller's, like a question's is.
            #
            # Each row is its line and nothing else. Until 2026-10-07 every row also carried the words
            # it shared with the document, and a mechanical rule proposed widening the lines above —
            # string matching steering the one choice the agent is there to make. Measured on 35
            # documents, word overlap alone found the right parent 9% of the time, and the propagation
            # rule advertised a new version of a rule 0 times in 15 (eval/placement).
            at = str(body.get("at") or "/v1/regions").rstrip("/") or "/v1/regions"
            rows, here = [], None
            if at == "/v1/regions":
                for r in store.regions():
                    rows.append({"address": f"/v1/regions/{r['dir']}", "kind": "area", "id": r["dir"],
                                 "name": r.get("key") or r["dir"], "line": r.get("use_when") or ""})
            elif at.startswith("/v1/regions/"):
                d = at[len("/v1/regions/"):]
                r = next((x for x in store.regions() if x["dir"] == d or x["key"] == d.upper()), None)
                if not r: return self._err(404, f"region {d} not found")
                here = {"parent": r["representative"], "region": r["dir"]}
                for c in advertised(r["representative"]):
                    rows.append({"address": f"/v1/nodes/{c['id']}", "kind": "node", "id": c["id"], "name": c["name"],
                                 "line": c.get("one_liner") or ""})
            elif at.startswith("/v1/nodes/"):
                n = store.node(at[len("/v1/nodes/"):])
                if not n: return self._err(404, f"node {at[len('/v1/nodes/'):]} not found")
                here = {"parent": n["id"], "region": n["region"]}
                for c in store.children_of(n["id"]):
                    rows.append({"address": f"/v1/nodes/{c['id']}", "kind": "node", "id": c["id"], "name": c["name"],
                                 "line": c.get("one_liner") or ""})
            else:
                return self._err(400, f"{at} is not a table a document can be placed from")
            return self._send(200, {"at": at, "rows": rows, "here": here, "revision": head(DATA)})
        if parts[:1] == ["walks"] and method == "POST":
            # The footprint, written: by the MCP server, which is the only thing that sees a walk.
            # Not a write to the repository — nothing here is committed — but it goes through
            # `_write` so the one actor header every write carries names who walked.
            if not WALKS: return self._err(501, "ONTOLOGY_WALKS is not configured — the footprint is off")
            try:
                if len(parts) == 1:
                    w = wstore().open(str(body.get("question") or ""), str(body.get("how") or ""),
                                      {"kind": "agent", "name": actor}, check=bool(body.get("check")))
                    return self._send(201, {"id": w["id"], "seq": w["steps"][-1]["n"], "at": w["at"]})
                if len(parts) == 3 and parts[2] == "steps":
                    s = wstore().step(parts[1], str(body.get("op") or ""), str(body.get("address") or ""), str(body.get("why") or ""))
                    return self._send(201, {"ok": True, **s})
                if len(parts) == 3 and parts[2] == "close":
                    w = wstore().close(parts[1], str(body.get("outcome") or ""), str(body.get("why") or ""))
                    return self._send(200, {"ok": True, "id": w["id"], "state": w["state"], "outcome": w["outcome"]})
            except walks.WalkError as e: return self._err(e.status, str(e))
            return self._err(404, "unknown path")
        if parts == ["suggest", "use-when"] and method == "POST":
            name, one = str(body.get("name") or "").strip(), str(body.get("one_liner") or "").strip()
            if not name or not one: return self._err(400, "name and one_liner are required")
            return self._send(200, {"use_when": suggest_use_when(name, one)})
        if parts == ["suggest", "description"] and method == "POST":
            # The line `put_file` writes when no description is given, handed back instead of
            # written. Same prompt and same two refusals, so the button shows what the write would
            # have done rather than a second opinion about it.
            name, content = str(body.get("name") or "").strip(), str(body.get("content") or "")
            if not name or not content.strip(): return self._err(400, "name and content are required")
            if not llm_configured(): return self._err(503, "no LLM is configured to draft one (ONTOLOGY_LLM_*) — type the line yourself")
            line = (describe_file(name, content) or "").strip()
            if not line: return self._err(422, "nothing could be drawn from that body — type the line yourself")
            return self._send(200, {"description": line, "name": name})
        if parts == ["suggest", "id"] and method == "POST":
            # **The same resolution the write performs**, not a second one. A button that shows an id
            # the save then changes is worse than no button: an id is permanent and the person is
            # being asked to agree to it.
            name = str(body.get("name") or "").strip()
            if not name: return self._err(400, "name is required")
            nid, generated = writer._resolve_id(None, name=name, kind="",
                                                one_liner=str(body.get("one_liner") or "").strip(),
                                                region=str(body.get("region") or "").strip())
            # `from` says which of the two happened, because they are different promises: a name that
            # answers for itself always gives this id, while a translated one is this model's reading
            # of a name and a person should look at it.
            return self._send(200, {"id": nid, "from": "model" if generated else "name"})
        if parts == ["validate"] and method == "POST":
            res = validate(store); return self._send(200 if res["ok"] else 422, res)
        if len(parts) == 4 and parts[0] == "curator" and parts[1] == "proposals" and method == "POST":
            status = {"accept": "accepted", "reject": "rejected"}.get(parts[3])
            if not status: return self._err(404, "accept | reject")
            out = curator.decide(cstore(), parts[2], status, body.get("why"), lambda p: apply_proposal(p, actor))
            # A decision that did not happen must not answer 200. `decide` says so in the body and
            # leaves the proposal pending, which is right, and every caller that reads the status
            # line — a script, a curl, the screen's own `request()` — was told the accept had worked
            # and showed "applied" over a queue item still sitting there. The same failure the
            # publish path had in the other direction: a status that disagrees with what happened.
            if isinstance(out, dict) and out.get("ok") is False:
                det = out.get("detail") if isinstance(out.get("detail"), dict) else {}
                # Say what happened, as a refusal the screen can translate. It used to answer
                # "apply failed" and nothing else through the web app: the current sentence a
                # conflict had found, and "this entity no longer exists", were both dropped (2026-10-10).
                if det.get("error") == "conflict":
                    return self._err(409, f"the line changed since this was proposed — it now reads: {det.get('current')}",
                                     reason="conflict", data={"id": det.get("field") or "", "current": det.get("current") or ""})
                if out.get("error") == "no such proposal":
                    return self._err(404, "no such proposal", reason="proposal_missing")
                if str(out.get("error") or "").startswith("proposal is "):
                    return self._err(409, out["error"], reason="already_decided", data={"status": out["error"][len("proposal is "):]})
                if det.get("error"):
                    return self._err(int(det.get("code") or 409), str(det["error"]), reason=det.get("reason"))
                return self._err(409, str(out.get("error") or "the proposal could not be applied"))
            return self._send(200, out)
        if len(parts) == 3 and parts[0] == "nodes" and parts[2] == "one-liner-draft" and method == "POST":
            # Draft only — the line goes through the queue like an area's, never straight to disk.
            return self._send(200, one_liner_draft(parts[1]))
        if parts[:1] == ["overlays"]:
            if not OVERLAYS: return self._err(501, "ONTOLOGY_OVERLAYS is not configured")
            try:
                if len(parts) == 1 and method == "POST":
                    return self._send(201, overlay_out(ostore().create(
                        body.get("question"), body.get("members") or [], body.get("by") or {},
                        overlay_resolve, overlay_rows_of)))
                if len(parts) == 2 and method == "PATCH":
                    return self._send(200, overlay_out(ostore().amend(
                        parts[1], body.get("add"), body.get("remove"), body.get("why"),
                        overlay_resolve, overlay_rows_of)))
                if len(parts) == 3 and parts[2] == "close" and method == "POST":
                    return self._send(200, overlay_out(ostore().close(parts[1], str(body.get("outcome") or ""),
                                                                      body.get("used") or [], overlay_resolve)))
            except overlays.OverlayError as e:
                return self._err(e.status, str(e))
            return self._err(404, "unknown path")
        if parts == ["curator", "route-draft"] and method == "POST":
            return self._send(200, route_draft(str(body.get("region") or ""), str(body.get("scope") or ""), body.get("changed")))
        if parts == ["curator", "proposals"] and method == "POST":
            # A routing proposal raised by a person. There is no immediate-apply path — it always goes through the queue
            # Its target must exist when it is filed: a proposal for a node or area that is not there
            # was accepted, then hung in the queue for ever with nowhere on the map to show it.
            ent, reg = str(body.get("entity") or "").strip(), str(body.get("region") or "").strip()
            if ent and not store.node(ent): return self._err(404, f"there is no {ent} to propose a line for", reason="target_missing", data={"id": ent})
            if not ent and reg and not any(r["dir"] == reg or r["key"] == reg.upper() for r in store.regions()):
                return self._err(404, f"there is no area {reg}", reason="region_missing", data={"region": reg})
            try: return self._send(201, curator.submit_route(cstore(), body, actor))
            except ValueError as e: return self._err(422, str(e))
        if len(parts) == 2 and parts[0] == "regions" and method == "DELETE":
            return self._send(200, writer.delete_region(parts[1], actor))
        if parts == ["regions"] and method == "POST":
            return self._send(201, writer.create_region(body, actor))
        if parts == ["vocab"]: return self._err(405, "vocabulary and kinds change through Knowledge review, not this API (operator decision 2026-09-07)")
        if parts == ["changes"] and method == "POST":
            # A change set (docs/CHANGE.md): several decisions, one commit, the lines over them
            # decided. `dry_run` is the same transaction without the commit. Where a review queue is
            # configured, a set that rewords an area's sentence — the line hop 0 prints, a person's —
            # is queued whole after a dry run proves it applies; accepting it applies it.
            dry = bool(body.get("dry_run"))
            # Rewording an area's sentence, or making a new area: either way hop 0 changes, and hop 0's
            # sentences are a person's. A new area slipped past the queue while a reworded one waited
            # in it (found 2026-10-10).
            rewords_hop0 = any(isinstance(d, dict) and ((d.get("op") == "reword" and d.get("field") == "use_when")
                                                        or (d.get("op") == "create" and d.get("parent") is None))
                               for d in (body.get("decisions") or []) if isinstance(body.get("decisions"), list))
            if HARNESS and rewords_hop0 and not dry:
                # The set is proved against the tree as it is now, and queued with that revision as its
                # base — so if the tree moves on before somebody accepts it, accepting says it is stale
                # rather than doing whatever the decisions mean against a tree they were not made on.
                if not body.get("base"): body = {**body, "base": head(DATA)}
                res = change.apply(writer, body, actor, dry_run=True)
                pid = f"cp_{uuid.uuid4().hex[:10]}"
                cstore().append({"event": "proposal", "id": pid, "at": curator._now(), "type": "change",
                                 "set": {k: v for k, v in body.items() if k != "dry_run"}, "why": str(body.get("why") or ""),
                                 "submitted_by": actor, "impact": res.get("impact"), "ids": res.get("ids"),
                                 "evidence": [f"node:{d.get('id')}" for d in body.get("decisions") if isinstance(d, dict) and d.get("id")]})
                return self._send(202, {"ok": True, "queued": pid, "status": "pending", "impact": res.get("impact"), "ids": res.get("ids"),
                                        "message": "the set changes hop 0 — an area's sentence, or a new area — so it waits in the review queue; accepting it applies it whole"})
            return self._send(200 if dry else 201, change.apply(writer, body, actor, dry_run=dry))
        if parts == ["nodes"] and method == "POST": return self._send(201, writer.create_node(body, actor))
        if len(parts) == 2 and parts[0] == "nodes":
            if method == "PUT": return self._send(200, writer.update_node(parts[1], body, actor))
            if method == "DELETE": return self._send(200, writer.delete_node(parts[1], actor))
        if len(parts) == 5 and parts[0] == "nodes" and parts[2] == "files" and parts[4] == "promote" and method == "POST":
            # Promotion is one transaction — split the create from the delete and the same file exists twice
            return self._send(201, writer.promote_file(parts[1], parts[3], body, actor))
        if len(parts) == 4 and parts[0] == "nodes" and parts[2] == "files":
            if method == "PUT": return self._send(200, writer.put_file(parts[1], parts[3], body, actor))
            if method == "DELETE": return self._send(200, writer.delete_file(parts[1], parts[3], actor))
        return self._err(405, "method not allowed for this path")


def _to_export(payload):
    """Move every address in an answer onto the export surface.

    Only `fetch` — the field every table states is the one way to go, and the only one a caller is
    told to use. Rewriting anything that merely looks like a path would catch prose, ids and the
    `path` field the validator keeps for its own bookkeeping.
    """
    if isinstance(payload, dict):
        return {k: (f"/v1/export{v[len('/v1'):]}"
                    if k == "fetch" and isinstance(v, str) and v.startswith("/v1/") and not v.startswith("/v1/export/")
                    else _to_export(v))
                for k, v in payload.items()}
    if isinstance(payload, list): return [_to_export(v) for v in payload]
    return payload


def dir_of(source: str) -> str:
    """An area's directory from a `source`, in either spelling. Before 2026-10-07 derive wrote the
    directory with hyphens turned into underscores; committed tables and older backbones still say so.
    Directory names are kebab-case (create_region refuses an underscore), so this is exact."""
    return str(source or "").replace("_", "-")


_LIVE_SAID: set = set()
_HEALTH_VALID: dict = {}


def _health_valid() -> dict:
    """`valid` and the first reasons it is not, for /healthz — computed once per commit, because the
    health check is polled and validation reads every entity."""
    # Keyed on the commit *and* the files as they are: a hand edit, or the leftovers of a killed write,
    # changes the files without moving HEAD, and the cached answer said valid when validate said
    # otherwise — and the other way round (2026-10-10).
    rev = (head(DATA) or "") + ":" + str(hash(store._nodes_key()))
    if rev not in _HEALTH_VALID:
        try:
            res = validate(store)
            _HEALTH_VALID.clear()
            _HEALTH_VALID[rev] = {"valid": bool(res["ok"]), "errors": [str(e) for e in res["errors"][:3]]}
        except Exception as e:
            return {"valid": False, "errors": [f"validation could not run: {type(e).__name__}: {e}"]}
    return _HEALTH_VALID[rev]


def _regions_live() -> dict:
    """`regions.json` as the files say it should be — the committed copy when it agrees, the derived
    document when it does not.

    The file is derived from the areas' `.md` files and committed beside them, and the two drift the
    moment somebody edits an area by hand and pushes without regenerating. Measured 2026-10-05: an
    operator wrote `export: yes` into a representative, committed, restarted — the validator said so
    at startup, in the log, and the server then served the stale table to every reader anyway: hop 0
    did not show the flag and the export surface did not cross with the area. Being told in a log
    line is not the same as a reader being served the truth. `store.regions()` already reads the
    files; this is the other read path brought to the same answer, so the two cannot disagree.

    The committed file stays what the validator checks, so the drift error persists until the disk
    is regenerated — by any write through the API, by `tidy --fix`, or by the startup heal in `main`.
    """
    committed = store.regions_json()
    try:
        derived = json.loads(deriving.regions_doc(store))
    except Exception:
        return committed            # a derive that cannot run is the validator's error to report
    if derived == committed: return committed
    rev = head(DATA)
    if rev not in _LIVE_SAID:
        _LIVE_SAID.add(rev)
        sys.stderr.write("iris-ontology: regions.json is stale against the files — serving what the files say; "
                         "regenerate with any API write or ./ontology/tidy.py <repo> --fix\n")
    return derived


# The three advertisements a model can revise, and the sentence each one is. A scope missing here is
# a scope with no prompt: it used to reach `WHAT[scope]` and come back as `500 internal error`, which
# names neither the mistake nor the fix.
DRAFT_PROMPTS = {
    "as": "the one line in which **the representative introduces itself** when this area is opened",
    "bb": "the one line used to decide **whether to choose this area at all** (what question brings you here)",
}
DRAFTABLE = frozenset(DRAFT_PROMPTS)


def _walk_row(w: dict) -> dict:
    """One walk as the history lists it: who and when, how it ended, and what it did — the tables it
    opened, the documents it read, where it stopped and how long it took. `close` is an outcome, not a
    step, so it is left out of all of those."""
    moves = [s for s in w.get("steps") or [] if s.get("op") != "close"]
    def _t(s):
        try: return datetime.datetime.fromisoformat(str(s.get("at") or "").replace("Z", "+00:00"))
        except ValueError: return None
    first, last = (_t(moves[0]), _t(moves[-1])) if moves else (None, None)
    return {**{k: w.get(k) for k in ("id", "question", "how", "by", "at", "touched_at", "state", "outcome", "closed_at")},
            "steps": len(w.get("steps") or []),
            "tables": sum(1 for s in moves if s.get("op") == "table"),
            "reads": sum(1 for s in moves if s.get("op") == "read"),
            "last": (moves[-1].get("address") or "") if moves else "",
            "last_op": (moves[-1].get("op") or "") if moves else "",
            "took": int((last - first).total_seconds()) if first and last else 0}


def _denied_kinds() -> set[str]:
    """Which kinds do not cross, from the vocabulary as it stands. Read per request rather than at
    startup: `vocab.yaml` is committed like everything else and a policy that needed a restart to
    take effect would be a policy nobody trusts."""
    # Imported by name. `validate` in this module is the **function**, not the module it came from,
    # so `validate.export_kinds` was an AttributeError — swallowed by the guard below, which turned a
    # policy that did nothing into a policy that looked applied. The guard stays, for a vocab.yaml
    # somebody is midway through editing; it is not allowed to hide a missing name.
    try: return export_kinds(store.vocab())
    except Exception: return set()


def _drop_kinds(payload, denied: set[str]):
    """Take the entities a peer may not see out of a listing it is being handed.

    Listing and fetching have to agree. Refusing the fetch alone leaves the address printed in a
    table the peer was given, and an address that is printed and then refused is worse than one that
    was never offered — it reads as an outage, and following it is what the tables tell an agent to
    do. This is the same failure a draft had.
    """
    if not denied or not isinstance(payload, dict): return payload
    out = dict(payload)
    # One level at a time, by the row's own kind. A row under a denied one is never reached, because
    # the denied one was dropped from the listing that would have led to it — and the fetch closes the
    # remembered-address route by walking the whole chain. Navigation and fetch agree; neither leaves
    # an address printed that the other refuses.
    for key in ("entries", "children"):
        rows = out.get(key)
        if isinstance(rows, list):
            out[key] = [r for r in rows
                        if not (isinstance(r, dict) and str(r.get("kind") or "") in denied)]
    return out


def _draft_anywhere(node: dict) -> bool:
    """Is this entity a draft, or under one. A published child of a draft parent is not in any
    listing either — the parent is what carries it — so following an address to it would be the same
    hole one level down."""
    seen, cur = set(), node
    while cur:
        if (cur.get("status") or "") == "draft": return True
        parent = cur.get("parent")
        if not parent or parent in seen: return False
        seen.add(parent)
        cur = store.node(parent)
    return False


def _kind_denied_anywhere(node: dict, denied: set[str]) -> bool:
    """Is this entity of a kind that does not cross, or under one.

    Up the chain for the same reason `_draft_anywhere` walks it: a published child of a hidden parent
    is in no listing either, so following an address to it would be the same hole one level down.
    """
    if not denied: return False
    seen, cur = set(), node
    while cur:
        if str(cur.get("kind") or "") in denied: return True
        parent = cur.get("parent")
        if not parent or parent in seen: return False
        seen.add(parent)
        cur = store.node(parent)
    return False


def main():
    if not DATA.is_dir(): sys.exit(f"ONTOLOGY_DATA {DATA} is not a directory")
    # A write the last process did not finish is rolled back before anything reads the tree.
    from service.write import recover_interrupted, _lock as _write_lock
    undone = recover_interrupted(DATA)
    if undone:
        sys.stderr.write(f"iris-ontology: a write was interrupted by the last shutdown ({undone}); rolled back to the last commit\n")
    # SIGTERM finishes the write in progress, then exits. As PID 1 with no handler the signal was
    # ignored, so every `docker compose restart` waited ten seconds and ended in a SIGKILL — mid-write
    # if one was running (2026-10-10).
    import signal, threading
    def _term(*_):
        def stop():
            with _write_lock: os._exit(0)
        threading.Thread(target=stop, daemon=True).start()
    signal.signal(signal.SIGTERM, _term)
    # Never a reason not to start: a service that exits here restarts in a loop, and then nothing —
    # not /healthz, not the regeneration in DATA-REPO.md — can even reach it to say what is wrong.
    try: res = validate(store)
    except Exception as e:
        traceback.print_exc()
        res = {"ok": False, "errors": [f"validation could not run: {type(e).__name__}: {e}"], "warnings": [], "stats": {"nodes": 0}}
    # A derived file committed stale is the one invalid state the server can mend on its own, and
    # through the same transaction every write uses: nothing to mutate, regenerate, validate, commit.
    # Only when every error is that one — anything else is somebody's decision — and only on a
    # clean tree, since the transaction refuses a dirty one rather than commit somebody's half-done
    # hand edit along with the fix. Left stale, readers are served the files' truth regardless
    # (`_regions_live`); this is the disk catching up with them.
    # Both are "the derived table is not what the files say" — the second is a table written before
    # 2026-10-07, when `source` spelled a hyphenated directory with underscores. Regenerating fixes both.
    drift = [e for e in res["errors"] if "no longer matches the files it is derived from" in e
             or "source must be the directory name" in e
             # Areas written as files with no regions.json yet, or one deleted by hand: the table is
             # missing rows, or has a row with no directory — derived, so regenerated (2026-10-10).
             or "regions.json: missing entry for" in e or "has no directory" in e
             or ("regions.json " in e and "differ from directory" in e)
             # Broken by hand: it is derived, so it is written again rather than mended.
             or e.startswith("regions.json: does not parse")]
    if drift and len(drift) == len(res["errors"]) and head(DATA):
        try:
            out = writer.transact("regions.json: regenerated — it was committed stale", "ontology", lambda: None)
            sys.stderr.write(f"iris-ontology: regions.json was committed stale ({len(drift)} area(s)); regenerated and "
                             f"committed as {str(out.get('revision', ''))[:12]}\n")
            res = validate(store)
        except WriteError as e:
            sys.stderr.write(f"iris-ontology: regions.json is committed stale and could not be regenerated — {e}. "
                             f"Readers are served what the files say; commit or discard your changes, then any API "
                             f"write or ./ontology/tidy.py <repo> --fix regenerates it.\n")
    sys.stderr.write(f"iris-ontology data={DATA} head={head(DATA)} nodes={res['stats']['nodes']} valid={res['ok']}\n")
    # A setting this build does not understand would otherwise be dead quietly: the person set a
    # provider, nothing uses it, and nothing says so. `/healthz` carries the same fact for install.sh.
    if LLM_PROVIDER not in curator.PROVIDERS:
        sys.stderr.write(f"iris-ontology: ONTOLOGY_LLM_PROVIDER={LLM_PROVIDER!r} is not one this build knows "
                         f"({', '.join(curator.PROVIDERS)}) — no LLM will be used\n")
    elif llm_configured():
        sys.stderr.write(f"iris-ontology llm provider={LLM_PROVIDER} model={LLM['MODEL']} "
                         f"max_tokens={LLM_MAX_TOKENS} temperature={LLM_TEMPERATURE}\n")
    else:
        missing = sorted(k for k, v in LLM.items() if not v)
        sys.stderr.write(f"iris-ontology: no LLM — ONTOLOGY_LLM_{', ONTOLOGY_LLM_'.join(missing)} unset\n")
    for e in res["errors"]: sys.stderr.write(f"  ERROR {e}\n")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
