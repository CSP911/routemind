1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W3, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force from 2026-01-01 - likely holds the O3/W3/K4 row for site visit and review frequency" --member /v1/nodes/hard-diligence-legend-revision/body "warns due diligence has three versions with different date ranges - need to confirm which version applies today (2026-09-21)"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ccfd62 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body

2. **Answer**
Site visit: yes, required. Re-review interval: every 12 months. (Also on file for this row: screening score required 73, financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body (the answer: site visit yes, re-review every 12 months)

4. **Notes**
The procurement table lists three separate due-diligence eras (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) living side by side under similarly named addresses (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend explicitly warns that the oldest version says nothing about being superseded — so grabbing the first "supplier due diligence" hit without checking the legend would have silently produced a stale answer. Today's date (2026-09-21) falls under the current table, so no correction was needed here, but the check was worth doing since the row layout (three qualifiers: origin/value/goods) is unique to the current version and wouldn't exist the same way in the older two. Also worth flagging: the overlay's close command reported the row address as "reached ... from somewhere the overlay never named," even though it was visible as a listed row under the `sec-hard-diligence` member from the start — it was never added as its own named member, only read directly, so the tool didn't count it as part of the declared working set. No actual ambiguity in the final answer itself.
