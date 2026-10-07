"""The review queue for routing changes, and the LLM client the ✨ Suggest buttons use.

A person files a routing change — an area's sentence, a row's line, whether an area crosses a link —
and it waits here until somebody accepts or rejects it. Nothing here writes a fact.

What was here before 2026-10-07 and is gone, all without a caller: the "sleep" that gathered run
observations, validation warnings and service fragments into an evidence bundle and had an LLM
propose promotions, contradictions and questions; the observations a run posted; and the drafts a
promotion wrote. They served an agent runtime that reported its runs back, which RouteMind does not
have.
"""
from __future__ import annotations
import json, os, re, uuid
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str: return datetime.now(timezone.utc).isoformat()


class CuratorStore:
    def __init__(self, root: str | os.PathLike):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.log = self.root / "proposals.jsonl"

    def _lines(self) -> list[dict]:
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines() if l.strip()] if self.log.exists() else []

    def proposals(self, status: str | None = None) -> list[dict]:
        cur: dict[str, dict] = {}
        for e in self._lines():                                    # last state wins
            if e.get("event") == "proposal": cur[e["id"]] = {**e, "status": "pending"}
            elif e.get("event") == "status" and e["id"] in cur: cur[e["id"]].update({"status": e["status"], "why": e.get("why"), "at_status": e["at"]})
        out = list(cur.values())
        return [p for p in out if p["status"] == status] if status else out

    def append(self, obj: dict) -> None:
        with self.log.open("a", encoding="utf-8") as f: f.write(json.dumps(obj, ensure_ascii=False) + "\n")


# ── accept / reject ────────────────────────────────────────────────────────────────────────
def decide(cstore: CuratorStore, pid: str, status: str, why: str | None, apply) -> dict:
    p = next((x for x in cstore.proposals() if x["id"] == pid), None)
    if not p: return {"ok": False, "error": "no such proposal"}
    if p["status"] != "pending": return {"ok": False, "error": f"proposal is {p['status']}"}
    if status == "rejected" and not (why or "").strip(): return {"ok": False, "error": "why is required to reject"}
    result = None
    if status == "accepted":
        result = apply(p) if apply else None                          # the ordinary APIs do the work
        if isinstance(result, dict) and result.get("ok") is False: return {"ok": False, "error": "apply failed", "detail": result}
    cstore.append({"event": "status", "id": pid, "status": status, "why": why, "at": _now()})
    return {"ok": True, "id": pid, "status": status, "result": result}


# ── routing proposals raised by a person (operator decision, 2026-09-10) ──────────────────
# The machine proposal types all **have to cite evidence ids**. A human submission has no such
# evidence and must not pretend to — the evidence for a human proposal is the address it targets.
# There is no immediate-apply path. You may approve your own, but it **always goes through the
# queue** — the record existing is itself the safeguard.
# `as` · `bb` · `core` are an **area's** advertisement, and all three are carried by its
# representative or by CORE.md. `entity` is one row in a table — the line any entity shows in its
# parent's listing. One type is why it can exist at all: a row is an entity like any other, so the
# line it shows is edited the same way an area's is, through the same queue.
# `peer` is `bb` pointed at somebody else's backbone: the line this area shows in a *peer's* hop 0.
# It goes through this queue and not through a direct write for the reason every other advertisement
# does — what an area says about itself is the one thing the whole system routes on, and it is worth
# a second pair of eyes. Across a link that is not a nicety: the reader is another organisation.
# `audience` is the other half of `peer`: who that line reaches. It travels the same road for the
# same reason — the two together are the whole export decision, and a widening that could be made
# with a direct write while the wording needed a second pair of eyes would put the queue in front of
# the smaller of the two.
PEER_NAME = re.compile(r"^[a-z][a-z0-9-]{0,30}$")
# `bb` is `use_when`, and since 2026-09-29 that is the line a peer reads too — there is one sentence
# and `export` decides whether it crosses. So the review that was already required for the local
# routing line now covers the exported one, and the separate `peer` scope becomes the yes/no.
ROUTE_SCOPES = {"as": "one_liner", "bb": "use_when", "core": "core_row", "entity": "one_liner",
                "export": "export", "audience": "export_to"}
