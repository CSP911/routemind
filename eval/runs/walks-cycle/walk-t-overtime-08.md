1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**
The overtime rate has three versions, and which one applies is decided by the date on the claim, not by where you happen to land first. A 2025-dated claim falls in the 2024-07-01 to 2025-12-31 window, so the applicable version is `hard-overtime-v2` (indexed by day and hours):

| day \ hours | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| D1 | 1.20x | 1.23x | 1.26x | 1.29x |
| D2 | 1.32x | 1.35x | 1.38x | 1.41x |
| D3 | 1.44x | 1.47x | 1.50x | 1.53x |
| D4 | 1.56x | 1.59x | 1.62x | 1.65x |

The version-selection rule itself ("which version applies to which date") is written down in `hard-overtime-legend-revision` in attendance.

3. **Source**
- /v1/nodes/hard-overtime-legend-revision/body (which version applies to a 2025 date — the answer to "where is that written down")
- /v1/nodes/hard-overtime-v2/body (the actual rate table for that version)
- /v1/nodes/hard-moved-overtime/body (pointer, found via payroll, that redirected the search to attendance)

4. **Notes**
- The natural first stop is payroll (overtime is a pay topic), but payroll's own page (`hard-moved-overtime`) warns that it holds only the *oldest* rule (correct before 2024-07-01) and explicitly says a 2025-dated question is not answered there — it redirects to attendance. Trusting the payroll table at face value would have given the wrong (oldest) version.
- The easy mistake once in attendance: `sec-hard-overtime` is labeled "THE CURRENT OVERTIME RATE TABLE" and sits right next to the version-legend node in the table listing — reaching for "current" is the wrong instinct here since "current" means 2026-01-01 onward, and the claim is dated 2025. The legend node (`hard-overtime-legend-revision`) is explicit that this is exactly the trap: "taking either extreme is wrong" for a 2025 date — neither the oldest (`overtime-rate-table`) nor the current (`sec-hard-overtime`) table applies; only the middle version (`hard-overtime-v2`) does.
- Both payroll's `hard-moved-overtime` and attendance's `hard-overtime-legend-revision` independently state which node is authoritative for date-to-version mapping, so the two sources agree and cross-confirm.
