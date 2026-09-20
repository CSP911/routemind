1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body

2. **Answer**: No site visit required. Re-review interval: every 36 months. (Screening score required: 32; financial statements not required — for context.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is current for today's date)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body (the actual figures)

4. **Notes**: The procurement area warns up front that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards) and explicitly says reaching for the newest is wrong for dates before 2026-01-01 — easy to grab the wrong table if you skip that check. Today's date (2026-09-20) falls in the current version (`sec-hard-diligence`, in force from 2026-01-01), so no correction was needed here, but the walk deliberately routes through the legend page rather than assuming. The current table is indexed by three qualifiers (origin/value/goods) and the O1/W1/K3 row was listed directly in the table view, so no legend lookups for origin/value/goods codes were needed since the codes were already given in the question. The row's closing section ("If the figures are exceeded") reads like boilerplate copied from an expense/spend-limit template (talks about "excess," "budget holder," "not recoverable") rather than anything specific to site visits or re-review cadence — ignored it as not relevant to the two figures asked for.
