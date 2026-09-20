1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.61x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/regions/payroll
/v1/regions/attendance
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

4. **Notes**: The obvious first guess was to look under payroll, since "multiplier" sounds like a pay-rate question — but payroll's own table flags that overtime premiums moved to attendance on 2026-01-01, so that would have been a dead end if followed further. Bigger trap: attendance lists three overtime pages (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) with no obvious cue on which is current except a dedicated legend-revision file. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so `sec-hard-overtime` is correct — but if the question had been dated in 2025 the answer would have been the superseded `hard-overtime-v2` instead, and grabbing the newest table without checking the revision legend would have silently given the wrong multiplier/rounding. The D3/H4/P4 row address was printed verbatim by the table listing, so no address construction was needed.
