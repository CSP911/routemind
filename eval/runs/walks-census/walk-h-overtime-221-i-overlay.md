1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, six hours, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "holiday overtime multiplier is a pay/payroll calculation question" --member /v1/regions/attendance "off-site/client work and holiday work logging rules may live here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_f93438 --address /v1/nodes/insurance --why "not relevant"
./bench/rmcli.py overlay close --id ov_2026-09-21_f93438 --outcome answered --used /v1/regions/attendance /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

2. **Answer**: Multiplier 2.43x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

4. **Notes**: The overlay's opening table showed a warning file at `/v1/nodes/hard-moved-overtime/body` under payroll saying overtime premiums moved to attendance on 2026-01-01, and both payroll and attendance regions had a "hard-overtime" node — payroll's stale reference and attendance's `sec-hard-overtime`, explicitly marked "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01." Also present were superseded siblings `hard-overtime-v2` (2024-07-01 to 2025-12-31) and an older `overtime-rate-table`; picking one of those instead of `sec-hard-overtime` would have been the easy mistake here. The table is indexed by three separate codes (day/hours/place) via three legends rather than one lookup, so all three had to be read before the row address (`hard-overtime-row-day-d3-hours-h3-place-p2`) could even be constructed correctly — the legends explicitly warn that "the rows do not repeat what is in the left [-hand column]," so skipping straight to a row guess wasn't an option. My one leftover overlay-remove call failed harmlessly (`/v1/nodes/insurance` was never actually added as a member, only listed as a candidate in the initial table print) — did not affect the close.
