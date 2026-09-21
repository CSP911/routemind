# The worst case: what walking costs when the map stops helping

    fingerprint a84ac6cf463a1a6d · tree measured directly · tokens from the 5 cost-instrumented walks

Chapter 2 priced routing at 6.7 calls and $0.12–$0.28 a question. **That is the price when the map
works.** This is the other end of the same axis, and it is not a larger number of the same kind.

## The tree, counted

| | |
|---|---|
| nodes in the tree | 1,212 |
| of those, tables (something opens beneath them) | **128** |
| of those, documents with a body | **1,212** |
| documents in the retrieval pool | 1,126 |
| **a full traversal** | **1,340 calls** |

## What a full traversal would cost

Measured across the five instrumented walks, a call carries **2,041 tokens of new content** on
average — the table or document it returns, added to a conversation that is otherwise cached.

    1,340 calls × 2,041 tokens  ≈  2.7M tokens of new content

**No context holds that.** The walk runner stops an agent at 40 turns, which is about 82k tokens —
and that ceiling is not a configuration choice that could be raised to 1,340. It is roughly what a
session can hold.

So the honest statement of the worst case is not that traversal is expensive:

> **A walk can see about 3% of this tree. Its median walk sees 0.52%.**

| | calls | share of the tree |
|---|---|---|
| median walk | 7 | 0.52% |
| the longest walk in 700 | 28 | 2.1% |
| the runner's ceiling | 40 | **3.0%** |
| full traversal | 1,340 | 100% — unreachable |

## Which changes what the map is for

The intuitive reading of Chapter 2 is that the routing table buys efficiency: 1,340 calls compressed
into 7, a factor of 190. That reading is wrong, and the arithmetic above is why.

**The table is not a speed-up over traversal, because traversal is not an option.** An agent cannot
fall back to reading everything; it runs out of session first and returns whatever it has. The
table's job is to make the 0.5% a walk can afford to look at be the right 0.5%.

This is the sharpest difference between the two arms, and it was not visible from the accuracy
table:

| | when its mechanism stops helping |
|---|---|
| retrieval | **degrades** — the answer slides down the ranking, and a longer candidate list recovers some of it |
| routing | **does not degrade** — the walk runs out of budget having seen 3% of the corpus, and reports whatever it reached |

Retrieval has a dial. `k=10` becomes `k=50` and `recall@20 ≈ p × min(1, 20/N)` predicts what that
buys. Routing's equivalent dial is the turn ceiling, and it does not scale the same way: doubling it
to 80 turns takes a walk from 3.0% of the tree to 6.0%, at double the cost, on a corpus where the
answer is one document in 1,126.

## What this says about indicator 2

Chapter 1 asked where a correct map stops working. This gives the shape of the answer even though it
does not give the point:

**As a map stops discriminating, the walk degrades toward traversal — and traversal is a cliff, not
a slope.** There is no regime in which a routing agent is "slow but still right", because the budget
that makes it fast is the same budget that makes it terminate at all.

That also explains why the failure found in Chapter 1 looked the way it did. A walk misled by one
sentence does not wander and recover. It goes somewhere plausible, finds a document that answers the
question it thinks it was asked, and stops — having spent six calls out of a possible forty, and
having no mechanism that would make it spend the other thirty-four.

## Limits

- **1,340 is a ceiling, not an observation.** No agent was made to attempt it; the number is counted
  from the tree and priced with measured per-call tokens.
- **2,041 tokens per call is a mean of five walks**, and varies with whether the call returns a table
  row or a document body.
- **The 40-turn ceiling is this runner's setting.** It is defended above as roughly a session's
  capacity rather than an arbitrary limit, but it was not tuned or tested at other values.
- **This says nothing about where the map stops discriminating** — only what happens after it does.
