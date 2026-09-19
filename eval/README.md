# The study

**How useful is human intervention in RAG, and where does it stop paying for itself?**

The intervention is realised as a routing layer upstream of retrieval: a human-written table that
splits a corpus into areas, describes each in one sentence, and arranges documents in a tree. An
agent reads the table and chooses where to retrieve. Every other place a person could intervene —
chunking, document quality, relevance feedback — is out of scope, and the report says so.

The frame is **difficulty × routing**: four bands of question difficulty, each run with the routing
layer and without it. The answer is how the gap between those two columns changes as difficulty
rises, which is a more useful thing than whether routing wins on average.

**Severe means where plain RAG breaks** — B1 hit@10 below 0.50 — rather than a large number on an
invented scale. That place has now been found, and it is not where the difficulty scale expected:
what decides whether a retriever finds an answer is **how many rivals the answer has**, not how
strangely the question is worded. A corpus built on that principle measures **hit@10 0.03**, against
**0.99** on the same documents asked in the index's own vocabulary. See
**[COLLAPSE.md](COLLAPSE.md)**, and [DIFFICULTY.md](DIFFICULTY.md) rev. 6 for what it overturned.

## The documents

| | |
|---|---|
| [PREREGISTRATION.md](PREREGISTRATION.md) | the design, fixed before any arm runs — arms, failure definitions, sub-questions, statistics, open parameters, threats |
| **[COLLAPSE.md](COLLAPSE.md)** | the collapse threshold, what `hit@10` and `recall@20` mean, and the corpus built to cross it |
| [DIFFICULTY.md](DIFFICULTY.md) | the difficulty scale — five factors, and rev. 6 on why four of them did nothing |
| [CORPUS.md](CORPUS.md) | what the corpus is, how it was built, what was checked, what it cannot support |
| [gold/](gold/) | the answer key — questions, where their answers are, and how each is graded |
| [fixtures/](fixtures/) | continuity fixtures — a failure routing accuracy cannot see, contributed from outside |

## Where it stands

| | |
|---|---|
| Corpus | **done** — 700 documents, 5 areas, validated |
| Difficulty factors | **done** — C, D, E per document in `bench/factors.csv` |
| Preconditions | P1 done (no near-duplicate descriptions, max 0.533). P2 waits on the gold set |
| Gold set | **pilot done** — 23 questions, 7/5/5/6 across the bands. The full set is blocked on the labeller question |
| Arms | **pilot run** — three arms (B1 no routing · A3 one decision · A1 the agent walking the tree) over 23 questions |
| Parameters | fixed by the pilot except the labeller: k=10, 2 areas per hop, **no hop budget**, router `claude-opus-5`, reranker `gpt-5` |
| Band cuts | threshold fixed at **B1 hit@10 < 0.50**. The calibration set is cancelled — the five-factor sum does not predict B1 |
| Collapse dataset | **built and measured** — 340 documents in 5 qualifier families, 640 questions. B1 **0.03** indirect against **1.00** direct. Replicated across 5 families, 5 corpus sizes and 2 embedding models |
| | **2 of the 5 families are not usable yet** — `accrual` and `overtime` are 96% and 81% incumbent documents in the top ten, so their misses are not evidence. See COLLAPSE.md §6 |
| Routing on it | **not yet run.** Checking the harness found three defects that would have voided the result — `READ` returned no text to the agent, its OpenAI path could not make a request, and child order came from the filesystem. All fixed; a 3-question walk now works end to end |

## Before anything runs

Six parameters in [PREREGISTRATION.md](PREREGISTRATION.md) §9 are open, and the document is frozen
once they are fixed: `k`, areas per hop, hop budget, the `needs` default, the router model, and who
labels ground truth. Five are fixed; the labeller is not. The band cuts are a seventh, and they are
fixed by measurement rather than by choice — the calibration run, not the discussion. After that the gold set is written against the finished corpus — never
alongside it — and the difficulty scale is validated against forty human ratings before a question
is graded by it.

## The order it has to happen in

Three documents, and keeping them apart is what stops a result being explained after the fact.

1. **Pre-registration** — written before. Claims, metrics, decision rules.
2. **Run log** — written during. Raw, complete, including the runs that failed.
3. **Report** — written after, from those two only. A metric that is not in the frozen
   pre-registration does not enter it.

Two things already follow that order rather than claim it: the corpus strata were fixed before any
document was generated, so no label was chosen after seeing what it labelled; and the difficulty
thresholds were measured and written down before a single question was graded against them.
