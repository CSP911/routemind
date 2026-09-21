1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G1, band B3, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel nightly cap and receipt threshold" --member /v1/nodes/evidence "evidence/receipt rules table, may hold the general receipt-required threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_828527 --address /v1/nodes/evidence --why "row already gives its own receipt threshold; general evidence table not needed"
./bench/rmcli.py overlay close --id ov_2026-09-21_828527 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body

2. **Answer**: Lodging cap is 127 USD per night. A receipt must be kept for any single spend above 36 USD (the receipt threshold). (For context, this is the per-diem table in force from 2026-01-01.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body

4. **Notes**: The expense area table listed the per-diem table (`sec-hard-perdiem`) as a table of legends plus one row per grade/band/stay combination, so I added it to the working set expecting to have to open a sub-table — but it turned out the overlay itself expanded directly to all the individual row addresses, including the exact one needed (G1/B3/S1), so no extra table hop was needed. I initially also added the general `/v1/nodes/evidence` table to the working set in case the receipt threshold was a company-wide rule rather than something in the per-diem row itself; it turned out the per-diem row carries its own "Receipt threshold" figure (36 USD), so the evidence table was unnecessary and I removed it before closing. Worth flagging: the expense table's own description warns that overseas per-diem has multiple superseded versions (`hard-perdiem-v2`, `overseas-rates`) alongside the current one (`sec-hard-perdiem`, in force from 2026-01-01) — it would be easy to grab a stale version by mistake if not reading the "WHY" column carefully.
