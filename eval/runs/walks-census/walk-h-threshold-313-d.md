1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body
```

2. **Answer**
For category C4, amount V2, term M4 (current table, in force from 2026-01-01): the division director signs it off. Yes — two competing quotes are required before that signature. Delegation limit is 5,055 thousand KRW, and 8 working days should be expected.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body (the figures)

4. **Notes**
The procurement area holds three versions of the approval threshold (oldest `threshold-table`, middle `hard-threshold-v2`, current `sec-hard-threshold`), and the legend page warns the oldest version never says it was superseded — it would be easy to grab the wrong one by just picking the first plausible-looking table. Checking the legend-revision page first (rather than assuming "current" = correct) confirmed today's date, 2026-09-21, falls under the current table `sec-hard-threshold` (in force from 2026-01-01), so no ambiguity here — but the walk would have been genuinely wrong if the question had been dated in 2025. No other confusion: the row address for C4/V2/M4 was printed directly in the table listing, so no guessing or address construction was needed.
