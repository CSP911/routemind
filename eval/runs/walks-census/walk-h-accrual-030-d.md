1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**: You accrue 0.64 days per month. The carry-over limit is 13 days — that is the most you can still be holding going into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**: The attendance area lists three leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, with an explicit warning that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so no ambiguity applied here, but it would have been easy to skip the legend-revision check and just grab the current table without confirming the date range — the warning page exists specifically because the older tables don't say they were superseded. The row itself reports a "carry-over limit," not an explicit "January" figure; I'm reading that carry-over limit as the answer to "how much can I still be holding in January" since that is the balance that survives into the new year. There was no separate January-specific cap anywhere in the row or its legends.
