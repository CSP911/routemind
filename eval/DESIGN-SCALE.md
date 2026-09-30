# Measuring indicator 2 — where a correct map stops working

Written before the experiment runs, in the same discipline as `PREREGISTRATION.md`: the hypothesis,
the variable, the prediction and the falsifier are fixed here, and a result that is not described in
advance does not enter the report.

Chapter 1 establishes that a **wrong** map fails, and how. This is the other failure: a map that is
correct at every level and stops working anyway. The study currently has one corpus, one partition
and one point on this axis, and a limit cannot be seen from one point.

---

## 1. The hypothesis

A routing table asks an agent to choose between **descriptions**, not documents. Each description is
one sentence. One sentence is a fixed-size summary of a set that is not fixed size.

Today, in this corpus:

| | |
|---|---|
| rows at hop 0 | 5 |
| documents behind one of those sentences | 125 – 372 |
| rows at hop 1 | 15 – 23 |

> **H.** A correct map fails when a description can no longer separate what sits beneath it. The
> failure is not in accuracy first — it is in **cost**: the walk wanders before it gets lost.

## 2. What varies, and what does not

The obvious experiment is to grow the corpus. It is the wrong one, because growing the corpus also
changes what the map must say, and then two things move at once — which is indicator 1 wearing
indicator 2's clothes.

**So the corpus does not move. The map does.**

| held fixed | varied |
|---|---|
| all 1,126 documents, byte for byte | the partition: how many areas, and what each sentence covers |
| all 700 questions and their answer keys | |
| hop 0 policy (`maintained`), models, `k`, candidate count | |

### 2.1 The partitions

Merging, not splitting. Splitting requires writing new descriptions by hand — which is the very
labour this study does not measure, and would smuggle authoring quality into a structural result.
Merging composes descriptions from ones already written and already checked.

| arm | areas | documents per description | how the description is made |
|---|---|---|---|
| **P5** | 5 | 125 – 372 | today's map, unchanged |
| **P3** | 3 | ~250 – 500 | two pairs merged, sentences concatenated |
| **P2** | 2 | ~560 | as above |
| **P1** | 1 | 1,126 | one description covering everything |

Every one of these is **correct**: a merged description truthfully names everything beneath it.
`mapcheck` R1–R6 must pass on each before it is walked, and that is the gate — if a partition cannot
pass, it is a wrong map and belongs to indicator 1.

### 2.2 The property that makes this clean

The corpus fingerprint is a hash over `name + one_liner + body` for every document. **A document's
parent is not part of it.** Re-parenting therefore leaves the fingerprint unchanged:

    all four partitions share fingerprint a84ac6cf463a1a6d

Which means the retrieval arms are untouched and directly comparable across every partition, and any
movement belongs to the map alone. This is a stronger isolation than the corpus-growth design can
offer at any price.

### 2.3 What P1 also settles

P1 is a description with no discriminating power at hop 0 — every question routes to the same place.
It is the control this study has wanted since the beginning, and it separates two claims that have
been running together:

- *the gain is the partition* — P1 should collapse toward retrieval
- *the gain is having a tree to walk and documents to read at all* — P1 should hold

Either result is informative and the study currently cannot tell them apart.

## 3. Measurement

Two quantities, kept apart, because the hypothesis says one moves before the other.

| | what | why |
|---|---|---|
| **leading** | calls per question — median, p95, max | the walk wandering. Expected to move first |
| **outcome** | hit rate by lever | the walk getting lost. Expected to move later or not at all |

**Stratified n=100 per partition**, drawn from the 700 by lever in the census proportions, with the
same 100 ids across all four so the comparison is paired. P5's numbers come from the existing census
restricted to those ids — no re-run, and it doubles as a check that the subset reproduces the whole.

    300 new walks (P3, P2, P1) · ~$48 at the measured $0.16/walk · ~4 hours at 2 parallel

Full 700 is run only where n=100 shows movement, and only on the partition that shows it.

## 4. The prediction, registered now

1. **Calls per question rises monotonically P5 → P3 → P2 → P1.** The agent faces fewer, broader
   descriptions and pays for it in table opens below hop 0.
2. **Hit rate holds at P3 and P2.** A merged-but-accurate description still routes correctly; the
   work moves down a level.
3. **P1 separates the two claims.** If hit holds near 0.99 at P1, the gain was never the partition —
   it was reading documents in a structure at all, and the partition is a cost optimisation. If hit
   falls toward the retrieval arms, the partition is the mechanism.
4. **`indirect` moves first and `direct` last.** A question already carrying the row's vocabulary
   does not need the description; a question in a person's words does.

Prediction 3 is the one worth being wrong about publicly. **If P1 holds, Chapter 3's framing is
wrong** — the study has been attributing to the table what belongs to the walk.

## 5. What would falsify H

- **Calls flat across all four partitions.** The map's shape does not cost anything, and the
  hypothesis that a description has a carrying capacity is unsupported at this corpus size.
- **Hit falls before calls rise.** The walk gets lost without wandering first, which breaks the
  leading-indicator claim and means cost cannot be used as an early warning.
- **P1 matches P5 on both.** No structural signal at all at 1,126 documents — in which case the
  experiment has located the limit as *above* this corpus, and the corpus-growth design becomes
  necessary after all.

## 6. What this still will not measure

**The carrying capacity in documents.** This varies documents-per-description from 225 to 1,126 by
merging, which is a factor of five and stops at the size of the corpus. If the limit is at 10,000
documents behind one sentence, this design cannot reach it and will report "no limit found", which
is not the same as "no limit".

**Authoring quality.** Merged descriptions are mechanical concatenations. A person writing one
sentence for 1,126 documents would write something better than five sentences stapled together, and
that difference is part of what the intervention *is*. P1 therefore measures a floor, not the
intervention's best case at that shape.

**Depth, and versions per subject.** Two other axes on which a correct map might fail — a tree too
deep to walk cheaply, and a revision legend with so many versions it becomes the haystack. Neither is
varied here. The versions axis is the cheaper of the two to add later: `crowd.py` generates them
programmatically, so 3 → 6 versions costs no model calls at all.

---

## Appendix — where indicator 2 currently stands

From the 700-question census, the only signal visible today:

| | median | p75 | p90 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| calls per question | 7 | 8 | 9 | 10 | 15 | 28 |

Eight walks in 700 (1.1%) took fifteen calls or more; **all eight hit.** The median is flat at 6–7
across all five families. A tail of successful long walks is what "working, with effort" looks like.
It is consistent with being some distance before a limit, and it is not evidence of where the limit
is. That is the gap this design exists to close.
