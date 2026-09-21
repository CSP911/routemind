1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, 9 years tenure, Busan branch: monthly leave accrual rate and max carryover holdable in January" --member /v1/regions/attendance "leave accrual and carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_542ea6 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body

2. **Answer**: Accrues 0.98 days per month. Carry-over limit is 14 days — that is the most that can still be held in January.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body (the answer)

4. **Notes**: The legend-revision page was the one place this could have gone wrong — there are three versions of the accrual table with different in-force windows, and the naive move is to grab the newest without checking. Today's date (2026-09-20) falls inside the current table's window (2026-01-01 onward), so `sec-hard-accrual` was correct, but a question dated in 2025 would need `hard-accrual-v2` instead — the legend page was explicit that this is the case where either extreme (always-oldest, always-newest) is wrong. Mapping the three qualifiers was mechanical and unambiguous: "two-year contract" → E2, "nine years" → T4 (exact match, no nearest-band guessing needed), "Busan branch" → L2. No ambiguity in the final row itself.
