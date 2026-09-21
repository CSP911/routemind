1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G2, band B2, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel cap" --member /v1/nodes/evidence "evidence table likely defines receipt threshold" --member /v1/nodes/hard-perdiem-legend-revision/body "warns about three per-diem versions, need to confirm which is current"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6fe68b --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 183 USD per night. A receipt must be kept for any spend above 37 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body
/v1/nodes/hard-perdiem-legend-revision/body

4. **Notes**: The overlay member I picked as "/v1/nodes/evidence" doesn't actually exist as an address — the expense area table lists it as two separate tables (`qualified-evidence` and `sec-evidence-in-awkward-cases`), not a single `/v1/nodes/evidence`. It didn't matter here because the per-diem row itself already carries a "Receipt threshold" figure (37 USD), so I never needed the general evidence tables. The real risk was the per-diem version trap: the expense table's row explicitly warns there are THREE versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and picking the wrong one for the question's implied date would silently give a superseded figure. Today's date (2026-09-21) falls in the current window, so `sec-hard-perdiem` was right, but this is exactly the kind of question where grabbing the first "per-diem" table found without checking the revision legend would have been wrong for a 2025-dated question. Also note the overlay close reported the row address as "reached" rather than a named member — I read it directly from the table listing under `sec-hard-perdiem` rather than adding it individually to the overlay first, which is harmless but worth flagging as a minor procedural deviation.
