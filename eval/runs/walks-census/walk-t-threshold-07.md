1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body

2. **Answer**
The approval threshold has been written 3 times total (2 rewrites of the original):
- Original ("Approval thresholds", at `threshold-table`): in force until 2024-07-01
- Second version (`hard-threshold-v2`): in force from 2024-07-01 to 2025-12-31
- Current version (`sec-hard-threshold`): in force from 2026-01-01 onwards

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/sec-hard-threshold
/v1/nodes/hard-threshold-v2/body

4. **Notes**
The procurement table only lists two of the three approval-threshold files directly (`hard-threshold-v2` and `sec-hard-threshold`); the oldest version is referenced only by name (`threshold-table`) inside the legend-revision and v2 document bodies, never printed as a selectable address by any `table` call I made. Per the rules given (only use addresses a table printed), I did not attempt to open it, so its content beyond "in force until 2024-07-01, had neither category nor term as qualifiers" is not directly verified — only referenced consistently from two independent documents (the legend and v2's own body), which is why I'm confident it exists and about its end date, but I have no primary read of it. Also worth flagging: the legend page itself warns this is the trap case — for a document dated in 2025 you must use the *middle* version, not the newest or oldest — easy to get wrong if you jump straight to `sec-hard-threshold` because it's labeled "current."
