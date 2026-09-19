#!/usr/bin/env python3
"""A corpus extension built to break retrieval, and the questions that break it.

Everything measured so far says the 700-document corpus cannot be broken by wording:

    A=3   BM25 recall@20 0.13   dense recall@20 0.95   B1 hit@10 0.80

A full paraphrase destroys the keyword half and the embedding half shrugs. `confusable.py` says why:
the closest pair of documents in the whole corpus sits at cosine 0.911, and the median document's
nearest neighbour is around 0.78. Nothing in it is *nearly the same thing*, so the dense side always
has a clean winner to return.

**The corpus is the difficulty, and it was never built to be hard.** So this adds a part that is.

## Qualifier families

A family is one subject written N times, identical in structure, wording and intent, differing only
in the values of two qualifiers — a grade and a country band, a day type and an hour band. Inside a
family the documents mean nearly the same thing, so the embedding cannot separate them; the only
thing that can is the qualifier, and a paraphrased question does not contain the qualifier's words.

    A=3 alone       kills BM25. Dense survives, because the answer is the only document on its subject.
    family alone    dense cannot choose, but BM25 matches "grade 3" and "Band C" exactly and rescues it.
    A=3 x family    the paraphrase removes the strings BM25 needs and the family removes the
                    separation dense needs. **Both halves fail at once.**

That corner is the prediction. It is written here before the run, and the run either finds it or does
not.

## Why this is fair, and why routing should win it

Nothing here is a trick question. Every document states its own qualifiers plainly in its first line,
every question names the situation a person would actually be in, and exactly one document answers
each question. A human with the routing table in front of them answers every one of these in seconds,
because the table's rows carry the qualifiers — which is the entire claim the study is testing. A
corpus where retrieval fails and a person with a map does not is the corpus the question needs.

## Frozen corpus, separate extension

`bench/corpus/` stays at 700 documents. This writes to `bench/corpus-hard/`, and the arms read both
only when `BENCH_EXTRA_CORPUS` points at it. Results on 700 and on 780 are then two rows of the same
table rather than one number that quietly changed meaning.

## No model wrote any of this

Templates, not generation — which is not a compromise, it is the point. Two documents written by a
model differ in a hundred small ways that a retriever can latch onto; two documents from one template
differ in exactly the qualifier, which is the variable under study. It also costs nothing, which is
why it exists: both providers' balances ran out mid-session and this was still possible.

    ./bench/crowd.py write          the documents and the gold set
    ./bench/crowd.py stats          what was written, and how tight it should be
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "corpus-hard"
GOLD = ROOT.parent / "eval" / "gold" / "hard.yaml"
MANIFEST = ROOT / "crowd-manifest.json"

# Each family: the area it belongs to, the two qualifier axes, and the templates. `doc` is the
# document body; `direct` and `para` are the two questions, one in the document's vocabulary and one
# in a person's. The paraphrase deliberately keeps the *facts* that pick the row — a person knows
# their own grade and destination — and drops every policy term, because that is what a real question
# looks like and it is what removes BM25's grip.
FAMILIES = [
 dict(
  key="perdiem", area="expense", section="Overseas per-diem by grade and country band",
  a=("grade", [("1", "junior staff"), ("3", "a manager"), ("5", "a senior manager"),
               ("7", "a division head")]),
  b=("band", [("A", "Japan"), ("B", "Singapore"), ("C", "Indonesia"), ("D", "Bangladesh")]),
  name="Overseas per-diem — grade {a} in band {b}",
  one="The nightly lodging cap, meal allowance and receipt threshold for a grade {a} traveller in band {b}",
  doc="""# Overseas per-diem, grade {a}, band {b}

## Who this row covers
A traveller at **grade {a}** on an overseas trip to a **band {b}** destination ({bx}).

## The caps
| | |
|---|---|
| Lodging, per night | {lodge} |
| Meals, per day | {meal} |
| Receipt threshold | {receipt} |
| Incidentals, per day | {inc} |

