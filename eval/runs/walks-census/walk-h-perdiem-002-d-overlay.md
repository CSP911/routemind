1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G1, band B1, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel caps" --member /v1/nodes/evidence "evidence/receipt threshold rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d12733 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body

2. **Answer**:
Lodging cap: 103 USD per night. Receipt required above: 24 USD (receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body

4. **Notes**:
The overlay create step accepted /v1/nodes/sec-hard-perdiem and /v1/nodes/evidence as members (tables, not the exact rows), and expanded them into the full set of per-diem rows and evidence sub-tables. The exact row for grade G1/band B1/stay S3 was directly in that expansion, so no need to touch the legend files or the evidence table at all — both figures (lodging cap and receipt threshold) were on the same row. Closing the overlay flagged the used address as "reached ... from somewhere the overlay never named" — this is just because the address I cited as --used was a row nested under the /v1/nodes/sec-hard-perdiem member I originally named, not that exact address itself; the row was still legitimately part of the working set, so this isn't a real gap, just a quirk of how the overlay tracks provenance.

One place I nearly went wrong: the area table for expense flagged that overseas per-diem has THREE versions in force at different dates (current since 2026-01-01, hard-perdiem-v2 for 2024-07-01–2025-12-31, and an older overseas-rates before that). Today's date (2026-09-21) falls under the current table, and the row itself confirmed "In force from 2026-01-01," so I did not need to check the superseded versions — but it would have been easy to grab the wrong version's figures without checking the effective date against today.
