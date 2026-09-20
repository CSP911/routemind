1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

2. **Answer**: For category C4, amount V3, term M2 (current table, in force from 2026-01-01): the **department head** signs it off. Yes, other prices are required first — **three competing quotes**. (Delegation limit 20,057 thousand KRW; 9 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date, 2026-09-20/21)
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body (the answer)

4. **Notes**: The procurement region has three versions of the approval threshold subject (pre-2024-07-01, 2024-07-01–2025-12-31, and current since 2026-01-01), and the legend-revision page warns explicitly that the oldest version doesn't flag itself as superseded — reaching for it or assuming "newest is always right" would be wrong for a question dated in 2025. Today's date (2026-09-20/21) falls under the current table (`sec-hard-threshold`), so no trap here, but the check was necessary. Once inside `sec-hard-threshold`, the row address `hard-threshold-row-category-c4-amount-v3-term-m2` matched the question's qualifiers exactly, so no need to consult the amount/category/term legends to translate plain-language qualifiers into codes — the question already gave codes directly.
