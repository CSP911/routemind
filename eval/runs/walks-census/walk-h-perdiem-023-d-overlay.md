1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B3, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are expense policy matters"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4d0284 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body

2. **Answer**:
Lodging cap: 139 USD per night. Receipt required above: 45 USD.

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body

4. **Notes**:
The overlay member I added (/v1/regions/expense) was a broad table, not the specific row — the CLI's close output flagged the row I actually used as "reached" (i.e., answered from somewhere the overlay never explicitly named as a member), since I drilled into /v1/nodes/sec-hard-perdiem and then the row without adding either as a formal overlay member. Worth noting for next time: add the row itself as a member before closing, to avoid that flag.

The bigger risk was version confusion: the table listing and the row body both warn that overseas per-diem has three historical versions (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem`/`hard-perdiem-row-*` set for 2026-01-01 onward). I nearly grabbed a stale version without checking the effective date. Today being 2026-09-21, the row read confirms it's "in force from 2026-01-01" with no end date, so it's current — but this is easy to get wrong if you don't check the revision note on the row itself.

Also possibly relevant: the question doesn't say "overseas," but grade/band/stay is specifically the overseas per-diem schema (domestic travel didn't turn up a matching grade/band/stay structure in the expense area), so I treated it as the overseas case.
