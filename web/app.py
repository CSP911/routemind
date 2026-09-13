#!/usr/bin/env python3
"""RouteMind Web — the map, and a server-side proxy to the ontology API.

Everything a person does here is a call to the ontology API. Nothing about the domain lives in this
file: it carries a request across the network, checks the shapes it can check cheaply, and hands the
answer back. That is why it can be read in one sitting and why a new domain needs no change here.

The proxy is server-side on purpose. The ontology API is not published to the browser, so the only
way to reach it is through a request this file made — which is also where the actor is stamped.

No authentication (operator decision, 2026-09-11). The map is reachable by anyone who can reach the
port. Two things follow and both are deliberate:

  * Every write API is open. Put this on a network where that is acceptable, or put a reverse proxy
    with authentication in front of it. The README says so in the first paragraph.
  * The `actor` on a commit, a proposal and an approval would otherwise all read "web", which makes
    the record useless for the one thing a record is for. The browser sends a name the person typed
    once (kept in their own browser); the server falls back to KNOWLEDGE_ACTOR, then to "web". It is
    a signature, not a credential — never treat it as one.
"""
from __future__ import annotations

import json as _iris_playbook_json
import os as _iris_playbook_os
import re as _iris_re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError as _IrisPlaybookHTTPError, URLError as _IrisPlaybookURLError
from urllib.parse import quote, unquote
from urllib.request import Request as _IrisPlaybookURLRequest, urlopen as _iris_playbook_urlopen

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi import HTTPException as _IrisPlaybookHTTPException
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(_iris_playbook_os.environ.get("KNOWLEDGE_STATIC", Path(__file__).resolve().parent.parent / "static"))
# Where a run is started, when there is anywhere to start one. Empty (the default) hides the button
# rather than leaving one that goes nowhere: the areas a person picked are the whole input to a run,
# and a button that drops them on the floor teaches that picking does not matter.
AGENT_URL = str(_iris_playbook_os.environ.get("KNOWLEDGE_AGENT_URL") or "").strip().rstrip("/")
DEFAULT_ACTOR = (str(_iris_playbook_os.environ.get("KNOWLEDGE_ACTOR") or "web").strip() or "web")[:64]

app = FastAPI(title="RouteMind", docs_url=None, redoc_url=None, openapi_url=None)

_MCP = None


def _renderer():
    """The MCP server, imported for its formatter. One renderer, three consumers — a connected agent,
    this popup, and the block the map copies for an agent that has no MCP. Three descriptions of one
    ontology would drift, and the one that drifts is the one nobody checks."""
    global _MCP
    if _MCP is None:
        here = Path(__file__).resolve().parent
        for cand in (here / "mcp", here.parent / "mcp"):      # in the image, and in a checkout
            if (cand / "knowledge_mcp.py").exists():
                sys.path.insert(0, str(cand)); break
        import knowledge_mcp
        _MCP = knowledge_mcp
    return _MCP


def _iris_route(method: str, path: str, **options: Any):
    """The same decorator the routes were written against, registering straight onto the app."""
    def decorator(endpoint):
        app.add_api_route(path, endpoint, methods=[str(method).upper()], **options)
        return endpoint
    return decorator


class KnowledgeError(HTTPException):
    """An answer from the ontology API, with the reasons it gave.

    A refusal arrives as `{"error": "...", "details": ["node x: kind 'y' not in vocab", ...]}`. The
    headline alone is "validation failed — nothing was written", which tells a person that something
    is wrong and nothing about what. The screen is written to print `details[]`; this is what puts
    them in the response for it to print.

    It subclasses HTTPException so that every `except HTTPException` already in this file still
    catches it, and the handler below wins because Starlette matches the most specific class first.
    """
    def __init__(self, status_code: int, detail: str, details: list[str] | None = None,
                 reason: str | None = None, values: dict[str, Any] | None = None):
        super().__init__(status_code=status_code, detail=detail)
        self.details = [str(d) for d in (details or []) if str(d).strip()]
        # `detail` is the sentence and stays the whole answer. `reason` names which refusal this is
        # and `values` holds what is inside it, so a screen can say the same thing in its own
        # language — see WriteError in ontology/service/write.py. Both are optional and most
        # refusals carry neither.
        self.reason, self.values = reason, values or {}


@app.exception_handler(KnowledgeError)
async def _knowledge_error(request: Request, exc: KnowledgeError) -> JSONResponse:
    body: dict[str, Any] = {"detail": exc.detail}
    if exc.details: body["details"] = exc.details
    if exc.reason: body["reason"] = exc.reason
    if exc.values: body["values"] = exc.values
    return JSONResponse(status_code=exc.status_code, content=body)


_ACTOR_OK = _iris_re.compile(r"^[\w .@-]{1,64}$", _iris_re.UNICODE)


def _require_admin(request: Request) -> dict[str, Any]:
    """There is no gate. Kept as a seam: putting one back is this function and nothing else."""
    return {}


def _request_user(request: Request) -> dict[str, Any]:
    # Percent-encoded on the way in, because HTTP headers are latin-1 and a name with a Korean — or
    # accented, or any non-ASCII — character otherwise arrives as mojibake, fails the check, and is
    # replaced by the default. Every commit then reads "web" and nobody notices until they look.
    raw = str(request.headers.get("X-Knowledge-Actor") or "")
    try: name = unquote(raw, errors="strict").strip()
    except Exception: return {}
    return {"username": name} if name and _ACTOR_OK.match(name) else {}


