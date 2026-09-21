1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W2, goods K1: is a premises visit required, and how often is the file reviewed again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, should have the matrix by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of supplier due diligence, need to confirm which applies today"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_49e3e8 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 24 months. (This is for the current table, in force from 2026-01-01, which applies since today is 2026-09-20.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (established that the current, three-qualifier table applies for today's date)
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body (row with Site visit: no, Re-review interval: every 24 months)

4. **Notes**
Supplier due diligence has three versions covering different date ranges, and the legend-revision page explicitly warns that reaching for the newest is wrong for anything before 2026-01-01, and that the oldest version says nothing about being replaced (so it can look current when it isn't). Since today's date is 2026-09-20, the current table (`sec-hard-diligence`, indexed by three qualifiers: origin, value, goods) is the right one — no ambiguity here, but it would have been easy to skip checking the date and just grab the first "current" looking table. The row address for O1/W2/K1 existed exactly as expected once opening the overlay, so no guessing at addresses was needed.