Lodging above the cap needs written approval from the budget holder **before** the booking, not
after. Meals are paid at the flat daily figure and are not itemised. Any single item above the
receipt threshold needs the original receipt; below it the card statement line is enough.

## Overruns
A night above the lodging cap that was not approved in advance is settled at the cap, and the
difference is personal. An unavoidable overrun — a cancelled flight, a closed hotel — is claimed with
a short written statement and the evidence, and is decided by the budget holder.""",
  direct="What is the per-night lodging cap and the receipt threshold for a grade {a} traveller on a band {b} trip?",
  para="I'm {ax} and I'm being sent to {bx} next month — how much can I spend on a hotel each night before I need sign-off first, and above what amount do I have to keep the paper receipt?",
  vals=lambda ai, bi: dict(
    lodge=f"{120 + 30*ai + 40*(3-bi)} USD", meal=f"{40 + 10*ai + 15*(3-bi)} USD",
    receipt=f"{20 + 5*ai + 10*(3-bi)} USD", inc=f"{8 + 2*ai + 3*(3-bi)} USD")),

 dict(
  key="overtime", area="payroll", section="Overtime multipliers by day type and hour band",
  a=("day", [("weekday", "an ordinary Tuesday"), ("weekend", "a Saturday"),
             ("public holiday", "a public holiday"), ("night", "the middle of the night")]),
  b=("hours", [("first 2 hours", "about an hour and a half"), ("2 to 4 hours", "three hours"),
               ("4 to 8 hours", "six hours"), ("over 8 hours", "a solid ten hours")]),
  name="Overtime rate — {a} work, {b}",
  one="The multiplier, rounding rule and approval requirement for {b} of overtime on {a} work",
  doc="""# Overtime rate, {a} work, {b}

## Who this row covers
Hours worked beyond the standard day, classified as **{a}** work, in the **{b}** band.

## The rate
| | |
|---|---|
| Multiplier | {mult} |
| Rounding | {round} |
| Approval needed in advance | {appr} |
| Counts toward the monthly cap | {cap} |

The multiplier applies to the base hourly rate only. Allowances that are paid monthly are not part of
the base and are not multiplied.

## How it is recorded
Hours are entered against the day they were worked, not the day the work was requested. A shift that
crosses midnight is split at midnight and each part takes its own day's classification, which is the
single most common source of a corrected payslip.""",
  direct="What overtime multiplier applies to {a} work in the {b} band, and is advance approval required?",
  para="I ended up working {bx} on {ax} — what do I actually get paid for that time, and was I supposed to clear it with someone beforehand?",
  vals=lambda ai, bi: dict(
    mult=f"{1.5 + 0.25*ai + 0.1*bi:.2f}x", round=f"to the nearest {5 + 5*bi} minutes",
    appr="yes" if (ai + bi) >= 3 else "no", cap="yes" if bi >= 1 else "no")),

 dict(
  key="accrual", area="attendance", section="Leave accrual by employment type and tenure",
  a=("type", [("permanent", "on a permanent contract"), ("fixed-term", "on a two-year contract"),
              ("part-time", "working three days a week"), ("secondee", "seconded in from a partner firm")]),
  b=("tenure", [("under 1 year", "been here about eight months"), ("1 to 3 years", "been here two years"),
                ("3 to 7 years", "been here five years"), ("7 years or more", "been here nine years")]),
  name="Leave accrual — {a} staff, {b}",
  one="The monthly accrual rate, carry-over limit and notice period for {a} staff at {b} of service",
  doc="""# Leave accrual, {a} staff, {b}

## Who this row covers
Someone employed as **{a}** whose continuous service is **{b}**.

## The entitlement
| | |
|---|---|
| Accrues per month | {rate} days |
| Carry-over limit | {carry} days |
| Notice required | {notice} working days |
| Accrues during unpaid leave | {unpaid} |

Accrual is credited at the end of each completed month. A month in which any unpaid leave was taken
is credited only if this row says accrual continues.

