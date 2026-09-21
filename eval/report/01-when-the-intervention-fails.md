# Chapter 1 — The moment human intervention fails

*The research question this study was registered against is: **how useful is human intervention in
RAG, and where does it stop paying for itself?** The intervention is a human-authored routing table
— a partition of the corpus into areas, one sentence describing each, and a hierarchy beneath. An
agent reads the table and decides where to look.*

*Chapter 2 measures what that costs. This chapter asks the prior question: **when does it stop
working at all?** There are two ways it can, and they are not the same failure.*

| | | status |
|---|---|---|
| **1** | the table is **wrong**, or has gone stale without anyone meaning it to | measured |
| **2** | the table is entirely **correct**, and at some point it still fails | **not measured** |

Both are failures of the intervention. Only the first has evidence here, and saying which is which
is most of this chapter's job.

---

## 1.1 Why this failure mode is the interesting one

Retrieval has no map. That is its weakness and, exactly, its immunity. A fusion retriever scores
0.028 on questions written in a person's words against documents indexed by codes — it does not
degrade on those, it fails outright — but it cannot be *misled*, because there is nothing for it to
believe.

A routing agent believes the table. That is where the gain comes from: 0.028 against 1.000 on the
same 320 questions, because the agent reads a sentence and goes to the right place instead of
ranking a haystack. It is also the whole exposure. **An agent that trusts the map inherits the map's
errors, and inherits them silently.**

So the two arms fail in different currencies:

| | how it fails | what reaches the user |
|---|---|---|
| retrieval | the answer is not in the top ten | an answer assembled from whatever was |
| routing | the map sends it somewhere plausible and wrong | **a confident answer from the wrong place, with a source attached** |

A wrong routing table does not degrade gracefully. It returns a clean-looking success.

## 1.2 Indicator 1 — a wrong table, and staleness nobody intended

### 1.2.1 It happened, once in 700, and it was one sentence

Two documents in this corpus are *forwarding notes*: they sit in the area a subject moved out of and
tell a walk where it went. Both said, of the page left behind:

> They remain correct for anything dated before **2026-01-01** and for nothing after it.

False. That page is the **oldest** of three versions and stopped being correct at **2024-07-01** —
eighteen months before the move the note describes. The note is not wrong about the move. It is
silent about a revision that happened before it, and silence reads as *nothing else to know*.

On the 700-question census, one walk read the note, did exactly what it said, and answered a claim
dated 2025 from the 2023 rule. It was the only miss in 700.

### 1.2.2 The part that proves it was the map and not the reader

The study runs two routing arms. `routing` walks and reads. `routing+overlay` does the same while
keeping a working set — an explicit record of which rows it has decided are in play and why.

**Both failed the same question, identically:**

    routing          hard-moved-overtime → payslip-overtime
    routing+overlay  hard-moved-overtime → payslip-overtime

Two agents sharing no context, one of them carrying memory of its own decisions, same two documents,
same wrong era. A working set cannot help here, because **nothing was forgotten**. The note was
read, understood, and obeyed. The reader did what a careful reader should do with a true-looking
sentence.

### 1.2.3 Fixing the sentence fixed the walk

The note now carries the full version table and says outright that a question dated after
2024-07-01 is answered elsewhere — *including dates before the move*, which is the case it used to
get wrong. Ten `changed` questions re-walked on the corrected corpus:

| | before | after |
|---|---|---|
| `changed`, routing | 0.900 (9/10) | **1.000 (10/10)** |
| the failing walk | `hard-moved-overtime` → `payslip-overtime` | `hard-moved-overtime` → `…-legend-revision` → `…-v2` |

**Same note, different destination.** The agent did not become more careful. It was given a sentence
that was true.

*(These are two corpora — fingerprints `a84ac6cf463a1a6d` and `2e0e821a7d9f667b` — and the numbers
do not merge. Ten questions on one lever show the fix works on the case that broke; the other six
levers were not re-run.)*

### 1.2.4 Staleness nobody intended is the general form

The forwarding note is one instance of a shape this corpus is built around. Subjects here have been
rewritten two and three times, and **the older versions do not announce it.** That is not an
oversight in the corpus; it is a property of how back offices actually write, stated in the
generator: *none of them were withdrawn, and the oldest says nothing at all about having been
replaced.*

Which means the burden of currency falls entirely on the map. When the map carries it, routing gets
every one of these right. When one sentence of the map is silent, the agent answers from a rule that
has been dead for eighteen months and cites it.

For retrieval the same corpus property shows up as a flat loss it cannot route around:

| lever | `rag` | `rag+rerank` | `routing` |
|---|---|---|---|
| `stale-old` — two revisions back | 0.133 | 0.200 | 1.000 |
| `stale-mid` — one revision back | 0.600 | 0.667 | 1.000 |
| `changed` — the current rule | 1.000 | 1.000 | 1.000 |

Note the shape: retrieval is **perfect** on the current rule and collapses as the question reaches
backwards, because every newer version of the same subject outranks the one being asked for and they
all look alike. Routing is flat across all three — until the map is wrong about one of them.

### 1.2.5 A check, so it cannot happen silently again

