# Difficulty — how a question is graded, and why

The study's frame is **difficulty × routing**: four bands of how hard a question is to answer, each
run with the routing layer and without it. The core question — *how useful is human intervention in
RAG, and where does it stop paying* — is answered by how the gap between those two columns changes
as difficulty rises.

Difficulty is therefore the independent variable, and it has to be fixed **before** any question is
written or any arm is run, or the bands become a description of the results.

Two commitments shape everything below.

**Difficulty is computed from structure, then checked against people.** Each question's difficulty is
a number computed from the question and the corpus — never from how any arm performed on it. This
survives the calibrated cuts below and is the reason they are safe: *where* the band boundaries sit is
learned from plain RAG, but *which side* a given question falls on is decided by its own structure,
before it is run.

**Difficulty is a property of a (question, answer) pair, not of a document.** The same document is
easy to reach when the question uses its words and hard when it does not. Document-level factors are
computed in advance; the pair-level ones are fixed when the question is written, against definitions
frozen here.

---

## The five factors

Each is graded 0–3. Three of the five need no model at all. The two that do — routing margin and
crowding — are computed with **`text-embedding-3-large`, pinned**, and that is the same model the
dense side of the retrieval arms uses. This was not the original intention and the reason for the
change is worth recording.

The plan was to compute D and E with a different model, since a difficulty scale built from the
retriever's own geometry is calibrated to that retriever's blind spots. Measured across
`text-embedding-3-large` and `text-embedding-ada-002` on all 700 documents:

| | same band across the two models |
|---|---|
| C depth | 700/700 — structural, no model involved |
| D margin | 192/700 (27%) |
| E crowding | 54/700 (8%) |
| C+D+E | 11/700 (2%) — **79% of documents change band** |

The shift is entirely one-directional: ada-002 scores every document harder, because its cosines run
higher across the board and a fixed 0.70 neighbour threshold therefore catches far more. **An absolute
threshold does not carry between embedding models.**

That leaves two ways to define the cuts, and they trade against different things.

- **Quantiles of whatever model is in use.** Stable across models — but it defines the top quarter of
  any corpus as hard, which would make the 79-vs-800 scale comparison vacuous: difficulty would be
  a fixed share by construction, and the effect of scale on difficulty could not appear.
- **Absolute cuts with the model pinned.** Comparable across corpus sizes, which the scale axis needs;
  breaks if the model changes, which is now a measured quantity rather than a worry.

The scale axis is load-bearing, so the cuts stay absolute and the model is pinned. The cost is stated
in §Threats and its size is known: **re-deriving D and E with a different embedding moves 79% of
documents by one to six points.** Anyone re-running this must use the same model or re-derive the
cuts, and the factor tool prints which model produced its numbers for exactly that reason.

Thresholds below are the observed quartiles of the corpus as it stands (700 documents, measured
2026-09-18, `text-embedding-3-large`).

### A · Lexical bridge — does the question use the document's words?

Fraction of the question's content tokens (stopwords removed) that appear in the answer document.
Pure string matching, no model.

| | | Meaning |
|---|---|---|
| **0** | ≥ 0.75 | the question is nearly a quotation of the document |
| **1** | 0.50 – 0.75 | the same words, differently arranged |
| **2** | 0.25 – 0.50 | the question paraphrases — "can I expense a client dinner" against a document titled *Entertainment caps* |
| **3** | < 0.25 | almost no shared vocabulary. The answer is reachable only by meaning — a person recognises it instantly and a term-matching system cannot |

Level 3 is the **lexical gap**, and it has to be written on purpose. A corpus and its questions
written by the same hand drift into shared vocabulary without anyone intending it.

### B · Area spread — how many areas must be consulted?

From the gold label, not measured.

| | | Meaning |
|---|---|---|
| **0** | one area, no plausible rival | |
| **1** | one area, but a second is defensible | a marker that the routing decision is contestable even when it has one right answer |
| **2** | two areas, **either** suffices (`needs: any`) | "how long is a contract kept" — approval or procurement |
| **3** | two or more, **all** required (`needs: all`) | "what do I log for a trip, and what does it pay" — attendance *and* expense. Neither alone is an answer |

Level 3 is the failure a global retriever does not have and this design does: an answer that no single
description claims.

### C · Depth — how far down the tree does the answer sit?

Hops from hop 0 to the answer document. Structural, no model.
Observed: depth 1 · 199 documents, 2 · 233, 3 · 42, 4 · 57, 5 · 124.

| | | |
|---|---|---|
| **0** | depth 1 | directly under the area representative |
| **1** | depth 2 | one section down |
| **2** | depth 3–4 | |
| **3** | depth 5 | every intermediate advertisement has to be read correctly, and a wrong turn at any hop ends it |

### D · Routing margin — how close is the second-best area?

