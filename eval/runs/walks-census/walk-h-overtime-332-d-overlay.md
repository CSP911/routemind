1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D4, hours H4, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/night/holiday premium rates moved here from payroll on 2026-01-01, per payroll table note"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3877fa --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

2. **Answer**: Multiplier 3.06x; minutes rounded to the nearest 20 minutes. (This row also requires approval in advance and counts toward the monthly cap, in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

4. **Notes**: Payroll's table explicitly warns that overtime premium rates moved to attendance on 2026-01-01, so I redirected there instead of trusting payroll's own listing — a question phrased this way ("multiplier," "rounding") would otherwise look like a payroll question. The bigger trap was version: there are three overtime-rate tables (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and current `sec-hard-overtime` from 2026-01-01), and the legend-revision doc stresses the newest is not always right — for 2025 dates the middle version applies. Today is 2026-09-21, so the current table was correct, but I read the revision doc first specifically to avoid grabbing `hard-overtime-v2` by habit. The row address matched the D4/H4/P3 qualifiers exactly, no interpretation needed. The overlay close flagged these addresses as "reached" rather than formal members, since I navigated to them directly from the table listing rather than adding them to the overlay first — functionally the same evidence, just not pre-declared.
