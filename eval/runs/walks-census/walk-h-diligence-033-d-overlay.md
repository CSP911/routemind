1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O1, value W4, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "origin/value/goods classification and site visit + review frequency for vendor diligence sounds like procurement due diligence rules"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_062572 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three due-diligence versions applies to today's date)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body (the row with the answer: Site visit = yes, Re-review interval = every 6 months)

4. **Notes**
There are three versions of the supplier due diligence table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was the correct table — but this is exactly the kind of question where grabbing the first "supplier due diligence" hit without checking the date would silently give a stale answer (the 2024-07-01–2025-12-31 version is indexed by only two qualifiers, not three, so it wouldn't even have had a matching O1/W4/K4 row directly). The overlay's close command flagged both sources as "reached" rather than pre-declared members, since only the top-level procurement region was added as a member and the specific row/legend addresses were found by drilling into that region's table rather than added via `overlay add` — functionally fine, just worth noting the mechanic.
