1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G1, band B4, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel nightly cap" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of 3 versions with different dates, need to confirm which is current" --member /v1/nodes/evidence "evidence/receipt requirement rules, may state the threshold above which a receipt is required"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8a3a5c --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

2. **Answer**:
Lodging cap: 155 USD per night. Receipt threshold: 54 USD (a receipt must be kept for any spend above this amount).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

4. **Notes**:
Creating the overlay against the parent table (/v1/nodes/sec-hard-perdiem) rather than the specific grade/band/stay row turned out fine — opening the overlay printed every individual row under it, including the exact G1/B4/S4 row, so I could read it directly. But the overlay's close command then flagged it as "reached" rather than a named member, since I'd never added that specific row address as a member — worth adding the specific row as a member next time to keep the overlay's own bookkeeping accurate, even though the answer itself was unaffected.

The expense region's table description explicitly warned that overseas per-diem has an older, superseded band-only cap still present in the table listing (hard-perdiem-v2, and legend-revision flagging three total versions). I added the legend-revision doc as a working-set member specifically to guard against citing a stale figure, but the row I read stated its own effective date directly ("In force from 2026-01-01"), which matches today (2026-09-21) and is the current version per the region table's note ("current table since 2026-01-01"), so I didn't need to open the legend-revision or v2 docs to confirm. Also added the evidence table as a member in case the receipt threshold lived there instead of in the per-diem row, but the per-diem row already carried its own "Receipt threshold" field, so evidence/ was unused.
