1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Junior analyst, Jakarta, 3-week trip: hotel nightly cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel nightly cap" --member /v1/nodes/evidence "evidence table may state receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_75b55d --address /v1/nodes/qualified-evidence --why "row itself states the receipt threshold, no need for general evidence table"
./bench/rmcli.py overlay remove --id ov_2026-09-21_75b55d --address /v1/nodes/sec-evidence-in-awkward-cases --why "not needed, threshold answered directly by per-diem row"
./bench/rmcli.py overlay close --id ov_2026-09-21_75b55d --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body

2. **Answer**: Hotel (lodging) cap is 139 USD per night. A receipt must be kept for any spend above 45 USD. (This is the current table, in force since 2026-01-01: junior analyst = grade G1, Jakarta = band B3, three weeks = stay S4.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → S4)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body (lodging cap 139 USD/night, receipt threshold 45 USD)

4. **Notes**: The expense area table flagged up front that overseas per-diem has three superseded versions (legend-revision, hard-perdiem-v2, and an older one) — easy to grab a stale row by accident if you don't check dates. I went straight for /v1/nodes/sec-hard-perdiem, described as "the current table since 2026-01-01," and the row itself confirmed "In force from 2026-01-01" against today's date (2026-09-21), so no need to open the superseded versions or the revision-legend file. The other overlay member I picked, /v1/nodes/evidence, turned out unnecessary — the per-diem row already carries its own "Receipt threshold" figure, so the general evidence/qualifying-evidence tables would have been redundant. Removing those two addresses from the overlay failed with a 404 ("not in this overlay") — they were sub-rows of a table member, not top-level overlay members, so they couldn't be removed directly; this didn't block closing the overlay against what was actually used. One thing worth flagging: the three-week stay banded exactly to "S4 = three weeks" in the legend, so no rounding judgment call was needed there, unlike Jakarta/junior analyst which were also exact matches.
