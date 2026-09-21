1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T3, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carryover/cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e1b3aa --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

2. **Answer**:
For type E4, tenure T3, site L2 (current table, in force from 2026-01-01):
- Accrues 1.54 days per month.
- Carry-over limit (the most that can still be held) is 11 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

4. **Notes**:
There are three versions of the leave accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend-revision doc warns explicitly that the oldest version never states it was superseded — so grabbing the first hit by name would be wrong for an older date. Today's date (2026-09-20/21, both given in this session) falls after the 2026-01-01 cutover, so the current table `sec-hard-accrual` is correct here; no date arithmetic was actually needed for this question, but it would have been easy to skip the legend-revision check and not realize that mattered. The question gives all three qualifiers (E4/T3/L2) directly in code form, so no legend lookup for site/tenure/type translation was needed — the row `hard-accrual-row-type-e4-tenure-t3-site-l2` matched exactly. I read "how much can I still be holding in January" as asking for the carry-over limit (the cap on days held across the year boundary into January), which is the field literally labeled "Carry-over limit, days" in the row — this seemed like the only field that fits that phrasing, but it's a judgment call since the doc doesn't use the word "January" anywhere.
