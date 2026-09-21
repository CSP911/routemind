1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Singapore, 2-year contract, 2 years tenure: monthly leave accrual and max carry-forward balance in January" --member /v1/regions/attendance "leave accrual rate and carry-over/cap rules likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_14c4e6 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body

2. **Answer**
Accrues 0.84 days of leave per month. Carry-over limit is 9 days — that is the most you can still be holding once the year turns over into January.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body

4. **Notes**
The three legends (type, tenure, site) are the part easy to get wrong — the accrual table is indexed by codes (E2/T2/L3), not by the plain-language descriptions in the question, and each legend lives in its own separate node rather than inline in the row table, so all three had to be fetched before the row address could even be picked. Mapping was straightforward and unambiguous here: "two-year contract" → E2, "been here two years" → T2, "Singapore entity" → L3, each an exact match in its legend rather than a nearest-fit guess. The table itself is dated "in force from 2026-01-01" and today is 2026-09-21, so this is the current, correct version — no need to fall back to the superseded `hard-accrual-v2`. The row's "carry-over limit" field is what answers "how much can I still be holding in January," since that limit is what survives the year-end rollover; the table doesn't spell out the January framing explicitly, so that inference is mine, not a quote from the source.