## Carry-over
Days above the carry-over limit lapse at year end and are not paid out. The limit is checked on the
last working day of December against the balance on that date, not against the balance at the time a
booking was made.""",
  direct="How many days per month do {a} staff with {b} of service accrue, and what is their carry-over limit?",
  para="I'm {ax} and I've {bx} — how much time off am I building up each month, and how much of it can I still have in January if I don't use it?",
  vals=lambda ai, bi: dict(
    rate=f"{1.0 + 0.25*bi - 0.25*ai:.2f}", carry=f"{5 + 3*bi}", notice=f"{3 + ai}",
    unpaid="yes" if ai == 0 and bi >= 2 else "no")),

 dict(
  key="threshold", area="approval", section="Approval thresholds by category and amount band",
  a=("category", [("equipment", "a couple of laptops"), ("services", "a consultant's time"),
                  ("travel", "flights and hotels"), ("entertainment", "dinner with a client")]),
  b=("amount", [("under 1m KRW", "about 700,000 won"), ("1m to 5m KRW", "roughly 3 million won"),
                ("5m to 20m KRW", "around 12 million won"), ("over 20m KRW", "about 40 million won")]),
  name="Approval threshold — {a}, {b}",
  one="Who signs, how many quotes are needed, and how long it takes for {a} spend of {b}",
  doc="""# Approval threshold, {a}, {b}

## Who this row covers
A commitment to spend on **{a}** where the total is **{b}**.

## What is required
| | |
|---|---|
| Signs it off | {who} |
| Competing quotes | {quotes} |
| Draft required first | {draft} |
| Working days to expect | {days} |

The total is the whole commitment, not the first invoice. Splitting one commitment into parts to stay
under a threshold is the thing this table exists to prevent, and a split is judged by intent rather
than by timing.

## If it is urgent
An urgent case is escalated, not skipped. The same signature is required; what changes is that it is
sought directly rather than in the queue, and the reason is recorded with the request.""",
  direct="Who signs off {a} spend of {b}, and how many competing quotes are required?",
  para="We want to buy {ax} and it'll come to {bx} — whose signature do I need on that, and do I have to go and get other prices first?",
  vals=lambda ai, bi: dict(
    who=["the team lead", "the department head", "the division director", "the CFO"][bi],
    quotes=["none", "two", "three", "three plus a written comparison"][bi],
    draft="yes" if bi >= 2 or ai == 3 else "no", days=f"{2 + 3*bi}")),

 dict(
  key="diligence", area="procurement", section="Due-diligence depth by contract value and supplier origin",
  a=("origin", [("domestic", "a Korean company"), ("EU", "a German firm"),
                ("US", "an American vendor"), ("other overseas", "a supplier in Vietnam")]),
  b=("value", [("under 10m KRW", "a small one, maybe 8 million won"),
               ("10m to 100m KRW", "somewhere around 60 million won"),
               ("100m to 500m KRW", "roughly 300 million won"),
               ("over 500m KRW", "a big one, over 700 million won")]),
  name="Due diligence — {a} supplier, contract {b}",
  one="The checks, documents and review interval required for a {a} supplier on a contract of {b}",
  doc="""# Due diligence, {a} supplier, contract {b}

## Who this row covers
A new or renewing supplier registered as **{a}**, on a contract whose value is **{b}**.

## What is checked
| | |
|---|---|
| Financial statements | {fin} |
| Sanctions and ownership screen | {screen} |
| Site visit | {visit} |
| Re-review interval | {review} |

A check that cannot be completed does not block registration by itself; it is recorded as an
exception with a reason and an owner, and the exception expires on the re-review date whether or not
anything has changed.

