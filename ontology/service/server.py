"""iris-ontology — HTTP API over the v2 data repository (SPEC-v2 §4).

  ONTOLOGY_DATA       the data git repository (default /data)
  ONTOLOGY_PUBLISH    publication directory Pi mounts read-only (default: none → no publish step)
  ONTOLOGY_FRAGMENTS  legacy flat fragment directory — no git, no validation (default: none → 501)
  ONTOLOGY_SERVICES   service-fragment git repository (default: none → 501)
  ONTOLOGY_SERVICE_PUBLISH  where fragments are published for Pi (default: none → no publish step)
  ONTOLOGY_HARNESS    data-harness store — experience.jsonl + edges.json (default: none → 501)
  ONTOLOGY_LLM_BASE_URL / ONTOLOGY_LLM_API_KEY / ONTOLOGY_LLM_MODEL  the sleeping brain's model (SPEC-curator; absent → mechanical sleep only)
  PORT                listen port (default 8100)

Reads serve the repository working tree. Writes go through Writer.transact: mutate → regenerate derived files →
validate → git commit → publish atomically (`current` symlink + REVISION). Vocabulary and kinds are not writable
here — changing them is a Knowledge-approved change to vocab.yaml (operator decision, 2026-09-07).
Pi never calls this API; it mounts the published tree.
"""
from __future__ import annotations
import json, os, re, sys, threading, time, traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.store import Store                     # noqa: E402
from service.validate import validate               # noqa: E402
from service.write import Writer, WriteError, publish, head, _dirty   # noqa: E402
from service.service_store import ServiceStore              # noqa: E402
from service.validate_service import validate_services      # noqa: E402
from service.write_service import ServiceWriter             # noqa: E402
from service import peers as peering                        # noqa: E402
from service import overlays                                # noqa: E402
from service import curator                                 # noqa: E402

DATA = Path(os.environ.get("ONTOLOGY_DATA", "/data"))
PUBLISH = Path(os.environ["ONTOLOGY_PUBLISH"]) if os.environ.get("ONTOLOGY_PUBLISH") else None
FRAGMENTS = Path(os.environ["ONTOLOGY_FRAGMENTS"]) if os.environ.get("ONTOLOGY_FRAGMENTS") else None
# The shared secret a peer backbone presents to read /v1/export. Unset means this backbone has no
# link and that whole surface answers 501 — which is the right default: opening one is a decision,
# not something an install drifts into. See docs/PEERING.md.
PEER_TOKEN = (os.environ.get("ONTOLOGY_PEER_TOKEN") or "").strip()
SERVICES = Path(os.environ["ONTOLOGY_SERVICES"]) if os.environ.get("ONTOLOGY_SERVICES") else None
SERVICE_PUBLISH = Path(os.environ["ONTOLOGY_SERVICE_PUBLISH"]) if os.environ.get("ONTOLOGY_SERVICE_PUBLISH") else None
# Its own path, never under ONTOLOGY_PUBLISH: Pi mounts that read-only and it is a git checkout
# swapped atomically, so a sibling that is neither would be published by accident. Unset → 501, the
# same way a missing ONTOLOGY_SERVICES answers.
OVERLAYS = Path(os.environ["ONTOLOGY_OVERLAYS"]) if os.environ.get("ONTOLOGY_OVERLAYS") else None
PORT = int(os.environ.get("PORT", "8100"))
store = Store(DATA); writer = Writer(DATA, PUBLISH, FRAGMENTS)
# Fragments carry decisions, Core carries structure (SPEC-service-fragment §1). Separate repo, separate
# publish, separate cadence — bound by the `core_revision` each fragment declares.
svc_store = ServiceStore(SERVICES) if SERVICES else None
svc_writer = ServiceWriter(SERVICES, SERVICE_PUBLISH, PUBLISH) if SERVICES else None
writer.keep_provider = lambda: pinned_core_revisions()      # Core publishes must keep the trees fragments pin


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

    **An id is a permanent address** — agents call `/v1/nodes/<id>`, edges point at each other by it,
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


