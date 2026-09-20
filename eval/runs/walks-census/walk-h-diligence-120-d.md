1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body

2. Answer

Yes, a site visit is required. The file (supplier record) is re-reviewed every 12 months.
(For completeness: screening score required is 54, financial statements for the last two years.)

3. Source

/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions is current for 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body (the answering row, current table in force from 2026-01-01)

4. Notes

The procurement area lists three separate supplier due diligence documents (`supplier-due-diligence`,
`hard-diligence-v2`, `sec-hard-diligence`) plus a legend-revision page warning that the oldest version
"says nothing at all about having been replaced." It would have been easy to grab the first plausible
match (`hard-diligence-v2`, described right there in the procurement table listing) without checking
dates. The legend-revision page makes clear today's date (2026-09-20) falls under the current table
(`sec-hard-diligence`, in force 2026-01-01 onward, indexed by three qualifiers), which matched the
question's three qualifiers (origin, value, goods) anyway — a useful cross-check that the right table
was picked.

The row itself ends with a paragraph headed "If the figures are exceeded," about unapproved/unavoidable
excess amounts and budget-holder sign-off — this reads like boilerplate carried over from an
expense-threshold template and has nothing to do with site visits or re-review cadence. It's a red
herring that could confuse someone skimming for "how often" language; the actual re-review interval is
stated plainly in the table above it.