# Scopes whose `after` may be empty, and where empty says something. Everywhere else an empty
# sentence is a proposal to advertise nothing, which is a mistake rather than a decision; for an
# audience it is "everybody this area already crosses to", which is the value most areas have.
EMPTIABLE = {"audience"}
# `export` is never empty — it is yes or no, and both are decisions. Withdrawing is `no`, which is
# the most consequential entry on this list and the one most deserving of a review; it used to be an
# empty string against a non-empty `before`, which was two different acts wearing one string.
EMPTIABLE_AGAINST = set()
# Scopes that name a peer as well as an area. The name is the key being written, not evidence.
PEER_SCOPES = set()
# Fields that hold a mapping rather than a sentence, so a proposal edits one key of them.
MAPPING_FIELDS = set()
# Fields that hold yes/no rather than a sentence. Declared here for the same reason MAPPING_FIELDS is:
# an unset boolean and a false one look identical from outside, so deciding by the value would make
# the *first* export decision on an area compare against the wrong thing.
BOOL_FIELDS = {"export"}
# Old spellings, read only: a proposal filed under one before 2026-10-07 may still be in a queue, and
# accepting it applies the field its new name means. New filings must use the new names — the screen
# has sent nothing else since 2026-09-29. `peer` used to be the second export sentence and is now the
# decision to export at all — the nearest thing to what it meant.
SCOPE_ALIAS = {"dr": "as", "peer": "export", "peer-line": "export"}


def submit_route(cstore: CuratorStore, body: dict, actor: str) -> dict:
    scope = str(body.get("scope") or "").strip()
    if scope in SCOPE_ALIAS:
        raise ValueError(f"scope {scope!r} is an old spelling — use {SCOPE_ALIAS[scope]!r}")
    if scope not in ROUTE_SCOPES:
        raise ValueError(f"scope must be one of {sorted(ROUTE_SCOPES)}")
    field = str(body.get("field") or ROUTE_SCOPES[scope])
    if field != ROUTE_SCOPES[scope]:
        raise ValueError(f"scope {scope} takes field {ROUTE_SCOPES[scope]} (got: {field})")
    region = str(body.get("region") or "").strip()
    entity = str(body.get("entity") or "").strip()
    after = str(body.get("after") or "").strip()
    # An entity names itself. Asking for a region as well would be a second answer to a question the
    # entity already settles, and the two could disagree.
    if scope == "entity":
        if not entity: raise ValueError("entity is required for scope `entity` — it is the row being edited")
    elif not region: raise ValueError("region is required")
    if not after and scope not in EMPTIABLE:
        if scope not in EMPTIABLE_AGAINST or not str(body.get("before") or "").strip():
            raise ValueError("after is required — it is the sentence the person settled on"
                             + (f". To withdraw scope `{scope}`, send the line it is withdrawing as "
                                f"`before`" if scope in EMPTIABLE_AGAINST else ""))
    peer = str(body.get("peer") or "").strip()
    if scope in PEER_SCOPES:
        if not PEER_NAME.match(peer):
            raise ValueError(f"peer is required for scope `{scope}` — the reader this line is for, "
                             f"in ASCII kebab-case")
    elif peer:
        raise ValueError(f"scope {scope} does not take a peer")
    unknown = sorted(set(body) - {"scope", "field", "region", "entity", "after", "before", "why",
                                  "target", "peer"})
    if unknown: raise ValueError(f"unknown field(s) {unknown}")
    pid = f"cp_{uuid.uuid4().hex[:10]}"
    cstore.append({"event": "proposal", "id": pid, "at": _now(), "type": "route",
                   "scope": scope, "field": field, "region": region, "entity": entity or None,
                   "peer": peer or None,
                   "before": str(body.get("before") or ""), "after": after,
                   "why": str(body.get("why") or ""), "target": body.get("target"),
                   "submitted_by": actor,
                   "evidence": [body.get("target") or (f"node:{entity}" if entity else f"region:{region}")]})
    return {"ok": True, "id": pid, "status": "pending"}


PROVIDERS = ("openai", "anthropic", "litellm")


class LLMError(RuntimeError):
    """The provider was reached and said no, or could not be reached at all.

    Separate from "the model answered, and the answer was unusable". The call sites turn any
    exception into `None`, which the writer reports as "could not be generated" — so a wrong key or
    a provider mismatch currently reads as "nothing could be drawn from the body". That conflation
    is older than this class and is not fixed here; what this does is carry the provider's own words
    so they reach the log instead of vanishing."""


