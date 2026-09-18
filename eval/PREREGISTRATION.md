# Pre-registration — human intervention in RAG, realised as a routing layer

**Status: DRAFT, 2026-09-18 (rev. 2, continuity added the same day).** This document is written *before* any arm is run. Once the open
parameters at the bottom are fixed it is frozen, and every later document in `eval/` is built from it.
A metric, arm or decision rule that is not in the frozen version does not enter the report.

Why the discipline: the strata below were chosen before the corpus was generated, and the failure
causes were labelled before any failure was observed. Keeping that order is the only thing that
stops a result from being explained after the fact. This file is that order, written down.

---

## 1. Research question

**How useful is human intervention in RAG, and where does it stop paying for itself?**

### Operationalisation

The intervention is realised as a **routing layer upstream of retrieval**: a human-authored table
that partitions the corpus into areas, describes each area in one sentence, and arranges documents in
a hierarchy. An agent reads the table and chooses where to retrieve.

Other places a person could intervene in RAG — chunking, document quality, metadata, relevance
feedback — are **out of scope**. The claim is about this intervention point; the question is broader
and the evidence is narrower, and the report says so.

The instance is RouteMind. The components are named generically — *partition*, *description*,
*hierarchy* — so that the study is about the idea and RouteMind is the case.

---

## 2. Preconditions — checked before measurement

| | What | Result |
|---|---|---|
| P1 | No two area descriptions are near-duplicates in embedding space. If they were, the router would be coin-flipping between them and routing accuracy would have a floor no model lifts | **Done.** Max pairwise cosine 0.533 (`use_when`), 0.484 (all fields). Nothing above 0.70. `bench/rows-check.py` |
| P2 | Share of gold questions whose answer needs two or more areas. A design with one description per area cannot claim what no description claims | Measured on the gold set once it exists |

---

## 3. Arms and ablations

Every arm sees the **same corpus, questions, embedding model, reranker and k**, and every question
passes through every arm (paired design).

The table is frozen for the whole study. Ablations change what is **exposed to the router**, not
what is in the repository.

### 3.1 Factorial: which part of the intervention works

| Arm | Partition | Description (`use_when`) | Hierarchy | What it isolates |
|---|---|---|---|---|
| A1 | yes | yes | yes | the full intervention |
| A2 | yes | **no** — area names only | yes | the sentence's contribution |
| A3 | yes | yes | **no** — flat | the tree's contribution |
| A4 | yes | no | no | the partition alone |

A2 and A3 are single-factor removals from A1, not a ladder. Their interaction (does the sentence only
pay when there is a hierarchy to descend?) falls out of the 2×2.

### 3.2 Floors: no intervention

| Arm | Retrieval | Why it is here |
|---|---|---|
| B1 | hybrid (BM25 + dense, RRF) + reranker, whole corpus | what a sceptic would build. donk8r |
| B2 | dense only, whole corpus | "the table is why this works" is not claimable without it. nitish-kmr |

Inside a chosen area, A-arms use **exactly B1's retrieval**. The only difference between A1 and B1 is
the routing layer.

"RAG vs RAG + human routing" is A1 vs B1. It is not run separately; it falls out of the factorial.

---

## 4. Corpus

`bench/corpus` — `examples/back-office` (79 documents, 5 areas, all with prose as of 2026-09-14)
grown to ~800. The five area rows are frozen at their 2026-09-14 text. New documents join existing
areas; no area is added, renamed or re-described.

### Strata — the independent variable

Every generated document is labelled at birth with whether its area's frozen description covers it.
The label lives in `bench/manifest.json`, **never in the document** — the frontmatter is embedded,
and a corpus carrying `stratum: S4` in its own text would let the retriever read the answer sheet.

| Stratum | Share | Meaning | If routing misses it |
|---|---|---|---|
| S1 | 50% | the description names this subject | a **routing-logic** failure |
| S2 | 25% | belongs to the area; no clause names it | a **content** failure — one line fixes it |
| S3 | 15% | straddles two areas; neither description claims it | content, and defensible |
| S4 | 10% | the company grew into it; no description anticipated it | content, at its worst |

Growth is deliberately uneven across areas (expense ×15, procurement ×5), because that is how a real
document set grows and it is what makes one sentence cover a hundred documents.

The 79 original documents are all S1 by construction: the descriptions were written for them.

### The continuous form of the same variable

Stratum is a categorical claim made at design time. It is checked by measuring, for every document,
the **embedding distance between the document and its area's description**. This gives the
"staleness" axis a continuous x, and it tests the labels: if S1 documents are not measurably closer to
their descriptions than S4 documents, the labelling is wrong and the report says so.

### Scale

