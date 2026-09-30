1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G1, band B4, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, likely has hotel nightly cap" --member /v1/nodes/hard-perdiem-legend-revision/body "explains which per-diem version covers which dates, need to confirm current version applies" --member /v1/nodes/evidence "evidence table may state receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_17003a --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body

2. **Answer**:
Lodging (hotel), per night: 147 USD.
Receipt required above: 48 USD (the receipt threshold).
This is from the per-diem table in force from 2026-01-01, which is the current version as of today (2026-09-20/21).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body

4. **Notes**:
The expense area's table flags up front that overseas per-diem has three versions with different figures (current `sec-hard-perdiem` since 2026-01-01, superseded `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and an older `overseas-rates`), so I deliberately added the revision-legend doc to the working set to confirm which one applies before trusting a number — it would have been easy to grab a superseded row by mistake. In the end I didn't need to open the legend separately: the row itself states "In force from 2026-01-01" and names the superseded versions, which was enough to confirm currency given today's date. I also pulled in the `evidence` table on the guess that the receipt threshold might live there instead, but the per-diem row already carries its own "Receipt threshold" field, so evidence wasn't needed. Opening `/v1/regions/expense` immediately surfaced grade/band/stay rows for G1/B4/S2 by name, so no guessing of the address was required.
