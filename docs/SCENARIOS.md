# Scenarios — the routing table over a whole lifetime

Everything else in `check/` asks whether one call answers correctly; a scenario asks whether **the
thing an agent reads still tells the truth after the ontology has been lived in** — areas created,
advertised, emptied, deleted, and created again.

`check/scenarios.py` is one backbone over time (**A**–**K**). It runs against a throwaway ontology it
starts itself, because several of these delete everything. (**L**–**P** were a room of linked
backbones over time and that room crossed with the rest; they were retired with standing links and the
exchange on 2026-10-08.)

```sh
docker compose exec ontology python3 /tmp/check/scenarios.py     # see the header of the file
```

## Why these and not others

Three properties are worth this much machinery, because each one fails silently:

**Residue.** Deleting is where a derived tree goes wrong — an id left in `regions.json`, a directory
left behind. None of it errors; the next agent just reads a routing table
with a row that fetches nothing.

**Advertisement is the whole interface.** An area that exists but says nothing to pick it by is
worse than an area that does not exist, because it costs a hop and answers nothing. So what reaches
hop 0, and what does not, is the thing to pin down.

**Absence is a claim.** Only hop 0 may say something is not here. Anything that changes what hop 0
lists changes what the system is entitled to claim.

## A — the routing table over a lifetime

| | What it proves |
|---|---|
| A1 | An empty ontology still prints a hop-0 table: a header, `(nothing here)`, and the absence rule. Empty is a state, not an error |
| A2 | One area created → it is at hop 0, with the sentence it is chosen by |
| A3 | A second → both, and the order does not depend on creation order |
| A4 | One deleted → gone from hop 0, the other untouched |
| A5 | All deleted → byte-for-byte the state A1 described. No residue in `regions.json`, and no `CORE.md` or `edges.yaml` for anything to drift into |

A5 is the one that matters. "It looks empty" and "it is empty" differ by exactly the bug this catches.

## B — what an area advertises

| | What it proves |
|---|---|
| B1 | Whether an area can exist with nothing to pick it by. Either the API refuses it, or hop 0 carries a row with an empty reason — both are defensible, but only one is true, and the answer belongs in a test rather than in someone's memory |
| B2 | A change to `use_when` reaches hop 0 — through the review queue, which is the only path that writes it |
| B3 | hop 0 lists areas and nothing else. A node reaching it would make the first table grow with the ontology, which is the thing this design exists to avoid |

## C — created, but not advertised

An **area** cannot be unadvertised: `regions.json` is built from every directory under `regions/`, so
creating one advertises it. A **node** can: `derive.py` drops `status: draft` from an area's node list.

| | What it proves |
|---|---|
| C1 | A draft node is absent from its area's advertised list and from the rendered table |
| C2 | What its address does when fetched directly. "The agent cannot see it" is either *hidden from the listing* or *refused on fetch*, and those are different promises |
| C3 | Clearing the draft makes it appear, with no other change |

## F — a VRF while the tree moves under it

An overlay names addresses in a tree that keeps changing. Nothing has ever tested the two together.

| | What it proves |
|---|---|
| F1 | An overlay whose member area is deleted afterwards. Reading it must not crash, and must not claim the deleted area still holds things |
| F2 | An overlay's rows are read at read time, not frozen at create time |

## G — the repository edited by hand

The README tells you to edit `vocab.yaml` and commit, so a dirty working tree is a state real people
reach — not an error case.

| | What it proves |
|---|---|
| G1 | Writes are refused there, and the refusal says why rather than failing somewhere further in |
| G2 | The screen is told **which** files, whole. It named the first one a character short: porcelain puts the path at column 3, and stripping the whole output ate the leading space of the first line only — so with one file dirty, the usual case, it named a file that does not exist |
| G3 | Reverting makes it writable again, with nothing left over |

## H — the clock expiry runs on

An overlay's age must not depend on where the service happens to be running.

| | What it proves |
|---|---|
| H | The same UTC stamp is the same age in UTC, Seoul, London, New York and Sydney — and that age is right. It was an hour out wherever summer time was in force: `time.mktime(...) - time.timezone` mixes a standard offset with a value that carries DST, and they cancel only outside it. Invisible in deployment, because the containers run UTC; visible to anyone who ran these checks on their own machine in July |

