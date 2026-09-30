1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V3, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - likely has the answer" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions - need to confirm which is in force today"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b390b5 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body

2. **Answer**:
For category C4, amount V3, term M3 (current table, in force since 2026-01-01): the division director signs it off, and yes — three competing quotes are required before signing (delegation limit 20,058 thousand KRW; 10 working days to expect).

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onward table applies to today's date)
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body (the actual figures)

4. **Notes**:
The procurement table listed three separate threshold pages (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with a warning that the subject "has been written three times" and the oldest never says it was superseded. It would have been easy to grab the current table on reflex without checking, but the legend-revision page is explicit that a 2025-dated question needs the middle version, not the newest — so checking today's date (2026-09-20/21, well after the 2026-01-01 cutover) against that table was a necessary step, not a formality. Once inside `sec-hard-threshold`, the overlay's expansion of that table member directly produced the exact three-qualifier row (C4/V3/M3), so no ambiguity there — the row name maps 1:1 to the question's inputs.
