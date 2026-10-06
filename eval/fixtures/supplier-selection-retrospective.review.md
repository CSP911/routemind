# `supplier-selection-retrospective` — for review, before any number exists

**Status: unscored.** No `.results.md` beside this file and no run record in `eval/runs/`. That is
deliberate and it is the point of the arrangement GovKM asked for on PR #1:

> Please proceed with the variant unscored and include the map beside it. When it lands, I'll review
> the fixture, authority assumptions, expected operative state, historical/distractor classification,
> and expected behavior of each arm before any result is generated.

So everything below is written down *first*. Once it is agreed the fixture is scored once, and
nothing on this page is edited afterwards. If a prediction here is wrong, it stays on the page wrong.

Three files, and which is which matters:

| File | What it is |
|---|---|
| `supplier-selection-retrospective.yaml` | the documents, and `truth:` — the answer sheet, scorer only |
| `supplier-selection-retrospective.map.yaml` | the routing text — **the system under test**, not ground truth |
| this file | the claims being frozen |

`supplier-selection-silent` stays beside it untouched as the control.

---

## 1. What was asked for, and where it is

| GovKM's requirement | Where |
|---|---|
| a later document, newer but non-authoritative | `z-supplier-e-performance-review`, 2025-12-08, newest of the five |
| it truthfully refers to the earlier supplier | it is entirely about Supplier E, and every line about that period is true |
| it has no authority to change current state | it registers nothing — and, deliberately, does not say so either (§2) |
| ask the current-state question again | questions 1-3, unchanged from the silent fixture |
| the map beside it | `supplier-selection-retrospective.map.yaml`, frozen |
| unscored until reviewed | no results file exists |

One thing was added that was not asked for: **question 4**, which asks for the review by name. The
requirement said a continuity-qualified system should reach Supplier F *"while retaining the
retrospective as valid historical evidence"*. Without a question that needs the review, a system
could pass 1-3 by learning to demote anything that looks retrospective, and the run would call that a
success. Question 4 is what makes that failure visible in the same run. If it is unwanted, it is one
block to delete and the other three are unaffected.

## 2. The one design decision worth arguing with

**The review does not announce its own non-authority.** It carries no sentence like "this changes no
registration" and names no successor.

That is a choice, and it is the whole reason the variant exists. GovKM's first fixture was solved by
the reranker at 1.000 because the July decision said *"This replaces the approval of Supplier A"* —
the relationship was in the prose, and semantic machinery can read prose. Letting the review declare
itself non-authoritative would repeat that exact mistake with the sign reversed: the trap would be
*readable* rather than *reconstructed*, and a reranker would clear it for the same reason it cleared
F5. The only cues left are tense and date — "was the registered source … from 17 February 2025",
"while it was in force" — which is what a real performance review actually offers.

The cost is that the fixture is now hard for a reason that is partly about what we declined to write.
If that reads as stacking the deck, this is the paragraph to attack.

## 3. Authority assumptions

Stated plainly, because they are assumptions and not facts about anyone's real back office:

1. **Only a registration decision registers.** `z-supplier-e-approved` and `z-supplier-f-approved`
   are the only two documents with authority over who the source is. The other three record events
   or review periods.
2. **Later authorised decision wins.** Supplier F's 1 September registration governs from that date.
   Nothing revokes it within the fixture's window.
3. **Recency is not authority.** The newest document in the fixture is the one with no authority at
   all. This is the inversion the fixture exists to test.
4. **Validity is not authority.** All five documents are valid records; `truth.states` marks four
   `active`. Being active and being operative are different properties, and the fixture is built on
   that gap.
5. **The map is written by someone who knows.** The continuity statement lives in the routing text,
   not in the corpus. Whether that is a fair thing to assume is the open question in §7.

`truth.states` keeps the contract's three values — `active` · `superseded` · `withdrawn`. GovKM
proposed splitting into withdrawn / superseded / expired / stale and we agreed on PR #1 not to widen
the vocabulary until this fixture has run cleanly. Nothing here depends on that split.

