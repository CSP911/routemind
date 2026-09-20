1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

2. **Answer**
For type E1, tenure T4, site L4 (current table, in force since 2026-01-01): accrues 0.70 days per month, with a carry-over limit of 16 days — that is the most you can still be holding.

3. **Source**
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

4. **Notes**
The attendance area lists three versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), flagged by a legend-revision warning — it would be easy to grab a superseded row instead. The current table's own listing states it is in force from 2026-01-01, which covers today (2026-09-20), so no need to open the legend-revision file to confirm. The row already matched the exact codes given in the question (E1/T4/L4), so no site/tenure/type legend lookup was needed either. The "carry-over limit" field is what answers "how much can I still be holding in January" — the table doesn't separately break out a January-specific figure, so I'm reading carry-over limit as the answer to that half of the question.
