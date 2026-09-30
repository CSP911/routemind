1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B4, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, likely has hotel nightly cap" --member /v1/nodes/evidence "evidence table may define the receipt-required threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e01392 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body

2. **Answer**: Lodging cap is 271 USD per night. A receipt must be kept for any spend above 53 USD (the receipt threshold). (For reference, this row also lists meals at 98 USD/day and incidentals at 20 USD/day, and is in force from 2026-01-01.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body

4. **Notes**: The overlay-create step named two candidate members from the region table (`/v1/nodes/sec-hard-perdiem` and `/v1/nodes/evidence`), expecting a generic evidence table might hold the receipt threshold. But opening the overlay showed the per-diem table decomposes into one row per grade/band/stay combination, and the exact row for G3/B4/S1 was already printed by address — no need to open the generic `sec-hard-perdiem` table or the `evidence` table separately, since the row itself carries its own "Receipt threshold" field. The one thing worth flagging: the expense area lists three versions of the overseas per-diem (a legend-revision warning, a superseded v2 for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` table for 2026-01-01 onward). Today's date (2026-09-21) falls under the current table, so no ambiguity here, but a careless reader could easily grab the superseded v2 figures instead — the version warning is easy to skim past.
