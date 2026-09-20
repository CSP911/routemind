1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
For category C3, amount V4, term M3 (current table, in force from 2026-01-01): the division director signs it off. Yes — three competing quotes plus a written comparison are required before this can be approved. (Delegation limit is 100046 thousand KRW; 13 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m3/body
/v1/nodes/hard-threshold-legend-revision/body (used to confirm the current table, not the superseded ones, applies to today's date)

4. **Notes**
The procurement area flags that approval thresholds have THREE historical versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and warns that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20/21) falls inside the current version's range, so `sec-hard-threshold` was the right table — but this is exactly the kind of question where grabbing the first plausible row without checking the revision legend would silently give a stale, superseded answer. I checked the legend explicitly rather than assuming. The row itself directly named both parts of the question (signer, and quote requirement) with no ambiguity once the right version was confirmed.
