1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two-year contract, two years tenure, Seoul office: monthly leave accrual rate and max carry-forward/holding into January?" --member /v1/regions/attendance "leave accrual and carry-over rules likely live in attendance table"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_70dc6b --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body
```

2. **Answer**
Accrues 0.80 days of leave per month. Carry-over limit (the most that can still be held going into January) is 7 days.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body — establishes today's date (2026-09-20/21) falls under the current (2026-01-01 onward) accrual table, not the superseded versions
- /v1/nodes/hard-accrual-legend-type/body — "on a two-year contract" → type E2
- /v1/nodes/hard-accrual-legend-tenure/body — "been here two years" → tenure T2
- /v1/nodes/hard-accrual-legend-site/body — "at the Seoul office" → site L1
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body — the row itself: 0.80 days/month accrual, 7-day carry-over limit

4. **Notes**
The attendance area has three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the older ones don't announce that they've been superseded — the legend-revision doc is the only thing that flags this, and it's easy to miss since it's listed as just one more row among many in the overlay table. Skipping it and grabbing the first accrual-looking row would have risked pulling stale figures. Also worth noting: none of the three qualifiers (E2/T2/L1) map obviously from plain language — each required its own legend lookup, and the legends explicitly warn to pick the "nearest entry" if an exact match isn't listed, which didn't end up mattering here since all three inputs matched exactly. The overlay close command reported the used addresses as "reached" rather than a plain confirmation — noting it here in case that phrasing is meaningful, but it didn't appear to indicate an error.