## I — a name that has to become a file

Three inputs are written straight into a path: a node id becomes `<id>.md`, an area name becomes the
directory, an attached file name is the file. Every filesystem stops one path component at 255 bytes.

| | What it proves |
|---|---|
| I1 | An over-long id is refused with a reason. None of the three was bounded, so each passed its kebab-case check, passed validation, and died inside the transaction on `OSError: [Errno 36] File name too long` — which the API could only report as `502 internal error`. Probing every malformed input the surface accepts (broken JSON, no `Content-Type`, wrong method, unknown path, an array for a body), these three were the only ones that came back with no reason |
| I2 | The same for an area name |
| I3 | The same for an attached file name |
| I4 | The longest name that fits is still written — 252 characters, because `.md` makes it exactly 255. A bound nobody has watched permit the longest legal name drifts down to whatever the first refusal happened to be |
| I5 | One byte over is refused |

## J — what the agent reads is the commit

There was a publish step until 2026-10-07: every write copied a checkout out for an agent runtime that
mounted it, and the screen warned "agents are reading an older tree" when the copy lagged. Agents here
read the repository through the API, so the warning was never true and the copy had no reader.

| | What it proves |
|---|---|
| J1 | A write answers with the commit it made |
| J2 | The revision the screen follows (`/v1/revision`) is that commit |
| J3 | No second, "published" revision is offered — by `/v1/revision` or `/healthz` — for anything to fall behind |

## K — two processes on one data directory

Nobody is meant to run two. They will: `--scale ontology=2`, a second install on the same mount, a
container left behind by a rebuild. The writer's lock was a threading lock and held only inside one
process, while the transaction it guards is a sequence of git commands on a shared working tree.

Twelve concurrent creates split across two processes, before: eight refused as "someone edited the
repository by hand" (nobody had), two 500s out of git's own `index.lock`, two callers told their
write failed while `git add -A` committed it under the other process's message, and the tree left
dirty with a file staged and never committed — the state in which every later write is refused until
a human runs git. None of that looks like a race from outside.

| | What it proves |
|---|---|
| K1 | Every write across two processes succeeds, **and what was reported matches what is on disk**. The second half is the one that matters |
| K2 | The tree is not left dirty, and the repository is still valid |
| K3 | A held lock gives up rather than hanging, and says a process is holding it — not that someone edited by hand |

## Q — the install a stranger gets

`check/install-check.sh`, and it is not run with the others: it clones the **committed** tree,
installs it in a temporary directory on its own port and image tags, and walks the export decision
end to end as another backbone's circuit sees it. Minutes, because it builds. Before a release, and after a change
large enough that you would not want to be the first person to find out.

Every scenario above builds its own world. This one is about the world a person arrives in, and the
mistakes are a different set — none of these could have come from a check, because a check never
appends a line to a `.env`, never reads a status code, and never runs anything in a container it did
not prepare.

| | What it found |
|---|---|
| Q1 | `install.sh` and docker compose read one `.env` and disagreed about which duplicate line wins — the installer waited on a port nothing served and said the stack had not come up, with a healthy stack behind it. Now `check/env-check.py` lifts the pipeline out of install.sh and runs it |
| Q2 | An accept that could not be applied answered **200**. Right in substance — nothing written, the proposal left pending — and every caller that branches on a status believed it, the screen included |
| Q3–Q6 | Found in the standing links retired on 2026-10-08: an audience refusing its own withdrawal, a refresh hint missing a field, checks dying on an empty seed, and a `mkdir` recipe one directory short. The last is now `check/env-check.py`'s to catch anywhere |

The image tags are the reason this can be run at all without thinking about it: they were shared, so a
verification build would have replaced the images the machine's own install next starts from.
`IMAGE_TAG` exists for that.

## Deliberately not here

**D — moves and containment** (`write-paths.sh` already moves a node within an area, across areas,
refuses a loop, and refuses deleting a node that holds one).
**E — absence wording and invented addresses** (`mcp-check.py` already walks that).
**What a circuit reads as the far end changes** (`follow-check.py`, which needs a second backbone).

Duplicating them would mean two places to update and one of them going stale.