# Knowledge unit (docker/pi/ontology/SPEC-curator.md); Web only carries a person's decision to it. Server-side
# proxy on the compose network, so the ontology API needs no published port and the browser never calls it.
# The actor recorded there is the signed-in username, never a client-supplied value.
ONTOLOGY_URL = _iris_playbook_os.environ.get("KNOWLEDGE_API_URL", "http://ontology:8100").rstrip("/")

def _ontology_proxy(method: str, path: str, actor: str, payload: dict | None = None) -> dict:
    body = _iris_playbook_json.dumps(payload).encode("utf-8") if payload is not None else None
    proxy_request = _IrisPlaybookURLRequest(
        ONTOLOGY_URL + path,
        data=body,
        method=method,
        # The actor is percent-encoded because this header is latin-1 too: a Korean name that survived
        # the browser hop dies on this one, as an exception rather than a wrong value.
        headers={"Content-Type": "application/json", "Accept": "application/json", "X-Actor": quote((actor or "web")[:64], safe="")},
    )
    try:
        with _iris_playbook_urlopen(proxy_request, timeout=180) as response: raw = response.read()
    except _IrisPlaybookHTTPError as exc:
        detail, details, reason, values = None, [], None, None
        try:
            answer = _iris_playbook_json.loads(exc.read().decode("utf-8"))
            detail = answer.get("error")
            # The reasons, not just the headline. Dropping these left every refused write reading
            # "validation failed — nothing was written", which is exactly as useful as silence.
            if isinstance(answer.get("details"), list): details = answer["details"]
            # Carried through untouched, and not interpreted here. This layer has no opinion about
            # what a refusal means; it only has to not lose it on the way past. Deciding here which
            # reasons are worth forwarding is how the screen ends up unable to translate one.
            reason = answer.get("reason") or None
            if isinstance(answer.get("values"), dict): values = answer["values"]
        except Exception: pass
        # The API's own 4xx are answers, not transport failures: "no such fragment" is a 404 and "already
        # exists" is a 409. Collapsing them into 502 makes the status line lie while the sentence tells the
        # truth, and anything branching on status branches wrong.
        #
        # 503 is an answer too, and it was being collapsed. "no LLM is configured" arrived at the screen
        # as 502 Bad Gateway — the sentence still said what to set, but every check and every caller
        # branching on the status saw a broken upstream. The rule is not "4xx"; it is "did the API mean
        # this", and the only status it does not mean is its own 500. 501 is one it means as well — "this
        # install has no overlay store" — and a consumer deciding whether overlays exist branches on it.
        status = exc.code if (400 <= exc.code < 500 or exc.code in (501, 503)) else 502
        raise KnowledgeError(status, detail or f"RouteMind API returned HTTP {exc.code}.", details,
                             reason=reason, values=values) from exc
    except (_IrisPlaybookURLError, TimeoutError) as exc:
        raise _IrisPlaybookHTTPException(status_code=503, detail=f"RouteMind API unavailable: {exc}") from exc
    try: data = _iris_playbook_json.loads(raw.decode("utf-8"))
    except Exception as exc: raise _IrisPlaybookHTTPException(status_code=502, detail="Knowledge API returned an invalid response.") from exc
    if not isinstance(data, dict): raise _IrisPlaybookHTTPException(status_code=502, detail="Knowledge API response must be an object.")
    return data

def _ontology_text(pathname: str, actor: str) -> str:
    """Node/fragment file bodies are Markdown, not JSON — `_ontology_proxy` would choke on them."""
    proxy_request = _IrisPlaybookURLRequest(
        ONTOLOGY_URL + pathname, method="GET",
        headers={"Accept": "text/plain, text/markdown, */*", "X-Actor": quote((actor or "web")[:64], safe="")},
    )
    try:
        with _iris_playbook_urlopen(proxy_request, timeout=60) as response:
            return response.read().decode("utf-8", "replace")
    except _IrisPlaybookHTTPError as exc:
        raise _IrisPlaybookHTTPException(status_code=404 if exc.code == 404 else 502, detail=f"RouteMind API returned HTTP {exc.code}.") from exc
    except (_IrisPlaybookURLError, TimeoutError) as exc:
        raise _IrisPlaybookHTTPException(status_code=503, detail=f"RouteMind API unavailable: {exc}") from exc


_KNOWLEDGE_PROPOSAL_STATUS = ("pending", "accepted", "acknowledged", "answered", "rejected")
_KNOWLEDGE_ID = _iris_re.compile(r"^[a-z0-9][a-z0-9-]*$")
# A document's file name is its entity's address, so it follows the id rule — no `_`, no `.` in the
# stem. This allowed both, from when a file was only a file, and let through names the ontology then
# refused with a message about an "id" the person had never typed.
_KNOWLEDGE_FILE = _iris_re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
_KNOWLEDGE_PROPOSAL_ID = _iris_re.compile(r"^cp_[0-9a-f]{6,32}$")


def _knowledge_actor(request: Request) -> str:
    user = _request_user(request)
    return str(user.get("username") or "").strip() or DEFAULT_ACTOR


@_iris_route("GET", "/knowledge")
def knowledge_review_page(request: Request) -> FileResponse:
    _require_admin(request)
    return FileResponse(STATIC_DIR / "knowledge.html")


# ---- overlays (docs/OVERLAY.md): one question's working set, made by an agent or by a person ----
#
# Pass-through: the shapes and the refusals are Knowledge's, and this layer adds only what it is the one
# place to add — the actor. `by.name` is stamped from the actor header rather than taken from the body,
# the same rule every write here follows; `by.kind` says whether an agent or a person drew it.
_KNOWLEDGE_OVERLAY_ID = _iris_re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$")


def _overlay_id(overlay_id: str) -> str:
    if not _KNOWLEDGE_OVERLAY_ID.match(overlay_id or ""):
        raise HTTPException(status_code=422, detail="Invalid overlay id.")
    return quote(overlay_id, safe="")


