# Where plain RAG collapses, and the dataset that proves it

**Threshold: `B1 hit@10 < 0.50`.** Measured on the dataset below: **0.03**.

This document defines the threshold, explains the two numbers it is stated in, describes the corpus
built to cross it, and says plainly what the result does and does not license.

---

## 1. The metrics, from the beginning

A retrieval-augmented system cannot hand a language model 1,114 documents. It retrieves a few and
hands over those.

    question -> [retriever] -> the k documents that look relevant -> [LLM] -> answer

`k` is how many. This study uses **k = 10**: the model sees ten documents out of 1,114. Everything
follows from one consequence of that.

> **If the answering document is not among those ten, no model can answer.** It cannot report what it
> was never shown. Inventing something is the only remaining option, which is the failure mode people
> call hallucination and is better described as *the retriever did not find it*.

So the first question in evaluating RAG is not whether the answer was good. It is whether the answer
was *in the box*.

### hit@10

For one question: 1 if a `D_true` document is among the top ten, 0 if not. Averaged over the
question set, a rate between 0 and 1.

    hit@10 = 1.00    the answer was in the box every time
    hit@10 = 0.50    half the time it was not
    hit@10 = 0.03    three questions in a hundred

### recall@20, and why there are two numbers

The retriever is two stages.

    stage 1   BM25 top 50 + dense top 50, fused by reciprocal rank -> 20 candidates
    stage 2   an LLM reranker scores those 20 and reorders them     -> the final 10

    recall@20   was the answer among the 20 candidates stage 1 produced
    hit@10      was it among the 10 that came out of stage 2

*(With exactly one correct document per question — this study's case — recall@k and hit@k are the
same quantity. They part company when a question has several correct documents, where recall asks
what fraction were retrieved. Everything below has one.)*

### The ceiling, which is the load-bearing idea

**The reranker reorders candidates. It cannot fetch a document that is not one.**

    the answer is not in the 20   ->   no reranking puts it in the final 10

So **`recall@20` is a mathematical upper bound on `hit@10`**. This matters for a reason beyond
tidiness: `recall@20` costs one cached embedding and no LLM call, while `hit@10` costs a reranking
call per question. The cheap number bounds the expensive one.

It also turned out to *be* the expensive one, to two decimal places, on the 700-document corpus:

| | fusion recall@20 | B1 hit@10 |
|---|---|---|
| A=2 | 0.93 | 0.93 |
| A=3 | 0.80 | 0.80 |

The reranker recovers everything that reaches the candidate list and nothing that does not.

### Why the threshold is 0.50

    hit@10 < 0.50   the retriever misses more often than it finds

Below a coin flip a retriever is not a tool that sometimes struggles; it is a tool that does not
work. `eval/DIFFICULTY.md` uses this as the definition of the **severe** band, so that "severe" names
a measured place rather than a large number on an invented scale.

---

## 2. What had to be built, and why nothing else worked

Three rounds failed to cross the threshold, and each failure narrowed the target.

**Paraphrase alone does not work.** Rewriting a question until it shares 8% of its vocabulary with
the answer destroys BM25 — recall@20 0.13, median rank outside the top 50 — and the dense half
shrugs: recall@20 0.95, median rank 3. `text-embedding-3-large` reads *"taking time off in chunks to
look after my father through the same ongoing health problem"* and returns the family-care-leave
document third. **The lexical-distance factor was measuring BM25's problem, not retrieval's.**

**The original corpus cannot be broken by arrangement.** Its closest pair of documents sits at cosine
0.911 and the typical document's nearest neighbour around 0.78. Nothing in it is *nearly the same
thing* as anything else, so the dense side always has a clean winner to return.

**Sixteen near-identical siblings do not work either**, in the form they were first built — English
phrases in the rows, no legends, two axes. Measured **hit@10 1.00** on both levers.

### The mechanism, measured rather than asserted

The first explanation for that was rival count alone: if N documents are equally plausible and the
retriever returns k, the answer arrives with probability about k/N, so N=16 at k=20 cannot fail. A
dose-response sweep says that is half of it.

| N per family | corpus | direct hit@10 | indirect hit@10 | indirect recall@20 | k/N at k=10 |
|---|---|---|---|---|---|
| 16 | 874 | 1.00 | 0.07 | 0.25 | 0.62 |
| 32 | 954 | 1.00 | 0.01 | 0.15 | 0.31 |
| 64 | 1,114 | 1.00 | 0.03 | 0.13 | 0.16 |
| 128 | 1,434 | 0.97 | 0.02 | 0.06 | 0.08 |
| 256 | 2,074 | 0.96 | 0.00 | 0.02 | 0.04 |

