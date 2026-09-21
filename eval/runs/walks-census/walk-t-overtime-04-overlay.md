1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In October 2024, what multiplier was paid for day D2 work in hour band H2? Answer under the version of the overtime rate that was in force on that date." --member /v1/regions/payroll "overtime rate multipliers by day type/hour band are likely payroll policy"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-20_477730 --address /v1/regions/attendance --why "check if attendance's sec-hard-overtime table uses D2/H2 terminology and has version history predating 2026"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_477730 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-v2/body

2. **Answer**: 1.35x

3. **Source**:
- /v1/nodes/hard-moved-overtime/body (established that pre-2026-01-01 dates stay in the payroll/attendance old rules, not the current sec-hard-overtime table)
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the overtime rate has three versions by date; 2024-07-01 to 2025-12-31 is the "second version," indexed by two qualifiers — matching day+hour-band)
- /v1/nodes/hard-overtime-v2/body (the actual table in force 2024-07-01 to 2025-12-31; row D2, column H2 = 1.35x)

4. **Notes**:
The first path I took was a near-miss: the payroll region's warning page (hard-moved-overtime) pointed to `payslip-overtime` as "the old rule, correct only before 2026-01-01," so I read that expecting it to answer the question. It didn't — it's a flat +50%/+100% premium-stacking rule (overtime/night/holiday) with no day or hour-band qualifiers at all, so it can't be the source for a "D2/H2" answer. It would have been easy to stop there and wrongly conclude "not found" or misapply that page's numbers.
The real answer lived in attendance, not payroll, under a separate versioned table (`hard-overtime-legend-revision` → `hard-overtime-v2` → future `sec-hard-overtime`). This versioning wasn't visible from the initial region table or the payroll warning page — only found by widening the overlay to attendance and noticing `sec-hard-overtime`'s neighboring "legend-revision" and "-v2" file rows.
The legend page's own worked example ("for a question dated in 2025 the answer is the middle one") plus the explicit qualifier count ("two qualifiers" for v2 vs. "three qualifiers" for current, which adds place) was the confirming detail that D2/H2 belongs to v2, not the current or oldest table. October 2024 falls cleanly inside v2's 2024-07-01–2025-12-31 window.
