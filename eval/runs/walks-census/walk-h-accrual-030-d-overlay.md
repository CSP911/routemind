1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T4, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carry-forward cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e18d3e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

2. **Answer**
Accrues 0.64 days per month. Carry-over limit (the most you can still be holding into January) is 13 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

4. **Notes**
The attendance area holds three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the oldest one gives no indication it was superseded — reading the legend-revision note first was necessary to avoid picking the wrong version. Today's date (2026-09-21) falls after the 2026-01-01 start of the current table, so `sec-hard-accrual` was correct. Once the version was settled, the row for E1/T4/L1 was a direct, unambiguous lookup — no need to consult the type/tenure/site legends since the question already gave the codes. The "carry-over limit" field in the row is what answers "how much can I still be holding in January" — the table doesn't label it as a January-specific figure, but carry-over limits by definition describe what may still be held at year turnover, so this is the intended match.
