1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/hard-accrual-v2

2. **Answer**:
Leave accrual has three written versions, and which one governs a claim depends on the claim's date, not on always using the newest:
- Until 2024-07-01: original version (`leave-accrual`)
- 2024-07-01 to 2025-12-31: second version (`hard-accrual-v2`)
- 2026-01-01 onwards: current version (`sec-hard-accrual`)

For a claim dated anywhere in 2025, the applicable version is the middle one — `hard-accrual-v2`, in force 2024-07-01 to 2025-12-31. Neither the oldest nor the current (2026-01-01 onward) table applies.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (explains the three versions and which date range each covers — this is the "where is that written down" answer)
- /v1/nodes/hard-accrual-v2 (confirms this is the specific version in force 2024-07-01 to 2025-12-31, matching a 2025 claim date)

4. **Notes**:
The attendance region table listing is genuinely booby-trapped here: it advertises "current table since 2026-01-01" for leave accrual up front, and the table row for `sec-hard-accrual` is labeled "THE CURRENT LEAVE ACCRUAL TABLE" in bold — it would be easy to grab that one reflexively without checking the claim's date. The legend/revision node exists specifically to stop that mistake, and it says so explicitly: "reaching for the newest is wrong for anything before 2026-01-01" and "the oldest says nothing at all about having been replaced," so skipping the legend and reading the oldest version's body directly would also give false confidence with no warning that it had been superseded. The legend page is the actual answer to "where is this written down" — the version tables themselves don't cross-reference each other.