For the answer document: the gap between the best-matching area description and the second-best,
each scored as the maximum over that description's clauses.
Observed: min 0.000 · p25 0.034 · median 0.072 · p75 0.129 · max 0.394.

| | | |
|---|---|---|
| **0** | > 0.129 | one area is plainly nearest |
| **1** | 0.072 – 0.129 | |
| **2** | 0.034 – 0.072 | |
| **3** | < 0.034 | two descriptions are effectively indistinguishable. Under 0.01 the router is choosing by noise |

**252 of 701 documents (36%) have a nearest description that is not their own area's.** That is not a
flaw in the corpus; it is the ambiguity this design moved from the retriever into the sentences, and
it is what makes level 3 available in quantity.

### E · Crowding — how many documents look like the answer?

Number of other documents within 0.70 cosine of the answer document.
Threshold chosen because it discriminates: at 0.80, 74% of documents have no neighbour at all and the
factor says nothing. At 0.70 — median 2, p75 3, p90 5, max 14, and 16% isolated.

| | | |
|---|---|---|
| **0** | 0 neighbours | nothing else in the corpus resembles it |
| **1** | 1–2 | |
| **2** | 3–5 | the reranker has real work to do |
| **3** | 6+ | a thicket. The right document is one of many that all answer *something* like the question |

---

## Bands

The five levels are summed, 0–15. The sum is the difficulty of a question. What the **cuts** in that
sum mean is the subject of this section, and it changed after the pilot.

### Why the cuts are calibrated against plain RAG

The first version cut at 0–2 / 3–5 / 6–9 / 10–15. Those numbers were chosen by eye, and the pilot
showed what that costs: the three lower bands came back at 1.00 on every arm. Twenty-three questions
bought one row of signal. "Severe" meant nothing more than *a big number on a scale I invented* —
there was no reason a sum of 10 should be the place anything happens.

So the cuts are placed where something does happen. **Severe is where plain RAG breaks**, and the
other three cuts are placed the same way, off the same curve:

| Band | Defined by | Meaning |
|---|---|---|
| **쉬움 / easy** | B1 hit@10 ≥ 0.95 | retrieval alone is essentially always right |
| **보통 / moderate** | 0.80 ≤ B1 < 0.95 | retrieval alone is usually right |
| **어려움 / hard** | 0.50 ≤ B1 < 0.80 | retrieval alone is right more often than not |
| **극악 / severe** | B1 hit@10 < 0.50 | **retrieval alone misses more than it hits** |

B1 is the baseline arm: hybrid retrieval and the reranker, no routing layer, whole corpus in scope.
Hit@10 against `D_true`, the same metric the report uses.

This is the definition the design has been reaching for all along. The claim under test is that human
intervention pays where retrieval stops coping; "where retrieval stops coping" is now a measured
place rather than an assertion.

### What this costs, stated plainly

**B1's column stops being a result.** It is the axis. Reading "B1 does worse in severe questions" off
the results table is reading the definition back out, and the report says so at the top of that table.

What remains a result, and is the whole study: **A3 and A1 in each band.** Whether routing recovers
what plain retrieval lost at B1 < 0.50 is not settled by any definition, and that is the number the
core question turns on.

### The calibration set keeps it non-circular

Fitting cuts on the same questions you report on would let a band boundary chase a single question.
It does not happen here, because the fit and the report never touch the same questions.

- A **calibration set** of ~60 questions is written first, spanning sums 0–15 with at least three
  questions at each sum. It is written to the same rules as the gold set and **never appears in it**.
- **Only B1 is run on it.** No router, no agent — the calibration must not be able to see the arms it
  will be used to judge.
- B1 hit@10 is plotted against the sum, and the three thresholds above are read off as sum cuts:
  the smallest sum at which the curve falls below 0.95, below 0.80, below 0.50.
- Those three integers are **frozen into this document with their date**, and the calibration set is
  retired. Every gold question's band is then its sum against the frozen cuts — computed before it is
  run, never adjusted after.

If the curve never falls below 0.50 even at a sum of 15, that is a finding and not a failure: it says
this corpus cannot be made hard enough for plain RAG to break, and the honest report is that routing
has no room to pay here. The corpus would then need to grow before the question can be asked.

### What the pilot already says about where the break is

The pilot is not a calibration set — it is 23 questions, and they are the ones being reported on — but
B1 ran on all of them and their sums are known, so the shape of the curve is not a mystery:

| sum | 0 | 2 | 4 | 5 | 6 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 hit@10 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 |
| n | 1 | 6 | 4 | 1 | 1 | 2 | 2 | 2 | 1 | 3 |

**Plain RAG does not break anywhere below a sum of 12, and at 12 it is still at 0.67.** On this
evidence the severe cut is at 13 or above, or it does not exist in this corpus — and the pilot's
hardest question was a 12, so nothing has yet been asked at the sums where a break could live.

