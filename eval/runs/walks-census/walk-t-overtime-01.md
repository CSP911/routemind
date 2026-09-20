1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body

2. **Answer**
+50% (i.e. a 1.5× multiplier) on the hourly basic pay rate, for ordinary overtime beyond the 40-hour week, under the oldest of three overtime-rate versions (in force until 2024-07-01, which covers March 2023).

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (establishes the three versions and which dates each covers)
/v1/nodes/overtime-rate-table/body (the version in force until 2024-07-01, containing the +50% figure for March 2023)

4. **Notes**
The payroll region has its own overtime page, /v1/nodes/payslip-overtime/body, which gives the same +50% figure and reads as a plausible direct answer — its parent page (hard-moved-overtime) only warns that it stopped being correct on 2026-01-01, with no mention of any earlier version boundary. Stopping there would have been an accident rather than a reasoned answer, because the attendance region turns out to hold a three-version history for this exact subject (hard-overtime-legend-revision) that payroll's page never mentions or cross-references: the oldest version runs only to 2024-07-01, a second version covers 2024-07-01 to 2025-12-31, and the current table starts 2026-01-01. The legend explicitly warns that "the oldest says nothing at all about having been replaced," which matches what happened here — nothing in payroll or in the oldest attendance table itself signals that it was superseded partway through. For March 2023 the oldest version applies, and its figure (+50%) happens to match payroll's page, but that agreement is coincidental to this particular date — a question dated in 2025 would need hard-overtime-v2 instead, and taking payroll's page (or the current sec-hard-overtime table) at face value would silently give the wrong version for that case. The real source for a date-sensitive overtime question is the versioned table in attendance, not payroll's unversioned copy.
