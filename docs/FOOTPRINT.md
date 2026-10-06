# The footprint — a walk you can watch, replay, and that the next walk can see

Decided 2026-10-07. Two features, one record.

**1. The live footprint.** While an agent walks, the map opens in the order the agent does — hop 0,
then the area it chose, then the node, then the document — and at each step the reason the agent
gave is recorded. The reasons may arrive late; the opening must be watched as it happens.

**2. History and replay.** Every walk is kept for six hours. A replay button opens the map again in
the same order. And the history is read by agents too: a hot path — where previous walks for this
name went, and which rows were walked and answered — shown as a hint, never as an answer.

## One record

Both features read the **walk record** (`ontology/service/walks.py`, directory `ONTOLOGY_WALKS`),
and nothing else does the job twice. The MCP server — the agent's only door — opens the walk when
hop 0 is served, reports every step below hop 0 with the reason the agent gave, and closes it when
the overlay is closed. The screen polls the record. The resolver and the tables read the record for
the hint. One home, three readers: invariant 11.

```
agent ──MCP──▶ POST /v1/walks            opens, with the question        (hop 0)
          ──▶ POST /v1/walks/{id}/steps {op: table|read|resolve, address, why}
          ──▶ POST /v1/walks/{id}/close {outcome: answered|not_found}
screen ◀──    GET  /v1/walks?since=N    every step after N, oldest first — the live footprint
screen ◀──    GET  /v1/walks/{id}       one walk, whole — the replay
agent  ◀──    /v1/resolve … "history"   walks that touched these names, and the paths they took
agent  ◀──    tables … HEAT column      walked / answered, per row, last six hours
```

## Decisions, and why

**Polling, numbered.** The screen asks every second for "everything after N", where N is the
largest step number it has seen. Steps are numbered from one counter across all walks, kept in a
file, so nothing between two asks can be lost and a restart cannot hand the screen a stale cursor.
A clock could not promise that; the operator's one requirement was no loss.

**`why` is required.** Every call below hop 0 — a table, a document — takes a one-line reason, and
the MCP refuses one without it. The record exists so a person can see what the agent was thinking,
not only where it went; a trail of addresses with no reasons is the access log, which exists.

**Six hours.** The operator's number. Long enough to replay the shift and to count what was hot;
short enough that the directory is not a log. An open walk untouched for an hour closes as
`abandoned` — a different fact from answered and from not-found.

**The hint is structural.** `history` on a resolution names addresses — "walks for this name went
hop 0 › procurement › vendor" — and HEAT counts rows. Neither says which record governs or what
any answer is; the walk still starts at hop 0 (invariant 1) and still reads the lines. A hot path
that said more would be the recency trap in a new coat.

**The screen expands, it does not navigate.** A step opens the rack or node it names, on top of
whatever the person has open; the replay does the same at a fixed pace. The person's own state is
not replaced.

## What is not here

- Pushing from the server. A one-second GET of a small JSON is cheaper than a socket and has no
  reconnect story to get wrong; the existing revision watch made the same call.
- The agent's prose. Only what it said in `why`. The transcript belongs to the client.
- Cross-walk reuse detection. The record now makes it visible — each walk carries its question —
  but nothing yet refuses a walk reused for a new question (invariant 1's stated limit).

## Checks

`check/footprint-check.py`: a step without `why` is refused; steps from two interleaved walks come
back by cursor in order with none lost; an open walk is closed `abandoned` after the hour and a
closed one gone after six; HEAT and `history` count what was walked; the MCP reports every call it
makes and closes the walk when the overlay closes. The screen's polling and replay are exercised
by `check/footprint-screen-check.py`: the real `static/knowledge.js` against a live record — a step
opens its area and node path, a failed poll loses nothing, exactly one tile is marked as now, and a
replay shows every step in order. Verified to fire on a poll that jumps to the newest step.
