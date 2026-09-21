1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B2, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel/per diem and receipt threshold are expense policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7de5bc --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body

2. **Answer**: Lodging cap is 111 USD per night. A receipt must be kept for any spend above 27 USD (the receipt threshold).

3. **Source**:
/v1/nodes/sec-hard-perdiem (table, to locate the row)
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body (the answer)

4. **Notes**: The `sec-hard-perdiem` table lists a row for exactly grade G1, band B2, stay S1 by name, so no legend lookup (grade/band/stay code translation) was needed — the question already gave codes, not job titles or city names. The table's own warning is worth flagging: there are three versions of this per-diem table (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` in force from 2026-01-01). Today is 2026-09-21, so the current table is correct, but a careless walk could have grabbed the superseded `hard-perdiem-v2` row instead since it was listed as a sibling member in the initial overlay and has the same row-naming pattern — worth double-checking the "in force from" date on whichever row you land on. Also note: I never added the specific row address as an overlay member before closing (I got there via `table`/`read` navigation, not `overlay add`), so the close command reported both used addresses as "reached" rather than "used" — functionally fine but a reminder that the working set is meant to be updated with `add`/`remove` as you narrow, not just implicitly discovered.
