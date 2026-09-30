1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B1, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "per diem / hotel nightly cap and receipt threshold likely live under expense region"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_801dfa --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

2. **Answer**: For grade G2, band B1, stay S1 (overseas per-diem table in force from 2026-01-01): hotel/lodging cap is 159 USD per night. The receipt threshold is 22 USD — spend above that amount requires a receipt. (For context, meals are capped at 47 USD/day and incidentals at 9 USD/day, but those weren't asked.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

4. **Notes**: The overlay-close command required a `--used` list, and I included /v1/nodes/sec-hard-perdiem/body out of habit since I'd opened that table on the way in — but I only ever ran `table` on it, never `read`, so its body was never actually fetched. The tool flagged it back as "reached" (i.e. not something my navigation trail actually visited), which is a fair catch. The real, sole source of the answer is the row body itself. Otherwise this walk was straightforward: the expense region table named `sec-hard-perdiem` as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01" up front, so there was no ambiguity about superseded versions (`hard-perdiem-v2`, `overseas-rates`) applying instead — today's date (2026-09-21) falls inside the current table's validity window. The G2/B1/S1 row address was printed exactly as needed with no construction required.
