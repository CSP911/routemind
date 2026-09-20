1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row: screening score required 76; financial statements — last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body

4. **Notes**
The procurement area lists three versions of the supplier due-diligence table (current since
2026-01-01, a superseded 2024-07-01–2025-12-31 version, and the original pre-2024-07-01 version),
with a warning that grabbing the newest one for an older date is wrong. Today's date (2026-09-20)
falls in the current table's range, so `sec-hard-diligence` was the right one to open — but this is
the exact trap the legend page calls out, and it would be easy to skip that check and grab a stale
row by habit. Once in the current table, the row address already spelled out the origin/value/goods
codes given in the question (O3/W4/K3), so no separate legend lookup was needed to translate the
question's terms into codes — I verified the row existed at that exact address rather than assuming.
