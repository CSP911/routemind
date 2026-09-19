# Run log — where does plain RAG break, and can it be broken on purpose?

**2026-09-19.** Written before the search, appended to during it. This is a run log, not a report:
raw, complete, and including the attempts that failed.

## Why this exists

`eval/DIFFICULTY.md` rev. 5 defines the severe band as the place plain RAG stops coping. That was a
definition with no measurement behind it. The pilot could not supply one — its hardest question
scored 12 of 15 and B1 was still at 0.67 — so nobody had yet asked this corpus anything at the
difficulty where a break could live.

The first sweep (`bench/probe.py`, 368 questions over 92 documents) found something that changes the
design rather than filling it in:

| | A=0 | A=1 | A=2 | A=3 |
|---|---|---|---|---|
| fusion recall@10 | 1.00 | 1.00 | 0.94 | **0.39** |
| fusion recall@20 | 1.00 | 1.00 | 0.95 | 0.81 |
| n | 125 | 71 | 97 | 75 |

and, across documents stratified by their own C+D+E from 0 to 9, recall@10 of 0.80–0.96 **with no
trend**. One factor does everything; three do nothing. Summing five factors equally is what flattened
the difficulty axis to 0.78–0.86 from sum 4 to sum 10 and made the pilot's lower three bands all
return 1.00.

So: **A is the only lever known to work, and it is not yet known to be enough.** The point of this
search is to find out what else breaks retrieval, and how far it can be pushed.

## The objective, stated so it can fail

Find question configurations where **B1 hit@10 is as close to 0 as the corpus allows**, subject to
two conditions that make the finding real rather than manufactured:

1. **Answerable.** A known document actually answers the question. Verified by a model that sees the
   question and that document and nothing else, and must quote the answering passage.
2. **Uniquely answerable.** No other document answers it as well. Verified against the documents that
   outranked the gold one — if one of them answers it, the miss is a labelling error, not a failure.

Without both, an adversarial search converges on questions so vague that nothing could match them,
which would be a fake break and worse than no result.

## The economy: search on the free signal

The reranker only ever reorders the fused top-20. So

    fusion recall@20  is a hard ceiling on B1 hit@10

and a question whose gold document is **not in the fused top-20 provably breaks B1**, with no rerank
call spent. A question embedding costs a fraction of a cent and no LLM call at all, so the search
runs on fusion rank and the reranker is spent only to confirm finalists and to measure the region
where fusion still holds.

## The ladder — each rung measured before the next is built

| | what | why | cost |
|---|---|---|---|
| **L0** | A=0..3 over 92 documents, B1 with the reranker | the baseline curve; where the break is, if it is anywhere | 368 rerank calls (running) |
| **L1** | two levers the first sweep never touched — `near` and `two` | crowding was scored by counting embedding neighbours, which is not the same as a question that cannot tell neighbours apart; area spread was never swept | 60 gen · 120 rerank |
| **L2** | stack whichever levers bit, with A=3 | if they are independent the effects multiply; if not, that is the finding | 40 gen · 80 rerank |
| **L3** | adversarial search: k variants per seed, keep the worst fusion rank, R rounds | the difference between *a hard question* and *the hardest question this corpus admits* | gen + embeddings only, then rerank the finalists |
| **L4** | corpus-side: inject distractor documents | **not executed.** It changes a corpus that is frozen at 700 documents and that is the operator's decision, not the search's | — |

### L1's two levers

    near   a question only one document in a crowded cluster (>= 8 documents) answers, where every
           sibling looks like it might. What separates them is a qualifier — a grade, a threshold, a
           date, an employment type — never the subject, because the subject is what they share.
    two    a question neither of two documents in different areas answers completely. Scored as
           `all` (both retrieved) and as `any` (either).

Each written at A=0 and at A=3, so the interaction is visible. A lever that only bites once the
wording is also far implies a different scale from one that bites on its own.

## Models, and the threat that comes with them

The Anthropic balance ran out mid-session (`HTTP 400: Your credit balance is too low`), which also
ended the unbounded-agent rerun at question 18 of 23. Everything below therefore runs on OpenAI:

| | model | |
|---|---|---|
| generation | `gpt-5.2` | writes the questions |
| verification | `gpt-5` | answerability and uniqueness, sees the gold document only |
| reranking | `gpt-5` | unchanged from the pilot |
| embedding | `text-embedding-3-large` | unchanged |

**Threat, recorded now rather than discovered later.** The corpus was written by Claude and the
questions are now written by GPT, against a retriever whose reranker is also GPT. A reranker may
favour text written by a sibling model, which would make the questions look *easier* than they are
and push the measured break point further out. The direction is conservative — it biases against
finding a break — but it is not nothing, and the model floor in PREREGISTRATION.md §9 governs the
router, not the question writer, so this does not violate it. Anything that survives here should be
re-checked with a Claude-written control set once the balance is restored.

## Results

### L0 — the baseline curve, and the ceiling that turned out to be exact

100 of 368 probes were reranked before the OpenAI balance ran out. The pattern is unambiguous well
before the rest would have arrived.

| A | n | fusion@10 | fusion@20 | **B1@10** |
|---|---|---|---|---|
| 0 | 34 | 1.00 | 1.00 | 1.00 |
| 1 | 19 | 1.00 | 1.00 | 1.00 |
| 2 | 27 | 0.93 | 0.93 | 0.93 |
| 3 | 20 | 0.35 | 0.80 | **0.80** |

**B1 equals fusion recall@20, to the second decimal.** The reranker recovers everything fusion puts
in its top 20 and nothing it does not. Two consequences, and the first is worth more than the run:

