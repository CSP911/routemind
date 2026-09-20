1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body

2. **Answer**: Lodging (hotel), per night: 151 USD. Receipt threshold: 51 USD — a receipt must be kept for any spend above this amount. (For context, also on this row: meals 90 USD/day, incidentals 18 USD/day.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body (the answer)

4. **Notes**: The expense area's table listing flags upfront that overseas per-diem has three versions in force over different date ranges, and warns that reaching for the newest one is wrong for dates before 2026-01-01 — and that the oldest version says nothing about having been superseded, so nothing there would stop you from citing it in error. Today's date (2026-09-20) falls under the current table (`sec-hard-perdiem`, in force since 2026-01-01), so no correction was needed here, but skipping that check would have been the easy mistake — the three tables use the same grade/band/stay-shaped structure so a wrong-version row could look just as plausible as the right one. The current table happened to have an exact pre-computed row for G1/B4/S3, so no interpolation or legend lookup (grade/band/stay definitions) was needed.
