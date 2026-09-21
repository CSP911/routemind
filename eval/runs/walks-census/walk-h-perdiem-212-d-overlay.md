1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B2, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are business trip expense rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d0a584 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

2. **Answer**: Lodging cap is 247 USD per night. A receipt is required for any spend above 41 USD (the receipt threshold).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established that today's date, 2026-09-20/21, falls under the current per-diem version, not the superseded ones)
- /v1/nodes/sec-hard-perdiem (table index, used to locate the G3/B2/S3 row address)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body (the actual figures)

4. **Notes**: The expense area has three separate versions of the overseas per-diem document (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page warns explicitly that reaching for the newest one is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about being superseded — so grabbing the first per-diem-looking row without checking the date would have been an easy mistake. Today's date (2026-09-20/21) falls cleanly in the current table's range, so no ambiguity here, but the check was necessary. The overlay tool flagged the addresses I used as "reached ... from somewhere the overlay never named" since I never formally added them as overlay members (only the top-level /v1/regions/expense) — I browsed to them via table/read directly rather than growing the member list, which didn't affect the answer but is worth noting for overlay hygiene.
