1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

2. **Answer**: Multiplier is 2.43x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

4. **Notes**: The payroll area's top-level table warns up front that overtime/night/holiday premium rates moved to attendance on 2026-01-01, and explicitly flags its own remaining overtime page (`hard-moved-overtime`) as stale — that saved a wrong turn into payroll. Inside attendance, there are two candidate "overtime rate" tables: `sec-hard-overtime` (current, in force from 2026-01-01) and `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31), plus a legend-revision file warning of a third, even older version. Today's date (2026-09-20) falls inside the current table's validity window, so `sec-hard-overtime` was the correct pick — but it would have been easy to grab the superseded v2 table by mistake if the "in force from 2026-01-01" labels weren't read carefully. The day/hours/place codes (D3/H3/P2) in the question matched the row addressing scheme directly, so no detour through the legend files (day/hours/place definitions) was needed to resolve the answer.