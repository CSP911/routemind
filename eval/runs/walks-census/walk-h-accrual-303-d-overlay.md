1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T1, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "attendance table covers leave accrual and carry-over/holding limits"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body
./bench/rmcli.py table /v1/nodes/sec-days-that-decide-money
./bench/rmcli.py overlay close --id ov_2026-09-20_2deed4 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body

2. **Answer**
For type E4, tenure T1, site L4: accrues 1.42 days per month. The carry-over limit is 7 days — that is the most that can still be held into the next year (January).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed today's date, 2026-09-20/21, falls under the current table, not the superseded versions)
/v1/nodes/sec-hard-accrual (located the specific E4/T1/L4 row)
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body (the figures: 1.42 days/month accrual, 7 days carry-over limit)

4. **Notes**
Leave accrual has three superseded/current versions indexed by date (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision doc warns explicitly that reaching for the newest table is wrong for any question dated before 2026-01-01. Today's date (2026-09-20/21) is safely inside the current table's window, so this wasn't actually a close call — but it would have been easy to skip that check and just grab whichever accrual table looked most obviously "current." I checked it anyway since the warning is explicit about this being the mistake worth avoiding.

The question's mention of "January" is not tied to any special January-only rule — I checked /v1/nodes/sec-days-that-decide-money on the chance there was a specific carry-over deadline or forfeiture date tied to the new year, but that table only covers joining/leaving-month proration, trip allowances, and unused-leave payout timing, nothing about a carry-over cutoff. "How much I can still be holding in January" reads as a plain-language way of asking for the carry-over limit (the cap on what rolls into the new year), which the accrual row already states directly (7 days), so no further table was needed.

Because the type/tenure/site codes (E4/T1/L4) were given directly in the question, the legend tables (site/tenure/type) were not needed to translate a plain-language description into codes.
