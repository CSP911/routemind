1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Tokyo, 8 nights, team manager: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "expense table covers business trip pay and receipt rules"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_164374 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body

2. **Answer**:
Hotel (lodging) cap: 167 USD per night. Receipt required above 28 USD.
(For context, the same row also gives meals at 57 USD/day and incidentals at 11 USD/day, but the question only asked about the hotel and the receipt threshold.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is in force for today's date, 2026-09-21)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body (the row with the figures)

4. **Notes**:
The overseas per-diem subject has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01 — the oldest version doesn't even say it was replaced. Today's date (2026-09-21) falls cleanly in the current table's range, so this wasn't actually a close call, but it would have been easy to skip that check and just grab `sec-hard-perdiem` on the name alone. Worth checking that page every time regardless of how obvious the date seems.

The other trap was "eight nights" — the stay-band legend has bands for 1/4/8/21 nights, and 8 lands exactly on a band boundary (S3) rather than needing rounding, so no ambiguity there, but it's the kind of value where sloppy reading could round to the wrong neighboring band (S2 or S4) if not read carefully.

The overlay close command reported the used addresses as "reached" rather than "used" — they were fetched via the table walk (table → legends → row) rather than added as explicit overlay members, so the overlay mechanism logs them differently. Doesn't change the answer, just a quirk of how this walk was conducted.
