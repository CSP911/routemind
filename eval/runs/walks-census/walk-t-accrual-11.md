1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py table /v1/nodes/hard-accrual-v2
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body

2. Answer
2023 (oldest rule, in force until 2024-07-01): two years of continuous service falls in the
"1 year and over" band → **15 days granted flat**, on 1 January, as an annual grant (no
monthly accrual, no carry-over).

2025 (the rule in force 2024-07-01 to 2025-12-31, "hard-accrual-v2"): this version pays out
as a **monthly accrual rate**, not a flat annual grant, indexed by employment type AND
tenure band. "Two years of continuous service" maps to tenure **T2**. The question does not
state employment type; taking the closest reading of "continuous service" as regular-payroll
employment (**type E1**, per the type legend), the rate is **0.42 days per month**
(≈5.04 days/year if annualized over 12 months — the source does not itself annualize it).
If a different employment type applies (contract/part-time/partner-firm), the rate differs:
E2/T2 = 0.50, E3/T2 = 0.58, E4/T2 = 0.66 days/month.

So: 15 days/year in 2023 → 0.42 days/month (type E1) in 2025, a change in both the amount
and the unit/method of accrual, not just a number change.

3. Source
/v1/nodes/hard-accrual-legend-revision/body — which of the three accrual versions covers which date
/v1/nodes/accrual-rule/body — 2023 figure (15 days, "1 year and over" band)
/v1/nodes/hard-accrual-v2/body — 2025 figure (monthly rate table by type × tenure)
/v1/nodes/hard-accrual-legend-tenure/body — maps "two years" to tenure T2
/v1/nodes/hard-accrual-legend-type/body — employment-type legend, used to flag the missing qualifier

4. Notes
- The three-version trap is real and explicit: RouteMind has a dedicated warning page
  (hard-accrual-legend-revision) saying the oldest version "says nothing at all about having
  been replaced." Without opening that page first, grabbing the current table
  (sec-hard-accrual, in force from 2026-01-01) for a 2025 question would have been the wrong
  answer — 2025 falls in the middle version (hard-accrual-v2), not the current one.
- The 2023 and 2025 rules are not the same shape of number. 2023 grants a flat 15
  days/year; 2025 gives a monthly accrual rate that has to be multiplied out to compare,
  and the source never does that multiplication itself. Reporting "15 days" vs "0.42" side by
  side without saying what each number means would be misleading — I annualized 0.42 for
  comparison but flagged that this is my computation, not the document's.
- Real ambiguity, not resolved by RouteMind: the 2025 table is indexed by employment type
  as well as tenure, and the question gives no employment type. I assumed "regular payroll"
  (E1) as the most natural reading of "continuous service" but this is a guess — the other
  three type rows (E2 0.50, E3 0.58, E4 0.66 for tenure T2) are equally valid answers under
  a different assumption. I listed all four in the Answer rather than silently picking one.
- Minor near-miss: the current (2026) table's row files are named
  hard-accrual-row-type-e1-tenure-t1-site-l1 etc., which looks superficially like it could be
  reused for 2025 by ignoring the site qualifier — it can't; hard-accrual-v2's own text says
  the pre-2026 versions had "neither type nor site" (oldest) or "type only, no site" (v2), and
  v2's numbers are given directly in its body table rather than through a legend/row scheme.
