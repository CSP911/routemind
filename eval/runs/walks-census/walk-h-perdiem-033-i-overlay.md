1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Dhaka, 3 weeks - hotel per night cap and receipt threshold" --member /v1/regions/expense "hotel per diem and receipt rules for business trips"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f03ad8 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

2. **Answer**: Lodging cap is 155 USD per night. A receipt must be kept for any spend above 54 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

4. **Notes**: This region has three overlapping versions of the overseas per-diem rules with no withdrawal notice on the old ones — the legend-revision doc warns explicitly that reaching for the newest table is wrong for anything before 2026-01-01, and that the oldest version doesn't even say it's been superseded. Today's date (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-perdiem`) was correct here, but this is clearly the trap: a question dated in mid-2025 would need `hard-perdiem-v2` instead, and it would be easy to grab the current table by habit without checking. The row itself is indexed by three separate codes (grade, band, stay) that only exist via three separate legend lookups — junior analyst → G1, Dhaka → B4, three weeks → S4 — none of which are guessable from the question's plain wording, so skipping any one legend would have produced a wrong address. No ambiguity in the final row: it gave both the nightly lodging cap and the receipt threshold together, so no second table (e.g. corp-card or evidence) was needed.
