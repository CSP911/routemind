1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "August 2025 nightly lodging cap for grade 2 traveller to band B2 destination, under version in force on that date" --member /v1/nodes/hard-perdiem-legend-revision/body "explains which per-diem version covers which date range" --member /v1/nodes/hard-perdiem-v2/body "version in force 2024-07-01 to 2025-12-31, covers August 2025" --member /v1/nodes/sec-hard-perdiem "current table from 2026-01-01, not in force in Aug 2025 but useful to confirm which is superseded"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3dbaa8 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD nightly lodging cap (grade G2, band B2), under the "Overseas per-diem, second version" (in force 2024-07-01 to 2025-12-31).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body
- /v1/nodes/hard-perdiem-v2/body

4. **Notes**: The overseas per-diem topic has three separate versions written at different times (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page is explicit that reaching for the newest table is wrong for any date before 2026-01-01, and that the oldest version says nothing about having been superseded — so a date check against the legend is mandatory, not optional. When I created the working-set overlay, adding the current table's address (/v1/nodes/sec-hard-perdiem) auto-expanded into dozens of individual grade/band/stay row addresses (the G1–G4 × B1–B4 × S1–S4 rows) that all belong to the *current* (2026-01-01+) table, not the version in force in August 2025 — it would have been easy to grab one of those close-looking G2/B2 rows by mistake instead of reading the v2 document, which reports the answer as a single grade×band matrix (no stay dimension) with no per-row addresses. I did not use any of those expanded rows, only the legend and the v2 body.
