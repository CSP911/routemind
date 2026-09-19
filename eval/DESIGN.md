# Experimental design — variables, population, and what the numbers can carry

**Draft, 2026-09-19.** What `PREREGISTRATION.md` states as commitments, written here as a design: what
varies, what is held, what is not held and in which direction it leans, what the questions are a
sample *of*, and which comparisons the sampling actually licenses.

It exists because those things were scattered. §8 of the pre-registration says "paired design" in one
line and §11 lists five threats; neither says what the unit of analysis is, what the population is,
or why a difference of 0.03 against 0.97 means anything given how the questions were made.

---

## 1. Unit of analysis

**The question.** Not the document, not the arm, not the family.

Every measurement below is a per-question outcome, and every comparison is between two arms *on the
same question*. A family's rate is an average over its questions and carries a question-level
interval; a corpus-level rate is an average over all of them.

This matters for one reason that is easy to get wrong: the 64 rows in a family are not 64 independent
draws from anything. They are one template evaluated at 64 points. A confidence interval computed as
if they were independent will be too narrow. §6 says what is done about that.

---

## 2. Variables

### 2a. Independent — what is deliberately varied

| | levels | how it varies |
|---|---|---|
| **arm** | `B1` · `A1` | within question: every question goes through both |
| **question purpose** | `direct` · `indirect` · `stale` | between questions, by construction |
| **corpus** | 779 base · 1,114 with the extension | between runs, one environment variable |
| **family** | perdiem · overtime · accrual · threshold · diligence | between questions; a blocking factor, not a treatment |

`arm × purpose` is the design. The other two are blocks: they exist so an effect can be shown to hold
in five different subjects and at two corpus sizes, not so they can be averaged over.

**A3 is not a level.** It was — one routing decision, then retrieval in the areas it named — and it is
unscheduled because A1's `scoped` score is the same control on a tighter scope (`PREREGISTRATION.md`
§4). `--arm A3` still runs.

### 2b. Dependent — what is measured

| | | primary? |
|---|---|---|
| `hit@10` | is a `D_true` document among the ten returned | **yes** |
| `recall@20` | is it among the twenty candidates, before reranking | bound on the above, free to compute |
| `rank` | where the first `D_true` sits; 999 for outside the top 50 | secondary |
| `routing_hit` | did the arm end up in an area that holds an answer | diagnostic (F1) |
| `hops` · `read_chars` · `usage.{in,out,cache_read,cache_write}` | what a walk spent | **cost side of the question** |
| `reranked` | whether a reranking call was made, or the miss was already decided | audit |

For A1, `hit@10` is computed twice and both are reported:

    read     over the documents the agent collected — what a consumer is handed
    scoped   over retrieval inside the subtree the walk opened, filled to k — the same haystack,
             without the reading

`read` is the headline on this corpus and `scoped` is the control. The report says which is which
every time it prints them, because they can differ by more than the arms do.

### 2c. Held constant — and how that is enforced rather than promised

| held | value | enforcement |
|---|---|---|
| corpus text | identical for all arms | one loader; `run.corpus()` builds the indexed string, and `READ` hands the agent the same string it indexes |
| embedding model | `text-embedding-3-large` | cache keyed by `model\0text`, so a switch cannot silently hit the wrong vectors |
| BM25 | k1=1.2, b=0.75, same stopwords | one implementation |
| candidates | fused top 20 | same constant in every arm |
| `k` | 10 | same |
| reranker | `gpt-5`, blind to areas | the reranker is never told which area a candidate came from |
| question text | byte-identical across arms | one gold file, read once |
| scoring | one `score()` | arms differ in what they hand it, never in how it is judged |
| child order | sorted by id | it used to come from `rglob`, so the agent's prompt depended on directory order |

Two of those were defects found by checking rather than by running, and both are recorded where they
were fixed: the agent used to see a different corpus string than the retriever indexed, and the table
it was shown was in filesystem order.

### 2d. Not held — and which way each leans

Naming the direction matters more than naming the threat. A confound that runs *against* the
hypothesis is a discount on the result; one that runs *with* it is a reason to distrust it.

| not held | direction | what is done |
|---|---|---|
| **reranker is stochastic** | unknown, small | one run so far. Repeat measurement is owed and is listed in §7 |
| **router below the model floor** (`claude-sonnet-5`, floor is Opus 5) | against — a weaker router makes A1 look worse | deviation recorded with its evidence; any failure a conclusion rests on is re-run on Opus 5 |
| **questions written by GPT, reranked by GPT** (the 368-question lexical sweep only) | with — a reranker may favour a sibling model's phrasing, inflating B1 | the hard corpus is templated, so it does not touch the 0.03; it does touch the 0.80 that 0.03 is compared against |
| **the extension is templated, the base corpus is model-written** | unknown | stated; a human-written control set is the first thing asked of a contributor |
| **provenance lines dilute short documents** | with — it makes B1 worse | measured: the incumbent's share of the top ten moved 38→81→64→62% as the notice went 1,200 chars → 2 lines → 1 line. Reported, not hidden |
| **the extension's subjects overlap the base corpus** | was *with*, now neutral | the revision notices make the older document demonstrably superseded, so returning it is a stale answer rather than an arguable alternative |
| **one domain, one fictional company** | unknown | external validity is by argument, not by sampling. §5 |

---

## 3. The population, and what the questions are a sample of

This is the part that is easiest to overstate, so it is stated narrowly.

**There is no population being sampled.** The corpus is constructed and the questions are generated
from it. Nothing here is an estimate of a parameter in a wider world, and no interval below should be
read as one.

