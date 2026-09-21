1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Jakarta, junior analyst, one night: hotel per diem cap and receipt threshold" --member /v1/regions/expense "how much a business trip pays, and receipt rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a9b299 --outcome answered --used /v1/regions/expense /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body

2. **Answer**: Hotel (lodging) cap is 127 USD per night. Receipts must be kept for any single spend above 36 USD (the receipt threshold). This is under the current overseas per-diem table, in force from 2026-01-01, grade G1 (junior analyst), band B3 (Jakarta), stay S1 (one night).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body (lodging 127 USD/night, receipt threshold 36 USD)

4. **Notes**: The expense area has three separate documents for "overseas per-diem" (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and a warning page explicitly flags that grabbing the newest one is wrong for anything dated before 2026-01-01. Today (2026-09-21) is safely inside the current table's range, but it would have been easy to skip the revision-legend check and just grab `sec-hard-perdiem` on the assumption "current" always means "right one" — the warning page exists specifically because that assumption breaks for 2025-dated questions. The per-diem row is indexed by three separate codes (grade/band/stay) each resolved through its own legend table rather than by plain-language lookup, so all three legends had to be read before the row address could be assembled correctly.
