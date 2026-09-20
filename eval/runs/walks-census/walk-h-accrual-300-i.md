1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body

2. **Answer**
Accrues 1.36 days per month. Carry-over limit is 4 days — that is the most you can still be holding into January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms today's date, 2026-09-20, falls under the current table, not the superseded ones)
- /v1/nodes/hard-accrual-legend-type/body (maps "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "been here eight months" → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (maps "at the Seoul office" → site L1)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l1/body (the figures: 1.36 days/month, 4-day carry-over limit)

4. **Notes**
- The attendance area lists three accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no indication from their names alone which applies — the legend-revision page is what settles it, and it explicitly warns that the oldest page "says nothing at all about having been replaced," so skipping that check and grabbing the first accrual-looking table found could easily land on a superseded version. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct.
- All three qualifiers in the question happened to be exact, unhedged matches in their legends ("here from our partner firm" = E4 verbatim, "been here eight months" = T1 verbatim, "at the Seoul office" = L1 verbatim), so no nearest-value judgment call was needed here — but the legends' fallback instruction ("take the nearest entry above it and record the choice") is a trap waiting for a slightly different phrasing, worth watching for on similar questions.
- The question's two parts ("accruing per month" and "can still be holding in January") map directly onto two fields in the same row (monthly accrual rate and carry-over limit) rather than needing a separate document — it would be easy to over-search here (e.g. digging into `/v1/nodes/annual-leave` for a carryover rule) when the hard-accrual row already has both figures.
