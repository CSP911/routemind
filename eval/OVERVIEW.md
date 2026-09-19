# The argument, end to end

**Draft, 2026-09-19.** One question at the top, the sub-questions it forces, the data those demand,
and the sampling and controls that follow from the data. Then the history — including the three
answers that were wrong, because the shape of the study is mostly the record of correcting them.

Read this first. Everything else in `eval/` is a section of it seen close up.

---

## 1. The core question

> **How useful is human intervention in RAG, and where does it stop paying for itself?**

Two halves, and the second is the one that makes it a study rather than a pitch. *How useful* alone
invites a number with nothing to compare it to. *Where it stops paying* requires finding the edge,
which means the design has to be able to produce a negative.

**The intervention is a routing layer upstream of retrieval**: a human-written table that splits the
corpus into areas, describes each in one sentence, and arranges documents in a tree. An agent reads
the table and walks it.

Other places a person could intervene — chunking, document quality, metadata, relevance feedback —
are out of scope. The claim is narrower than the question, and the report says so.

RouteMind is the instance. The parts are named generically — *partition*, *description*, *hierarchy* —
so the study is about the idea.

---

## 2. Why it decomposes, and into what

The core question cannot be measured directly. Four things have to be settled first, and each is a
sub-question because the core answer is unreadable without it.

| | sub-question | why the core question needs it |
|---|---|---|
| **Q1** | *Which part of the intervention pays?* | "the table helps" is three claims — the partition, the descriptions, the hierarchy. If they are not separated, a win cannot be attributed and a loss cannot be fixed |
| **Q2** | *Where does it stop paying?* | this **is** the second half of the core question. It needs a difficulty axis the arms did not choose, and it needs the region where plain retrieval is fine, because that is where the answer is "it does not pay" |
| **Q3** | *When it fails, whose fault?* | a routing miss is a description that never named the subject, or a decision that was genuinely hard, or a model that could not follow an instruction. Three different fixes. Conflating them makes the result unactionable |
| **Q4** | *What does it cost?* | "pays for itself" is a ratio and only the numerator was ever measured. The denominator is calls, tokens, latency — and the human time to write and keep the table |
| **Q5** | *Does the answer stay right when the documents change?* | accuracy on a frozen corpus says nothing about a corpus that moves, and a stale answer is the failure a confident system makes most convincingly |

**The floor under all of them is a control.** Every one is a comparison against the same system with
the table removed — `B1`, hybrid retrieval and a reranker over the whole corpus. Without it the
numbers are absolute and absolute numbers mean nothing here.

---

## 3. What that demands of the data — and therefore what was built

Each demand below is a line from a sub-question to a thing that had to exist.

| the demand | comes from | what was built |
|---|---|---|
| a corpus with a hand-written routing table over it | all | **779 documents**, five areas, tree-structured, frozen so results stay comparable |
| a difficulty axis fixed **before** any arm runs | Q2 | five structural factors, then — after measurement — the axis that actually predicts failure |
| a region where plain retrieval **fails** | Q2 | the 779 never break. **340 more documents** were built that do |
| a region where plain retrieval is **fine** | Q2 | the 779. This is not a failed corpus, it is the other row of the table |
| questions whose answer is known and unique | all | templated generation, plus two checks that killed 128 rows and 102 leaks |
| a control asking the same thing in the index's own words | all | every row gets **two** questions: `direct` and `indirect` |
| documents that state which version is in force | Q5 | a dated line on every row, plus a **revision notice** per family |
| questions where the *older* document is correct | Q5 | **50 stale questions**, written against what each superseded document says |
| a per-question record of what a walk spent | Q4 | hops, characters read, and input/output/cache tokens, recorded per question |

Two of those deserve their own sentence.

**Why a second corpus at all.** The 779 cannot be broken. Under the hardest paraphrase that can be
written against it — questions sharing 8% of their vocabulary with the answer — B1 still scores 0.80.
Q2 asks where the intervention stops paying, and the honest answer on that corpus is *it never starts*.
So a corpus was built with the structure that does break retrieval, and **both are reported as two
rows**, because the finding is about corpus shape and not about retrieval in general.

