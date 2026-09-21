1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Austin vendor, KRW 700M, office consumables only: site visit required? review/re-diligence frequency?" --member /v1/regions/procurement "vendor diligence, site visits, and re-review cadence are procurement policy"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_21edab --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months. (This is the O3/W4/K1 row: Austin origin, KRW 700M value band, office-consumables goods category; screening score required is 74 and audited financial statements for the last three years are also required, though those weren't asked.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body (the answer: site visit yes, re-review every 6 months)

4. **Notes**
- The procurement table listed two due-diligence tables in the working set: the current `sec-hard-diligence` (in force from 2026-01-01) and a superseded `hard-diligence-v2` (2024-07-01 to 2025-12-31), plus a `hard-diligence-legend-revision` warning that three versions exist. Today's date (2026-09-20/21) falls under the current table, so I used `sec-hard-diligence` and did not need to open the revision-legend or v2 pages — but it would be easy to grab the wrong version's row here if you didn't check the in-force dates first.
- The three legends (origin, value, goods) are the only place the English-language mapping to row codes is written; the row documents themselves only speak in codes (O3/W4/K1). Skipping any one of the three legends risks guessing a code wrong, since e.g. "Austin" isn't self-evidently O3 without the table.
- `overlay close` reported all four used addresses as "reached" rather than exact matches to overlay members — the legends and the specific row file were never added as explicit overlay members (I only seeded the overlay with the parent `/v1/regions/procurement`), so this is expected behavior, not an error.
