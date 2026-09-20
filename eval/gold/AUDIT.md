# Desk audit of the answer keys

**2026-09-20.** What `./bench/audit.py` can decide, what it cannot, and the judgements made on what
it handed over. Written because four of the six runs discarded this week died of a wrong answer key,
every one of them discovered by watching an arm fail — which is the expensive way round and also the
misleading one: a walk that wanders looks like a routing failure whether the map is bad or the
question has no answer as written.

## What the script decides, and what it hands over

| | |
|---|---|
| **reachable** | the gold document hangs off an area, so a walk can arrive at it — decided |
| **in range** | a retriever can see it at all — decided |
| **named** | the question shares a word with what the gold document is called — decided |
| **unique** | no *other* document answers as well — **shortlisted, then read** |

The last one cannot be mechanised here, and the reason is worth stating: on a hard question the top
three are non-gold by definition, so "a rival outranks the gold" flags every hard question and
therefore flags nothing. The script's job is to make the list short and put the evidence beside it.

**A rival that is another version of the same subject is not a flag.** Three versions of one rule are
supposed to look alike and outrank each other; that is what the time axis is made of.

## The judgement on `hard.yaml` — by pattern, not one by one

320 indirect questions share one shape, so they were judged as five patterns with sampled instances
rather than read individually. Saying otherwise would be a claim about reading I did not do.

| family | what outranks the gold | does it answer? |
|---|---|---|
| perdiem | `domestic-trip-*`, `overseas-trip-exchange-rate-receipt-tagging` | **no** — the questions name a foreign city, and rate-tagging is not a cap |
| accrual | `january-destruction-list`, `nontaxable-allowance-review`, `annual-health-check-rule` | **no** — document retention, a payroll allowance check, health checks |
| threshold | `card-po-quote-validity-deadline`, another family's amount legend | **no** — how long a quote stays valid is not who signs or how many quotes |
| diligence | `card-po-supplier-request-procedure`, `procurement-overview` | **no** — getting a PO issued, and an area index |
| overtime | `overtime-request-procedure`, `unrequested-overtime-case` | **partly — and it was fixed** |

### The one that failed

The overtime questions asked *"…what do I actually get paid for that time, **and did it need clearing
with anyone beforehand**"*. The second half is answered by the frozen corpus: `overtime-request-procedure`
is how to clear hours in advance, and `unrequested-overtime-case` is what happens when you did not.
A question half of which another document answers is half a mislabelled question.

The row's `Approval needed in advance` field is why it was written that way, and that field is exactly
the one the incumbent already covers. The ask now uses **rounding**, which the old rate table does not
carry — it lists categories and premiums and nothing about minutes — so the two no longer overlap.

## `hard-temporal.yaml`

34 of 60 clean; the rest are flagged for low BM25 rank with same-subject versions above them, which is
the design. Spot-read: `overseas-rates` does state band B lodging at 180 USD, and `hard-perdiem-v2`
covers 2024-07-01 onwards, so a question dated March 2023 has exactly one answer and the date is what
picks it. No unrelated document answers these.

## What this does not certify

The uniqueness judgement above is mine, and I generated the corpus. That is the circularity
`PREREGISTRATION.md` §11 names and it is not resolved by being careful. The check that would resolve
it is a second reader, which is the first thing `DATASETS.md` asks a contributor for.

What it does do is separate the two questions that kept getting confused: **is this question
answerable and uniquely so** — decided here, before any arm runs — and **did the arm find it**, which
is what the arms are for.

## One key defect, found three times, fixed for the family — 2026-09-20

A key widened after seeing a result is the easiest way to manufacture a hit, so this is written out
in full: what was wrong, how it was checked, and how far the fix was applied.

**The defect.** `leave-accrual` is the prose page for the oldest leave rule — "the table is on the
page below" — and `accrual-rule` is that table, carrying the identical three tiers. The gold set
named only the prose page. `mapcheck` R5 lists **both** as supersession targets for the accrual
subject, which is the corpus itself saying they are two faces of one answer.

**How it surfaced.** Three `routing+overlay` walks answered correctly and cited the table:
`t-accrual-01` (15 days for two years, pre-2024-07-01), `t-accrual-09` (the boundary question, same
figure, correctly reasoning that 29 June is two days before the change), `t-accrual-11` (both
versions, and it declined to annualise a monthly rate rather than invent one). Each scored a
mechanical miss. The `routing` arm passed all three only because it happened to name every document
it opened — an accident, not a difference in skill, and the accident is what hid the defect.

**How far the fix goes.** `D_alt: {leave-accrual: [accrual-rule]}` is on **all six** questions keyed
on `leave-accrual` — `t-accrual-01, -02, -03, -09, -11, -12` — not only the three that tripped on
it. Applying a correction to the family rather than to the failures is what keeps it a correction.
Then `./bench/walkscore.py rescore` re-ran every walk of **both** arms against the new keys from
their kept verbatim reports. Nothing was re-walked; no report was altered; only `hit` recomputed.

**A bug in the fix, caught by the fix not working.** `D_alt` was first a flat list, added to what the
walk named. That is right for `needs: any` by accident and wrong for `needs: all`: `t-accrual-11`
named the substitute *and* the second required document and still failed, because the substitute
satisfied nothing. It is now a per-entry mapping — an alternative stands in for the one key entry it
is equivalent to. The first `rescore` reported "0 changed" when one walk should have flipped, which
is the only reason the bug was found.

Nothing was changed about the corpus or the questions. This is the fourth time this campaign that a
"routing failure" turned out to be a defect in the answer key.

## Two walks stalled on a tool that never answers — 2026-09-20

`h-threshold-023-d` and `t-accrual-11` (both `routing+overlay`) stopped mid-walk having decided to
wait for a background-monitor notification, and wrote no report. Neither was a routing failure and
neither is data: the agent simply stopped. Both were relaunched from the same generated prompt.

The prompt now says every call is synchronous and forbids background, monitor and waiting tools, so
the next agent cannot make the same choice. Worth noting because a stall looks like nothing at all
in a campaign file — the only sign was a report file that was never written, which is why
`walkscore record` is fed from the file rather than from whatever the agent replied.