The same arms run at **two corpus sizes: 79 and ~800.** "Nearly anything works at 80 documents"
(donk8r) is a claim this design can test directly.

State at time of writing: 358 of 717 generated (S1 202 · S2 82 · S3 42 · S4 32). Generation halted on
a dropped connection and resumes from the manifest.

---

## 5. Failure — defined

Ground truth per question: **A_true**, the set of areas that contain an answer; **D_true**, the set of
documents that answer it. D_true is a *set* because the ontology deliberately holds a parent and its
table (`retention` and `retention-table` both answer "how long is a contract kept").

The chain is: question → router picks areas **A_picked** → retrieval inside them → ranked list → answer.

| | Name | Definition | Caps what follows? |
|---|---|---|---|
| F1 | routing failure | A_true ∩ A_picked = ∅ | **yes** — the reranker can only order what it was handed |
| F1r | routing miss (recall) | some area of A_true not in A_picked | partial |
| F1p | routing waste (precision) | an area in A_picked with nothing in it | costs tokens, dilutes reranking |
| F2 | retrieval failure | routing hit, but no D_true document in the top-k inside the picked areas | |
| F3 | rank failure | a D_true document is returned, below k | |
| F4 | **false absence** | the system says there is no answer, and there is | |
| F5 | **stale answer** | routing hit, retrieval hit, the operative document is in the top-k — and the answer rests on a document it superseded | |

F1 is logged separately from F2 and F3 on every question (donk8r): a wrong hop 0 must not show up as a
retrieval miss, or the reranker gets tuned for a problem the table caused.

**F4 is asymmetric.** The B-arms cannot commit it — they have no absence to claim. Only an A-arm can,
because hop 0 asserts it is the whole world. Counting only "was the document found" would hide both the
design's most expensive failure and its reason for existing.

**F5 is orthogonal to all of the above.** A system can pass F1 through F3 perfectly and still be wrong,
because four true, relevant, findable documents describe four states of the same subject over time and
only one is current. This is not a retrieval failure; it is a failure to distinguish *found the
material* from *established which material is operative* — after a correction, a supersession, or a
moved responsibility. Raised by GovKM, 2026-09-18. Every arm can commit it, A and B alike.

### Cause of a routing miss

Recorded on every F1, from the stratum label — decided before the miss was observed:

- miss on an **S1** document → the description named it and the router still did not pick it →
  routing-logic failure, the expensive kind, and the one the study is most concerned with
- miss on **S2/S3/S4** → the description never said it → content failure, fixed by editing one line

### Not failures

- A question with no answer in the corpus. The correct behaviour is to say so; routing "failure" here
  is correct refusal. The gold set contains some of these **on purpose** — without them F4 has nothing
  to bite on and the cost of the intervention is measured on one side only.
- Retrieving a parent where the child was expected, or the reverse. D_true is a set.

---

## 6. Sub-questions, in order

### Stage 1 — router only. No generation, no LLM judge.

| | Question | Design |
|---|---|---|
| **Q1** | Which part of the intervention pays? | the 2×2 (§3.1) against both floors (§3.2). F1–F3 |
| **Q2** | Where does it stop paying? | the A1−B1 gap, sliced two ways: by **staleness** (stratum, and the continuous distance) and by **scale** (79 / 800) |
| **Q3** | When it fails, whose fault? | S1 misses vs non-S1 misses, counts and ratio. The router model is fixed and named; if a second model is affordable, S1 misses that survive a model change are the logic failures that are not one model's opinion |
| **Q4a** | The cost of intervention — iteration | **hops per answered question, median and p95.** An agentic router hides a stale table by iterating; hops should rise before accuracy falls. Requires an iterative router with a hop budget |
| **Q5a** | Currency — is the operative document *found* | on continuity fixtures (§7a): the operative document in the top-k, and its rank **against its distractors**. A reranker blind to dates has no reason to put July above March |

### Stage 2 — generation attached.

| | Question | Design |
|---|---|---|
| **Q4b** | The cost of intervention — false absence | F4 rate on answerable questions (the cost) and correct-refusal rate on unanswerable ones (the benefit). Same mechanism, both signs |
| **Q5b** | Currency — is the operative document *used* | F5: does the generated answer rest on the operative document or on one it superseded |

Q5 runs **first against `git tag baseline-pre-continuity`**, the implementation before any state, age
or supersession field exists — so the fixtures measure what the system was, and any continuity-aware
change is a delta from a preserved result rather than a test designed around the fix. The contributor
asked for exactly this, and it is the same discipline as the rest of this document.

In stage 1, F4 is estimated as *potential* false absence: questions where F1 occurred and hop 0 was in
a state that permits an absence claim (every link up).

---

## 7. Gold set

Not yet written. What this document fixes about it:

