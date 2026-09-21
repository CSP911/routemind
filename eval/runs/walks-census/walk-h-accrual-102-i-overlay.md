1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, 8 months tenure, Singapore entity: monthly leave accrual rate and max carry-over into January?" --member /v1/regions/attendance "leave accrual, carry-over, and contract-length rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5d75b3 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body

2. **Answer**
Accrues 0.76 days per month. Maximum carry-over is 6 days.

(This is the row for type E2 — "on a two-year contract" — tenure T1 — "been here eight months" — site L3 — "in the Singapore entity" — under the leave accrual table in force from 2026-01-01, which is the version that applies to today's date, 2026-09-20/21.)

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions applies to today's date)
- /v1/nodes/hard-accrual-legend-type/body (mapped "two-year contract" → type E2)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "eight months" → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (mapped "Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body (the figures: 0.76 days/month accrual, 6-day carry-over limit)

4. **Notes**
The leave accrual subject has three superseded/current versions with overlapping silent history — the oldest version says nothing about being replaced, so date-checking against `hard-accrual-legend-revision` before trusting any figure was necessary; skipping that step and grabbing the first accrual table found would have been the easy way to go wrong. The question phrase "how much can I still be holding in January" reads at first like it might be asking about a separate rollover/expiry policy, but the row's own field is literally "Carry-over limit, days" — no separate carry-over document existed in the working set, so this field is the answer. All three qualifiers (E2/T1/L3) matched their legend rows exactly on wording ("on a two-year contract", "been here eight months", "in the Singapore entity"), so no nearest-neighbor guessing was needed here, unlike cases where the legend note about taking the nearest entry would matter.
