1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body

2. **Answer**: Lodging cap is 243 USD per night. Receipts must be kept for any spend above 38 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body

4. **Notes**: The expense area's table listing flags that overseas per-diem has three superseded/current versions depending on date, so I checked `hard-perdiem-legend-revision` before trusting the row data — jumping straight to `sec-hard-perdiem` without that check would have been fine today (2026-09-20 falls under the 2026-01-01-onwards version, which is current), but the warning explicitly says reaching for the newest is wrong for dates before 2026-01-01, so this is a step worth never skipping. The row itself bundles lodging, meals, receipt threshold, and incidentals together, so it's easy to answer only "what can I put on lodging" and miss that the question also asks about the receipt threshold, which is a separate figure in the same row, not derived from the lodging cap.
