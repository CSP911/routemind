1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B1, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense region covers business trip pay and receipt rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_fdae74 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 107 USD per night. The receipt threshold is 27 USD — above that amount, evidence/receipt must be kept.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/sec-hard-perdiem
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

4. **Notes**: The expense region table surfaces three separate overseas per-diem documents (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) that all cover the same subject but for different date ranges, and the oldest one gives no indication it was superseded — reading the legend-revision node first was necessary to avoid grabbing a stale version. Since today's date (2026-09-20/21) falls after 2026-01-01, `sec-hard-perdiem` is the correct current table. Once there, the grade/band/stay combination in the question maps to an exact row (`hard-perdiem-row-grade-g1-band-b1-stay-s4`) with no interpolation needed, so this was a clean single-row lookup once the correct table version was identified.
