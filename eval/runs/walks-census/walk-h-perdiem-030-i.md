1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: A junior analyst on a one-night stay in Dhaka can claim up to 143 USD per night for lodging. Any spend above 45 USD requires a receipt (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body
/v1/nodes/hard-perdiem-legend-revision/body (confirms the current table applies for a 2026-09-20 question)

4. **Notes**: The top-level expense table lists two other per-diem documents (`hard-perdiem-v2` and a legend-revision file) alongside the current `sec-hard-perdiem` table, with a loud warning that there are three versions with different date ranges — it would have been easy to grab the wrong one, or to assume "current" without checking the date against the revision legend. Since today is 2026-09-20, the current table (in force 2026-01-01 onward) is correct, but this is exactly the trap the revision doc warns about for anyone answering an older-dated question. The per-diem row's "Receipt threshold" field answers the receipt part of the question directly — I didn't need to visit the separate `evidence` table, since the row itself carries that figure alongside the lodging cap.
