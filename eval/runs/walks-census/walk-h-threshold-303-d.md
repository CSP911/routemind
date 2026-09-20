1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body

2. **Answer**
For category C4, amount V1, term M4 (current table, in force from 2026-01-01): the department head signs it off. No competing quotes are required ("Competing quotes: none"). Delegation limit is 1,051 thousand KRW, and 5 working days are expected.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (to confirm which of the three threshold-table versions applies for today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body (the answer itself)

4. **Notes**
The procurement area warns up front that the approval-threshold subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and that reaching for the newest one is only correct if the question's date actually falls in its window — the oldest version doesn't even mention having been superseded, so skipping the legend check and just grabbing `sec-hard-threshold` would have been a lucky guess rather than a checked answer. Today (2026-09-20) does fall in the current table's window, so `sec-hard-threshold` was correct, but I read the legend before trusting that.

The question already supplied the codes (C4, V1, M4) directly, so I didn't need the amount/term legends to translate a description into a code — I only opened the category legend to sanity-check what C4 means ("dinner with a client"), which wasn't strictly necessary but cost nothing. No ambiguity in the row itself: "Competing quotes: none" directly answers "do I have to get other prices first" — no.
