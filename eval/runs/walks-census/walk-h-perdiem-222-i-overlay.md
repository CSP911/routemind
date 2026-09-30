1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Jakarta, 8 nights - hotel per-night cap and receipt threshold" --member /v1/regions/expense "trip/hotel allowances and receipt rules live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_986a12 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 263 USD per night. Receipt required for any spend above 50 USD (the receipt threshold).
(For context, also on this row: meals 94 USD/day, incidentals 19 USD/day — not asked for but on the same row.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body — "department head" → grade G3
- /v1/nodes/hard-perdiem-legend-band/body — "Jakarta" → band B3
- /v1/nodes/hard-perdiem-legend-stay/body — "eight nights" → stay S3
- /v1/nodes/hard-perdiem-legend-revision/body — confirms today's date (2026-09-21) falls under the current table
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body — the figures: lodging 263 USD/night, receipt threshold 50 USD

4. **Notes**:
The overseas per-diem subject has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision doc is explicit that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-21) is safely inside the current table's window (2026-01-01 onward, no end date given), so `sec-hard-perdiem` was correct here — but this is clearly a trap for questions dated in 2025, where the current table would give the wrong figures. Worth double-checking the date on every per-diem question rather than assuming "current" is always right.

The three legend tables (grade/band/stay) had to be resolved separately before the row address could even be built (grade G3 + band B3 + stay S3) — "eight nights" mapped exactly onto "stay S3" with no rounding needed, which was a relief since the legend note about taking "the nearest entry above" for unlisted values suggested I might have had to make a judgment call.

The overlay close reported all five used addresses as "reached" rather than matching named members, because I only added the parent `/v1/regions/expense` and then drilled into `sec-hard-perdiem` and its child rows/legends without re-adding each leaf as an overlay member. Not an error, just a quirk of how the overlay tracks narrowing.
