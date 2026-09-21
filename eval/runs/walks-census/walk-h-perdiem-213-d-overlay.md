1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B2, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01" --member /v1/nodes/hard-perdiem-legend-revision "explains which per-diem version covers which dates - need to confirm current table applies"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_192172 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging: 251 USD per night. Receipt threshold: 44 USD (a receipt must be kept for any spend above this amount).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s4/body
/v1/nodes/hard-perdiem-legend-revision/body

4. **Notes**:
The expense area's table listing flagged up front that overseas per-diem has three versions in force over different date ranges, with the older ones still present and not marked as withdrawn. That's the trap: a careless read could grab `hard-perdiem-v2` (2024-07-01 to 2025-12-31) or the oldest `overseas-rates` table by mistake, or fail to check at all. Today's date (2026-09-21) falls in the "2026-01-01 onwards" window, so the current three-qualifier table (`sec-hard-perdiem`) is the right one — confirmed by reading `hard-perdiem-legend-revision` explicitly rather than assuming. The G3/B2/S4 row was found directly under `sec-hard-perdiem` without needing the grade/band/stay legend files, since the question already gave all three qualifiers in the table's own notation.
