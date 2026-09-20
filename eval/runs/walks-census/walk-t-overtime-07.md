1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime

2. Answer
The overtime rate has been written three times (two rewrites since the original):
- Version 1 (original): in force until 2024-07-01
- Version 2: in force from 2024-07-01 to 2025-12-31
- Version 3 (current): in force from 2026-01-01 onwards

3. Source
/v1/nodes/hard-overtime-legend-revision/body (the version count and all three dates, stated explicitly)
/v1/nodes/hard-overtime-v2/body (confirms version 2's dates and that it supersedes an earlier rule referred to as `overtime-rate-table`)
/v1/nodes/sec-hard-overtime (confirms the current version's start date of 2026-01-01 and that it replaces `overtime-rate-table` and the older rules)

4. Notes
The walk starts in payroll because that's where "overtime rate" naturally points, and payroll does have a page for it: /v1/nodes/payslip-overtime/body. That page gives rates but no version history at all, and /v1/nodes/hard-moved-overtime/body in payroll describes it only as "the old rule, correct only before 2026-01-01" — implying, wrongly, that there are just two eras (old vs. current). Stopping there would have produced "rewritten once" and the wrong date. The real answer only surfaced after leaving payroll for attendance and finding /v1/nodes/hard-overtime-legend-revision/body, which exists specifically to correct this: it states outright that there are three versions and that the middle one (2024-07-01 to 2025-12-31) is easy to miss because "the oldest says nothing at all about having been replaced." It's unclear whether payroll's payslip-overtime page actually reflects version 1 or some blend, since it isn't dated and isn't reachable from the legend-revision page.

The first version's own document was never opened: its id, `overtime-rate-table`, appears only as plain text inside other documents (hard-overtime-v2 and sec-hard-overtime), never as a full address printed by any table. Per the rule against constructing addresses, I left it unopened — the legend-revision page already gave its effective date range without needing the body.