The corpus has the headroom, barely. C+D+E is a property of the document, and a question adds A+B
(0–6), so the reachable sum of a question is `CDE + 6`:

| CDE | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| documents | 7 | 46 | 98 | 138 | 152 | 126 | 82 | 29 | 17 | 5 |

- **51 documents** (7.3%) can carry a question at sum ≥ 13
- **22** (3.1%) at sum ≥ 14
- **5** (0.7%) at sum ≥ 15

So the calibration set has to be deliberately top-heavy: the interesting region is 11–15, and it is
where the corpus is thinnest. It gets **at least 8 questions at each of 13, 14 and 15** — which uses
most of those 51 documents and every one of the five at CDE 9 — and thinner coverage below 11, where
the pilot has already shown the curve is flat at 1.00. Reaching those sums means A=3 and B=3 on every
one of them: fully paraphrased, and spanning two areas. They will not occur naturally and must be
written to hit the mark.

If the curve still refuses to drop below 0.50 at a sum of 15, that is the answer to the study's core
question on this corpus, and DIFFICULTY.md records it as such rather than moving a threshold to
produce a severe band.

**Frozen cuts:** _not yet calibrated — the calibration run has not been made. Until it is, the
provisional cuts 0–2 / 3–5 / 6–9 / 10–15 stand, and every result carrying them is marked provisional._

**The composition is recorded, not just the band.** A severe question is stored as `A3 B2 C1 D3 E1`,
so a failure can be read against which factor was extreme. This is the cause-splitting asked for in
the discussion, at a finer grain than covered/uncovered.

### Not a band: unanswerable

Questions with **no answer in the corpus** are a separate category, not the top of the scale. The
correct behaviour is to say so, and they exist to measure false absence (F4) — the failure only an
arm with a routing table can commit. Counting them as "severe" would mix a system that failed to find
something with a system that correctly reported nothing to find.

---

## The gold set this implies

- **At least 15 questions per band**, by design rather than by luck. A band that fills up by accident
  is a band whose questions were chosen after the fact.
- Plus unanswerable questions as a separate group.
- Each question carries: `A_true`, `D_true`, `needs: any | all`, the five factor levels, the band, and
  the stratum of its answer document (the *why* label, which is now secondary to difficulty).
- Level A3 and B3 questions must be **written deliberately**. They do not occur naturally in a corpus
  whose questions and documents share an author.

---

## Threats to the scale itself

1. **D and E share a model with the thing being measured.** A document the retriever's embedding finds
   crowded is scored crowded, so the scale is partly a description of that embedding. Three of the
   five factors are model-free and C alone is fully structural; the report gives results by factor so
   a reader can see how much of an effect rests on D and E.
2. **The cuts are this corpus's quartiles, and now this corpus's retriever too.** A corpus with a
   different shape would produce different bands from the same documents; so would a stronger
   baseline retriever, which would push every cut upward. The cuts are recorded with their date, their
   model and the calibration run that produced them, so a later run can say whether it is comparing
   like with like. A reader who wants a corpus-independent reading should use the factor sum, which is
   reported alongside the band for every question.
3. **The band boundary is fitted, so B1 near a boundary is partly fitted noise.** The calibration set
   is disjoint from the gold set, which stops a boundary from chasing a reported question, but ~60
   questions still place each cut with real uncertainty. The report gives results by factor sum as
   well as by band, so no conclusion has to rest on one integer.
4. **A and B are assigned when the question is written**, by the same hand that wrote the corpus.
   The human validation below is the check on that, and it is the only check there is.

## Validation

The scale is structural and the claim is that it tracks how hard a person would find the question.
That claim is checked, not assumed.

Forty questions spanning all four bands are rated 1–4 by the operator, blind to the computed band.
This is a check on the **sum** — that the five factors track human-perceived difficulty at all — and
it is independent of where the cuts fall, so it can be run before the calibration set exists.
Agreement is reported as Spearman's ρ against the computed sum and as weighted kappa against the band.

The operator rates them because the corpus was written by the assistant; a scale and a corpus from one
hand is not a check. **If agreement is poor, the factors or the cuts are revised — before the gold set
is written**, and the revision is recorded here with its date and reason.

---

## What this replaces

The strata S1–S4 were the original independent variable: whether an area's frozen description covers a
document. They are **no longer the axis**. Coverage is one cause of difficulty among several, and a
design that made it the only one could not represent a question that is hard because it is phrased
differently, or because forty documents resemble the answer.

The strata remain as a **secondary label** on every document, and they answer a different question:
*why* was this hard, and *whose fault* is a miss — a description that never named the subject, or one
that did while the router still missed it. `eval/PREREGISTRATION.md` §4 keeps them in that role.
