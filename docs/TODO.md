# TODO

Open work that has been decided on but not done. Newest first. Each item says who it waits on.

## Overlay: the ten-question comparison — *operator: when, and which questions*

docs/OVERLAY.md, "How we will know it helped". The same ten questions or fewer, run twice — as agents
work without overlays, and through them — counting calls to an answer and how many were reached.

- Needs data with **several areas and questions that cross them**. Today's install has two areas
  (`library`, `order-delivery`) and nearly every question ends inside one, which is exactly the case
  an overlay cannot improve. Pick or write the questions first; a comparison on one-area questions
  measures only the overhead.
- Run it against a **copy** of the data, the way the 2026-09-11 trial was run, never the live install.
- Read `used` in the closed records: rows marked `reached` say the overlay was drawn a level too coarse.

## Overlay: the curator reads closed records — *Knowledge*

The record is shaped for it (`why`, `used` with `member` / `removed` / `reached`, `outcome`). Nothing
reads it yet. Closed records are kept 30 days (`ONTOLOGY_OVERLAY_KEEP_DAYS`); the curator will want
longer once it does.

## The shipped examples — *operator*

`seed/` is empty. The operator wants clinic / library as English examples in git, which a real user
then deletes. Undecided: ship them in `seed/` (every install starts with them) or as an optional
`examples/` a person loads. Knowledge owns `seed/`.

## Checks that write into the live install — *Web*

`check/llm-paths.sh` writes into the install at :8080, which is somebody's. It should run against a
throwaway ontology the way `write-paths.sh` and `overlay-check.py` do.

## Draft latency — *watch*

An entity's one-liner draft took 13 s through the live proxy on gpt-5.2. Fine behind a button; if it
lands badly, the Knowledge session can trim what the prompt is given (the siblings' lines are the
expensive part and the part that makes it exact).
