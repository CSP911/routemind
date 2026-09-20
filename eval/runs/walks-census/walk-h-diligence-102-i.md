1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body

2. Answer

No, a site visit is not required. The file is re-reviewed every 36 months.
(For reference: screening score required is 48, financial statements are not required.)

3. Source

/v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
/v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
/v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body (the answer: site visit no, re-review every 36 months)

4. Notes

The main hazard here was version drift: the "supplier due diligence" subject has three superseded
versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision
page warns explicitly that reaching for the newest is only correct for dates on or after 2026-01-01.
Today's date (2026-09-20) falls inside the current version's range, so `sec-hard-diligence` was the
right table, but it would have been easy to skip that check and just grab the first-looking match.

The other near-miss was reading `/v1/nodes/supplier-due-diligence/body` (the generic overview of the
three-check process: sanctions/ownership, code of conduct, disqualification screen) and almost
treating it as the answer — it never mentions site visits or a re-review cadence at all. Those figures
only live in the specific origin/value/goods row, which is three legend lookups away from the region
table. Nothing in the top-level tables hints that a "site visit" question resolves to a per-row table
cell rather than a general policy page, so the path there requires knowing (or discovering) that the
current table is indexed by three qualifiers before the actual figures show up.
