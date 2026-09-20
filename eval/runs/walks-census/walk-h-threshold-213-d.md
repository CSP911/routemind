1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body

2. **Answer**
Yes, other prices (quotes) are required first: two competing quotes are needed. The division director signs it off. (Delegation limit for this row is 5,039 thousand KRW, with 8 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m4/body
(supporting: /v1/nodes/hard-threshold-legend-revision/body — confirmed today's date, 2026-09-21, falls under the current 2026-01-01-onward table rather than an older version)

4. **Notes**
The procurement table lists three separate "approval threshold" pages (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with no obvious warning until you open the legend-revision page — it explicitly says the oldest version says nothing about being superseded, so grabbing the first threshold-looking file found (rather than checking the current/superseded framing and the date) would have silently given a stale, wrong answer. Today's date (2026-09-21) clearly falls after 2026-01-01, so the current table `sec-hard-threshold` was correct, but this is the kind of question where a 2025-dated version of the same question would need the middle table instead — worth being deliberate about every time. Once in the current table, the row for C3/V2/M4 existed exactly as named, so no legend lookups for category/amount/term codes were needed.
