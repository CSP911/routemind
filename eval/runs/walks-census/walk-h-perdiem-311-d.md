1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body

2. **Answer**: For grade G4, band B2, stay S2 (current table, in force from 2026-01-01): lodging cap is 307 USD per night. The receipt threshold is 42 USD — above that amount you must keep the receipt.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies for today's date, 2026-09-20)
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s2/body (the figures)

4. **Notes**: The expense area lists three overlapping documents for overseas per-diem (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) with an explicit warning that none of them mark themselves as superseded — the oldest says nothing about being replaced. It would have been easy to grab the first per-diem-looking table found without checking dates. The legend-revision page made clear that today's date (2026-09-20) falls under the current table `sec-hard-perdiem` (2026-01-01 onward), not the other two. The question already gave literal codes (G4/B2/S2), which matched the row naming directly, so no grade/band/stay legend lookup was needed beyond confirming the row existed.
