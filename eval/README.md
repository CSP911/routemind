# The study

**How useful is human intervention in RAG, and where does it stop paying for itself?**

The intervention is realised as a routing layer upstream of retrieval: a human-written table that
splits a corpus into areas, describes each in one sentence, and arranges documents in a tree. An
agent reads the table and chooses where to retrieve. Every other place a person could intervene —
chunking, document quality, relevance feedback — is out of scope, and the report says so.

The frame is **difficulty × routing**: four bands of question difficulty, each run with the routing
layer and without it. The answer is how the gap between those two columns changes as difficulty
rises, which is a more useful thing than whether routing wins on average.

## The documents

| | |
|---|---|
| [PREREGISTRATION.md](PREREGISTRATION.md) | the design, fixed before any arm runs — arms, failure definitions, sub-questions, statistics, open parameters, threats |
| [DIFFICULTY.md](DIFFICULTY.md) | the difficulty scale — five factors, four levels each, where the thresholds came from |
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
| Parameters | fixed by the pilot except the labeller: k=10, 2 areas per hop, 3 returns, router `claude-opus-5`, reranker `gpt-5` |

## Before anything runs

Six parameters in [PREREGISTRATION.md](PREREGISTRATION.md) §9 are open, and the document is frozen
once they are fixed: `k`, areas per hop, hop budget, the `needs` default, the router model, and who
labels ground truth. After that the gold set is written against the finished corpus — never
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
