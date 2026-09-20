1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**
Signature needed: the department head.
Competing quotes required: none.
(Delegation limit for this row is 1,035 thousand KRW; working days to expect is 5.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body
/v1/nodes/hard-threshold-legend-revision/body (confirms the current table applies for today's date, 2026-09-20)

4. **Notes**
The three qualifiers ("flights and hotels" → category C3, "about 700,000 won" → amount V1, "until we cancel it" → term M4) each had to be looked up separately in dedicated legend files before the row address could be built — nothing in the question maps directly to the row address, and the tool warns explicitly never to construct an address, so all three legends had to be read first. The real trap was the threshold table's revision history: there are three superseded versions (pre-2024-07-01, 2024-07-01–2025-12-31, and the current one from 2026-01-01), and the oldest version "says nothing at all about having been replaced" — so if I hadn't checked the revision-legend page I could easily have trusted an old row that looked complete and self-contained. Today's date (2026-09-20/21) falls under the current table (sec-hard-threshold), which was the one I already used, so no correction was needed here, but it was worth verifying explicitly rather than assuming "current" was current.
