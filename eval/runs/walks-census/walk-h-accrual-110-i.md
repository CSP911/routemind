# Walk h-accrual-110-i

## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body

## Answer
Under the current leave accrual table (in force since 2026-01-01, applicable to today's date of
2026-09-20), for a two-year-contract employee (type E2), with two years of continuous service
(tenure T2), at the Seoul office (site L1):

- Accrues 0.80 days of leave per month.
- Carry-over limit is 7 days — that is the most that can still be held going into January.

## Source
- /v1/regions/attendance (table, area index)
- /v1/nodes/hard-accrual-legend-revision/body (confirms current table applies for a 2026-09-20 question)
- /v1/nodes/sec-hard-accrual (table, current accrual table index)
- /v1/nodes/hard-accrual-legend-type/body (maps "two-year contract" → type E2)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (maps "Seoul office" → site L1)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body (the figures: 0.80 days/month accrual, 7-day carry-over limit)

## Notes
- The legend-revision warning page was the one place this walk could have gone wrong: it flags that
  leave accrual has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01
  onward) and that reaching for the newest is only correct for a 2026 date. Today's date
  (2026-09-20) falls cleanly in the current version's range, so `sec-hard-accrual` was the right
  table, but this is exactly the kind of question where grabbing the first accrual table found
  (rather than checking the legend first) would have silently used the wrong version had the
  question been dated in 2025.
- The three qualifiers (type, tenure, site) each needed their own legend lookup rather than
  guessing at codes — the row addresses are literal three-qualifier codes (e2/t2/l1) and the
  legends state plainly they are "the only place the mapping is written down," so skipping them
  and guessing at a plausible-sounding address would have been wrong per the tool's own warning
  never to construct an address.
- "How much can still be holding in January" maps directly to the row's "Carry-over limit" field;
  no separate table for year-end carryover mechanics was needed since this row states the limit
  outright.
