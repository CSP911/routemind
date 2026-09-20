1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body

2. **Answer**
For 2,000,000 KRW net of VAT (band 500,000–3,000,000 KRW): Division head, delegated. 2 competing quotes required.

3. **Source**
/v1/nodes/threshold-table/body (the answer)
/v1/nodes/hard-threshold-legend-revision/body (established the three-version history and the 2024-07-01 cutover)
/v1/nodes/hard-threshold-v2/body (confirmed the pre-2024-07-01 predecessor is `threshold-table` and that v2 only starts 2024-07-01)

4. **Notes**
29 June 2024 is exactly two days before the first change (2024-07-01), so it falls just outside the "second version" (`hard-threshold-v2`, in force 2024-07-01 to 2025-12-31) and just inside the oldest version's coverage. The trap here was `hard-threshold-v2`: it's the SUPERSEDED page that surfaces most prominently under /v1/regions/procurement and reads as "the historical one," but reading its own text shows it starts on 2024-07-01, one day after the question's date — it does not cover 29 June. The actual oldest version's document (`threshold-table`) isn't listed anywhere under /v1/regions/procurement's first-level table or under the current `sec-hard-threshold` table; it only turned up by going one level deeper into /v1/nodes/purchase-request → /v1/nodes/approval-threshold, which is a differently-named table ("Approval thresholds by amount") that doesn't obviously read as "the old version of the threshold table" from its listing description alone. Without the legend-revision page's explicit date ranges, it would have been easy to grab `hard-threshold-v2` and misreport it as covering this date.
