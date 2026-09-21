1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**:
Overtime rate has three versions by date. A claim dated in 2025 falls in the second version, in force 2024-07-01 to 2025-12-31, indexed by day (D1–D4) and hours (H1–H4):

| day \ hours | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| D1 | 1.20x | 1.23x | 1.26x | 1.29x |
| D2 | 1.32x | 1.35x | 1.38x | 1.41x |
| D3 | 1.44x | 1.47x | 1.50x | 1.53x |
| D4 | 1.56x | 1.59x | 1.62x | 1.65x |

(The multiplier, rounding rule, and approval requirement beyond this table carried over unchanged from the original rule until 2026-01-01, when a third, current version with a third qualifier — place — took over.)

3. **Source**:
- /v1/nodes/hard-moved-overtime/body (payroll) — pointed away from payroll to attendance, flagged three versions exist
- /v1/nodes/hard-overtime-legend-revision/body (attendance) — confirmed 2025 dates map to the middle version, `hard-overtime-v2`
- /v1/nodes/hard-overtime-v2/body (attendance) — the actual rate table used for the answer

4. **Notes**:
The natural first stop is payroll (since overtime is a pay figure), and payroll's own table listing still shows an "Overtime, night and holiday premiums" entry (`payslip-overtime`) without any obvious red flag in the row description alone — it's easy to click that and quote the wrong, oldest rule (correct only before 2024-07-01). The saving grace is the region-level "When to be here" text on payroll, which explicitly says overtime rates moved to attendance on 2026-01-01, and the `hard-moved-overtime` node, which spells out that there are three versions and that a 2025 date is NOT covered by the page sitting in payroll despite that page never having been marked withdrawn.

The second near-miss: once in attendance, the temptation is to grab `sec-hard-overtime`, labeled "THE CURRENT OVERTIME RATE TABLE" — current as of today's date (2026-09-21), but not current for a claim dated in 2025. Both the moved-overtime note and the legend-revision doc explicitly warn that reaching for the newest table is wrong for anything before 2026-01-01, which is exactly the trap here. The legend-revision doc directly confirms 2025 dates require the middle version, `hard-overtime-v2`, so that's the one used.
