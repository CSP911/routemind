1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C1, amount V3, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision "warning about three versions of threshold table, need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_be4125 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

2. **Answer**: For category C1, amount V3, term M3: the division director signs it off, and yes — three competing quotes are required before approval. (Delegation limit for this row: 20,010 thousand KRW; 10 working days to expect.)

3. **Source**: /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions applies as of today, 2026-09-21), /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body (the actual figures, in force from 2026-01-01).

4. **Notes**: The procurement table's approval-threshold entries carry an explicit warning (`hard-threshold-legend-revision`) that the subject has been written three times — a superseded 2024-07-01–2025-12-31 version (`hard-threshold-v2`) and an even older one (`threshold-table`) both still exist alongside the current one (`sec-hard-threshold`), and the oldest doesn't say it was replaced. It would have been easy to grab the first threshold row that matched C1/V3/M3 without checking which version's date range covers today (2026-09-21) — I confirmed the current table (in force 2026-01-01 onward) is the right one before reading the row. No other ambiguity: the question already used the table's own C1/V3/M3 notation, so no need to consult the amount/category/term legends to translate a real-world figure into a band.
