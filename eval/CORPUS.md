# The corpus — what it is and how it was built

The document set the study runs against. It is generated, gitignored, and rebuildable; this page is
the record of what it is, so a result can be read against the material that produced it.

**Measured 2026-09-18.** Numbers here come from `bench/factors.py`, `bench/coverage.py` and the
manifest, not from intent.

---

## What it is

| | |
|---|---|
| Files | **817** — 700 generated documents · 38 section pages · 79 original |
| Areas | 5, frozen: approval · attendance · expense · payroll · procurement |
| Body text | median 1,130 characters · ~232,000 tokens in total |
| Tree depth | 0 · 5 area representatives, 1 · 268, 2 · 278, 3 · 76, 4 · 70, 5 · 120 |
| Kinds | rule 143 · table 135 · case 125 · topic 120 · procedure 111 · deadline 59 · role 56 · form 47 · system 21 |
| Clusters | 69 subject clusters across the five areas |

Per area, against what was there before growth:

| | before (2026-09-12) | now | growth |
|---|---|---|---|
| expense | 19 | 302 | ×16 |
| attendance | 19 | 210 | ×11 |
| payroll | 14 | 140 | ×10 |
| approval | 13 | 110 | ×8 |
| procurement | 14 | 55 | ×4 |
| **total** | **79** | **817** | **×10** |

Growth is deliberately uneven. A real document set does not grow evenly, and the point of the study
is what happens when one sentence has to cover three hundred documents.

---

## The frozen rows

Five sentences, one per area, in the representative's `use_when`. **They were written on 2026-09-12,
before any of this, and are not touched.** Freezing them is the study's central condition: a test
that rewrites the rows alongside the corpus measures a table nobody would actually maintain.

Concretely, `expense`:

> what to do with a receipt · whether the corporate card may be used here · how much a business trip
> pays · the entertainment cap · the card was lost

Five clauses, now covering 302 documents.

**Provenance matters here.** The five sentences were not written by the assistant that generated the
documents — `git log` places them in `a78a263`, two days before this work began. Everything below hop
0 (section pages, document one-liners) *was* written during generation, and is therefore not
independent. What that costs is in §Limitations.

---

## How a document was made

`bench/spec.yaml` → `bench/generate.py` → `bench/corpus/`, resumable from `bench/manifest.json`.

1. **The spec came first.** 69 clusters, each with a subject, the ground it covers, a count, and a
   stratum with a written reason. Nothing was generated until the spec was fixed, so no document's
   label was chosen after seeing the document.
2. **Documents were generated per cluster, eight at a time.** Each call was given every existing
   document in that area (id and one-liner) and **every figure already established in it**, with
   instructions not to contradict them. Batches of eight because a single call for twenty-four
   documents arrives truncated.
3. **Written as documents, not as retrieval targets.** Markdown, a table where there are rates, bold
   on the one trap a reader would otherwise fall into, and a closing line pointing at a neighbouring
   subject — matching the 79 that were already there.
4. **Section pages were added afterwards** (`bench/restructure.py`), one per cluster, so no parent
   has more than 25 children and the tree has depth to route down.

### What was checked

| | Result |
|---|---|
| Contradictions between batches | 90 figure-contexts examined, **0 conflicts** |
| Duplication within a cluster | 2 of 2,896 pairs above 0.5 Jaccard, both the corpus's own rule → table → worked-example pattern |
| Validation | `validate ok: True` — ids, kinds, parents, the derived table, the children-per-parent budget |
| Redundancy | the 5 closest same-cluster pairs were cut, bringing the set to exactly 700 |

---

## Strata — why a document is or is not covered

Every generated document carries a label, fixed **before** generation, recording whether its area's
frozen sentence covers it. It lives in `bench/manifest.json` and **never in the document**: the
frontmatter is part of what gets embedded, and a corpus carrying `stratum: S4` in its own text would
let the retriever read the answer sheet.

| | n | Meaning |
|---|---|---|
| **S1** | 317 | a clause names this subject |
| **S2** | 198 | belongs to the area; no clause names it — budgets, subscriptions, month-end close |
| **S3** | 108 | straddles two areas; neither sentence claims it — allowances that ride on pay |
| **S4** | 77 | the company grew into it; no sentence anticipated it — travel insurance, personal data, equity |

The line between S2 and S4 is not coverage — neither is covered. It is whether the area was *always*
about it. Checking a supplier has always been part of registering one, so supplier due diligence is
S2; carbon reporting is a duty the company took on, so it is S4. One cluster was relabelled on that
principle after measuring, and it was the cluster sitting closest to its row of every S4.

