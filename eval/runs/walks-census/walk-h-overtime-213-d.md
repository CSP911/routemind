1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

2. **Answer**: Multiplier is 2.37x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

4. **Notes**: The obvious first guess was payroll, since overtime rates sound like a payroll topic, but /v1/regions/payroll flags outright that overtime premiums moved to attendance on 2026-01-01 and that the payroll page is now the old rule — a clean warning that stopped a wrong turn before it started. Inside attendance, there were two competing overtime nodes: `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (current, in force from 2026-01-01). Since today is 2026-09-20, the current table was the correct one, and the table listing itself labeled it "THE CURRENT OVERTIME RATE TABLE" so this wasn't really ambiguous, just something that would have been easy to get wrong by grabbing the first "overtime" hit. The row address for D3/H2/P4 was printed verbatim in the table listing, so no construction or guessing of legend codes (day/hours/place) was needed — the question already used the same coded terms (D3, H2, P4) that the table's own row addresses use, which made the final lookup a direct match rather than requiring a trip through the day/hours/place legend files.
