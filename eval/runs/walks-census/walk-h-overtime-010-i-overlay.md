1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, three hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers are typically pay-related" --member /v1/regions/attendance "overtime hours/rounding rules may be attendance policy"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2a3f44 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

2. **Answer**: Multiplier 1.32x; rounding to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

4. **Notes**: The payroll region's own overview flagged that overtime premiums moved out of payroll into attendance on 2026-01-01 (seen in the overlay listing as `hard-moved-overtime/body`), which confirmed attendance was the right region and payroll a dead end — good thing the overlay surfaced both regions up front instead of guessing one. The bigger trap was the legend-revision warning: this subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), each indexed differently, and the old version says nothing about being superseded, so naively reading the oldest or most-obviously-named table would have silently given a wrong-era answer. Today's date (2026-09-20/21) put this squarely in the current table, `sec-hard-overtime`. The three legends (day/hours/place) had to be read separately to translate "ordinary Tuesday" → D1, "three hours" → H2, "at my desk" → P1 before the specific row address could even be constructed from the table's printed list — the table itself gives no shortcut past that translation.
