#!/usr/bin/env python3
"""The time axis: five levers over three versions of the same rule.

Every subject in `bench/corpus-hard` now exists three times — the frozen corpus's own page, an
intermediate table, and the current 64-row one — with two cutover dates between them. That is the
point of the middle version: with a single revision the whole axis is a two-way choice and "reach for
the newest" wins without understanding anything. A question dated in 2025 needs the middle one, so
neither extreme is safe.

    stale-old   a date before the first cutover          -> the frozen corpus's page
    stale-mid   a date inside the middle window          -> the intermediate table
    changed     "when did this change, and to what"      -> the revision notice
    boundary    two days either side of a cutover        -> whichever version covers that day
    both        "what was it then, and then"             -> two versions at once, needs: all

`changed` matters more than it looks. The revision notices were measured as reaching the top ten on
**0%** of indirect questions — but nobody had ever asked for them. A document nothing asks for and
nothing retrieves has not been tested; it has been ignored by both sides.

`boundary` is the one that separates reading a date from noticing there is one. The two questions in
a pair differ by two days and by nothing else, and they have different answers.

Templated, free, and checkable with ./bench/audit.py.

    ./bench/temporal.py > eval/gold/hard-temporal.yaml
"""
import json

MID, MID_END, EFF = "2024-07-01", "2025-12-31", "2026-01-01"
BEFORE = ["March 2023", "September 2023", "January 2024"]
INSIDE = ["October 2024", "March 2025", "August 2025"]

FAMS = [
 dict(key="perdiem", area="expense", v1="overseas-rates", subject="the overseas per-diem",
      ask="what was the nightly lodging cap",
      q1="for a grade 2 traveller going to a band B2 destination",
      asks_old="for a trip to a band B destination"),
 dict(key="overtime", area="attendance", v1="overtime-rate-table", subject="the overtime rate",
      ask="what multiplier was paid",
      q1="for day D2 work in hour band H2",
      asks_old="for ordinary overtime beyond the forty-hour week"),
 dict(key="accrual", area="attendance", v1="leave-accrual", subject="leave accrual",
      ask="how much leave was accrued or granted",
      q1="for type E2 staff in service band T2",
      asks_old="for someone with two years of continuous service"),
 dict(key="threshold", area="procurement", v1="threshold-table", subject="the approval threshold",
      ask="what was the delegation limit or who signed",
      q1="for category C2 spend in amount band V2",
      asks_old="for a purchase of two million won net of VAT"),
 dict(key="diligence", area="procurement", v1="supplier-due-diligence", subject="supplier due diligence",
      ask="what screening was required",
      q1="for an origin O2 supplier at contract value W2",
      asks_old="for a new supplier"),
]


def build():
    out = []
    for f in FAMS:
        v2, rev = f"hard-{f['key']}-v2", f"hard-{f['key']}-legend-revision"
        n = 0
        def add(lever, q, docs, needs="any"):
            nonlocal n; n += 1
            out.append(dict(id=f"t-{f['key']}-{n:02d}", q=q, area=f["area"], docs=docs,
                            needs=needs, lever=lever, family=f["key"]))
        for d in BEFORE:
            add("stale-old",
                f"In {d}, {f['ask']} {f['asks_old']}? Answer under the version of {f['subject']} "
                f"that was in force on that date.", [f["v1"]])
        for d in INSIDE:
            add("stale-mid",
                f"In {d}, {f['ask']} {f['q1']}? Answer under the version of {f['subject']} that was "
                f"in force on that date.", [v2])
        add("changed", f"How many times has {f['subject']} been rewritten, and from what date does "
                       f"each version apply?", [rev])
        add("changed", f"I have a claim dated in 2025 and I am not sure which version of "
                       f"{f['subject']} applies to it. Where is that written down?", [rev])
        add("boundary", f"For something dated 29 June 2024 — two days before the first change — "
                        f"{f['ask']} {f['asks_old']}? Use the version in force on that day.", [f["v1"]])
        add("boundary", f"For something dated 3 July 2024 — two days after the first change — "
                        f"{f['ask']} {f['q1']}? Use the version in force on that day.", [v2])
        add("both", f"{f['ask'].capitalize()} {f['asks_old']} in 2023, and what had it become by "
                    f"2025? I need both versions of {f['subject']}, not just the current one.",
            [f["v1"], v2], needs="all")
        add("both", f"We are reconciling claims from 2023 and from 2025 against {f['subject']}. "
                    f"Which two versions do I need, and {f['ask']} under each?",
            [f["v1"], v2], needs="all")
    return out


if __name__ == "__main__":
    qs = build()
    import collections
    c = collections.Counter(q["lever"] for q in qs)
    print(f"""# The time axis — {len(qs)} questions over three versions of each subject.
#
# Generated: ./bench/temporal.py > eval/gold/hard-temporal.yaml
#
#   {' · '.join(f'{k} {v}' for k, v in sorted(c.items()))}
#
# Three versions exist per subject: the frozen corpus's own page (one qualifier, no dates on it at
# all), an intermediate table ({MID} to {MID_END}, two qualifiers), and the current 64-row table
# ({EFF} onwards, three qualifiers). A question dated in 2025 needs the middle one, so an arm cannot
# pass by preferring the newest document or the oldest.
#
# `boundary` pairs differ by two days and by nothing else, and have different answers.
# `changed` asks for the revision notice itself — a document that was measured as never retrieved,
# which until now meant only that nobody had asked for it.
#
# Check with ./bench/audit.py before running anything against this.

questions:""")
    for q in qs:
        docs = "\n".join(f"  - {d}" for d in q["docs"])
        print(f"""- id: {q['id']}
  q: {json.dumps(q['q'], ensure_ascii=False)}
  A_true: [{q['area']}]
  D_true:
{docs}
  needs: {q['needs']}
  intent_A: 1
  intent_B: 0
  family: {q['family']}
  lever: {q['lever']}
  support: []
""")
