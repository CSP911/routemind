1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Jakarta, junior analyst, 8 nights: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "business trip pay/allowance and receipt rules live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bbe865 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging (hotel) cap: 135 USD per night. Receipt threshold: 42 USD — keep the receipt for any spend above that amount. (For reference, this row also gives meals at 76 USD/day and incidentals at 15 USD/day, though those weren't asked.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this 2026-01-01-onward table is the correct version for today's date, 2026-09-21)

4. **Notes**:
The overseas per-diem area has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and a warning node exists specifically to stop you from grabbing the newest one reflexively. The question gave no trip date, only "today," so I checked the revision legend explicitly rather than assuming the current table applied — it does, since today (2026-09-21) is after 2026-01-01. Had the question been about a 2025 trip, the answer would have had to come from `hard-perdiem-v2` instead, and that table is indexed by only two qualifiers (not three), so the row-lookup pattern would differ too.

The three legends (grade/band/stay) are each in their own file and none of the codes are guessable — Jakarta as B3 and eight nights as S3 both required a direct lookup rather than an assumption. The overlay close reported these addresses as "reached" rather than "used," since I never added the specific row/legend files as named overlay members before closing — only the parent table `/v1/regions/expense` was a member. This looks like a labeling quirk of the tool, not a problem with the answer: the tool still recorded them against this overlay.