- Written **after** the corpus is complete, against the corpus — never alongside it. Corpus and
  questions by the same hand in the same pass would be written to match each other.
- Each question carries: `A_true`, `D_true`, `needs: any | all` (does one area suffice, or is the
  answer only complete with both — a trip settlement is attendance *and* expense; a retention period
  is approval *or* procurement), and its stratum inherited from D_true.
- Stratified so every stratum has enough questions to report on its own. Ten questions split by
  stratum share gives S4 one question, which is not a measurement.
- Includes unanswerable questions (§5).
- Questions are written the way people ask, not the way documents are written. A question lifted from
  a document's own sentences measures findability of that document, not routing.

**Independence.** The corpus was generated by the same assistant that would otherwise write the
questions and label A_true. That is circular. Resolution recorded here once decided (§9).

---

## 7a. Continuity fixtures

A second kind of input, contributed rather than derived from the corpus. One subject, several
documents about it over time, and the truth about which is operative now. The contract, a worked
example and a checker are in `eval/fixtures/`.

Two rules carry over from the strata: the documents are plain — dated the way a person would date
them, with no field that says "current" — and the truth never enters the corpus. A third is new: a
fixture's documents join an existing area, so routing to them is governed by that area's frozen
description like everything else.

What a fixture measures is Q5. It is scored on its own questions, not on the gold set's.

## 8. Statistics

- Paired design: every question through every arm. Differences are per-question, not per-arm means.
- Effect sizes with bootstrap confidence intervals over questions.
- **A pilot of ~20 questions is a plumbing check, not a result.** Claims of difference need on the
  order of 100+ questions. The report distinguishes the two.
- Per-stratum results are reported even where n is small, with n shown.

---

## 9. Open parameters — fixed before freezing

| | Parameter | Candidates |
|---|---|---|
| k | how many retrieved documents count as "found" | 5 or 10 |
| areas per hop | how many areas the router may pick at once | 1 · 2 · 3 |
| hop budget | maximum returns to hop 0 per question | 3 (the overlay design's own figure) |
| `needs` | default when a question spans areas | `any` unless marked `all` |
| router model | fixed and named; second model if affordable | — |
| labeller | who writes A_true — the operator, mechanical derivation from the manifest, or both | see §7 |

---

## 10. Explicitly excluded from this study

Product features proposed in the same discussion, deferred until measurement is done. Adding them
first would make two things vary at once.

- Policy-based routing (enforced overrides of the router's choice)
- Area weights, a floor under them, deliberate decay
- A drift monitor (sample an area, summarise it, diff against the human sentence). Note that Q2's
  continuous distance is the same instrument used as a measurement rather than a monitor.
- **Continuity fields on entities** — `state` (active · superseded · withdrawn), `age`, and a pointer
  to what an entity supersedes. Proposed in the same discussion. Deferred until Q5 has run against
  the baseline tag, for the reason given under Q5. One note for when they come: supersession in the
  fixtures is between *documents* (a July decision replaces a March one), so the fields belong on
  entities and surface in an area's table, not on the hop 0 rows.

---

## 11. Threats to validity — named now

1. **The corpus is LLM-generated.** Regular, well-formed, and possibly easier for an LLM-backed
   retriever than real documents. The 79 originals are human-edited; the report compares results on
   the 79 against the 800 for a hint of how much this matters. Real documents, if any become
   available, would be the honest check.
2. **Ground truth may not be independent of the corpus author.** §7, §9.
3. **One domain, one fictional company.** Five areas is a small partition.
4. **The router is one model.** Q3's "logic failure" is that model's failure unless a second confirms.
5. **Upkeep is not measured.** "Pays for itself" implies a cost of writing and maintaining the table,
   and nobody times it. Q3 is a proxy: a content failure costs one line, a logic failure costs a model.
   The report says proxy.

---

## 12. What exists

| | |
|---|---|
| `bench/spec.yaml` | 73 clusters, per area, per stratum, with `why` for each label |
| `bench/plan.json` | the counts (800 total, 50/25/15/10) |
| `bench/generate.py` | expands the spec; resumable from the manifest |
| `bench/manifest.json` | id → area, parent, stratum, cluster, pair |
| `bench/retrieve.py` | BM25 + dense (`text-embedding-3-large`) + RRF, embeddings cached |
| `bench/rerank.py` | LLM scoring, blind to areas |
| `bench/rows-check.py` | P1 |
| `bench/smoke.py` | retrieve + rerank end to end |
| `eval/fixtures/` | the continuity-fixture contract, one worked example, and `check.py` |
| `git tag baseline-pre-continuity` | the implementation Q5 is measured against first |

`bench/` is not versioned (generated, large). This file and everything else in `eval/` is.
