# Links between backbones

RouteMinds that must not become one, meeting where it does not merge them.

**An install is one backbone and an exchange, from the first `docker compose up`.** With one backbone
the exchange reflects nothing and costs a container — and that is the price of the second one being a
file and a registration rather than a migration. Two backbones *can* peer directly and the code still
does it; the default is the exchange because the moment somebody adds a second backbone is exactly
the wrong moment to be rewriting the first one's configuration.

## What it is for, and what it is not for

**Not scale.** hop 0 is about 1.3 KB with five areas; fifty would be thirteen, which is nothing to a
model. The table grows with areas and areas grow slowly. If hop 0 feels big, split areas.

It is for **ownership**: two ontologies that must not merge. Different owners, different review
queues, different git repositories, different legal boundaries. Head office and a subsidiary. A
company and its supplier. Engineering and back-office under different heads.

Two teams who *should* share a vocabulary should share a repository. A link is for when they must not.

## The shape

```
   this backbone                        the peer
   ─────────────                        ────────
   /v1/regions          hop 0, its own areas *and* the peer's
   /v1/peers/<name>/…   ─── relayed ──▶  /v1/export/…   (token, read-only, shared areas only)
```

An area crosses by carrying **`use_when_export`** on its representative, and by nothing else.

## Sharing is opt-in, per area, in writing

`use_when_export` is the line this area shows in *another* backbone's hop 0. Absent means the area
crosses no link at all — there is no default that shares, and "we forgot to exclude it" is not a state
this can be in. The coarse half of export policy falls out of that: what is shared is what somebody
wrote a sentence for.

It is a **second** sentence rather than a reuse of `use_when` because an advertisement is written for
one backbone's hop 0 and has no reason to be true in another's. A subsidiary's *"needs head-office
approval"* means nothing read at head office.

It goes through the review queue, scope `peer`, for the reason every other advertisement does: what an
area says about itself is the one thing the whole system routes on. Across a link that stops being a
nicety, because the reader is another organisation.

## And who, when it is not everybody

`export_to` on the same representative names the peers an area crosses to. Absent — the common case —
means everybody `use_when_export` opened it to. It can only ever **narrow**: an area with no export
line crosses to nobody, and naming an audience for it restricts nothing, so that is an error rather
than a warning. It is the one of these mistakes that reads exactly like a restriction that is working.

The names are peer names as the enforcing side knows them: this backbone's own `peers.yaml` on a
direct link, the exchange's `members.yaml` behind one. In practice both are the organisation's short
name, and a name that could not be a member is refused.

**Enforcing it needs the caller to have a name, and that is what one secret per link buys.** A list of
peers is worthless against a caller nobody can tell apart. Two secrets — one each way — is legal, is
what most people write first, and quietly costs exactly this: the far end is anonymous, and an
audience closes to it. Fail closed is the deliberate choice in both directions, for a caller with no
name and for a reader an exchange declined to name. The alternative reads better and is the bug: an
unnamed caller falling through to *no audience matched, so show it* turns a restriction into a
decoration.

**Behind an exchange the two halves are enforced in different places, and the reason is worth saying
plainly.** A backbone answering a room sees the room, not the reader, so it hands the room the rows
with the audience written on them and the room drops the ones the asker is not named in — which means
the room *sees* what it will not pass on. That is inherent to anything on a data path and is the
sharpest form of "who should run an exchange". The **document** behind such a row is refused at the
backbone that owns it: the room says who it is fetching for (`X-Peer-For`), and the backbone applies
the audience to the prose. The listing is composed by whoever is speaking to the reader; the prose is
served by whoever wrote it, and only the second of those is a boundary rather than a policy.

A backbone believes `X-Peer-For` only from a peer its own `peers.yaml` calls `kind: exchange`. A claim
that gets a caller **more** is exactly the one that cannot be taken on the caller's word — the mirror
of `X-Peer-Kind`, where the claim gets the claimant less and is therefore safe.

An area that is not on your list answers **404**, the same as one that was never shared. Whether a
backbone holds something it has not shared with you is itself something you have no business learning.

The same rule reaches one thing that is not an audience at all. A **draft** entity is hidden from its
area's listing and answers by address, which is right for the owner — draft means unfinished, not
secret — and was a hole across a link, where the listing is the only access control there is. Anybody
holding an address from before it became a draft kept reading it. It is 404 across a link now, and
unchanged locally. docs/SCENARIOS.md P1.

