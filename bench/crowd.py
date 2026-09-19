#!/usr/bin/env python3
"""A corpus part built so that plain RAG provably cannot answer it, and routing provably can.

## What the measurements forced

Three rounds said the same thing from different angles. A full paraphrase destroys BM25 (recall@20
0.13) and the dense half shrugs (0.95). The closest pair of documents in the frozen 700 sits at
cosine 0.911, so nothing in it is *nearly the same thing* as anything else. And the first attempt
here — five families of sixteen near-identical documents — did not break B1 either: measured
hit@10 1.00 on both its levers.

The sixteen is why, and it is arithmetic rather than bad luck. **If N documents are equally
plausible for a query and the retriever returns k, the answer arrives with probability about k/N.**
At N=16 and k=20 every sibling fits in the candidate list, the reranker reads the qualifiers off
them, and it picks correctly every time. Nothing about the wording can change that.

    N = 16   recall@20 = 1.00      measured
    N = 40   about 0.50
    N = 64   about 0.31
    N = 128  about 0.16

So the axis is not how strange the question is. **It is how many rivals the answer has**, and it is
calculable before anything is run — which is what makes a threshold reachable on purpose rather than
hoped for. It also explains the crowding factor's flat result: E was the right idea at the wrong
scale, counting neighbours in a corpus whose largest cluster was 27.

## The design

Each family is one subject written N times over three axes, plus **legends**.

    rows       64 documents. Each states its three qualifiers in the system's vocabulary —
               "grade 3", "band C", "6 to 10 nights" — and nothing else distinguishes them.
    legends    3 documents mapping a person's vocabulary onto the system's: which cities are in
               which band, which job titles are which grade, how the night bands are counted.

A question comes in two forms against the same row:

    direct     asks in the system's vocabulary. A control: everything should answer this.
    indirect   asks the way a person would — "I'm a team manager going to Jakarta for four nights."
               No row contains "manager" or "Jakarta". Only the legends do.

The indirect question therefore needs a **lookup and then a fetch**: read the legend, learn the row,
open the row. Single-shot top-k retrieval cannot do that at any k, because the legend is not the
answer and the answer is one of sixty-four documents the query cannot distinguish.

## Why this is fair, which matters more than whether it is hard

**The legends are ordinary retrievable documents.** They sit in the corpus and in the tree, and every
arm can retrieve them. There is no information the routing arm has and the baseline does not. The
question is answerable, has exactly one answer, and a person handed the whole corpus answers it in a
minute.

What differs is the *shape of the access*, and that is the entire claim under test: the walker takes
two steps and the single-shot retriever takes one. If routing wins here it wins for a reason that can
be stated in a sentence, and if it loses on a corpus built this favourably to it, that is worth
knowing sooner than later.

## The routing arm has to be able to use it, and that was checked

`./bench/crowd.py routecheck` reports what the agent actually sees: the section's table lists the
three legends and the N rows, each with a one-liner, so the walk is legend-then-row and the table
fits in a prompt. A family large enough to break retrieval is not automatically a family an agent
can walk, and the two constraints pull in opposite directions — that check is where the tension is
made visible rather than assumed away.

## Templates, not generation

Two model-written documents differ in a hundred incidental ways a retriever can latch onto; two from
one template differ in exactly the variable under study. It is also free, which is why the first
version of this file exists at all.

    ./bench/crowd.py write [--grid 4x4x4]     the documents, legends and gold set
    ./bench/crowd.py stats                    what was written
    ./bench/crowd.py bm25                     half the prediction, free
    ./bench/crowd.py routecheck               can the walker use it
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "corpus-hard"
GOLD = ROOT.parent / "eval" / "gold" / "hard.yaml"
MANIFEST = ROOT / "crowd-manifest.json"

# Each axis: (system value, the way a person says it). The person's form appears in no row — only in
# that axis's legend — which is what makes the indirect question a lookup rather than a match.
FAMILIES = [
 dict(key="perdiem", area="expense", subject="Overseas per-diem",
  unit="the nightly lodging cap, the daily meal allowance and the receipt threshold",
  axes=[
   ("grade", "grade {v}", [("1", "a junior analyst"), ("3", "a team manager"),
                           ("5", "a department head"), ("7", "a managing director"),
                           ("2", "a senior analyst"), ("4", "a senior manager"),
                           ("6", "a division head"), ("8", "an executive officer")],
    "Which grade a job title belongs to"),
   ("band", "band {v}", [("A", "Tokyo"), ("B", "Singapore"), ("C", "Jakarta"), ("D", "Dhaka"),
                         ("E", "Zurich"), ("F", "Lisbon"), ("G", "Nairobi"), ("H", "La Paz")],
    "Which country band a destination city falls in"),
   ("stay", "{v}", [("1 to 2 nights", "one night"), ("3 to 5 nights", "four nights"),
                    ("6 to 10 nights", "eight nights"), ("over 10 nights", "three weeks"),
                    ("a day trip", "no overnight at all"), ("11 to 20 nights", "a fortnight"),
                    ("21 to 30 nights", "a full month"), ("over 30 nights", "two months")],
    "How a trip length is banded")],
  fields=lambda i, x: [("Lodging, per night", f"{95 + 4*x} USD"),
                       ("Meals, per day", f"{38 + 9*i[0] + 14*i[1] + 5*i[2]} USD"),
                       ("Receipt threshold", f"{18 + 4*i[0] + 9*i[1] + 3*i[2]} USD"),
                       ("Incidentals, per day", f"{7 + 2*i[0] + 3*i[1] + i[2]} USD")],
  ask="what can I put on a hotel each night, and above what amount do I have to keep the receipt"),

 dict(key="overtime", area="payroll", subject="Overtime rate",
  unit="the multiplier, the rounding rule and whether approval was needed first",
  axes=[
   ("day", "{v} work", [("weekday", "an ordinary Tuesday"), ("weekend", "a Saturday"),
                        ("public holiday", "Liberation Day"), ("night", "two in the morning"),
                        ("weekday evening", "a Wednesday after dinner"),
                        ("sunday", "a Sunday"), ("holiday night", "New Year's Day, very late"),
                        ("rest day", "my rostered day off")],
    "Which day type a date or time counts as"),
   ("hours", "{v}", [("first 2 hours", "about ninety minutes"), ("2 to 4 hours", "three hours"),
                     ("4 to 8 hours", "six hours"), ("over 8 hours", "eleven hours"),
                     ("under 1 hour", "twenty minutes"), ("8 to 12 hours", "ten hours"),
                     ("12 to 16 hours", "fourteen hours"), ("over 16 hours", "a full day and a half")],
    "How overtime hours are banded"),
   ("place", "{v}", [("on site", "at my desk"), ("at a client", "out at a client's office"),
                     ("on standby", "on standby at home"), ("remote", "from home"),
                     ("travelling", "on a train between offices"), ("overseas", "in the Osaka office"),
                     ("on call", "carrying the pager"), ("in transit", "waiting at the airport")],
    "Which work-location category applies")],
  fields=lambda i, x: [("Multiplier", f"{1.20 + 0.03*x:.2f}x"),
                       ("Rounding", f"to the nearest {5 + 5*(i[1] % 4)} minutes"),
                       ("Approval needed in advance", "yes" if (i[0] + i[1]) >= 3 else "no"),
                       ("Counts toward the monthly cap", "yes" if i[1] >= 1 else "no")],
  ask="what do I actually get paid for that time, and did it need clearing with anyone beforehand"),

 dict(key="accrual", area="attendance", subject="Leave accrual",
  unit="the monthly accrual rate, the carry-over limit and the notice required",
  axes=[
   ("type", "{v} staff", [("permanent", "on the regular payroll"), ("fixed-term", "on a two-year contract"),
                          ("part-time", "in three days a week"), ("secondee", "here from our partner firm"),
                          ("probationary", "still in my first three months"),
                          ("rehired", "back after leaving for a while"),
                          ("dual-hatted", "splitting my time between two teams"),
                          ("agency", "placed through an agency")],
    "Which employment type a working arrangement counts as"),
   ("tenure", "{v}", [("under 1 year", "been here eight months"), ("1 to 3 years", "been here two years"),
                      ("3 to 7 years", "been here five years"), ("7 years or more", "been here nine years"),
                      ("under 3 months", "been here since March"), ("10 years or more", "been here twelve years"),
                      ("15 years or more", "been here since the merger"),
                      ("20 years or more", "been here my whole career")],
    "How continuous service is banded"),
   ("site", "{v}", [("head office", "at the Seoul office"), ("branch", "at the Busan branch"),
                    ("overseas", "in the Singapore entity"), ("home-based", "fully from home"),
                    ("plant", "on the factory site"), ("client-embedded", "sitting with the client"),
                    ("regional hub", "at the Osaka hub"), ("mobile", "on the road most weeks")],
    "Which site category a working location belongs to")],
  fields=lambda i, x: [("Accrues per month, days", f"{0.40 + 0.02*x:.2f}"),
                       ("Carry-over limit, days", f"{4 + 3*i[1] + i[2]}"),
                       ("Notice required, working days", f"{2 + i[0] + (i[2] % 3)}"),
                       ("Accrues during unpaid leave", "yes" if i[0] == 0 and i[1] >= 2 else "no")],
  ask="how much time off am I building up each month, and how much can I still be holding in January"),

 dict(key="threshold", area="approval", subject="Approval threshold",
  unit="who signs it, how many competing quotes are needed and how long it takes",
  axes=[
   ("category", "{v}", [("equipment", "a couple of laptops"), ("services", "a consultant's time"),
                        ("travel", "flights and hotels"), ("entertainment", "dinner with a client"),
                        ("software", "a year of some SaaS thing"), ("facilities", "rewiring a meeting room"),
                        ("marketing", "a booth at a trade show"), ("training", "a course for the team")],
    "Which spend category a purchase falls under"),
   ("amount", "{v}", [("under 1m KRW", "about 700,000 won"), ("1m to 5m KRW", "roughly 3 million won"),
                      ("5m to 20m KRW", "around 12 million won"), ("over 20m KRW", "about 40 million won"),
                      ("under 100k KRW", "sixty thousand won"), ("20m to 50m KRW", "35 million won"),
                      ("50m to 200m KRW", "120 million won"), ("over 200m KRW", "half a billion won")],
    "How a commitment's value is banded"),
   ("term", "{v}", [("one-off", "just the once"), ("annual", "renewing every year"),
                    ("multi-year", "locked in for three years"), ("open-ended", "until we cancel it"),
                    ("monthly", "billed every month"), ("per-use", "only when we call on them"),
                    ("pilot", "a trial for now"), ("framework", "a standing arrangement we draw down on")],
    "Which commitment term a purchase has")],
  fields=lambda i, x: [("Delegation limit", f"{200 + 25*x} thousand KRW"),
                       ("Signs it off", ["the team lead", "the department head", "the division director",
                                         "the CFO", "the board"][min(4, (i[1] + i[2]) // 2)]),
                       ("Competing quotes", ["none", "two", "three", "three and a written comparison"][min(3, i[1])]),
                       ("Working days to expect", f"{2 + 3*i[1] + i[2]}")],
  ask="whose signature do I need, and do I have to get other prices first"),

 dict(key="diligence", area="procurement", subject="Supplier due diligence",
  unit="the checks required, the documents to collect and the re-review interval",
  axes=[
   ("origin", "{v}", [("domestic", "a company in Daejeon"), ("EU", "a firm in Stuttgart"),
                      ("US", "a vendor in Austin"), ("other overseas", "a supplier in Da Nang"),
                      ("UK", "a firm in Leeds"), ("Japan", "a company in Nagoya"),
                      ("China", "a manufacturer in Shenzhen"), ("sanctioned-adjacent", "a trader in Istanbul")],
    "Which origin category a supplier's location belongs to"),
   ("value", "{v}", [("under 10m KRW", "eight million won"), ("10m to 100m KRW", "sixty million won"),
                     ("100m to 500m KRW", "three hundred million won"), ("over 500m KRW", "seven hundred million won"),
                     ("under 1m KRW", "under a million won"), ("500m to 1b KRW", "eight hundred million won"),
                     ("1b to 5b KRW", "two billion won"), ("over 5b KRW", "six billion won")],
    "How a contract's value is banded"),
   ("goods", "{v}", [("commodity", "just office consumables"), ("bespoke", "something made to our spec"),
                     ("professional services", "people's time"), ("software", "a licence"),
                     ("logistics", "shipping and warehousing"), ("construction", "a fit-out"),
                     ("data processing", "they'd hold our customer records"),
                     ("regulated", "something the regulator has to see")],
    "Which supply category a purchase belongs to")],
  fields=lambda i, x: [("Screening score required", f"{30 + x}"),
                       ("Financial statements", ["not required", "last year", "last two years",
                                                 "last three years, audited"][min(3, i[1])]),
                       ("Site visit", "yes" if (i[1] >= 2 or i[2] >= 5) else "no"),
                       ("Re-review interval", f"every {[36, 24, 12, 6][min(3, i[1])]} months")],
  ask="do we have to go and see their premises, and how often does their file get looked at again"),
]


def slug(s): return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


# The rows are indexed by **codes**, not by descriptive phrases, and this is the load-bearing detail
# rather than a cosmetic one. A row that says "on standby" can be matched by a question that says
# "on standby at home"; a row that says "P3" cannot be matched by anything a person would type. The
# first version leaked a discriminating word on 102 of 320 indirect questions this way — the third
# axis of three families was written in English, so BM25 and the reranker could pick the row without
# ever consulting a legend, and the lookup the design exists to force was optional.
#
# It is also what real systems do: tariff codes, pay bands, risk tiers. The legend is the only place
# the mapping is written down, which is exactly the claim being tested.
CODE = {"grade": "G", "band": "B", "stay": "S", "day": "D", "hours": "H", "place": "P",
        "type": "E", "tenure": "T", "site": "L", "category": "C", "amount": "V", "term": "M",
        "origin": "O", "value": "W", "goods": "K"}


def code_for(axis, n):
    return f"{axis} {CODE[axis]}{n + 1}"


def build(grid):
    docs, questions, manifest, support = [], [], {}, {}
    for fam in FAMILIES:
        sec = f"sec-hard-{fam['key']}"
        # `tpl` is dropped: every axis is now rendered as "<axis> <code>". The descriptive phrase
        # survives only on the legend's left-hand side, which is where a person's words belong.
        axes = [(name, vals[:n], legend) for (name, tpl, vals, legend), n in zip(fam["axes"], grid)]
        manifest[sec] = {"id": sec, "area": fam["area"], "section": True,
                         "cluster": fam["subject"], "family": fam["key"], "parent": fam["area"]}
        n_rows = grid[0] * grid[1] * grid[2]
        docs.append((fam["area"], sec, f"""---
