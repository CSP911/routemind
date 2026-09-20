1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body

2. **Answer**
Hotel (lodging) cap: 255 USD per night.
Receipt required above: 44 USD (the receipt threshold).
(For context, same row also gives meals 84 USD/day and incidentals 17 USD/day, but those weren't asked for.)

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which per-diem version is current for today's date, 2026-09-20)
/v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
/v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
/v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body (the figures)

4. **Notes**
The overseas per-diem topic has three superseded/current versions living side by side under
/v1/regions/expense (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the oldest one
never says it was replaced — the legend-revision page exists specifically to stop you from grabbing
the wrong one. It was easy to almost skip that check since `sec-hard-perdiem` is billed as "THE
CURRENT TABLE" right in the table listing, which tempted me to go straight there. But the revision
page was worth reading anyway to confirm 2026-09-20 genuinely falls in the "2026-01-01 onwards"
band rather than assuming it from the label. No ambiguity in mapping "department head" → G3,
"Jakarta" → B3, or "one night" → S1 — all three appeared verbatim in their legends, no nearest-match
judgment calls needed.
