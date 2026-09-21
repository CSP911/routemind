1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
```

2. **Answer**
A claim dated in 2025 falls under the second (middle) version of leave accrual, in force from 2024-07-01 to 2025-12-31. This version's monthly accrual rate is indexed by type and tenure (two qualifiers):

| type \ tenure | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| E1 | 0.40 | 0.42 | 0.44 | 0.46 |
| E2 | 0.48 | 0.50 | 0.52 | 0.54 |
| E3 | 0.56 | 0.58 | 0.60 | 0.62 |
| E4 | 0.64 | 0.66 | 0.68 | 0.70 |

Carry-over limit and notice-required figures were not changed in this version and follow the original (pre-2024-07-01) "leave entitlement" rule.

This version is superseded (as of 2026-01-01 by the current table, indexed by three qualifiers, at `sec-hard-accrual`) but is the correct one for any 2025-dated claim.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (explains which of the three versions applies by date)
- /v1/nodes/hard-accrual-v2/body (the applicable version's figures)

4. **Notes**
The attendance table lists three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no obvious date markers in their one-line descriptions except "current" on the newest and "superseded" on the middle one — it would be easy to grab the current table (`sec-hard-accrual`) since it's flagged as authoritative, or the oldest since it's unmarked as superseded and doesn't even mention being replaced. The dedicated legend/revision page is what actually resolves this and explicitly calls out 2025 as the case where "taking either extreme is wrong" — i.e. neither the oldest nor the current table applies. Without reading that legend first, the natural instinct would have been to jump straight to the file explicitly marked "THE CURRENT LEAVE ACCRUAL TABLE," which would have been wrong for a 2025 claim.
