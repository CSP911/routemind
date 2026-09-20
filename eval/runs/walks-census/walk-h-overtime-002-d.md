1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

2. **Answer**: Multiplier is 1.26x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

4. **Notes**: The payroll area table warned that overtime premiums moved to attendance on 2026-01-01, with the old rule still parked at `/v1/nodes/hard-moved-overtime/body` — going there instead would have led to a superseded answer. The attendance area table itself lists both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and two older superseded versions (`hard-overtime-v2`, `overtime-rate-table`, plus a `hard-overtime-legend-revision` warning file) sitting right next to it with very similar names — easy to grab the wrong one if not reading the "in force" language carefully. Once inside `sec-hard-overtime`, the row addresses are systematically named by day/hours/place code, so the exact row for D1/H1/P3 was unambiguous and required no legend lookup since the question already gave codes rather than plain-language day/hours/place descriptions.
