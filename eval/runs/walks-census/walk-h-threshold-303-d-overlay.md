1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V1, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is the likely home for signature + competitive pricing requirement"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cd4159 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body

2. **Answer**:
For category C4, amount V1, term M4 (delegation limit 1,051 thousand KRW): signed off by the department head. Competing quotes required: none — no other prices need to be obtained first. Expect 5 working days.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current table applies for today's date, 2026-09-21)
/v1/nodes/sec-hard-threshold (located the specific C4/V1/M4 row address)
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body (the answer)

4. **Notes**:
The procurement region has three versions of the approval threshold table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the oldest version says nothing about being superseded — reaching straight for the newest table without checking the legend-revision page would have worked out fine here only by luck, since today (2026-09-21) falls in the current version's range. Checked the legend-revision page explicitly before trusting `sec-hard-threshold` rather than assuming. No ambiguity in the row lookup itself — the table listed all 64 rows by exact category/amount/term address, so C4-V1-M4 was a direct match with no guessing required.
