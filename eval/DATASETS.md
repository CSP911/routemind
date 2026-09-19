# The datasets — what exists, how it was made, and what it is checked against

Written for someone joining from outside, who has not read the rest of `eval/`. It assumes no
familiarity with the project and defines its terms as it goes. Everything here is reproducible from
the repository; the last section says how.

---

## 1. What the study is trying to find out

A retrieval system cannot hand a language model a whole corpus. It retrieves a few documents and
hands over those — here, **ten documents out of 1,114**. Everything follows from one consequence:

> If the document that answers the question is not among those ten, no model can answer it. It cannot
> report what it was never shown.

RouteMind's claim is that a **human-written routing layer** — a table that splits a corpus into
areas, describes each in a sentence, and arranges documents in a tree — earns its upkeep by letting
an agent walk to the answer instead of ranking the whole corpus at once. The study asks where that
intervention pays and where it stops paying.

So the datasets exist to answer two things: **where does plain retrieval fail**, and **does walking a
human-made tree fix it**.

---

## 2. The corpora

Two, and they are kept apart on purpose.

### 2a. The base corpus — 779 retrievable documents

A synthetic back-office knowledge base in five areas:

    approval · attendance · expense · payroll · procurement

Generated from a written specification of 69 topic clusters, before any question was written. It has
a tree: areas contain section pages, section pages contain documents. Section pages are signposts
rather than answers, so they are part of the tree the agent walks and are kept out of the pool the
retriever searches — 779 retrievable of 860 nodes.

**It is frozen.** Nothing in this study modifies it, so any two results measured on it are comparable.

**What it does not do: it does not break retrieval.** The hardest questions that could be written
against it — full paraphrases sharing 8% of their vocabulary with the answer — still score 0.80
(definition of that number in §4). That finding is itself a result, and it is why the second corpus
exists.

### 2b. The hard extension — 340 documents

Built after measurement showed what the base corpus could not do. It loads **on top of** the base
only when an environment variable points at it, giving **1,114 retrievable documents**, so results on
779 and on 1,114 are two rows of one table rather than one number that quietly changed meaning.

It is five groups of documents, one per area. Each group is one subject written 64 times, differing
only in the values of three qualifiers:

| group | area | the three qualifiers |
|---|---|---|
| perdiem | expense | grade × country band × length of stay |
| overtime | payroll | day type × hour band × work location |
| accrual | attendance | employment type × service band × site class |
| threshold | approval | spend category × amount band × commitment term |
| diligence | procurement | supplier origin × contract value × supply category |

Three kinds of document in each group:

    64  rows      the answers. Each states its qualifiers as **codes** — "grade G3", "band B2",
                  "stay S2" — and the four figures that apply. Nothing else separates one row from
                  its 63 siblings; within a group they share 83-89% of their words.
     3  legends   the mapping from a person's words onto those codes: which city is which band,
                  which job title is which grade, how a length of stay is banded.
     1  section   the page that lists the above. Legends are listed first.

**The codes are the point.** A row that said "on standby" could be matched by a question that said
"on standby at home"; a row that says `P3` cannot be matched by anything a person would type. Real
systems index this way — tariff codes, pay bands, risk tiers — with the mapping written down
elsewhere.

**Nothing here was written by a model.** These are templates. Two model-written documents differ in a
hundred incidental ways a retriever can latch onto; two documents from one template differ in exactly
the variable under study. Regenerating is one command and takes seconds.

---

## 3. The question sets

| set | n | how it was written | what it is for |
|---|---|---|---|
| `eval/gold/pilot.yaml` | 23 | by hand | a plumbing check on the base corpus — does the scoring run end to end |
| lexical sweep | 368 | `gpt-5.2`, four wordings of the same question per document | how far a question's wording can drift before retrieval loses it |
| lever set | 120 | `gpt-5.2` | two untested shapes — a crowded cluster, and a question needing two areas. **Written, never measured** |
| `eval/gold/hard.yaml` | 640 | templates | the extension. Two questions per row |
| `eval/gold/hard-sample.yaml` | 80 | every eighth of the above | the subset put through the real reranker, which costs money per question |
| `eval/gold/hard-smoke.yaml` | 3 | hand-picked | proves the harness runs end to end before it is trusted with a run |

