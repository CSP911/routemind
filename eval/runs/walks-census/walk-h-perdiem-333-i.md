1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py table /v1/nodes/evidence
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py read /v1/nodes/sec-hard-perdiem/body

2. **Answer**:
Hotel (lodging) cap: 347 USD per night.
Receipt threshold: above 66 USD a receipt must be kept (this is the per-diem row's own receipt threshold field, for grade G4 / band B4 / stay S4).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body (lodging 347 USD/night, receipt threshold 66 USD)

4. **Notes**:
The expense table listed two other per-diem documents (`hard-perdiem-v2` and `hard-perdiem-legend-revision`) with dates overlapping "overseas per-diem" — easy to grab the wrong version. `sec-hard-perdiem` is explicitly flagged as the table in force from 2026-01-01, and today is 2026-09-20, so that's the correct one; the v2 table (2024-07-01 to 2025-12-31) and the older `overseas-rates` are both superseded and I didn't open them.

The bigger trap was the receipt threshold. There's a completely separate, general "qualifying evidence" table (`/v1/nodes/qualified-list/body`) that gives a receipt/evidence cutoff of 30,000 KRW for domestic-style spend evidence — a different currency and a different concept (what document type is required) from the per-diem row's own "Receipt threshold: 66 USD" field (which sits alongside the lodging/meal/incidentals caps for this specific grade/band/stay combination). Since the question was specifically about the Dhaka trip's hotel per-diem, I used the 66 USD figure from the matching per-diem row rather than the unrelated KRW evidence-type table. Worth flagging because the two thresholds could easily be conflated by a naive reading — same word "receipt threshold"/"receipt" appears in both, but they answer different questions.
