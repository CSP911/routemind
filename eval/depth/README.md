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

## Result, complete (2026-10-10) — the claude -p walker, both trees, all 73 questions

The API credit did not come back, so the whole comparison was walked again — both trees, every
question — by `bench/agent.py` with `ROUTER_PROVIDER=claude-cli` (an isolated `claude -p` session per
turn, `--model sonnet`; no tools, no MCP, no settings, the walker's own system prompt). One model and
one day for both trees, so the pairing holds. Walks in `eval/runs/depth-cli-sonnet/`.

| | hit | turns | opens | back | input tokens / walk | $ / walk (CLI-reported) |
|---|---|---|---|---|---|---|
| folded | **65/73 (89%)** | 5.8 | 2.9 | 0.4 | 23,800 | 0.099 |
| flat | **65/73 (89%)** | 4.8 | 1.8 | 0.3 | 59,500 | 0.240 |

By band: pilot 17/23 vs 16/23, direct 10/10 vs 10/10, indirect 20/20 vs 20/20, temporal 18/20 vs
19/20. Discordant: one each way (h5 folded only, t-overtime-12 flat only) — exact McNemar p = 1.00.
Nobody ran out of turns.

Against the predictions: (1) **no accuracy difference** — not small, none, at this scale and with
this model; a strong model scans a 244-row table as well as it walks three short ones. (2) flat
takes fewer opens, yes. (3) flat costs **2.4× the input** — every view of a wide table is paid again
on every turn after it. (4) returns to hop 0 equal.

**What it means for change sets.** Folding a wide table does not buy accuracy here; it buys cost,
by a factor of about two and a half, and it buys a table a person can read. That is enough to keep
`knowledge_place` suggesting a fold past nine rows, and not enough to make it mandatory. What this
run cannot say: whether a weaker model or a much larger map (thousands of rows in one table) loses
accuracy on the flat tree — the two places the argument for folding would have to be made on
accuracy rather than cost.

### And with Opus (claude -p opus), 2026-10-10

Same 73 questions, same trees, `ROUTER_MODEL=opus`. Walks in `eval/runs/depth-cli-opus/`.

| | hit | turns | opens | $ / walk |
|---|---|---|---|---|
| folded | **67/73 (92%)** | 5.5 | 2.9 | 0.185 |
| flat | **67/73 (92%)** | 4.6 | 1.9 | 0.421 |

Discordant: **0 and 0** — the same six questions missed on both trees (five in the hard pilot set, one
temporal). The strongest walker repeats Sonnet's pattern a step higher: the tree's shape changes
nothing about accuracy, and flat costs **2.3×**. Every miss is a question neither tree could answer
better, which says the remaining errors are in the questions or the documents, not in the folding.

### And with a weaker model (claude -p haiku), 2026-10-10

Same 73 questions, same trees, `ROUTER_MODEL=haiku`. Walks in `eval/runs/depth-cli-haiku/`.

| | hit | turns | opens | $ / walk |
|---|---|---|---|---|
| folded | 61/73 (84%) | 7.0 | 3.1 | 0.008 |
| flat | **66/73 (90%)** | 5.5 | 2.0 | 0.014 |

Discordant: **folded only 0, flat only 5** — exact McNemar p = 0.06. All five on the hard end: the
pilot set's e1, h4, s2, s5, and one temporal question. On the folded tree the weak model chose a holder
by its line and stopped short (e1: read the year-end overview, never opened the section with the
manual deductions — 1 open, 3 turns) or wandered between sections (s2, s5: 8 opens, 15–16 turns, and
read the legend documents of the qualifier families instead). With every row in one table it saw the
right document's own line and read it.

**This is the case against folding, measured.** Folding costs a strong model nothing in accuracy and
saves it 2.4× the tokens. It costs a weak model accuracy, because every holder is one more decision
made on one line — and a holder's line ("Year-end settlement in detail") says less about what is
under it than the documents' own lines do. Two consequences, both taken:

- `knowledge_place` keeps suggesting a fold past nine rows, never requiring one; and a holder's line
  has to name what is under it, not label a section — the tool description now says to.
- The study's claim is model-dependent and is written as such: with a strong router, fold for cost;
  with a weak one, prefer wider tables with good document lines. Neither is settled beyond n=73.
