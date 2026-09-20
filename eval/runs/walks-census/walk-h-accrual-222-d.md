1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body
./bench/rmcli.py table /v1/nodes/sec-days-that-decide-money

2. Answer:
For type E3, tenure T3, site L3 (current table, in force since 2026-01-01):
- Accrues 1.24 days per month.
- Carry-over limit: 12 days — this is the cap on how much accrued leave you can still be holding (e.g. going into January).

3. Source:
/v1/nodes/hard-accrual-legend-revision/body (confirms which version applies for a 2026-09-20 question)
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body (accrual rate and carry-over limit)

4. Notes:
The attendance area lists three separate versions of the leave accrual page (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), with an explicit warning that the oldest version never says it was superseded — it would be easy to land on the wrong one without checking the legend-revision page first. Today's date (2026-09-20) puts this squarely in the current table (`sec-hard-accrual`), so that ambiguity didn't end up mattering here, but it's the kind of thing that silently gives a wrong answer if skipped.
The row for E3/T3/L3 exists directly and only had one plausible read, so no legend lookups for type/tenure/site codes were needed. The one soft spot is the phrase "how much can I still be holding" — I read this as the carry-over limit (12 days), since that's the only figure in the row describing a maximum balance rather than a rate. I did check the "days that decide money" table in case there was a January-specific carryover rule, but it only covers joining/leaving-month proration, trip allowances, and unused-leave payout — nothing about a carry-over deadline or a different figure for January specifically. So the carry-over limit from the accrual row is the best answer, but it's implicit rather than explicitly tied to the word "January."
