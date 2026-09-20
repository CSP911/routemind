1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

2. **Answer**
Sign-off: the division director.
Competing quotes required: three (yes, other prices must be obtained first).
This is category C3 (flights and hotels), amount band V3 (around 12 million won), term M4 (until we cancel it) — delegation limit for this row is 20,043 thousand KRW, so 12 million won falls within it (no pre-approved-excess procedure applies). Working days to expect: 11.

3. **Source**
/v1/regions/procurement
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/sec-hard-threshold
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

4. **Notes**
The approval-threshold subject has three superseded/current versions (threshold-table, hard-threshold-v2, sec-hard-threshold) with a legend-revision page warning that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version never says it was replaced. Today's date (2026-09-21, per the session's later date reminder — the task text itself said 2026-09-20, a one-day discrepancy that didn't matter here since both fall after 2026-01-01) put this squarely in the current table, so no ambiguity there, but it would be an easy trap on an older-dated question.
The three qualifiers (category/amount/term) each have their own legend page mapping plain-language phrasing to codes, and the row address has to be hand-assembled from all three (c3/v3/m4) — there's no shortcut table matching phrases directly to rows. "Around 12 million won" matched the V3 legend entry exactly ("around 12 million won"), and "until we cancel it" matched M4 verbatim too, so no nearest-entry judgment call was needed this time — but the legend explicitly allows for approximating to the nearest listed value when there's no exact match, which is worth remembering for future walks. Also worth noting: the delegation limit is expressed as "20043 thousand KRW," i.e. 20,043,000 won, not 20,043 won — easy to misread the unit.
