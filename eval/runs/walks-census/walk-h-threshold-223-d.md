1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

2. **Answer**
The division director signs it off. Yes, other prices are required first: three competing quotes.
(Delegation limit for this row is 20043 thousand KRW; working days to expect is 11 — included for context, not asked.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body (the actual answer)

4. **Notes**
The question gave the qualifiers already coded (C3, V3, M4), so the legend files for translating category/amount/term words into codes were not needed — only the revision-legend mattered here.
The real trap was version drift: the procurement table listing showed both a current table (`sec-hard-threshold`, in force since 2026-01-01) and a superseded one (`hard-threshold-v2`, 2024-07-01 to 2025-12-31), plus an even older one, with a dedicated warning page saying the oldest version "says nothing at all about having been replaced." It would have been easy to grab the first threshold-looking table without checking dates. Today's date (2026-09-21) falls under the current table, so `sec-hard-threshold` was correct, but this is exactly the kind of question where picking the wrong version silently returns a plausible-looking wrong answer — the legend-revision page is what catches that.
