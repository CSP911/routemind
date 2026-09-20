1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body
```

2. **Answer**
The department head signs it off. Yes, two competing quotes are required. (Delegation limit for this row is 5,022 thousand KRW; expect 7 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the current table applies for a 2026-09-20 question)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body (final answer: department head, two quotes)

4. **Notes**
The approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) covering different date ranges, and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being replaced. Today's date (2026-09-20/21) falls cleanly under the current table (`sec-hard-threshold`, in force 2026-01-01 onward), so this wasn't actually ambiguous, but it would have been easy to skip the revision check and get the right answer for the wrong reason — or get a wrong answer on a rephrased question with an earlier date. The three legends (category/amount/term) each say plainly they are the "only place the mapping is written down," which made translating the plain-English question into the C2/V2/M3 row lookup unambiguous once found.
