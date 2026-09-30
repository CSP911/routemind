1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H1, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multiplier/rounding rules by day type, hour band, and location are likely under attendance"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_03b049 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.29x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

4. **Notes**: The overtime rate subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31 as `hard-overtime-v2`, and 2026-01-01 onwards as `sec-hard-overtime`), and the legend-revision doc explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being replaced. Since today is 2026-09-20/21, the current table (`sec-hard-overtime`) was correct, but this was a real fork — a question dated in 2025 would need `hard-overtime-v2` instead, and nothing about the table's row-naming would have flagged that mistake. Once past the version check, the row for D1/H1/P4 existed exactly as named among the 64 rows, so no ambiguity there.
