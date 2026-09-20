1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

2. Answer
Category C4 (dinner with a client), amount V4 (about 40 million won), term M4 (until we cancel it).
Delegation limit: 100,063 thousand KRW. Signs it off: the CFO. Competing quotes required: three, plus a written comparison. Working days to expect: 14.
So: yes, you need the CFO's signature, and yes, you must get three competing quotes with a written comparison before approval.

3. Source
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

4. Notes
The three qualifiers (category/amount/term) each mapped cleanly onto a legend entry with no "nearest entry" guessing needed: "dinner with a client" is a literal legend row (C4), "about 40 million won" matches "about 40 million won" (V4) exactly, and "until we cancel it" matches "until we cancel it" (M4) exactly — the question's wording appears to have been lifted straight from the legends, so there was no ambiguity in classification.
The real trap was the date. The procurement table's own listing flagged that the approval threshold subject has three superseded versions, and a revision-legend page exists specifically warning not to reach for the newest table by default — for a 2025-dated question the middle version (hard-threshold-v2) would be correct, not the current one. Today's date (2026-09-21) falls after the current table's 2026-01-01 effective date, so sec-hard-threshold was correct here, but this is clearly the deliberate trap of the walk and skipping the revision-legend check would have been the wrong move on a different date.
