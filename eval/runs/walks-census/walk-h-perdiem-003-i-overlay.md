1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Junior analyst, Tokyo, 3 weeks: hotel nightly cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel cap" --member /v1/nodes/evidence "receipt/evidence threshold for what needs to be kept"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_c4f1ef --address /v1/nodes/qualified-evidence --why "domestic KRW evidence-qualification ceiling, not the overseas per-diem USD receipt threshold — wrong table for this question"
./bench/rmcli.py overlay close --id ov_2026-09-21_c4f1ef --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

2. **Answer**
Hotel (lodging) cap: 107 USD per night. Receipt must be kept above 27 USD (the receipt threshold on this same row). This is grade G1 (junior analyst) × band B1 (Tokyo) × stay S4 (three weeks), from the per-diem table in force since 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

4. **Notes**
The expense area's table listed a `/v1/nodes/evidence` table for "what has to be attached for a spend to be accepted," which looked like the natural place for a receipt threshold. Following it led to `/v1/nodes/qualified-evidence` → `qualified-list/body`, which gives a receipt-keeping ceiling of 30,000 KRW — but that is the general domestic simple-receipt-vs-qualifying-evidence rule, priced in Korean won, unrelated to an overseas Tokyo trip. It would have been an easy wrong answer to staple onto the per-diem hotel figure. The actual receipt threshold for this trip is sitting right on the per-diem row itself (27 USD), in the same currency and scope as the lodging cap, so I used that instead and dropped the KRW table from the overlay with a reason.

Also worth flagging: the expense table's own description warns that overseas per-diem has three superseded versions (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and an older `overseas-rates`). I went straight for `sec-hard-perdiem`, described as "in force from 2026-01-01," and didn't open the older versions — today being 2026-09-21, that's clearly current, but on a question near a boundary date this is where I'd have had to check the revision-legend doc first.
