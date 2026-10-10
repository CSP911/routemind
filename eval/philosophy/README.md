# Does the agent behave the way the README says? — absence, and a map that lies

Three sentences in the README are claims about behaviour, not about retrieval:

1. **Every walk starts at hop 0, and every step records why.**
2. **Only someone who has read hop 0 may conclude that something is not here.**
3. **An agent that trusts the map inherits the map's errors, and nothing flags them.**

This puts each to Claude Code through the real MCP door — `claude -p` with nothing but the knowledge
server: no built-in tools, no settings, its instructions exactly what any client gets. The whole stream
is kept, so what the agent *did* is read from its tool calls, not from its answer.

```sh
./eval/philosophy/run.py --api http://localhost:<port>/api/knowledge --repo <install>/data/repo \
    --compose-dir <install> --models sonnet,haiku --out eval/runs/<date>-philosophy
./eval/philosophy/score.py eval/runs/<date>-philosophy
```

Use an install of `examples/back-office` of its own: the wrong-map half commits deliberate falsehoods
into its data repository and reverts them when it is done. Questions and falsehoods are in
[questions.yaml](questions.yaml).

## Result, 2026-10-10 — 12 questions × 2 models (Claude Code's `sonnet` and `haiku`)

| | sonnet | haiku |
|---|---|---|
| control (3) — answer in one document | 3/3 | 3/3 |
| absent (4) — no document says it | 4/4 said so, none invented a rule | 4/4 |
| wrong line (M1, M2, M4) — answered from the document, not the false line | 3/3 | 3/3 |
| wrong hop-0 sentence (M3) — recovered to the right area | 1/1 | 1/1 |
| hidden table (M5) — row renamed to something else, still found | 1/1 | 1/1 |
| first call was hop 0 · every later call had a `why` | 12/12 · 12/12 | 12/12 · 12/12 |
| cost (12 walks; CLI-reported) | $0.59 | $0.04 |

Every answer was read, not only matched: `run 2026-10-10-philosophy/` holds each answer and every
call. The regex in `score.py` misjudged three, all in the agent's favour on reading — "I couldn't find"
was not in the first absence pattern (widened), and in w4 the agent quoting the false line in order to
flag it tripped the "refuse" pattern (dropped).

**What the absences looked like.** Each absent question was answered "not in RouteMind" after reading
three to seven documents in the area that could have held it — the instruction "before saying a detail
is not covered, read the documents in the table you are in" is being followed. a4 (a meal with a public
official) is the useful one: the documents ban *gifts* to officials at any amount and say nothing about
meals. Both models said exactly that, gave the general meal cap as general, and did not extend the ban
or invent an exception.

**What the false lines showed — and did not.**
- **M1 and M2 were never exercised.** Neither model opened the documents whose lines were made false:
  in this corpus every fact is in two documents, and both reached the answer through the other one.
  That is robustness of a redundant corpus, not evidence about trusting lines.
- **M4 and M5 were exercised** (added after the first pass for that reason). M4 states the wrong first
  step in both lines over the lost-card procedure; M5 renames the only month-by-month table as
  something about parental leave. Both models opened the documents anyway and answered from them.
- **M3 sent both models to the wrong area**, exactly as the census's one miss did. Here, unlike the
  census, the wrong area held nothing that looked like an answer, so both went on to the right one.
  The census miss is the other case — the wrong place *had* a plausible document — and this does not
  test it.

**Claim 3, "nothing flags them", held — until the instructions asked.** In the first pass the answers
were right and the map stayed wrong: one of four walks that passed a false line said so. One sentence
was added to the server's instructions (`mcp/knowledge_mcp.py`): *if a line or an area's sentence
disagrees with the document or sent you to the wrong place, answer from the document and say which line
is wrong.* Re-run (`2026-10-10-philosophy-flag/`):

| walks that passed a false line, and said so | before | after |
|---|---|---|
| a wrong document line (M4, M5) | 1/4 | **4/4** — e.g. "Map issue for whoever maintains RouteMind: the proration table is listed under 'Returning from parental leave'…" |
| a wrong hop-0 sentence (M3) | 0/2 | **0/2** |

The hop-0 case is the one that matters most, and it is still silent: an agent that walked into the
wrong area, found nothing and moved on does not report the sentence that sent it there. Not fixed.

## What this does not show

- **Twelve questions, one corpus, one run each.** A rate from n=1 per cell is an anecdote; read the
  table as "did not fail", not as an accuracy.
- **The corpus is redundant on purpose** (eval/COLLAPSE.md), which is why two of the five falsehoods
  never met the agent. A map whose facts each live once would test claim 3 harder.
- **The wrong area here was empty of answers.** The dangerous misroute — a wrong area holding a
  plausible wrong document — is not in this set.
- `haiku` and `sonnet` are Claude Code's aliases as of the run; the models actually used are recorded
  in each result file.
