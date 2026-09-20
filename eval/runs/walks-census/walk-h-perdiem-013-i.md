1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body
./bench/rmcli.py table /v1/nodes/evidence
./bench/rmcli.py read /v1/nodes/evidence/body
```

2. **Answer**
Lodging cap: 123 USD per night. Receipt threshold: 36 USD (above this amount, evidence/receipt must be kept for the spend).

(For reference, the same row also gives meals at 67 USD/day and incidentals at 13 USD/day, though those weren't asked.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s4/body (lodging cap and receipt threshold)

4. **Notes**
- The mapping from plain-language facts (job title, city, trip length) to the row's grade/band/stay codes isn't obvious from the per-diem table alone — it requires three separate legend lookups first, and it's easy to miss that the legends exist since the main table just lists 64 rows by code.
- "Three weeks" isn't a literal band label — the stay legend only lists named examples (one night / four nights / eight nights / three weeks), so S4 was a direct match here, not an extrapolation.
- There's a second, unrelated "receipt threshold" concept in this domain: /v1/nodes/evidence/body sets a general 30,000 KRW threshold for when a simple receipt is insufficient and a tax invoice is required for domestic spend evidence. That is a different rule, in a different currency, for a different purpose (evidence quality, not a per-diem cap). It would be easy to answer with 30,000 KRW instead of the per-diem row's own 36 USD "Receipt threshold" field — I checked both and used the per-diem row's field since the question is specifically about the Singapore trip's per-diem, not general domestic evidence rules.
- Confirmed the current (2026-01-01 onward) per-diem table applies rather than the superseded `hard-perdiem-v2` or `overseas-rates`, since today's date (2026-09-20) falls after 2026-01-01.