def chat_client(provider: str, base_url: str, api_key: str, model: str, *,
                max_tokens: int = 1024, temperature: float = 0.0):
    """A chat client for one of three providers. Returns `client(system, user, *, json_object)`.

    **`json_object` is the call site's to decide, never the operator's.** Two prompts parse JSON out
    of the answer and four read one line; if a setting could switch that, changing it would break
    the parse and show up only as "the LLM gives strange answers". So it is an argument here and has
    no environment variable.

    **No model allowlist.** The instruction was "every officially available model", and a list
    written today refuses every model released after today — the exact opposite. `model` is a free
    string; what a key can actually reach is a question for `GET /v1/models` at install time, which
    stays true as the lists change.

    Anthropic is not OpenAI-shaped: a different path, a different auth header, `system` as a
    top-level field rather than the first message, and the answer in `content[]` rather than
    `choices[]`. Treating it as "OpenAI-compatible" is what the previous single client assumed, and
    it only ever spoke to LiteLLM."""
    import urllib.error, urllib.request
    provider = (provider or "litellm").strip().lower()
    if provider not in PROVIDERS:
        raise ValueError(f"unknown LLM provider {provider!r} — one of {', '.join(PROVIDERS)}")
    base, anthropic = base_url.rstrip("/"), provider == "anthropic"
    url = base + ("/v1/messages" if anthropic else "/v1/chat/completions")
    headers = {"Content-Type": "application/json"}
    headers.update({"x-api-key": api_key, "anthropic-version": "2023-06-01"} if anthropic
                   else {"Authorization": "Bearer " + api_key})
    # Remembered across calls so a provider that wants the other spelling is discovered once, not
    # on every request. Newer OpenAI reasoning models refuse `max_tokens` and some refuse a
    # temperature other than 1 — which of those is true is not worth guessing from a model name,
    # because the names change faster than this code does. Ask, read the answer, adjust.
    state = {"token_key": "max_tokens", "temperature": True}

    def payload(json_object: bool) -> dict:
        if anthropic:
            # No `response_format` here. The two prompts that want JSON already say so in their own
            # words, which is the only mechanism this API offers.
            return {"model": model, "messages": [], "max_tokens": max_tokens,
                    "temperature": temperature}
        d = {"model": model, "messages": [], state["token_key"]: max_tokens}
        if state["temperature"]: d["temperature"] = temperature
        if json_object: d["response_format"] = {"type": "json_object"}
        return d

    def send(system: str, user: str, json_object: bool) -> str:
        d = payload(json_object)
        if anthropic:
            d["system"] = system
            d["messages"] = [{"role": "user", "content": user}]
        else:
            d["messages"] = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        req = urllib.request.Request(url, data=json.dumps(d).encode(), headers=headers, method="POST")
        r = urllib.request.urlopen(req, timeout=180)
        got = json.loads(r.read())
        if anthropic:
            return "".join(b.get("text", "") for b in (got.get("content") or []) if b.get("type") == "text")
        return got["choices"][0]["message"]["content"]

    def client(system: str, user: str, *, json_object: bool = False) -> str:
        try:
            return send(system, user, json_object)
        except urllib.error.HTTPError as e:
            detail = ""
            try: detail = e.read().decode("utf-8", "replace")[:600]
            except Exception: pass
            # One retry, and only for something the provider itself named. Anything else is a real
            # failure and is reported as it came, not papered over.
            fixed = False
            if e.code == 400 and not anthropic:
                if "max_completion_tokens" in detail and state["token_key"] == "max_tokens":
                    state["token_key"] = "max_completion_tokens"; fixed = True
                elif "max_tokens" in detail and state["token_key"] == "max_completion_tokens":
                    state["token_key"] = "max_tokens"; fixed = True
                if "temperature" in detail and state["temperature"]:
                    state["temperature"] = False; fixed = True
            if fixed:
                try:
                    return send(system, user, json_object)
                except Exception:
                    pass          # fall through and report the first refusal, which named the cause
            raise LLMError(f"{provider} {model} refused with HTTP {e.code}: {detail}") from e
        except Exception as e:
            raise LLMError(f"{provider} {model} at {base} could not be reached: {e}") from e

    return client

