# Chapter 2 — What it costs

*Chapter 1 established where retrieval breaks: on 700 questions over one frozen corpus, fusion
retrieval scores 0.516 overall and 0.028 on questions written in a person's words against documents
indexed by codes. A reranker takes that to 0.541 and 0.069. Walking the routing table scores 0.999.
This chapter is the other column, and it is the reason that comparison is not yet an argument.*

---

## 2.1 The number that was missing

Every accuracy figure in Chapter 1 favours routing, several of them by more than an order of
magnitude. None of them said what routing costs. A result that only reports the side it wins on is
not a result; it is an advertisement, and the honest version of the claim cannot be written until
the other column exists.

So this chapter measures it, on the same corpus, the same questions, the same fingerprint.

    fingerprint a84ac6cf463a1a6d · claude-sonnet-5 walks · gpt-5 reranker
    embeddings text-embedding-3-large, cached on disk
    call counts from all 700 walks · dollars and latency from 5 walks, measured directly

The asymmetry in that last line is deliberate and worth stating up front. Call counts are a census:
every one of the 700 walks recorded what it ran. Dollars and latency are five walks, one per lever,
measured with the runner's own usage reporting. Five is a small number and this chapter does not
pretend otherwise.

## 2.2 What each arm actually does, per question

| | `rag` | `rag+rerank` | `routing` |
|---|---|---|---|
| network round trips | **1** | **1.56** | **6.7** |
| what they are | one query embedding | + 0.56 reranking calls | 3.4 table opens, 3.3 document reads |
| new content processed | ~30 tokens | ~2,500 tokens | **14,000–26,000 tokens** |
| wall clock | under a second | a few seconds | **23–111 seconds** |
| measured cost | negligible | model-dependent | **$0.12–$0.28** |

Two of those figures need explaining.

**Why the reranker averages 0.56 calls and not 1.0.** A question whose answer is not among the
fused candidates is never sent to the reranker — the miss is already decided, and spending a call to
reorder twenty wrong documents buys nothing. 390 of 700 questions were reranked; the other 310 were
already lost. This is a real efficiency of the arm, and it also means the reranker's cost is
concentrated on the questions where it might help.

**Why routing is 6.7 calls and not 2.** A walk opens the top-level table, picks an area, opens that
area's table, often opens a subject's table below it, and then reads documents. Three and a half
table opens and three and a third reads is the median shape of that. The distribution has a tail:
the p95 is 10 calls and one walk in 700 took 28.

## 2.3 The cost scales with the question

| lever | new content | output | cost | time | turns |
|---|---|---|---|---|---|
| `direct` | 16,842 | 1,330 | $0.122 | 23 s | 6 |
| `changed` | 13,799 | 1,927 | $0.128 | 24 s | 8 |
| `indirect` | 18,190 | 2,363 | $0.161 | 43 s | 9 |
| `indirect` | 18,591 | 2,286 | $0.170 | 47 s | 10 |
| `both` | 25,633 | 7,694 | $0.281 | 111 s | 14 |

The median is $0.161. The spread is more informative than the median: **a question needing two
documents costs roughly twice one needing a single row, and takes five times as long.** Cost tracks
the number of documents the answer rests on, which is the thing the question asks for — so this is
not overhead that better engineering removes. It is the work.

## 2.4 One number that will be quoted wrongly

Raw usage reports **200,000 to 500,000 input tokens per walk.** That figure is real, it is what the
API returns, and repeating it without qualification would overstate the cost by an order of
magnitude.

The reason is that each tool call resends the conversation so far, and almost all of it is served
from cache:

| | fresh input | cache write | cache read | output |
|---|---|---|---|---|
| `direct` | 12 | 16,842 | 198,549 | 1,330 |
| `indirect` | 20 | 18,591 | 358,535 | 2,286 |
| `both` | 28 | 25,633 | 498,935 | 7,694 |

Cache reads bill at a fraction of fresh input. The genuinely new content — the prompt plus each tool
result as it arrives — is the cache-write column: 14k to 26k tokens.

So there are three numbers available and two of them mislead:

- **500,000 tokens** — overstates by an order of magnitude. Counts the same text many times.
- **~20 tokens** — understates by three orders. Counts only what missed cache entirely.
- **$0.12–$0.28** — measured, and the one this chapter uses.

Anyone reproducing this will see the 500k figure first. It is flagged here so the correction arrives
before the objection does.

## 2.5 What is actually being traded

**Latency is the one a user feels.** Sub-second against 23 to 111 seconds is not a tuning
difference; it is a different kind of interaction. Retrieval answers inside a request. A walk is a
job you wait for, and at the hardest lever it is nearly two minutes. No amount of parallelism fixes
this for a single user asking a single question.

**Cost is one to two orders of magnitude.** A reranking call moves about 2,500 tokens once. A walk
moves 14k–26k of new content across six to fourteen turns. The exact multiple depends on which
models are priced, which is why this chapter gives tokens and calls beside the dollars rather than a
single ratio.

**The table is written and kept by hand, and appears in no column above.** The map in this corpus is
five area descriptions and a set of revision notices — small, but authored and maintained by a
person. This study lost three runs to a map that had drifted without anyone noticing, which is why
`mapcheck` exists and runs before any arm does. That labour is a real cost of the method and this
chapter does not price it, because nothing here measured it.

**A wrong table is worse than no table.** One sentence in one forwarding note produced the only miss
in 700 walks — and it produced a *confident answer from the wrong era with a source attached*. Both
routing arms failed it identically, including the one carrying a working set, which is what
establishes the fault was in the map rather than in the reader. Retrieval cannot fail this way,
because it reads no map. Chapter 3 takes this up in full.

## 2.6 What this chapter establishes

Putting the two columns together, for this corpus:

> Retrieval collapses on a specific, nameable class of question — one written in a person's words
> against documents indexed by codes, or one asking about a version that has since been replaced.
> On that class it does not degrade gracefully; it fails outright, at 0.028. Walking the table costs
> 20–100× more per question and fixes exactly that class.

And the part that follows from the cost column, which Chapter 1 alone could not support:

> 320 of these 700 questions are ones retrieval already answers first time, at 0.991. Nothing in
> this study argues for walking those.

Which arm to use is therefore not a question this study answers. It is a question about the mix of
questions a system actually receives, and **nothing here measures that mix for anyone but this
corpus.** A deployment whose traffic looks like the `direct` lever should not pay this. One whose
traffic looks like `indirect` cannot afford not to.

---

### Limits of this chapter

- **n=5 for dollars and latency.** One walk per lever, one run each. The shape is clear; the
  precision is not there and no interval is quoted.
- **One model per arm.** All walks are `claude-sonnet-5`; the reranker is `gpt-5`, run once. Chapter
  1's reranker figures are a single draw and carry no variance estimate.
- **Cost of maintaining the table is unmeasured.** Stated as a cost, not quantified as one.
- **Corpus embedding is excluded.** It is a one-time 1,126-document cost, cached on disk, and it is
  paid by both retrieval arms equally.
