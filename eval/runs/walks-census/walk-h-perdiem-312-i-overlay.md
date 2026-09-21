1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "MD, Singapore, 8 nights: hotel per-night cap and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade, band, stay length - likely has hotel component" --member /v1/nodes/evidence "receipt/evidence threshold for expense claims"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_fd2327 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body
```

2. **Answer**
Lodging cap: 311 USD per night. Receipt threshold: above 45 USD you must keep the receipt (this is the row's own threshold, not the general KRW evidence rule).

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body (lodging 311 USD/night, receipt threshold 45 USD)

4. **Notes**
The legends had to be resolved in sequence (grade, band, stay) before the actual row address could be constructed from the printed pattern — the overlay's initial member list only pointed at the section, not the specific row, since the row depends on three separate lookups. I nearly conflated the per-diem row's own "Receipt threshold: 45 USD" with the general evidence table's KRW-denominated rule (/v1/nodes/qualified-list, "Up to 30,000 KRW a simple receipt is fine"). Checked that table to be sure, and it's clearly a separate, domestic/general-expense evidence rule in a different currency — the per-diem row is self-contained and gives its own threshold for this specific claim, so I used that rather than the general table. Confirmed the row is the current one (in force from 2026-01-01, today is 2026-09-21) rather than one of the two superseded per-diem versions flagged in the expense area's overview.
