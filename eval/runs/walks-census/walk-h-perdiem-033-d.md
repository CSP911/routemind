1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

2. **Answer**:
For grade G1, band B4, stay S4 (current table, in force from 2026-01-01): lodging cap is 155 USD per night, and the receipt threshold is 54 USD — above that amount a receipt must be kept.
(For context: meals are 95 USD/day and incidentals are 19 USD/day, though these weren't asked.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

4. **Notes**:
The question gave grade/band/stay codes directly (G1, B4, S4), so there was no need to consult the legend files (hard-perdiem-legend-grade/band/stay) that translate job titles/destinations/trip lengths into these codes — I went straight to the matching row in the 64-row table.

The main hazard here was version confusion: the expense table listing explicitly warns that overseas per-diem has three versions with different dates (current since 2026-01-01, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). It would be easy to grab a stale rate from one of the superseded documents if scanning quickly. I confirmed I used `sec-hard-perdiem`, explicitly labeled as THE CURRENT table and in force from 2026-01-01, which covers today's date (2026-09-20).

The document itself also lists a "receipt threshold" alongside lodging/meals/incidentals — it would be easy to misread "receipt threshold" as an unrelated evidence rule (there's a separate `/v1/nodes/evidence` table for evidence generally), but here it's a per-diem-specific figure sitting right in the same row, so no cross-reference was needed.
