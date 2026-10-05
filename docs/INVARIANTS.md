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
question*. Enforced in the MCP server, the agent's only door: hop 0 (from `knowledge_resolve` or
`knowledge_table` with no address) issues a **walk** id, and every call below hop 0 must carry it
or is refused with "start at hop 0". A walk expires when an overlay is closed, when a new hop 0 is
served, or after ten minutes. The screen and `curl` read the API directly and are not bound: this
is a rule about agents, who are the ones that answer questions. *Limit, stated:* an agent can
carry a walk into its next question; the walk records the question it was opened for, so the
reuse is visible, and a question log (not yet built) is what would catch it.

**2. "Not here" may be said only by someone who has seen the whole list.** An absence conclusion
(an overlay closed `not_found`, a resolver NXDOMAIN acted on) is accepted only inside a walk, i.e.
with hop 0 read for this question. Inside one area, "not here" means "not in this drawer" and the
system does not let it be reported as more. Enforced by the same walk id as 1.

**3. One fact, one home.** Every fact has one source file. Anything derived from it — `regions.json`,
the hop-0 listing, a session, a cache — is regenerated in the same transaction that changes the
source, or recomputed on read; it is never a second copy somebody can edit. Checked by editing each
source by hand and asserting every reader reflects it (`check/drift-check.py` for the derived table;
the rest to be enumerated).

**4. Every reader of one fact gets the same answer.** Two paths to one fact return the same bytes:
the area listing and the area detail, the owner's view and the export surface, `store.regions()`
and `store.regions_json()`. Checked by `check/same-answer-check.py`: every area's routing sentence,
export flag, representative and title; a spread of nodes' name, line, kind, parent, aliases and
body; the edges; the core — each read from the file and from every API path, the export surface,
the resolver, the placement walk and what the MCP prints, 420 cells, on a clean tree and again with
an uncommitted hand edit. Verified to fire: with the pre-2026-10-05 stale-table behaviour put back,
the listing and hop 0 disagree with the file and the check says which cells.

**5. A routing change is a commit.** Every write that changes what hop 0 or a node line says — API,
screen, graft, tidy, the startup heal — goes through one transaction: refuse a dirty tree, mutate,
regenerate, validate, roll back on failure, commit. A hand edit is the one write outside it, and it
is handled by 3: the validator refuses further writes until the table is regenerated, and readers
are served the files' truth meanwhile. Checked by `check/transact-check.py`: statically, every
`Writer` method that touches the tree is read as a syntax tree and must reach `transact`, directly
or by delegation, so a method added without it fails here first; dynamically, every write path —
each API write, the proposal queue's accept, `tidy --fix`, a graft and its ungraft — is driven once
to succeed and once to fail, and after each the commits gained, the tree's cleanliness and the
response are read back. Verified to fire: with the rollback removed for one run, the first failure
that reached the validator leaves the tree dirty and the check names it.

**6. What crosses a link is a subset of what `export` allows.** A peer sees an area only if its
representative's *file* says `export: yes`; an audience sees only its own. Checked by
`check/peer-check.py` and `check/exchange-check.py`, against file truth (3), not the committed
table — the 2026-10-05 defect was exactly the committed table disagreeing with the file.

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
else; a document's frontmatter has no `state`, `supersedes`, `current`. The fixture contract says
this for fixtures; the live validator is to say it for the repository.

**10. Secrets are never in tracked files.** A token lives in the environment; a tracked file names
the variable (`token_env`) and nothing else. Checked by a scan of every tracked file, in `check/`,
not by hand before a push.

## What is not on this list

Things that are true but are design, not invariants: one sentence per area; `use_when` is what an
agent routes on and what a peer reads; ages come from git. They follow from 3 and 4.

## How the list is used

No new mechanism until every existing one has the invariant it depends on checked. A finding that
does not map to one of these ten is either a new invariant — add it here first — or a bug in an
existing one, named by number in the commit.
