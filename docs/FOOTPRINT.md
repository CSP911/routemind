# The footprint — a walk you can watch and replay

Decided 2026-10-07. Two features, one record.

**1. The live footprint.** While an agent walks, the map opens in the order the agent does — hop 0,
then the area it chose, then the node, then the document — and at each step the reason the agent
gave is recorded. The reasons may arrive late; the opening must be watched as it happens.

**2. History and replay.** Every walk is kept for six hours. A replay button opens the map again in
the same order. The history is for people. An agent is shown nothing from it: a hot path for
agents was built on 2026-10-07 and taken out the same day — where others went is not routing.

## One record

Both features read the **walk record** (`ontology/service/walks.py`, directory `ONTOLOGY_WALKS`),
and nothing else does the job twice. The MCP server — the agent's only door — opens the walk when
hop 0 is served, reports every step below hop 0 with the reason the agent gave, and closes it when
the next hop 0 is served (`abandoned`) or an overlay is closed. The screen polls the record. One
home: invariant 11.

```
agent ──MCP──▶ POST /v1/walks            opens                           (hop 0)
          ──▶ POST /v1/walks/{id}/steps {op: table|read, address, why}
          ──▶ POST /v1/walks/{id}/close {outcome: answered|not_found}
screen ◀──    GET  /v1/walks?since=N    every step after N, oldest first — the live footprint
screen ◀──    GET  /v1/walks/{id}       one walk, whole — the replay
screen ◀──    GET  /v1/walks?limit=10&offset=20   a page of the history, newest first, with the total
```

## Decisions, and why

**Polling, numbered.** The screen asks every second for "everything after N", where N is the
largest step number it has seen. Steps are numbered from one counter across all walks, kept in a
file, so nothing between two asks can be lost and a restart cannot hand the screen a stale cursor.
A clock could not promise that; the operator's one requirement was no loss.

**`why` is required.** Every call below hop 0 — a table, a document — takes a one-line reason, and
the MCP refuses one without it. The record exists so a person can see what the agent was thinking,
not only where it went; a trail of addresses with no reasons is the access log, which exists.

**Six hours.** The operator's number. Long enough to replay the shift;
short enough that the directory is not a log. An open walk untouched for an hour closes as
`abandoned` — a different fact from answered and from not-found.

**No hint for the agent.** A `history` on a resolution and a HEAT column on every table were built
and removed the same day (2026-10-07), with the resolver itself. They said nothing about which record
governs, but they put "where others went" next to the lines an agent routes on — the recency trap in
a new coat. The agent reads the lines and follows the addresses; the record is for people.

**The screen expands, it does not navigate.** A step opens the rack or node it names, on top of
whatever the person has open. The person's own state is not replaced.

**Every recent walk at once.** Several agents can walk together, and the live view shows all of them
— every walk still open, and every walk that moved in the last ten minutes — each in its own colour,
with a line under the map for each. Choosing one in the history below the map shows that one alone,
until Live lets it go (a picker in the bar did this until 2026-10-09). Until
2026-10-08 the view followed whichever walk had moved last, so a second agent pulled the screen away
from the first (operator).

**A replay keeps the walk's rhythm.** The gap between two recorded steps, divided by the chosen
speed (1×, 2×, 4×, 8×), and never under 0.15 s or over 6 s. It was a fixed 0.9 s a step, which made a
walk that stopped to think look exactly like one that did not. With no walk chosen, every kept walk
is replayed together, interleaved in the order the steps were taken. The same button stops it.

**A walk is drawn as a trace, not only as marked tiles** (2026-10-09). A line runs along the map's own
cables in the order the tiles were walked, each numbered on its tile; the newest stretch is drawn as it arrives,
with a dot travelling along it, and the reason for the step it is on sits beside that tile. While a
walk moves the rest of the map is dimmed. Under the bar the walk in focus is a row of steps: pressing
one shows the map as it was at that step, until Live. When a walk ends, a card in the window's corner
says how it went — tables, documents, how long, the outcome — and the close itself is an outcome,
never a step, so the trace does not run back to hop 0. With reduced motion the dot and the drawing-in
are left out.

