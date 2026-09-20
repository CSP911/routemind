1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body

2. **Answer**
The division director signs it off. Yes, other prices are required first: two competing quotes are needed. (Delegation limit for this row is 5,007 thousand KRW; expect 8 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirms 2026-09-20 falls under the current table)
/v1/nodes/hard-threshold-legend-category/body (a couple of laptops → category C1)
/v1/nodes/hard-threshold-legend-amount/body (roughly 3 million won → amount V2)
/v1/nodes/hard-threshold-legend-term/body (until we cancel it → term M4)
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body (final answer: signer and quotes)

4. **Notes**
The approval threshold subject has three superseded/current versions, and the legend-revision page warns explicitly that reaching for the newest table is wrong for dates before 2026-01-01 — today (2026-09-20) does fall under the current table (`sec-hard-threshold`), so no trap there, but it's the kind of thing that's easy to get wrong if you don't check the date first. The bigger thing to get right was the term qualifier: "until we cancel it" is an open-ended commitment, and it's tempting to read it as a one-time purchase (term M1, "just the once") since laptops are usually bought outright — but the phrasing matches term M4 verbatim in the legend, implying this is being acquired as a standing/cancel-anytime arrangement (e.g., a lease or subscription) rather than a one-off buy. Using the three legend tables (category/amount/term) independently and combining the codes into a single row address was the only way to get the exact row — the row addresses are not guessable and had to come from the table listing.