## 4. Expected operative state, per question

| # | Question | Operative | Why that one |
|---|---|---|---|
| 1 | Which supplier is currently approved for Z? | `z-supplier-f-approved` | the registration in force |
| 2 | Can I place a new order for Z with Supplier E? | `z-supplier-f-approved` | E was replaced 1 Sep 2025 |
| 3 | What delivery window applies to a Z order placed today? | `z-supplier-f-approved` | twelve working days, September terms |
| 4 | How did Supplier E perform on delivery while it held Z? | `z-supplier-e-performance-review` | the only record of that period |

Question 4 runs the other way on purpose: the document that is a distractor in 1-3 is the answer in 4.

## 5. Distractor classification

| Document | Date | Class | Why it is dangerous |
|---|---|---|---|
| `z-supplier-f-approved` | 2025-09-01 | **operative** (1-3) | — |
| `z-supplier-e-approved` | 2025-02-17 | **superseded registration** | near-identical wording to the operative one; pure relevance cannot separate them |
| `z-supplier-e-performance-review` | 2025-12-08 | **newer non-authoritative** | newest of all five, names Supplier E throughout, and is the answer to question 4 |
| `z-annual-sourcing-note-2025` | 2025-11-10 | **neutral history** | second-newest; mentions both registrations without preferring either |
| `z-inspection-rejects-batch` | 2025-05-29 | **event** | says outright it changes no registration; carried from the silent fixture as a constant |

The three failure modes GovKM named map onto the middle rows: recency → the review, relevance →
the February registration, authority → neither, reach September.

## 6. Expected behaviour of each arm

Pre-registered. **n=4, one run each.** `0.250` means "one question of four". No interval attaches to
any figure here and none will be quoted as if one did.

| arm | found | operative | reasoning |
|---|---|---|---|
| `rag` | 1.000 | **0.250** | every document is retrievable; 1-3 fall to the February registration or the review, 4 lands correctly because the review is both newest and the only on-topic document |
| `rag+rerank` | 1.000 | **0.250** | no supersession sentence to read this time. The reranker may reorder within the top-k without changing a verdict, exactly as it did on the silent fixture |
| `routing` | 1.000 | **1.000** | the walk reads the map, which says which registration is in force and which records are history |

Two things about that table that are not predictions:

- **`rag+rerank` may come out worse than `rag`, not equal.** The review is newest *and* densely
  on-topic, so a reranker has a reason to lift it for "which supplier is currently approved". If it
  does, that is a more interesting result than the tie and it is not being predicted away here.
- **The `routing` arm does not exist yet.** `eval/fixtures/score.py` implements `rag` and
  `rag+rerank` only. It has to be built before this fixture can be scored, and building a scoring
  arm after writing the expectation is the thing this whole unscored arrangement is designed to keep
  honest. The expectation above is frozen now, in this file, before that code is written.

## 7. What is still open, and where I would rather be told I am wrong

1. **Is the map a fair place to put the continuity statement?** The routing arm's 1.000 above is not
   a claim that the system inferred anything. It is a claim that a person wrote one sentence and the
   walk obeyed it. That is a real property — it is why `stale-old` held at 15/15 on the 700-question
   corpus — but it is a different property from deriving currency from authority and time, which is
   what §3.5 assumes away. `docs/AGE.md` states the same boundary from the other side: AGE gives the
   walk two git-derived times and is explicitly not a supersession record.
2. **Is a December performance review of a supplier replaced in September realistic?** It is written
   as a procurement-review-file document. If a back office would not produce one, the fixture is
   measuring something that does not occur.
3. **Is question 4 worth having?** Argued for in §1; deletable without touching the rest.
4. **Does the neutral 2025-11-10 note still earn its place** now that there is a sharper newer
   document? It is carried over so the variant differs from the silent fixture by exactly one
   document, but it may now be noise.

---

**Nothing here has been run.** Every number in §6 is a prediction written before the scoring code for
one of the three arms exists.
