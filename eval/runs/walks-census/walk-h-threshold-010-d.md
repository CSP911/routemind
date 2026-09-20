1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

2. **Answer**
Signature: the team lead.
Other prices first: yes — two competing quotes are required.
(Delegation limit for this row: 5004 thousand KRW; working days to expect: 5.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirms which version is current for today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body (the answer)

4. **Notes**
The procurement region lists both a superseded `hard-threshold-v2` file and a current `sec-hard-threshold` table, with no obvious cue at the region level about which applies to a 2026 date. The `hard-threshold-legend-revision` page exists specifically to resolve this — it states the current table (`sec-hard-threshold`, in force 2026-01-01 onward) is the right one for today's date, and warns that the oldest version says nothing about being superseded, so guessing without checking would have been risky for older dates (though not for this one, since 2026-09-20 clearly falls in the current table's range). Once inside `sec-hard-threshold`, the row addresses are literal and predictable (category-c1-amount-v2-term-m1), so no legend lookup for category/amount/term codes was needed since the question already gave the codes directly.
