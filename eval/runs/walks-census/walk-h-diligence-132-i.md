1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(This is row origin O2 / value W4 / goods K3: Stuttgart / 700 million won / people's time. Screening score required is 60; financial statements needed are the last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed 2026-09-20 falls under the current table, not the superseded versions)
/v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → W4)
/v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body (final answer: site visit yes, re-review every 6 months)

4. **Notes**
The due diligence subject has three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls cleanly under the current table (`sec-hard-diligence`, in force from 2026-01-01), so there was no real ambiguity here, but it would have been easy to skip that check and grab the current table without verifying the date applies — worth flagging since a question dated in 2025 would need `hard-diligence-v2` instead. All three qualifiers in the question (Stuttgart, seven hundred million won, "people's time") were exact, unambiguous matches to legend rows (O2, W4, K3 respectively) — no nearest-entry judgment calls were needed, which is unusual for this dataset and worth noting as the "clean" case of this walk.
