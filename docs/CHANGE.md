# A change set — several decisions, one commit, the lines over them decided

Decided 2026-10-09 (operator: "데이터를 넣을 때 필요하면 노드도 직접 만들고, 기존 구조를 변경해야 한다면 변형도
했으면 — 관련된 라우팅 테이블도 바뀌고. 하나의 변화로 인한 연쇄 작업까지 가능하도록").

## The problem it answers

`knowledge_place` put every document in as a leaf under the node the walk stopped at, and said "the
lines above were not changed — if one no longer says this is there, tell the person". Measured on a
real install, the result was flat: wide tables, no holders, and parent lines that quietly stopped
describing what hung under them. A person filing the same material folds it as it accumulates — a
holder with a one-line summary once three or four things belong together, the previous version
under "previous versions" once a new one arrives — and keeps the sentence above in step. Nothing let an
agent do that in one act, and nothing made the sentence above anybody's decision.

## One structure

```
POST /v1/changes          (dry_run: true for the preview; the same transaction, commit left out)
{
  "why":  "one line — it becomes the commit",
  "base": "<revision the tables were read at>",       optional
  "decisions": [ … at most KNOWLEDGE_CHANGE_MAX (20) … ],
  "expose": [ "<id or $ref>" ]                        what this knowingly makes readable through a circuit
}

create  { ref: "$h", name, one_liner, content?, kind?, parent: <id> | "$ref" | null, area?, use_when? }
move    { id, parent: <id> | "$ref" }
reword  { id, field: one_liner | use_when | name, after, before? }
write   { id, content }
keep    { id, field, why? }
delete  { id }
```

**A set is decisions, not a script.** At most one decision per (entity, aspect) — the aspects are
existence, parent, one_liner, use_when, name, body — and two on one aspect are refused by name. The
order of application is fixed by the server: creates (new areas first, then by parent reference),
moves, rewordings and bodies, deletes. So the same set in any order makes the same tree, the same
impact and the same ids, and `check/change-check.py` holds that. A `$ref` is the set's own name for
something it creates; the id comes from the same rule as any create, and the answer maps refs to ids.
A `create` with no parent is a new area's face: `area` is its directory, `use_when` the sentence hop 0
prints, and it is how "nothing at hop 0 covers this" stops being a dead end.

## The impact is computed, not guessed

> An entity is **impacted** when its table — its children's ids and their lines — differs before and
> after the set. Every impacted line must be decided in the set: `reword` it or `keep` it.

That one rule makes the cascade climb exactly as far as the rewording goes. Put a document under P:
P's table changed, so P's line is impacted. Keep it: P's parent's table is the same as before, and
nothing above is impacted. Reword it: P's parent's table changed, so its line is impacted — up to the
area's face, whose line is `use_when`, the one hop 0 prints. A move impacts both the parent it left
and the one it joined; across areas, both faces. A body edit changes no table and impacts nothing.

The answer carries the impact whole, and so does a refusal:

```
tables     every table that changes, before and after
lines      each impacted line: id, field, its text now, decided (reword | keep | null), because
exposure   entities that newly can or no longer can be read through a circuit (an exported area)
carried    what a move took along under it
```

A write is refused — 409, nothing written — while a line is undecided or an exposure is not
acknowledged in `expose`; a dry run reports them instead, with `applies` saying whether the set would
go. Through the MCP, **the refusal is the preview**: `here` prints the tables and the undecided lines,
and the next `here` carries the decisions.

## The base

`base` is the revision the decisions were made against — the placement walk sends the one its tables
were read at. If a file the decisions rest on — what they touch, the parents they name, and every
line on the way up from those — changed between `base` and HEAD, the set is stale (409, the files
named). Unrelated movement is fine; it is not a whole-repository lock. A `reword` may also carry
`before`, and is a conflict when the line no longer reads that.

## One commit, and the decisions in it

A set that applies is one commit; one refused anywhere — a late conflict, a stale base, the validator
— is no commit and a clean tree, even when earlier decisions in it had already written files
(`transact` rolls back with `reset --hard`, since a dry run restores after `git add`). `keep` is not
visible in a diff, so the decisions are the commit's trailers, where `git log` and the ages read them:

```
change: taxi receipts belong under the request

Create: late-night-taxi-receipts under purchase-request
Keep: purchase-request.one_liner — its line already covers evidence
Base: 4ce2bba…
```

## Three decisions, 2026-10-09

**A person at the map is shown, an agent is refused.** Every write's answer — the ordinary create,
the drag that moves a tile, a delete — carries `impacted`: the lines whose tables it changed. The
screen shows them in a strip over the map with *Rewrite* and *Still right*; nothing stops the person,
who can see the map. An agent's omission is silent, so `/v1/changes` refuses an undecided line.

**With a review queue, a set that rewords an area's sentence waits there whole.** `use_when` is the
line hop 0 prints and is a person's (2026-09-11). Where `ONTOLOGY_HARNESS` is configured, such a set
is dry-run to prove it applies, then queued as one proposal of type `change`; accepting it applies it
with the same base check, so what moved under it since is handed back, not overwritten. Every other
set applies directly — place writes (operator, 2026-10-08).

**`delete` is in the set, with the rule it always had**: an entity holding nodes is refused by name.
Retiring a version is not a delete: the new one goes in, a holder "previous versions" is created and
the old one moved under it, in one set — documents carry no state (invariant 9), so which is current
is said by the lines, and the old record is still there to be read.

## What a wide table gets

A placement walk that prints more than nine rows says so once — "if some of these belong together,
`here` can fold them" — and nothing more. Whether they belong together is the judgement the agent is
there to make; the mechanical rule that proposed widening lines by word overlap was measured at 9%
and removed on 2026-10-07.

## Checks

`check/change-check.py`: one commit or none, the dry run moving nothing and naming the id, the
cascade stopping at a kept line and climbing past a reworded one, a move impacting both ends and the
exposure acknowledged, a set in another order giving the same impact, two decisions on one aspect
refused, a stale base naming the file, a new area from hop 0, the holder rule on delete, a late
failure leaving no file, the ordinary create's nudge, the queue taking a set whole, and the agent's
`here` refused with the lines and placing with them decided. `check/place-check.py` walks around it;
`check/transact-check.py`'s static half holds that the new write path reaches `transact`.
