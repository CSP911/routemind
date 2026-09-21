1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "In January 2024, what multiplier was paid for ordinary overtime beyond the forty-hour week? Answer under the version of the overtime rate that was in force on that date." --member /v1/nodes/hard-moved-overtime/body "old payroll page about overtime rates, may hold historical Jan 2024 rate before 2026-01-01 move" --member /v1/regions/attendance "overtime premium rates now live here; may have effective-dated history"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_1ccfc1 --address /v1/nodes/hard-moved-overtime/body --why "payroll page only points elsewhere; actual old-version rate found under attendance/overtime-and-hours instead"
./bench/rmcli.py overlay close --id ov_2026-09-20_1ccfc1 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body

2. **Answer**: +50% (1.5x) — the rate in force until 2024-07-01, which covers January 2024.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (identified which of the three overtime-rate versions applies to a January 2024 date, and that the oldest version's page is `overtime-rate-table`)
- /v1/nodes/overtime-rate-table/body (the actual rate: Ordinary overtime beyond the 40-hour week = +50%)

4. **Notes**:
The payroll region's table explicitly warns that overtime/night/holiday premium rates "moved to attendance on 2026-01-01 — the page still here is the old rule," which made it tempting to read `/v1/nodes/hard-moved-overtime/body` as the answer for a pre-2026 date. That would have been wrong: that page just redirects forward, it doesn't hold the old rate. The real complication is that there are three historical versions of the overtime rate (until 2024-07-01; 2024-07-01 to 2025-12-31; 2026-01-01 onward), all living in the attendance region, and the legend-revision page is explicit that reaching for the newest table is wrong for anything before 2026-01-01, and that the 2024-07-01–2025-12-31 version (`hard-overtime-v2`) is a trap for a 2025-dated question specifically. Since the question date is January 2024 — before 2024-07-01 — neither `hard-overtime-v2` nor the current `sec-hard-overtime` table applies; the correct source is the oldest, unversioned-looking `overtime-rate-table`, which per the legend page's own text "says nothing at all about having been replaced." Without reading the legend-revision page first, it would have been easy to grab `hard-overtime-v2` by mistake since it's the most prominently labeled "second version" and sits right next to the current table in the listing.
