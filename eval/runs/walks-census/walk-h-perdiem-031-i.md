1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body
./bench/rmcli.py table /v1/nodes/evidence

2. **Answer**
Lodging cap: 147 USD per night. Receipt threshold: 48 USD — above that amount a receipt must be kept.
(For context, this row also gives meals at 85 USD/day and incidentals at 17 USD/day, though not asked.)

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body — established that today's date (2026-09-20) falls under the current table, not the two superseded versions
/v1/nodes/hard-perdiem-legend-grade/body — junior analyst → grade G1
/v1/nodes/hard-perdiem-legend-band/body — Dhaka → band B4
/v1/nodes/hard-perdiem-legend-stay/body — four nights → stay S2
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body — the figures

4. **Notes**
- The expense region table flags up front that overseas per-diem has three separate versions in force over different date ranges, and warns that "the oldest says nothing at all about having been replaced" — so grabbing the first per-diem-looking node without checking dates would have silently produced numbers from the wrong era. Reading the legend-revision doc first to confirm 2026-09-20 falls in the "current" (2026-01-01 onward) band was the right call and avoided that trap.
- The per-diem table is indexed by three separate codes (grade/band/stay) each defined in its own legend file, not spelled out in the row list itself — the row addresses only show the codes (g1/b4/s2), not the underlying meaning, so all three legends had to be opened before the right row address could be identified. "Four nights" mapped exactly onto the S2 boundary ("four nights"), so no rounding judgment call was needed there, but the legends do warn to take the nearest lower entry if a value isn't listed outright — worth watching for in a walk where the inputs aren't as clean a match.
- The row itself already carries a field literally labeled "Receipt threshold," which directly answers the second half of the question — I did not need to descend into the general /v1/nodes/evidence tree (qualifying evidence, ceilings on simplified receipts, etc.) since that governs evidence rules generally rather than this specific per-diem figure. I opened the evidence table to check whether it would override or clarify this number, but nothing there redefined the per-diem-specific threshold, so the row's own figure stands as the answer.
