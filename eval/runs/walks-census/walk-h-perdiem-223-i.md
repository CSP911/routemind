1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body

2. **Answer**:
Lodging cap: 267 USD per night. Receipt threshold: 53 USD — above that amount a receipt must be kept (this is the current, 2026-01-01-onwards table, so it applies to a trip taken today, 2026-09-20).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem versions is in force for today's date)
- /v1/nodes/sec-hard-perdiem (index table, to find the grade/band/stay legends and row address)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body (the figures: 267 USD lodging, 53 USD receipt threshold)

4. **Notes**:
The expense area table lists three per-diem documents (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, `sec-hard-perdiem`) with no indication from the region table alone which one is current for a given date — the legend-revision page had to be read first to confirm the 2026-01-01-onwards table applies to today's date (2026-09-20) rather than the superseded `hard-perdiem-v2`. It would have been easy to jump straight to `sec-hard-perdiem` since it's flagged "current," but the legend-revision page is the only place that states the older versions weren't withdrawn and aren't marked as replaced on their own pages — worth checking explicitly rather than trusting the "current" label at face value.

Also worth flagging: "three weeks" maps to stay S4 exactly by the legend's wording, but the legend's rows are examples ("one night," "four nights," "eight nights," "three weeks") rather than defined numeric ranges, so it's not visible whether S4 covers all stays beyond eight nights or has an upper bound of its own — the table gives no way to check that from here.
