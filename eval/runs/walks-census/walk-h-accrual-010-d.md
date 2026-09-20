1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

2. **Answer**: For type E1, tenure T2, site L1 (current table, in force from 2026-01-01): accrues 0.48 days per month. The carry-over limit is 7 days — that is the most you can still be holding in January (i.e., the cap on what carries over into the new year).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to a 2026-09-20 question)
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body (the figures)

4. **Notes**: The attendance area warns up front that leave accrual has three versions with different effective dates, and the legend-revision page stresses not to reach for the newest table by default. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is the right one — but this is the exact trap the page calls out, and it was worth confirming explicitly rather than assuming "current" is always correct. The question already gave codes in the table's own notation (E1, T2, L1), so the row was a direct hit in the table listing with no need to consult the site/tenure/type legend files to translate plain-language descriptions into codes — on a question phrased in plain language, those legends would be required reading first.