**At N=16 the same sixteen rows now score 0.07 instead of 1.00.** Nothing about the count changed;
the rows were re-indexed by codes and the mapping moved into legends. So the dominant cause is not
how many rivals the answer has — it is that **the question's words point at a different document than
the answer**. The rows are not outranked by their siblings; they are outranked by everything in the
corpus that shares vocabulary with the query, and the family never reaches the candidate list at all.
That is why the measured recall@20 sits far below k/N at every N.

Rival count is the second factor, and it multiplies:

    recall@20  ≈  p × min(1, 20/N)        with p ≈ 0.25

| N | observed | predicted |
|---|---|---|
| 16 | 0.25 | 0.250 |
| 32 | 0.15 | 0.156 |
| 64 | 0.13 | 0.078 |
| 128 | 0.06 | 0.039 |
| 256 | 0.02 | 0.020 |

`p` is the chance the question reaches its answer's family at all — indirection takes it from 1.00 to
about 0.25 — and `min(1, 20/N)` is the share of that family the candidate list can hold. Two
parameters, five points, one of them (N=64) off by a factor of 1.7 and the rest close.

> **Difficulty, for a retriever, is where the question's vocabulary points, and then how many rivals
> stand at the end of it.** Both are properties of the corpus, not of the question's phrasing, and
> both are calculable before anything runs.
>
> It is also why the crowding factor came back flat. **E was the right idea at the wrong scale and on
> the wrong quantity** — counting neighbours in a corpus whose largest cluster was 27, when what
> matters first is whether the query points at the cluster at all.

**Not one embedding model's quirk.** `text-embedding-3-small` over the same questions: direct 1.00 at
N=16 and 0.99 at N=64, indirect **0.01** and **0.03**. The collapse is where it is under both models.

**Operating point: N=64 (`--grid 4x4x4`).** At 128 and 256 even the direct control slips to 0.97 and
0.96, so the corpus is no longer clean at that size; at 64 the control is 1.00 and indirect is 0.03.

---

## 3. The dataset

`bench/crowd.py write --grid 4x4x4` — templates, deterministic, no model involved.

    5 families x 64 rows   320 documents
    5 families x 3 legends  15 documents
    5 sections               5
                           ---
                           340, on top of the frozen 700

| family | area | axes |
|---|---|---|
| perdiem | expense | grade × country band × length of stay |
| overtime | payroll | day type × hour band × work location |
| accrual | attendance | employment type × service band × site class |
| threshold | approval | spend category × amount band × commitment term |
| diligence | procurement | supplier origin × contract value × supply category |

### Rows are indexed by codes

Each row states its three qualifiers as **codes** — `grade G3`, `band C`, `stay S2` — and states
nothing else that distinguishes it from its 63 siblings. Within a family the rows share 0.83–0.89 of
their vocabulary.

This is load-bearing rather than cosmetic. The first version wrote the third axis in English, and
102 of 320 indirect questions then shared a *discriminating* word with their own row — a word that
row had and its siblings did not. BM25 and the reranker could pick the row without ever consulting a
legend, and the lookup the design exists to force was optional. With codes the leak is **0 of 320**.

It is also what real systems do. Tariff codes, pay bands, risk tiers, plan codes: an index keyed to
symbols, with the mapping written down somewhere else.

### Legends are where the mapping lives

Three documents per family map a person's vocabulary onto the codes:

| What you have | What the rows call it |
|---|---|
| Tokyo | band A |
| Singapore | band B |
| Jakarta | band C |

**The legends are ordinary retrievable documents.** They sit in the corpus and in the tree, and every
arm can retrieve them. There is no information the routing arm has and the baseline does not — which
is the single most important property of this dataset and the first thing a sceptic should check.

### Two questions per row, same answer

    direct     "For grade G3, band C, stay S2, what can I put on a hotel each night...?"
    indirect   "I'm a team manager — Jakarta, eight nights — what can I put on a hotel each night...?"

The indirect question contains **no word that appears in its answer row**. `manager`, `Jakarta` and
`eight nights` appear only in the legends. Answering it needs a **lookup and then a fetch**: read the
legend, learn the code, open the row.

`direct` is the control, and the result is unusable without it.

---

## 4. The result

Hybrid fusion over 1,114 documents, 640 questions, at the N=64 operating point:

| lever | n | hit@10 | recall@20 | median rank |
|---|---|---|---|---|
| direct | 320 | **1.00** | 1.00 | 1 |
| indirect | 320 | **0.03** | 0.11 | 999 |

