1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body
```

2. **Answer**
For type E3, tenure T2, site L3 (current table, in force from 2026-01-01): accrues 1.16 days per month, with a carry-over limit of 9 days — that is the most you can still be holding in January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies for today's date)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body (figures)

4. **Notes**
Leave accrual has three superseded/current versions with overlapping validity windows, and the oldest version gives no indication it was replaced. Checked `hard-accrual-legend-revision` first to confirm today (2026-09-20) falls under the current table (`sec-hard-accrual`, in force since 2026-01-01) rather than the 2024-07-01–2025-12-31 version — easy to grab the wrong one if you skip that check. The question already gave exact codes (E3/T2/L3), so no legend lookup was needed to translate plain-language qualifiers into codes; went straight from the table listing to the matching row address. "How much can I still be holding in January" maps to the row's "Carry-over limit" field — the max balance retained across the year boundary.
