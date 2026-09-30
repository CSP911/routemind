1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W1, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/premises-visit and file review frequency sound like vendor risk categorization under procurement thresholds"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_87c2d6 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body

2. **Answer**
No, a site visit is not required. The file (re-review) is looked at again every 36 months.
(For reference, this row also requires a screening score of 81, and financial statements are not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which of three due-diligence table versions is current for today's date, 2026-09-20)
- /v1/nodes/sec-hard-diligence (the current table, listing the row for origin O4 / value W1 / goods K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body (the row itself, with the answer)

4. **Notes**
- Under `/v1/regions/procurement`, three near-identical "supplier due diligence" documents exist for different date ranges (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), with a legend-revision page warning that the oldest one gives no indication it was ever superseded. It would be easy to grab the wrong one by name-matching alone; checking the revision legend against today's date (2026-09-20) before reading a row was necessary, not optional.
- The row body ends with a boilerplate "If the figures are exceeded" section about excess amounts and budget-holder approval — that reads like expense/threshold template text, not due-diligence content, and doesn't actually apply to a site-visit/re-review question. Ignored it as apparently mismatched boilerplate rather than part of the answer.
- The overlay's `close` command reported the three addresses I read as "reached" rather than as named members, because I had only added the parent `/v1/regions/procurement` row as a member and then drilled into child tables/files directly rather than adding each leaf address to the overlay first. Didn't affect the answer, but worth noting for how the tool distinguishes "member of the working set" from "address actually read."
