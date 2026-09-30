1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G2, band B3, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "expense row covers business trip pay and receipt rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6a6685 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging (hotel), per night: 203 USD. Receipt threshold: 49 USD (a receipt must be kept for any spend above this amount).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body
/v1/nodes/hard-perdiem-legend-revision/body

4. **Notes**:
The expense area holds three separate versions of this per-diem table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision doc warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded — so an unwary reader could easily cite the wrong one without ever suspecting it. Today's date (2026-09-21) falls after 2026-01-01, so `sec-hard-perdiem` (the current, three-qualifier table) is correct, and its per-row page even ends with "the difference is not recoverable" / exception language that's worth knowing exists but wasn't asked for here. The overlay's close command reported the two addresses I used as "reached" rather than as named members — I had only added the parent `/v1/regions/expense` row to the working set, not the specific leaf addresses, so this is just the tool noting the overlay membership wasn't updated as I drilled down; the answer itself is unaffected.
