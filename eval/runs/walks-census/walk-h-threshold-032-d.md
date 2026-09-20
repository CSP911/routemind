1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body

2. **Answer**
For category C1, amount V4, term M3 (current table, in force from 2026-01-01, which applies to today's date 2026-09-20): the division director signs it off. Delegation limit is 100,014 thousand KRW, and yes — three competing quotes plus a written comparison are required before this can be signed. Working days to expect: 13.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (established which version applies for today's date)
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body (the row with the answer)

4. **Notes**
The procurement region's landing page flags up front that approval-threshold data has three superseding versions, and the oldest one gives no indication it was ever replaced — so checking the legend-revision page before reading a row was necessary, not optional. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-threshold` is the right one; grabbing the first "approval threshold" row found without checking the version legend would have risked silently pulling from `hard-threshold-v2` or the original `threshold-table` instead. The C1/V4/M3 combination pointed to an exact, individually-addressed row in the current table, so no interpretation of the legends for category/amount/term codes was needed here — the codes were given directly in the question.
