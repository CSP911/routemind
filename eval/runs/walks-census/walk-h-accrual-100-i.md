1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body
```

2. **Answer**
You accrue 0.72 days of leave per month. The carry-over limit is 4 days, so that is the most you can still be holding in January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
- /v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
- /v1/nodes/hard-accrual-legend-tenure/body (eight months → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (Seoul office → site L1)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body (the figures: 0.72 days/month accrual, 4-day carry-over limit)

4. **Notes**
- The attendance table's warning about leave accrual having three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01) was the one place I could have gone wrong — it's tempting to grab the first accrual-looking row without checking which version's date window covers today (2026-09-20). The legend-revision page confirmed the current table (`sec-hard-accrual`) is the right one.
- The three legends (type/tenure/site) map plain-language descriptions to codes and explicitly warn that the accrual rows "do not repeat" the human-readable descriptions — so skipping straight to a row address without reading all three legends risks guessing the wrong E/T/L combination. Each of the three inputs in the question (two-year contract, eight months, Seoul) matched a legend entry exactly, with no fuzzy "nearest entry" judgment needed.
- The row itself answers both halves of the question directly: "Accrues per month, days" for the monthly build-up, and "Carry-over limit, days" for how much can still be held into January. No separate carryover/forfeiture table was needed.
