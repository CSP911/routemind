1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here five years, fully remote: monthly leave accrual rate and max carryover/holding into January?" --member /v1/regions/attendance "accrual rates, tenure, contract type, remote work, and carryover rules for leave are most likely here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_08d2a2 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

2. **Answer**
Accrues 0.94 days per month. Carry-over limit into January is 13 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

4. **Notes**
Leave accrual has three versions in force over different date ranges (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the revision-legend page is explicit that grabbing the newest one is wrong for a question dated before 2026-01-01. Today (2026-09-20) is after that cutoff, so the current table `sec-hard-accrual` was correct here, but this is the kind of question where I'd have gotten the wrong figures entirely if I'd skipped that check or if the question had been dated in 2025. The row is selected by three independent qualifiers (employment type, tenure band, site) each with its own legend translating plain-English phrasing ("on a two-year contract", "been here five years", "fully from home") into codes (E2, T3, L4) — none of that mapping is guessable, it had to be read from the legend files. The row itself also states a carry-over limit (13 days), which directly answers the "how much can I still be holding in January" half of the question — I didn't need a separate carryover-policy document.
