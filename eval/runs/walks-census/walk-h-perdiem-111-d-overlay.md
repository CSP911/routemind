1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B2, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are expense policy"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_94eb15 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body

2. **Answer**: Lodging cap of 179 USD per night; receipts must be kept for any single spend above 34 USD (the receipt threshold).

3. **Source**:
/v1/nodes/sec-hard-perdiem/body (table listing, confirmed this is the current per-diem table, in force from 2026-01-01)
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body (the row with the actual figures)

4. **Notes**: The table of areas surfaced /v1/regions/expense as the only plausible match for hotel/receipt questions, and opening it listed a `sec-hard-perdiem` table alongside two older, explicitly superseded per-diem documents (`hard-perdiem-v2`, covering 2024-07-01 to 2025-12-31) and a warning node (`hard-perdiem-legend-revision`) flagging that overseas per-diem has three versions with different figures. It would have been easy to grab a superseded version by mistake — the current table's own header states "in force from 2026-01-01," which matches today's date (2026-09-21), so I used that one and didn't need to open the revision-legend warning or the v2 doc at all. The row address itself already spelled out grade/band/stay exactly as asked (g2/b2/s2), so no legend lookups (grade/band/stay definitions) were needed either — the question came pre-coded. One thing worth flagging for whoever reads this: the row also has an "If the figures are exceeded" section describing an approval/exception process, which wasn't asked about, so I left it out of the answer.