**The strata are a secondary label.** They were the study's independent variable and are not any more:
coverage is one cause of difficulty among several. They answer *why* a question was hard and *whose
fault* a miss was — a sentence that never named the subject, or one that did while the router still
missed. `eval/DIFFICULTY.md` is the axis; this is the diagnosis.

---

## Difficulty material

`bench/factors.csv` carries C, D and E for all 700 documents. A and B are properties of a
(question, answer) pair and are fixed when the gold set is written.

```
C depth      0: 228   1: 245   2: 107   3: 120
D margin     0: 176   1: 171   2: 172   3: 181
E crowding   0: 116   1: 329   2: 201   3:  54

C+D+E   0:7  1:46  2:98  3:138  4:152  5:126  6:82  7:29  8:17  9:5
```

What each band can be built on, once a question adds A and B (0–6):

| | documents available |
|---|---|
| easy | 151 |
| moderate | 567 |
| hard | 700 |
| severe | 411 |

The gold set needs 15 per band. The tightest is 151.

### Ambiguity, which was not designed and is worth having

**252 of 700 documents (36%) sit nearest to an area description that is not their own**, and 99 have
a gap under 0.02 between the best and second-best — effectively a tie. None of this was planned. It
is the ambiguity this design moves out of the retriever and into the sentences, and it is the raw
material for the severe band.

---

## Limitations

1. **It is LLM-generated.** Regular, well-formed, and possibly easier for an LLM-backed retriever than
   real documents would be. The 79 originals are human-edited; comparing results on those against the
   700 is the only internal check available, and it is weak.
2. **Below hop 0, nothing is independent.** Section pages and document one-liners were written during
   generation. Only the five frozen sentences predate the corpus, so the study's staleness condition
   holds at hop 0 and not below it. This is a consequence of the build order, not a property of the
   material, and a corpus built to test deeper staleness would fix the intermediate advertisements
   before growing the documents beneath them.
3. **One domain, one fictional company, five areas.** A small partition.
4. **Questions and documents would share an author** unless the gold set is written against the
   finished corpus rather than alongside it, and labelled by someone else. That is an open parameter
   in `eval/PREREGISTRATION.md` §9, not a solved problem.
5. **Generation stopped 16 documents short of the spec** when the API credit ran out, and five more
   were cut as redundant. 700 against a planned 721. The distribution is unaffected; the shortfall
   falls in `procurement`, already the least-grown area by design.

---

## Rebuilding it

```sh
./bench/generate.py            # expands spec.yaml, resumable from the manifest
./bench/restructure.py         # section pages and the tree, idempotent
./bench/factors.py --csv       # C, D, E per document
./bench/coverage.py            # coverage per stratum
```

**The corpus is versioned, and it has to be.** The rule used to be "version the generator, not its
output", which is sound for `bench/crowd.py` — standard library only, same 352 documents every run,
so the generator genuinely is the artefact. It is not sound for `bench/generate.py`, which asks an
LLM to write the base corpus: run it twice and you get two different corpora. With the corpus
ignored, the fingerprint stamped on every run record was unreproducible by anyone, including us on a
fresh checkout, which quietly cost this study the property it claims. `bench/corpus/` and
`bench/corpus-hard/` are now tracked — 4.8MB of markdown. What stays ignored is what is *derived*
from them: embeddings, section indexes, probe results, logs.

The two manifests go with them. They are not derived either: they are what marks a document as a
*section*, a signpost this study added, walkable but kept out of the retrieval pool. Without them
every section page gets indexed and the fingerprint changes.

**How this was checked, and why it had to be.** The paragraph above was first written with the
corpus tracked and the manifests still ignored, advertising a command that did not run. Reading the
ignore file and reasoning about it is not a check. Cloning the repository into an empty directory
and running the command is:

```sh
git clone <this repo> /tmp/check && cd /tmp/check
BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/crowd.py fingerprint
#   1126 documents   sha256 a84ac6cf463a1a6d

BENCH_EXTRA_CORPUS=bench/corpus-hard BENCH_USE_WHEN=maintained ./bench/mapcheck.py   # R1-R5 pass
BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/crowd.py stats                          # 0/320, 0/320
```

A clean clone is the standing test for "is the dataset complete". Anything that only works in the
author's working directory is not in the dataset, whatever the ignore file says.
