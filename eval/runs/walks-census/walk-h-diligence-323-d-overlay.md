1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W3, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "due diligence / site visit / review frequency for vendors sounds procurement-related"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_aed09d --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on this row, for context: screening score required is 89, financial statements for the last two years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is in force for today's date, 2026-09-20/21)
- /v1/nodes/sec-hard-diligence (the current table, in force from 2026-01-01, listing all origin/value/goods rows)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k4/body (the row itself — Site visit: yes, Re-review interval: every 12 months)

4. **Notes**
This subject has three versions covering different date ranges, and a warning page (`hard-diligence-legend-revision`) says the oldest version says nothing about having been replaced, so reaching for the newest without checking is a trap for older-dated questions. For today's date (2026-09-20/21) the current table `sec-hard-diligence` (in force from 2026-01-01) is correct, so no real ambiguity here — but this is exactly the kind of question where grabbing the first due-diligence row found (e.g. an O4/W3/K4 row from the superseded `hard-diligence-v2` table, which is indexed by only two qualifiers) would have silently given a stale answer. The question's O4/W3/K4 codes matched the row title directly, so the origin/value/goods legends were not needed to translate plain-language descriptions into codes.
