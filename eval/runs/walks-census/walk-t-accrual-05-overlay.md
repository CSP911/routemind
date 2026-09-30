1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "In March 2025, how much leave was accrued or granted for type E2 staff in service band T2? Answer under the version in force on that date." --member /v1/nodes/hard-accrual-legend-revision/body "explains which accrual version covers which date range" --member /v1/nodes/hard-accrual-v2/body "candidate version in force 2024-07-01 to 2025-12-31, covers March 2025" --member /v1/nodes/sec-hard-accrual "current table since 2026-01-01, likely NOT applicable to March 2025 but keep for comparison"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5ad4ee --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 days per month monthly accrual rate for type E2, tenure/service band T2, under the leave accrual version in force from 2024-07-01 to 2025-12-31 (which covers March 2025).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (established March 2025 falls under the "second version," not the oldest or the current 2026 table)
- /v1/nodes/hard-accrual-v2/body (the type-by-tenure rate table itself; E2 row, T2 column = 0.50)

4. **Notes**: The attendance table lists three separate accrual documents (a pre-2024-07-01 page, `hard-accrual-v2`, and the current `sec-hard-accrual`), and none of them announce in their own title that an older or newer version exists — that's exactly why the legend-revision page exists, and skipping it would have been the easy mistake. The trap is real: `sec-hard-accrual` (the current, 2026-01-01 table) is indexed by three qualifiers (type, tenure, *and* site) and expands into dozens of per-row files like `hard-accrual-row-type-e2-tenure-t2-site-l1/body` — grabbing one of those for a March 2025 question would silently answer with the wrong-era rule, and worse, would force picking an arbitrary site the question never specified. The legend-revision page explicitly names this failure mode ("reaching for the newest is wrong for anything before 2026-01-01") and states the v2 table is the correct one for any 2025 date. The v2 table itself confirms it uses only two qualifiers (type × tenure, no site), which matches the question's inputs exactly. One naming ambiguity worth flagging: the question says "service band T2" while the documents call this dimension "tenure" — the tenure legend describes it as continuous-service banding, so I treated "service band" and "tenure" as the same axis; I did not need to open the tenure-legend file itself since the v2 table's column header already reads "T2" directly.