**Why every row is asked twice.** A single number showing failure is unusable: the first objection is
that the dataset is rigged. The `direct` control answers it — same documents, same retriever, same
reranker, and the only thing that changes is which vocabulary the question uses.

---

## 4. The sampling frame, and why it is a frame and not a sample

    5 families x 3 axes x 4 values = 64 cells per family = 320 rows
      x 2 wordings                                       = 640 questions
      + 50 stale questions                               = 690

Every cell exists. Nothing was drawn from a larger pool, and **there is no population being estimated**.

- A rate over the 640 is a **census** of the frame. `B1 indirect hit@10 = 0.02` has no sampling error.
- The **A1 sample of 300** — 100 direct, 150 indirect, 50 stale, taken across the grid so every axis
  value appears — estimates the frame and nothing wider.
- Any statement about a different corpus is an **argument**, not a calculation. The argument is that
  qualifier-indexed tables with the mapping held elsewhere, and superseded rules never stamped
  superseded, are ordinary in real corpora. The *size* of the effect does not travel; the structure
  does.

Full account: **[DESIGN.md](DESIGN.md) §3**.

---

## 5. Controls, as consequences rather than a checklist

The control list is short because the arms were built to share everything except the thing under test.

**Held, and enforced rather than promised:** one corpus loader, so the string the agent reads is the
string the retriever indexes; the embedding cache keyed by model, so switching models cannot silently
reuse the old vectors; the same BM25 constants, the same 20 candidates, the same `k`, the same
reranker — which is never told which area a candidate came from; byte-identical question text across
arms; one scoring function, so the arms differ in what they hand it and never in how it is judged;
sorted child lists, because the agent is shown that list verbatim and it used to come from the
filesystem.

**Not held, with the direction each leans** — because a confound running against the hypothesis is a
discount and one running with it is a reason to distrust the result:

| | leans |
|---|---|
| router below the model floor (`claude-sonnet-5`) | **against** — makes the intervention look worse |
| GPT wrote the sweep's questions and GPT reranks them | **with** — inflates the baseline it is compared to |
| provenance lines dilute short documents | **with** — makes the baseline worse |
| the reranker is stochastic and was run once | unknown |

Full table, and how the last two were measured rather than asserted: **[DESIGN.md](DESIGN.md) §2**.

---

## 6. The history, including the three wrong answers

The design is mostly the record of being corrected by measurement. Skipping this makes the current
shape look arbitrary.

**First axis: coverage.** Whether an area's frozen description covers a document (strata S1–S4). It
was the independent variable, chosen before the corpus was generated. **Dropped** when it turned out
to describe one cause of difficulty among several — a question can be hard because it is phrased
differently, or because forty documents resemble the answer, and a covered/uncovered axis cannot say
either. Demoted to a secondary label.

**Second axis: five structural factors.** Lexical bridge, area spread, depth, routing margin,
crowding — each 0–3, summed. A 23-question pilot came back **1.00 on every arm in three of four
bands**, which is one row of signal for 23 questions. **Rebuilt** so the band cuts sat where plain RAG
actually breaks, rather than at numbers chosen by eye.

**Third axis: wording.** 368 questions, four wordings each, over 92 documents. The result killed the
scale:

    A=3 (full paraphrase)   BM25 recall@20 0.13, answer's median rank outside the top 50
                            dense recall@20 0.95, median rank 3
                            B1 0.80

A paraphrase destroys the keyword half and the embedding half shrugs. **The lexical factor was
measuring BM25's problem, not retrieval's.** And the three document-side factors were flat across
their whole range — no trend at all. One factor did everything and it was measuring the wrong thing.

It also caught the baseline handicapping itself: at A=3, dense alone scores 0.88 and fusing it with a
collapsed BM25 gives 0.39. The report owes a dense-only floor.

