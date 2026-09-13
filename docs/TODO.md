# TODO

Open work that has been decided on but not done. Newest first. Each item says who it waits on.

## Snapshot isolation costs hop 0 twenty percent — *watch, then measure again*

Every read now takes the writers' lock shared, loads the tree, and lets go (`Store.snapshot`), which
is what stopped an answer being assembled from two different instants. Measured 2026-09-14 on
`examples/back-office`, 79 entities, 300 requests each:

| | before | after |
|---|---|---|
| `/v1/regions` — hop 0, the hot path | 8.37 ms | **10.01 ms** |
| `/v1/regions/<area>` | 19.06 ms | 13.15 ms — *faster*, the nodes load once |
| `/v1/core` | 0.19 ms | 1.64 ms |

The 20% on hop 0 buys correctness and is worth it as it stands. What is left in it: the snapshot is
rebuilt on every request, and the tree only changes when a write commits. A writer could leave a
generation stamp — one small file under `.git/`, written inside the exclusive lock — and a reader
could `stat` it and reuse the snapshot it already has when nothing has moved. That turns the common
case into one stat.

**Not done, and not obviously worth doing yet.** Two reasons to wait. The absolute numbers are small
and nobody has reported it. And a stamp only a writer bumps would not notice a **hand edit** to
`data/repo`, which is a supported thing to do and today shows up on the next read — so the stamp
would have to be something a hand edit also moves, which is most of what makes the current cost. Do
not start this without a measurement from a real install saying hop 0 is too slow.

## Overlay: the ten-question comparison — *operator: when, and which questions*

docs/OVERLAY.md, "How we will know it helped". The same ten questions or fewer, run twice — as agents
work without overlays, and through them — counting calls to an answer and how many were reached.

- Needs data with **several areas and questions that cross them**. This is no longer the blocker it
  was: `examples/back-office` is five areas and 79 entities, built four levels deep with handoffs
  that cross areas (a trip settlement is attendance *and* expense; an approval threshold is approval
  *and* procurement). What is still needed is the questions themselves — pick or write them first, a
  comparison on one-area questions measures only the overhead.
- Run it against a **copy** of the data, the way the 2026-09-11 trial was run, never the live install.
- Read `used` in the closed records: rows marked `reached` say the overlay was drawn a level too coarse.

## Overlay: the curator reads closed records — *Knowledge*

The record is shaped for it (`why`, `used` with `member` / `removed` / `reached`, `outcome`). Nothing
reads it yet. Closed records are kept 30 days (`ONTOLOGY_OVERLAY_KEEP_DAYS`); the curator will want
longer once it does.

## Checks that write into the live install — *Web*

`check/llm-paths.sh` writes into the install at :8080, which is somebody's. It should run against a
throwaway ontology the way `write-paths.sh`, `overlay-check.py` and `scenarios.py` do.

Seen 2026-09-12, and worse than "untidy". Its three cleanup calls are `curl -s -o /dev/null -X DELETE`
with no status check, so when one fails nothing notices. One did: the run printed **`both LLM paths
ok`** while leaving `approval-fmprobe` and its document deleted from the working tree and never
committed. That is the dirty-tree state, so from then on *every* write to that install was refused
with "someone edited the repository by hand" — and nobody had. Recovering it took `git -C data/repo
checkout -- .` and a delete through the API. A second run cleaned up correctly, so the underlying
delete failure is intermittent and not yet pinned down; what is not intermittent is that the check
cannot tell.

Two things, and the first is worth doing even if the second waits: **assert the cleanup** (and that
the tree is clean when the script ends, naming the recovery command if it is not), then **move it off
the live install**. It needs a real `ONTOLOGY_LLM_*` config, so the throwaway has to inherit the
environment rather than start bare.

## Draft latency — *watch*

An entity's one-liner draft took 13 s through the live proxy on gpt-5.2. Fine behind a button; if it
lands badly, the Knowledge session can trim what the prompt is given (the siblings' lines are the
expensive part and the part that makes it exact).
