1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body
```

2. **Answer**

Accrues 1.22 days per month. Carry-over limit into the new year (January) is 11 days.

(Row: type E3 — "in three days a week"; tenure T3 — "been here five years"; site L2 — "at the Busan branch". Current table, in force since 2026-01-01, applies since today is 2026-09-20.)

3. **Source**

- /v1/nodes/hard-accrual-legend-revision/body (established which version applies today)
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body (figures: 1.22 days/month accrual, 11 days carry-over limit)

4. **Notes**

- There are three versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table, so this wasn't a trap here, but it's the kind of thing that's easy to get wrong on a similarly-phrased question dated in 2025.
- The three qualifiers ("three days a week", "five years", "Busan branch") each had to be translated through a separate legend file into a code (E3/T3/L2) before the row address could be built — none of these mappings are guessable from the question's wording alone (e.g., "three days a week" isn't "part-time," it's literally type E3, a specific row in the type legend).
- "How much can I still be holding in January" reads like it's asking about a carryover cap that might live in a separate annual-leave/carryover policy page, but the same accrual row already had a "Carry-over limit, days" field (11), so no separate lookup was needed — worth being careful not to over-search once the row itself answers both halves of the question.
