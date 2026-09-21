1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Jakarta, 4 nights - hotel nightly cap and receipt threshold?" --member /v1/regions/expense "expense region covers business trip amounts, hotel/corporate card use, and receipt requirements"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3fe4f9 --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

2. **Answer**:
Lodging cap: 131 USD per night. Receipt threshold: above 39 USD a receipt must be kept. (For reference, the same row also gives meals at 71 USD/day and incidentals at 14 USD/day, but only the hotel and receipt figures were asked for.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms today, 2026-09-21, falls under the current table)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body (the figures)

4. **Notes**:
The overseas per-diem subject has three superseding versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision page is explicit that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version never says it was replaced. It would have been easy to just grab `sec-hard-perdiem` on the assumption that current = correct without checking the date, which happens to be right here (today is 2026-09-21, well after the 2026-01-01 cutover) but only by chance of when the question was asked — for a question dated in 2025 it would have been the wrong table entirely. Also worth flagging: the three legend tables (grade/band/stay) all say "if not listed, take the nearest entry" — none of my three lookups (junior analyst, Jakarta, four nights) needed that fallback, they were exact matches, but it's a place a walk could silently go wrong if a title or city were slightly different from the legend's wording.
