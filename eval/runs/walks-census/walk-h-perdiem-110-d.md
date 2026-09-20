1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body
```

2. **Answer**
For grade G2, band B2, stay S1 (in force since 2026-01-01, current as of today 2026-09-20):
- Lodging cap: 175 USD per night
- Receipt threshold: 31 USD — a receipt must be kept for any spend above this amount

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which version applies for today's date)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body (the figures)

4. **Notes**
The expense region flags up front that overseas per-diem has three superseded/current versions indexed by date, and that the oldest version says nothing about being replaced — an easy trap if you grab the first per-diem table you see without checking dates. I read the revision-legend page before trusting `sec-hard-perdiem`, confirmed 2026-01-01 onward is current and covers today's date, and only then read the row. The row address for G2/B2/S1 existed exactly as printed in the table listing (`hard-perdiem-row-grade-g2-band-b2-stay-s1`), so no construction or guessing was needed. The row itself answers both parts of the question in one document (lodging line and receipt-threshold line), so no merging across sources was required.
