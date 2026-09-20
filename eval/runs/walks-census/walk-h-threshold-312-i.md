1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body
```

2. **Answer**
Signature: the department head signs it off.
Quotes: yes — two competing quotes are required.
(Delegation limit for this row is 5,054 thousand KRW; 7 working days to expect.)

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions applies to today, 2026-09-21 → current table)
- /v1/nodes/hard-threshold-legend-category/body (mapped "dinner with a client" → category C4)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3)
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body (the answering row)

4. **Notes**
The "locked in for three years" phrase is what made this a procurement/approval-threshold question rather than a plain expense-report question — on first read it sounds like it's just describing a one-off client dinner, and it would be easy to route straight to /v1/regions/expense and miss the term dimension entirely. The three qualifiers (category, amount, term) all had to be looked up in separate legend files before the row address could be built, and none of the three "what you have" phrasings match the row's code vocabulary by eyeballing — they have to be read literally against the legend tables. Also worth flagging: there are three superseded versions of this threshold table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and the legend-revision page warns that the oldest version doesn't self-identify as replaced. Today's date (2026-09-21) falls under the current table, but it would be easy to grab a stale row if that check were skipped.
