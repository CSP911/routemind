1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Regular payroll, nine years tenure, fully remote: monthly leave accrual and max carryover into January?" --member /v1/regions/attendance "attendance table covers leave accrual and carryover rules"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d53aa0 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

2. **Answer**
Accrues 0.70 days per month. Can hold (carry-over limit) up to 16 days into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l4/body

4. **Notes**
The main trap here is the three-version accrual history: the legend-revision page warns that reaching for the newest table is wrong for dates before 2026-01-01, and a 2025-dated question would need `hard-accrual-v2` instead. Today's date (2026-09-20) falls squarely in the current table's range, so `sec-hard-accrual` was correct, but it would have been easy to skip that check and just grab the newest-looking table.

The other trap is translating the plain-language question into the three index qualifiers: "regular payroll" → type E1, "nine years" → tenure T4 (bucketed as "been here nine years" exactly, not an approximation), and "fully from home" → site L4. Each qualifier lives in its own legend document and none of them repeat the mapping, so all three had to be fetched separately before the row address could be built. "How much can I still be holding in January" maps to the row's "Carry-over limit" field, not a separate January-specific figure — there is no distinct January rule, the carry-over limit is simply what's allowed to persist into the new year.
