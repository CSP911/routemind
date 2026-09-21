1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B1, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per night cap and receipt threshold likely live in expense/travel rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2bb2ab --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 235 USD per night. Receipts must be kept for any spend above 35 USD (the receipt threshold). (For context, this row also carries a meal allowance of 71 USD/day and incidentals of 14 USD/day.)

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body

4. **Notes**: The expense region's table listed twenty candidate rows, but only one, `/v1/nodes/sec-hard-perdiem`, was described as "THE CURRENT OVERSEAS PER-DIEM TABLE" and indexed by grade/band/stay codes exactly matching the question's shape (G3, B1, S4), so it was an easy pick — I never had to touch the other 19 members. The row itself flags that there are three versions of this table (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and this one from 2026-01-01), which is where I nearly went wrong: had today's date (2026-09-21) fallen before 2026-01-01, this exact row would have been the wrong version and I'd have needed `hard-perdiem-v2` or `overseas-rates` instead. I checked the in-force date against today before trusting the figures. Also: I never added the specific row address as an overlay member before reading it (I drilled into it via the `sec-hard-perdiem` table listing instead), so the close command reported it as "reached" rather than a named member — harmless here, but worth noting for the overlay's own bookkeeping.
