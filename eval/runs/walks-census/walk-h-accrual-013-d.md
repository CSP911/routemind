1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body

2. **Answer**: You accrue 0.54 days per month, and can carry over (hold) up to 10 days into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies for today's date)
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body (monthly accrual rate and carry-over limit)

4. **Notes**: The attendance table lists three separate accrual documents — `leave-accrual`, `hard-accrual-v2`, and `sec-hard-accrual` — each covering a different date range, with a warning that the oldest one never says it was superseded. It would have been easy to grab the wrong version if I hadn't checked the legend-revision page first; since today is 2026-09-20, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one. The row for E1/T2/L4 existed directly at a predictable address, so no legend lookups for type/tenure/site codes were needed. The only interpretive step was reading "carry-over limit" as the answer to "how much can I still be holding in January" — the table doesn't spell out that the carry-over limit is specifically a January figure, but that's the only field describing a maximum balance you're allowed to hold rather than an ongoing monthly rate, so it's the natural fit.
