1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "Liberation day, six hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/hard-moved-overtime/body "confirms overtime premiums moved to attendance region 2026-01-01, this payroll page is the old rule"
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay add --id ov_2026-09-21_e72c68 --address /v1/nodes/sec-hard-overtime --why "current overtime rate table in force since 2026-01-01, by day type/hours/place"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e72c68 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

2. **Answer**: Multiplier 2.40x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

4. **Notes**: The payroll region is a trap — it's where an instinct-first search lands ("overtime" sounds like a payroll topic), but its own table warns overtime premiums moved to attendance on 2026-01-01 and today is 2026-09-21, so that page is superseded. The real table (sec-hard-overtime) doesn't spell out day/hours/place in the row names in plain English — it uses coded axes (D1-D4, H1-H4, P1-P4) that only resolve through three separate legend files. Guessing the mapping instead of reading all three legends would be easy to get wrong, especially "at my desk" → P1, which isn't the obvious first guess among four workplace categories. Also had to be careful to pick the *current* table (sec-hard-overtime, in force since 2026-01-01) rather than the superseded hard-overtime-v2, since the region listed three versions with a warning file addressing exactly that ambiguity.