- **The target is measurable for free.** Breaking B1 means driving fusion recall@20 below 0.50, and
  fusion costs one cached question embedding and no LLM call. The expensive half of this study was
  measuring something the cheap half already determined.
- **Wording does not break RAG.** B1 at A=3 is 0.80 — "moderate" on the scale's own cuts, nowhere
  near severe. The lexical axis the difficulty scale was built on cannot reach the severe band.

### L0b — why not, decomposed (`bench/decompose.py`, no API)

| | n | BM25@20 | dense@20 | fused@20 | BM25@10 | dense@10 | fused@10 |
|---|---|---|---|---|---|---|---|
| A=0 | 125 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 |
| A=1 | 71 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 1.00 |
| A=2 | 97 | 0.82 | 0.97 | 0.95 | 0.76 | 0.94 | 0.94 |
| A=3 | 75 | **0.13** | **0.95** | 0.81 | 0.05 | 0.88 | 0.39 |

Median rank of the answer at A=3: BM25 **999** (outside the top 50), dense **3**, fused **13**.

**A paraphrase destroys the keyword half and barely touches the embedding half.** The A factor
measures BM25's problem, not retrieval's. `text-embedding-3-large` reads "taking time off in chunks
to look after my father through the same ongoing health problem" and returns the family-care-leave
document at rank 3.

**And the baseline is handicapping itself.** At A=3, dense alone scores 0.88 at 10; reciprocal rank
fusion with a collapsed BM25 list drags that to 0.39, and the full B1 pipeline — fusion plus the
reranker — reaches 0.80, still below dense alone. At A=3 the two halves agree on the answer 13% of
the time and exactly one half has it 81% of the time, so RRF is averaging a signal with noise. This
is a threat to the study and not a small one: **if B1 is crippled by naive fusion, part of any
routing advantage is an artefact of the baseline.** The report must carry dense-only as a second
floor, or the fusion must be weighted by which half is actually carrying signal.

### L0c — why the corpus cannot be broken (`bench/confusable.py`, no API)

The closest pair of documents in the whole 700 sits at cosine **0.911**, and the typical document's
nearest neighbour is around 0.78. Nothing in this corpus is *nearly the same thing as* anything else,
so the dense side always has a clean winner to return.

**The corpus is the difficulty, and it was never built to be hard.**

### L1/L2/L3 — blocked

`probe2.py`'s 120 questions (`near` and `two`, at A=0 and A=3) were written and are on disk.
`harden.py`'s adversarial search is written. Neither can run: measuring any new question requires
embedding it. Both providers are at zero.

    Anthropic   HTTP 400: Your credit balance is too low to access the Anthropic API.
    OpenAI      You have no credits remaining.

Also lost to this: the unbounded-agent rerun, which reached question 18 of 23. Its log survives and
records what matters — on the severe questions A1 hit the 30-turn ceiling (`hops 30 ... EXHAUSTED`,
`back 1`), so removing the return budget did not change the outcome, it only spent more. The budget
was not what those questions were failing on.

### L4 — the hard extension, built (`bench/crowd.py`, no API)

The measurements above name exactly what the corpus lacks, so it was built rather than waited for.
**80 documents in 5 qualifier families**, written from templates rather than by a model — two
model-written documents differ in a hundred incidental ways a retriever can latch onto; two documents
from one template differ in exactly the qualifier, which is the variable under study.

| family | area | axes | n |
|---|---|---|---|
| perdiem | expense | grade 1/3/5/7 × country band A/B/C/D | 16 |
| overtime | payroll | weekday/weekend/holiday/night × four hour bands | 16 |
| accrual | attendance | permanent/fixed-term/part-time/secondee × four tenure brackets | 16 |
| threshold | approval | equipment/services/travel/entertainment × four amount bands | 16 |
| diligence | procurement | domestic/EU/US/other × four contract-value bands | 16 |

Within a family the documents share **0.84–0.90** of their vocabulary; across families, 0.05–0.09.
Two questions per document, 160 in `eval/gold/hard.yaml`: one in the document's words, one in a
person's. Both have exactly one answer and the answer is stated plainly — the difficulty is entirely
in telling one document from its fifteen siblings.

`bench/corpus/` is untouched at 700. The extension loads only under `BENCH_EXTRA_CORPUS`, so 779
documents and 859 are two rows of one table.

**The prediction, on record before the dense half can be measured:**

    A=3 alone        kills BM25, dense survives          -> measured, B1 0.80
    family alone     dense cannot choose, but BM25 matches "grade 3" exactly and rescues it
    family x A=3     the paraphrase removes what BM25 needs and the family removes what dense needs

Half of it is already confirmed, for free, because BM25 needs no API:

| lever | n | BM25 hit@10 | hit@20 | median rank |
|---|---|---|---|---|
| family | 80 | 0.93 | 1.00 | **1** |
| family × paraphrase | 80 | 0.28 | 0.38 | **62** |

BM25 is *perfect* on qualifier families asked in the document's words — rank 1 — and collapses to
rank 62 when the same question is asked in a person's words. The keyword half behaves exactly as
predicted in both cells.

**What remains unmeasured is the one cell the whole design turns on: dense retrieval on
`family × paraphrase`.** If it collapses too, the severe band exists and it is a corner of two axes
rather than a point on one. If it holds, no arrangement of this kind of corpus breaks a modern
embedding model, and that is a finding worth more than the band.

### What runs first when there is a balance

    ./bench/probe.py run --rerank                                   # finish L0: 268 probes left
    BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/run.py eval/gold/hard.yaml --arm B1
    ./bench/probe2.py run --rerank                                  # L1, questions already written
    ./bench/harden.py search && ./bench/harden.py verify            # L3

The first two are the ones that matter. Everything else is already on disk.
