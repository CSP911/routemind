1. Commands
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 9 years tenure, Seoul office: monthly leave accrual rate, and max carryover/holding into January" --member /v1/regions/attendance "leave accrual, part-time proration, carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body
./bench/rmcli.py overlay add --id ov_2026-09-20_8db856 --address /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body --why "matching row for E3 (3 days/week), T4 (9 years), L1 (Seoul) — gives monthly accrual and carry-over limit"
./bench/rmcli.py overlay close --id ov_2026-09-20_8db856 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body

2. Answer
You accrue 1.28 days of leave per month. The carry-over limit (the most you can be holding into January) is 13 days.

3. Source
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l1/body

4. Notes
The three-versions warning at hard-accrual-legend-revision/body was the thing that could have gone wrong: there are three separate accrual tables (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and reaching for "the newest" is explicitly called out as wrong for older dates. Today's date (2026-09-20/21) falls in the current table's window, so sec-hard-accrual was correct here, but on a differently-dated question this would need the v2 or oldest table instead.

The row selection itself was mechanical but required all three legends, not just tenure: "three days a week" maps to type E3 (not a site or tenure qualifier, despite reading like a schedule detail), "nine years" maps to tenure T4 (an exact match, not a nearest-below case), and "Seoul office" maps to site L1. It would be easy to only fetch the tenure legend and guess at type/site, which risks landing on the wrong one of 64 rows.

The row also reports a carry-over *limit*, not a running balance — it answers "how much can I hold" as a cap, not as a computed number from actual leave taken. I treated the question's "how much can I still be holding" as asking for that cap, since RouteMind has no record of the person's actual current balance.
