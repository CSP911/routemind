1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W4, goods K1: site visit required? review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table - need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_08a874 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 6 months. (Also on this row, for context: screening score required is 58, and financial statements must be the last three years, audited.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current for today's date, 2026-09-20/21)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k1/body (the row with the answer)

4. **Notes**:
The procurement region table pointed straight at `/v1/nodes/sec-hard-diligence` as "THE CURRENT SUPPLIER DUE DILIGENCE TABLE," but there's also a legend-revision page warning that this subject has been written three times, with the current version only in force from 2026-01-01. It would have been easy to skip that check since the table description already said "current," but the revision page explicitly calls out that a 2025-dated question needs the middle version instead — so I read it anyway to be sure today's date (2026-09-20/21) really does fall under the current-table window rather than assume it. It does.

The overlay's `close` command flagged the row address as "reached = answered from somewhere the overlay never named," because I only added the parent table (`sec-hard-diligence`) and the legend page as members, not the specific origin/value/goods row itself — I went straight from the table listing to reading the row without formally adding it to the working set first. Not an error, just a mechanical note on how the tool books credit.
