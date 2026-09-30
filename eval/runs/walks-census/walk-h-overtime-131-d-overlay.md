1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H4, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime hours/multiplier likely under attendance" --member /v1/regions/payroll "multiplier could be a payroll computation rule"
./bench/rmcli.py table /v1/nodes/hard-overtime-legend-revision
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f3fece --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

2. **Answer**: Multiplier 2.07x; minutes rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of three overtime-rate versions applies for today's date, 2026-09-21)
- /v1/nodes/sec-hard-overtime (the current overtime rate table, indexed by day/hours/place — located the D2/H4/P2 row)
- /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body (the answer itself)

4. **Notes**: The overtime rate subject has three versions in force over different date ranges (until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision doc explicitly warns not to reach for the newest by default. Today's date (2026-09-21) falls in the current range, so `sec-hard-overtime` was the right table, but this was a real branch point — a question dated in 2025 would need `hard-overtime-v2` instead. The row address itself directly matched the D2/H4/P2 qualifiers once the right table version was found, so no ambiguity there. The overlay close command reported the used addresses as "reached" rather than "used," noting they weren't in the overlay's original member list (I'd only added the two top-level region tables as members, not the specific rows I ended up reading) — didn't affect the answer, but worth noting for how the overlay bookkeeping works.
