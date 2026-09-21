1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B4, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip hotel per diem and receipt requirement"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4cdf80 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 151 USD per night. A receipt must be kept for any spend above 51 USD (the receipt threshold).

3. **Source**:
- /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body (lodging cap 151 USD/night, receipt threshold 51 USD)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem table versions applies for today's date, 2026-09-21)

4. **Notes**: The expense region's overlay surfaces three separate per-diem documents at once — `hard-perdiem-legend-revision` (a warning), `hard-perdiem-v2` (explicitly superseded), and `sec-hard-perdiem` (current). It would be easy to grab `hard-perdiem-v2` by mistake since it sits right next to the current table with a similar name and no obvious flag in the listing itself. The legend-revision doc is what actually disambiguates: it states the current table (`sec-hard-perdiem`) covers 2026-01-01 onward, and since today is 2026-09-21, that's the right one — the older `hard-perdiem-v2` (2024-07-01 to 2025-12-31) would have been wrong. Also worth flagging: the row address itself (`hard-perdiem-row-grade-g1-band-b4-stay-s3`) directly encodes grade/band/stay, so once inside `sec-hard-perdiem` the match was exact and required no legend lookups for G1/B4/S3 individually. The overlay close command reported these two addresses as "reached" rather than tracked members, since I navigated to them via `table`/`read` rather than an explicit `overlay add` — worth doing the add step next time to keep the working set accurate.