id: {sec}
name: "{fam['subject']} — by {', '.join(a[0] for a in axes)}"
kind: section
one_liner: "{n_rows} rows indexed by {' and '.join(a[0] + ' code' for a in axes)}, plus the three legends that turn a person's words into those codes"
parent: {fam['area']}
---
# {fam['subject']}

Every row states {fam['unit']} for one combination of **{'**, **'.join(a[0] for a in axes)}**.
Nothing else separates them, so settle the three qualifiers first and open only the row that matches.

The three legends below are how you settle them: they map what a person knows — a job title, a city,
a length of time — onto the values the rows are indexed by.
"""))

        # The legends. Retrievable documents like any other: no arm is handed anything another arm
        # cannot also retrieve, and the difference is only how many steps it may take.
        for name, vals, legend in axes:
            lid = f"hard-{fam['key']}-legend-{slug(name)}"
            rows = "\n".join(f"| {p} | {code_for(name, n)} |" for n, (v, p) in enumerate(vals))
            docs.append((fam["area"], lid, f"""---
id: {lid}
name: "{fam['subject']} — {legend.lower()}"
kind: reference
one_liner: "{legend}. Read this before choosing a row; the rows are indexed by the right-hand column"
parent: {sec}
---
# {legend}

This table is the only place the mapping is written down. The {fam['subject'].lower()} rows are
indexed by the value in the right-hand column and do not repeat what is in the left.