## Renewals
A renewal is treated as a new registration if the value moves into a different band or the ownership
has changed. Otherwise the re-review interval governs and the previous file is carried forward.""",
  direct="For a {a} supplier on a contract of {b}, is a site visit required and how often is the file re-reviewed?",
  para="We're about to sign with {ax} and the contract is {bx} — do we have to go and see their premises, and how often does someone have to look at their file again after that?",
  vals=lambda ai, bi: dict(
    fin=["not required", "last year only", "last two years", "last three years, audited"][bi],
    screen="yes" if (ai > 0 or bi >= 1) else "basic",
    visit="yes" if bi >= 2 else "no",
    review=f"every {[36, 24, 12, 6][bi]} months")),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build():
    docs, questions, manifest = [], [], {}
    for fam in FAMILIES:
        akey, avals = fam["a"]; bkey, bvals = fam["b"]
        sec_id = f"sec-hard-{fam['key']}"
        manifest[sec_id] = {"id": sec_id, "area": fam["area"], "section": True,
                            "cluster": fam["section"], "family": fam["key"]}
        docs.append((fam["area"], sec_id, f"""---
id: {sec_id}
name: "{fam['section']}"
kind: section
one_liner: "One row per combination of {akey} and {bkey}; the row is the answer and the {akey} and {bkey} are how you find it"
parent: {fam['area']}
---
# {fam['section']}

Every row below states the same four things for a different combination of **{akey}** and
**{bkey}**. Nothing else distinguishes them, so read the two qualifiers first and open only the row
that matches.
"""))
        for ai, (a, ax) in enumerate(avals):
            for bi, (b, bx) in enumerate(bvals):
                v = fam["vals"](ai, bi)
                did = f"hard-{fam['key']}-{slug(a)}-{slug(b)}"
                fmt = dict(a=a, b=b, ax=ax, bx=bx, **v)
                body = fam["doc"].format(**fmt)
                name = fam["name"].format(**fmt)
                one = fam["one"].format(**fmt)
                docs.append((fam["area"], did, f"""---
