1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

2. **Answer**: Multiplier is 2.88x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table listing, confirmed this is the current overtime table in force from 2026-01-01)
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body (row with the answer)

4. **Notes**: The payroll region initially looks like the natural home for "multiplier," but /v1/regions/payroll itself warns that overtime, night and holiday premium rates moved to attendance on 2026-01-01, and lists a `hard-moved-overtime` node confirming payroll's own overtime page is stale. That redirect is the one place this walk could easily go wrong — trusting payroll's old overtime rules instead of following the move notice to attendance. Once in attendance, /v1/nodes/sec-hard-overtime was an unambiguous exact match on day/hours/place, and its row address for D4/H3/P1 was printed verbatim by the table listing, so no address had to be inferred or constructed. Did not need to consult the day/hours/place legend files since the question already gave codes (D4, H3, P1) rather than natural-language descriptions.
