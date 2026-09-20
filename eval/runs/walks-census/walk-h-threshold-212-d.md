1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m3/body

2. **Answer**
For category C3, amount V2, term M3 (current table, in force from 2026-01-01): the department head signs it off. Yes, other prices are required first — two competing quotes. Delegation limit is 5,038 thousand KRW; expect 7 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-20/21, falls under the current version, not the superseded ones)
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m3/body (the answer)

4. **Notes**
The procurement table lists three versions of the approval threshold (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), and the table listing itself warns that reaching for the newest is wrong for dates before 2026-01-01. It would have been easy to grab `hard-threshold-v2` by mistake since it sorts before the current table and its description also looks plausible at a glance — I checked the legend-revision page explicitly before reading a row to confirm today's date (2026-09-20/21) belongs to the current (2026-01-01 onwards) version. No ambiguity once that was checked: the row for C3/V2/M3 was a single unambiguous file.
