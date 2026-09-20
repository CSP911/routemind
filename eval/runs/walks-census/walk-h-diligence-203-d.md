1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body

2. **Answer**:
No site visit is required. The file is re-reviewed every 36 months. (Also on this row: screening score required is 65, financial statements not required.)

3. **Source**:
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k4/body

4. **Notes**:
The procurement region table flagged that supplier due diligence has three versions (`hard-diligence-legend-revision` warns of this), so there was a real risk of reading the superseded `hard-diligence-v2` table instead of the current one. The `sec-hard-diligence` table states plainly it is "in force from 2026-01-01" and replaces the older rules, and today's date (2026-09-20) falls inside that window, so the current table was the right pick — this was confirmed again in the row document's own footer ("In force from 2026-01-01"). Row addresses are laid out predictably (origin-o3-value-w1-goods-k4), so once the current table was open, the exact row could be read directly without needing the legend pages that translate a person's words into O/W/K codes — the question already gave the codes.
One oddity worth flagging: the row document ends with a generic "If the figures are exceeded" section about unapproved excess amounts and budget-holder approval. That reads like boilerplate carried over from the threshold table rather than something specific to site visits or re-review intervals, and it does not bear on this question — I ignored it, but it could mislead someone skimming for "how often" language.
