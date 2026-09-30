1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll employee, 2 years tenure, Seoul office: monthly leave accrual rate, and how much can be held/carried over into January?" --member /v1/nodes/sec-hard-accrual "current accrual table since 2026-01-01, need rate by type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_91fd8a --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

2. **Answer**
On the regular payroll (type E1), with two years of service (tenure T2), at the Seoul office (site L1): leave accrues at 0.48 days per month, and the carry-over limit is 7 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

4. **Notes**
The three qualifiers in the question ("regular payroll", "two years", "Seoul office") aren't self-explanatory codes — they only resolve to E1/T2/L1 via three separate legend files, each of which insists it's "the only place the mapping is written down." Skipping straight to guessing the row address (e.g. assuming "regular" = the lowest-numbered type) would have been easy and wrong-feeling-right; the legends were necessary, not just a formality. The phrase "how much can I still be holding in January" doesn't literally say "carry-over," so it's worth flagging that I mapped it to the "Carry-over limit, days" field rather than to accrued year-to-date balance — the question is about the cap on what survives into the new year, not a running total, and the current table (in force since 2026-01-01, matching today's date 2026-09-20) is the right version to use since there are two superseded versions (hard-accrual-v2, and an older leave-accrual) that could have been picked by mistake if the revision-legend warning had been ignored. Also note the overlay close reported all four addresses as "reached" rather than as named members — the overlay was created with only the parent table as a member, and I added the leaf files by reading them directly rather than via `overlay add`; the tool still accepted them as valid `--used` addresses.
