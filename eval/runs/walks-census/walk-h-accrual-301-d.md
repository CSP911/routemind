1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body

2. **Answer**
For type E4, tenure T1, site L2: you accrue 1.38 days per month. The carry-over limit is 5 days — that is the most you can still be holding once the new year (January) starts.

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body
(/v1/nodes/hard-accrual-legend-revision/body used only to confirm the current table applies for a 2026-09-20 question)

4. **Notes**
The attendance table lists three accrual documents with different validity windows (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and a warning page says the oldest one never states it was superseded. It would have been easy to grab the first accrual-looking row found without checking dates. Checked the legend-revision page first: today (2026-09-20) falls in the 2026-01-01-onwards window, so `sec-hard-accrual` is correct and the other two versions were not opened.

The E4/T1/L2 combination was an exact, direct row in the 64-row table — no interpolation or legend lookup for type/tenure/site codes was needed since the codes were given verbatim in the question.

"How much can I still be holding in January" reads as asking about the carry-over limit (5 days), i.e., the cap on unused leave rolled into the new year — this table doesn't separately break that out by month, so this is the only figure in this row that answers a January-specific cap.