**Then: build a corpus that breaks.** Five families of 16 near-identical rows. Measured **1.00 on both
levers** — no collapse. The reason is arithmetic: with 16 rivals and 20 candidates every sibling
arrives and the reranker reads the qualifiers off them.

**Then the thing that actually worked, and it was not the one predicted.** Re-index the same 16 rows
by codes and move the person-to-code mapping into separate legend documents: **1.00 → 0.07**. Same
count, same subject, different structure. So the dominant cause is not how many rivals the answer has
— it is that **the question's words point at a different document than the answer**. Rival count is
the second factor and multiplies:

    recall@20 ≈ 0.25 × min(1, 20/N)      five points, N from 16 to 256, two parameters

Both hold under a second embedding model. Neither is one model's quirk.

**Then two defects in the answer key**, both caught by checking rather than by running. 128 of 320
rows carried figures identical to a sibling's, so a retriever that returned the twin had supplied the
right answer and was scored as missing. And the families' subjects overlapped the frozen 779 — on one
family the incumbent corpus filled 96% of the top ten — so a miss might be the old corpus answering
rather than the retriever failing, and **that bias ran towards the hypothesis**, which is the worst
direction.

**Then the fix, which failed first.** Adding provenance to every row so the corpus itself says which
version is in force. The first attempt was a 1,200-character block against 400 characters of content;
it dominated the rows' embeddings and pushed the incumbent's share from 38% to 81%. Two lines
recovered part of it, one line is what remains. **Chasing that share was itself a mistake**: a row
indexed by codes cannot out-rank a document written in the question's own subject words, and it is
not meant to. What the notice buys is that a miss is now *defensible* — the corpus states which
version is in force, so returning the older one is a stale answer rather than an arguable alternative,
and the gold label records what the documents say instead of ruling from outside them.

**And three defects in the harness**, found before the routing arms ran and any one of which would
have voided them: `READ` returned no text to the agent, so the walker could not use what it read; its
OpenAI path could not form a valid request; and the order of a table's rows came from `rglob`, so the
prompt depended on directory order.

---

## 7. Where it stands

| | |
|---|---|
| threshold | `B1 hit@10 < 0.50`, the point where retrieval misses more often than it finds |
| base corpus (779) | does not reach it. 0.80 under the hardest paraphrase — **and that is a result** |
| extension (1,114) | `direct` 0.99 · `indirect` **0.02** · recall@20 0.05 |
| replication | five families, five corpus sizes, two embedding models, deterministic |
| running now | B1 over all 690; then A1 over the 300-question purpose-stratified sample |
| not yet run | reranker variance, an Opus 5 re-run, a different-vendor control set |
| not measured at all | **the cost of writing and maintaining the table.** Q4's denominator is still half missing, and the report must say so rather than let a reader assume it is zero |

**What would falsify the claim**, written down before the run: if A1 does not rise materially above
B1 on `indirect`, routing does not recover what retrieval lost on a corpus built to be recoverable
that way. Or if A1's `scoped` score rises along with its `read` score — then the gain was scope
narrowing and the agentic part earned nothing. [DESIGN.md](DESIGN.md) §8.

---

## 8. The rest of `eval/`

| | |
|---|---|
| [DESIGN.md](DESIGN.md) | variables, sampling frame, pairing, power, falsification |
| [DATASETS.md](DATASETS.md) | every dataset, how it was made, what it is checked against — written for someone arriving from outside |
| [COLLAPSE.md](COLLAPSE.md) | the threshold, what `hit@10` and `recall@20` mean from first principles, and the corpus built to cross it |
| [PREREGISTRATION.md](PREREGISTRATION.md) | the commitments, fixed before the arms run |
| [DIFFICULTY.md](DIFFICULTY.md) | the difficulty scale, and rev. 6 on why four of its five factors did nothing |
| [fixtures/](fixtures/) | the continuity-fixture contract, for outside contributions |
| [runs/](runs/) | the record, including the attempts that failed |