It travels the road the line it narrows travels: the **review queue**, scope `audience`, with no
immediate-apply path. The two together are the whole export decision, and a widening that could be
made with a direct write while the wording needed a second pair of eyes would put the queue in front
of the smaller of the two. One rule is its own: an empty `after` is a decision here — *everybody this
area already crosses to* — and a mistake everywhere else. And there is no drafting it. The other
scopes revise a sentence about what an area holds, which is in the ontology and can be read; who may
see it is a decision about other organisations, which is not in here and is nobody's to guess.

Neither this nor `use_when_export` has a field on the map screen yet. Both are API and queue.

### A different sentence for one reader

`use_when_export_for` on the same representative maps a peer name to the line **that** peer is shown
instead of the default. Everybody else keeps the default and nobody is told there are other versions.

It is applied where the audience is applied and for the same reason: the backbone that owns the area
sees the room, not the reader, so it hands the room the map and the room picks. The lines meant for
other members are dropped on the way out — who else is told what is between them and the origin.

The rules are the default line's rules, one per entry, because each becomes exactly the same cell in
exactly the same kind of table: one table cell, no `|`, not the `one_liner`. Two more are its own. An
override **identical to the default** is an error rather than a warning — it reads as a decision to
say something different and says the same thing, so the day the default changes one reader silently
keeps the old sentence and nobody is looking there. And an override for a peer the audience leaves out
is an error, because it would never be read.

### The screen

All three are on the area's rack, under **Across a link**: the line, who it crosses to, and a
different line for one reader. Three sections and three proposals, not one form with three fields —
"stop advertising this area" and "reword it" must never arrive as one thing to say yes or no to.

Each goes through the review queue with its own scope (`peer`, `audience`, `peer-line`), and the
review card names the peer a `peer-line` proposal is for: without it a reviewer sees
`use_when_export_for` and two sentences with no way to tell whose line they are, which is the whole of
what they are being asked to judge.

**Withdrawing takes the whole decision with it.** Clearing the line clears the audience and the
per-peer overrides alongside it, and the answer says so. They narrow and replace a line; with no line
there is nothing to narrow and nothing to replace, and left behind they are state that means nothing
— which the validator refuses, so the withdrawal itself failed with advice written for the opposite
act. The cascade only ever removes, so nothing about it can widen what an area shares.

**Withdrawing goes through the queue too.** An empty `after` on scope `peer` is allowed against a
non-empty `before` and refused against nothing — the same empty string is *I have not written it yet*
and *stop this area crossing*, and only the second is a decision. Until 2026-09-13 it was refused
outright, which meant the one export decision with no queued path was the one that takes knowledge
away from another organisation.

## Taking one back

Rows go when the peer stops advertising them, and until recently they went *eventually* — within
`ADVERT_TTL`, five seconds at each hop, so ten or fifteen across a room. That is fine in one direction
and not in the other. Advertising something late is a delay; **withdrawing** something late is the
withdrawn thing still sitting on somebody else's table, and narrowing an audience is a withdrawal for
whoever just left the list.

So a backbone whose **export set** changes — which areas cross, the line each shows, who each is for —
posts `/v1/export/refresh` to its peers, and their only response is to forget what they remember about
it. Nothing is stored and nothing becomes readable that was not readable before: only sooner. An
exchange passes it on to its other members, because a withdrawal that reaches the room and stops there
still waits out every member's own cache.

**A hint, not a protocol.** `ADVERT_TTL` remains the guarantee and failures are swallowed: a peer that
is down is not a reason to fail somebody's save, and it reads the new set on its own within seconds of
coming back. It is sent off the request thread for the same reason.

It fires on the export set and not on the revision, because most commits change nothing a peer can
see and a poke on each one would tell every peer to re-read for somebody fixing a typo in a document
body.

A hint carries no path to check itself against, the way an advertisement does, so it carries a budget
that only goes down. The flood stops because it must, not because the rooms happen to be wired into a
tree.

`./check/refresh-check.py` — 17 assertions with the cache turned **up** to thirty seconds rather than
off, which is the only way to tell a fresh answer from a lucky one. The control comes first: the same
withdrawal made behind the server's back stays visible, and then the hint takes it off a table two
hops away.

## A domain, and what a kind is allowed to do

