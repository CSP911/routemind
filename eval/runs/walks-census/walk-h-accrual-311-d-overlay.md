1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T2, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carryover/holding cap by employee type, tenure, site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c88cec --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

2. **Answer**:
For type E4, tenure T2, site L2 (current table, in force since 2026-01-01):
- Accrues 1.46 days per month.
- Carry-over limit (the cap on what can still be held over into January) is 8 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

4. **Notes**:
The near-miss here was version confusion: the attendance overlay surfaces three separate accrual documents (`hard-accrual-v2`, the legend-revision warning, and `sec-hard-accrual`), and grabbing the wrong one is easy since they all sound current. The legend-revision page makes clear that `sec-hard-accrual` is the only one valid for a question dated in 2026 (in force from 2026-01-01), so I checked it before reading the actual E4/T2/L2 row. The "January" phrasing in the question is really just asking about the carry-over limit (the amount you can still be holding over into the new year), not a separate figure — the row's table has exactly one field for that, "Carry-over limit, days," so no separate lookup was needed. The row was reachable directly from the `sec-hard-accrual` table listing by its type/tenure/site-coded address, no legend lookups needed since the three qualifiers were already given in E4/T2/L2 form.
