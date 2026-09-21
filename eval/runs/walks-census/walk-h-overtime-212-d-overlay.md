1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H2, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime hours/multipliers are typically an attendance topic" --member /v1/regions/payroll "overtime pay multiplier could be a payroll topic"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c6cdb9 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

2. **Answer**: Multiplier is 2.34x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions is in force for today's date, 2026-09-21)
- /v1/nodes/sec-hard-overtime (the current overtime rate table, indexed by day/hours/place, used to locate the exact row)
- /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body (the row with the multiplier and rounding figures)

4. **Notes**: The overtime rate topic exists in three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc explicitly warns that reaching for the newest is wrong for dates before 2026-01-01 — the oldest version doesn't even say it was replaced. Since today is 2026-09-21, the current table (`sec-hard-overtime`, in force from 2026-01-01) was the right one, but this was a real branch point worth checking rather than assuming. Also initially added the payroll region as a candidate for "multiplier" since overtime is a pay topic, but the payroll table itself contains a note (`hard-moved-overtime/body`) that overtime premiums moved to attendance on 2026-01-01, confirming attendance was the correct region and payroll wasn't needed as a source.
