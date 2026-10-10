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

## Result, 2026-10-10 — 12 questions × 2 models (c4 was added with the second-area note, below) (Claude Code's `sonnet` and `haiku`)

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

The hop-0 case stayed silent under the instruction: from inside a walk, leaving an area that held
nothing looks like ordinary searching. The server is what sees the walk switch areas, so since this run
it says so over the second area's table — *"This walk entered payroll first. If hop 0's sentence for
payroll is what sent you there and that area did not hold the answer, say so … If the question spans
both areas, carry on."* Re-run (`2026-10-10-philosophy-note/`), with a question that spans two areas on
purpose (c4) to see whether the note makes the agent blame a sentence that is fine:

| | before the note | with it |
|---|---|---|
| a wrong hop-0 sentence reported (M3) | 0/2 | **2/2** — "The payroll line sent me to the wrong place first, so whoever keeps the map may want to fix it." |
| a sentence blamed on a question that genuinely spans two areas (c4) | — | **0/2** — both answered from both areas and blamed nothing |

## The plausible wrong area ([questions-trap.yaml](questions-trap.yaml))

The case the first pass left out — a false hop-0 sentence that sends the agent into an area holding a
plausible *wrong* answer, the shape of the census's one miss. T1 moves "what a division head may approve
alone" from approval to procurement, whose purchase-threshold table has a division-head band (purchases
only). T2 moves "how much a business trip pays" from expense to payroll, whose tax-free table mentions
the trip allowance "within policy rates" without the amounts.

| `2026-10-10-philosophy-trap/` | sonnet | haiku |
|---|---|---|
| followed the false sentence into the wrong area | 2/2 | 2/2 |
| stopped there with the plausible answer | 0/2 | 0/2 |
| went on, and answered from the right document | 2/2 | 2/2 |
| reported the false sentence | 2/2 | 1/2 |

**It was the documents that saved it, not only the agent.** The plausible page in procurement says, in
its own text, *"The authority itself is set by the delegation rules in Documents & Approval; this table
is those rules applied to purchasing"*; payroll's overview points to Expenses for trip amounts. Both
agents followed those pointers. The example corpus is written that way on purpose — a page that is a
partial view says where the whole is. A corpus whose pages do not point onward is the real trap, and
this does not test it. What it does say: in a map that is wrong at hop 0, cross-references in the
documents are what stand between the agent and a confident wrong answer — which makes "say where the
authority is" a writing rule for whoever keeps the documents, not a nicety.

## What this does not show

- **Twelve questions, one corpus, one run each.** A rate from n=1 per cell is an anecdote; read the
  table as "did not fail", not as an accuracy.
- **The corpus is redundant on purpose** (eval/COLLAPSE.md), which is why two of the five falsehoods
  never met the agent. A map whose facts each live once would test claim 3 harder.
- **The wrong areas here held either nothing (M3) or plausible pages that point onward (T1, T2).** A
  wrong area whose plausible page does not say where the real answer is — the census miss — is not in
  this set.
- `haiku` and `sonnet` are Claude Code's aliases as of the run; the models actually used are recorded
  in each result file.
