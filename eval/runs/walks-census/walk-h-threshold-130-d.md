1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body

2. **Answer**:
For category C2, amount V4, term M1 (current table, in force from 2026-01-01): the department head signs it off. Yes, other prices are required first — three competing quotes and a written comparison are needed before sign-off. (Delegation limit: 100028 thousand KRW; working days to expect: 11.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirms which version applies for today's date, 2026-09-20/21)
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body (the row with the answer)

4. **Notes**:
The procurement table warns up front that approval thresholds have three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards) with the same subject and no explicit "superseded" marking on the oldest — so grabbing the first threshold-looking table found would risk citing the wrong version. Checked the legend-revision page before reading any row to confirm today's date (2026-09-20/21) falls in the current version's range, which pointed to `sec-hard-threshold` rather than `hard-threshold-v2` or the original `threshold-table`. The three-part address (category-amount-term) meant the row was addressable directly from the table listing without needing to consult the amount/category/term legend files, since C2/V4/M1 were already given in the question in the table's own coding.