BM25 alone: **1.00 at rank 1** on direct, **0.00 at rank 572** on indirect — zero by construction,
because no word of an indirect question appears in its row.

With the real reranker, on a sample of 80 (40 per lever):

| lever | n | fusion recall@20 | fusion hit@10 | **B1 hit@10** |
|---|---|---|---|---|
| direct | 40 | 1.00 | 0.95 | **1.00** |
| indirect | 40 | 0.125 | 0.075 | **0.125** |

The ceiling holds exactly on the indirect lever: B1 equals fusion recall@20, the reranker promoting
every candidate that arrived and inventing none. On the direct lever it promotes the two that fusion
had ranked 11–20, taking 0.95 to 1.00. The sample's 0.125 is a lucky draw — its own recall@20 is
0.125 against 0.11 for the population — and the population figure is the one to quote.

> **Threshold `B1 hit@10 < 0.50`. Measured 0.03, with a proved upper bound of 0.11.**

### The shape of the failure

    on 193 of 320 indirect questions, the retriever returned a **legend** in the top 10

**It fetches the lookup table and never the answer.** The legend is the only document sharing
vocabulary with the question. A person reads the legend, learns the code, and opens the row — two
steps. Single-shot top-k retrieval has one step, and spends it on the first.

This is not a quirk of this corpus. It is what one-shot retrieval does whenever the question and the
index speak different languages and something in the corpus translates between them.

### Why the control closes the obvious objection

Same documents, same corpus, same retriever, same reranker. Asked in the index's own language the
answer comes back **first**, on 318 of 320. So:

- the documents are not broken
- the questions have answers
- the retriever is not misconfigured
- **only the human phrasing breaks it**

Without the 0.99 there is no reply to *"you just built a weird dataset."* With it, the only
difference between 0.99 and 0.03 is which vocabulary the question was written in.

---

## 5. Can the routing arm use it?

A family large enough to break retrieval is not automatically a family an agent can walk, and the two
constraints pull against each other. `./bench/crowd.py routecheck` is where that tension is made
visible rather than assumed away.

    section table      67 rows (3 legends + 64 rows), ~2,590 tokens
    legends lead       yes — "legend" sorts before "row", so they head the table
    the walk needed    area -> section -> three legends -> one row.  Five steps, no guessing.

Three commitments hold the comparison honest:

1. **hop 0 was not touched.** The frozen `use_when` sentences were written before this extension
   existed and do not mention it. A routing layer that wins because its table was rewritten for the
   test has not won anything.
2. **No information asymmetry.** Legends are in the retrieval pool. The baseline can retrieve
   everything the walker can open.
3. **Child order is now sorted.** It used to be whatever `rglob` returned — not reproducible across
   machines, and the agent is shown that list verbatim. A benchmark whose prompt depends on directory
   order cannot be replicated.

**Three defects were found by checking rather than by running**, and any one of them would have made
the routing result meaningless.

1. **`READ` returned nothing to the model.** `bench/agent.py` recorded the id and continued blind, so
   the walker was a router that selects documents rather than an agent that uses them. The real
   server's `knowledge_read` is documented as returning the document as written. On this corpus the
   defect is fatal by construction: every indirect question is *read the legend, learn the code, open
   the row*, and a walk that cannot see what it read could not have solved one — and would have been
   scored as failing at routing while being prevented from routing. READ now returns the text,
   clipped at 6,000 characters like the server, with `read_chars` recorded because reading is the
   part of a walk whose cost a hop count does not show.
2. **The agent's OpenAI path could not make a request.** It hand-rolled the call with `max_tokens`,
   which the newer models refuse while naming the replacement in the error body — and it discarded
   the body, so the failure arrived as `HTTP Error 400: Bad Request`, three times, retrying a 4xx
   that cannot fix itself. It now goes through the shared helper that already knew this.
3. **Child order came from `rglob`.** The agent is shown that list verbatim, so the prompt depended
   on directory order. Sorted now.

### What a walk looks like, end to end

Three questions through the fixed harness with `gpt-5` as the router (no Anthropic spend):

    h-perdiem-111-d    2 hops, 0.8k read.  OPEN expense | OPEN sec-hard-perdiem | READ <the row> | DONE
                       answer at rank 1.

    h-accrual-222-i    3 hops, 2.9k read.  OPEN attendance | OPEN annual-leave | OPEN sec-hard-accrual
                       | READ legend-type | READ legend-tenure | READ legend-site
                       | READ hard-accrual-row-type-e3-tenure-t3-site-l3 | DONE
                       **exactly the intended walk, and the row it opened is the answer.**

    h-perdiem-111-i    13 hops, 3.1k read, two returns to hop 0, and it never found the section —
                       it went into the frozen corpus's own overseas-travel documents instead.

