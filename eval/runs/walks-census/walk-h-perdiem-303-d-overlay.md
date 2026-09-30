1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B1, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense region covers business trip payment amounts and receipt rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ac352f --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 299 USD per night. A receipt must be kept for any spend above 39 USD (the receipt threshold).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s4/body

4. **Notes**: The initial overlay member was the broad `/v1/regions/expense` table, not a specific row — the exact grade/band/stay row wasn't addressable until drilling into `/v1/nodes/sec-hard-perdiem`, whose listing of 64 rows made the G4/B1/S4 row directly visible and obviously the right pick. Worth flagging: the expense region's row list also surfaced `hard-perdiem-legend-revision` (warning of THREE per-diem table versions across different date ranges) and `hard-perdiem-v2` (superseded, in force 2024-07-01 to 2025-12-31) alongside `sec-hard-perdiem` (current, in force from 2026-01-01). It would be easy to grab the wrong version if not reading the "in force" dates carefully — today (2026-09-21) falls under `sec-hard-perdiem`, confirmed by the footer note on the row itself ("In force from 2026-01-01"), so I did not need to open the superseded v2 table. Also note: `overlay close` reported the used address as "reached" rather than a named member — I read the row directly from the sub-table listing without a separate `overlay add` step, so the close command flagged it as reached-but-unnamed rather than a pre-added member. The answer itself is unambiguous once the correct row is found: a clean two-column table with no conflicting figures elsewhere in the row.
