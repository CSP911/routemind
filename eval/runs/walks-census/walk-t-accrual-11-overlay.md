1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "How much leave was accrued/granted for someone with two years of continuous service in 2023, and what had it become by 2025?" --member /v1/nodes/hard-accrual-legend-revision/body "explains which accrual version covers which date range" --member /v1/nodes/hard-accrual-v2/body "version in force 2024-07-01 to 2025-12-31, covers 2025 portion" --member /v1/nodes/sec-hard-accrual "current table since 2026-01-01, may show current version but need older too"
./bench/rmcli.py overlay add --id ov_2026-09-20_0a030f --address /v1/nodes/leave-accrual --why "oldest version, in force until 2024-07-01, indexed by one qualifier (tenure only) — covers 2023"
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0a030f --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/accrual-rule/body /v1/nodes/hard-accrual-v2/body /v1/nodes/hard-accrual-legend-tenure/body

2. **Answer**
- In 2023 (oldest version, in force until 2024-07-01, indexed by tenure only): two years of continuous service falls under "1 year and over" → **15 days**, granted annually on 1 January, no carry-over.
- By 2025 (second version, in force 2024-07-01 to 2025-12-31): two years of continuous service maps to tenure band **T2** (per the tenure legend). This version indexes by two qualifiers — tenure AND employment type — so the rate is no longer a single number. The monthly accrual rate for tenure T2 by type is:
  - E1: 0.42 days/month (≈5.04 days/year)
  - E2: 0.50 days/month (≈6.00 days/year)
  - E3: 0.58 days/month (≈6.96 days/year)
  - E4: 0.66 days/month (≈7.92 days/year)
  The question does not state an employment type, so no single figure can be picked from this table — all four T2 rows are given above. (The 2026-current three-qualifier table, which adds site, was deliberately not used — it does not apply to 2025.)

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (established which of the three versions covers 2023 vs. 2025)
- /v1/nodes/accrual-rule/body (2023 figure: 15 days for 1+ years of service)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "two years" to tenure band T2)
- /v1/nodes/hard-accrual-v2/body (2025 figure: monthly accrual rate by type × tenure)

4. **Notes**
- The trap here was reaching for the current table (`sec-hard-accrual`, in force from 2026-01-01) for the "what had it become by 2025" half. The legend-revision page explicitly warns that a 2025-dated question needs the *middle* version (`hard-accrual-v2`), not the newest — I nearly pulled the current, three-qualifier (tenure+type+site) table before reading that warning.
- The oldest version's address is not `hard-accrual`-prefixed at all — it lives at `/v1/nodes/leave-accrual` → `/v1/nodes/accrual-rule/body`, reached via `/v1/nodes/annual-leave`, not via the `/v1/regions/attendance` row that lists the hard-accrual family. If I'd only followed the hard-accrual-* rows shown in the attendance table, I would have missed the 2023 version entirely and wrongly concluded RouteMind had no pre-2024-07-01 table.
- The 2023 and 2025 figures are not directly comparable in unit: 2023's 15 days is an annual grant with no carry-over; 2025's number is a *monthly accrual rate*, indexed by employment type as well as tenure. I annualized by ×12 for a rough sense of scale, but the document does not itself state an annual total for the v2 table, and the employment type was never specified in the question — so the 2025 answer is genuinely four numbers, not one, and I flagged that rather than guessing a type.