The second of those is the study's thesis in one question: **the walk found what retrieval could not,
and scoped retrieval inside the very subtree the walk opened still missed it.** The third is the
subject of the threat below.

## 6. What this does and does not license

**Licensed.** On a corpus containing qualifier-indexed families with the mapping held in separate
legend documents, single-shot hybrid retrieval with an LLM reranker fails at 0.03 hit@10 while the
same retriever on the same documents scores 0.99 when the question uses the index's vocabulary. The
failure is a two-step lookup that one-shot retrieval structurally cannot perform.

**Not licensed.** Nothing about RAG in general. The frozen 700-document corpus does **not** break:
B1 stays at 0.80 under the hardest paraphrase the lexical sweep could produce. Both corpora belong in
the report as two rows, because the finding is about **corpus composition**, not about retrieval as
such. A reader whose corpus has no qualifier families should expect the 0.80, not the 0.03.

**A confound that must be fixed before the routing arms run.** The five families were given subjects
that fit the five frozen areas — and the frozen 700 already covers those areas thoroughly. So a
question about part-time leave accrual can be answered, in general terms, by a document that existed
before any of this was built, and scoring that as a miss measures a labelling decision rather than a
retriever. `./bench/crowd.py anatomy` splits the top ten by what it is made of:

| family | answer | sibling row | own legend | other family | **frozen 700** |
|---|---|---|---|---|---|
| accrual | 0% | 0% | 4% | 0% | **96%** |
| overtime | 0% | 13% | 6% | 0% | **81%** |
| perdiem | 2% | 31% | 2% | 0% | **66%** |
| threshold | 0% | 21% | 11% | 6% | **62%** |
| diligence | 1% | 39% | 15% | 7% | **38%** |

`sibling row` is the intended failure — the family was reached and the qualifier was not. `frozen 700`
is the confound, and on **accrual it is 96%**: the extension never enters the running at all.

So the families are not equally usable. **`diligence` is clean** and shows the designed failure.
`perdiem` and `threshold` are mixed. **`accrual` and `overtime` are not usable as they stand** — their
misses are not evidence. Either their subjects move to something the 700 does not cover, or the
incumbent documents that answer the question join `D_true`, or those two families are excluded and
said to be excluded. This is the same uniqueness rule that caught 128 rows carrying identical figures,
applied across the corpus boundary instead of within a family, and it was found by checking the
routing method rather than by running it.

**Open threats.**

- *The baseline may be handicapping itself.* At A=3 on the original corpus, dense alone scores 0.88
  at ten while fusing it with a collapsed BM25 list scores 0.39. The two halves agree 13% of the time
  there, so reciprocal rank fusion is averaging signal with noise. **Dense-only belongs in the report
  as a second floor**, or the fusion needs weighting by which half is carrying signal. On the hard
  extension this threat is weaker — dense alone cannot separate 64 identical rows either — but it
  must be measured rather than argued.
- *Templates are not prose.* The rows are machine-uniform. A corpus of human-written near-duplicates
  would be messier and probably easier. The claim is about the structure, and the structure is real
  in enterprise corpora; the uniformity is a simplification and is stated as one.
- *One vendor wrote the questions and another scores them.* The lexical sweep's questions were
  written by `gpt-5.2` and reranked by `gpt-5`. The hard extension's questions are templated, so this
  threat does not touch the 0.03 — but it does touch the 0.80 the extension is compared against.

---

## 7. Reproducing it

    ./bench/crowd.py write --grid 4x4x4     # 340 documents + 640 questions, deterministic
    ./bench/crowd.py stats                  # within/across-family vocabulary, and the leak check
    ./bench/crowd.py bm25                   # free: the keyword half
    ./bench/crowd.py routecheck             # free: what the walker is handed
    ./bench/crowd.py fusion                 # embeddings only: recall@20, which bounds B1
    ./bench/crowd.py anatomy                # what fills the top ten, and how much is the incumbent
    ./bench/crowd.py curve                  # dose and response over N

    BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/run.py eval/gold/hard-sample.yaml --arm B1

`--grid` sets rows per family as `a x b x c`, up to `8x8x8`. The expected ceiling is printed on
write, so a target can be chosen before anything is measured. `bench/corpus/` stays frozen at 700;
the extension loads only under `BENCH_EXTRA_CORPUS`.

Records: `eval/runs/2026-09-19-break-search.md` for the search that led here,
`eval/runs/2026-09-19-hard-b1-sample.json` for the reranked sample.
