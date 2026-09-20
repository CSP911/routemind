1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

2. **Answer**: Lodging (hotel) cap is 279 USD per night. The receipt threshold is 59 USD — spend above that amount requires a receipt to be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

4. **Notes**: The question's grade/band/stay codes (G3, B4, S3) were given directly, so no legend lookup was needed to translate job title/destination/trip length into codes — the row was reachable in one direct step from the sec-hard-perdiem index. The one place this could have gone wrong: the expense area lists three versions of the overseas per-diem (a legend-revision warning, a superseded v2 table for 2024-07-01–2025-12-31, and the current sec-hard-perdiem table effective 2026-01-01). Today's date (2026-09-20) falls under the current table, so sec-hard-perdiem was correct, but it would be easy to grab the superseded hard-perdiem-v2 node by mistake since it sits right next to the current one in the expense area listing. Also worth flagging: the row bundles a single "Receipt threshold" figure alongside lodging/meals/incidentals rather than a hotel-specific threshold, so the answer treats that 59 USD as the applicable general threshold — the document doesn't separately break the threshold out per spend category.
