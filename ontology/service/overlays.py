"""Overlays — one question's working set, kept beside the ontology and never inside it.

An overlay is the areas and entities an agent (or a person) chose to work within for one question,
with the reason for each choice. It narrows **where to look**. It never changes what exists: "not in
the overlay" means go back to hop 0, never "not in Knowledge" — every table this prints carries that
sentence, because the moment an overlay can be read as an inventory it has become a lie.

It is run evidence, not structure. The ontology repository holds what the domain is made of, and a
commit per question would bury that under traffic. So this lives in its own directory, one JSON file
per overlay, no git — and it expires, which nothing in the ontology ever does.

Expiry is evaluated **when someone looks**. There is no thread and no scheduler: an overlay nobody
asks about costs nothing by being stale, and the one moment staleness matters is the moment it is
read. If this ever seems to need a background job, something above it went wrong.
"""
from __future__ import annotations
import json, re, time
from pathlib import Path

ID_RE = re.compile(r"^ov_\d{4}-\d{2}-\d{2}_[0-9a-f]{4,8}$")
OPEN, ANSWERED, NOT_FOUND, ABANDONED = "open", "answered", "not_found", "abandoned"
OUTCOMES = (ANSWERED, NOT_FOUND)


class OverlayError(Exception):
    def __init__(self, status: int, message: str, details=None):
        super().__init__(message); self.status, self.details = status, details or []


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _age_hours(stamp: str) -> float:
    """How old a stamp is. An unreadable one is old, not new.

    It used to answer 0.0 for anything it could not parse, which reads as "written a moment ago" — so
    a record with a stamp this function does not understand was never abandoned and never forgotten.
    In a store whose whole job is to not accumulate, "I cannot tell how old this is" has to fall on
    the side that lets it go.

    Both spellings of the same instant are accepted, because only the `Z` form is written here and a
    caller reaching for `datetime.isoformat()` — which writes `+00:00` — would otherwise make every
    record it touched immortal, silently and with no error anywhere.
    """
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try: t = time.mktime(time.strptime(stamp, fmt)) - time.timezone
        except Exception: continue
        return max(0.0, (time.time() - t) / 3600.0)
    return float("inf")