A **domain** is one exchange and the backbones around it. Between domains the question stops being
*which areas* and becomes *which sorts of thing* — and `vocab.yaml`, which is already where a kind is
defined, reviewed and committed, is where that is written:

```yaml
kinds:
  - id: table
    desc: a table of values — amounts, caps, rates, day counts
    export: no          # this sort of thing stays inside this backbone
```

**One decision per kind, not one per entity.** Twelve, not seventy-nine. And a **deny** list rather
than an allow list: the area-level `use_when_export` is already the opt-in, and making an export a
twelve-part act would mean the part everybody skips is the one that matters. A value that is neither
yes nor no is refused rather than read as one — `export: maybe` reads as caution and would be
permission.

**Listing and fetch agree, and that is the whole of the difficulty.** A row dropped from a table and
still readable by address is a leak; a row left in a table and refused on fetch reads as an outage,
and following an address exactly as printed is what every table tells an agent to do. So a denied kind
goes from the listing, its address answers the same 404 as something that never existed, and the fetch
walks the whole parent chain — a published child of a hidden parent is in no listing either.

An area whose **face** is of a denied kind does not cross at all. Its rows are the representative's
children, so offering it would offer a table nothing in which can be read, and an empty table reads as
*there is nothing here* rather than *you may not see it*.

None of this changes what the owner holds. It is a policy about what leaves.

## Who read what

**Nothing is copied and nothing is kept.** A relayed document is held for the length of one request
and discarded — no cache at the reader, which is the difference between a link and a merge. The cost
is accountability: with a physical copy there is at least an artefact at the far end, and this leaves
nothing anywhere unless the owner writes a line. *What did the other domain read from us last month*
is the first question anybody asks.

Until 2026-09-13 the answer available was an HTTP access line:

```
172.20.0.2 "GET /v1/export/nodes/payroll-overview HTTP/1.1" 200
```

which does not say who — and every read through an exchange arrives from the same container, so they
were all identically anonymous.

The owner records one JSON line per read: when, **which link carried it**, **who was at the far end**,
what was asked for, served or refused, and how big. Two names because they are two questions, and
behind two rooms the second is the neighbouring room rather than the backbone inside it — not a gap,
but what no-transit means. A room's members are its own business.

**Refusals are recorded too, and matter more.** A served read is the ordinary case; a refused one is
somebody following an address they should not have, and a run of them is the only signal there is that
a link is being probed rather than used. A wrong token is recorded before the door.

To stderr always, so an install that configures nothing still has it, and to `ONTOLOGY_ACCESS` as well
— one file per UTC day, because stderr rotates away and an audit that rotates away is not one.

`./check/domain-check.py` — 31 assertions on two domains: the policy on both the listing and the
address, the whole area when its face is denied, both names in the record, a refusal with its reason,
and a document read across the boundary that leaves no trace anywhere on the reader's disk.

## The export surface is separate, not the ordinary one behind a check

`/v1/export/…` builds every answer from the exported set, so no path through it — and no mistake in a
token check — reaches an area nobody shared. A filter applied on the way out has to be right every
time; a surface built from the exported set is right by construction.

* **404, never 403,** for anything outside it. Whether this backbone holds something it has not shared
  is not the peer's business either.
* **Every address leaving it is moved onto it.** The ordinary reader prints `/v1/nodes/x`, and a peer
  following that resolves it against *its own* ontology — with colliding ids it would not even fail,
  it would quietly read a different node with the same name.
* **Read-only.** Writes go to the backbone that owns the area, through its own screen and its own
  review queue. Not a limitation waiting to be lifted: two ontologies that write to each other have
  been merged, and not merging them is what a link is for.

`ONTOLOGY_PEER_TOKEN` unset — the default — makes the whole surface answer 501.

## Documents are relayed, not linked to

hop 0 hands out this backbone's own addresses (`/v1/peers/hq/…`) and this service does the fetching.
The alternative — printing the peer's URL and letting the agent go direct — is simpler and wrong for
one reason that outweighs the rest: **every agent would then need every peer's credential.** Relaying
keeps it in one place, in this service's environment, where the LLM key already is. Firewalls are the
second reason and the smaller one.

Nothing is cached but the advertisement, for five seconds, failures included. That cache is for the
sad path — a peer that is gone would otherwise cost every request the full timeout — and not for
answering on a peer's behalf. **A failure is never served from an earlier success.** Documents are not
cached at all: a cache of somebody else's ontology is a copy, and a copy is what a link exists to
avoid.

