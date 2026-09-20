1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.46x; minutes rounded to the nearest 15 minutes. (Approval needed in advance: yes; counts toward the monthly cap: yes.) This is from the current overtime rate table, in force since 2026-01-01, which applies as of today (2026-09-20).

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

4. **Notes**: The attendance area's table listed a legend-revision warning that overtime rate has three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`), which is worth flagging since picking an old version would silently give a wrong multiplier. The current table (`sec-hard-overtime`) already indexes rows by exact day/hours/place code combination (64 rows total), so once D3/H3/P3 was identified as the target combination, the row address `hard-overtime-row-day-d3-hours-h3-place-p3` was directly available in the table listing — no need to open the day/hours/place legend files since the question already gave the codes (D3, H3, P3) rather than plain-language descriptions. Did not open the legend files, so I cannot independently confirm what D3/H3/P3 mean in plain terms, only that they are valid codes matching a row in the current table.
