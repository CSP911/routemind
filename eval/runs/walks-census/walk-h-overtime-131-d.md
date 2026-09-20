1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

2. **Answer**: Multiplier is 2.07x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

4. **Notes**: The payroll region initially looked like the right place to search (it's the traditional home for overtime rates), but its table page explicitly warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01, and the page still there is the old rule. Since today's date is 2026-09-20, that payroll page would have been the wrong, superseded source. The attendance region confirms `sec-hard-overtime` is "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," replacing `overtime-rate-table` and `hard-overtime-v2` — both of which also appear in the attendance table listing and could easily be mistaken for the answer if not read carefully. The row address itself was printed directly by the table (day-d2-hours-h4-place-p2), so no guessing or construction was needed once the right table was open.
