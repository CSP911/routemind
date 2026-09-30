1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 8 months tenure, Seoul office: monthly leave accrual rate and max carryover balance allowed in January?" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f7e0b0 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body

2. **Answer**
Accrues 1.36 days per month. Carry-over limit (the most that can be held going into January) is 4 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms today, 2026-09-20/21, falls under the current 2026-01-01-onwards table, not the superseded versions)
/v1/nodes/hard-accrual-legend-type/body ("here from our partner firm" → type E4)
/v1/nodes/hard-accrual-legend-tenure/body ("been here eight months" → tenure T1)
/v1/nodes/hard-accrual-legend-site/body ("at the Seoul office" → site L1)
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body (the row: 1.36 days/month accrual, 4-day carry-over limit)

4. **Notes**
The three-way legend indexing (type/tenure/site) is easy to get wrong if you skip the legend files and guess codes directly — the wording in the question ("here from our partner firm", "been here eight months", "at the Seoul office") happened to match the legend rows verbatim, which made the lookup unambiguous, but I deliberately read all three legends rather than assuming a mapping.

The bigger trap was the version warning on `hard-accrual-legend-revision/body`: leave accrual has three versions (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-accrual-v2`, and 2026-01-01 onward as `sec-hard-accrual`). It was tempting to just grab the newest table since it's the one linked from the region table's "WHY" blurb, but the walk explicitly warns "reaching for the newest is wrong for anything before 2026-01-01" — I checked today's date (2026-09-20/21) against the boundary before trusting `sec-hard-accrual`, since a question phrased identically but dated in 2025 would need `hard-accrual-v2` instead.

I read "how much can I still be holding in January" as asking for the carry-over limit (the balance cap carried into the new year), not a projected balance computed from the accrual rate — the table gives carry-over as a flat per-row limit (4 days) rather than a formula, so no further computation was needed or appropriate.

The overlay close reported all five addresses as "reached" rather than formally tracked members — that's because only the parent table `/v1/regions/attendance` was registered as a --member; the specific legend and row files were discovered while narrowing and weren't separately added with `overlay add`. This didn't affect the answer, just the bookkeeping label.