| What you have | What the rows call it |
|---|---|
{rows}

If what you have is not listed, take the nearest entry above it and record the choice with the claim.
"""))
            manifest[lid] = {"id": lid, "area": fam["area"], "parent": sec, "legend": name,
                             "cluster": fam["subject"], "family": fam["key"], "stratum": "S1"}
            support.setdefault(fam["key"], []).append(lid)

        for ia, (va, pa) in enumerate(axes[0][1]):
            for ib, (vb, pb) in enumerate(axes[1][1]):
                for ic, (vc, pc) in enumerate(axes[2][1]):
                    sysv = [code_for(axes[j][0], n) for j, n in enumerate((ia, ib, ic))]
                    # "row" sorts after "legend", which is how the legends come to sit at the top
                    # of the section's table. A person writing this table would put them there, and
                    # the agent only ever sees the child list — never the section's own prose.
                    did = f"hard-{fam['key']}-row-{slug(sysv[0])}-{slug(sysv[1])}-{slug(sysv[2])}"
                    # The first figure is a function of the whole triple and of nothing else, so no
                    # two rows in a family can carry the same answer. They could before: 128 of 320
                    # rows were textually identical in their figures to a sibling, because some
                    # families computed every field from only two of their three axes. A retriever
                    # that returned the twin was then scored as missing while having supplied the
                    # correct answer, which is a mislabelled question rather than a hard one.
                    flat = (ia * len(axes[1][1]) + ib) * len(axes[2][1]) + ic
                    tbl = "\n".join(f"| {k} | {v}" + " |" for k, v in fam["fields"]((ia, ib, ic), flat))
                    docs.append((fam["area"], did, f"""---