id: {did}
name: "{name}"
kind: reference
one_liner: "{one}"
parent: {sec_id}
---
{body}
"""))
                manifest[did] = {"id": did, "area": fam["area"], "parent": sec_id,
                                 "cluster": fam["section"], "family": fam["key"],
                                 akey: a, bkey: b, "stratum": "S1"}
                questions.append({"id": f"h-{fam['key']}-{ai}{bi}-d", "q": fam["direct"].format(**fmt),
                                  "A_true": [fam["area"]], "D_true": [did], "needs": "any",
                                  "intent_A": 0, "intent_B": 0, "family": fam["key"], "lever": "family"})
                questions.append({"id": f"h-{fam['key']}-{ai}{bi}-p", "q": fam["para"].format(**fmt),
                                  "A_true": [fam["area"]], "D_true": [did], "needs": "any",
                                  "intent_A": 3, "intent_B": 0, "family": fam["key"],
                                  "lever": "family x paraphrase"})
    return docs, questions, manifest


def cmd_write(a):
    docs, questions, manifest = build()
    for area, did, text in docs:
        p = OUT / "regions" / area / f"{did}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    GOLD.parent.mkdir(parents=True, exist_ok=True)
    head = ("# Gold set — the hard extension.\n#\n"
            "# Generated by bench/crowd.py from templates, not written by hand and not written by a\n"
            "# model. Two questions per document: one in the document's own words and one in a\n"
            "# person's. Both have exactly one answer, and the answer is stated plainly in the\n"
            "# document — the difficulty is entirely in telling that document from its fifteen\n"
            "# siblings, which say the same thing about a different grade or a different band.\n#\n"
            "#   lever `family`              the sixteen siblings, asked in the document's words\n"
            "#   lever `family x paraphrase` the same, asked the way somebody would actually ask\n#\n"
            "# Regenerate rather than edit: ./bench/crowd.py write\n\nquestions:\n")
    lines = [head]
    for q in questions:
        lines.append(f"- id: {q['id']}\n  q: {json.dumps(q['q'], ensure_ascii=False)}\n"
                     f"  A_true: [{q['A_true'][0]}]\n  D_true: [{q['D_true'][0]}]\n"
                     f"  needs: {q['needs']}\n  intent_A: {q['intent_A']}\n  intent_B: {q['intent_B']}\n"
                     f"  family: {q['family']}\n  lever: {json.dumps(q['lever'])}\n")
    GOLD.write_text("\n".join(lines), encoding="utf-8")
    nd = sum(1 for _, i, _ in docs if not manifest[i].get("section"))
    print(f"  {nd} documents + {len(FAMILIES)} sections -> {OUT.relative_to(ROOT.parent)}")
    print(f"  {len(questions)} questions -> {GOLD.relative_to(ROOT.parent)}")


def cmd_stats(a):
    docs, questions, manifest = build()
    import collections
    from retrieve import tokens
    texts = {i: t.split("---", 2)[-1] for _, i, t in docs if not manifest[i].get("section")}
    print(f"\n  {len(texts)} documents in {len(FAMILIES)} families\n")
    print("   family      n   mean jaccard within family   vs the rest of the extension")
    for fam in FAMILIES:
        mem = [i for i in texts if manifest[i].get("family") == fam["key"]]
        tk = {i: set(tokens(texts[i])) for i in mem}
        pairs = [len(tk[x] & tk[y]) / len(tk[x] | tk[y])
                 for n, x in enumerate(mem) for y in mem[n + 1:]]
        other = [i for i in texts if manifest[i].get("family") != fam["key"]]
        to = {i: set(tokens(texts[i])) for i in other[:40]}
        cross = [len(tk[x] & to[y]) / len(tk[x] | to[y]) for x in mem[:6] for y in to]
        print(f"   {fam['key']:<10} {len(mem):>3}          {sum(pairs)/len(pairs):.3f}"
              f"                    {sum(cross)/len(cross):.3f}")
    print("\n  A family whose members share most of their words is a family the embedding will place")
    print("  on top of each other. The qualifier is the only thing that separates them, and the")
    print("  paraphrased question is the one that does not contain it.\n")


def cmd_bm25(a):
    """Half the prediction, for free. BM25 needs no API and no credit.

    The claim is that `family x paraphrase` removes the exact strings the keyword half depends on.
    That half can be checked now, over the whole extended corpus, with nothing bought. If the direct
    questions score near 1.00 and the paraphrases collapse, the lever works on BM25 and only the
    dense half is still an open question.
    """
    import os, collections
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    sys.path.insert(0, str(ROOT))
    import probe
    from retrieve import BM25
    import yaml as _y
    texts, area, raw = probe.corpus_texts()
    bm = BM25(texts)
    qs = _y.safe_load(GOLD.read_text(encoding="utf-8"))["questions"]
    by = collections.defaultdict(lambda: [0, 0, 0, []])
    for q in qs:
        ranked = [i for _, i in bm.search(q["q"])]
        d = q["D_true"][0]
        r = ranked.index(d) + 1 if d in ranked else 999
        b = by[q["lever"]]
        b[0] += r <= 10; b[1] += r <= 20; b[2] += 1; b[3].append(r)
    import statistics
    print(f"\n  BM25 alone over {len(texts)} documents · {len(qs)} questions\n")
    print("    lever                     n    hit@10   hit@20   median rank")
    for lever, (h10, h20, n, rk) in sorted(by.items()):
        print(f"    {lever:<24} {n:>3}    {h10/n:5.2f}    {h20/n:5.2f}    "
              f"{statistics.median(rk):>6.0f}")
    print("\n    999 means the answer is not in BM25's top 50 at all.")
    print("    The dense half cannot be checked without embedding the new documents, which needs")
    print("    an API balance. Everything is in place for it: ./bench/probe.py-style run over")
    print("    eval/gold/hard.yaml with BENCH_EXTRA_CORPUS set.\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("write"); sub.add_parser("stats"); sub.add_parser("bm25")
    a = ap.parse_args()
    {"write": cmd_write, "stats": cmd_stats, "bm25": cmd_bm25}[a.cmd](a)
