1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E3, tenure T4, site L3 (current table, in force since 2026-01-01): accrues 1.32 days per month; carry-over limit is 15 days — that is the most you can still be holding in January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body
/v1/nodes/hard-accrual-legend-revision/body (used to confirm the 2026-01-01 current table is the correct version for today's date, 2026-09-20)

4. **Notes**
The question gave codes directly (E3/T4/L3) rather than plain-language descriptions, so there was no need to consult the legend files for type, tenure, or site — the row address could be built straight from the qualifiers once the table of 64 rows was open. The one thing worth checking carefully was the version: the attendance area lists three separate accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with an explicit warning that reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20, the current table was correct, but I read the legend-revision page to confirm that rather than assume it. "How much can I still be holding in January" reads like it might be asking about something time-specific (e.g. a mid-year rule), but it maps directly onto the row's "Carry-over limit" field — the amount of unused leave allowed to roll into the new year.
