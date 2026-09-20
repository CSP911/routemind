1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body

2. **Answer**
The department head signs it off. Yes — three competing quotes are required first. (Delegation limit for this row is 20,008 thousand KRW / ~20 million won; 12 million won falls within it. Expect about 8 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body

4. **Notes**
"A couple of laptops" maps directly and unambiguously to category C1 in the category legend — no nearest-entry judgment call needed. Same for "around 12 million won" → amount V3 and "just the once" → term M1: both phrases are the legend's exact wording, not approximations I had to round to. The one place I could have gone wrong was the version: the procurement table listed three vintages of the threshold data (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) and the revision-legend page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) is safely inside the current table's validity window (2026-01-01 onward), so `sec-hard-threshold` was correct, but I checked the revision page before reading the row rather than assuming — this is exactly the trap the page says to watch for.
