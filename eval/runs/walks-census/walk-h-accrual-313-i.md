1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

2. **Answer**
You accrue 1.50 days of leave per month. The carry-over limit is 10 days — that is the most you can still be holding into January.
(Basis: type E4 "here from our partner firm", tenure T2 "been here two years", site L4 "fully from home", under the accrual table in force since 2026-01-01, which applies to today's date of 2026-09-20.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

4. **Notes**
The accrual subject has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version never says it was replaced — easy to grab the wrong one by just taking the first hit. Today's date (2026-09-20) falls squarely in the current table's range (2026-01-01 onward), so this wasn't a borderline case, but it would have been easy to skip the version check entirely and not notice the trap.
The three qualifiers (type/tenure/site) are each phrased in the question in casual language ("from our partner firm", "two years", "fully from home") and only resolve to row codes (E4, T2, L4) via three separate legend files — none of the codes are guessable from the table listing alone, and guessing wrong on any one of the three would have pulled a completely different row (64 rows total, one for each type×tenure×site combination).
"How much can I still be holding in January" maps to the row's "Carry-over limit" field rather than anything about a specific January date or a separate carryover policy page — there was no January-specific rule to find, so the natural reading of the question (checking for a special new-year policy) turned out to be a dead end; the carry-over limit field already answers it.
