1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body

2. **Answer**:
For category C2, amount V4, term M2 (current table, in force from 2026-01-01): the division director signs it off. Yes, other prices are required first — three competing quotes plus a written comparison. (Delegation limit: 100029 thousand KRW; working days to expect: 12.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body (the answer)

4. **Notes**:
The procurement region lists both the current threshold table and two superseded versions (`hard-threshold-v2`, `threshold-table`) side by side with no obvious visual distinction — it would be easy to grab a row from `hard-threshold-v2` by mistake since its row-naming pattern is similar. The legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded, so checking it before reading a row was necessary rather than optional. Today's date (2026-09-21) falls cleanly in the "2026-01-01 onwards" bracket so the current table (`sec-hard-threshold`) was correct, but the deliberate trap in the setup (three versions, no self-declared obsolescence) made it worth confirming explicitly rather than assuming the first table listed was current. The row itself directly matched the C2/V4/M2 qualifiers given in the question, so no legend lookups for category/amount/term codes were needed.
