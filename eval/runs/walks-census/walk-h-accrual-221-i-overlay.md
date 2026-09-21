1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 5 years tenure, Busan branch: monthly leave accrual rate and max carryover balance in January" --member /v1/regions/attendance "leave accrual and carryover rules"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_677530 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

2. **Answer**
Accrues 1.22 days per month. Maximum carry-over balance is 11 days — that is the most that can still be held once January arrives.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

4. **Notes**
This subject has three superseded versions of the same table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. With today's date at 2026-09-20/21, the current table (`sec-hard-accrual`, in force from 2026-01-01) is correct — but it would have been easy to skip that check and grab whichever version turned up first. "How much can I still be holding in January" is not a separate lookup — it's the carry-over limit column on the same row, worded as if it were about a future point in time rather than a table field. Read literally it could be mistaken for a request to project a running balance, but the row's own field name ("Carry-over limit, days") settles it: it's the cap, not a balance forecast, and the table gives no data (current PTO balance) to compute a forecast from anyway. The three qualifiers (E3 = three days a week, T3 = five years, L2 = Busan branch) each required a legend lookup since none of the row addresses are guessable — the task's ban on constructing addresses was correctly a strict requirement, since the row IDs are only discoverable via the type/tenure/site legend tables.
