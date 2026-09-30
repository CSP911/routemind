1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Jakarta, eight nights — hotel nightly cap and receipt threshold" --member /v1/regions/expense "business trip / hotel spend and receipt rules likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7e265b --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body

2. **Answer**:
Lodging (hotel) cap: 199 USD per night.
Receipt threshold: above 46 USD you must keep the receipt.
(For context, same row also gives meals 85 USD/day and incidentals 17 USD/day, but these were not asked for.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body — maps "team manager" → grade G2
- /v1/nodes/hard-perdiem-legend-band/body — maps "Jakarta" → band B3
- /v1/nodes/hard-perdiem-legend-stay/body — maps "eight nights" → stay S3 (exact match, no rounding needed)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body — the rates row itself, in force from 2026-01-01, current as of today (2026-09-21)

4. **Notes**:
- The expense table lists an explicit trap: `/v1/nodes/hard-perdiem-legend-revision/body` warns overseas per-diem has THREE versions (`overseas-rates`, `hard-perdiem-v2` superseded 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` in force from 2026-01-01). It would be easy to grab a stale rate from one of the older nodes since they're indexed right alongside the current one under /v1/regions/expense. I stuck with `sec-hard-perdiem` because its own table description says "THE CURRENT ... TABLE, in force from 2026-01-01," and today's date (2026-09-21) falls inside that window — didn't need to open the legend-revision doc itself since the row body restated the same in-force date and confirmed the supersession chain.
- All three lookup keys (grade, band, stay) required going through separate legend files rather than the row table itself — the row addresses are pre-coded (g2/b3/s3) and give no hint which words map to which code without the legends. Eight nights mapped exactly to "S3" in the stay legend, so no nearest-value judgment call was needed there.
- The overlay close command reported all four addresses I used as "reached" rather than as named overlay members — I navigated to them via `table`/`read` after the initial overlay create instead of issuing explicit `overlay add` calls for each. Outcome was still recorded correctly as answered, but worth flagging in case a stricter walk expects every address to be added to the overlay before being used.
