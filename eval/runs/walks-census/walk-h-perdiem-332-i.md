1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body

2. **Answer**: A managing director on an 8-night trip to Dhaka can put up to **343 USD per night** on a hotel. A receipt has to be kept for any spend **above 63 USD**.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies to today's date, 2026-09-20)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body (the figures: lodging 343 USD/night, receipt threshold 63 USD)

4. **Notes**: The expense area explicitly warns that overseas per-diem has three superseded/current versions indexed by different qualifier counts (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and that reaching for the newest is wrong for dates before 2026-01-01 — a real trap if the walk skipped the revision-legend file. Today's date (2026-09-20) clearly falls after 2026-01-01, so `sec-hard-perdiem` is correct, but I deliberately read the revision file to confirm rather than assume. The three legend files (grade/band/stay) are the only place the plain-language → code mapping exists, and the row address has to be hand-built from all three codes (grade-g4-band-b4-stay-s3) — nothing prints that exact address directly, so care was needed to get the ordering and codes right. No ambiguity in the mapping itself: "managing director," "Dhaka," and "eight nights" each hit an exact row in their respective legends, not a nearest-match fallback.
