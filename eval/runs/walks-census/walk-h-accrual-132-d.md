1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E2, tenure T4, site L3: accrues 1.00 day per month. Carry-over limit is 15 days — that is the most you can still be holding in January (i.e., the cap on what carries over into the new year).

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body
/v1/nodes/hard-accrual-legend-revision/body (used to confirm the current table applies for today's date, 2026-09-20)

4. **Notes**
The table at /v1/nodes/sec-hard-accrual already indexes rows by type+tenure+site, so the address for E2/T4/L3 was printed directly — no need to consult the separate site/tenure/type legend files. The one place this could have gone wrong: there are three versions of the leave accrual page (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the revision note is explicit that reaching for the newest is only correct for dates from 2026-01-01 onward — for a 2025-dated question the middle version would be the right answer, not the current one. Since today is 2026-09-20, the current table was correct here, but I checked the revision note before finalizing rather than assuming. The question's phrasing ("how much can I still be holding in January") maps to "carry-over limit" in the table — there's no separate figure elsewhere for a January-specific cap, so I read this as the standard carry-over limit that applies at year-end/into January.
