1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T4, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap are attendance topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_123e61 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body

2. **Answer**:
Accrues 1.30 days per month. Carry-over limit (the most that can still be held going into January) is 14 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions applies to today's date)
- /v1/nodes/sec-hard-accrual (located the specific row for type E3, tenure T4, site L2)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body (the figures: 1.30 days/month accrual, 14-day carry-over limit)

4. **Notes**:
The attendance area has three separate versions of the leave-accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend-revision document warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls inside the current table's range (2026-01-01 onwards), so `sec-hard-accrual` was correct here, but this is an easy place to go wrong on a question dated in 2025 — it would need `hard-accrual-v2` instead. The question already gave the row codes (E3, T4, L2) directly, so no legend lookup for type/tenure/site translation was needed. I read "how much can I still be holding in January" as asking for the carry-over limit (the cap on days held across the year boundary into January), which is exactly the "Carry-over limit, days" field in the row — there was no separate "January" field, so this interpretation seemed to be the intended match rather than an exact literal one.
