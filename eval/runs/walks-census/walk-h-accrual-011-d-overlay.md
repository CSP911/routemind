1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E1, tenure T2, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site since 2026-01-01 - likely has monthly accrual rate and cap"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body
./bench/rmcli.py read /v1/nodes/sec-days-that-decide-money/body
./bench/rmcli.py overlay close --id ov_2026-09-20_539a32 --outcome answered --used /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
For type E1, tenure T2, site L2: accrues 0.50 days per month, with a carry-over limit of 8 days. (Notice required to book leave: 3 working days; this type does not accrue during unpaid leave.)

3. **Source**:
- /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body (the figures)
- /v1/nodes/hard-accrual-legend-revision/body (confirms the current table, in force from 2026-01-01, is the right version for today's date, 2026-09-20)

4. **Notes**:
The overlay table listed exactly the row matching E1/T2/L2 by name, so no legend lookup was needed to translate a job title/city/tenure length into codes — the question already gave the codes directly. I still checked hard-accrual-legend-revision to make sure the current table (sec-hard-accrual, effective 2026-01-01) rather than an older superseded version (hard-accrual-v2 or leave-accrual) was the right one for today's date; it was.

The "how much can I still be holding in January" phrasing had me second-guessing whether it meant something calendar-specific — like a year-end carry-over rule tied to a January cutoff, distinct from the row's flat "carry-over limit" figure. I checked sec-days-that-decide-money (about proration in joining/leaving months and payouts for unused leave) on the chance there was a separate January-specific carry-over rule, but it only covers proration and payout timing, not a carry-over cap — nothing there contradicted or supplemented the row's carry-over limit. I'm treating "carry-over limit, 8 days" as the direct answer to "how much can I still be holding," since that's the only cap this table defines and there's no separate January-specific figure anywhere in this area.
