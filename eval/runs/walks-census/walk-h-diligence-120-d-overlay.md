1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W3, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/site-visit and review-frequency rules by origin/value/goods sound like vendor risk criteria under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f5deb6 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months. (Also on this row, for context: screening score required 54, financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three due-diligence table versions applies today)
- /v1/nodes/sec-hard-diligence (current table, in force 2026-01-01 onward; located the exact origin/value/goods row)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body (the row itself — source of the answer)

4. **Notes**
The supplier due diligence subject has three separate versions of the same table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that the oldest version never mentions being superseded, so grabbing the first hit under that name would silently give a wrong-era answer. Today's date (2026-09-20/21) is after the 2026-01-01 cutover, so the current table `sec-hard-diligence` is the right one — but this is exactly the kind of question where reaching for "current" out of habit could have been right by luck rather than by checking. No ambiguity once the row was located: the origin/value/goods triple maps to a single row with unambiguous "Site visit: yes" and "Re-review interval: every 12 months" fields.
