1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/sec-hard-overtime/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

2. Answer: Multiplier is 2.40x; minutes are rounded to the nearest 15 minutes.

3. Source:
/v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
/v1/nodes/hard-overtime-legend-hours/body (six hours → hours H3)
/v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body (multiplier 2.40x, rounding to nearest 15 minutes)

4. Notes: The payroll area's table explicitly warned that overtime premiums moved to attendance on 2026-01-01, which confirmed I should not use the old payroll page or its superseded rate table — a plausible wrong turn avoided early. Within attendance, there are three historical versions of the overtime rules (current since 2026-01-01, `hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`); today's date (2026-09-20) put me squarely on the current `sec-hard-overtime` table, but it would be easy to grab a superseded row if not careful. The three qualifiers (day/hours/place) are each resolved by a separate legend that maps plain-language descriptions to codes — "Liberation Day" mapped directly and unambiguously to D3, "six hours" to H3, and "at my desk" to P1, so no fuzzy nearest-entry judgment calls were needed here.
