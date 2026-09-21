1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E1, tenure T4, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e0c157 --outcome answered --used /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

2. **Answer**: For type E1, tenure T4, site L4 (current table, in force from 2026-01-01): accrues 0.70 days per month. Carry-over limit is 16 days — this is the most that can still be held (i.e. the cap on the balance carried into the new year, January).

3. **Source**: /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

4. **Notes**: The overlay I created only listed /v1/nodes/sec-hard-accrual as a member, but opening that table itself printed the full set of per-type/tenure/site rows as its contents (not as overlay members) — the exact row for E1/T4/L4 was one of those, so I read it directly rather than adding it to the overlay first. Closing the overlay flagged this as "reached" (answered from an address the overlay never explicitly named) rather than "used," which is accurate bookkeeping but worth noting since it looked at first like the row should have been a first-class member. The question's phrase "how much can I still be holding in January" is not spelled out anywhere as a January-specific rule — the table has no month-of-year distinctions, so I read it as asking about the general carry-over limit (16 days), which is the cap on leave balance regardless of month. If RouteMind intended a January-specific reset/proration rule, I did not find one in this row or in the legend/revision files I skipped past.
