1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T2, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry-over cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_6f5ac5 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body

2. **Answer**: For type E1, tenure T2, site L4 (current table, in force from 2026-01-01): accrues 0.54 days per month; carry-over limit is 10 days (this is the cap on how much you can still be holding into January).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body

4. **Notes**: The leave accrual subject has three versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) that only differ by the date in question, not by type/tenure/site — I checked the legend-revision page first to confirm today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01) rather than the superseded `hard-accrual-v2`. That was the one place this walk could have silently gone wrong: grabbing the newest-looking table without checking it actually covers the date in play. Once on the current table, the E1/T2/L4 row was a direct, unambiguous lookup — no legend lookups needed since the question already gave codes rather than descriptions. The row itself answers both halves of the question directly: "Accrues per month" for the monthly build-up, and "Carry-over limit" for what can still be held into January.
