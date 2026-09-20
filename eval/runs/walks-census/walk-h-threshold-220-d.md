1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body

2. Answer
For category C3, amount V3, term M1 (delegation limit 20,040 thousand KRW), the document is signed off by the department head. Yes, other prices are required first: three competing quotes.

3. Source
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions is current for today's date, 2026-09-21)
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body (the answer)

4. Notes
The procurement table's listing flagged up front that the approval threshold subject has been written three times (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), with a warning that "the oldest says nothing at all about having been replaced" — so grabbing the first plausible-looking threshold table without checking the legend-revision page would silently give a stale answer. Checked that page before opening the row and confirmed 2026-09-21 falls in the "2026-01-01 onwards" band, so `sec-hard-threshold` was the right table. The row itself was a direct, unambiguous hit — C3/V3/M1 matched the address exactly, so no need to consult the category/amount/term legends to translate qualifiers.
