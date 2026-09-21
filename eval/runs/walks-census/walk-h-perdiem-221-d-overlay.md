1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B3, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are expense/travel policy matters"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_40e179 --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body

2. **Answer**: Lodging (hotel) cap is 259 USD per night. The receipt threshold is 47 USD — above that amount, evidence/receipt must be kept. (For reference, the same row also lists meals at 89 USD/day and incidentals at 18 USD/day, but those weren't asked.) This is the current overseas per-diem table, in force from 2026-01-01, which covers today's date (2026-09-21).

3. **Source**:
/v1/nodes/sec-hard-perdiem (table, to locate the row)
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body (the figures)

4. **Notes**: The expense region's overlay listed a `hard-perdiem-legend-revision` node warning that overseas per-diem has three versions with different dates (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` table from 2026-01-01). It would be easy to grab the wrong version if working from stale memory or an old bookmark — I confirmed `sec-hard-perdiem` is described as "THE CURRENT" table and its date range (from 2026-01-01) covers today, so no version ambiguity here. The G3/B3/S2 row matched the question's qualifiers exactly, so no legend lookups (grade/band/stay definitions) were needed. One oddity: `overlay close --used` reported both addresses as "reached" rather than matched members, since I never explicitly ran `overlay add` for them before closing — cosmetic, didn't affect the answer.
