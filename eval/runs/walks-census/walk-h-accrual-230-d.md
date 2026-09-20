1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E3, tenure T4, site L1: accrues 1.28 days per month, with a carry-over limit of 13 days (the most you can be holding over into January).

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body (used to confirm the current table, in force since 2026-01-01, is the right version for a question dated 2026-09-20 and for January)

4. **Notes**
The attendance area's table listing flags up front that leave accrual has THREE superseded versions (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), with an explicit warning not to assume the newest applies. It would have been easy to skip that check and just grab the current row — in this case the current table is correct since both today's date and the January in question fall in the 2026-01-01-onwards range, but the legend-revision page was worth reading to confirm that rather than assume it. No ambiguity in matching E3/T4/L1 to a row — the table is indexed exactly by those three qualifiers and the address printed directly.
