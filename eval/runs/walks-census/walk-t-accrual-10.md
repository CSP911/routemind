1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 (monthly accrual rate) for type E2, service band T2.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-v2/body

4. **Notes**: The date 2024-07-03 is exactly two days after 2024-07-01, the date the legend
page names as when the first change took effect (the original undated "leave entitlement"
rule in `leave-accrual` gave way to the "second version" in `hard-accrual-v2`). That put
2024-07-03 inside the `hard-accrual-v2` window (2024-07-01 to 2025-12-31), so that table is
the version in force on the day in question — not the oldest table and not the current
`sec-hard-accrual` table (which only starts 2026-01-01). The legend page's explicit warning
that "the oldest says nothing at all about having been replaced" was the useful guardrail
here: without it, a plain date-range read could easily have stopped at the older, undated
table and missed that it had been superseded. The v2 table only carries a "type × tenure"
grid (two qualifiers, as the legend promised) — E2/T2 reads directly off it as 0.50, with no
ambiguity about which cell to use.
