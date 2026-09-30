1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Ordinary Tuesday, six hours, at client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime rules and rounding likely live under attendance" --member /v1/regions/payroll "overtime multiplier/pay rate might be defined in payroll"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0b14c8 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

2. **Answer**
Multiplier: 1.47x. Rounding: to the nearest 15 minutes. (This is from the current overtime rate table, in force from 2026-01-01; approval was not needed in advance for this row, and it counts toward the monthly cap.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

4. **Notes**
The question's phrasing ("an ordinary Tuesday", "six hours", "out at a client's office") is lifted almost verbatim from the three legend tables (day/hours/place), so mapping to codes D1/H3/P2 was unambiguous once the legends were read — no rounding-to-nearest-band judgment calls needed. The one thing worth flagging: `/v1/nodes/hard-overtime-legend-revision/body` and `hard-overtime-v2/body` warn that overtime rate has three historical versions with different figures. I stuck with `sec-hard-overtime` (current, in force from 2026-01-01) since today's date is 2026-09-20/21, which falls inside that window — but a walker who grabbed the superseded `hard-overtime-v2` row instead would get a different multiplier and rounding rule for the same day/hours/place codes, silently. Also noted in passing: `/v1/nodes/hard-moved-overtime/body` under payroll says overtime premiums moved to attendance as of 2026-01-01, confirming attendance (not payroll) was the right region and payroll's overtime-shaped rows there are stale pointers, not the source.