def suggest_use_when(name: str, one_liner: str, core_description: str) -> str:
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
    # A brand-new area has no description and no row in the architecture document yet — the form that
    # opens one asks for two things and derives the rest. Handing the model an empty field next to
    # "invent no capability the area has not claimed" left it nothing to do but ask the caller for the
    # missing context, so say what is missing and what to do about it.
    known = [f"area name: {name}"]
    if one_liner and one_liner != name: known.append(f"what it is: {one_liner}")
    if core_description: known.append(f"its row in the architecture document: {core_description}")
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
    if not field: raise WriteError(400, "scope must be as | bb | core")
    if field == "core_row":
        before = next((x.get("description", "") for x in store.regions_json().get("regions", []) if x["id"] == r["key"]), "")
    else:
        before = rep.get(field) or ""

    # What this area holds right now — the material to compare the advertisement against
    holds = [f"file {f['name']} — {f['description']}" for f in rep["files"]]
    holds += [f"node {c['name']} ({c['kind']}) — {c['one_liner']}" for c in store.children_of(rep["id"])]
    c = llm_client()
    if not c:
        raise WriteError(503, "route-draft needs an LLM (ONTOLOGY_LLM_*)")
    WHAT = {"as": "the one line in which **the representative introduces itself** when this area is opened",
            "bb": "the one line used to decide **whether to choose this area at all** (what question brings you here)",
            "core": "the **one-line summary** carried in the area table of the architecture document"}[scope]
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
writer.describe = lambda name, content: describe_file(name, content) if llm_configured() else None
writer.describe_configured = lambda: llm_configured()


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


# The automatic nap was retired (2026-09-09). It triggered on "something arrived from a run", and
# that collection path is gone. A timer with no signal never fires — dead code pretending to be
# alive, so it is not kept. The curator is called by a person (POST /v1/curator/sleep).

def draft_target() -> tuple[str, str] | None:
    """Where the curator's drafts go, and what kind they get — declared in `vocab.yaml`, not here.

        curator:
          draft_area: learned      # an area whose `area_rules` allow drafts
          draft_kind: task         # a kind from this vocabulary

    This used to be two literals naming one domain's area and one of its Korean kind names, which
    meant the curator could only ever write into that domain. Absent, promotion is refused with a
    sentence saying what to declare — better than writing into an area that does not exist.
    """
    c = (store.vocab().get("curator") or {})
    area, kind = str(c.get("draft_area") or "").strip(), str(c.get("draft_kind") or "").strip()
    return (area, kind) if area and kind else None


_NO_TARGET = ("this install has not declared where curator drafts go — set curator.draft_area and "
              "curator.draft_kind in vocab.yaml")


def create_draft(d: dict, evidence: list, actor: str):
    """A guard-passed promotion becomes a draft at once — visible to people, invisible to an agent
    until it is confirmed."""
    target = draft_target()
    if not target: return {"ok": False, "error": _NO_TARGET}
    area, kind = target
    runs = sorted({e.split(":", 1)[1] for e in evidence if e.startswith("run:")})
    content = "\n".join(d.get("points") or []) + ("\n# runs cited: " + ", ".join(runs) if runs else "") + "".join(f"\n# weak: {w}" for w in (d.get("weak") or [])) + "\n"
    try:
        return writer.create_node({"id": d["id"], "name": d["name"], "kind": kind, "region": area, "holds": "pointers", "status": "draft",
                                   "one_liner": d["one_liner"], "injected_by": "curator",
                                   "files": [{"name": "points.md", "description": d.get("why") or "tidied by the curator", "content": content}]}, actor)
    except WriteError as e: return {"ok": False, "error": str(e), "details": e.details}


def discard_draft(nid: str, actor: str = "curator"):
    n = store.node(nid)
    if not n or n.get("status") != "draft": return {"ok": False, "error": "not a draft"}
    try: return writer.delete_node(nid, actor)
    except WriteError as e: return {"ok": False, "error": str(e)}


