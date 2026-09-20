1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**: You build up 0.78 days of leave per month under type E2, tenure T1, site L4. The carry-over limit is 7 days — that is the most you can still be holding when carrying into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**: The type/tenure/site codes (E2, T1, L4) were given directly in the question and matched the row's own labeling exactly, so no detour through the legend files (`hard-accrual-legend-type`, `-tenure`, `-site`) was needed to translate plain-English descriptions into codes. The real risk here was the date: `sec-hard-accrual` is explicitly flagged as the third of three versions of this same subject (`leave-accrual`, then `hard-accrual-v2`, then this one), each with different figures, and the area listing surfaces all three side by side with no visual weight favoring the current one. Grabbing the first "accrual" row without checking `hard-accrual-legend-revision` would risk citing a superseded rate. Today's date (2026-09-20) falls after 2026-01-01, so the current table is correct, but that had to be verified rather than assumed. Also worth flagging: "how much can I still be holding in January" is answered by the row's "carry-over limit" field — the question doesn't use that term, so it would be easy to miss that this is what's being asked about (as opposed to some separate January-specific accrual note, which does not exist).
