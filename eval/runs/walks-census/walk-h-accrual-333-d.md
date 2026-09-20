1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body

2. **Answer**:
For type E4, tenure T4, site L4 (current table, in force since 2026-01-01):
- Accrues 1.66 days of leave per month.
- Carry-over limit is 16 days — that is the most you can still be holding into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body

4. **Notes**:
The attendance area lists three versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), each superseding the last, plus a legend-revision file warning about exactly this. It would have been easy to grab a superseded row by mistake. I confirmed `sec-hard-accrual` is the one in force from 2026-01-01 with no stated end date, so it covers both today (2026-09-20) and the January in question, and went straight to the E4/T4/T4... row (type E4, tenure T4, site L4) since the table listing already indexed rows by exact type/tenure/site code — no need to open the legend files since the question already gave codes directly rather than descriptions needing translation. The "carry-over limit" field is what I'm reading as the answer to "how much can I still be holding in January" — the table doesn't use the word "January" itself, so this is an inference that carry-over limit = cap on balance held into the new year, which is worth flagging as the one interpretive step in an otherwise direct lookup.
