1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

2. **Answer**: For type E1, tenure T3, site L2 (current table, in force from 2026-01-01): you accrue 0.58 days per month, and the carry-over limit is 11 days — that is the most you can still be holding into January.

3. **Source**: /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

4. **Notes**: The question gave the type/tenure/site codes directly (E1, T3, L2), so there was no need to open the legend files (`hard-accrual-legend-type`, `hard-accrual-legend-tenure`, `hard-accrual-legend-site`) to translate plain-language qualifiers into codes — going there would have been a wasted step. The only real fork was the version warning: `sec-hard-accrual`'s listing flags that leave accrual has three versions (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual` table effective 2026-01-01). Since today is 2026-09-20, the current table is the right one and the row itself confirms it's "in force from 2026-01-01," so no need to chase the superseded versions or the legend-revision doc. The phrase "how much can I still be holding in January" maps to the row's "Carry-over limit" field — it isn't a separate January-specific figure, it's the same year-round carry-over cap, which is what limits the balance you're allowed to be sitting on going into the new year.
