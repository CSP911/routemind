1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V2, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01, covers category/amount/term -> signer"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_758733 --outcome answered --used /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body

2. **Answer**:
For category C2, amount V2, term M2: the department head signs it off. Yes, other prices are required first — two competing quotes. (Delegation limit for this row is 5021 thousand KRW; 6 working days to expect.) This is the current table, in force from 2026-01-01, so it applies as of today (2026-09-21).

3. **Source**:
/v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body (the row itself, which is what the answer came from)
/v1/nodes/sec-hard-threshold (the current threshold table this row belongs to, used to confirm it is the in-force version)

4. **Notes**:
The question's "C2/V2/M2" looked like it might be a template that failed to fill in with real values — but rmcli's table listing under /v1/regions/procurement showed these are literal row-address components (category c1-c4 × amount v1-v4 × term m1-m4), so the question was answerable exactly as asked once the corresponding row address was found in the overlay listing.

There are three superseded/current versions of the threshold table (`threshold-table` → `hard-threshold-v2` → the current `sec-hard-threshold`, effective 2026-01-01), flagged by a `hard-threshold-legend-revision` warning file in the procurement table. I did not open the older versions or the revision-legend file since the row I read stated its own effective date (2026-01-01) and today (2026-09-21) falls inside it — but it would be easy to grab the SUPERSEDED `hard-threshold-v2` row by mistake if working faster and not checking the "in force from" line at the bottom of the row.

Minor oddity: when creating the overlay I only added the parent table `/v1/nodes/sec-hard-threshold` as a member (not the specific row), then read the row directly from the address the overlay table printed. On close, rmcli noted the used row was "reached = answered from somewhere the overlay never named" — i.e. reading a sub-row isn't automatically registered as a member of the overlay. Worth explicitly `overlay add`-ing the exact row next time to avoid that flag.
