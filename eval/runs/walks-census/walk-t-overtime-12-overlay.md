1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "Reconciling claims from 2023 and 2025 against the overtime rate: which two versions are needed, and what multiplier was paid under each?" --member /v1/nodes/hard-moved-overtime/body "payroll page says overtime moved to attendance on 2026-01-01; may point to where historical rates live" --member /v1/regions/attendance "overtime rate now lives here per payroll's note"
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py overlay add --id ov_2026-09-20_b4cba2 --address /v1/nodes/overtime-rate-table/body --why "oldest version, in force until 2024-07-01, covers 2023 claim"
./bench/rmcli.py overlay remove --id ov_2026-09-20_b4cba2 --address /v1/regions/attendance --why "was a placeholder table address, not a real member; narrowed to specific nodes instead"
./bench/rmcli.py overlay add --id ov_2026-09-20_b4cba2 --address /v1/nodes/hard-overtime-v2/body --why "middle version, in force 2024-07-01 to 2025-12-31, covers 2025 claim"
./bench/rmcli.py overlay add --id ov_2026-09-20_b4cba2 --address /v1/nodes/hard-overtime-legend-revision/body --why "explains which version covers which date range; already read, confirms 2023->oldest, 2025->v2"
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b4cba2 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body /v1/nodes/hard-overtime-v2/body

2. **Answer**:
Two versions are needed:

- **For the 2023 claim**: the oldest version (in force until 2024-07-01, no day/hour qualifiers). Multipliers: ordinary overtime +50%, night hours (22:00–06:00) +50%, holiday work +50%, night hours worked during holiday work +100% (night and holiday premiums stack; overtime premium does not also stack on top of those two).

- **For the 2025 claim**: the second version ("v2", in force 2024-07-01 to 2025-12-31, indexed by day and hours worked). Multiplier table:

  | day \ hours | H1 | H2 | H3 | H4 |
  |---|---|---|---|---|
  | D1 | 1.20x | 1.23x | 1.26x | 1.29x |
  | D2 | 1.32x | 1.35x | 1.38x | 1.41x |
  | D3 | 1.44x | 1.47x | 1.50x | 1.53x |
  | D4 | 1.56x | 1.59x | 1.62x | 1.65x |

  (Rounding rule and approval requirements beyond this table carried over unchanged from the oldest version.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (identified which version covers which date range)
- /v1/nodes/overtime-rate-table/body (2023 claim — oldest version, +50%/+100% premiums)
- /v1/nodes/hard-overtime-v2/body (2025 claim — middle version, day/hours multiplier table)

4. **Notes**:
The payroll region's own page (`/v1/nodes/hard-moved-overtime/body`, pulled into the overlay first but not read since its summary line said it all: overtime moved to attendance on 2026-01-01) is a trap for a naive walk — it only tells you where the *current* rule lives, not that there are three historical versions of it. The real fork is inside attendance: a `hard-overtime-legend-revision` page explicitly warns there are three versions (oldest, "v2" for 2024-07-01–2025-12-31, and current from 2026-01-01) and that reaching for either extreme (oldest or current) is wrong for a 2025 date — you need the middle one. Without that page, the obvious move for a 2025 claim would have been to grab the current table (`sec-hard-overtime`), which would be wrong since that only took effect 2026-01-01. The oldest table's address (`overtime-rate-table`) is not given as a full path anywhere — the legend revision page only names it as a bare id — so it had to be located by browsing `sec-overtime-and-hours`, whose listing has an entry with that exact slug. The two tables aren't structurally comparable: the 2023 version is a flat set of category premiums (+50%/+100%), while the 2025 version is a 2-qualifier day×hours matrix — so "what multiplier" doesn't reduce to a single number for the 2025 side.
