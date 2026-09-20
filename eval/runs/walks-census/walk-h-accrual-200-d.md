1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**: For type E3, tenure T1, site L1 (current table, in force from 2026-01-01): you accrue **1.04 days per month**, and the carry-over limit is **4 days** — that is how much you can still be holding when carrying into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onward table is the right version for a 2026-09-20 question)

4. **Notes**: The row table at `/v1/nodes/sec-hard-accrual` lists 64 rows (4 types × 4 tenures × 4 sites) with near-identical descriptions truncated to "The monthly accrual rate, the carry-over limit and the notice r…", so it would be easy to grab the wrong E/T/L combination by misreading the address — had to read the address string itself (`...-e3-tenure-t1-site-l1...`) carefully rather than the truncated description. Also worth flagging: there are three versions of this table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — today (2026-09-20) is safely inside the current version's range, so no correction was needed, but this is the kind of question where picking the wrong version silently gives a plausible-looking wrong number. The phrase "how much can I still be holding in January" isn't spelled out anywhere as a distinct January-specific rule; I read it as asking about the row's "carry-over limit" field, which is the cap on balance carried from one year into the next (i.e., into January) — no separate January-specific figure exists in this row.
