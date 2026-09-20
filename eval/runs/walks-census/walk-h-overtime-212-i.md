1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

2. **Answer**: Multiplier 2.34x, minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/regions/payroll (routed away — overtime moved to attendance 2026-01-01)
/v1/regions/attendance
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

4. **Notes**: The first instinct is to look in payroll for "what pays what," but payroll's own table explicitly flags that overtime/night/holiday premium rates moved to attendance on 2026-01-01, with a hard-moved-overtime warning node — that redirect is easy to miss if you jump straight to payslip line items. Attendance itself has THREE versions of the overtime table (a legend-revision warning node lists them), so picking sec-hard-overtime (current, in force since 2026-01-01) rather than hard-overtime-v2 (2024-07-01 to 2025-12-31, superseded) matters — using the wrong version would give a different multiplier/rounding silently. The row table itself gives no direct way to search by plain-language terms ("Liberation day", "three hours", "on standby at home") — each of the three qualifiers (day/hours/place) has to be translated through its own legend file into a D/H/P code first, then the single matching row (d3-hours-h2-place-p3) is assembled from those codes. Getting any one of the three legend lookups wrong yields a different, silently wrong row of the 64.
