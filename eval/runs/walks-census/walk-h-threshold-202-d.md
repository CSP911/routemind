1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body
```

2. **Answer**
For category C3, amount V1, term M3 (delegation limit 1,034 thousand KRW): the **department head** signs it off. No, you do not have to get other prices first — competing quotes required: **none**. Expect 4 working days.

3. **Source**
- `/v1/nodes/hard-threshold-legend-revision/body` (confirmed which of the three threshold-table versions applies to today's date, 2026-09-20/21)
- `/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body` (the answer itself)

4. **Notes**
The procurement table lists three approval-threshold documents side by side (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with only truncated descriptions — easy to grab the wrong one. The legend-revision page exists specifically to warn that the oldest version "says nothing at all about having been replaced," so picking by recency alone would have been a mistake for older dates; for today's date the current table (`sec-hard-threshold`, in force from 2026-01-01) is correct, but I only trusted that after reading the revision legend rather than assuming. Once inside `sec-hard-threshold`, the row address was predictable from the category/amount/term codes (`hard-threshold-row-category-c3-amount-v1-term-m3`), so I read it directly instead of opening the three separate legend files for category/amount/term — those legends are only needed if you don't already know your C/V/M codes, which the question here supplied directly.
