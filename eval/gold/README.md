# Gold sets

A gold set is the answer key: questions, and where their answers are. Without one there is no way to
say whether a system that chose `expense` was right.

| | |
|---|---|
| `pilot.yaml` | 23 questions — a plumbing check, not a result |
| `pilot-graded.csv` | the same, with A measured and the band computed |
| `grade.py` | measures A from the text, reads C/D/E, computes the band |

## What an entry carries

```yaml
q:       "Nobody did any work on the Sunday while we were abroad. Who decides whether it counts, and does it still pay?"
A_true:  [expense, attendance]     # areas that contain an answer — what routing is scored against
D_true:  [overseas-trip-per-diem-attendance-role]   # documents that answer it — a set
needs:   all                       # `any`: one area suffices · `all`: incomplete without both
intent_A: 3                        # what the question was written to be
intent_B: 3
```

`D_true` is a set because the corpus deliberately holds a parent and its table — `retention` and
`retention-table` both answer how long a contract is kept. Scoring one as the only right answer
would measure the corpus's shape rather than the retrieval.

**A is measured, not trusted.** `grade.py` computes the fraction of the question's content tokens
that appear in the answer document and bands it per `eval/DIFFICULTY.md`. Where the measurement
disagrees with `intent_A`, the measurement wins and the intent stays as a record of what was
attempted. On the pilot it disagreed 12 times in 23.

## The pilot

Five per band was the target; the first pass produced 7 / 2 / 5 / 6, and a moderate row of two
questions says nothing. Three moderate questions were added on documents whose C+D+E is 4, giving
**7 / 5 / 5 / 6 across 23**. Choosing which questions fill a band is stratified sampling — the band
definition is frozen, and no question was moved on the strength of a result.

What the bands are made of, averaged:

| | A | B | C | D | E | n |
|---|---|---|---|---|---|---|
| easy | 0.1 | 0.0 | 0.1 | 1.0 | 0.4 | 7 |
| moderate | 0.0 | 0.2 | 1.0 | 2.0 | 0.8 | 5 |
| hard | 1.8 | 1.2 | 1.6 | 2.0 | 1.4 | 5 |
| severe | 2.3 | 2.7 | 1.3 | 2.2 | 2.7 | 6 |

A, B and E rise across the bands; D is flat after moderate; C is noisy. Worth watching when the full
set is written — a factor that does not separate is a factor carrying no weight.

## The vocabulary leak, measured

Across the 23 questions the share of question tokens present in the answer document is **median
0.56, max 1.00, and eight questions sit at or above 0.75** — near-quotations. Two are exactly 1.00.

`eval/DIFFICULTY.md` predicted this: a corpus and its questions written by the same hand drift into
shared vocabulary without anyone intending it. It is now a number rather than a caution, and it says
plainly that **A3 questions have to be written against the measurement**, not by trying to paraphrase
and hoping.

## What the pilot cannot do

- **It was written by the assistant that generated the corpus.** `A_true` is a first pass. The
  operator's judgment — *does any other area also answer this?* — has not been applied, and the
  labeller question is still open (`PREREGISTRATION.md` §9).
- 23 questions is a plumbing check. Claims of difference need on the order of 100.
- There are no unanswerable questions in it yet, so false absence (F4) cannot be measured from it.
