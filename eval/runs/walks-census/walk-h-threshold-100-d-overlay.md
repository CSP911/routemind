1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V1, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - exactly what this question asks about"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_05d039 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body

2. **Answer**:
Signature: the team lead. Competing quotes: none required. (Delegation limit for this row is 1,016 thousand KRW; expected turnaround is 2 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three approval-threshold table versions is in force for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body (the answer itself)

4. **Notes**:
The procurement region table warns up front that the approval threshold subject has been written three times, with three different tables in force over different date ranges, and that "the oldest says nothing at all about having been replaced" — so grabbing the first threshold-looking table found would have been a live risk of quoting a superseded (pre-2024-07 or 2024-07–2025-12) rule instead of the current one. Checked the legend-revision page first to confirm 2026-09-21 falls under the current table (`sec-hard-threshold`, in force from 2026-01-01), then went straight to the exact C2/V1/M1 row, which existed verbatim — no interpolation or legend lookup for the codes was needed since the question already gave them in the table's own vocabulary.
