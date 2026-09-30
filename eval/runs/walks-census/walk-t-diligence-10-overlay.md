1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 3 July 2024 (two days after the first change) — what screening was required for an origin O2 supplier at contract value W2? Use the version in force on that day." --member /v1/regions/procurement "procurement table covers approval thresholds/screening by supplier origin and contract value"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py table /v1/nodes/hard-diligence-v2
./bench/rmcli.py overlay close --id ov_2026-09-20_4c399b --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-v2/body

2. **Answer**
Checks-required code 35, for origin O2 / value W2, under the supplier due diligence version in force from 2024-07-01 to 2025-12-31 (3 July 2024 falls in this window — two days after the version's 2024-07-01 start, which is "the first change").

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirms which of the three supplier-due-diligence versions covers 2024-07-03)
- /v1/nodes/hard-diligence-v2/body (the origin×value matrix in force for that date; O2/W2 → 35)

4. **Notes**
The phrase "two days after the first change" was the key to picking the right version: supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and 2024-07-01 is the start date of the second version — so "the first change" is that transition, and 3 July 2024 is two days into the resulting version. The legend-revision page states this plainly and warns against defaulting to the newest table, so I checked it before trusting the matrix.

The one near-miss: the current (2026-01-01-onward) table at /v1/nodes/sec-hard-diligence is a three-qualifier system (origin × value × goods) with per-cell explanatory files, which made it look like the "real"/detailed answer format. It is not in force for July 2024 and doesn't apply here — I opened its table only to confirm the v2 matrix (which has no goods qualifier and no per-cell legend) really is self-contained and not missing a companion legend file. It is: hard-diligence-v2 has no sibling legend/goods files, so its own two-qualifier matrix is the whole answer, and the value in the O2/W2 cell (35) is the check-code itself rather than a named screening procedure — the source document does not decode it further for this version.
