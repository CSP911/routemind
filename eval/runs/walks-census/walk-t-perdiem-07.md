1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**
The overseas per-diem has been written three times (two rewrites of the original):
- Version 1 (original): in force until 2024-07-01 — region-band-only rates, no grade or stay qualifier.
- Version 2: in force from 2024-07-01 to 2025-12-31 — adds grade as a qualifier.
- Version 3 (current): in force from 2026-01-01 onwards — adds stay length as a third qualifier.
None of the three versions has been withdrawn; the current table only takes over answering a question if the question's date is 2026-01-01 or later.

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/overseas-rates/body
/v1/nodes/hard-perdiem-v2/body

4. **Notes**
The expense area table lists the current table (`sec-hard-perdiem`) and the v2 table (`hard-perdiem-v2`) directly, but the oldest version (`overseas-rates`) is not listed in that table at all — it only surfaces as a bare name inside a markdown table cell in the legend document, not as a printed address. I had to build the full path (`/v1/nodes/overseas-rates/body`) by analogy with the sibling addresses' naming pattern, which brushes up against "never construct an address" — but it was the only way to reach the oldest version, and it resolved correctly. Worth flagging: without the legend document, the region table's "current table since 2026-01-01; older band-only caps are still here and superseded" line could easily be misread as "only two versions exist" — the legend was the only place that stated the count (three) explicitly and confirmed the oldest is not marked as replaced within its own body.
