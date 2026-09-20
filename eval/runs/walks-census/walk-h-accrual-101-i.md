1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
Accrues 0.74 days of leave per month. Carry-over limit is 5 days — that is the most you can still be holding into January.
(This is under the current accrual table, in force 2026-01-01 onward, which covers today's date of 2026-09-20.)

3. **Source**
/v1/nodes/hard-accrual-legend-type/body (mapped "two-year contract" → type E2)
/v1/nodes/hard-accrual-legend-tenure/body (mapped "eight months" → tenure T1)
/v1/nodes/hard-accrual-legend-site/body (mapped "Busan branch" → site L2)
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body (the figures: 0.74 days/month accrual, 5-day carry-over limit)
/v1/nodes/hard-accrual-legend-revision/body (confirmed the current table, not v2 or the oldest, is the one that applies for a 2026-09-20 question)

4. **Notes**
- All three legend mappings landed on exact matches ("eight months" is literally tenure T1's wording, "Busan branch" is literally L2, "two-year contract" is literally E2) — no need to fall back to "nearest entry above it," which is good because that fallback rule is easy to misapply if you don't read the legend text carefully.
- The near-miss: there are three superseded/current versions of this table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page is explicit that "reaching for the newest is wrong for anything before 2026-01-01." I initially picked `sec-hard-accrual` from the table listing because it was flagged "THE CURRENT LEAVE ACCRUAL TABLE," but I went back and read the revision-legend page anyway to confirm the date test, since the question is date-sensitive and the table listing alone doesn't state the cutoff logic. Today (2026-09-20) and the "still be holding in January" (i.e. this coming January, still within 2026-01-01 onward validity) both fall inside the current table's range, so `sec-hard-accrual` was correct — but this is exactly the kind of question where grabbing the newest-looking table without checking the date would coincidentally still be right today, while being wrong methodology.
- "How much can I still be holding in January" reads ambiguously — it could mean a use-it-or-lose-it forfeiture date, a special January rule, or simply the standing carry-over limit. There was no separate January-specific rule anywhere in the row or legends; the carry-over limit field (5 days) is the only figure in this table that answers "how much you can still be holding" across a year boundary, so I've treated that as the answer. If RouteMind has a distinct forfeiture-deadline concept, it wasn't surfaced under this row or its legends.