def apply_proposal(p: dict, actor: str):
    """Accepting a proposal runs the ordinary write path — never a side door."""
    if p["type"] == "promote" and p.get("draft_node"):
        n = store.node(p["draft_node"])
        if not n: return {"ok": False, "error": f"draft node {p['draft_node']} no longer exists"}
        return writer.update_node(p["draft_node"], {"status": "published"}, actor)          # confirmed → next publish carries it
    if p["type"] == "promote":
        d = p.get("draft") or {}
        nid = str(d.get("id") or "").strip()
        if not nid: return {"ok": False, "error": "promote needs draft.id — a mechanical candidate has no draft; pass one in `override.draft`"}
        points = list(d.get("points") or [])
        runs = sorted({r for e in p.get("evidence", []) for r in ([e.split(":",1)[1]] if e.startswith("run:") else [])})
        target = draft_target()
        if not target: return {"ok": False, "error": _NO_TARGET}
        area, kind = target
        content = "\n".join(points) + ("\n# runs cited: " + ", ".join(runs) if runs else "") + "\n"
        return writer.create_node({"id": nid, "name": d.get("name"), "kind": kind, "region": area, "holds": "pointers",
                                   "one_liner": d.get("one_liner"), "injected_by": "curator",
                                   "files": [{"name": "points.md", "description": d.get("why") or "tidied by the curator — the runs it rests on are in the file", "content": content}]}, actor)
    if p["type"] == "route":
        # Approval happens later than drafting. If the value moved in between, this does not overwrite
        # it — it **hands the current value back**.
        scope, region = p["scope"], p["region"]
        if scope == "entity":
            # The same conflict rule as an area's line, for the same reason: approval happens later
            # than drafting, and if the sentence moved in between this hands the current one back
            # rather than overwriting what someone else decided.
            n = store.node(p.get("entity") or "")
            if not n: return {"ok": False, "error": f"entity {p.get('entity')} no longer exists"}
            cur = n.get("one_liner") or ""
            if p.get("before") and cur != p["before"]:
                return {"ok": False, "error": "conflict", "code": 409, "field": "one_liner",
                        "current": cur, "submitted_before": p["before"]}
            return writer.update_node(n["id"], {"one_liner": p["after"]}, actor)
        if scope == "core":
            key = next((r["key"] for r in store.regions() if r["dir"] == region or r["key"] == region.upper()), None)
            if not key: return {"ok": False, "error": f"region {region} not found"}
            cur = next((r.get("description", "") for r in store.regions_json().get("regions", []) if r["id"] == key), "")
            if p.get("before") and cur != p["before"]:
                return {"ok": False, "error": "conflict", "code": 409, "field": "core_row",
                        "current": cur, "submitted_before": p["before"]}
            return writer.put_core_row(key, p["after"], actor)
        r = next((x for x in store.regions() if x["dir"] == region or x["key"] == region.upper()), None)
        if not r or not r.get("representative"): return {"ok": False, "error": f"region {region} has no representative"}
        rep = store.node(r["representative"])
        # From the table, not from a two-way if. It read `"one_liner" if scope == "as" else "use_when"`,
        # which is correct for exactly the two scopes that existed and writes the wrong field for any
        # third — a `peer` proposal would have silently overwritten the area's own `use_when`.
        field = curator.ROUTE_SCOPES.get(curator.SCOPE_ALIAS.get(scope, scope))
        if not field: return {"ok": False, "error": f"unknown route scope {scope!r}"}
        cur = (rep.get(field) or "")
        if p.get("before") and cur != p["before"]:
            return {"ok": False, "error": "conflict", "code": 409, "field": field,
                    "current": cur, "submitted_before": p["before"]}
        return writer.update_node(rep["id"], {field: p["after"]}, actor)
    if p["type"] == "repin":
        w = need_services(); return w.update_service(p["service"], {"core_revision": p["to"]}, actor)
    return None



def pinned_core_revisions() -> set[str]:
    """Core revisions the fragments pin — publish() must not prune these."""
    return {str(s.get("core_revision")) for s in svc_store.services() if s.get("core_revision")} if svc_store else set()


def need_services():
    if not svc_writer: raise WriteError(501, "ONTOLOGY_SERVICES is not configured")
    return svc_writer


# `_advert_file` retired (2026-09-11). It advertised a file at `/v1/nodes/<id>/files/<name>` — a
# second address for something that now has its own. Every row goes through `_advert_child`.


# Internal bookkeeping, kept out of responses. `path` is the repository path itself; `present_files`
# are file names the API does not serve; `file_scopes` is a map of names with no addresses — scope
# moved onto the file's own row. On a node, `dir` is a character-for-character duplicate of `id`. An
# area's `dir` is different: that one is a name, and consumers read it.
_NODE_INTERNAL = ("path", "dir", "present_files", "file_scopes", "holds", "files")
# Service fragments are the same: `dir` duplicates `id` here too. Confirmed unused by the screen
# before removal — the second half of the two-phase rule.
_SERVICE_INTERNAL = ("path", "dir", "present_files")


def _advert_service_file(sid: str, f: dict) -> dict:
    return {**f, "type": "data", "fetch": f"/v1/services/{sid}/files/{f['name']}"}


