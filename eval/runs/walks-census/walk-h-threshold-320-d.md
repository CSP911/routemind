1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body

2. **Answer**
For category C4, amount V3, term M1 (current table, in force from 2026-01-01): the department head signs it off. Yes, other prices are required first — three competing quotes. Delegation limit is 20,056 thousand KRW, and 8 working days should be expected.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-21)
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body (the answer)

4. **Notes**
The procurement area lists three versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded. Today's date (2026-09-21) falls in the current version's range (2026-01-01 onward), so `sec-hard-threshold` was correct, but this was the one place I could easily have gone wrong by skipping the revision check and just grabbing the newest table without confirming the date actually falls in its range. No other ambiguity — the C4/V3/M1 row was named directly and matched the question's codes exactly, and it answers both parts of the question (signer, and quotes-first requirement) in one place.
