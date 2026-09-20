1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body

2. Answer

Accrues 1.34 days per month. Carry-over limit is 16 days, so that is the most that can still be held into January.

3. Source

/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body

4. Notes

The legend-revision page was the one place that could have gone wrong: leave accrual has three versions (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and it explicitly warns that reaching for the newest table is wrong for dates before 2026-01-01, and that the oldest page never says it was superseded. Today (2026-09-20) falls in the current version's range, so `sec-hard-accrual` was correct, but this was a genuine branch point rather than an obvious default.

The three qualifiers each had a direct, unambiguous match in their legend ("in three days a week" → E3, "been here nine years" → T4, "fully from home" → L4), so no nearest-entry judgment call was needed here — each legend also warns to take the nearest entry and record the choice if there's no exact match, which didn't apply in this case but is worth flagging as a place future walks could go wrong.

"How much can I still be holding in January" reads like it could mean something else (e.g. a rollover deadline or forfeiture date), but the row's only relevant figure is the carry-over limit (16 days), which is the cap on what can be held at any time, including into the new year — so that's what I reported.
