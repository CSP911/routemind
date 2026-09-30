1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H3, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding rules are payroll concepts" --member /v1/regions/attendance "hours worked and time tracking could define rounding rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b72f97 --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.46x. Minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

4. **Notes**: The initial overlay member for /v1/regions/payroll turned out to be a dead end — its own row (/v1/nodes/hard-moved-overtime/body) warns that overtime premiums moved out of payroll into attendance as of 2026-01-01, which is why the real table (sec-hard-overtime) lives under /v1/regions/attendance instead. Good thing I hedged with both regions in the initial overlay rather than picking payroll alone. The overtime table has three prior/current versions (overtime-rate-table, hard-overtime-v2, and the current sec-hard-overtime effective 2026-01-01); today's date (2026-09-21) falls under the current version, so no version confusion there, but it's the kind of thing that could easily trip up a less careful pass — worth double-checking the effective-date line on the row itself, which confirmed "In force from 2026-01-01." The row address was not printed by name anywhere until I opened the sec-hard-overtime table, so the overlay close was flagged as "reached" (an address not named in the working set) rather than a direct hit — expected, not an error.
