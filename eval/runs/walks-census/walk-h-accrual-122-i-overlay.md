1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here five years, in the Singapore entity: how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover cap questions live under attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2698ab --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
Accrues 0.92 days per month. Carry-over limit is 12 days (the most you can still be holding once the new year turns over, so this is the figure for January). Also: 5 working days' notice is required to take leave, and this type does not accrue during unpaid leave.

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body

4. **Notes**:
The table is indexed by three independent qualifiers (type, tenure, site) that only resolve through their legends — "two-year contract" → type E2, "five years" → tenure T3, "Singapore entity" → site L3 — so the row address (hard-accrual-row-type-e2-tenure-t3-site-l3) can't be guessed from the question wording; it has to be assembled after reading all three legends.

The near-miss: this subject has three superseded versions (leave-accrual, hard-accrual-v2, sec-hard-accrual) with different indexing schemes, and the revision-legend page warns explicitly that reaching for the newest is wrong for any question dated before 2026-01-01. Today is 2026-09-20 and the question's "January" plainly means the upcoming one, so the current sec-hard-accrual table (in force from 2026-01-01) is right here — but this is exactly the kind of question where grabbing the current table without checking the date would happen to work today and quietly be wrong on an earlier-dated walk. Checked the revision legend anyway before closing, since the row itself doesn't say why it's the right version, only that it is one of three.

"How much can I still be holding in January" is not phrased as "carry-over limit" anywhere in the source, so it took inference to map the question to that field rather than, say, a separate forfeiture-deadline document — no such separate document turned up in the working set, and the row's own carry-over figure is the only number that answers "still holding."
