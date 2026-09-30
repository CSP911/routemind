1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T3, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry-over/cap questions live here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9e1208 --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

2. **Answer**: For type E1, tenure T3, site L4 (current table, in force from 2026-01-01): accrues 0.62 days per month; the carry-over limit is 13 days — that is the most that can still be held into January.

3. **Source**:
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

4. **Notes**: The E1/T3/L4 combination in the question maps directly to a single row name in the table (hard-accrual-row-type-e1-tenure-t3-site-l4), so no legend lookup was needed to translate a person's words into codes — the codes were already given. The only thing worth flagging: the table has three historical versions (hard-accrual-legend-revision warns of this), but today's date (2026-09-20/21) falls within the current version's effective range (from 2026-01-01), so no version confusion arose here. The overlay close reported the two addresses as "reached" rather than "used" because I never added them as explicit overlay members before closing — I drilled into the table without adding rows as members first. Didn't change the answer, but worth noting for next time: add the specific row as a member before closing, not just the region.
