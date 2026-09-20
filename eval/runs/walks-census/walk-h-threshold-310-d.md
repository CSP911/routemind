1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body

2. **Answer**
Signature required: the team lead.
Other prices first: yes — two competing quotes are required.
(Delegation limit for this row: 5,052 thousand KRW; working days to expect: 5.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body (the answer itself)

4. **Notes**
The procurement area warns up front that the approval-threshold subject has three superseded versions
covering different date ranges (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards), and
explicitly calls out that the oldest version says nothing about being replaced — so grabbing the first
match by name would have silently returned a stale answer. Checked the legend/revision page before
trusting `sec-hard-threshold`, confirmed today's date (2026-09-20) falls in the "2026-01-01 onwards"
current range, and only then used that table. The row address itself directly encoded the three
qualifiers (category/amount/term) from the question, so no separate legend lookup for C4/V2/M1 codes
was needed — the row existed exactly as named.