What there *is* is a **sampling frame**, and it is finite and fully enumerated:

    5 families x 3 axes x 4 values  =  64 cells per family  =  320 rows
    x 2 wordings                    =  640 questions
    + 50 stale questions, written against what each superseded document says

Every cell exists; nothing was drawn from a larger pool. So:

- **A rate over the 640 is a census, not an estimate.** `B1 indirect hit@10 = 0.02` is the exact value
  over the whole frame, and it has no sampling error at all.
- **A rate over the A1 sample of 300 is an estimate of the frame**, and there the interval applies.
- **Neither is an estimate for any other corpus.** That step is an argument (§5), not a calculation.

### The A1 sample

A1 is the expensive arm — several model calls with the conversation resent each turn — so it runs on
300 of the 690, drawn by purpose:

| purpose | n | per family | what it establishes |
|---|---|---|---|
| `direct` | 100 | 20 | the control: the documents, questions and retriever are sound |
| `indirect` | 150 | 30 | the collapse: legend, then code, then row |
| `stale` | 50 | 10 | the mirror: the older document is correct, and reaching for the newest is wrong |

**Systematic, not random.** Within each family the cells are taken across the 4×4×4 grid by walking
the axis-sum order, which guarantees every value of every axis appears — verified, five families,
three axes, all four values each. A random draw would buy randomisation-based inference the design
does not use anyway, and would cost reproducibility, which it does use: the same command produces the
same 300 questions on any machine.

The cost of that choice is stated plainly: **no inference here rests on random sampling.** The
intervals in §6 are computed over questions treated as exchangeable within a family, which is an
assumption, not a fact.

---

## 4. Pairing, and why the comparison is within-question

Every question goes through every arm, on the same corpus, with the same retrieval components. The
comparison is therefore **paired**, and the right statistic is the per-question difference — not the
difference of two rates.

    for each question:   B1 hit ∈ {0,1}   A1 hit ∈ {0,1}
    the four cells:      both hit · A1 only · B1 only · neither

The claim under test lives in one cell: **A1 only**. A test of two independent proportions would
ignore that the same questions produced both columns and would be the wrong test, wider than it needs
to be and answering a question nobody asked.

McNemar's test on the discordant pairs (`A1 only` vs `B1 only`) is the primary test. The effect size
reported alongside it is the paired difference in rates with a bootstrap interval over questions.

---

## 5. External validity, stated as an argument

Nothing above generalises by sampling, because nothing was sampled from anywhere. What can be argued:

**The structure is real.** Qualifier-indexed tables with the mapping held elsewhere — tariff codes,
pay bands, risk tiers, plan codes, per-country per-grade travel schedules — are ordinary in
enterprise corpora, and usually larger than 64 rows. Superseded rules that were never stamped
superseded are likewise ordinary, and are the reason "stale answer" is a named failure type.

**What does not generalise** is the size of the effect. On the frozen 700 — a corpus with no
qualifier families and no supersession — B1 does not fall below 0.80 under the hardest paraphrase that
could be written. A reader whose corpus looks like that should expect 0.80, not 0.03. The report
carries both as two rows for exactly this reason, and a claim about "RAG" without naming the corpus
shape is not one this study supports.

---

## 6. Power, and what the intervals mean

The primary contrast is B1 against A1 on `indirect`, at n=150 paired.

- The observed B1 rate on the full frame is 0.02. Detecting any A1 rate above about 0.12 at n=150 is
  a matter of arithmetic rather than power: the discordant count would be large and one-sided.
- The direction that could fail to reach significance is the opposite one — A1 *also* failing. At
  n=150, if both arms sat near 0.05, the design could not separate them, and the honest report would
  be that routing does not recover this corpus.
- Per family (n=30 indirect) a rate near 0.10 carries a 95% interval of roughly ±0.11. **Family-level
  numbers are for seeing whether the direction holds in five subjects, not for ranking the families.**

Intervals are bootstrapped over questions. Because 64 questions in a family are one template at 64
points, a plain bootstrap understates the uncertainty; intervals are therefore also reported with the
family as the resampling unit (5 clusters), which is conservative to the point of bluntness. Both are
shown, and where they disagree the conservative one governs the claim.

---

## 7. What is owed before the report

- **Reranker variance.** One run. The primary contrast should be repeated at least twice.
- **Opus 5 re-run** of whatever failures a conclusion rests on.
- **A human-written or different-vendor control set**, to size the vendor-affinity threat.
- **The base-corpus row.** The extension's numbers mean little without 779 beside them.
- **Upkeep.** "Pays for itself" implies a cost of writing and maintaining the table, and nobody has
  timed it. Token counts now measure the cost of *using* the table; the cost of *having* one is still
  unmeasured, and the report must say so rather than let the reader assume it is zero.

---

## 8. What would falsify the hypothesis

Written down before the run, so that it cannot be revised afterwards into something the result
happens to satisfy.

The claim is that a human-written routing layer earns its upkeep where retrieval stops coping.

It is **falsified** if, on `indirect`:

- A1 `read` hit@10 is not materially above B1 — say, below 0.30 when B1 is near 0.02. Then walking a
  tree does not recover what retrieval lost, on a corpus built to be recoverable that way.
- Or A1 `read` is above B1 but A1 `scoped` is too, by a similar margin. Then the gain is scope
  narrowing and not the reading, and the agentic part is not what earned it.

It is **not** falsified by A1 failing on `stale`. That is a different claim (does a walker notice
which version is current), reported separately, and failing it is a finding about supersession rather
than about routing.

And the result is **already bounded** on the other side: on the frozen 700, B1 does not collapse at
all, so the honest form of any conclusion is conditional on the corpus containing the structure §5
describes.
