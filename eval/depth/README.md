# Flat or folded — does the shape of the tree change what a walking agent finds?

Asked 2026-10-09, when change sets (docs/CHANGE.md) let `knowledge_place` fold a wide table — make a
holder, move siblings under it — instead of adding one more leaf beside the others. The operator's
observation that started it: tables built by placing were flat, with many rows at the area level,
where a person would have compressed them into a few lines they could remember. Folding costs hops.
Whether it buys anything was not known, and the change-set work went ahead on the argument alone.
This is the measurement.

## The two trees

The same 1,126 documents (the bench corpus and `bench/corpus-hard`), the same one-liners, the same
five frozen hop-0 sentences, the same agent (`bench/agent.py`, no working set), the same questions:

| | entities | deepest | area tables (rows) | widest table |
|---|---|---|---|---|
| **folded** — as built: documents under section holders | 1,212 | 5 | 15 · 23 · 20 · 15 · 15 | 67 |
| **flat** — every holder removed, what it held lifted to the nearest ancestor that is not one | 1,126 | 4 | 61 · 244 · 212 · 76 · 162 | 244 |

`flat` is what placing produced before change sets: leaves under the first node a walk stopped at.
A document that hangs under another document keeps its place in both — only holders go.

## Questions

73, fixed before any walk: the 23 of the pilot set (base corpus, all four difficulty bands, some
`needs: all`), and the 50 of `eval/gold/walk-sample50.yaml` (20 indirect and 10 direct questions over
the qualifier families, where retrieval collapses; 20 temporal ones over superseded versions).

A walk **hits** when it reads an answer document (`D_true`, or an accepted alternative in `D_alt`) —
every one of them when the question `needs: all`. Also recorded: turns, opens, returns to hop 0,
whether it ran out of turns (30), and tokens.

## Predictions, written before the first walk

1. **Hit rate: folded ≥ flat, but not by much on easy questions.** A 244-row table is long but every
   row is still there to read; a strong model can scan it. The difference should appear where rows
   are confusable — the qualifier families and the temporal versions — because in a flat table the
   rivals sit side by side with nothing grouping them, while folded puts them behind a holder whose
   line says what the group is.
2. **Turns and opens: flat fewer.** No holders to open; the agent goes area → document directly.
3. **Tokens: flat more**, despite fewer turns — every view of an area table is a few thousand tokens,
   and a walk that goes BACK re-reads it.
4. **Returns to hop 0: no difference.** Hop 0 is identical.

What would overturn the change-set argument: flat hitting as often as folded, at fewer turns and no
more tokens. Then folding is a cost with nothing bought, and `knowledge_place` should stop suggesting
it.

## Run

```sh
./eval/depth/run.py --pilot      # 6 questions × 2 trees — cost and sanity
./eval/depth/run.py              # 73 × 2, resumable; walks in eval/runs/depth/<tree>/
./eval/depth/run.py --report
```

Model: `ROUTER_MODEL` (this run: `claude-sonnet-5`), the Anthropic key in `ONTOLOGY_LLM_API_KEY`.

## Result so far (2026-10-09) — incomplete: the API credit ran out

`folded` was walked on all 73 questions; `flat` on 35 before the Anthropic account's credit ran out
(38 walks refused with "credit balance is too low" — recorded in `eval/runs/depth/run.log`, not
scored). On the 35 walked on both, with `claude-sonnet-5`:

| | hit | turns | opens | back | input tokens / walk | est. $ / walk |
|---|---|---|---|---|---|---|
| folded | 31/35 (89%) | 8.1 | 3.6 | 0.3 | 28,700 | 0.041 |
| flat | 30/35 (86%) | 7.2 | 2.6 | 0.3 | 102,000 | 0.110 |

Discordant: folded only 2 (m7, s5), flat only 1 (s1) — exact McNemar p = 1.00. On the indirect
qualifier questions both hit 7/7, and flat took more turns (12.1 vs 10.1) and went back to hop 0
more (1.0 vs 0.1).

Against the predictions: (1) no hit-rate difference visible at n=35 — not enough to say there is
none; (2) flat fewer opens, yes; (3) flat ~3.5× the input tokens, yes — and more than predicted;
(4) returns equal overall, but not on the indirect questions. The cost result is already clear; the
accuracy result needs the remaining 38 flat walks.
