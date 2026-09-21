1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B4, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "per diem, hotel cap, and receipt threshold are expense policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_70925e --outcome answered --used /v1/regions/expense /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body

2. **Answer**: Lodging cap is 275 USD per night. A receipt must be kept for any spend above 56 USD (the receipt threshold). This is the current overseas per-diem table, in force from 2026-01-01.

3. **Source**:
/v1/regions/expense
/v1/nodes/sec-hard-perdiem
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s2/body

4. **Notes**: The expense table's overlay listed two per-diem-related warning files (`hard-perdiem-legend-revision/body` and `hard-perdiem-v2/body`) alongside `sec-hard-perdiem`, flagging that overseas per-diem has three versions with different rates. It would have been easy to grab a superseded row by mistake. I confirmed `sec-hard-perdiem` is explicitly labeled "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01" and today's date (2026-09-21) falls inside that window, so no need to open the legend-revision or v2 documents — the grade/band/stay codes given in the question (G3/B4/S2) matched a row address exactly, so no legend lookup was needed either.