Five seconds is short because of what it bounds: while a success is cached, a link that just died
still reads as alive. No cache makes that window zero, so it is kept small and stated here.

## What absence means once there is a link

This is the part that matters. The design rests on one sentence — *only hop 0 may say something is not
here* — and it is true because hop 0 is the whole world. **A link makes it false.**

So the sentence is computed, not written down, and the MCP takes it from the API: whether the list is
still the whole world is not something a client can know.

| | What hop 0 says |
|---|---|
| no links | "Nothing outside this list exists in RouteMind." As before |
| every link up | "…or in the backbones it is linked to (HQ, BRANCH)." Absence may still be claimed |
| **any link down** | **"This list is incomplete."** The rows it cannot stand behind are dropped, the failing links are named with the reason, and the agent is told **not to say anything is absent** while a link is down |

There is no smaller honest claim than none. A table missing rows cannot be the grounds for saying
anything is missing.

For the same reason, **"the peer said no" and "I could not reach the peer" never merge.** A relayed
404 is that backbone speaking and is carried through as its own answer; a timeout is nobody speaking
and comes back 504 with `reason: peer_unreachable`.

## Trying one out

Nothing about the backbones already running changes. Each one's `peers.yaml` holds a single entry —
the exchange — and still holds one when there are ten.

```sh
mkdir -p data-b/repo data-b/publish data-b/overlays data-b/harness data-b/access
docker compose -f docker-compose.yml -f docker-compose.peer.yml up -d
#  http://localhost:8080   this office
#  http://localhost:8081   the other one
```

The `mkdir` first, and it is not tidiness: these are bind mounts, docker creates a missing one **owned
by root**, and the container runs as `KNOWLEDGE_UID` and cannot write it. It says so — *"/data/repo is
not writable by uid …"* — and it says so after failing to start, which is one step later than useful.
`install.sh` does this for the first backbone and the operator's screen prints it in the plan it hands
you; only the line you copy out of here was missing it.

Two full installs, each with its own repository under `data/` and `data-b/`. Two services rather than
one service with two data directories, on purpose: **this is the remote case with a shorter cable.**
When the two are in different companies nothing changes but the URL and who holds the token.

Four things, and the operator's screen prints all four for you:

1. `EXCHANGE_TOKEN_BRANCH` in `.env` — one secret, used in both directions.
2. `data-b/repo/peers.yaml`, naming the exchange. Its half of the declaration.
3. A member entry at the exchange, naming it. The other half — neither side alone enrols anybody.
4. A `use_when_export` on whatever it should share, through **Advertise upstream** (scope `peer`).

Only the fourth is about knowledge, and only the fourth goes through a review queue. The first three
are wiring.

`peers.yaml` is in the repository because who a backbone is linked to is part of what it is: it
belongs in git, in review and in the history. The token is the opposite and comes from the
environment — the split `.env` already makes for the LLM key.

## On the map

**One card per domain, and the map draws the one you picked.** Every domain hop 0 knows about gets a
card: this backbone, whoever is advertising through a link, and any link that is not answering. The
card carries the name, the revision, a shelf and the first few area names; the map below is the detail
for whichever card is selected.

**Two walls, not one.** *Here* holds this backbone alone; *across a link* holds everyone else. This
backbone is not a peer of itself, and a card of it sitting in the row with the others says it is. The
split earns something else too: a group heading that says *across a link* makes the same words on each
of its cards pure ink, so the chip is kept for the one state a heading cannot carry — a link that is
not answering. The shelves still share **one** scale across both walls, because comparing what this
backbone advertises against what reaches it is the comparison most worth having.

The wall appears **only once there is more than one domain**. A single-backbone install — which is
most of them, and the one `install.sh` makes — sees exactly the screen it saw before this existed. A
wall of one is not a wall.

Everything on the wall was tried against the alternatives first, and the alternatives lost for reasons
worth keeping:

  * **One row for everything**, which is what this was. Every area, local and remote, on one bus. It
    breaks at five backbones — not by being wide, but by *overlapping*: the local backbone is pinned
    to the middle of the canvas and each remote device sits at the midpoint of its own group, so one
    of them eventually lands on top of it.
  * **A ring of backbones.** It puts an order on a set that has none — there is no backbone 1 and
    backbone 2 — and it turns the other domains into a menu rather than a picture.
  * **Hops as vertical tiers, with the rooms as clouds.** True to the topology and still a diagram of
    a structure nobody needs to look at while working.

