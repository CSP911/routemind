1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B3, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per night cap and receipt threshold for travel likely under expense/business trip rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c67ea1 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body

2. **Answer**:
Lodging cap: 191 USD per night. Receipt required above 40 USD (the receipt threshold). (For context, the same row also lists meals at 75 USD/day and incidentals at 15 USD/day, effective from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body

4. **Notes**:
The overlay's opening member (/v1/regions/expense) was a coarse first guess — the real answer lived several hops deeper, under /v1/nodes/sec-hard-perdiem, which is the current overseas per-diem table (in force from 2026-01-01) indexed directly by grade/band/stay codes. That table listed the exact row (grade-g2-band-b3-stay-s1) as one of 64, so no legend lookups were needed since the question already gave codes rather than a country or job title.

One thing that could easily trip someone up: /v1/nodes/hard-perdiem-legend-revision warns there are THREE versions of the overseas per-diem table (current from 2026-01-01, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). Since today is 2026-09-21, the current table is the right one, but I didn't actually open the revision-legend doc — I inferred the effective date was fine because the row body itself stated "In force from 2026-01-01" and named the two older/superseded versions, which was enough to confirm freshness without a separate hop.

Also worth flagging: the overlay close command reported the used address as "reached ... from somewhere the overlay never named" — I read the row directly via the table listing rather than first adding it as an explicit overlay member. The working set was still useful for orientation but I skipped narrowing it with an explicit add before reading, which the tool flagged as a minor procedural gap (not an accuracy issue).
