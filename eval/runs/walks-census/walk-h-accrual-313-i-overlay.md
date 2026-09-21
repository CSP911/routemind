1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 2 years tenure, fully remote/from home: monthly leave accrual rate, and how much can be held/carried into January?" --member /v1/regions/attendance "leave accrual and carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_22c50d --outcome answered --used /v1/regions/attendance /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

2. **Answer**
Accrues 1.50 days of leave per month. Carry-over limit (the most you can be holding into January) is 10 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l4/body

4. **Notes**
There are three versions of the leave accrual rules (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page warns the newest is not always right for a given question date. Today's date (2026-09-20) is well after 2026-01-01, so the current table (`sec-hard-accrual`) applies without ambiguity — but this is the kind of question where grabbing the newest table without checking would sometimes be wrong.

The employment-type legend had a tempting trap: "on a two-year contract" maps to type E2, which reads suspiciously close to "been here two years" in the question. But that legend entry is about contract type, not tenure length — the question's "here from our partner firm" phrase matches the E4 row exactly and unambiguously, so type E4 was correct, not E2. Tenure ("been here two years") separately and exactly matched T2 in the tenure legend, and "fully from home" matched L4 in the site legend exactly. All three qualifiers matched named entries with no ambiguity, so no nearest-entry judgment calls were needed.