The cards are **small multiples**: the same card repeated, so the eye reads the difference in the data
rather than re-reading a new layout each time. Two rules follow from that and are not negotiable.
Every card keeps every slot, filled or not — a card that changes shape with its contents defeats the
whole point. And the shelves share one scale, so *five of five* and *one of five* are one glance apart.

The shelf counts **advertised areas only**. What a remote domain *holds* is not knowable from here and
must not be guessed at: an area nobody advertised does not exist to this backbone, and a bar implying
otherwise would be inventing the one number the design refuses to send.

A link that is not answering keeps its card, marked, with nothing on the shelf. A wall that dropped it
would make a failed link look exactly like an install that never had one. It is a card for the **link**
and not for a backbone: behind an exchange this backbone cannot tell "that backbone stopped
advertising" from "that backbone is gone" — only the link's own state is knowable from here — so the
card says the knowable thing.

A peer's areas are still that peer's. Both installs in the example have a `payroll`, and picking each
card in turn shows two different areas, which is right: nothing merged them.

**A working exchange is not drawn.** The areas behind it are grouped by the backbone that owns them,
not by the one that carried them — hanging three backbones' areas under one EXCHANGE device would say
the exchange holds them, and it does not. Network diagrams draw the adjacency and not the fabric
between, for the same reason. The address still says the whole truth
(`/v1/peers/ix/peers/branch/…`), which is where a path belongs.

An exchange that has **failed** is drawn, because then it is the thing that broke and naming it is the
only useful thing left to say.

And nothing across a link is cached by the screen. The map's own cache holds this backbone's areas —
as good as the revision they were saved at — and refetches the remote rows every load. A saved picture
cannot know whether a peer is answering now, and drawing a dead link as a live one is the one mistake
this picture must not make.

## Checks

`./check/peer-check.py` — 66 assertions on two throwaway backbones linked both ways. Mostly negative:
things that exist, read fine locally, and must still come back 404 across the link.

Half of those are **steady states**; the other half are the transitions, which is what makes this
dynamic routing rather than a config file that happens to be read over HTTP:

| | |
|---|---|
| an area starts advertising | it reaches the other backbone with nothing restarted, and what it points at is readable straight away — a row that appears without its documents is a promise the link cannot keep |
| an area stops advertising | the row goes **and so does the reach**. A withdrawal that only hid the row would leave every address still readable, which is a missing menu item, not a withdrawal. The 404 is the other backbone saying no, not a link that failed |
| the link goes down | the rows it can no longer stand behind are dropped, and absence stops being claimed |
| **the link comes back** | it is used again unprompted, and **absence may be claimed again**. A backbone that stayed cautious for ever after one blip would be as wrong as one that never noticed, and harder to see, because everything still works |
| an audience is written | the peer it names keeps the area; a caller that cannot be named loses it, address and all — and the link still reads as up, because "you are not on the list" is not an outage and must not suspend the absence rule |

## The exchange

Where backbones meet. It is in the base compose file and `install.sh` attaches the first backbone to
it, so an install is wired for a second before anyone wants one.

Everybody names the exchange and nobody names anybody else, so N backbones take N links instead of
N(N−1)/2:

| backbones | direct | at an exchange |
|---|---|---|
| 2 | 1 | 2 |
| 3 | 3 | 3 |
| 6 | **15** | 6 |
| 10 | **45** | 10 |
| **adding one** | **edit every other backbone** | **one registration** |

At two it costs more than it saves, which is why this is a decision rather than arithmetic. What it
buys is that the shape never changes: adding the tenth backbone touches the same one file as adding
the second, and the nine already running are not edited, restarted, or aware of it.

**It is not a backbone and cannot become one.** No repository, no areas, no vocabulary, no
`/v1/regions` — so no hop 0, and the sentence everything rests on has no third kind of thing to be
confused about. That is why it is called an exchange: an IX carries no prefixes of its own and nobody
mistakes one for a network. Calling it "backbone zero" would have invited the next person to give it
areas.

To a backbone it is indistinguishable from any other peer — same `/v1/export`, same token, same
read-only rule. **No backbone has any code that knows what an exchange is.**

It does not decide what is shared. It reads what each member published and can no more widen that
than any other peer can; `use_when_export` stays in each ontology, through each review queue.

