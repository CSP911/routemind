1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D3, hours H4, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-v2/body "superseded 2024-07-01 to 2025-12-31 version, keep for comparison only" --member /v1/nodes/hard-overtime-legend-revision/body "explains which version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8fba95 --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

2. **Answer**: Multiplier is 2.55x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

4. **Notes**: The overtime table has three historical versions (current since 2026-01-01, `hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), so the near-miss risk was pulling the figures from the superseded `hard-overtime-v2` page instead of the current `sec-hard-overtime` one. Today's date (2026-09-21) falls in the current table's "in force from 2026-01-01" window, and the row itself restates that effective date, so there was no real ambiguity once the correct table was opened — but a walk that stopped at the first overtime-looking row without checking the "in force" note could easily have grabbed the wrong version's multiplier. The overlay's row list conveniently included an exact D3/H4/P2 address, so no interpolation across day/hour/place legends was needed.
