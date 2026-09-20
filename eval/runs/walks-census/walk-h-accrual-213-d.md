1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

2. **Answer**
For type E3, tenure T2, site L4 (current table, in force from 2026-01-01, which applies to today's date of 2026-09-20):
- Accrues 1.18 days per month.
- Carry-over limit is 10 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

4. **Notes**
Leave accrual has three versions in force over different date ranges (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend page warns the oldest version never says it was superseded — so grabbing the first accrual-looking hit without checking dates would have been wrong. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct; this was a live risk, not a hypothetical one, since the question gives no date itself and it would be easy to assume "current" without checking. The question's three qualifiers (E3, T2, L4) mapped directly onto row codes without needing the legend files for type/tenure/site, so I skipped opening those — worth flagging in case that mapping isn't actually 1:1 in all cases. "How much can I still be holding in January" reads naturally as the carry-over limit field, but the table doesn't use the word "January" or "carry into the new year" anywhere, so that interpretation is inferred rather than stated outright.
