1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W2, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely holds site-visit and review-frequency by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns diligence table has three versions with different date ranges - need to confirm which version applies today (2026-09-21)"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9a4485 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months. (This row also requires a screening score of 69 and last year's financial statements, in case that's useful context, but the question only asked about the site visit and re-review interval.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three diligence table versions applies to today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body (the actual figures: site visit no, re-review every 24 months)

4. **Notes**
- The procurement region table listed a superseded version (`hard-diligence-v2`, in force 2024-07-01 to 2025-12-31) right alongside the current one (`sec-hard-diligence`), with only short labels distinguishing them. It would be easy to grab the wrong one without checking the legend-revision page first — the warning on that page is explicit that reaching for the newest is wrong for older question dates, and reaching for an old one is wrong now. Today's date (2026-09-21) falls under the current table (2026-01-01 onwards), so `sec-hard-diligence` was correct.
- Opening `sec-hard-diligence` as an overlay member did not just add one row — it expanded into all 64 individual origin/value/goods row files (O1–O4 × W1–W4 × K1–K4), each with its own address. This is because the current table is "indexed by three qualifiers," per the legend page — the table is really 64 rows, not one. It was easy to spot the right one visually (`hard-diligence-row-origin-o3-value-w2-goods-k4`) since addresses spell out the three qualifiers directly, but on a table with less legible addresses this could have required checking the legend-goods/legend-origin/legend-value pages to map O3/W2/K4 to the right row rather than pattern-matching the address.
- The overlay's close output flagged the row address as "reached" rather than a named member, since I read it directly by its printed address rather than issuing a separate `overlay add`. Worth noting the tool distinguishes between addresses formally added to the working set versus ones just read and cited at close — no functional problem here, just a bookkeeping nuance.
