# Invariants

Sentences that are true on every path or the system refuses — not descriptions of features. Each
one names where it is enforced and how it is checked. A feature with no invariant behind it is a
feature nobody can tell is broken.

Written 2026-10-06, after two weeks in which every real use found a seam the 28 suites had not:
the first real question (one area read, absence claimed), the first hand edit (a flag the
validator caught and the server served stale anyway), the first stranger's fixture (the map
reached and obeyed, or not reached at all). The common cause, almost every time, was one fact with
two homes, or a rule that lived in a prompt rather than in code.

## The ten

**1. Every walk starts at hop 0.** Nothing below the area list — an area's table, a node's table,
a document, a circuit's table — is served to an agent that has not been served hop 0 *for this
question*. Enforced in the MCP server, the agent's only door: hop 0 is `knowledge_table` with no
address, and the server remembers, for the session it serves, that it was opened; every call below
hop 0 before that is refused with "start at hop 0". The agent carries no id (2026-10-07: an argument
nobody could explain was dropped). A walk ends when a new hop 0 is served, when an overlay is closed,
or after ten minutes. The screen and `curl` read the API directly and are not bound: this is a rule
about agents, who are the ones that answer questions. *Limit, stated:* an agent can go on below
hop 0 into its next question without asking for hop 0 again; nothing in the server can tell where
one question ends, and a question log (not yet built) is what would catch it.

**2. "Not here" may be said only by someone who has seen the whole list.** An absence conclusion
is accepted only from someone who has read hop 0. Inside one area, "not here" means "not in this
drawer". The agent's instructions say so, and 1 guarantees that every agent below hop 0 has read
it. With the overlay tool off — the default since 2026-10-07 — no tool records an absence, so the
system enforces nothing more than that; where `KNOWLEDGE_TOOLS_EXTRA=overlay` turns it on, an
overlay is closed `not_found` only inside a walk.

**3. One fact, one home.** Every fact has one source file. Anything derived from it — `regions.json`,
the hop-0 listing, a session, a cache — is regenerated in the same transaction that changes the
source, or recomputed on read, or follows the source when it changes; it is never a second copy
somebody can edit. The inventory, each with the check that proves it follows:

| derived state | its source | how it follows | checked by |
|---|---|---|---|
| `regions.json`, committed | the areas' files | regenerated in every write; served from the files when stale; healed at startup | `check/drift-check.py` |
| the node cache in the store | every entity file | keyed on every file's mtime | `check/same-answer-check.py` (the hand-edited run) |
| ages | git history | keyed on the commit | `check/age-check.py` |
| `/healthz` `valid` | validation | keyed on the commit | `check/drift-check.py` |
| what a circuit reads | the other backbone's export surface | not cached — every read is a read of the far end | `check/follow-check.py` |
| a circuit's session (6 h) | the far end's memory | a restart there revokes every one; the circuit re-mints on the 401 | `check/follow-check.py`, `check/session-check.py` |
| the MCP's area list in its first tool | hop 0 | refreshed on every `tools/list` | `check/follow-check.py` |
| a walk (10 min) | the question | ended by a new hop 0, an overlay close, or time | `check/walk-check.py` |

**4. Every reader of one fact gets the same answer.** Two paths to one fact return the same bytes:
the area listing and the area detail, the owner's view and the export surface, `store.regions()`
and `store.regions_json()`. Checked by `check/same-answer-check.py`: every area's routing sentence,
export flag, representative and title; a spread of nodes' name, line, kind, parent and body — each
read from the file and from every API path, the export surface, the placement walk and what the MCP
prints, 380 cells, on a clean tree and again with
an uncommitted hand edit. Verified to fire: with the pre-2026-10-05 stale-table behaviour put back,
the listing and hop 0 disagree with the file and the check says which cells.

**5. A routing change is a commit.** Every write that changes what hop 0 or a node line says — API,
screen, tidy, the startup heal — goes through one transaction: refuse a dirty tree, mutate,
regenerate, validate, roll back on failure, commit. A hand edit is the one write outside it, and it
is handled by 3: the validator refuses further writes until the table is regenerated, and readers
are served the files' truth meanwhile. Checked by `check/transact-check.py`: statically, every
`Writer` method that touches the tree is read as a syntax tree and must reach `transact`, directly
or by delegation, so a method added without it fails here first; dynamically, every write path —
each API write, the proposal queue's accept and `tidy --fix` — is driven once
to succeed and once to fail, and after each the commits gained, the tree's cleanliness and the
response are read back. Verified to fire: with the rollback removed for one run, the first failure
that reached the validator leaves the tree dirty and the check names it.

**6. What a circuit reads is a subset of what `export` allows.** Another backbone sees an area only
if its representative's *file* says `export: yes`, and nothing under a kind marked `export: no`.
Checked by `check/circuit-check.py`, `check/follow-check.py` and `check/drift-check.py`, against file
truth (3), not the committed table — the 2026-10-05 defect was exactly the committed table
disagreeing with the file.

**7. Nothing is reported done that did not happen.** A write's response is the transaction's
result; a refused step is reported as refused and no summary is printed after it. Checked by the
same `check/transact-check.py`: on every write path a 2xx must coincide with exactly one new commit
whose id the response names, and a non-2xx with none — the response and the repository read back
together, so a success printed over a refusal, or a refusal printed over a commit, is a failing
cell.

**8. An advertised row has something behind it.** An area with no representative, a CORE row with
no area, an edge to nothing, a node with neither body nor children: errors, not warnings, because a
reader cannot tell such a row from a real one. Enforced by the validator and `tidy`.

**9. Documents carry no state.** Which record governs is written in the map's lines and nowhere
else; a document's frontmatter has no `state`, `supersedes`, `superseded_by`, `operative`,
`current`, `replaces`, `replaced_by`. The fixture contract has refused these since 2026-09-18; the
live validator refuses them since 2026-10-06 (`FORBIDDEN_STATE_FIELDS`, with the store keeping
every key a file carries so the rule reads the file, not a projection of it). Checked in
`ontology/check.py`: a state field written into a document by hand is refused, naming the node and
the fields and where the fact belongs, and the shipped repositories still validate.

**10. Secrets are never in tracked files.** A token lives in the environment; a tracked file names
the variable (`token_env`) and nothing else. Checked by `check/secrets-check.py` over every tracked
file: provider keys, private-key blocks, a tracked `.env`, a token written in YAML, and a path from
somebody's machine. Runs with the static checks; verified to fire on each shape planted in a
temporary repository.

**11. Every walk is recorded, and the screen reads that record.** The MCP server
opens a walk when hop 0 is served, reports every step below hop 0 with the reason the agent gave,
and closes it when the next hop 0 is served; the record lives in `ONTOLOGY_WALKS`
(`docs/FOOTPRINT.md`). The screen's live footprint and its replay read that record and nothing else;
the agent is shown nothing from it (2026-10-07: a hint of where others went is not routing). Steps are numbered from one counter so a reader
polling by cursor loses nothing; a step without a reason is refused. Checked by
`check/footprint-check.py`; the screen's polling and replay by `check/footprint-screen-check.py`.

## What is not on this list

Things that are true but are design, not invariants: one sentence per area; `use_when` is what an
agent routes on and what a peer reads; ages come from git. They follow from 3 and 4.

## How the list is used

No new mechanism until every existing one has the invariant it depends on checked. A finding that
does not map to one of these ten is either a new invariant — add it here first — or a bug in an
existing one, named by number in the commit.
