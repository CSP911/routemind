1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Singapore, four nights: hotel amount per night and receipt threshold?" --member /v1/regions/expense "trip expense rules, hotel per-night caps, receipt requirement thresholds likely here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_dc0448 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body

2. **Answer**: Lodging cap: 179 USD per night. Receipt required for any single spend above 34 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body

4. **Notes**: The overseas per-diem subject has three superseded/current versions gated by date (`overseas-rates` until 2024-07-01, `hard-perdiem-v2` 2024-07-01–2025-12-31, `sec-hard-perdiem` from 2026-01-01), and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-21) falls in the current-table window, so `sec-hard-perdiem` was correct, but this is exactly the kind of question where grabbing the first per-diem hit without checking the revision legend would have silently given the wrong figures for an older-dated trip. The row itself is indexed by three separate qualifiers (grade, band, stay) each requiring its own legend lookup — "team manager" → grade G2, "Singapore" → band B2, "four nights" → stay S2 — none of which is guessable without the legend tables; getting any one wrong (e.g. treating "four nights" as S1/S3 by miscounting) would point at a different row with different numbers. The overlay close command reported these addresses as "reached" rather than pre-listed members, since only the table-level row for hard-perdiem-legend-revision was a named member — the legend/row files themselves were drilled into afterward, which the tool still accepted and recorded correctly.
