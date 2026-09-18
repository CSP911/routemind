# Difficulty — how a question is graded, and why

The study's frame is **difficulty × routing**: four bands of how hard a question is to answer, each
run with the routing layer and without it. The core question — *how useful is human intervention in
RAG, and where does it stop paying* — is answered by how the gap between those two columns changes
as difficulty rises.

Difficulty is therefore the independent variable, and it has to be fixed **before** any question is
written or any arm is run, or the bands become a description of the results.

Two commitments shape everything below.

**Difficulty is computed from structure, then checked against people.** Not assigned by judgment and
not derived from how the system performs. A band defined by what the retriever fails at is a band
that cannot be used to measure the retriever.

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

The five levels are summed, 0–15.

| Band | Sum | What it means |
|---|---|---|
| **쉬움 / easy** | 0–2 | the question names the document in the document's own words, one obvious area, shallow, no rivals |
| **보통 / moderate** | 3–5 | one factor is genuinely hard, or several are mildly so |
| **어려움 / hard** | 6–9 | two or three factors working together |
| **극악 / severe** | 10–15 | paraphrased, spanning areas, deep, ambiguous and crowded at once |

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
2. **The cuts are this corpus's quartiles.** A corpus with a different shape would produce different
   bands from the same documents. The cuts are recorded with their date and their model so a later
   run can say whether it is comparing like with like.
3. **A and B are assigned when the question is written**, by the same hand that wrote the corpus.
   The human validation below is the check on that, and it is the only check there is.

## Validation

The scale is structural and the claim is that it tracks how hard a person would find the question.
That claim is checked, not assumed.

Forty questions spanning all four bands are rated 1–4 by the operator, blind to the computed band.
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
