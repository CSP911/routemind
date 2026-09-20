1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
```

2. **Answer**
For type E4, tenure T4, site L1: you accrue 1.60 days of leave per month. You can carry over (hold) up to 13 days into January — the carry-over limit.

3. **Source**
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body (accrual rate and carry-over limit)
- /v1/nodes/hard-accrual-legend-revision/body (confirms this current table, in force from 2026-01-01, is the correct version for today's date, 2026-09-20)

4. **Notes**
The E4/T4/L1 qualifiers happened to match the address naming exactly, so no legend lookups for site/tenure/type codes were needed here — that won't always be true. The bigger risk was version: leave accrual has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version says nothing about being replaced, so grabbing the first accrual-looking row without checking the revision legend could silently give a stale answer. Since today is 2026-09-20 (well within the 2026-01-01-onwards window), the current table was correct, but I verified this explicitly rather than assuming "current" is always right. The "how much can I still be holding in January" phrasing maps to "Carry-over limit, days" in the table — it's not spelled out as a January-specific figure, so it would be easy to go looking for a separate "January" row that doesn't exist.
