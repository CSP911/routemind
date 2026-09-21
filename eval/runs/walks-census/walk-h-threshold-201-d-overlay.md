1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V1, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is the procurement table"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cdb5f7 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body

2. **Answer**
For category C3, amount V1, term M2 (delegation limit 1,033 thousand KRW): the team lead signs it off, and no competing quotes are required. Expect 3 working days.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established which of the three approval-threshold versions is in force for a question dated 2026-09-21)
- /v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, indexed by category/amount/term)
- /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body (the exact row, source of the answer)

4. **Notes**
The approval threshold subject has three superseded/current versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) covering different date ranges, and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest version gives no hint it was ever replaced. Today's date (2026-09-21) falls under the current table, `sec-hard-threshold`, so that's the one used — but it would have been easy to grab `hard-threshold-v2` by mistake since it sat right next to the current one in the overlay's row list with a very similarly named address. The category/amount/term row address for C3/V1/M2 existed verbatim in the current table's listing, so no legend lookups for what "C3", "V1", or "M2" mean were needed — the question already gave the codes in the table's own vocabulary.