**One secret per member, used both ways.** The exchange presents it when reading that member, and the
member presents it when reading the exchange. There is no shared password and no observer role, so
every caller has a name — which is what makes the next paragraph possible.

**Split horizon.** A member is never handed back what it advertised. Without it every backbone would
see its own areas twice, once locally and once reflected, and the second copy would look like somebody
else's.

**The path.** Every reflected row carries the members it came through, nearest last. An agent can see
how far away a piece of knowledge is — two hops is somebody else's somebody else — and a row whose
path already names this exchange is dropped. Backbones never re-advertise what they learn, so one
exchange cannot loop; two exchanges peering can, and this is what stops it. BGP's AS_PATH, for BGP's
reason.

The address carries the path too: `/v1/peers/ix/peers/branch/regions/payroll` reads as *through the
exchange, to the branch, its payroll*. Everything that reads an address peels **every** prefix, not
one.

`./check/exchange-check.py` — 31 assertions on three backbones and an exchange: reading a document two
backbones away, killing a member to watch the others carry on, and the same advertise/withdraw
transitions one hop further out. Those are worth repeating here because an exchange holds a cache and
a split-horizon rule in between, and either could turn a withdrawal into something that stays
visible — the failure that looks exactly like everything working.

## A secret and a public address

One secret per link, used in both directions, and three things about a shared secret that a test of
"does the right token work" never reaches.

**It is compared in constant time.** `==` on strings stops at the first differing byte, so how long it
takes says how much of a guess was right. Between two organisations that is a way in needing no bug
and nobody's mistake, only patience. An empty expected secret matches nothing, so a link with no token
configured is closed rather than open to everyone.

**It will not travel in clear text to a public address.** `http://` inside a compose network or a VPN
is the ordinary shape and stays out of the way; `http://` to an address outside every private range is
a bearer token on the wire, and a link refuses to present one there and says so. The refusal is
**ours** — `reachable=True` — because it is this end declining, not the peer being unreachable, and
the absence rule must not be suspended over a decision we made. A name that does not resolve is not
treated as public: a peer that is simply down would otherwise produce a refusal about secrecy and send
whoever reads it looking in entirely the wrong place.

**It can be rotated without a flag day.** `also_accept_env` on a `peers.yaml` or `members.yaml` entry
names a second variable that is still accepted. Add the new secret there on both sides, switch what
each presents, then drop the old one. Without it the only way to change a secret is to stop both ends
at the same moment — which is why nobody does, and a room makes it worse, because every member's link
stops at once.

`./check/peer-check.py` — the last 21 of its 87 assertions.

## Two exchanges

A member of an exchange may itself be an exchange (`kind: exchange`), which is how two organisations
meet without either joining the other's room. It is the same contract used a second time — an exchange
reads a neighbouring exchange with exactly the member code it uses on a backbone — and it adds two
rules that only exist once there are two rooms.

**Who may enrol whom: each side enrols the other, or there is no link.** The same two halves as
everywhere else, with both of them now held by operators. IX1 names IX2 in its `members.yaml`, IX2
names IX1 in its, one secret between them used in both directions. The operator's screen prepares
exactly this and can only finish half of it: it hands back one entry to keep and one to send, and the
link starts working when the second person has agreed enough to paste theirs. Until then the room
reports the neighbour as unreachable, which is the honest answer.

**No transit.** A room offers a neighbouring room its own backbones, and never what a third room told
it. HOME sees REMOTE and does not see FAR — not because FAR is secret, but because nobody at either
end agreed to a relationship with the other, and the operator in the middle would be answering for two
rooms that never met. An IX route server declines transit for the same reason. It also bounds every
path at one exchange-to-exchange hop, which is what makes a ring of exchanges structurally unable to
loop rather than merely unlikely to.

The rule is applied **before** the neighbour is read, and that is not an optimisation. Reading is a
request, and a request answered by making the same request is how two rooms hang each other up: IX1
asks IX2 what it is advertising, IX2 asks IX1 to find out, and neither ever answers. Filtering
afterwards leaves that intact and perfectly hidden — the rows come out right whenever the timeout is
longer than the wait. This was written the wrong way round first and the check found it as an outage
on a link that was fine.

