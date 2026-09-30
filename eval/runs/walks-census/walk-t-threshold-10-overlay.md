1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 3 July 2024 (two days after the first change), what was the delegation limit or signer for category C2 spend in amount band V2? Use version in force that day." --member /v1/regions/procurement "approval threshold by category, amount and term - matches C2/V2 delegation limit question"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_735aaa --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body

2. **Answer**
5005 thousand KRW — the C2 / V2 cell in the approval-threshold table that was in force from 2024-07-01 to 2025-12-31 (the version covering 3 July 2024).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirms which of the three threshold versions covers 2024-07-03)
/v1/nodes/hard-threshold-v2/body (the C2/V2 = 5005 thousand KRW figure)

4. **Notes**
The approval-threshold subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that grabbing the current table (`sec-hard-threshold`) is wrong for anything before 2026. "Two days after the first change" reads as 2024-07-01 + 2 days = 2024-07-03, which lines up with the question's stated date and points at the middle version (`hard-threshold-v2`), not the oldest or newest — this cross-check is what the legend page seems designed to force.

The one place this could trip someone up: the `hard-threshold-v2` table's column is headed "Who signs it, by category and amount" but every cell in it is a KRW amount, not a name — there's no signer identity anywhere in this version. I'm reporting the amount as the delegation limit rather than inventing a signer, since none is given in this version's table.