id: {did}
name: "{fam['subject']} — {', '.join(sysv)}"
kind: reference
one_liner: "{fam['unit'].capitalize()} for {', '.join(sysv)}"
parent: {sec}
---
# {fam['subject']}, {', '.join(sysv)}

## Who this row covers
{', '.join(sysv).capitalize()}. The three qualifiers are what select this row; see the legends if you
are not sure which values apply to you.

| | |
|---|---|
{tbl}

## If the figures are exceeded
An excess that was not approved in advance is settled at the figure above and the difference is not
recoverable. An unavoidable excess is claimed with a short written statement and the evidence, and
is decided by the budget holder rather than by this table.
"""))
                    manifest[did] = {"id": did, "area": fam["area"], "parent": sec,
                                     "cluster": fam["subject"], "family": fam["key"],
                                     "stratum": "S1", "axes": dict(zip(
                                         [a[0] for a in axes], sysv)),
                                     "meaning": dict(zip([a[0] for a in axes], (va, vb, vc)))}
                    qid = f"h-{fam['key']}-{ia}{ib}{ic}"
                    questions.append(dict(
                        id=qid + "-d", q=f"For {', '.join(sysv)}, {fam['ask']}?",
                        D_true=[did], lever="direct", family=fam["key"], area=fam["area"],
                        intent_A=0, support=[]))
                    questions.append(dict(
                        id=qid + "-i",
                        q=f"I'm {pa} — {pb}, {pc} — {fam['ask']}?"
                          if fam["key"] == "perdiem" else
                          f"{pa.capitalize()}, {pb}, {pc}: {fam['ask']}?",
                        D_true=[did], lever="indirect", family=fam["key"], area=fam["area"],
                        intent_A=3, support=support[fam["key"]]))
    return docs, questions, manifest


def parse_grid(s):
    g = [int(x) for x in s.lower().split("x")]
    if len(g) != 3 or any(not 1 <= v <= 8 for v in g):
        sys.exit("  --grid wants three numbers 1-8, like 4x4x4")
    return g


def cmd_write(a):
    grid = parse_grid(a.grid)
    docs, questions, manifest = build(grid)
    import shutil
    if OUT.exists(): shutil.rmtree(OUT)
    for area, did, text in docs:
        p = OUT / "regions" / area / f"{did}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    manifest["_grid"] = {"grid": grid, "rows_per_family": grid[0] * grid[1] * grid[2]}
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    n = grid[0] * grid[1] * grid[2]
    head = f"""# Gold set — the hard extension, grid {a.grid} ({n} rows per family).
