1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

2. **Answer**
You accrue 1.52 days of leave per month. The carry-over limit is 10 days, so that is the most you can still be holding into January (any unapproved excess above that is settled at 10 and the rest is not recoverable).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed the current, 2026-01-01-onward table applies to today's date)
- /v1/nodes/hard-accrual-legend-type/body ("here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here five years" → tenure T3, exact match)
- /v1/nodes/hard-accrual-legend-site/body ("at the Seoul office" → site L1, exact match)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body (final figures: 1.52 days/month accrual, 10-day carry-over limit)

4. **Notes**
The main trap was the accrual subject having three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no warning on the oldest page that it had been replaced — the legend-revision page was the only thing that made it safe to trust the current table for today's date (2026-09-20). It would have been easy to just grab `sec-hard-accrual` without checking, and in this case it happened to be right, but that's luck, not method.
The other near-miss: all three qualifiers ("partner firm", "five years", "Seoul office") happened to be exact matches in their legends, so there was no need to invoke the "take the nearest entry above" fallback — but I checked all three legends fully before assuming that, since a partial match could easily have sent this to the wrong row silently.
"How much can I still be holding in January" reads like it could be asking about a carryover/expiry deadline rather than the carry-over limit itself, but the accrual row's "Carry-over limit, days" field is the only figure in the sourced documents that answers "how much can you hold," so I've treated that as the answer rather than chasing a separate expiry-date page.
