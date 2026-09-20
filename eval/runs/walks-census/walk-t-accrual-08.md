1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**:
For a claim dated in 2025, the applicable leave accrual version is the second one, "Leave accrual, second version," in force 2024-07-01 to 2025-12-31 (indexed by type and tenure, no site qualifier). Monthly accrual rate by type × tenure:

| type \ tenure | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| E1 | 0.40 | 0.42 | 0.44 | 0.46 |
| E2 | 0.48 | 0.50 | 0.52 | 0.54 |
| E3 | 0.56 | 0.58 | 0.60 | 0.62 |
| E4 | 0.64 | 0.66 | 0.68 | 0.70 |

Other figures (carry-over limit, notice required) were unchanged from the original ("leave entitlement") rule until 2026-01-01. The current table (`sec-hard-accrual`, from 2026-01-01) adds site as a third qualifier and does NOT apply to a 2025 date; the oldest table (`leave-accrual`, until 2024-07-01) also does not apply.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (explains which version covers which date range)
- /v1/nodes/hard-accrual-v2/body (the actual 2025-applicable accrual rate table)

4. **Notes**:
The attendance area table listed three separate accrual-related nodes (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no obvious ordering, and the temptation is to grab `sec-hard-accrual` since it's labeled "THE CURRENT LEAVE ACCRUAL TABLE" and sits higher/more prominently in the listing — that would have been wrong for a 2025-dated claim. The legend-revision file exists specifically to head off that mistake and explicitly calls out the 2025 case as "the one where taking either extreme is wrong" (i.e. neither oldest nor current). Reading the legend before picking a table was the right move; without it I'd have defaulted to "current" and given the wrong figures.