**The backbone has only one lock, and it is the same word.** `kind: exchange` in a backbone's own
`peers.yaml` is what tells it that it is answering a room — and here no header can stand in for the
label, because believing a caller that says it is a room would hand that caller the *whole* shared set
instead of its own share. That is the one direction a claim must never be taken on the caller's word.

So the label is load-bearing and getting it wrong fails silently: audiences and per-peer lines stop
having any effect, a document restricted to a member comes back 404 because the room could not say who
it was fetching for, and every screen still looks fine. A backbone now notices — a peer declared as a
backbone that answers with the exchange schema gets a **note** on its link, naming the line to fix.
Not an error and not `reachable: false`: the link is up and carrying rows, and calling it down would
suspend the absence rule over a line in a file. Every install made before 2026-09-13 has this exact
file, so `install.sh` says so too rather than editing somebody's repository behind them.

**Two locks at the exchange, because `kind` is one word typed by hand.** The label in `members.yaml` is what
stops the read from happening, and only a decision made before the read can prevent the hang. The
asker's own `X-Peer-Kind` header is what still holds when the label is wrong. Believing a caller about
what it is, is safe here and nowhere else: the claim can only ever get the claimant **less**. With the
label wrong *and* the caller saying nothing, there is nothing left to go on and the knowledge crosses —
so the operator's screen names the line to fix rather than reassuring anyone that it does not matter.

A neighbour that answers with the exchange schema while declared as a backbone is reported as exactly
that, and its rows are dropped on the way to another room. That net catches the leak; nothing catches
the hang but the label.

`./check/ix-peering-check.py` — 37 assertions on three rooms in a line, each with a backbone of its
own: one hop across, two hops refused in both directions, a document read through three relays, the
deadlock, and the mislabel with both of its halves.

### Seeing it, rather than reading about it

Everything above is one throwaway process per backbone inside a check. To look at it:

```sh
./examples/seed-demo.sh
docker compose -f docker-compose.yml -f docker-compose.peer.yml \
               -f docker-compose.admin.yml -f docker-compose.demo.yml up -d --build
```

Six backbones and two rooms — HOME and BRANCH on IX, VENDOR, AUDIT and DEPOT on PARTNER-IX, and
LEGACY, a direct link that is declared and never started. Six areas out of nineteen carry a
`use_when_export` line, and the other thirteen stay home, which is the part that is hard to believe
until it is on a screen. The wall at http://localhost:8080/knowledge draws one card per domain and
LEGACY wears its own chip; the operator's screen at :8090 shows PARTNER-IX carrying five rows that
none of its own backbones wrote.

It is a demonstration and not a deployment: real domains are five separate installs with five
operators, and the only thing they would share is a member entry at each end. The seeder says what it
touches, skips anything already there, and only ever appends to `data/`.

## The operator's screen

```sh
docker compose -f docker-compose.yml -f docker-compose.peer.yml \
               -f docker-compose.admin.yml up -d
#  http://localhost:8090
```

Who is attached, whether each is answering, which revision, how many areas it advertises — and what it
takes to attach one more.

**It holds no docker socket and starts nothing.** The dangerous part of "add a backbone" was never the
`mkdir`; it is granting container-execution rights to a service that faces a network. What is actually
tedious is the rest — a name, four directories, a secret, a `peers.yaml`, a member entry, a compose
block, a free port — and none of that needs any privilege. So the screen prepares all of it and hands
back the command. **It thinks; docker runs; the operator stays the one who did it.**

**It cannot read what the members share, and cannot make an area cross.** The exchange has a second
door for the operator, and it answers membership and health and never a reflected row: you learn that
BRANCH is attached and advertising two areas, not what they are. An area crosses because somebody
wrote `use_when_export` on it in its own repository, through its own review queue — a screen out here
that could do either would be the way around the only rule that keeps sharing deliberate.

Two doors, two keys, and neither is a spare: a member's token does not open `/admin`, and the admin
token does not read the reflection. `EXCHANGE_ADMIN_TOKEN` unset — the default — means there is no
operator door at all.

Membership *is* the exchange's own state, so that it can edit: registering a backbone writes the
member entry, which is the exchange's half of the declaration. The backbone's half is still a
`peers.yaml` naming this exchange, written over there. Neither side alone enrols anybody.

`./check/admin-check.py` — 25 assertions, most of them about what the door cannot open.

## Not done

* **Two vocabularies.** A peer's areas are described by the peer's `vocab.yaml`, and this backbone's
  validator never sees them — which is correct, and must stay that way.
