1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body

2. **Answer**
Signs it off: the division director.
Competing quotes required: yes — three competing quotes plus a written comparison.
(Delegation limit for this row: 100,045 thousand KRW; working days to expect: 12.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (established today's date requires the current, 2026-01-01-onward table, not the superseded versions)
/v1/nodes/hard-threshold-legend-category/body (flights and hotels → category C3)
/v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
/v1/nodes/hard-threshold-legend-term/body (renewing every year → term M2)
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body (the answer)

4. **Notes**
The procurement table surfaces three approval-threshold nodes side by side (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with truncated, similar-looking descriptions — it would be easy to grab the first or the most-recently-added one without checking dates. The legend-revision page explicitly warns that the oldest version "says nothing at all about having been replaced," so nothing in the old table itself would flag that it's stale; only cross-checking today's date (2026-09-20) against the revision legend caught this. I nearly skipped straight to the flat `sec-hard-threshold` table and tried to guess a row address by pattern (category+amount+term) rather than reading the three legend files first — the tool's own warning ("Never construct one") plus the fact that the legends are the *only* place the word-to-code mapping is written down made that the wrong shortcut. All three qualifiers (category, amount, term) mapped cleanly to listed values with no ambiguity, so no nearest-entry judgment call was needed here.
