1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.26x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

4. **Notes**: The obvious first stop is payroll, since overtime premiums live on a payslip — but payroll's own table flags that overtime premiums moved to attendance on 2026-01-01, and since today (2026-09-20) is after that date, the payroll version (`payslip-overtime`) would have been the wrong, superseded answer. The attendance area itself also carries an old superseded overtime table (`hard-overtime-v2`, in force 2024-07-01 to 2025-12-31) sitting right next to the current one (`sec-hard-overtime`) — easy to grab the wrong one if you don't check the "in force" dates. The three legends (day/hours/place) had to be read in full before picking a row, since "an ordinary Tuesday" → D1, "about ninety minutes" → H1, and "on standby at home" → P3 are not guessable from the row address list alone — the wording matches the legend rows almost verbatim, which is the intended path, but it would be easy to instead map "on standby at home" to "from home" (P4) if read too quickly; the legend distinguishes standby-at-home (P3) from plain from-home (P4) explicitly.
