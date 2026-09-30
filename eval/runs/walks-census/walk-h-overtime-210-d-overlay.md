1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H2, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers and rounding rules would live under attendance"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e5c1c5 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body

2. **Answer**: Multiplier 2.28x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body

4. **Notes**: The overtime rate subject has three versions in force over different date ranges (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the legend-revision page warns explicitly that the oldest version never says it was superseded — so grabbing the first "overtime" hit without checking dates would have been the easy mistake here. Today's date (2026-09-21) falls in the current window, so `sec-hard-overtime` (the three-qualifier table) was correct rather than the superseded `hard-overtime-v2`. Once in the current table, the row address was a direct, unambiguous match on day/hours/place, so no further narrowing was needed.
