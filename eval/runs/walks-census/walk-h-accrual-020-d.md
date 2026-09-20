1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

2. **Answer**
For type E1, tenure T3, site L1 (current table, in force since 2026-01-01, which applies to today's date 2026-09-20): accrues 0.56 days per month, with a carry-over limit of 10 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body (the figures)

4. **Notes**
The attendance area has three separate versions of the leave accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and none of the older ones say they've been superseded. It would have been easy to just grab whichever row looked closest without checking dates. I read the legend/revision note first to confirm that for a question asked on 2026-09-20, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one — not the 2024-07-01–2025-12-31 version. The row for E1/T3/L1 existed directly under that current table, so no interpolation across legends was needed. The only remaining ambiguity is semantic: the table's field is literally "Carry-over limit," and I'm reading "how much can I still be holding in January" as asking for that cap, since carry-over is what determines the balance you're allowed to hold across the year boundary into January. The table doesn't separately describe a "January" checkpoint, so this is an inference, not a directly quoted answer to that exact phrasing.
