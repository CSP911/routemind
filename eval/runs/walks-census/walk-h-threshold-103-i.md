1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body
```

2. **Answer**
The department head signs it off. No competing quotes are required (0 needed).
This falls under category C2 (a consultant's time), amount V1 (about 700,000 won), term M4 (until we cancel it) — delegation limit 1,019 thousand KRW, 5 working days to expect.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirms current 2026-01-01 table applies, given today's date)
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body (final answer)

4. **Notes**
The approval threshold subject has three historical versions (legend-revision warns explicitly about this), so checking today's date (2026-09-20/21) against the "in force" ranges before reading a row was necessary — using the current table (`sec-hard-threshold`, in force from 2026-01-01) without that check could have been right by luck but not by reasoning. The three qualifiers (category/amount/term) are each defined in a separate legend page that doesn't repeat in the row itself, so all three had to be read before the specific row address could even be constructed — the "until we cancel it" wording in the question maps directly and unambiguously to term M4, and "a consultant's time" to category C2, so no interpretation was needed there. No ambiguity or wrong turns in this walk.
