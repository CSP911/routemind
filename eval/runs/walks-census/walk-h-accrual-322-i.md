1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body
```

2. **Answer**
Under the current leave accrual table (in force since 2026-01-01, applicable to today's date 2026-09-20): you accrue **1.56 days per month**. The carry-over limit is **12 days** — that is the most you can still be holding once the new year turns over (into January).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here five years" → tenure T3)
- /v1/nodes/hard-accrual-legend-site/body (mapped "Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body (final row: monthly accrual and carry-over limit)

4. **Notes**
- The legend-revision warning page was the thing to check first: leave accrual has three superseded/current versions, and grabbing the newest table without checking the date would have been a mistake for a question dated earlier than 2026-01-01. Today (2026-09-20) falls in the current table's range, so `sec-hard-accrual` was correct — but it wasn't safe to assume that without reading the revision page.
- All three qualifier phrases in the question happened to match the legend wording almost verbatim ("here from our partner firm" = E4, "been here five years" = T3, "in the Singapore entity" = L3), so there was no ambiguity or nearest-match judgment call needed here — a cleaner-than-usual walk.
- "How much can I still be holding in January" reads like it might be asking about a separate carryover/expiry policy page, but the row itself already answers it directly via "Carry-over limit, days" — no need to chase a separate node for that.
