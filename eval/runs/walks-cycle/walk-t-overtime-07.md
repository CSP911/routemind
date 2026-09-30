1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**:
The overtime rate has been written three times (two rewrites after the original):
- Until 2024-07-01: original version (`overtime-rate-table`, in payroll)
- 2024-07-01 to 2025-12-31: second version (`hard-overtime-v2`, in attendance)
- From 2026-01-01 onwards: current version (`sec-hard-overtime`, in attendance)

3. **Source**:
- /v1/nodes/hard-moved-overtime/body
- /v1/nodes/hard-overtime-legend-revision/body

4. **Notes**:
The payroll area is where overtime "lives" by instinct, but a large warning notice there
(`hard-moved-overtime`) explains the topic moved to attendance on 2026-01-01, and that the page
still in payroll is only the oldest (pre-2024-07-01) version — it says nothing about being
replaced, which is called out explicitly as a trap. That notice pointed to
`hard-overtime-legend-revision` in attendance as the authoritative version table, which is what
answered the question directly — no need to open the three individual rate tables
(`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) since the legend page already
states the version count and date ranges. The near-miss here would have been answering from the
payroll page alone and reporting only one version, or assuming the oldest was still current since
nothing on that page itself says otherwise.