### The two questions per row, which is the whole design

Every row in the extension gets asked twice, for the same answer:

    direct     "For grade G2, band B2, stay S2, what can I put on a hotel each night?"
    indirect   "I'm a team manager — Singapore, four nights — what can I put on a hotel each night?"

The indirect question contains **no word that appears in its answer row**. `manager`, `Singapore` and
`four nights` appear only in the legends. Answering it needs a **lookup and then a fetch**: read the
legend, learn the code, open the row.

`direct` is the control, and the result is unusable without it. It proves the documents are not
broken, the questions have answers, and the retriever is not misconfigured — so that when `indirect`
fails, the only thing that changed is which vocabulary the question was written in.

Each question records: the answer document, the area it is in, which legends are needed, and which
lever it belongs to.

---

## 4. What is measured, and against what

### The two numbers

**`hit@10`** — the share of questions where the answer document was among the ten the retriever
returned. 1.00 means always; 0.03 means three questions in a hundred.

**`recall@20`** — the same, for the twenty candidates produced *before* the final reranking step. The
retrieval pipeline has two stages: keyword search and embedding search are fused into 20 candidates,
then a language model rescores those 20 and the top 10 are kept.

*(With one correct document per question — this study's case — `recall@k` and `hit@k` are the same
quantity. They differ only when a question has several correct answers.)*

**Why both:** the reranker reorders candidates, it cannot fetch a document that is not one. So
`recall@20` is a **mathematical upper bound** on `hit@10`, and it costs one cached embedding and no
model call, while `hit@10` costs a model call per question. Measured on three corpora so far, the two
agree to the second decimal — the reranker recovers everything that reaches the candidate list and
nothing that does not.

### The threshold

    B1 hit@10 < 0.50      the retriever misses more often than it finds

`B1` is the baseline arm: keyword + embedding retrieval with the reranker, no routing layer, whole
corpus in scope. Below a coin flip a retriever is not a tool that sometimes struggles; it is a tool
that does not work. This is the definition of the study's **severe** band.

### Where things currently stand against it

| | n | direct `hit@10` | indirect `hit@10` | indirect `recall@20` |
|---|---|---|---|---|
| base corpus, hardest paraphrase | 368 | — | 0.80 | 0.80 |
| extension, fusion | 640 | 1.00 | **0.03** | 0.11 |
| extension, with the real reranker | 80 | 1.00 | 0.125 | 0.125 |

Keyword search alone on the extension: **1.00 at rank 1** on direct, **0.00 at rank 572** on indirect.

**The failure has a characteristic shape.** On most indirect questions the retriever returns a
**legend** in the top ten — the lookup table, not the answer — because the legend is the only document
that shares vocabulary with the question. A person reads the legend, learns the code, opens the row:
two steps. Single-shot retrieval has one and spends it on the first.

### Replication

Not one measurement. The collapse holds:

- across **five independent groups**, different subjects and different qualifiers;
- across **five corpus sizes**, 16 to 256 rows per group — and at every size, including 16;
- across **two embedding models**, `text-embedding-3-large` and `text-embedding-3-small`;
- **deterministically** — embeddings are cached and the fusion is arithmetic, so a rerun is identical. Only the reranking step is stochastic, and it was sampled once.

A two-parameter model fits the size sweep: `recall@20 ≈ 0.25 × min(1, 20/N)`, where 0.25 is the chance
the question reaches its answer's group at all and `20/N` is the share of that group the candidate
list can hold.

---

## 5. The checks that guard the data

A dataset that is hard for the wrong reason is worse than no dataset. Each of these was written
because it caught something.

| check | what it prevents | last result |
|---|---|---|
| `crowd.py stats` — leak | a question sharing a *discriminating* word with its own row, which lets the retriever pick it without using a legend | **0 of 320** (was 102) |
| `crowd.py stats` — uniqueness | two rows carrying identical figures, so a retriever that returns the twin gave the right answer and is scored as missing | **0 of 320** (was 128) |
| `crowd.py anatomy` | the extension never entering the running, because the base corpus already covers the subject | **see the open problem below** |
| `crowd.py routecheck` | a group large enough to break retrieval but too large for an agent to walk | 67-row table, ~2,590 tokens, legends first |
| `crowd.py bm25` | half the prediction, free — keyword search needs no API | direct 1.00, indirect 0.00 |
| index consistency | the two code paths building document text differently, so the bound and the measurement disagree | caught: `hit@10` 0.125 above a `recall@20` of 0.100 |

