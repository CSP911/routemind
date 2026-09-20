1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**
Lodging cap: 95 USD per night. Receipt threshold: above 18 USD a receipt must be kept (this row's receipt threshold applies to the claim generally, not lodging specifically — see Notes).
(Junior analyst = grade G1, Tokyo = band B1, one night = stay S1, under the table in force from 2026-01-01.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body
/v1/nodes/hard-perdiem-legend-revision/body (confirms this version is current for 2026-09-20)

4. **Notes**
- The per-diem table is indexed by three qualifiers (grade, band, stay) that have to be looked up separately in three legend files before the right row can be addressed — none of the row addresses can be guessed or built, they have to come from what the tables print.
- There are three versions of this per-diem document (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the revision-legend page is explicit that reaching for the newest is wrong for a question dated before 2026-01-01. Today (2026-09-20) falls under the current table, so no correction was needed here, but this is the easiest place to get a stale or an over-eager answer.
- The row bundles four figures (lodging, meals, receipt threshold, incidentals) under one "receipt threshold" value; it is not spelled out whether this threshold is specific to lodging or is a single per-claim threshold covering all four lines. I read it as the general receipt threshold for this row rather than a lodging-only figure, since it sits in the same table as the other three per-category caps with no further qualification — but the document doesn't say so outright, and a reader wanting a lodging-only threshold should be aware of that ambiguity.
