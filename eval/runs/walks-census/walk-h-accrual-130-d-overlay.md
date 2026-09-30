1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T4, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap by employee type, tenure, and site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_63fe50 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l1/body

2. **Answer**
For type E2, tenure T4, site L1: accrues 0.96 days per month. The carry-over limit (the most you can still be holding, e.g. into January) is 13 days. Leave does not accrue during unpaid leave. An excess not approved in advance is settled at these figures and is not recoverable; an unavoidable excess needs a written statement and is decided by the budget holder.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to today's date, 2026-09-20/21)
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l1/body (the figures themselves)

4. **Notes**
This domain has three versions of the leave accrual table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the oldest version says nothing about being superseded — reading it in isolation would give a wrong answer with no warning sign. Checked the legend-revision doc first to confirm today (2026-09-20) falls under the current table `sec-hard-accrual` (in force from 2026-01-01), not `hard-accrual-v2`. The question already gave the row's qualifiers as codes (E2/T4/L1) rather than plain-language descriptions, so the legend-site/tenure/type lookup docs weren't needed — went straight to the matching row. "How much can I still be holding in January" reads naturally as the carry-over limit (13 days); the table doesn't single out January specifically, so I'm treating the carry-over limit as the general answer to "how much can I be holding" rather than assuming a January-specific reset rule exists elsewhere — nothing in the row or its neighbors suggested a separate January-only figure.
