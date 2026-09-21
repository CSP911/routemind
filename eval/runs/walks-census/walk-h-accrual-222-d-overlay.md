1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E3, tenure T3, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site, in force since 2026-01-01"
./bench/rmcli.py overlay add --id ov_2026-09-20_0ad9ae --address /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body --why "exact row for E3/T3/L3"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0ad9ae --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body
```

2. **Answer**
For type E3, tenure T3, site L3: accrues 1.24 days per month, with a carry-over limit of 12 days (this is what can still be held over into January).

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body

4. **Notes**
The `/v1/regions/attendance` table listed both a current row (`sec-hard-accrual`, in force since 2026-01-01) and two superseded versions (`hard-accrual-v2` for 2024-07-01 to 2025-12-31, and an older one before that) plus a "legend revision" doc explaining which version applies when. Today's date (2026-09-20) falls under the current table, so I went straight to `sec-hard-accrual` without needing the legend-revision doc — but it would have been easy to grab a superseded row by mistake if the date weren't checked first. The phrase "how much can I still be holding in January" maps to the row's "Carry-over limit" field, not a separate January-specific figure — there was no distinct January rule in this row, so I treated carry-over limit as the answer to that half of the question. Worth flagging: I did not open the site/tenure/type legend docs since E3/T3/L3 were given directly as codes matching the row-address pattern exactly, so no ambiguity there.
