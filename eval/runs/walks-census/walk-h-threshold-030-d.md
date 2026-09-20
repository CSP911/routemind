1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body

2. **Answer**:
For category C1, amount V4, term M1 (current table, in force from 2026-01-01, which applies to today's date 2026-09-20): the department head signs it off. Yes, other prices are required first — three competing quotes and a written comparison. Delegation limit is 100012 thousand KRW, and 11 working days should be expected.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies to 2026-09-20)
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body (the answer)

4. **Notes**:
The procurement area holds three generations of the approval threshold table (old, v2, and current), and the oldest one gives no indication it was ever superseded — the legend-revision page is explicit that you have to check the date rather than assume the newest table applies. Today (2026-09-20) falls under the current table (`sec-hard-threshold`, since 2026-01-01), so that was the correct one to use; it would have been easy to grab `hard-threshold-v2` by mistake since it sorts near the current table in the listing. Once inside `sec-hard-threshold`, the row addresses are literal — `hard-threshold-row-category-c1-amount-v4-term-m1` — so C1/V4/M1 matched directly without needing to consult the amount/category/term legend files.