_overlay_store = None


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

    `status: draft` is how the curator writes something a person has not accepted yet, and the whole
    point of it is stated on the screen: *"A draft node is invisible to the agent. Accepting publishes
    it; rejecting deletes it. That is what keeps the curator's own writing from returning as
    evidence."* `create_draft` says the same thing in one line — visible to people, invisible to an
    agent.

    It was not true. `derive.py` drops drafts from `regions.json`, but every advertised listing here
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
    row = {"id": c["id"], "name": c["name"], "kind": c["kind"], "one_liner": c["one_liner"],
           "type": kind, "has_body": has_body, "children": len(kids),
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

    def _send(self, code: int, payload, ctype="application/json; charset=utf-8"):
        if self._as_peer and isinstance(payload, dict): payload = _to_export(payload)
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
                dirty = ""
                try: dirty = _dirty(DATA)
                except Exception: dirty = ""
                return self._send(200, {"ok": True, "data": str(DATA), "head": head(DATA),
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
                                        "writable": not dirty, "uncommitted": dirty,
                                        "published": (PUBLISH / "REVISION").read_text().strip() if PUBLISH and (PUBLISH / "REVISION").exists() else None})
            if parts[:1] != ["v1"]: return self._err(404, "unknown path")
            parts = parts[1:]
            # Before anything else, and read-only. A link carries advertisements and documents in one
            # direction: writes go to the backbone that owns the area, through its own screen and its
            # own review queue. That is not a limitation to lift later — it is the reason the link
            # exists. Two ontologies that write to each other have been merged.
            if parts[:1] == ["export"]:
                # One exception, and it is not a write. `refresh` discards something this backbone
                # *remembers* about the caller and leaves everything it holds untouched: nothing can
                # be read afterwards that could not be read before, only sooner. A peer sends it when
                # what it advertises has changed, so a withdrawal does not sit on this table for the
                # length of a cache. See `peers.announce` for why withdrawal is the case worth it.
                if parts[1:] == ["refresh"] and method == "POST": return self._refresh()
                if method != "GET": return self._err(405, "a link is read-only — write to the backbone that owns it")
                return self._export(parts[1:])
            if parts[:1] == ["peers"]:
                if method != "GET": return self._err(405, "a link is read-only — write to the backbone that owns it")
                if len(parts) < 3: return self._err(404, "unknown peer path")
                try:
                    payload, ctype = peering.relay(DATA, parts[1], parts[2:])
                    # Sent as whatever it is. A document body is Markdown on this backbone and is
                    # Markdown across a link too — a caller should not be able to tell, from the shape
                    # of an answer, which side of a link it came from.
                    return self._send(200, payload, ctype)
                except peering.PeerError as e:
                    # The peer's own status is passed through when it answered, and 504 when it did
                    # not. A relayed 404 means that backbone does not hold the thing — which is its
                    # claim to make. A timeout is nobody's claim and must not arrive looking like one.
                    return self._err(e.status, str(e), reason=("peer_said_no" if e.reachable else "peer_unreachable"),
                                     data={"peer": parts[1], "reachable": e.reachable})
            if method == "GET": return self._get(parts)
            before = _export_state()
            out = self._write(method, parts)
            # Only when what crosses a link actually changed — every other save is nobody else's
            # business, and a poke on each one would make a link's chatter track this backbone's
            # edit rate instead of its export rate. Off the request thread, because a peer that is
            # slow must not make somebody's save slow, and one that is down must not make it fail.
            if _export_state() != before:
                threading.Thread(target=peering.announce, args=(DATA,), daemon=True).start()
            return out
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

    def _refresh(self):
        """Forget what this backbone remembers about the caller, and nothing else."""
        token = self.headers.get("X-Peer-Token") or ""
        who = _peer_by_token(token)
        if not who:
            # No shared-token fallback here, unlike a read. Forgetting is per peer, and a caller with
            # no name says which peer to forget no better than a stranger does.
            return self._err(401, "peer token missing or wrong")
        peering.forget(who["name"])
        return self._send(200, {"ok": True, "forgot": who["name"]})

    # ---- what crosses a link ----
    def _export(self, parts):
        """The only surface a peer backbone can read. See docs/PEERING.md.

        **It is a separate surface, not the ordinary one behind a check.** An area reaches a peer only
        by having written `use_when_export`, and every handler here starts from that set — so there is
        no path through this code, and no bug in a token check, that can serve an area nobody decided
        to share. A filter applied on the way out would have to be right every time; a surface built
        from the exported set is right by construction.

        The line a peer sees is `use_when_export`, never `use_when`. An advertisement written for one
        backbone's hop 0 has no reason to be true in another's — a subsidiary's "needs head-office
        approval" means nothing read at head office. So each is written for its reader, and the one
        for the outside goes through the review queue like every other advertisement (scope `peer`).
        """
        token = self.headers.get("X-Peer-Token") or ""
        who = _peer_by_token(token)
        if not PEER_TOKEN and not any(p["token"] for p in peering.declared(DATA)):
            return self._err(501, "this backbone advertises to no peer — set ONTOLOGY_PEER_TOKEN to open a link")
        if not who and not (PEER_TOKEN and token == PEER_TOKEN):
            return self._err(401, "peer token missing or wrong")

        # Who is on the other end of the line, and who they are asking for. The two are the same
        # thing on a direct link and are not behind an exchange: there, the caller is the room and
        # the reader is one of its members, so the room says which. It is believed only when this
        # backbone's own peers.yaml calls it an exchange — a claim that gets a caller *more* is
        # exactly the one that must not be taken on the caller's word.
        reader = who["name"] if who else None
        if who and who["kind"] == "exchange":
            reader = (self.headers.get("X-Peer-For") or "").strip() or who["name"]

        rj = store.regions_json()
        shared = {r["source"].replace("_", "-"): r for r in rj.get("regions", [])
                  if (r.get("use_when_export") or "").strip()}
        # An audience narrows what the line opened. Fail closed twice over: an unnamed caller is
        # nobody, and a restricted area is invisible to nobody. Only a room is handed rows it may not
        # pass on — it is the one doing the filtering for its members, and it can only do that if it
        # can see what it is filtering, which is the same thing as saying an exchange on the data
        # path sees everything. docs/PEERING.md says so where it says who should run one.
        to_a_room = bool(who) and who["kind"] == "exchange" and not (self.headers.get("X-Peer-For") or "").strip()
        visible = {k: r for k, r in shared.items() if _visible(r, reader)}
        if not to_a_room: shared = visible
        # The revision the peer is being told about. It is what makes staleness visible on the other
        # side: git already numbers every state this repository has been in, so a link needs no clock.
        rev = head(DATA)

        if parts == ["regions"]:
            return self._send(200, {"revision": rev, "schema": rj.get("schema"), "regions": [
                {"id": r["id"], "source": r["source"], "title": r["title"],
                 "description": r.get("description", ""),
                 # Named `use_when` because that is what it is to the reader: the line it chooses by.
                 # Which side of the link it was written for is our business, not theirs.
                 "use_when": r["use_when_export"], "representative": r.get("representative"),
                 # Carried only to a room, which needs it to filter for its members. A backbone that
                 # is being answered directly has already been filtered for and has no business
                 # knowing who else was considered.
                 **({"export_to": r.get("export_to") or []} if to_a_room and r.get("export_to") else {}),
                 "fetch": f"/v1/export/regions/{src}"}
                for src, r in sorted(shared.items())]})

        # A document is always answered from the narrow set. The listing may be handed to a room
        # whole so that it can filter; the prose never is. A room asking for a body without saying
        # who it is for is asking for itself, and a room is not an audience.
        if len(parts) == 2 and parts[0] == "regions":
            if parts[1] not in visible: return self._err(404, f"no exported area {parts[1]}")
            self._as_peer = True
            return self._get(["regions", parts[1]])

        if len(parts) >= 2 and parts[0] == "nodes":
            n = store.node(parts[1])
            # 404 and not 403: whether this backbone holds a thing it has not shared is itself
            # something the peer has no business learning. The two answers must be indistinguishable.
            if not n or (n.get("region") or "") not in {r["source"] for r in visible.values()}:
                return self._err(404, f"no exported node {parts[1]}")
            self._as_peer = True
            return self._get(parts)

        return self._err(404, "unknown export path")

    # ---- reads ----
    def _get(self, parts):
        if parts == ["core"]: return self._send(200, store.core(), "text/markdown; charset=utf-8")
        if parts == ["revision"]: return self._send(200, {"head": head(DATA), "published": store_published()})
        if parts == ["vocab"]: return self._send(200, store.vocab())
        if parts == ["graph"]: g = store.graph(); g["revision"] = head(DATA); return self._send(200, g)
        if parts == ["edges"]: return self._send(200, {"revision": head(DATA), "edges": store.edges()})
        if parts == ["regions"]:
            q = dict(x.split("=", 1) for x in urlparse(self.path).query.split("&") if "=" in x)
            expand = q.get("expand") == "entries"
            # A listing is an advertisement too. `path` and `nodes` stay in regions.json but are
            # **not emitted**: publish a path and someone builds an address out of it (someone did),
            # and `nodes` is internal bookkeeping the validator uses to catch drift against the
            # directory, not something a caller should act on. There is one way to go: `fetch`.
            rj = store.regions_json()
            def entries_of(rep_id):
                rep = next((n for n in store.nodes() if n["id"] == rep_id), None)
                if not rep: return []
                return [_advert_child(c) for c in advertised(rep_id)]
            mine = [
                {"id": r["id"], "source": r["source"], "title": r["title"], "description": r.get("description", ""),
                 "use_when": r.get("use_when", ""), "representative": r.get("representative"),
                 "fetch": f"/v1/regions/{r['source'].replace('_', '-')}",
                 **({"entries": entries_of(r.get("representative"))} if expand else {})}
                for r in rj.get("regions", [])]
            theirs, links = peering.rows(DATA)
            return self._send(200, {"revision": head(DATA), "schema": rj.get("schema"),
                                    "regions": mine + theirs,
                                    **({"links": links, "absence": _absence(links)} if links else {})})
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
                 "expands_in": n.get("expands_in"), "aliases": n["aliases"],
                 "status": n["status"], "injected_by": n.get("injected_by"), "order": n["order"],
                 "fetch": f"/v1/nodes/{n['id']}"} for n in store.nodes()]})
        if len(parts) == 2 and parts[0] == "nodes":
            n = store.node(parts[1])
            if not n: return self._err(404, f"node {parts[1]} not found")
            # A representative may contain other representatives (SPEC-v2 §1.1) — what it carries comes with it
            # Under one type a file IS a child: one row per entity, carrying its own address.
            # Listing `files` as well would advertise everything twice, at two addresses, for one
            # thing — which is what made a single-file node draw itself as a node on the map.
            return self._send(200, {**{k: v for k, v in n.items() if k not in _NODE_INTERNAL},
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
        if parts == ["validate"]: return self._send(200, validate(store))
        if len(parts) == 2 and parts[0] == "curator":
            q = dict(x.split("=", 1) for x in urlparse(self.path).query.split("&") if "=" in x)
            if parts[1] == "proposals": return self._send(200, {"proposals": cstore().proposals(q.get("status"))})
            if parts[1] == "last-sleep": return self._send(200, cstore().last_sleep())
            if parts[1] == "observations":
                rows = cstore().observations()
                return self._send(200, {"observations": rows[-500:], "total": len(rows),
                                        "since_last_sleep": max(0, len(rows) - int(str(cstore().last_sleep().get("log_position") or "0").split("-")[0]))})
        if parts == ["services"]:
            if not svc_store: return self._err(501, "ONTOLOGY_SERVICES is not configured")
            return self._send(200, {"revision": head(SERVICES), "services": [
                {**{k: v for k, v in s.items() if k not in _SERVICE_INTERNAL},
                 "files": [_advert_service_file(s["id"], f) for f in (s.get("files") or [])],
                 "fetch": f"/v1/services/{s['id']}"} for s in svc_store.services()]})
        if len(parts) == 2 and parts[0] == "services":
            if not svc_store: return self._err(501, "ONTOLOGY_SERVICES is not configured")
            s = svc_store.service(parts[1])
            if not s: return self._err(404, f"no fragment for service {parts[1]}")
            # A fragment's files carry their own fetch too — this was the last place an address was assembled
            return self._send(200, {**{k: v for k, v in s.items() if k not in _SERVICE_INTERNAL},
                                    "files": [_advert_service_file(parts[1], f) for f in (s.get("files") or [])]})
        if len(parts) == 4 and parts[0] == "services" and parts[2] == "files":
            if not svc_store: return self._err(501, "ONTOLOGY_SERVICES is not configured")
            t = svc_store.file(parts[1], parts[3])
            return self._send(200, t, "text/plain; charset=utf-8") if t is not None else self._err(404, "file not listed in the fragment's `## Files`")
        if parts == ["services-validate"]:
            if not svc_store: return self._err(501, "ONTOLOGY_SERVICES is not configured")
            return self._send(200, validate_services(svc_store, PUBLISH))
        if len(parts) == 4 and parts[0] == "services" and parts[2] == "fragment":
            p = writer.fragment_path(parts[1], parts[3])
            return self._send(200, p.read_text(encoding="utf-8"), "text/plain; charset=utf-8") if p.exists() else self._err(404, "no such fragment")
        if len(parts) == 3 and parts[0] == "services" and parts[2] == "fragment":
            d = writer.fragment_path(parts[1], "x.md").parent
            return self._send(200, {"service": parts[1], "files": sorted(p.name for p in d.iterdir() if p.is_file()) if d.exists() else []})
        return self._err(404, "unknown path")

    # ---- writes ----
    def _write(self, method, parts):
        actor = self._actor(); body = self._body()
        if parts == ["suggest", "use-when"] and method == "POST":
            name, one = str(body.get("name") or "").strip(), str(body.get("one_liner") or "").strip()
            if not name or not one: return self._err(400, "name and one_liner are required")
            return self._send(200, {"use_when": suggest_use_when(name, one, str(body.get("core_description") or "").strip())})
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
        if parts == ["curator", "sleep"] and method == "POST":
            return self._send(200, curator.sleep(store, svc_store, cstore(), PUBLISH, SERVICE_PUBLISH, llm_client(), dry_run=bool(body.get("dry_run")),
                                                 mode=body.get("mode") or "sleep", create_draft=lambda d, ev: create_draft(d, ev, actor), svc_writer=svc_writer))
        if len(parts) == 4 and parts[0] == "curator" and parts[1] == "proposals" and method == "POST":
            status = {"accept": "accepted", "reject": "rejected"}.get(parts[3])
            if not status: return self._err(404, "accept | reject")
            return self._send(200, curator.decide(cstore(), parts[2], status, body.get("why"), lambda p: apply_proposal(p, actor), body.get("override"),
                                                  discard_draft=lambda nid: discard_draft(nid, actor)))
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
            try: return self._send(201, curator.submit_route(cstore(), body, actor))
            except ValueError as e: return self._err(422, str(e))
        if parts == ["curator", "observations"] and method == "POST":
            try: return self._send(201, cstore().record_observations(body))
            except ValueError as e: return self._err(422, str(e))
        if len(parts) == 2 and parts[0] == "regions" and method == "DELETE":
            return self._send(200, writer.delete_region(parts[1], actor))
        if parts == ["regions"] and method == "POST":
            # The representative node and the CORE row are one transaction — a title-only row at hop 0 never gets chosen
            return self._send(201, writer.create_region(body, actor))
        if len(parts) == 3 and parts[0] == "core" and parts[1] == "regions" and method == "PUT":
            # One row's description cell only. No whole-document write — CORE.md is carried whole into every prompt
            return self._send(200, writer.put_core_row(parts[2], body.get("description"), actor))
        if parts == ["publish"] and method == "POST":
            if not PUBLISH: return self._err(501, "ONTOLOGY_PUBLISH is not configured")
            return self._send(200, {"ok": True, "revision": publish(DATA, PUBLISH, body.get("revision"), keep=pinned_core_revisions())})
        if parts == ["vocab"]: return self._err(405, "vocabulary and kinds change through Knowledge review, not this API (operator decision 2026-09-07)")
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
        if parts == ["edges"] and method == "POST": return self._send(201, writer.add_edge(body, actor))
        if len(parts) == 4 and parts[0] == "edges":
            if method == "PUT": return self._send(200, writer.update_edge(parts[1], parts[2], parts[3], body, actor))
            if method == "DELETE": return self._send(200, writer.delete_edge(parts[1], parts[2], parts[3], actor))
        if parts == ["services"] and method == "POST": return self._send(201, need_services().create_service(body, actor))
        if len(parts) == 2 and parts[0] == "services":
            if method == "PUT": return self._send(200, need_services().update_service(parts[1], body, actor))
            if method == "DELETE": return self._send(200, need_services().delete_service(parts[1], actor))
        if len(parts) == 4 and parts[0] == "services" and parts[2] == "files":
            if method == "PUT":
                return self._send(200, need_services().put_file(parts[1], parts[3], body.get("content", ""), body.get("description", ""), actor))
            if method == "DELETE": return self._send(200, need_services().delete_file(parts[1], parts[3], actor))
        if parts == ["services-publish"] and method == "POST":
            w = need_services()
            if not SERVICE_PUBLISH: return self._err(501, "ONTOLOGY_SERVICE_PUBLISH is not configured")
            return self._send(200, {"ok": True, "revision": w.publish_head()})
        if len(parts) == 4 and parts[0] == "services" and parts[2] == "fragment" and method == "PUT":
            return self._send(200, writer.put_fragment(parts[1], parts[3], body.get("content", "")))
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


def _export_state():
    """What this backbone advertises across a link, as one comparable value: which areas, the line
    each shows, and who each is for. Deliberately not the git revision — most commits change nothing
    a peer can see, and a poke on every save would tell every peer to re-read for somebody fixing a
    typo in a document body."""
    try:
        return sorted((r.get("source"), r.get("use_when_export") or "", tuple(r.get("export_to") or []))
                      for r in (store.regions_json().get("regions") or []))
    except Exception:
        return None


def _peer_by_token(token: str) -> dict | None:
    """Which declared peer presented this, if any.

    The door still opens for the shared `ONTOLOGY_PEER_TOKEN`, which is what a single-link install
    has and all it needs. What a *named* caller buys is the only thing that needs a name: an audience
    written on an area is a list of peers, and a list of peers is worthless against a caller nobody
    can tell apart. One secret per peer, in both directions — the rule the exchange already keeps —
    is what makes the two ends of a link know each other, and it is declared in the same peers.yaml
    that says who this backbone reads.
    """
    if not token: return None
    return next((p for p in peering.declared(DATA) if p["token"] and p["token"] == token), None)


def _visible(region: dict, reader: str | None) -> bool:
    """May this reader see this area at all.

    Absent audience is the common case and means everyone the area is exported to. A named audience
    narrows it and can never widen it: an area with no `use_when_export` never gets here.

    Fail closed on both unknowns. A caller this backbone cannot name is not on any list, and neither
    is a reader an exchange declined to name — so a restricted area is invisible to both. The
    alternative reads far better and is the bug: an unnamed caller falling through to "no audience
    was matched, so show it" is how a restriction becomes a decoration.
    """
    aud = region.get("export_to") or []
    return not aud or (bool(reader) and reader in aud)


def _absence(links) -> str:
    """What this backbone is entitled to claim, given the state of its links.

    The absence rule is the load-bearing sentence of the whole design — *only hop 0 may say something
    is not here* — and it is true because hop 0 is the whole world. A link makes that false: the world
    is now this list plus what the peers advertise. So the sentence is computed rather than written
    down, because the only thing that knows whether it still holds is the thing that just tried to
    read every peer.

    With a link down there is no honest version of it. The answer is not a smaller claim, it is no
    claim: a table that is missing rows cannot be the grounds for saying anything is missing. Saying
    so out loud is the difference between an agent that reports what it could not see and one that
    reports that something does not exist.
    """
    down = [l for l in links if not l["reachable"]]
    if not down:
        # Only the links that actually brought something. A link that is up and advertising nothing
        # adds nothing to the world, so the plain sentence is not merely acceptable there — it is the
        # accurate one, and naming an empty link would tell a reader to expect rows that are not
        # coming. It also stops an install with one backbone from announcing "the backbones it is
        # linked to (EXCHANGE)", which names as a backbone the one thing that is careful not to be.
        named = ", ".join(l["label"] for l in links if l.get("areas"))
        if not named:
            return ("Nothing outside this list exists in RouteMind. This list is the grounds on which "
                    "you may say something is absent — no smaller table is.")
        return (f"Nothing outside this list exists in RouteMind or in the backbones it reaches "
                f"through {named}. This list is the grounds on which you may say something is absent "
                f"— no smaller table is.")
    why = "; ".join(f"{l['label']}: {l['error']}" for l in down)
    return ("**This list is incomplete.** " + ("A link" if len(down) == 1 else "Links") +
            f" could not be read ({why}), so areas that exist may be missing from it. Answer from what "
            f"is here if you can, and say what you could not reach — but do not say anything is absent "
            f"while a link is down. Nobody has spoken for what is behind it.")


def store_published():
    p = PUBLISH / "REVISION" if PUBLISH else None
    return p.read_text().strip() if p and p.exists() else None


def main():
    if not DATA.is_dir(): sys.exit(f"ONTOLOGY_DATA {DATA} is not a directory")
    res = validate(store)
    sys.stderr.write(f"iris-ontology data={DATA} head={head(DATA)} publish={PUBLISH} fragments={FRAGMENTS} nodes={res['stats']['nodes']} edges={res['stats']['edges']} valid={res['ok']}\n")
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
    if PUBLISH and res["ok"] and head(DATA):
        try: publish(DATA, PUBLISH, keep=pinned_core_revisions()); sys.stderr.write(f"published {store_published()}\n")
        except WriteError as e: sys.stderr.write(f"  publish failed: {e}\n")
    # Fragments are validated against the *published* Core, so this must come after Core's publish.
    if svc_store:
        sres = validate_services(svc_store, PUBLISH)
        sys.stderr.write(f"iris-ontology services={SERVICES} head={head(SERVICES)} publish={SERVICE_PUBLISH} {sres['stats']} valid={sres['ok']}\n")
        for e in sres["errors"]: sys.stderr.write(f"  SERVICE ERROR {e}\n")
        if SERVICE_PUBLISH and sres["ok"] and head(SERVICES):
            try: publish(SERVICES, SERVICE_PUBLISH, head(SERVICES)); sys.stderr.write(f"published services {head(SERVICES)}\n")
            except WriteError as e: sys.stderr.write(f"  service publish failed: {e}\n")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
