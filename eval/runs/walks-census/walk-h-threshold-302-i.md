1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

2. Answer
Signature: the department head.
Other prices first: no — competing quotes required is "none" for this row.
(Delegation limit for this row is 1,050 thousand KRW, so ~700,000 won falls within it. Working days to expect: 4.)

3. Source
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

4. Notes
The category/amount/term legends are the only place mapping plain-language descriptions to the row codes exists — "dinner with a client" → C4, "about 700,000 won" → V1, and "locked in for three years" → M3 all matched their legend entries exactly (no need to round to a nearest band). The near-miss risk here is term: "locked in for three years" sounds superficially like a one-time purchase (a single dinner), but the question explicitly frames it as a 3-year commitment, so M3 (not M1, "just the once") is correct — this is presumably a recurring/contracted client-entertainment arrangement, not a single meal. Also worth flagging: the procurement table lists three superseded versions of the threshold table (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`); I confirmed `sec-hard-threshold` is "in force from 2026-01-01" and today's date (2026-09-21) falls within that range, so no need to consult the older versions or the legend-revision warning page in detail.
