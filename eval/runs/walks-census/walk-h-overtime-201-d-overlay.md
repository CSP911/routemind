1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H1, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers by day/hour/location and minute rounding rules likely live in attendance"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_145636 --outcome answered --used /v1/regions/attendance /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body

2. **Answer**: Multiplier 2.19x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the current, 2026-01-01-onwards table is the right version, since the question carries no earlier date)
- /v1/nodes/sec-hard-overtime (located the specific D3/H1/P2 row address)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body (the answer: 2.19x, rounding to the nearest 5 minutes)

4. **Notes**: The overtime rate subject has three superseded/current versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) with the oldest giving no indication it had been replaced — the legend-revision page warns this is exactly the trap. The question gave no explicit date, but since today is 2026-09-20/21, the current table (`sec-hard-overtime`, in force from 2026-01-01) is the correct one; had the question specified a 2025 date, `hard-overtime-v2` would have been the right source instead. No other ambiguity — the three qualifiers (day, hours, place) map directly and unambiguously to one row address.
