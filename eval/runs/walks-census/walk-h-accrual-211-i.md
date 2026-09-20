1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

2. **Answer**
You accrue 1.14 days of leave per month, and can hold at most 8 days of carried-over leave into January (the carry-over limit).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onwards table is the right version for today's date, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body (three days a week → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (two years → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (Busan branch → site L2)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body (accrual rate and carry-over limit)

4. **Notes**
The main hazard here was the three-version accrual history flagged by `hard-accrual-legend-revision`: reaching for the newest table without checking dates is explicitly called out as wrong for pre-2026 questions. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct — but this required a deliberate check rather than an assumption. The other near-miss was reading the accrual table's row index too literally: the 64 rows are addressed by codes (E/T/L numbers), not by the plain-language descriptions in the question, so each of the three qualifiers ("three days a week," "two years," "Busan branch") had to be run through its own legend file before the right single row could be addressed — skipping any one of the three legends would have made it impossible to construct a valid row address. "How much can I still be holding in January" was interpreted as the carry-over limit (8 days), since that is the only figure in the row governing how much leave may persist past year-end; the table does not separately name a "January" figure.