@_iris_route("GET", "/api/knowledge/overlays")
def api_knowledge_overlays(request: Request, state: str = Query(default="")) -> dict[str, Any]:
    # A closed overlay's state is how it ended — answered or not_found — and one nobody closed is abandoned.
    if state and state not in ("open", "answered", "not_found", "abandoned"):
        raise HTTPException(status_code=422, detail="state must be open, answered, not_found or abandoned.")
    return _ontology_proxy("GET", "/v1/overlays" + ("?state=" + quote(state, safe="") if state else ""), _knowledge_actor(request))


@_iris_route("POST", "/api/knowledge/overlays")
def api_knowledge_create_overlay(payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    by = data.get("by") if isinstance(data.get("by"), dict) else {}
    kind = str(by.get("kind") or "person")
    if kind not in ("person", "agent"):
        raise HTTPException(status_code=422, detail="by.kind must be person or agent.")
    data["by"] = {"kind": kind, "name": actor}
    return _ontology_proxy("POST", "/v1/overlays", actor, data)


@_iris_route("GET", "/api/knowledge/overlays/{overlay_id}")
def api_knowledge_overlay(overlay_id: str, request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/overlays/" + _overlay_id(overlay_id), _knowledge_actor(request))


@_iris_route("PATCH", "/api/knowledge/overlays/{overlay_id}")
def api_knowledge_patch_overlay(overlay_id: str, payload: dict, request: Request) -> dict[str, Any]:
    return _ontology_proxy("PATCH", "/v1/overlays/" + _overlay_id(overlay_id), _knowledge_actor(request), dict(payload or {}))


@_iris_route("POST", "/api/knowledge/overlays/{overlay_id}/close")
def api_knowledge_close_overlay(overlay_id: str, payload: dict, request: Request) -> dict[str, Any]:
    return _ontology_proxy("POST", "/v1/overlays/" + _overlay_id(overlay_id) + "/close", _knowledge_actor(request), dict(payload or {}))


@_iris_route("GET", "/api/knowledge/proposals")
def api_knowledge_proposals(request: Request, status: str = Query(default="")) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if status and status not in _KNOWLEDGE_PROPOSAL_STATUS:
        raise HTTPException(status_code=422, detail="Unknown proposal status.")
    suffix = "?status=" + quote(status, safe="") if status else ""
    return _ontology_proxy("GET", "/v1/curator/proposals" + suffix, actor)


@_iris_route("GET", "/api/knowledge/last-sleep")
def api_knowledge_last_sleep(request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/curator/last-sleep", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/state")
def api_knowledge_state(request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    health = _ontology_proxy("GET", "/healthz", actor)
    out: dict[str, Any] = {
        "core_revision": str(health.get("published") or ""),
        "writable": bool(health.get("writable", True)),
        "uncommitted": str(health.get("uncommitted") or ""),
    }
    # The curator is optional and most installs do not configure it. Letting its absence fail this
    # call put "ONTOLOGY_HARNESS is not configured" across the top of the map on every default
    # install — a raw environment variable, from a subsystem the screen does not even display, as the
    # first thing a new person read.
    try: out["last_sleep"] = _ontology_proxy("GET", "/v1/curator/last-sleep", actor)
    except HTTPException: pass
    return out


@_iris_route("POST", "/api/knowledge/sleep")
def api_knowledge_sleep(payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    mode = str((payload or {}).get("mode") or "sleep")
    if mode not in ("sleep", "nap"):
        raise HTTPException(status_code=422, detail="mode must be sleep or nap.")
    return _ontology_proxy("POST", "/v1/curator/sleep", actor, {"mode": mode, "dry_run": bool((payload or {}).get("dry_run"))})


@_iris_route("POST", "/api/knowledge/suggest/description")
def api_knowledge_suggest_description(payload: dict, request: Request) -> dict[str, Any]:
    # A draft of the line a document is chosen by, read from its body. Draft only: the person puts it in
    # the field, edits it, and it is saved with the document when they press Create (operator,
    # 2026-09-11: every routing line is a person's; the LLM is a button).
    data = dict(payload or {})
    if not str(data.get("content") or "").strip():
        raise HTTPException(status_code=422, detail="content is required — the suggestion is read from the body.")
    body = {"name": str(data.get("name") or "document.md").strip(), "content": str(data["content"])}
    return _ontology_proxy("POST", "/v1/suggest/description", _knowledge_actor(request), body)


@_iris_route("POST", "/api/knowledge/suggest/id")
def api_knowledge_suggest_id(payload: dict, request: Request) -> dict[str, Any]:
    # An address for a name — the name's own slug when it is all ASCII, a translation when it is not.
    name = str((payload or {}).get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=422, detail="name is required.")
    return _ontology_proxy("POST", "/v1/suggest/id", _knowledge_actor(request), {"name": name})


@_iris_route("POST", "/api/knowledge/suggest/use-when")
def api_knowledge_suggest_use_when(payload: dict, request: Request) -> dict[str, Any]:
    # Drafting, not applying. What comes back goes into an editable box; the form sends whatever the
    # person left there, which may be nothing like this.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    body = {k: str(data.get(k) or "").strip() for k in ("name", "one_liner", "core_description")}
    if not body["name"] or not body["one_liner"]:
        raise HTTPException(status_code=422, detail="name and one_liner are required to draft a condition.")
    return _ontology_proxy("POST", "/v1/suggest/use-when", actor, body)


@_iris_route("POST", "/api/knowledge/route-draft")
def api_knowledge_route_draft(payload: dict, request: Request) -> dict[str, Any]:
    # What the Region holds that its own advertisement does not yet mention, and a sentence that would.
    # `changed` is a hint only: the screen knows what was just made, but not what was made yesterday and
    # is being submitted today, so working out what is missing is Knowledge's job and not this layer's.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    region = str(data.get("region") or "").strip()
    scope = str(data.get("scope") or "").strip()
    if not region:
        raise HTTPException(status_code=422, detail="region is required.")
    # `as` is the word since 2026-09-10; `dr` is still taken because Knowledge accepts both during the
    # handover and a proposal filed under the old spelling must stay reviewable.
    if scope not in ("as", "dr", "bb", "core"):
        raise HTTPException(status_code=422, detail="scope must be as, bb or core.")
    body: dict[str, Any] = {"region": region, "scope": scope}
    changed = data.get("changed")
    if isinstance(changed, list) and changed:
        body["changed"] = [str(x).strip() for x in changed if str(x).strip()][:40]
    return _ontology_proxy("POST", "/v1/curator/route-draft", actor, body)


@_iris_route("POST", "/api/knowledge/nodes/{node_id}/one-liner-draft")
def api_knowledge_one_liner_draft(node_id: str, request: Request) -> dict[str, Any]:
    # A draft for the row an entity shows in its holder's table, from its body and its siblings' rows.
    # A draft only: what goes up is what the person edits and submits, through the proposal queue.
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or ""):
        raise HTTPException(status_code=422, detail="Invalid node id.")
    return _ontology_proxy("POST", "/v1/nodes/" + quote(node_id, safe="") + "/one-liner-draft", actor, {})


@_iris_route("POST", "/api/knowledge/proposals")
def api_knowledge_create_proposal(payload: dict, request: Request) -> dict[str, Any]:
    # A person submitting a routing change. `after` is what they are submitting, which is the draft as
    # they edited it — never the draft itself, so a sentence nobody read cannot become a proposal.
    # `type` is not sent: the server stamps it, and a client that could choose the type could file a
    # routing change as something the reviewer reads differently.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    scope = str(data.get("scope") or "").strip()
    # `as` is the word since 2026-09-10; `dr` is still taken because Knowledge accepts both during the
    # handover and a proposal filed under the old spelling must stay reviewable.
    # `entity` is one row in a node's table — the line it shows in its holder's listing. It names the
    # entity and not an area: the entity settles where it is, and a second answer could disagree.
    if scope not in ("as", "dr", "bb", "core", "entity"):
        raise HTTPException(status_code=422, detail="scope must be as, bb, core or entity.")
    where = "entity" if scope == "entity" else "region"
    for field in (where, "after"):
        if not str(data.get(field) or "").strip():
            raise HTTPException(status_code=422, detail=f"{field} is required.")
    if where == "entity" and not _KNOWLEDGE_ID.match(str(data["entity"]).strip()):
        raise HTTPException(status_code=422, detail="entity must be an entity id.")
    body: dict[str, Any] = {
        "scope": scope, where: str(data[where]).strip(),
        "before": str(data.get("before") or ""), "after": str(data["after"]).strip(),
        "why": str(data.get("why") or "").strip(),
    }
    if str(data.get("target") or "").strip():
        body["target"] = str(data["target"]).strip()
    return _ontology_proxy("POST", "/v1/curator/proposals", actor, body)


@_iris_route("POST", "/api/knowledge/proposals/{proposal_id}/{decision}")
def api_knowledge_proposal_decide(proposal_id: str, decision: str, payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if decision not in ("accept", "reject"):
        raise HTTPException(status_code=422, detail="decision must be accept or reject.")
    if not _KNOWLEDGE_PROPOSAL_ID.match(str(proposal_id or "")):
        raise HTTPException(status_code=422, detail="Invalid proposal id.")
    body: dict[str, Any] = {}
    why = str((payload or {}).get("why") or "").strip()
    if decision == "reject":
        if not why:
            raise HTTPException(status_code=422, detail="A reason is required to reject a proposal.")
        body["why"] = why[:600]
    elif why:
        body["why"] = why[:600]
    override = (payload or {}).get("override")
    if isinstance(override, dict) and isinstance(override.get("draft"), dict):
        body["override"] = {"draft": override["draft"]}
    return _ontology_proxy("POST", "/v1/curator/proposals/" + quote(proposal_id, safe="") + "/" + decision, actor, body)


# ---- ontology reading: what the editor needs before it can write ----

@_iris_route("GET", "/api/knowledge/revision")
def api_knowledge_revision(request: Request) -> dict[str, Any]:
    # The one cheap question the screen asks on a timer: has what the agent reads changed? `published`
    # is the revision the agent gets; `head` is what the repository holds. The screen follows the
    # former, so a commit that was not published does not redraw anything — the agent does not see it
    # either, and a map that ran ahead of the agent would be a map of something else.
    return _ontology_proxy("GET", "/v1/revision", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/graph")
def api_knowledge_graph(request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/graph", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/regions")
def api_knowledge_regions(request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/regions", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/view")
def api_knowledge_view(request: Request, path: str = Query(default=""), service: str = Query(default="")) -> dict[str, Any]:
    """What an agent is handed at this step, rendered by the code that hands it to them.

    This used to ask the agent runtime for it, so that the screen would never be a second
    implementation of the prompt. There is no such runtime here — and the reason survives the move:
    the renderer is `mcp/knowledge_mcp.py`, the same module an MCP client talks to. The popup shows
    the literal bytes a connected agent receives, because it is produced by the same function.

    `service` is accepted and ignored. It existed to give a run's service fragment as context; the
    address in `path` already names whatever is being looked at.
    """
    actor = _knowledge_actor(request)
    m = _renderer()
    # The renderer wants the v1 root; ONTOLOGY_URL stops one segment short of it.
    api = m.Api(ONTOLOGY_URL + "/v1", actor)
    target = path or "/v1/regions"
    try:
        # A table renders as a table; anything else is a document and is shown as written. Asking the
        # renderer which it is — rather than guessing from the address — is the same rule the agent
        # follows, so the popup cannot disagree with the agent about what a row is.
        if any(rx.match(target) for rx in m.TABLE_SHAPES) or target in ("/v1/regions", "/"):
            text = m.table_for(api, target)
        else:
            text = m.read_for(api, target) if target.startswith("/v1/") else m.hop0(api)
        status = "ok"
    except m.ApiError as exc:
        text, status = str(exc), "error"
    revision = ""
    try: revision = str(_ontology_proxy("GET", "/healthz", actor).get("published") or "")
    except HTTPException: pass
    return {"status": status, "text": text, "ontology_revision": revision}


@_iris_route("GET", "/api/knowledge/regions/{region_dir}")
def api_knowledge_region(region_dir: str, request: Request) -> dict[str, Any]:
    # The list row no longer says what a Region says about itself — since 2026-09-09 that lives on its
    # representative, and only this call returns it (`advertises`, the representative's `files`, and
    # `children`). The topology screen opens a Region with it.
    return _ontology_proxy("GET", "/v1/regions/" + quote(region_dir, safe=""), _knowledge_actor(request))


# ── what a linked backbone holds ──────────────────────────────────────────────
# One route with a wildcard tail, and deliberately not one per shape. Everything under /v1/peers/ is
# the ontology relaying somebody else's answer, and this layer has no opinion about what shape that
# answer has — inventing one here would mean a second place to update every time the addresses on the
# other side change, and the whole discipline is that addresses come from the table that printed them.
#
# Read-only, because a link is. The proxy has no write route for this and the ontology answers 405.
_PEER_SEG = _iris_re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")


@_iris_route("GET", "/api/knowledge/peers/{peer}/{rest:path}")
def api_knowledge_peer(peer: str, rest: str, request: Request):
    parts = [p for p in (rest or "").split("/") if p]
    if not _PEER_SEG.match(peer or "") or not parts or not all(_PEER_SEG.match(p) for p in parts):
        raise HTTPException(status_code=404, detail="not an address a table printed")
    path = "/v1/peers/" + "/".join(quote(p, safe="") for p in [peer, *parts])
    # A document body is Markdown on both sides of a link, so this route cannot assume JSON any more
    # than the local one can. Which it is follows the address, exactly as it does locally: `/body`
    # and a fragment file are text, everything else is a table.
    if parts[-1] == "body" or parts[-1].endswith((".md", ".yaml", ".yml")):
        return PlainTextResponse(_ontology_text(path, _knowledge_actor(request)),
                                 media_type="text/markdown; charset=utf-8")
    return _ontology_proxy("GET", path, _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/vocab")
def api_knowledge_vocab(request: Request) -> dict[str, Any]:
    # Kinds and relations are Knowledge's vocabulary; the editor offers only these and never a free-text kind.
    return _ontology_proxy("GET", "/v1/vocab", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/nodes/{node_id}")
def api_knowledge_node(node_id: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or ""):
        raise HTTPException(status_code=422, detail="Invalid node id.")
    return _ontology_proxy("GET", "/v1/nodes/" + quote(node_id, safe=""), actor)


@_iris_route("GET", "/api/knowledge/nodes/{node_id}/body")
def api_knowledge_node_body(node_id: str, request: Request) -> PlainTextResponse:
    """An entity's own document. A node and a file are one kind of thing, so an entity that has been
    written into has a body, and this is the address its advertisement carries.

    A 404 here means "nobody has written this yet", which the API distinguishes from "no such
    address" — the screen and an agent both need to tell those apart, so the status is passed through
    rather than flattened."""
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or ""):
        raise HTTPException(status_code=422, detail="Invalid node id.")
    return PlainTextResponse(_ontology_text("/v1/nodes/" + quote(node_id, safe="") + "/body", actor),
                             media_type="text/markdown; charset=utf-8")


@_iris_route("GET", "/api/knowledge/nodes/{node_id}/files/{filename}")
def api_knowledge_node_file(node_id: str, filename: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or "") or not _KNOWLEDGE_FILE.match(filename or ""):
        raise HTTPException(status_code=422, detail="Invalid node id or file name.")
    body = _ontology_text("/v1/nodes/" + quote(node_id, safe="") + "/files/" + quote(filename, safe=""), actor)
    return {"node": node_id, "name": filename, "content": body}


@_iris_route("POST", "/api/knowledge/validate")
def api_knowledge_validate(payload: dict, request: Request) -> dict[str, Any]:
    # Validation is read-only and free — the editor runs it before and after every write.
    return _ontology_proxy("POST", "/v1/validate", _knowledge_actor(request), {})


# ---- ontology writing: nodes and their data files ----

@_iris_route("POST", "/api/knowledge/regions")
def api_knowledge_create_region(payload: dict, request: Request) -> dict[str, Any]:
    # An AS is born with the two lines the agent uses to choose it, or it is born invisible. `use_when`
    # is the hop-0 condition and `core_description` becomes the CORE.md row behind it; the API requires
    # both, and this refuses without them rather than sending a request that will fail — an empty slot
    # meant to be filled later does not get filled.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    source = str(data.get("source") or "").strip()
    if not _KNOWLEDGE_ID.match(source):
        raise HTTPException(status_code=422, detail="source must be ASCII kebab-case.")
    rep = data.get("representative") if isinstance(data.get("representative"), dict) else {}
    for field, where in (("name", rep), ("one_liner", rep), ("use_when", rep)):
        if not str(where.get(field) or "").strip():
            raise HTTPException(status_code=422, detail=f"representative.{field} is required.")
    if not str(data.get("core_description") or "").strip():
        raise HTTPException(status_code=422, detail="core_description is required — it is the hop-0 row for this AS.")
    body: dict[str, Any] = {
        "source": source,
        "core_description": str(data["core_description"]).strip(),
        # `id` and `kind` are Knowledge's to derive, as they are for a node. Anything a person did
        # supply is passed through; nothing is invented here.
        # `use_when_export` is optional and its absence is meaningful: an area with none does not
        # cross a link at all. Passed through like the rest — the decision is the ontology's.
        "representative": {
            **{k: str(rep[k]).strip()
               for k in ("name", "one_liner", "use_when", "use_when_export", "kind", "id")
               if str(rep.get(k) or "").strip()},
            # A list, and passed as one. Who an area crosses to is the ontology's decision like the
            # rest of this; nothing here narrows or widens it.
            **({"export_to": rep["export_to"]} if rep.get("export_to") else {}),
        },
    }
    if isinstance(data.get("edges"), list) and data["edges"]:
        body["edges"] = data["edges"]
    return _ontology_proxy("POST", "/v1/regions", actor, body)


@_iris_route("DELETE", "/api/knowledge/regions/{region_dir}")
def api_knowledge_delete_region(region_dir: str, request: Request) -> dict[str, Any]:
    """Delete an area — its directory, its representative, the edges that named it and its CORE row,
    in one transaction.

    The API refuses while anything but the representative is still in it, and that refusal is passed
    through rather than worked around here. Deleting an area is how a person clears the examples this
    ships with, so it has to exist; deleting one with someone's work still inside it, because a
    screen looped over the contents on their behalf, is not the same act.
    """
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(region_dir or ""):
        raise HTTPException(status_code=422, detail="Invalid area name.")
    return _ontology_proxy("DELETE", "/v1/regions/" + quote(region_dir, safe=""), actor)


@_iris_route("POST", "/api/knowledge/nodes")
def api_knowledge_create_node(payload: dict, request: Request) -> dict[str, Any]:
    # A node needs a Region, a kind and a first relation — Knowledge's validator refuses a node nothing
    # relates to ("declare it only if something relates to it"). The form asks for all of it rather than
    # guessing a default, because a guessed Region is a wrong fact that publishes.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    for field in ("name", "region", "one_liner"):
        if not str(data.get(field) or "").strip():
            raise HTTPException(status_code=422, detail=f"{field} is required.")
    if str(data.get("id") or "").strip() and not _KNOWLEDGE_ID.match(str(data["id"]).strip()):
        raise HTTPException(status_code=422, detail="id must be ASCII kebab-case.")
    holds = str(data.get("holds") or "content")
    if holds not in ("content", "pointers"):
        raise HTTPException(status_code=422, detail="holds must be content or pointers.")
    files = data.get("files") if isinstance(data.get("files"), list) else []
    edges = data.get("edges") if isinstance(data.get("edges"), list) else []
    body: dict[str, Any] = {
        "name": str(data["name"]).strip(),
        "region": str(data["region"]).strip(), "one_liner": str(data["one_liner"]).strip(),
        "holds": holds, "injected_by": str(data.get("injected_by") or "operator"),
        "files": files, "edges": edges,
    }
    # Sent only when supplied; absent means Knowledge derives it. `kind` decides which relations the
    # validator will allow, and relations are the curator's business — so this is not a value Web
    # invents a default for (operator, 2026-09-10).
    for field in ("id", "kind"):
        if str(data.get(field) or "").strip():
            body[field] = str(data[field]).strip()
    # A node made inside a node. Absent means the area's representative holds it, as before.
    if str(data.get("parent") or "").strip():
        if not _KNOWLEDGE_ID.match(str(data["parent"]).strip()):
            raise HTTPException(status_code=422, detail="parent must be an entity id.")
        body["parent"] = str(data["parent"]).strip()
    if data.get("aliases"):
        body["aliases"] = data["aliases"]
    if data.get("status"):
        body["status"] = data["status"]
    return _ontology_proxy("POST", "/v1/nodes", actor, body)


@_iris_route("PUT", "/api/knowledge/nodes/{node_id}")
def api_knowledge_update_node(node_id: str, payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or ""):
        raise HTTPException(status_code=422, detail="Invalid node id.")
    # Deliberately shorter than the API's EDITABLE, which also takes `use_when` and `expands_in`.
    # Those two are not omissions:
    #   use_when   is the hop-0 routing signal — the one every run reads before choosing a Region.
    #              Changing it goes through the proposal queue so a record exists (operator,
    #              2026-09-10: "no immediate-apply path"). Accepting a proposal applies it inside Knowledge;
    #              Web never writes it, and adding it here would be the immediate path that decision
    #              ruled out.
    #   expands_in says where a node's depth lives outside the ontology; nothing on this screen knows.
    # `parent` was the third, as "containment is the curator's to decide, not a person's". That had
    # stopped being true before it was reversed: creating a document under a node, creating a node and
    # promotion all set containment directly. On 2026-09-11 the operator asked for it outright — drag an
    # entity onto what should hold it. The tables are read off `parent`, so both change with the write;
    # Knowledge refuses a parent in another area and a loop, so neither is re-checked here.
    allowed = {k: v for k, v in (payload or {}).items() if k in ("name", "kind", "one_liner", "aliases", "holds", "status", "parent")}
    if "parent" in allowed and not _KNOWLEDGE_ID.match(str(allowed["parent"] or "")):
        raise HTTPException(status_code=422, detail="parent must be an entity id.")
    if not allowed:
        raise HTTPException(status_code=422, detail="Nothing to update. Renaming and moving Regions are not supported.")
    return _ontology_proxy("PUT", "/v1/nodes/" + quote(node_id, safe=""), actor, allowed)


@_iris_route("DELETE", "/api/knowledge/nodes/{node_id}")
def api_knowledge_delete_node(node_id: str, request: Request) -> dict[str, Any]:
    # Deleting a node takes its edges with it — the API answers with which ones, and the screen shows them.
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or ""):
        raise HTTPException(status_code=422, detail="Invalid node id.")
    # Not while it holds another node (operator, 2026-09-11). Knowledge deletes a subtree in one
    # transaction, which is right for documents — they go with what holds them — and wrong for a
    # structure someone built inside it. Held here, not only on the screen, so every client of this
    # proxy gets the same rule.
    record = _ontology_proxy("GET", "/v1/nodes/" + quote(node_id, safe=""), actor)
    held = [str(e.get("id")) for e in (record.get("entries") or []) if e.get("type") in ("dr", "empty")]
    if held:
        raise KnowledgeError(409, f"{node_id} holds {len(held)} node(s) — delete or move them out first.", held,
                             reason="holds_children", values={"id": node_id, "n": len(held), "held": ", ".join(held)})
    return _ontology_proxy("DELETE", "/v1/nodes/" + quote(node_id, safe=""), actor)


@_iris_route("PUT", "/api/knowledge/nodes/{node_id}/files/{filename}")
def api_knowledge_put_node_file(node_id: str, filename: str, payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or "") or not _KNOWLEDGE_FILE.match(filename or ""):
        raise HTTPException(status_code=422, detail="Invalid node id or file name.")
    if filename == "INDEX.md":
        raise HTTPException(status_code=422, detail="INDEX.md is generated from the node, not edited directly.")
    data = payload or {}
    if "content" not in data:
        raise HTTPException(status_code=422, detail="content is required.")
    # `description` is the line the agent routes by, and as of 2026-09-10 it is Knowledge's to write
    # from the document, not a field a person types. Absent is passed through as absent: on an edit the
    # API keeps the existing line, and on a new file it is Knowledge that has to supply one. Sending
    # `""` here would look like an intentional blank and is not the same thing.
    body: dict[str, Any] = {"content": str(data.get("content") or "")}
    if str(data.get("description") or "").strip():
        body["description"] = str(data["description"]).strip()
    return _ontology_proxy("PUT", "/v1/nodes/" + quote(node_id, safe="") + "/files/" + quote(filename, safe=""), actor, body)


@_iris_route("GET", "/api/knowledge/services")
def api_knowledge_services(request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/services", _knowledge_actor(request))


@_iris_route("GET", "/api/knowledge/services/{service_id}")
def api_knowledge_service(service_id: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    return _ontology_proxy("GET", "/v1/services/" + quote(service_id, safe=""), actor)


@_iris_route("GET", "/api/knowledge/services/{service_id}/files/{filename}")
def api_knowledge_service_file(service_id: str, filename: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    _knowledge_fragment_name(filename)
    body = _ontology_text("/v1/services/" + quote(service_id, safe="") + "/files/" + quote(filename, safe=""), actor)
    return {"service": service_id, "name": filename, "content": body}


@_iris_route("POST", "/api/knowledge/services")
def api_knowledge_create_service(payload: dict, request: Request) -> dict[str, Any]:
    # `core_revision` is what makes the fragment's references checkable — the API requires it, and the screen
    # offers the current Core revision rather than letting a person type one.
    actor = _knowledge_actor(request)
    data = dict(payload or {})
    service = str(data.get("service") or "").strip()
    if not _KNOWLEDGE_SERVICE.match(service):
        raise HTTPException(status_code=422, detail="service id must be lowercase letters, digits and underscore.")
    for field in ("one_liner", "core_revision"):
        if not str(data.get(field) or "").strip():
            raise HTTPException(status_code=422, detail=f"{field} is required.")
    body: dict[str, Any] = {"service": service, "one_liner": str(data["one_liner"]).strip(),
                            "core_revision": str(data["core_revision"]).strip()}
    for field in ("publisher", "game_line", "updated"):
        if data.get(field):
            body[field] = str(data[field]).strip()
    if isinstance(data.get("regions"), list):
        body["regions"] = [str(x).strip() for x in data["regions"] if str(x).strip()]
    return _ontology_proxy("POST", "/v1/services", actor, body)


@_iris_route("PUT", "/api/knowledge/services/{service_id}")
def api_knowledge_update_service(service_id: str, payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    allowed = {k: v for k, v in (payload or {}).items()
               if k in ("one_liner", "core_revision", "publisher", "game_line", "regions", "updated")}
    if not allowed:
        raise HTTPException(status_code=422, detail="Nothing to update.")
    return _ontology_proxy("PUT", "/v1/services/" + quote(service_id, safe=""), actor, allowed)


@_iris_route("DELETE", "/api/knowledge/services/{service_id}")
def api_knowledge_delete_service(service_id: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    return _ontology_proxy("DELETE", "/v1/services/" + quote(service_id, safe=""), actor)


@_iris_route("PUT", "/api/knowledge/services/{service_id}/files/{filename}")
def api_knowledge_put_service_file(service_id: str, filename: str, payload: dict, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    _knowledge_fragment_name(filename)
    data = payload or {}
    if "content" not in data:
        raise HTTPException(status_code=422, detail="content is required.")
    if not str(data.get("description") or "").strip():
        raise HTTPException(status_code=422, detail="description is required — one line saying what this file holds.")
    return _ontology_proxy("PUT", "/v1/services/" + quote(service_id, safe="") + "/files/" + quote(filename, safe=""), actor,
                           {"content": str(data.get("content") or ""), "description": str(data["description"]).strip()})


@_iris_route("DELETE", "/api/knowledge/services/{service_id}/files/{filename}")
def api_knowledge_delete_service_file(service_id: str, filename: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_SERVICE.match(service_id or ""):
        raise HTTPException(status_code=422, detail="Invalid service id.")
    _knowledge_fragment_name(filename)
    return _ontology_proxy("DELETE", "/v1/services/" + quote(service_id, safe="") + "/files/" + quote(filename, safe=""), actor)


# ---- publishing: the moment a change reaches the agent ----
#
# Every write through this API already commits and republishes, so these two are the explicit way to say
# "publish what is committed now" — and, more importantly, the way the screen can show whether what the agent
# reads is what the repository holds. A draft node is stripped from the checkout at publish time, which is the
# rule that keeps the curator's own writing from coming back as evidence.

@_iris_route("GET", "/api/knowledge/publish-state")
def api_knowledge_publish_state(request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    health = _ontology_proxy("GET", "/healthz", actor)
    # Service fragments are optional and a standalone install has none. Asking for them unconditionally
    # made this whole answer a 502, and the screen quietly dropped the publish and validate state with it.
    try:
        services = _ontology_proxy("GET", "/v1/services", actor)
    except (HTTPException, KnowledgeError):
        services = {}
    head_rev = str(health.get("head") or "")
    published = str(health.get("published") or "")
    return {
        "core": {"head": head_rev, "published": published, "in_sync": bool(head_rev) and head_rev == published},
        "fragments": {"head": str(services.get("revision") or ""), "count": len(services.get("services") or [])},
        "validate": _ontology_proxy("POST", "/v1/validate", actor, {}),
    }


@_iris_route("POST", "/api/knowledge/publish")
def api_knowledge_publish(payload: dict, request: Request) -> dict[str, Any]:
    # `what` says which tree: the Core ontology, or the service fragments. They have separate repositories,
    # separate publish trees and separate validators, so they publish separately.
    actor = _knowledge_actor(request)
    what = str((payload or {}).get("what") or "core")
    if what == "core":
        check = _ontology_proxy("POST", "/v1/validate", actor, {})
        if not check.get("ok"):
            raise HTTPException(status_code=422, detail="Validation fails — publishing would hand the agent a broken map.")
        return _ontology_proxy("POST", "/v1/publish", actor, {})
    if what == "fragments":
        return _ontology_proxy("POST", "/v1/services-publish", actor, {})
    raise HTTPException(status_code=422, detail="what must be core or fragments.")


@_iris_route("POST", "/api/knowledge/services-validate")
def api_knowledge_validate_services(payload: dict, request: Request) -> dict[str, Any]:
    return _ontology_proxy("GET", "/v1/services-validate", _knowledge_actor(request))


@_iris_route("DELETE", "/api/knowledge/nodes/{node_id}/files/{filename}")
def api_knowledge_delete_node_file(node_id: str, filename: str, request: Request) -> dict[str, Any]:
    actor = _knowledge_actor(request)
    if not _KNOWLEDGE_ID.match(node_id or "") or not _KNOWLEDGE_FILE.match(filename or ""):
        raise HTTPException(status_code=422, detail="Invalid node id or file name.")
    return _ontology_proxy("DELETE", "/v1/nodes/" + quote(node_id, safe="") + "/files/" + quote(filename, safe=""), actor)


# ── the pages ─────────────────────────────────────────────────────────────────

@_iris_route("GET", "/")
def root() -> RedirectResponse:
    """Straight to the map. There is one screen here; a portal in front of one door is a door."""
    return RedirectResponse("/knowledge", status_code=307)


@_iris_route("GET", "/api/app-config")
def app_config() -> dict[str, Any]:
    """What the screen cannot know about this install: whether a run has anywhere to go, and whether
    an id and a kind can be derived or have to be typed. Both change what the screen must show, and
    a screen guessing either way is wrong for half the installs."""
    llm, health = False, {}
    try:
        health = _ontology_proxy("GET", "/healthz", "web")
        llm = bool(health.get("llm"))
    except HTTPException:
        pass   # The map says the API is unreachable on its own; this endpoint does not duplicate that.
    return {"agent": bool(AGENT_URL), "agent_url": AGENT_URL, "derives": llm,
            # Which provider is in use, and which this build understands. A provider it does not know
            # turns the LLM off, and "off" on its own reads as "I forgot to set a key" — these two
            # fields are what lets an install say the true thing instead.
            "llm_provider": health.get("llm_provider"),
            "llm_providers": health.get("llm_providers") or [],
            "actor_default": DEFAULT_ACTOR}


@app.middleware("http")
async def _revalidate_the_page(request: Request, call_next):
    """The page and its assets are revalidated on every load.

    Every asset was linked as `?v=0.1.0` and that string never changed, while the server sent no
    Cache-Control — so browsers cached heuristically and served an old script beside a new one. A day
    of fixes was reported as done while an open tab kept running what it had loaded first. `no-cache`
    means "ask before using", not "never store": the ETag makes an unchanged file a 304, so this costs
    a round trip and nothing else, and no one has to remember to bump a version string.
    """
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/static/") or path in ("/", "/knowledge"):
        response.headers["Cache-Control"] = "no-cache"
    return response


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def main() -> None:
    port = int(_iris_playbook_os.environ.get("PORT") or 8080)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    main()