class OverlayStore:
    """One JSON file per overlay in a flat directory.

    `open_hours` closes an untouched overlay as `abandoned`; `keep_days` forgets a closed one. Both
    are settings rather than constants because neither number is knowable in advance — 24 hours is
    only "much longer than a run", and the right number for keeping records is however long the thing
    that reads them needs, which does not exist yet.
    """

    def __init__(self, root: Path, *, members_max: int = 8, rows_max: int = 120,
                 open_hours: float = 24.0, keep_days: float = 30.0):
        self.root = Path(root)
        self.members_max, self.rows_max = members_max, rows_max
        self.open_hours, self.keep_days = open_hours, keep_days
        self.root.mkdir(parents=True, exist_ok=True)

    # ---- files ----
    def path(self, oid: str) -> Path:
        if not ID_RE.match(oid or ""): raise OverlayError(404, f"no overlay {oid!r}")
        return self.root / f"{oid}.json"

    def _read(self, p: Path) -> dict | None:
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: return None

    def _write(self, ov: dict) -> None:
        p = self.path(ov["id"])
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(p)                      # a reader never sees half a record

    def new_id(self) -> str:
        import uuid
        return f"ov_{time.strftime('%Y-%m-%d', time.gmtime())}_{uuid.uuid4().hex[:6]}"

    # ---- expiry, evaluated on the way past ----
    def _settle(self, ov: dict) -> dict | None:
        """Apply expiry to one record. Returns None when it should no longer exist."""
        if ov.get("state") == OPEN and _age_hours(ov.get("touched_at") or ov.get("at", "")) >= self.open_hours:
            ov["state"], ov["outcome"] = ABANDONED, None
            ov["closed_at"] = _now()
            # Not an error and not a silence: the record says it was left, which is a different fact
            # from "answered" and from "nothing here", and all three are worth telling apart later.
            ov["trail"].append({"op": "abandon", "why": f"untouched for {self.open_hours:g}h", "at": ov["closed_at"]})
            self._write(ov)
        if ov.get("state") != OPEN and _age_hours(ov.get("closed_at") or ov.get("at", "")) >= self.keep_days * 24:
            self.path(ov["id"]).unlink(missing_ok=True)
            return None
        return ov

    def all(self) -> list[dict]:
        out = []
        for p in sorted(self.root.glob("ov_*.json")):
            ov = self._read(p)
            if not ov: continue
            ov = self._settle(ov)
            if ov: out.append(ov)
        return out

    def get(self, oid: str) -> dict:
        ov = self._read(self.path(oid))
        if not ov: raise OverlayError(404, f"no overlay {oid}")
        ov = self._settle(ov)
        if not ov: raise OverlayError(404, f"overlay {oid} has expired")
        return ov

    # ---- writes ----
    def _fits(self, members: list[dict], rows_of) -> None:
        """Both caps, checked **before anything is written.**

        The member cap can be counted here; the row cap cannot — how many rows an address brings is a
        question about the ontology, so the caller passes the counter. Doing it here rather than in
        the endpoint is what keeps a refusal from being a write that gets undone: an overlay created
        and then deleted, or a member added and then rolled back, is a half-succeeded state, and this
        codebase has paid for those before.

        Only on the way in. A live overlay whose table grew because the ontology grew still prints in
        full — the alternative is a table that stops early, and a short table read as a whole one is
        the single failure an overlay must never have."""
        if len(members) > self.members_max:
            raise OverlayError(409, f"an overlay holds at most {self.members_max} members — narrow to entities rather than whole areas")
        if rows_of is None: return
        counts = [(m["address"], rows_of(m["address"])) for m in members]
        total = sum(n for _, n in counts)
        if total > self.rows_max:
            worst, n = max(counts, key=lambda x: x[1])
            raise OverlayError(409, f"that is {total} rows and the limit is {self.rows_max} — {worst} alone brings {n}. "
                                    f"Add entities instead of the whole area.")

    def create(self, question: str, members: list[dict], by: dict, resolve, rows_of=None) -> dict:
        question = str(question or "").strip()
        if not question:
            # A person ticking boxes has not typed one either, and the screen should ask. An overlay
            # whose question is unknown teaches nothing on the way out, and the record is the point.
            raise OverlayError(400, "question is required — it is what this overlay is for, and what makes the record worth keeping")
        rows = self._members(members, resolve, [])
        self._fits(rows, rows_of)
        ov = {"id": self.new_id(), "question": question, "by": self._by(by), "state": OPEN,
              "at": _now(), "touched_at": _now(), "members": rows,
              "trail": [{"op": "create", "address": m["address"], "why": m["why"], "at": m["at"]} for m in rows],
              "outcome": None, "used": [], "closed_at": None}
        self._write(ov)
        return ov

    def amend(self, oid: str, add: str | None, remove: str | None, why: str, resolve, rows_of=None) -> dict:
        ov = self.get(oid)
        if ov["state"] != OPEN:
            raise OverlayError(409, f"overlay {oid} is {ov['state']} — a closed record does not change")
        if bool(add) == bool(remove):
            raise OverlayError(400, "exactly one of add | remove")
        why = str(why or "").strip()
        if not why:
            raise OverlayError(400, "why is required — the record has to say what was thought, not only what happened")
        if add:
            new = self._members([{"address": add, "why": why}], resolve, ov["members"])
            self._fits(ov["members"] + new, rows_of)
            ov["members"] = ov["members"] + new
            ov["trail"].append({"op": "add", "address": new[0]["address"], "why": why, "at": new[0]["at"]})
        else:
            addr = _norm(remove)
            if not any(m["address"] == addr for m in ov["members"]):
                raise OverlayError(404, f"{addr} is not in this overlay")
            ov["members"] = [m for m in ov["members"] if m["address"] != addr]
            ov["trail"].append({"op": "remove", "address": addr, "why": why, "at": _now()})
        ov["touched_at"] = _now()
        self._write(ov)
        return ov

    def close(self, oid: str, outcome: str, used: list[str], resolve) -> dict:
        ov = self.get(oid)
        if ov["state"] != OPEN:
            raise OverlayError(409, f"overlay {oid} is already {ov['state']}")
        if outcome not in OUTCOMES:
            raise OverlayError(400, f"outcome must be one of {' | '.join(OUTCOMES)}")
        members = {m["address"] for m in ov["members"]}
        ever = {t.get("address") for t in ov["trail"] if t.get("address")}
        marked = []
        for a in (used or []):
            addr = _norm(a)
            if not resolve(addr):
                raise OverlayError(422, f"{addr} is not an address this ontology serves")
            # Answering from something that was never a member is the **normal** case: an agent adds
            # an area, reads its table, and follows a row down. Refusing that would refuse the honest
            # close. It is also the most useful thing in the record — it says the overlay was drawn a
            # level too coarse, which is exactly what comparing runs is trying to learn.
            marked.append({"address": addr,
                           "how": "member" if addr in members else ("removed" if addr in ever else "reached")})
        ov.update({"state": outcome, "outcome": outcome, "used": marked,
                   "closed_at": _now(), "touched_at": _now()})
        ov["trail"].append({"op": "close", "why": outcome, "at": ov["closed_at"]})
        self._write(ov)
        return ov

    # ---- helpers ----
    def _by(self, by: dict) -> dict:
        by = by or {}
        kind = str(by.get("kind") or "").strip().lower()
        if kind not in ("agent", "person"):
            raise OverlayError(400, "by.kind must be agent | person")
        return {"kind": kind, "name": str(by.get("name") or "").strip() or "unnamed"}

    def _members(self, members: list[dict], resolve, existing: list[dict]) -> list[dict]:
        rows, seen = [], {m["address"] for m in existing}
        if not members: raise OverlayError(400, "members is required — an overlay with nothing in it narrows nothing")
        for m in members:
            addr = _norm((m or {}).get("address"))
            why = str((m or {}).get("why") or "").strip()
            if not addr: raise OverlayError(400, "each member needs an address")
            if not why: raise OverlayError(400, f"{addr} has no why — without it the record says what happened and not what was thought")
            if addr in seen: raise OverlayError(409, f"{addr} is already in this overlay")
            got = resolve(addr)
            if not got:
                # Deliberately **not** "an address nobody printed". Nothing records what was printed;
                # what can be checked is that the address resolves to something served. Saying more
                # than that would claim a guard we do not have.
                raise OverlayError(422, f"{addr} is not an address this ontology serves — follow a `fetch` from a table rather than assembling one")
            seen.add(addr); rows.append({"address": addr, "why": why, "at": _now()})
        return rows


def _norm(address) -> str:
    a = str(address or "").strip()
    return ("/" + a.lstrip("/")).rstrip("/") if a else ""
