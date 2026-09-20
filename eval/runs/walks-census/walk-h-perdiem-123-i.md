1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body

2. **Answer**
Lodging cap: 203 USD per night. Receipt is required above 49 USD (the receipt threshold). (For reference, the same row also sets meals at 90 USD/day and incidentals at 18 USD/day.)
This is for grade G2 (team manager), band B3 (Jakarta), stay S4 (three weeks), under the per-diem table in force since 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body

4. **Notes**
The expense region table flagged upfront that overseas per-diem has three versions in force at different times (a legend-revision doc, a superseded v2, and the current sec-hard-perdiem table). It would have been easy to grab the wrong version or blend the older band-only caps with the current grade/band/stay table — the region table explicitly warns the older caps are "still here and are superseded." I went straight for `sec-hard-perdiem`, the one marked current as of 2026-01-01, which covers today's date (2026-09-20), and didn't need to open the superseded versions.
The three legends (grade, band, stay) are each a separate lookup and none of them repeat in the row table — you have to resolve "team manager," "Jakarta," and "three weeks" into codes G2/B3/S4 before the 64-row index means anything. "Three weeks" isn't an exact match in the stay legend (rows are one/four/eight nights, then three weeks) but it maps cleanly to S4 as the top band, so no ambiguity there.
