1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G4, band B3, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "business trip / per diem / hotel allowance and receipt threshold rules"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a571bd --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 331 USD per night. Receipt threshold: 57 USD (must keep the receipt for spend above this amount).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body (the figures)
/v1/nodes/hard-perdiem-legend-revision/body (confirms this current table, in force from 2026-01-01, is the correct version for today's date, 2026-09-21)

4. **Notes**:
The overseas per-diem subject has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), each covering a different date range, and the oldest one gives no indication it was ever replaced. It would have been easy to grab the row from an outdated version without checking. I confirmed today's date (2026-09-21) falls under the current table (2026-01-01 onwards) before trusting the figures. The row itself directly matched the three qualifiers (G4/B3/S4) with no ambiguity in the legend or lookup.
