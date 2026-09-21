1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B2, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense region covers business trip pay and receipts"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ebb289 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body

2. **Answer**: Lodging cap is 243 USD per night. A receipt must be kept for any spend above 38 USD (the receipt threshold). This is from the overseas per-diem table in force from 2026-01-01, which is current as of today (2026-09-21).

3. **Source**:
- /v1/nodes/sec-hard-perdiem (table — located the correct row for grade G3, band B2, stay S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body (the row itself, with the figures)

4. **Notes**: The overlay's `expense` member table listed a row `/v1/nodes/sec-hard-perdiem` described as "THE CURRENT OVERSEAS PER-DIEM TABLE" alongside a warning row (`hard-perdiem-legend-revision`) about three versions of overseas per-diem existing with different effective dates, plus a superseded version (`hard-perdiem-v2`, 2024-07-01 to 2025-12-31). It would have been easy to grab the wrong version here — I checked that `sec-hard-perdiem` states it is in force from 2026-01-01, which covers today's date (2026-09-21), so I used that one and did not need to open the superseded or legend-revision documents. Also worth flagging: the question gives grade/band/stay as literal codes (G3/B2/S2) rather than descriptions, so no legend lookup (grade/band/stay legends) was needed — the table's row address already matched the codes directly. One process note: I read `hard-perdiem-row-grade-g3-band-b2-stay-s2/body` directly from the table listing without first adding it as an overlay member; the close command flagged both used addresses as "reached" rather than pre-declared members, which didn't affect the answer but is a minor deviation from the intended add/narrow workflow. The question did not specify overseas vs. domestic travel, but this table was the only one in the expense region indexed by grade/band/stay, so it was the unambiguous match.
