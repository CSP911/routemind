1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V4, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold table by category, amount, and term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9b7f1e --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body

2. **Answer**: For category C4, amount V4, term M1: the department head signs it off (delegation limit 100,060 thousand KRW). Yes, other prices are required first — three competing quotes and a written comparison. Expect 11 working days.

3. **Source**: /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is current for today's date, 2026-09-21), /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body (the row with the actual figures).

4. **Notes**: The approval threshold subject has three versions in force at different dates (`threshold-table` until 2024-07-01, `hard-threshold-v2` from 2024-07-01 to 2025-12-31, `sec-hard-threshold` from 2026-01-01 onwards), and the legend-revision page warns the oldest version never says it was superseded — so grabbing the first "approval threshold" hit without checking dates would have been wrong for a 2025-dated question. Today's date (2026-09-21) falls cleanly in the current table's range, so this wasn't actually a close call here, but it was worth verifying rather than assuming "current" was right by default. The table at `/v1/nodes/sec-hard-threshold` is indexed directly by category/amount/term codes, so once I had the right table there was no ambiguity in finding the C4/V4/M1 row — the address encodes the three qualifiers exactly as given in the question.
