1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 3 July 2024 (two days after the first change), how much leave was accrued or granted for type E2 staff in service band T2? Use the version in force on that day." --member /v1/regions/attendance "leave accrual/grant by staff type and service band is an attendance topic"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_193715 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-v2/body

2. **Answer**: 0.50 days per month (monthly accrual rate for type E2, service band T2, under the version in force 2024-07-01 to 2025-12-31).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-v2/body

4. **Notes**: Leave accrual has three versions indexed by date, and the legend page explicitly warns against reaching for the newest one — the current table (`sec-hard-accrual`) only applies from 2026-01-01, so it would have been wrong here despite being the most prominent "CURRENT" table in the working-set listing. The question's phrasing ("two days after the first change") matches the 2024-07-01 boundary where the second version (`hard-accrual-v2`) takes effect, which cross-checks that 3 July 2024 falls inside that version's 2024-07-01–2025-12-31 range rather than the oldest, undated-boundary version. The oldest version's page reportedly never mentions being superseded, which is the trap the legend page exists to prevent — a version-blind read of the oldest table would have looked complete and self-consistent while being wrong for this date.
