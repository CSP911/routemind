1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body

2. **Answer**:
For grade G3, band B4, stay S1 (current table, in force from 2026-01-01): lodging cap is 271 USD per night. Receipts must be kept for any spend above 53 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s1/body

4. **Notes**:
The expense area's table listing flagged that overseas per-diem has THREE versions in force over different date ranges (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), which is the easiest way to grab a superseded rate by accident. I deliberately picked `sec-hard-perdiem`, labeled as the table in force from 2026-01-01, since today is 2026-09-20 and falls within that range — no need to open the superseded versions. The row itself also states its own effective date (2026-01-01) and names the two earlier versions, which double-confirms it's current. Nothing else in the walk was ambiguous — the region table pointed straight to /v1/regions/expense, and the row address for G3/B4/S1 was printed exactly as needed.
