"""Who read what across a link, and whether they were allowed to.

**This exists because nothing else remembers.** A relayed document is held in memory for the length
of one request and discarded — no cache, no copy, which is the whole point of a link rather than a
merge. The cost of that is accountability: with a physical copy there is at least an artefact at the
other end, and with this there is nothing anywhere unless the owner writes a line. "What did the
other domain read from us last month" is usually the first question anybody asks, and until
2026-09-13 the only answer available was an HTTP access line reading

    172.20.0.2 "GET /v1/export/nodes/payroll-overview HTTP/1.1" 200

which does not say who. Every read that comes through an exchange arrives from the same container, so
they were all identically anonymous.

**It is written by the owner, not by the reader**, and the owner already knows the name: the link a
request came in on identifies the peer, and an exchange says which of its members it is fetching for.
Two names, and both are recorded, because they answer different questions — *which link carried this*
and *who was at the far end of it*.

Behind two exchanges the second name is the neighbouring room, not the backbone inside it. That is
not a gap in the record; it is what no-transit means. A room's members are its own business, and a
backbone two rooms away has no relationship with this one to be recorded.

**Refusals are recorded too, and matter more.** A served read is the ordinary case. A refused one is
somebody holding an address they should not be following, and a run of them is the only signal there
is that a link is being probed rather than used.

One line per read, as JSON, appended. To stderr always, so a default install has the record without
configuring anything, and to `ONTOLOGY_ACCESS` as well when it is set — stderr rotates away and an
audit that rotates away is not one.
"""
from __future__ import annotations

import json
import os
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

# One writer per process. Appends are small and O_APPEND is atomic for them on every filesystem this
# runs on, but two threads formatting into one handle can still interleave, and half a line in an
# audit record is worse than no line — it cannot be told from a truncated one.
_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record(store_dir: str | os.PathLike | None, *, peer: str | None, reader: str | None,
           path: str, outcome: str, reason: str | None = None, size: int | None = None) -> dict:
    """Write one line. Never raises: a record that can bring down the thing it is recording is worse
    than no record, and the read it describes has already happened either way."""
    line = {"at": _now(), "peer": peer or "?", "reader": reader or "?", "path": path,
            "outcome": outcome}
    if reason: line["reason"] = reason
    if size is not None: line["size"] = size
    text = json.dumps(line, ensure_ascii=False, sort_keys=False)
    try:
        sys.stderr.write("access " + text + "\n")
    except Exception:
        pass
    if store_dir:
        try:
            d = Path(store_dir)
            d.mkdir(parents=True, exist_ok=True)
            # One file per UTC day. Rotation nobody has to configure, and the name is the question a
            # person actually asks — "what happened on the 12th".
            with _lock:
                with (d / f"{line['at'][:10]}.jsonl").open("a", encoding="utf-8") as f:
                    f.write(text + "\n")
        except Exception as e:
            try: sys.stderr.write(f"access: could not write the record ({type(e).__name__})\n")
            except Exception: pass
    return line


def read(store_dir: str | os.PathLike | None, *, day: str | None = None, limit: int = 500) -> list[dict]:
    """The record back, newest last. For an operator answering a question, and for the checks.

    A day that was never written is an empty list and not an error: nothing having happened is an
    answer, and the alternative teaches whoever reads it that a missing file means something broke.
    """
    if not store_dir: return []
    d = Path(store_dir)
    files = sorted(d.glob("*.jsonl")) if not day else [d / f"{day}.jsonl"]
    out: list[dict] = []
    for f in files:
        if not f.is_file(): continue
        for raw in f.read_text(encoding="utf-8").splitlines():
            if not raw.strip(): continue
            try: out.append(json.loads(raw))
            except Exception: continue
    return out[-limit:]
