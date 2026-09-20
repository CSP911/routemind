1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body

2. **Answer**
Accrues 1.12 days per month. The carry-over limit is 7 days — that is the most you can still be holding into January (any unapproved excess above that is settled and not recoverable).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms which of the three accrual versions applies for a 2026-09-20 question — the current one)
- /v1/nodes/hard-accrual-legend-type/body ("in three days a week" → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body ("at the Seoul office" → site L1)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body (1.12 days/month accrual, 7-day carry-over limit)

4. **Notes**
Leave accrual has three superseded/current versions indexed under different node names (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page explicitly warns that grabbing the newest one is wrong for any date before 2026-01-01, and that the oldest version doesn't announce that it was ever replaced. Since today is 2026-09-20 the current table applies, but this was the one place I could have silently gotten a stale answer if I'd skipped that check.

The bigger trap was the three qualifier phrases in the question mapping to codes that aren't obviously in the order you'd expect: "in three days a week" (a part-time schedule) maps to an *employment type* code (E3), not a tenure or site code — it sits in the same legend table as "on a two-year contract" (E2), which is easy to confuse with the "been here two years" *tenure* fact (T2) elsewhere in the question. The two "two-year" phrases in the prompt — one about contract type, one about tenure — point at two different legends and two different codes; conflating them would have picked the wrong row entirely. The three legends had to be read in full and cross-checked against the exact wording ("on a two-year contract" vs. "been here two years") before combining into e3-t2-l1.

The question's second half ("how much can I still be holding in January") is really asking about the carry-over limit, not a separate January-specific rule — there's no distinct "January" figure in the row; the carry-over limit is presumably the balance you can still be holding once the year rolls over.
