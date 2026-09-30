1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Part-time (3 days/week), 2 years tenure, Seoul office: monthly leave accrual rate and max carryover/holdable balance into January?" --member /v1/regions/attendance "leave accrual, part-time proration, carryover rules likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5d5884 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body /v1/nodes/hard-accrual-legend-revision/body
```

2. **Answer**

Accrues 1.12 days per month. The carry-over limit is 7 days — that is the most that can still be held going into January.

3. **Source**

- /v1/nodes/hard-accrual-legend-type/body (mapped "three days a week" → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (mapped "Seoul office" → site L1)
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions is in force for today's date and for January)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body (the figures: 1.12 days/month accrual, 7-day carry-over limit)

4. **Notes**

- The three qualifiers (employment type, tenure band, site) are each coded through a separate legend document, and none of the codes are guessable from the question's wording — "three days a week" only maps to E3 after reading `hard-accrual-legend-type/body`. Skipping any one legend and guessing the row address would have been easy to get wrong since the row address is built from three independent codes.
- `hard-accrual-legend-revision/body` warns explicitly that reaching for the newest table is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about being superseded. Today's date (2026-09-20) and the "in January" part of the question both fall inside the current table's open-ended "2026-01-01 onwards" range, so the current `sec-hard-accrual` row is correct here — but this is the kind of question where using the wrong version would silently produce a plausible-looking wrong number.
- "How much can I still be holding in January" is answered by the row's carry-over limit (7 days), read as the cap on balance retained across the year boundary — the row doesn't separately spell out a "January" concept, so this is an interpretation of "carry-over limit" as the answer to that phrasing.
