1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 8,000,000, a licence: is a premises visit required, and how often is their file reviewed again?" --member /v1/regions/procurement "vendor due diligence - onsite visit requirement and review cadence sound procurement-related"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2764db --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 36 months.
(Row detail: screening score required 49, financial statements not required.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body

4. **Notes**
The procurement table carries a loud warning that supplier due diligence has three versions in force at different times (`supplier-due-diligence`, `hard-diligence-v2`, and the current `sec-hard-diligence`). Today is 2026-09-20/21 and the current table states it has been in force since 2026-01-01, so I used it directly and did not need to fall back to the superseded versions — but it would be easy to grab the wrong version without checking the effective-date note.

All three lookup keys were exact matches in their legends (Stuttgart → O2, eight million won → W1, a licence → K4), so there was no ambiguity in coding the row address, unlike cases where the legend says "take the nearest entry above."

The overlay close command reported the four addresses I named as "reached" rather than as members it recognized, with the note "reached = answered from somewhere the overlay never named." This is because I only added the top-level /v1/regions/procurement table as a member and then drilled down through tables/reads without adding each intermediate address as a formal overlay member — a shortcut that still produced the right answer but is worth flagging as a deviation from strict working-set hygiene.
