1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H2, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers by day type, hour band, and location are likely attendance rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a7dd0e --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

2. **Answer**: Multiplier 2.37x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions is in force for today's date)
- /v1/nodes/sec-hard-overtime (table listing, used to find the exact D3/H2/P4 row address)
- /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body (the answer)

4. **Notes**: The overtime rate subject has three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) covering different date ranges, and the legend-revision doc warns the oldest version says nothing about being replaced — so grabbing the first plausible-looking overtime table without checking dates would have silently given a wrong, out-of-date multiplier. Today's date (2026-09-20/21) falls in the "2026-01-01 onwards" band, so `sec-hard-overtime` was correct, but this is exactly the kind of question where reaching for the newest table without checking is only right by luck. Once inside `sec-hard-overtime`, the row for day D3, hours H2, place P4 was listed explicitly by address, so no construction of addresses was needed.
