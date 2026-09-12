# Links between backbones

Two RouteMinds that must not become one, with a wire between them.

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

```sh
docker compose -f docker-compose.yml -f docker-compose.peer.yml up -d
#  http://localhost:8080   this office
#  http://localhost:8081   the other one
```

Two full installs, each with its own repository under `data/` and `data-b/`. Two services rather than
one service with two data directories, on purpose: **this is the remote case with a shorter cable.**
When the two are in different companies nothing changes but the URL and who holds the token.

Then, on each side:

1. Give an area a `use_when_export`, through **Advertise upstream** on its rack (scope `peer`).
2. Write `peers.yaml` in that repository:
   ```yaml
   peers:
     - name: branch
       label: BRANCH
       url: http://ontology-b:8100
       token_env: ONTOLOGY_PEER_TOKEN_BRANCH
   ```
3. Set that variable, and `ONTOLOGY_PEER_TOKEN` for what this backbone accepts, in `.env`.

`peers.yaml` is in the repository because who a backbone is linked to is part of what it is: it
belongs in git, in review and in the history. The token is the opposite and comes from the
environment — the split `.env` already makes for the LLM key.

## On the map

A peer is a second backbone with its own bus, joined by a dashed wire. Its areas hang off **it**, not
off this one — drawn on a single bus they would read as areas of this ontology. Both installs in the
example have a `payroll` and the map shows two, one under each backbone, which is right: they are
different areas and nothing merged them.

A link that is down is still drawn, marked, with nothing under it. A map that dropped it would make a
failed link look exactly like an install that never had one.

## Checks

`./check/peer-check.py` — 36 assertions on two throwaway backbones linked both ways, including
killing one mid-run to watch the survivor stop claiming absence. Mostly negative: things that exist,
read fine locally, and must still come back 404 across the link.

## An exchange, when there are more than two

Two backbones peer directly and that is the simplest thing that works. Six that all want to see each
other need fifteen links. An **exchange** is where they meet instead: everybody names it, nobody names
anybody else, and six links do what fifteen did. The seventh backbone costs one link, not six.

```sh
mkdir -p data/exchange && cp examples/exchange/members.yaml data/exchange/
#  then point each backbone's peers.yaml at the exchange instead of at each other
docker compose -f docker-compose.yml -f docker-compose.peer.yml -f docker-compose.exchange.yml up -d
```

`members.yaml` lives under `data/` because it is this installation's, the way `data/repo` is — the
copy in `examples/` is a starting point, not a default.

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

`./check/exchange-check.py` — 22 assertions on three backbones and an exchange, including reading a
document two backbones away and killing a member to watch the others carry on without it.

## Not done

* **One export line for all peers.** Per-peer lines, and per-peer visibility, are a policy layer worth
  designing whole rather than smuggling in as a map.
* **Exchanges do not peer with each other yet.** The path attribute that makes it safe is there and is
  checked; what is missing is a member entry that points at another exchange, and the thought about
  who is allowed to enrol whom.
* **No withdraw.** A peer's rows go when it stops advertising them or stops answering; there is no
  message that says so.
* **Two vocabularies.** A peer's areas are described by the peer's `vocab.yaml`, and this backbone's
  validator never sees them — which is correct, and must stay that way.
