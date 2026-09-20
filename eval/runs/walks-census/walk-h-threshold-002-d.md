1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body

2. **Answer**: For category C1, amount V1, term M3 (current table, in force from 2026-01-01, which applies since today is 2026-09-20): the department head signs it off. Competing quotes required: none — no other prices need to be obtained first. (Delegation limit 1002 thousand KRW; 4 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version's date range applies)
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m3/body (the answer)

4. **Notes**: The procurement region flagged up front that approval-threshold has three versions with overlapping-looking names, and warned specifically against reflexively grabbing the newest one. I checked the legend-revision page before reading the row, which confirmed 2026-01-01-onwards is the current version and today's date (2026-09-20) falls in it — so `sec-hard-threshold` was correct, but it would have been easy to skip that check since C1/V1/M3 as given in the question already look like codes rather than plain language, making it tempting to jump straight to the row without verifying the date/version first. No ambiguity in the row itself: it directly names the signer and states "Competing quotes: none" in the same table, so no separate lookup was needed for the "other prices" half of the question.
