1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**: For category C4, amount V4, term M1 (delegation limit 100,060 thousand KRW): the department head signs it off. Yes, other prices are required first — three competing quotes plus a written comparison. Expect 11 working days.

3. **Source**:
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body (main answer)
/v1/nodes/hard-threshold-legend-revision/body (confirms the current table, in force since 2026-01-01, is the correct version for today's date, 2026-09-21)

4. **Notes**: The procurement table surfaced three versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), with an explicit warning file (`hard-threshold-legend-revision`) saying reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-21) is safely inside the current table's range, so no ambiguity in this case — but the row itself doesn't say which version's numbers apply, so skipping the revision-legend check would have been a guess rather than a verified answer. No confusion otherwise: the C4/V4/M1 address was printed exactly by the table listing, no construction needed.
