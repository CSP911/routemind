1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body

2. Answer
No, a site visit is not required. The file (re-review) interval is every 36 months.

3. Source
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body

4. Notes
This subject has three superseded versions of the due-diligence table (`supplier-due-diligence`,
`hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that
reaching for the newest one is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls
in the current table's range (2026-01-01 onward), so `sec-hard-diligence` was the correct table —
but this was a real branch point, not a formality, since the middle version covers all of 2025 and
would have been the right answer for a question dated last year.

The row document itself ends with a boilerplate-looking "If the figures are exceeded" section about
unapproved excesses and budget-holder sign-off — that reads like it was copy-pasted from an expense
or threshold template and has nothing to do with site visits or re-review intervals. It's easy to
skim that section and think it's relevant to "how often does their file get looked at again"; it
isn't — the actual answer is in the table above it (Site visit / Re-review interval rows).
