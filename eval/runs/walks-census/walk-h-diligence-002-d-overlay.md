1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W1, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods, likely holds the site-visit and review-frequency requirement" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is current for today's date" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify terms or scope"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_18deaf --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(For reference, the same row also sets: screening score required = 32, financial statements not required.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms today's date, 2026-09-20/21, falls under the current table, in force from 2026-01-01)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k3/body (the actual figures)

4. **Notes**
- There are three superseded generations of the supplier-due-diligence subject (`supplier-due-diligence`, then `hard-diligence-v2`, then the current `sec-hard-diligence`), and the legend-revision page is explicit that reaching for the newest without checking the date is wrong for anything dated before 2026-01-01. Today's date is in the current window, so this was a non-issue here, but it would have been easy to skip that check and grab the wrong generation for a differently-dated question.
- Opening the `sec-hard-diligence` table expanded into 64 individual per-row files (one for every origin×value×goods combination), not a single table with columns. The row for O1/W1/K3 was named directly and unambiguously, so no lookup against the origin/value/goods legends was needed — the question already gave qualifiers in the table's own vocabulary.
- The row's closing section ("If the figures are exceeded," talking about excesses, budget holders, and unapproved amounts) reads like boilerplate carried over from an expense/threshold-style template — it doesn't obviously apply to a site-visit/re-review decision, and I did not use it in the answer. Flagging it since it could mislead a reader into thinking there's an appeals process for the site-visit or interval figures.
- The overlay's close output reported the row as "reached" rather than a named "member" — I had only added the parent table `sec-hard-diligence` as a member, and the specific per-row address surfaced only once that table was opened, so the tool didn't count it as something I'd pre-declared. Worth knowing this distinction exists when reading overlay close output.
