1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D4, hours H2, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime premium rates moved here from payroll on 2026-01-01, per payroll's hard-moved-overtime note"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ac8acd --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

2. **Answer**
Multiplier: 2.82x
Rounding: to the nearest 10 minutes
(This is the current table, in force from 2026-01-01; today is 2026-09-20/21, so it applies.)

3. **Source**
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

4. **Notes**
The payroll region's own table carries a warning that overtime premiums moved to attendance on 2026-01-01, which pointed straight at the right region rather than making me search payroll in vain. Inside attendance, `/v1/nodes/sec-hard-overtime` describes itself as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" and is indexed by day/hours/place codes, with a per-row address pattern (`hard-overtime-row-day-<D>-hours-<H>-place-<P>`) that directly matched the question's D4/H2/P3 — no legend lookup was needed since the question already gave codes rather than plain-language day/hour/place descriptions. I did not add that row as an overlay member before reading it (I went straight from the table listing to `read`), so on close the tool reported it as "reached = answered from somewhere the overlay never named" rather than as a tracked member — worth noting since the overlay's member list technically never included the address that actually answered the question. There is also a superseded `hard-overtime-v2` (2024-07-01 to 2025-12-31) and an older `overtime-rate-table`; since today's date is after 2026-01-01, the current table was the correct one and I did not need to consult the older versions.
