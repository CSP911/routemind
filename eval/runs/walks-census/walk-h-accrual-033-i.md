1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

2. **Answer**
Accrues 0.70 days per month. Carry-over limit (how much can still be held going into January) is 16 days.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (established the current table, in force since 2026-01-01, is the one that applies for a 2026-09-20 question)
- /v1/nodes/hard-accrual-legend-type/body (regular payroll → type E1)
- /v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (fully from home → site L4)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body (the row itself: 0.70 days/month accrual, 16-day carry-over limit)

4. **Notes**
- The attendance table flags that leave accrual has three superseded/current versions with different qualifier counts (one, two, three qualifiers respectively), and warns that "the oldest says nothing at all about having been replaced" — reaching for the wrong version by habit would be an easy, silent mistake. Since the question carries today's date (2026-09-20), the current three-qualifier table (`sec-hard-accrual`, in force from 2026-01-01) is the right one; a 2025-dated question would have needed the middle version (`hard-accrual-v2`) instead.
- All three legends (type, tenure, site) explicitly say each is "the only place the mapping is written down" and each row is indexed by exact codes, not by the plain-English descriptions in the question — so the mapping had to be done explicitly (regular payroll = E1, nine years = T4, fully from home = L4) rather than guessed from wording similarity.
- The phrase "how much can I still be holding in January" reads naturally as asking about the carry-over limit (16 days) rather than a separate January-specific rule; no separate January-dated rule was found or needed — the row's carry-over figure directly answers it.
