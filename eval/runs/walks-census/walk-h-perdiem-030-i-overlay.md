1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Dhaka, one night: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "business trip pay/hotel caps and receipt rules likely here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6cda35 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body

2. **Answer**: Lodging cap is 143 USD per night. A receipt must be kept for any spend above 45 USD. (For reference, meals are capped at 80 USD/day and incidentals at 16 USD/day, but these weren't asked about.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established today's date, 2026-09-21, falls under the current per-diem version, not the two superseded ones)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body (the figures: 143 USD lodging/night, 45 USD receipt threshold)

4. **Notes**: This table (`sec-hard-perdiem`) is versioned three ways for the same subject, and the oldest version says nothing about being superseded — so checking `hard-perdiem-legend-revision` first, before trusting the newest-looking table, was the deciding step. Today's date (2026-09-21) falls after 2026-01-01, so the current table applies, but if this had been asked with a 2025 date the answer would have had to come from `hard-perdiem-v2` instead, which would have been an easy wrong turn if I'd just grabbed the top-listed table. The three legends (grade/band/stay) are separate documents and none of the per-diem rows repeat the human-readable inputs, so all three had to be resolved before the single matching row (grade-g1-band-b4-stay-s1) could be addressed — guessing the row address from the question's words directly would not have worked.
