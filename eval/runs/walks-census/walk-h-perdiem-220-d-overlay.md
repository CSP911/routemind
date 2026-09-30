1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B3, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, likely holds hotel caps" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three per-diem versions with different dates - need to confirm which applies to today 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cc57c4 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 255 USD per night. The receipt threshold is 44 USD — a receipt must be kept for any spend above that amount. (For reference, the row also carries meals at 84 USD/day and incidentals at 17 USD/day.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body (the figures); /v1/nodes/hard-perdiem-legend-revision/body (confirmed this current table, in force from 2026-01-01, is the correct version for today's date, 2026-09-20 — not the superseded `hard-perdiem-v2` or the oldest `overseas-rates`).

4. **Notes**: The expense region table flags up front that overseas per-diem has three superseding versions with different effective-date ranges, and the older versions don't say anywhere in themselves that they've been replaced — so opening the wrong one wouldn't self-correct. I nearly skipped the version check since I opened the row I needed (`sec-hard-perdiem`) directly by its "in force since 2026-01-01" label, but I pulled the revision legend anyway to confirm rather than assume, since the row's own footer only names the other two versions without stating a hard cutover date rule. The row itself did double as confirmation (footer states "In force from 2026-01-01"), so today's date clears it. One oddity: `overlay close` reported the row address as "reached" rather than "member" even though it was inside the `sec-hard-perdiem` table member I'd added — the overlay apparently tracks membership at the table level I named, not at the individual row I actually read, so citing a specific row under a table member shows up as "reached" rather than a clean match. Not an error, just worth knowing if closing output is being audited literally.