### The open problem, stated plainly

The five groups were given subjects that fit the five existing areas — and the base corpus already
covers those areas. `crowd.py anatomy` splits what actually fills the top ten:

| group | the answer | a sibling row | its own legend | **a base-corpus document** |
|---|---|---|---|---|
| accrual | 0% | 0% | 4% | **96%** |
| overtime | 0% | 13% | 6% | **81%** |
| perdiem | 2% | 31% | 2% | **66%** |
| threshold | 0% | 21% | 11% | **62%** |
| diligence | 1% | 39% | 15% | **38%** |

`a sibling row` is the intended failure: the group was reached, the qualifier was not. The last column
is the problem. On `accrual` the extension never enters the running at all.

And the two documents **disagree**. For "part-time, five years, how much leave per month", the base
corpus says fifteen days granted annually and explicitly that part-time is not adjusted; the extension
row says 1.24 days accrued per month, by employment type. Different numbers, different mechanism.

**This is being treated as a second axis rather than as contamination.** A corpus where an older
general rule and a newer specific table both exist, and the older one is never stamped "superseded",
is what real corpora look like — and returning the superseded rule is one of the failure types this
study already names (*stale answer*). The planned fix adds a dated **revision notice** document to
each group, retrievable like any other, so the currency of a rule is something an arm can find rather
than something it must guess. Until that lands, the numbers for `accrual` and `overtime` are not
evidence and are not quoted as such.

---

## 6. What has not been run

- **The routing arms have never run on the extension.** Checking the harness first found three defects
  that would each have voided the result — the agent's `READ` returned no text to the model, its
  OpenAI path could not form a valid request, and the order of a table's rows came from the
  filesystem. All fixed, and a three-question walk now runs end to end: on one of them the agent read
  all three legends and opened the correct row, while retrieval restricted to the very subtree it had
  opened still missed.
- The 120 lever questions.
- Difficulty factors for the 320 new documents.
- Reranker variance — the 80-question sample was run once.

---

## 7. Where a contributor fits

The most valuable thing an outside contributor can bring is **a failure the accuracy numbers cannot
see**. `eval/fixtures/` holds the contract for one such kind — *continuity fixtures*, which test
whether an answer stays correct after the underlying documents change. The revision-notice work in §5
is the same territory, and the two should meet.

Concretely useful, in order:

1. **A control set written by a different hand.** The sweep's questions were written by a GPT model
   and scored by a GPT reranker; the extension's are templated. A set written by a person, or by a
   different model family, would tell us how much of the 0.80 is vendor affinity.
2. **Continuity fixtures** against `eval/fixtures/README.md`.
3. **A judgement call we cannot make alone:** when two documents in a corpus answer the same question
   differently, what is the correct answer? §5 takes one position. It is arguable.

---

## 8. Running it

    ./bench/crowd.py write --grid 4x4x4     # regenerate the extension and its questions
    ./bench/crowd.py stats                  # the leak and uniqueness checks
    ./bench/crowd.py bm25                   # keyword search only — no API key needed
    ./bench/crowd.py routecheck             # what the walking agent is handed
    ./bench/crowd.py anatomy                # what fills the top ten, and how much is the base corpus
    ./bench/crowd.py fusion                 # embeddings only: recall@20, which bounds the result
    ./bench/crowd.py curve                  # the size sweep, 16 to 256 rows per group

    BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/run.py eval/gold/hard-sample.yaml --arm B1

`--grid a x b x c` sets rows per group; the expected bound is printed when it writes, so a target can
be chosen before anything is measured. The base corpus stays at 779 unless `BENCH_EXTRA_CORPUS` is set.

Further reading, in the order it was written: **[COLLAPSE.md](COLLAPSE.md)** (the threshold and the
corpus built to cross it), **[DIFFICULTY.md](DIFFICULTY.md)** (the difficulty scale, and rev. 6 on why
four of its five factors did nothing), **[PREREGISTRATION.md](PREREGISTRATION.md)** (the design, fixed
before the arms run), and `eval/runs/` (the record, including the attempts that failed).
