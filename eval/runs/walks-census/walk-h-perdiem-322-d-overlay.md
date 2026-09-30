1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B3, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip pay / hotel per diem and receipt threshold likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_56517a --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body

2. **Answer**: Lodging cap is 327 USD per night. The receipt threshold is 54 USD — above that amount a receipt must be kept.

3. **Source**:
/v1/nodes/sec-hard-perdiem (table, confirmed this is the current overseas per-diem table, in force from 2026-01-01)
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body (the row itself, with the figures)

4. **Notes**: The overlay I created only listed /v1/regions/expense as a member, but the row I actually needed (hard-perdiem-row-grade-g4-band-b3-stay-s3) came from opening the sec-hard-perdiem table directly rather than being added as an overlay member first — the close command flagged these as "reached" rather than pre-named, which is accurate. The grade/band/stay naming in the question is a giveaway for this exact table (it's the only one in the working set indexed by those three codes), so this walk was short and unambiguous. One thing worth flagging: the region table's warning that overseas per-diem has three versions (current sec-hard-perdiem, superseded hard-perdiem-v2, and an older overseas-rates) — I did not open hard-perdiem-legend-revision to double check version boundaries, but the row's own footer states it is "in force from 2026-01-01" with no end date, and today is 2026-09-21, so it's current. Did not need to check receipt/evidence rules elsewhere since the per-diem row states its own receipt threshold directly.
