1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Jakarta, three-week trip: nightly hotel cap and receipt threshold?" --member /v1/regions/expense "business trip lodging allowance and receipt rules live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_98026b --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body

2. **Answer**: Nightly hotel (lodging) cap is 267 USD. The receipt threshold is 53 USD — any spend above that amount needs a receipt kept as evidence. (For reference, the same row also gives meals at 99 USD/day and incidentals at 20 USD/day, but those weren't asked for.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions is in force for a 2026 date)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body (the figures themselves — this is the answer's actual source)

4. **Notes**: The overseas per-diem area has three overlapping versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and none of them say they've been superseded — reading the legend-revision page first was necessary to avoid grabbing the wrong one. With today's date in 2026, the current table (`sec-hard-perdiem`, in force from 2026-01-01) is correct, but this would have been an easy place to silently answer from a stale version if I'd jumped straight to the row.

Also, the three legend pages (grade/band/stay) and the final row page were read directly rather than added to the overlay with `overlay add` first — the close command still accepted them but flagged them as "reached = answered from somewhere the overlay never named." The lookup worked, but the working set I built didn't actually track the path I took to the answer; if this scores dropped classification correctness, that's likely why. Next time I'd `overlay add` each legend/row address as I opened it, not just cite it at close time.
