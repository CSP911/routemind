"""The footprint: every walk an agent takes, as it takes it — one record, read by the screen and by
the next agent alike.

A walk is a question's path through the routing table: hop 0, the areas it opened, the nodes, the
documents it read, and at every step the reason the agent gave. The MCP server opens the walk and
reports each step here; the screen follows the record and expands the map in the same order, live or
replayed. Invariant 11 in docs/INVARIANTS.md: *every walk is recorded, and the screen reads that
record.* Nothing is computed from it for the agent — a "where others went" hint was tried and taken
out (operator, 2026-10-07): it is not part of routing.

**Numbered, not timed.** Every step gets the next integer from one counter across all walks, and a
reader asks for "everything after N". A clock would lose steps — two in the same millisecond, a
reader that polls between them — and the screen's one requirement was *no loss*. The counter is
kept in a file so a restart continues it rather than starting over, which would hand a reader its
own old cursor as new.

**Six hours.** A closed walk is kept for six hours (the operator's number, 2026-10-07) — long enough
to replay what happened this shift, short enough that the directory does
not become a log. An open walk nobody touches for an hour is closed as `abandoned`, which is a
different fact from answered and from not-found.

**Reasons are required.** A step without a `why` is refused: the record exists so a person can see
not just where the agent went but what it was thinking when it went there, and a trail of
addresses with no reasons is the access log, which already exists.

Same shape as the overlay store, on purpose: one JSON file per record, written through a temp file
so a reader never sees half of one, expiry decided on the way past.
"""
import json, re, threading, time, uuid
from pathlib import Path

OPEN, CLOSED = "open", "closed"
OUTCOMES = ("answered", "not_found", "abandoned")
ID_RE = re.compile(r"^wk_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9a-f]{6}$")
OPS = ("open", "resolve", "table", "read", "close")


class WalkError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message); self.status = status


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _age_hours(stamp: str) -> float:
    try:
        import calendar
        t = calendar.timegm(time.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"))
    except Exception:
        return 0.0
    return max(0.0, (time.time() - t) / 3600.0)


class WalkStore:
    def __init__(self, root: Path, *, keep_hours: float = 6.0, open_hours: float = 1.0, steps_max: int = 400):
        self.root = Path(root)
        self.keep_hours, self.open_hours, self.steps_max = keep_hours, open_hours, steps_max
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    # ---- files ----
    def path(self, wid: str) -> Path:
        if not ID_RE.match(wid or ""): raise WalkError(404, f"no walk {wid!r}")
        return self.root / f"{wid}.json"

    def _read(self, p: Path) -> dict | None:
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: return None

    def _write(self, w: dict) -> None:
        p = self.path(w["id"]); tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(w, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(p)

    def _next_seq(self) -> int:
        """One counter for every step of every walk. In a file, so a restart continues it."""
        p = self.root / "_seq"
        try: n = int(p.read_text().strip() or 0)
        except Exception: n = 0
        n += 1
        tmp = p.with_suffix(".tmp"); tmp.write_text(str(n)); tmp.replace(p)
        return n

    def seq(self) -> int:
        try: return int((self.root / "_seq").read_text().strip() or 0)
        except Exception: return 0

    # ---- expiry, on the way past ----
    def _settle(self, w: dict) -> dict | None:
        if w.get("state") == OPEN and _age_hours(w.get("touched_at") or w.get("at", "")) >= self.open_hours:
            self._close(w, "abandoned", f"untouched for {self.open_hours:g}h")
        if w.get("state") != OPEN and _age_hours(w.get("closed_at") or w.get("at", "")) >= self.keep_hours:
            self.path(w["id"]).unlink(missing_ok=True)
            return None
        return w

    def all(self, state: str | None = None) -> list[dict]:
        out = []
        for p in sorted(self.root.glob("wk_*.json")):
            w = self._read(p)
            if not w: continue
            w = self._settle(w)
            if w and (not state or w["state"] == state): out.append(w)
        return out

    def get(self, wid: str) -> dict:
        w = self._read(self.path(wid))
        if not w: raise WalkError(404, f"no walk {wid}")
        w = self._settle(w)
        if not w: raise WalkError(404, f"walk {wid} has expired")
        return w

    # ---- writes ----
    def _step(self, w: dict, op: str, address: str, why: str) -> dict:
        s = {"n": self._next_seq(), "op": op, "address": address, "why": why, "at": _now()}
        w["steps"].append(s); w["touched_at"] = s["at"]
        return s

    def open(self, question: str, how: str, by: dict | None, check: bool = False) -> dict:
        """A new walk, from hop 0. The first step is the opening itself, so a reader polling by
        cursor learns of the walk the same way it learns of everything else."""
        q = str(question or "").strip()
        with self._lock:
            w = {"id": f"wk_{time.strftime('%Y-%m-%d', time.gmtime())}_{uuid.uuid4().hex[:6]}",
                 "question": q, "how": str(how or ""), "by": {k: str(v) for k, v in (by or {}).items() if v},
                 "at": _now(), "touched_at": _now(), "state": OPEN, "outcome": None, "closed_at": None, "steps": [],
                 **({"check": True} if check else {})}
            self._step(w, "open", "/v1/regions", q or "(no question given)")
            self._write(w)
        return w

    def step(self, wid: str, op: str, address: str, why: str) -> dict:
        if op not in ("resolve", "table", "read"): raise WalkError(400, f"op must be resolve, table or read (got {op!r})")
        why = str(why or "").strip()
        if not why: raise WalkError(400, "why is required — a step with no reason is the access log, which already exists")
        with self._lock:
            w = self.get(wid)
            if w["state"] != OPEN: raise WalkError(409, f"walk {wid} is {w['state']} — a step cannot be added to it")
            if len(w["steps"]) >= self.steps_max: raise WalkError(409, f"walk {wid} has {self.steps_max} steps already — it is looping")
            s = self._step(w, op, str(address or ""), why[:200])
            self._write(w)
        return s

    def _close(self, w: dict, outcome: str, why: str) -> None:
        w["state"], w["outcome"], w["closed_at"] = CLOSED, outcome, _now()
        self._step(w, "close", "", why)
        self._write(w)

    def close(self, wid: str, outcome: str, why: str = "") -> dict:
        if outcome not in OUTCOMES: raise WalkError(400, f"outcome must be one of {', '.join(OUTCOMES)}")
        with self._lock:
            w = self.get(wid)
            if w["state"] != OPEN: raise WalkError(409, f"walk {wid} is already {w['state']}")
            self._close(w, outcome, str(why or outcome)[:200])
        return w

    # ---- reads for the screen and the next agent ----
    def since(self, n: int, checks: bool = False) -> dict:
        """Every step after cursor `n`, oldest first, with the walk each belongs to. The reader keeps
        the last `n` it saw and asks again; nothing between two asks can be missed. A check's walks
        are left out unless asked for — they still take step numbers, so the cursor is unaffected."""
        rows = []
        for w in self.all():
            if w.get("check") and not checks: continue
            for s in w["steps"]:
                if s["n"] > n:
                    rows.append({"walk": w["id"], "question": w["question"], "state": w["state"], "outcome": w["outcome"],
                                 "by": w.get("by") or {}, **s})
        rows.sort(key=lambda r: r["n"])
        return {"seq": self.seq(), "steps": rows}
