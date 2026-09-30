1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W4, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "site visit and file review cadence sound like vendor/supplier due diligence, likely under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_08f4a0 --outcome answered --used /v1/regions/procurement /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (For reference, the same row also requires a screening score of 61 and last three years of audited financial statements.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions is current for today's date)
/v1/nodes/sec-hard-diligence (table listing, used to find the specific origin/value/goods row)
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body (answer)

4. **Notes**: Supplier due diligence has three versions in force over different date ranges, and the legend-revision page warns explicitly that reaching for the newest version is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about being superseded — so checking dates first mattered here. Today's date (2026-09-20) falls under the current table (`sec-hard-diligence`, in force from 2026-01-01), so no special handling was needed this time, but it would have been easy to skip that check and grab the wrong version by habit. Otherwise this was a clean, direct walk: procurement → the current diligence table → the exact origin/value/goods row, with no ambiguity in the final figures.
