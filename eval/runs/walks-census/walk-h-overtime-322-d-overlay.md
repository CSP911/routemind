1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H3, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers are pay-related, likely in payroll table" --member /v1/regions/attendance "day/hour/place could relate to attendance rules for overtime"
./bench/rmcli.py overlay remove --id ov_2026-09-21_282b54 --address /v1/nodes/hard-moved-overtime/body --why "not needed, superseded pointer only"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_282b54 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.94x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table, to locate the row)
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body (the answer)

4. **Notes**: The top-level table lists both a payroll row and an attendance row as plausible matches for "overtime multiplier." Payroll turned out to be a dead end — `/v1/nodes/hard-moved-overtime/body` under it is a WARNING stub saying overtime premiums moved to attendance on 2026-01-01, so the real table is `sec-hard-overtime` under attendance. My `overlay remove` call on that stub address failed with a 404 because it was never actually added as a member (it only appeared in the printed table alongside the payroll region member, not as its own overlay row) — a reminder that the rows shown under a region member aren't themselves overlay members until added explicitly. Once at `sec-hard-overtime`, the row address for D4/H3/P3 was printed directly (64 rows indexed by day/hours/place code), so no legend lookup was needed since the question already gave the codes. The overlay close reported the used addresses as "reached" rather than "used," implying they weren't first added as overlay members before being read — functionally fine for answering, but worth adding members before reading next time to avoid that mismatch.
