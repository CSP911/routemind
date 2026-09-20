1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body

2. **Answer**
For category C2, amount V1, term M3 (delegation limit 1018 thousand KRW): the department head signs it off. No competing quotes are required (none) — so no, other prices do not need to be obtained first. Expect 4 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-20/21)
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body (the answer)

4. **Notes**
The procurement table area has three superseded/overlapping versions of the approval threshold (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being replaced. Today's date (2026-09-20/2026-09-21) falls after 2026-01-01, so the current table `sec-hard-threshold` was correct, but this was the one place a careless walk could have grabbed the wrong version (e.g. `hard-threshold-v2`) without noticing anything wrong, since that page doesn't flag itself as superseded. Also had to be careful not to conflate "signs it off" (department head) with "competing quotes" (none) — the row bundles both answers together cleanly, so no second document was needed once the right row was found.
