1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In October 2024, how much leave was accrued/granted for E2 staff in service band T2, under the accrual policy in force at that date?" --member /v1/regions/attendance "leave accrual by employee type and service band is an attendance topic"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_6d88f5 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-v2/body

2. **Answer**
0.50 days accrued per month for E2 staff in service band (tenure) T2, under the "leave accrual, second version" (in force 2024-07-01 to 2025-12-31), which covers October 2024.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (established which of the three accrual versions applies to October 2024)
- /v1/nodes/hard-accrual-v2/body (the E2 × T2 = 0.50 figure)

4. **Notes**
Leave accrual has three separate versions in RouteMind, each at a different address, with no cross-links between them except a dedicated legend page (`hard-accrual-legend-revision`). The overlay's own row list surfaced `sec-hard-accrual`, labeled "THE CURRENT LEAVE ACCRUAL TABLE" — that phrasing is a trap: it's current as of the walk's *today* (2026-09-20/21), not as of the question's October 2024 date, and it uses a three-qualifier schema (type, tenure, and site) that postdates 2024. Reading the legend first was what caught this; without it, "current" reads as an invitation to grab `sec-hard-accrual` and report the wrong number. The legend explicitly named 2024-07-01–2025-12-31 as `hard-accrual-v2`'s range, which cleanly contains October 2024, so no ambiguity remained once that page was read. `hard-accrual-v2`'s table itself confirms it added "type and tenure" as its two qualifiers (matching E2/T2 exactly) and explicitly disclaims covering 2026 onward.
