1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body
```

2. **Answer**
The team lead signs it off. Yes, you need to get other prices first — two competing quotes are required. (Delegation limit for this row is 5,020 thousand KRW; expect about 5 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body

4. **Notes**
The procurement table listing made clear there are three versions of the approval threshold (current since 2026-01-01, a superseded 2024-07-01–2025-12-31 version, and an older one still). Today's date (2026-09-21) falls inside the current version's range, so I used `sec-hard-threshold`, not `hard-threshold-v2`. Easy to go wrong here if you grab the first threshold-looking node instead of checking which is actually in force.

The row address isn't guessable from the question text — it has to be assembled from three separate legend lookups (category, amount, term), each of which maps a plain-English description to a code letter/number. "A consultant's time" → C2, "roughly 3 million won" → V2, "just the once" → M1. None of these codes are obvious without reading all three legends first; I did not construct the row address until I had all three confirmed.
