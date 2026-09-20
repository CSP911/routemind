1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body

2. **Answer**
For type E2, tenure T2, site L1 (current table, in force since 2026-01-01):
- Accrues 0.80 days of leave per month.
- Carry-over limit is 7 days — that is the most that can still be held (carried into January).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed the current, 2026-01-01-onward table applies to today's date)
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body (the figures)

4. **Notes**
Attendance has three versions of the leave-accrual table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the revision-legend page warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest page never says it was superseded. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`), so that was the correct one — but it would have been easy to skip the legend check and just grab whichever row looked newest without confirming the date rule. The question's phrasing ("how much can I still be holding in January") maps directly onto the row's "Carry-over limit" field — there's no separate January-specific figure, so I treated the carry-over limit as the answer to that half of the question rather than searching further for a January-specific rule.