The defect was found by a walk failing, which is the expensive way round and also the ambiguous one:
a walk that goes wrong cannot tell you whether the map or the model was at fault. So it is now a
rule decided from the corpus alone, before any arm runs:

> **`mapcheck` R6** — a forwarding note must name every date its subject's own revision legend
> names, not only the date it moved.

Both notes failed R6. The corrected corpus passes with nothing carried. And carrying a known failure
is deliberately awkward: `--carry R6` has to be typed on every run, prints `CARRIED` where it cannot
be missed, and changes the closing line to say the table describes the corpus *except where listed*.

This matters more than the one bug it caught. **The intervention is a human artefact, and human
artefacts drift.** This study lost three runs to maps that had drifted without anyone noticing. R1–R6
exist because "we maintain it carefully" is not a measurement.

## 1.3 Indicator 2 — a correct table that stops working anyway

The second failure is the one this chapter cannot demonstrate, and the honest thing is to say so
plainly rather than let the first one stand in for both.

**At this corpus, a correct map does not fail.** 1,126 documents, 5 areas, 700 questions: 699 hits,
and the single miss was a wrong map, not a correct one. Nothing here shows a limit.

### 1.3.1 What that leaves unanswered

The question is not whether the map is *accurate* but whether it stays *usable* as the thing it
describes grows. A one-sentence description of an area is a fixed-size summary of a set that is not
fixed-size. Somewhere it stops being enough:

- **How many documents** before one sentence per area cannot separate them?
- **How many areas** before choosing between them at hop 0 is itself the hard problem?
- **How deep** before the walk costs more than the ranking it replaced?
- **How many versions** of one subject before the revision legend is itself a haystack?

None of these were varied. **The study has exactly one corpus size, and a scaling limit cannot be
seen from one point.**

### 1.3.2 The asymmetry with retrieval, which is the uncomfortable part

Retrieval's collapse *is* characterised, because scale was varied on that side. Fitting five corpus
sizes gives a two-parameter model:

    recall@20  ≈  p × min(1, 20/N)      p ≈ 0.25

| N (rivals) | 16 | 32 | 64 | 128 | 256 |
|---|---|---|---|---|---|
| observed | 0.25 | 0.15 | 0.13 | 0.06 | 0.02 |
| predicted | 0.250 | 0.156 | 0.078 | 0.039 | 0.020 |

`p` is the chance the question reaches its answer's family at all; `min(1, 20/N)` is the share of
that family a twenty-candidate list can hold. **Retrieval's failure is predictable before running
anything.** Routing's is not, because nobody has run the equivalent sweep.

That is a gap in the study, not a property of routing.

### 1.3.3 The only leading indicator currently visible

If a correct map is going to fail with scale, the cost should move before the accuracy does — the
walk should wander before it gets lost. There is a faint version of that in the census:

| | median | p75 | p90 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| calls per question | 7 | 8 | 9 | 10 | 15 | **28** |

Eight walks in 700 (1.1%) took fifteen calls or more. **All eight hit.** Seven of the eight are
`indirect`; five of the longest are one family.

Read carefully, this says very little. The median is flat at 6–7 across all five families, including
the two whose subject moved areas — so there is no family-level strain, only a tail. A tail of
successful long walks is what "working, with effort" looks like, and it is *consistent with* being
some distance before a limit. It is not evidence of where the limit is.

### 1.3.4 What would actually measure it

The sweep retrieval already had, run on the routing side: **the same questions against corpora of
increasing size, with the map kept correct at every size** — so that the only thing varying is how
much one sentence per area is being asked to carry. The prediction worth registering in advance is
that calls per question rises first and accuracy holds, until the description can no longer separate
what sits beneath it.

Until that runs, the honest statement is the narrow one:

> A correct routing table did not fail at 1,126 documents and 5 areas. Where it would is unmeasured,
> and this study cannot say.

## 1.4 What Chapter 1 establishes

**Human intervention fails in two ways, and this study has evidence for one.**

The measured failure is the map being wrong — and it is worse than it sounds, because it does not
announce itself. One false sentence produced a confident, sourced, wrong answer; both routing arms
committed it identically; and it took a 700-question census to see it at all, because a 50-question
sample had drawn the agent that happened to go the other way. The correction is not "be careful with
the table" but a check that decides it from the corpus before any arm runs.

The unmeasured failure is scale. Retrieval's limit is characterised by a two-parameter law fitted
across five corpus sizes. Routing's is characterised by nothing, because the study varied scale on
one side and not the other.

Chapter 2 measures what the intervention costs when it is working. It should be read knowing that
the cost column and the accuracy column are both taken at a single point on an axis that has not
been explored.

---

### Limits of this chapter

- **One corpus size.** The central gap, stated in §1.3 rather than buried here.
- **One instance of indicator 1.** One defect, found once, in two documents of the same kind. That
  it generalises to *forwarding notes* is a claim R6 makes; that it generalises to maps in general
  is an argument, not a measurement.
- **The re-walk is ten questions on one lever**, on a corpus that differs from the census by two
  documents. It shows the fix works on the case that broke and nothing more.
- **One model.** All walks are `claude-sonnet-5`, one run each. Whether a stronger reader distrusts
  a confident-but-false forwarding note was not tested, and was deliberately dropped: R6 decides
  whether the note is wrong without running a model at all.
