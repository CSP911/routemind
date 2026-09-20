1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body

2. **Answer**
You accrue 1.42 days per month. The carry-over limit is 7 days — that is the most you can still be holding in January (i.e. carried into the new year).

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body

4. **Notes**
The attendance region lists three accrual versions (a legend-revision warning, plus `hard-accrual-v2` and `leave-accrual` as superseded pages) — easy to grab a stale table by mistake. Went straight for `sec-hard-accrual`, explicitly marked as the current table in force from 2026-01-01, which covers today's date (2026-09-20). The E4/T1/T1/L4 codes in the question matched the row address directly, so no detour through the type/tenure/site legend files was needed. The row itself doesn't use the word "January" or "carry-over into the new year" explicitly — it just states a "carry-over limit" of 7 days — so reading that as the answer to "how much can I still be holding in January" required inferring that carry-over limit is evaluated at year boundary, which is the only figure in the row that plausibly answers a January-balance question.
