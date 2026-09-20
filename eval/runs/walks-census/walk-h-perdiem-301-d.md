1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body

2. **Answer**:
For grade G4, band B1, stay S2 (in force from 2026-01-01, current as of 2026-09-20): the hotel/lodging cap is 291 USD per night. A receipt must be kept for any single spend above 33 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body

4. **Notes**:
The expense area's table listing flags upfront that overseas per-diem has three versions in force at different times (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would have been easy to grab the older `hard-perdiem-v2` node (also listed directly under `/v1/regions/expense`) by mistake since it appears at the same level as the current table's entry point. Checked the row's own footer, which confirms it is the 2026-01-01 version and is current for today's date (2026-09-20), so no correction was needed. The G4/B1/S2 combination matched a single row directly with no ambiguity once the correct table (`sec-hard-perdiem`) was opened.
