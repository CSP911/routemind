1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B3, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel night cap for G3/B3/S3" --member /v1/nodes/evidence "evidence table likely states receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_10a438 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body

2. **Answer**: Lodging cap is 263 USD per night. The receipt threshold is 50 USD — above that amount a receipt must be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body

4. **Notes**: The expense area table warned that overseas per-diem has three versions in force at different times (a legend-revision node, a superseded `hard-perdiem-v2`, and the current table). Today's date (2026-09-21) falls after the current table's effective date (2026-01-01), so I went straight to the current table (`sec-hard-perdiem`) rather than the superseded `hard-perdiem-v2` — worth double-checking on any question that doesn't clearly fall after 2026-01-01, since picking the wrong version would give a wrong lodging cap. The overlay's row listing under `sec-hard-perdiem` went straight to the exact grade/band/stay row (G3/B3/S3), so I never needed the separate `evidence`/`qualified-evidence` member — the per-diem row itself carries its own "Receipt threshold" figure. The overlay-close output flagged the used address as "reached … from somewhere the overlay never named," which just reflects that I added the parent `sec-hard-perdiem` as the member rather than the specific row address printed inside it — not an error, just a quirk of how the overlay records provenance one level down.
