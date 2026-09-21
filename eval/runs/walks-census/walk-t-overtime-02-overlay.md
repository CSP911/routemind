1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "In September 2023, what multiplier was paid for ordinary overtime beyond the forty-hour week? Answer under the version of the overtime rate in force then." --member /v1/nodes/hard-moved-overtime/body "warns overtime premiums moved to attendance on 2026-01-01; need historical rate that applied in Sept 2023" --member /v1/regions/attendance "overtime rates now live here per payroll's redirect note; may hold historical versions"
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py overlay add --id ov_2026-09-20_11d3d8 --address /v1/nodes/hard-overtime-legend-revision/body --why "explains three versions of overtime rate and which dates each covers"
./bench/rmcli.py overlay add --id ov_2026-09-20_11d3d8 --address /v1/nodes/overtime-rate-table/body --why "oldest version, in force until 2024-07-01, covers Sept 2023"
./bench/rmcli.py overlay remove --id ov_2026-09-20_11d3d8 --address /v1/nodes/hard-overtime-v2/body --why "superseded version 2024-07-01 to 2025-12-31, does not cover Sept 2023"
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py overlay close --id ov_2026-09-20_11d3d8 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body

2. **Answer**: +50% (i.e. 1.5x pay) for ordinary overtime beyond the 40-hour week. This is the oldest of three published versions of the overtime rate table (in force until 2024-07-01), which is the version that governs September 2023.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (identified which of the three overtime-rate versions covers Sept 2023)
- /v1/nodes/overtime-rate-table/body (the actual rate: +50% for ordinary overtime)

4. **Notes**: Payroll's own table warns that overtime premiums moved out of payroll into attendance on 2026-01-01, which is a red herring for a distinct reason than the one that actually matters — the real trap is that the overtime rate itself has been rewritten three times (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), all living at different addresses, and the legend-revision page explicitly says the oldest version "says nothing at all about having been replaced," so naively reading /v1/nodes/sec-hard-overtime (labeled "THE CURRENT OVERTIME RATE TABLE") or the v2 page without checking dates would silently give a wrong-era answer. The legend page's own worked example is about a 2025 date needing the middle version, not the oldest — it doesn't spell out the pre-2024-07-01 case, so I had to infer that Sept 2023 falls under the "until 2024-07-01" row myself. My initial overlay member for /v1/regions/attendance turned up a listing that included hard-overtime-v2 and sec-hard-overtime but not the oldest table directly; the oldest table's address (/v1/nodes/overtime-rate-table/body) only surfaced after opening /v1/nodes/sec-overtime-and-hours, a node not obviously about historical rates from its label alone.
