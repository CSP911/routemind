1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B4, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night limit and receipt threshold are expense/business-trip topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_5aef51 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body

2. **Answer**: Lodging cap is 215 USD per night. A receipt is required above 55 USD.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body

4. **Notes**: The expense region's overlay listed twenty rows, including a "legend-revision" warning that overseas per-diem has three versions in effect at different date ranges (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` for 2026-01-01 onward), plus the superseded `hard-perdiem-v2` document itself sitting right next to the current one. It would be easy to grab a rate from the wrong version if not careful about today's date (2026-09-21). The row I read confirmed its own effective date range in its footer ("In force from 2026-01-01"), which matched today's date, so I did not need to open the superseded version or the legend-revision doc to be sure. The overlay-close step reported the used address as "reached... from somewhere the overlay never named," since I had only added the parent `/v1/regions/expense` table as a member, not the specific row — a minor mechanical note, not an error.
