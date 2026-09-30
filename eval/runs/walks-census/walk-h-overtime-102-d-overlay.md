1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H1, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime rules by day/hour/place likely under attendance" --member /v1/regions/payroll "multiplier/rounding could be a payroll computation rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3d2894 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.74x; minutes rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-overtime (the current overtime rate table, listing the per-day/hours/place rows)
- /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body (the actual figures)

4. **Notes**: This subject has three superseded versions of the overtime table (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — the oldest version doesn't even say it was replaced. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-overtime`) was correct, but this was the exact trap the walk warned about and worth double-checking rather than assuming "current" is always right. The row address for D2/H1/P3 was printed verbatim in the table listing, so no address construction was needed — the three-qualifier row addresses are fully enumerated (64 rows) rather than needing a lookup by legend. Did not need to consult the day/hours/place legend docs since the question already gave codes (D2, H1, P3) directly matching a listed row.
