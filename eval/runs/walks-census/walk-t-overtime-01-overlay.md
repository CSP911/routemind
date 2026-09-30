1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2023, what multiplier was paid for ordinary overtime beyond the forty-hour week? Answer under the version of the overtime rate that was in force on that date." --member /v1/regions/payroll "overtime pay rate/multiplier would be documented under payroll rules"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py read /v1/nodes/payslip/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay add --id ov_2026-09-20_b758d6 --address /v1/nodes/hard-overtime-legend-revision/body --why "explains which of three overtime rate versions applies to which date range"
./bench/rmcli.py overlay add --id ov_2026-09-20_b758d6 --address /v1/nodes/hard-overtime-v2/body --why "version in force 2024-07-01 to 2025-12-31 - need to check if this or an earlier v1 covers March 2023"
./bench/rmcli.py overlay remove --id ov_2026-09-20_b758d6 --address /v1/nodes/payslip-overtime/body --why "this payroll page states a single flat old rule without version dates; attendance's legend-revision shows the pre-2026 period actually has multiple versions, so this page is superseded/incomplete for pinpointing March 2023" (failed: HTTP 404, address was never a member of the overlay)
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py overlay add --id ov_2026-09-20_b758d6 --address /v1/nodes/overtime-rate-table/body --why "legend-revision says the version in force until 2024-07-01 (covers March 2023) is indexed as overtime-rate-table - this is the actual answer source"
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b758d6 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body

2. **Answer**:
+50% (a 1.5x multiplier) on the hourly basic pay rate, for ordinary overtime beyond the 40-hour week. This is the rate under the oldest version of the overtime rules, which was in force until 2024-07-01 and so covers March 2023.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (tells which of the three overtime-rate versions applies to which date range; March 2023 falls under the "until 2024-07-01" version, indexed as `overtime-rate-table`)
- /v1/nodes/overtime-rate-table/body (the actual rate table for that version: "Ordinary overtime (beyond the 40-hour week) — +50%")

4. **Notes**:
The first plausible answer, /v1/nodes/payslip-overtime/body under payroll, also gives "+50%" for overtime beyond the standard week and looked like a clean hit — it's reached directly from the payroll region and its own text calls itself "the old rule, correct only before 2026-01-01," which sounds like exactly one clean cutover. It would have been wrong to stop there, though not wrong in the final number: attendance's /v1/nodes/hard-overtime-legend-revision/body reveals the pre-2026 period actually has two distinct rate regimes (one ending 2024-07-01, a second — with a completely different, hours-and-day-indexed multiplier table — running 2024-07-01 to 2025-12-31), and the payroll page doesn't mention this split at all. Anyone taking a date in the 2024-07-01–2025-12-31 window and reading only the payroll page would get "+50%" when the correct answer for that period is the graduated 1.20x–1.65x table in /v1/nodes/hard-overtime-v2/body — a real trap the legend page calls out by name. For March 2023 specifically the two payroll-region and attendance-region sources happen to agree (both land on +50%/1.5x), so the number wasn't at risk here, but the *justification* was: without checking the legend/versioning page, "why this version applies" would have been asserted rather than shown, which is exactly the kind of thing this walk is supposed to catch. The `overlay remove` call for payslip-overtime failed with an HTTP 404 because it had only been visited via `table`/`read`, never actually added as an overlay member — a harmless slip, left in the command log as run.