#
# Generated: ./bench/crowd.py write --grid {a.grid}.  Regenerate rather than edit.
#
# Two questions per row, same answer, different vocabulary:
#
#   direct     asks in the system's words ("grade 3, band C, 6 to 10 nights"). A control.
#   indirect   asks the way a person would ("a team manager, Jakarta, eight nights"). None of those
#              words appears in any row — only in the legends — so answering needs a lookup and then
#              a fetch, and the answer is one of {n} rows the query cannot otherwise separate.
#
# `support` names the legend documents an arm has to pass through. They are ordinary retrievable
# documents: no arm can reach anything another arm cannot.

questions:
"""
    lines = [head]
    for q in questions:
        sup = "".join(f"\n  - {s}" for s in q["support"]) or " []"
        lines.append(f"""- id: {q['id']}
  q: {json.dumps(q['q'], ensure_ascii=False)}
  A_true: [{q['area']}]
  D_true: [{q['D_true'][0]}]
  needs: any
  intent_A: {q['intent_A']}
  intent_B: 0
  family: {q['family']}
  lever: {q['lever']}
  support:{sup}
""")
    GOLD.write_text("\n".join(lines), encoding="utf-8")
    rows = sum(1 for _, i, _ in docs if manifest.get(i, {}).get("axes"))
    legs = sum(1 for _, i, _ in docs if manifest.get(i, {}).get("legend"))
    print(f"  grid {a.grid} · {rows} rows + {legs} legends + {len(FAMILIES)} sections "
          f"= {len(docs)} documents")
    print(f"  {len(questions)} questions -> {GOLD.relative_to(ROOT.parent)}")
    print(f"  expected recall@20 if the query cannot separate the rows: ~{min(1.0, 20/n):.2f}"
          f"   (hit@10 ~{min(1.0, 10/n):.2f})")


def cmd_stats(a):
    grid = parse_grid(a.grid)
    docs, questions, man = build(grid)
    manifest = man
    from retrieve import tokens
    import collections
    body = {i: t.split("---", 2)[-1] for _, i, t in docs if man.get(i, {}).get("axes")}
    print(f"\n  grid {a.grid} · {len(body)} rows in {len(FAMILIES)} families\n")
    print("   family      rows   jaccard within   jaccard across")
    for fam in FAMILIES:
        mem = [i for i in body if man[i]["family"] == fam["key"]]
        tk = {i: set(tokens(body[i])) for i in mem}
        pr = [len(tk[x] & tk[y]) / len(tk[x] | tk[y]) for n, x in enumerate(mem[:20]) for y in mem[n+1:20]]
        oth = [i for i in body if man[i]["family"] != fam["key"]][:30]
        to = {i: set(tokens(body[i])) for i in oth}
        cr = [len(tk[x] & to[y]) / len(tk[x] | to[y]) for x in mem[:6] for y in to]
        print(f"   {fam['key']:<10} {len(mem):>5}          {sum(pr)/len(pr):.3f}            "
              f"{sum(cr)/len(cr):.3f}")
    # Does any word of an indirect question appear in its own answer row?
    leak = 0
    for q in questions:
        if q["lever"] != "indirect": continue
        d = q["D_true"][0]
        if d not in body: continue
        qt = set(tokens(q["q"])); dt = set(tokens(body[d]))
        shared = qt & dt
        # The shared words are the family's own subject words, which every row has. What matters is
        # whether anything *discriminating* leaked — a word in this row and not in its siblings.
        sibs = [i for i in body if man[i]["family"] == man[d]["family"] and i != d]
        common = set.intersection(*[set(tokens(body[i])) for i in sibs[:12]]) if sibs else set()
        disc = shared - common
        if disc: leak += 1
    # Two rows carrying the same answer make a mislabelled question, not a hard one: a retriever
    # that returns the twin has supplied the right figures and is scored as having missed. This
    # failed at 128 of 320 before the primary figure was made a function of all three axes.
    import re as _re
    dup = collections.defaultdict(list)
    for i, t in body.items():
        dup[(man[i]["family"], tuple(_re.findall(r"^\| ([^|]+) \| ([^|]+) \|$", t, _re.M)))].append(i)
    clash = sum(len(v) for v in dup.values() if len(v) > 1)
    print(f"\n  rows whose figures are identical to a sibling's: {clash}/{len(body)}"
          f"   {'ok' if clash == 0 else '<<< MISLABELLED — every one of these is an unfair miss'}")
    n_ind = sum(1 for q in questions if q["lever"] == "indirect")
    print(f"  indirect questions sharing a *discriminating* word with their own row: "
          f"{leak}/{n_ind}")
    print("  (a discriminating word is one this row has and its siblings do not — that is the leak")
    print("   that would let BM25 or the reranker pick the row without using a legend)\n")


def cmd_bm25(a):
    import os, collections, statistics
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
    print(f"\n  BM25 alone over {len(texts)} documents · {len(qs)} questions\n")
    print("    lever        n    hit@10   hit@20   median rank")
    for lev, (h10, h20, n, rk) in sorted(by.items()):
        print(f"    {lev:<10} {n:>4}    {h10/n:5.2f}    {h20/n:5.2f}    {statistics.median(rk):>6.0f}")
    print()


def cmd_fusion(a):
    """B1 without paying for B1.

    `probe.py` measured B1 hit@10 against fusion recall@20 across four wordings and they agreed to
    the second decimal: 1.00/1.00, 1.00/1.00, 0.93/0.93, 0.80/0.80. The reranker recovers what fusion
    puts in its top 20 and nothing else, so recall@20 *is* B1's ceiling and, in practice, B1. That
    costs one embedding per question and no LLM call — which is what makes sweeping 640 questions
    over 1,114 documents an affordable thing to do rather than a decision about money.

    A sample still goes through the real reranker afterwards. An equality that held on one corpus is
    evidence, not a licence.
    """
    import os, collections, statistics, json as _j
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    sys.path.insert(0, str(ROOT))
    # **run.py's corpus, not probe.py's.** The two build the indexed text differently — "name
    # one_liner body" against "name. one_liner\n\nbody" — which is a different string, a different
    # embedding and a different ranking. Measuring the ceiling with one and B1 with the other
    # produced the contradiction that found this: B1 hit@10 came back at 0.125 on forty questions
    # whose fusion recall@20 was 0.100, and a ceiling that can be beaten is not a ceiling.
    import run as runner
    from retrieve import Hybrid
    import yaml as _y
    texts, area, _one, _kids, _hb = runner.corpus()
    h = Hybrid(texts).warm()
    qs = _y.safe_load(GOLD.read_text(encoding="utf-8"))["questions"]
    if a.sample: qs = qs[::max(1, len(qs) // a.sample)]
    h.dense.embed([q["q"] for q in qs])
    out, by = [], collections.defaultdict(lambda: [0, 0, 0, []])
    for n, q in enumerate(qs, 1):
        fused = h.search(q["q"], n=50)
        d = q["D_true"][0]
        r = fused.index(d) + 1 if d in fused else 999
        sup = [s for s in q.get("support") or [] if s in fused[:10]]
        out.append({"id": q["id"], "lever": q["lever"], "family": q["family"],
                    "rank": r, "legends_in_top10": len(sup)})
        b = by[q["lever"]]; b[0] += r <= 10; b[1] += r <= 20; b[2] += 1; b[3].append(r)
        if n % 50 == 0: print(f"    {n}/{len(qs)}", file=sys.stderr)
    (ROOT / "crowd-fusion.json").write_text(_j.dumps(out, indent=1), encoding="utf-8")
    print(f"\n  hybrid fusion over {len(texts)} documents · {len(qs)} questions\n")
    print("    lever        n    hit@10   recall@20   median rank")
    for lev, (h10, h20, n, rk) in sorted(by.items()):
        print(f"    {lev:<10} {n:>4}    {h10/n:5.2f}      {h20/n:5.2f}    {statistics.median(rk):>6.0f}")
    print("\n    recall@20 is B1's ceiling and, on the evidence so far, B1 itself.")
    ind = [o for o in out if o["lever"] == "indirect"]
    if ind:
        print(f"    legends reached in the top 10 on {sum(bool(o['legends_in_top10']) for o in ind)}"
              f"/{len(ind)} indirect questions — what the single-shot arm gets instead of the answer")
    by_fam = collections.defaultdict(lambda: [0, 0])
    for o in ind:
        by_fam[o["family"]][0] += o["rank"] <= 20; by_fam[o["family"]][1] += 1
    if by_fam:
        print("\n    indirect recall@20 by family")
        for f, (hh, nn) in sorted(by_fam.items()):
            print(f"      {f:<12} {hh/nn:5.2f}   n={nn}")
    print()


def cmd_curve(a):
    """Dose and response: is the rival count actually what breaks it?

    Two points are not a curve. The claim is that a retriever returning k finds the answer with
    probability about k/N when N documents are equally plausible, and the evidence for it so far is
    N=16 scoring 1.00 and N=64 scoring 0.03. If that is the mechanism, the points between must lie
    on it; if they do not, something else is doing the work and the dataset is hard by accident.

    Each grid rewrites the extension, embeds what is new and measures fusion on a sample. Embeddings
    only — no reranker, because recall@20 bounds it. The 4x4x4 corpus is restored at the end.

    A second embedding model runs over the same questions under --model, because a collapse that
    only one embedding model suffers is a fact about that model.
    """
    import os, collections, statistics, shutil, importlib
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    sys.path.insert(0, str(ROOT))
    if a.model: os.environ["EMBED_MODEL"] = a.model
    import run as runner
    from retrieve import Hybrid
    import yaml as _y
    grids = [g.strip() for g in a.grids.split(",")]
    print(f"\n  embedding model: {os.environ.get('EMBED_MODEL', 'text-embedding-3-large')}")
    print(f"\n     N     docs   n    direct hit@10   indirect hit@10   indirect recall@20   k/N")
    out = []
    for gs in grids:
        grid = parse_grid(gs)
        N = grid[0] * grid[1] * grid[2]
        class _A: pass
        w = _A(); w.grid = gs
        cmd_write(w)
        importlib.reload(runner)
        texts, area, _o, _k, _h = runner.corpus()
        allq = _y.safe_load(GOLD.read_text(encoding="utf-8"))["questions"]
        # Per lever. The gold set alternates direct, indirect, direct, ... so a flat stride lands on
        # one lever only: the first run of this sweep sampled 160 direct questions, reported the
        # indirect cells as 0/0 rendered as 0.00, and the zeros looked exactly like a total collapse.
        qs = []
        for lev in ("direct", "indirect"):
            sub_q = [q for q in allq if q["lever"] == lev]
            qs += sub_q[::max(1, len(sub_q) // (a.sample // 2))][:a.sample // 2]
        h = Hybrid(texts).warm()
        h.dense.embed([q["q"] for q in qs])
        by = collections.defaultdict(lambda: [0, 0, 0])
        for q in qs:
            fused = h.search(q["q"], n=50)
            d = q["D_true"][0]
            r = fused.index(d) + 1 if d in fused else 999
            b = by[q["lever"]]; b[0] += r <= 10; b[1] += r <= 20; b[2] += 1
        di, ind = by["direct"], by["indirect"]
        assert di[2] and ind[2], f"a lever came back empty: direct {di[2]}, indirect {ind[2]}"
        row = dict(grid=gs, N=N, docs=len(texts), n=len(qs),
                   direct=di[0] / max(1, di[2]), indirect=ind[0] / max(1, ind[2]),
                   ind20=ind[1] / max(1, ind[2]))
        out.append(row)
        print(f"   {N:>4}   {len(texts):>5}  {len(qs):>3}       {row['direct']:5.2f}"
              f"             {row['indirect']:5.2f}              {row['ind20']:5.2f}"
              f"          {min(1.0, 10/N):5.2f}")
    print("\n   k/N is the prediction for a query that cannot separate the rows at all, with k=10.")
    print("   Above it means the query still carries some signal; below it means the rows are")
    print("   outranked by documents from outside the family as well.\n")
    (ROOT / f"crowd-curve{'-' + a.model if a.model else ''}.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    class _A2: pass
    r = _A2(); r.grid = "4x4x4"; cmd_write(r)
    print("   restored the 4x4x4 corpus.\n")


def cmd_anatomy(a):
    """What actually fills the top ten, and whether the extension is even in the running.

    A miss is only evidence if the thing that came back instead does not answer the question. The
    families were given subjects that fit the five frozen areas, and the frozen 700 already covers
    those areas thoroughly — so a question about part-time leave accrual can be answered, in general
    terms, by a document that was there before any of this was built. Scoring that as a miss measures
    a labelling decision rather than a retriever.

    This splits the top ten into what it is made of. `a sibling row` is the intended failure — the
    family was reached and the qualifier was not. `frozen 700` is the confound.
    """
    import os, collections, yaml as _y
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    sys.path.insert(0, str(ROOT))
    import run as runner
    from retrieve import Hybrid
    texts, area, _o, _k, _h = runner.corpus()
    h = Hybrid(texts).warm()
    man = json.loads(MANIFEST.read_text())
    qs = [q for q in _y.safe_load(GOLD.read_text(encoding="utf-8"))["questions"]
          if q["lever"] == "indirect"]
    qs = qs[::max(1, len(qs) // a.sample)]
    h.dense.embed([q["q"] for q in qs])
    acc = collections.defaultdict(collections.Counter)
    for q in qs:
        fam, d = q["family"], q["D_true"][0]
        for t in h.search(q["q"], n=10):
            if t == d: k = "answer"
            elif man.get(t, {}).get("family") == fam and "-legend-" in t: k = "own legend"
            elif man.get(t, {}).get("family") == fam: k = "sibling row"
            elif t.startswith("hard-"): k = "other family"
            else: k = "frozen 700"
            acc[fam][k] += 1
        acc[fam]["_n"] += 1
    ks = ["answer", "sibling row", "own legend", "other family", "frozen 700"]
    print("\n  what fills the top 10 on an indirect question\n")
    print(f"    {'family':<12}{'n':>4}   " + "".join(f"{k:>14}" for k in ks))
    for fam in sorted(acc):
        n = acc[fam]["_n"]
        print(f"    {fam:<12}{n:>4}   " + "".join(f"{acc[fam][k]/n/10:>13.0%} " for k in ks))
    print("\n    sibling row  the intended failure — the family was reached, the qualifier was not")
    print("    frozen 700   the confound — the incumbent corpus already answers this, and a miss")
    print("                 scored against the extension may not be a miss at all\n")


def cmd_routecheck(a):
    """What the walker is handed. A family big enough to break retrieval has to stay walkable."""
    import os, yaml as _y
    os.environ.setdefault("BENCH_EXTRA_CORPUS", "bench/corpus-hard")
    sys.path.insert(0, str(ROOT))
    import run as runner
    texts, area, one_liner, children, has_body = runner.corpus()
    qs = _y.safe_load(GOLD.read_text(encoding="utf-8"))["questions"]
    print(f"\n  the tree the agent walks: {len(one_liner)} nodes, {len(texts)} of them retrievable\n")
    for fam in FAMILIES:
        sec = f"sec-hard-{fam['key']}"
        kids = children.get(sec, [])
        legends = [k for k in kids if "-legend-" in k]
        table = "\n".join(f"  {k}  —  {one_liner.get(k,'')}" for k in kids)
        print(f"   {sec}")
        print(f"     rows in the table : {len(kids)}  ({len(legends)} legends + {len(kids)-len(legends)} rows)")
        print(f"     table size        : {len(table):,} characters ≈ {len(table)//4:,} tokens")
        print(f"     legends lead the table    : {'yes' if all('-legend-' in k for k in kids[:3]) else 'NO — buried among the rows'}")
    # Is the area reachable from hop 0? The frozen use_when sentences never mentioned these rows.
    rows = runner.rows()
    print(f"\n   hop 0 has {len(rows)} areas; every family sits under one of them "
          f"({', '.join(sorted({f['area'] for f in FAMILIES}))}).")
    print("   The frozen use_when sentences were written before this extension existed and do not")
    print("   mention it. That is deliberate: if the routing layer only wins because its table was")
    print("   rewritten for the test, it has not won anything.\n")
    ind = [q for q in qs if q["lever"] == "indirect"]
    print(f"   an indirect question, as the walker meets it:\n     {ind[0]['q']}")
    print(f"     answer  : {ind[0]['D_true'][0]}")
    print(f"     legends : {', '.join(ind[0]['support'])}")
    print("\n   The walk it needs: open the area, open the section, read three legends, open one row.")
    print("   Five steps and no guessing. The single-shot arm gets one list of ten.\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("write", "stats", "bm25", "routecheck", "fusion", "curve", "anatomy"):
        s = sub.add_parser(name); s.add_argument("--grid", default="4x4x4")
        if name in ("fusion", "anatomy"): s.add_argument("--sample", type=int, default=0)
        if name == "curve":
            s.add_argument("--grids", default="4x4x1,4x4x2,4x4x4,4x8x4,8x8x4")
            s.add_argument("--sample", type=int, default=160)
            s.add_argument("--model", default="")
    a = ap.parse_args()
    {"write": cmd_write, "stats": cmd_stats, "bm25": cmd_bm25,
     "routecheck": cmd_routecheck, "fusion": cmd_fusion, "curve": cmd_curve,
     "anatomy": cmd_anatomy}[a.cmd](a)
