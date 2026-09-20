1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body
```

2. **Answer**
For grade G1, band B1, stay S3 (current table, in force from 2026-01-01):
- Hotel/lodging cap: **103 USD per night**
- Receipt required above: **24 USD** (the receipt threshold)

3. **Source**
- /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body

4. **Notes**
The expense area's table page flags upfront that overseas per-diem has three versions in force at different times (`sec-hard-perdiem` current since 2026-01-01, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`), with a warning file `hard-perdiem-legend-revision`. It would be easy to grab a stale rate from one of the superseded nodes if not careful about dates. Since today is 2026-09-20, `sec-hard-perdiem` is the correct, current table, and its own row document restates that it's in force from 2026-01-01, which confirmed the choice. The row document itself gave both the lodging cap and the receipt threshold directly, with no need to cross-reference a separate evidence/receipts table.
