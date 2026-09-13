# Scenarios — the routing table over a whole lifetime

Everything else in `check/` asks whether one call answers correctly; a scenario asks whether **the
thing an agent reads still tells the truth after the ontology has been lived in** — areas created,
advertised, emptied, deleted, and created again.

Two runners, because there are two lifetimes. `check/scenarios.py` is one backbone over time
(**A**–**K**); `check/room-check.py` is a room over time (**L**–**N**), which became a lifetime worth
having the day an exchange started shipping in the default install. `check/cross-check.py` is
**P** — the two crossed, which is where three real defects were: a promise that was right for a local
reader and wrong for a remote one is invisible from either side alone. All three run against throwaway
ontologies they start themselves, because several of these delete everything.

```sh
docker compose exec ontology python3 /tmp/check/scenarios.py     # see the header of the file
./check/room-check.py
./check/cross-check.py
```

## Why these and not others

Three properties are worth this much machinery, because each one fails silently:

**Residue.** Deleting is where a derived tree goes wrong — a row left in `CORE.md`, an id left in
`regions.json`, a directory left behind. None of it errors; the next agent just reads a routing table
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
| A4 | One deleted → gone from hop 0, **and its row is gone from `CORE.md`** |
| A5 | All deleted → byte-for-byte the state A1 described. No residue in `regions.json`, and the `CORE.md` table keeps its header so the next area can be written into it |

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

## J — the publish that fails after the commit

The commit is inside the transaction; publishing is after it, and publishing can fail on its own.

| | What it proves |
|---|---|
| J1 | A write whose publish fails is not reported as failed, and says the checkout is behind. It used to answer `500 internal error` for a write that had fully succeeded — an agent told that retries and gets `409 exists`, a person presses Submit again, and both then act on a lie about what is in the ontology |
| J2 | The commit stands and the entity reads back straight away. Reads serve the repository, not the checkout |
| J3 | `/healthz` shows the published tree behind the repository — the exact comparison the screen's bar makes |
| J4 | The next successful write catches the checkout up. Nothing needs undoing |

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

## L — membership in a room

`check/room-check.py`. Two backbones and an exchange. Registering one is an ordinary Tuesday;
**removing** one is the widest-blast-radius button on the operator's screen, and what it must not
touch is as much of the scenario as what it must.

| | What it proves |
|---|---|
| L1 | The shipped shape: one backbone, one exchange, nothing to reflect. Hop 0 must read exactly as it would with no exchange — same rows, absence claimable, **nobody named** — or every single-backbone install is being told about a link it does not have |
| L2 | A second backbone registered but not yet advertising changes nothing at hop 0. Being in the room is not the same as sharing |
| L3 | It advertises → the row arrives with nothing restarted, what it points at is readable straight away, and the absence sentence starts naming the room it comes through. A row that appears without its documents is a promise the link cannot keep |
| L4 | Removed at the exchange → its rows and **their addresses** go from the other backbone, absence goes back to naming nobody, and **its own ontology is untouched**: it simply stops meeting here |
| L5 | Registered again → the row comes back |

## M — the room itself goes away

`check/room-check.py`. Not a member: the exchange. This scenario exists because the default changed
under the older ones — an exchange now ships in every install, which means every link in every install
runs through one process that nobody had yet switched off on purpose.

| | What it proves |
|---|---|
| M1 | Each backbone keeps answering, keeps serving **its own** areas, drops the rows it can no longer stand behind, says the list is incomplete, **stops claiming absence**, and names what failed and why. A read across the dead room is not a 404 — nobody is saying no |
| M2 | It comes back → used again unprompted, and absence may be claimed again. A backbone that stayed cautious for ever after one blip is as wrong as one that never noticed, and much harder to see, because everything still works |

## N — an audience over a lifetime

`check/room-check.py`, with the steady states in `peer-check.py` and `exchange-check.py`.

| | What it proves |
|---|---|
| N1 | An audience naming the reader changes nothing for it — and does not hand it the list. Who else was considered is not the reader's business |
| N2 | An audience naming somebody who is not in the room leaves **everyone** out, the address stops working and not just the row, the backbone still holds it locally, and **nothing anywhere errors**: the link is up, because "you are not on the list" is not an outage and must not suspend the absence rule |
| N3 | Taking it away puts the area back, address and all |
| N4 | It goes through the **review queue**, scope `audience`, like the line it narrows. An empty `after` is a decision here and a mistake everywhere else; there is no drafting it, because who may see something is not in the ontology for a model to read |

N2 also pins the one thing the operator's view must keep showing: a member advertising an area, whoever
it is for. Health is not policy, and an audience that showed up on the exchange's screen would be
visible to the one party it does not restrict.

## P — where the new configuration meets the old

`check/cross-check.py`. Two backbones and an exchange, with the features that were built before links
existed switched on beside them. Everything else about peering asks *does a link work*; these ask the
question that only appears once there is one: **which of the promises this ontology already makes are
still true when the reader is another backbone?** Each was a settled answer for a local reader and a
different question for a remote one, and three of them were wrong.

| | What it proves |
|---|---|
| P1 | A **draft** is hidden from a listing and answers by address. Right for the owner — "draft" means unfinished, not secret — and across a link that listing is the *only* access control there is, so anyone holding yesterday's address kept reading a thing that had been taken off the table. Now 404 across a link, indistinguishable from a node that was never there, and unchanged locally |
| P2 | A **hand-edited tree** refuses writes and must keep serving a peer. The tempting answer is to stop until somebody tidies up, and it is wrong twice over: the peer would see an outage, stop claiming absence, and none of it would be true |
| P3 | An **overlay** refuses an address across a link — it narrows this backbone's own tree, and one that quietly got smaller whenever a link dropped would turn "look here" into "this is all there is". The refusal was right and its *reason* said the address had been assembled, when hop 0 had printed it and every table says to follow one exactly as printed. Blaming the reader for doing the documented thing is worse than not refusing |
| P4 | An **audience and an outage** are two reasons a row is missing and only one of them suspends absence. Off the list → the row goes, absence stands. The link then drops → the outage is what is reported. It comes back → the policy is what remains |
| P5 | A **252-character id** — the longest there is, because `.md` makes it 255 — crosses a room whole, three prefixes deep, and reads back untruncated |
| P6 | **Deleting** an exported area, as opposed to withdrawing it. Refused while it holds anything, by a rule written before links existed and still right; once empty, the row and the address go at the peer, as that backbone saying no rather than a link that failed |

A fourth defect was found while writing P3 and is checked there: a malformed overlay member came back
`500 internal error`, naming neither the mistake nor the fix — the class of bug section I exists for.

## Deliberately not here

**D — moves and containment** (`write-paths.sh` already moves a node within an area, across areas,
refuses a loop, and refuses deleting a node that holds one).
**E — absence wording and invented addresses** (`mcp-check.py` already walks that).
**O — rooms meeting rooms** (`ix-peering-check.py` walks one hop across, two hops refused in both
directions, the deadlock and the mislabel).
**Withdrawal latency** (`refresh-check.py`, which needs the cache turned *up* rather than off and so
cannot share a runner with anything here).

Duplicating them would mean two places to update and one of them going stale.
