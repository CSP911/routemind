1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body
```

2. **Answer**
For grade G1, band B3, stay S3 (in force from 2026-01-01, current as of today 2026-09-20):
- Lodging (hotel), per night: **135 USD**
- Receipt threshold: **42 USD** — a receipt must be kept for any spend above this amount

(For context, the same row also lists Meals per day: 76 USD, and Incidentals per day: 15 USD, though these weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem table versions is current for today's date)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body (the figures)

4. **Notes**
The expense region flags up front that overseas per-diem has three superseded/current versions layered on the same subject, and the legend-revision doc is explicit that "the oldest says nothing at all about having been replaced" — so grabbing the first per-diem-looking table found would silently return stale figures. Checked the revision doc against today's date (2026-09-20) before trusting `sec-hard-perdiem` as current. The row address for G1/B3/S3 was printed verbatim by the table listing, so no address construction was needed — worth noting since the instructions warn against guessing addresses even though the naming pattern is very regular and would have been easy to guess correctly.
