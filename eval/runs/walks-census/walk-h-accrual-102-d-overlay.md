1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E2, tenure T1, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - has the monthly accrual figure" --member /v1/nodes/hard-accrual-legend-revision/body "warns about three versions of accrual rules, need to confirm current version applies"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_58a5b6 --outcome answered --used /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E2, tenure T1, site L3 (current table, in force from 2026-01-01): you accrue 0.76 days per month, and the carry-over limit is 6 days — that is the most you can still be holding in January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body (accrual and carry-over figures)
/v1/nodes/hard-accrual-legend-revision/body (confirms which version applies for today's date, 2026-09-21)

4. **Notes**
The opened overlay only had two named members (the parent table `sec-hard-accrual` and the revision-legend page); the exact E2/T1/L3 row lived one level below the table I named, so the close command recorded it as "reached" rather than a listed member. Worth naming the exact row address as a member next time instead of the parent table, to avoid that mismatch.

The near-miss worth flagging: this domain has three superseded versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend page is explicit that grabbing the newest is wrong for any question dated before 2026-01-01. Today's date (2026-09-21) is safely inside the current table's range, so no correction was needed here, but it would have been easy to skip that check and just assume "current" without confirming the date actually falls in the current version's window.

"How much can I still be holding in January" reads slightly ambiguous — it could mean a carry-over/rollover cap (what I answered) or a running balance projection. The row's field is explicitly labeled "Carry-over limit, days," which matches the carry-over reading, so I went with that.
