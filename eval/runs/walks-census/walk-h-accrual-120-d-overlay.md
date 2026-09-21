1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T3, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "attendance area covers leave accrual and balance rules"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_8b0a45 --outcome answered --used /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

2. **Answer**:
- Accrues 0.88 days per month.
- Carry-over limit (the most you can still be holding, e.g. going into January) is 10 days.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

4. **Notes**:
The attendance area's working set surfaced a legend node warning that leave accrual has THREE versions with different figures (`hard-accrual-legend-revision`, `hard-accrual-v2`, and the current `sec-hard-accrual`). It would have been easy to grab the wrong version. Today's date (2026-09-20/21) falls within the current table's stated force period ("in force from 2026-01-01"), and the row itself repeats that same in-force date, so I used the current table without needing to open the superseded versions. The row also confirms the qualifiers (type E2, tenure T3, site L1) select it directly — no legend lookups were needed since the question already gave codes rather than descriptions. "How much can I still be holding" was read as the carry-over limit field rather than the notice-required or accrues-during-unpaid-leave fields, which is the natural reading of "holding" as an accumulated balance.