**Along the cables, not across the map** (2026-10-09, operator). The first trace joined tile centres
with straight lines, which cut diagonally over names and ignored the wiring — it did not say which way
the walk went. The trace now follows the cabling the map draws: down the trunk, along the bus, down
the drop to the area, into its rack and on to the tile; a step back up and across goes up to where the
two branches part, never over the shared stretch twice. Inside a rack it crosses the header at the gap
nearest the incoming cable — between two buttons, or beside the title — then runs along the rule
under the header and down the gaps between tiles, so it never covers a word. Passing through a tile
is a break in the line: the tile itself is lit. Walks sharing a cable run beside each other a few
pixels apart, in lanes taken from their colours, like lines on a metro map. A step onto something
the cabling does not reach falls back to a squared-off elbow.

**The reason in full, and a reload that comes back to the walk** (2026-10-09, operator). The reason
beside the tile wraps onto up to four lines of 340px — about 190 characters — instead of being cut to
one line of 360; anything longer ends in "…", with the whole sentence on hover and on the line above
the map. It goes right of the tile, else left, else under the tile's caption: the first of those
inside the drawing that covers no other tile. On load, the walks still going (open, or moved in the
last ten minutes) are opened on the map as the live view would have opened them, and the camera goes
to the newest — but only on a map nobody has opened anything on yet. Until then a reload in the middle
of a walk came back to a closed map, the trace stopping at the area tiles.

**History under the map, ten to a page** (2026-10-09, operator). Every kept walk, newest first: when,
the question, who, what it did (tables · documents → where it stopped), how long, how it ended. Each
row can be shown on the map at its last step, replayed, or opened for its reasons. The service pages
it (`limit` 1–200, `offset`), ordered by the walk's opening step number — `at` is to the second, and
walks opened in the same second came back in an order that changed between pages. The first page
follows the record as steps arrive; another page stays put while somebody reads it. The result card
steps aside while the history is in view, since it would sit on its last rows and page buttons.

**How a walk ends** (2026-10-10). `answered` when the agent's placement lands or an overlay is closed
answered; `not_found` from an overlay; `abandoned` when the next question started (a new hop 0) or an
hour passed; and `ended` when the agent's session closed with the walk still open — the MCP server
says so when its client goes away. With overlays off (the default) a question an agent answered from
what it read is closed `ended` or `abandoned`, not `answered`: the server cannot know an answer was
given, and does not claim one. A placement records each table it stepped through, and closes
`answered` with the document and the commit.

## What is not here

- Pushing from the server. A one-second GET of a small JSON is cheaper than a socket and has no
  reconnect story to get wrong; the existing revision watch made the same call.
- The agent's prose. Only what it said in `why`. The transcript belongs to the client.
- Cross-walk reuse detection. Nothing yet tells where one question ends and the next begins
  without a new hop 0 (invariant 1's stated limit).

## Checks

`check/footprint-check.py`: a step without `why` is refused; steps from two interleaved walks come
back by cursor in order with none lost; an open walk is closed `abandoned` after the hour and a
closed one gone after six; the MCP reports every call it makes, shows the agent nothing from the
record, and closes the walk when the next hop 0 is served. The screen's polling and replay are exercised
by `check/footprint-screen-check.py`: the real `static/knowledge.js` against a live record — a step
opens its area and node path, a failed poll loses nothing, exactly one tile is marked as now, a
replay shows every step in order; two walks at once are both on the map in two colours, each marked
where it is now; a 1.5 s pause takes about that long at 1× and much less at 8×; and stopping is
immediate; the trace, its numbers and the reason are drawn — every straight run of the trace level or
upright, and some of them lying on the cables themselves — a step pressed in the row pins the map
there, and the card appears once the walk ends; the history pages ten at a time with no walk on two
pages, and showing a row on the map pins that walk at its last step; a long reason is wrapped, not cut; and
a reload opens the walks still going, but not over what a person has open nor for a walk long over. The service side of the paging —
ten, then the rest, newest first, a row's summary not counting the close — is in footprint-check. Verified to fire on a poll that jumps to the newest step.
