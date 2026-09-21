1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Team manager, Tokyo, four nights: hotel per-diem cap and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel cap for Tokyo by grade" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three per-diem versions by date, need to confirm which applies now" --member /v1/nodes/evidence "receipt threshold - above what amount a receipt must be kept"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py overlay remove --id ov_2026-09-21_3884bf --address /v1/nodes/qualified-evidence --why "general evidence-qualification table; the per-diem row already gives its own receipt threshold specific to this claim"
./bench/rmcli.py overlay close --id ov_2026-09-21_3884bf --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**
Lodging cap: 163 USD per night. Receipt required above 25 USD (the receipt threshold on this same row). This is grade G2 (team manager), band B1 (Tokyo), stay S2 (four nights), current table in force since 2026-01-01 — today's date (2026-09-21) falls in this version's window.

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body
/v1/nodes/hard-perdiem-legend-revision/body

4. **Notes**
The three per-diem qualifiers (grade, country band, stay length) are each resolved by a separate legend document rather than being obvious from the question — "team manager" isn't self-evidently G2, and "four nights" isn't self-evidently S2 (it's the boundary value for S2, not S1 or S3, and it would be easy to misjudge without checking the legend table, which bands stays as one/four/eight nights/three weeks). Getting any one of the three qualifiers wrong silently returns a different, equally plausible-looking row, so all three had to be checked explicitly rather than inferred.

The revision-warning document was the most important thing not to skip: overseas per-diem has three superseded-but-still-present versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the warning explicitly says the oldest version never states it was replaced — reaching for whichever table shows up first would be wrong. Today's date (2026-09-21) confirmed the current table (`sec-hard-perdiem`, in force from 2026-01-01) was the right one to use, but this needed an explicit date check, not an assumption.

The "receipt threshold" answer came from a field embedded inside the per-diem row itself (25 USD), not from the general evidence-qualification table (`/v1/nodes/qualified-evidence`) I'd initially pulled into the working set. That general table looked like a plausible source given the question's wording ("above what amount do I have to keep the receipt"), but it covers what counts as qualifying evidence in general, not the per-diem-specific threshold — using it would have risked citing the wrong number if the two ever diverge. Worth flagging: I did not open its body to confirm the two thresholds don't conflict; I trusted the per-diem row's own field as authoritative for this specific claim.
