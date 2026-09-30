1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "MD, Tokyo, 8 nights: hotel nightly cap and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel caps" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted - likely the receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_008aeb --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body

2. **Answer**: A managing director on an 8-night Tokyo trip is grade G4, band B1, stay S3. The lodging cap is 295 USD per night. The receipt threshold for this row is 36 USD — above that amount a receipt must be kept.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body (lodging 295 USD/night, receipt threshold 36 USD)

4. **Notes**: The expense area table flagged that overseas per-diem has three superseded versions (hard-perdiem-legend-revision, hard-perdiem-v2, plus an older one) — I made sure to pick /v1/nodes/sec-hard-perdiem, explicitly labeled the current table in force from 2026-01-01, and not one of the older ones. I also opened /v1/nodes/qualified-evidence and read its /v1/nodes/qualified-list/body expecting it might hold "the" receipt threshold, since the question phrasing ("above what amount do I have to keep the receipt") echoes that table's own description ("the ceiling on a simple receipt"). That table turned out to be a general domestic evidence-type rule denominated in KRW (30,000 KRW ceiling for a simple receipt vs. qualifying evidence), unrelated to the overseas per-diem row, which carries its own USD-denominated "Receipt threshold" field. Easy to conflate the two since both are called "receipt threshold[s]" in plain language — the per-diem row's own field is the one that actually answers this question, not the general evidence table.
