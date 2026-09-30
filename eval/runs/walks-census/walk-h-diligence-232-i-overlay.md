1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 700M KRW, personal data processing: is an on-site visit required, and how often is the vendor re-reviewed?" --member /v1/regions/procurement "vendor due diligence, site visits, and re-review cadence are procurement policy"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_858c9a --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The vendor's file is re-reviewed every 6 months.

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed the 2026-01-01-onward table is the correct version for today's date)
/v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
/v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
/v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k3/body (Site visit: yes; Re-review interval: every 6 months)

4. **Notes**
The question gives no date, so it's easy to just grab `sec-hard-diligence` because it's flagged "CURRENT" and move on — but the region's table row for it explicitly warns that this subject has three versions and reaching for the newest is only correct from 2026-01-01 onward, so I checked the revision-legend page first rather than assuming. Today (2026-09-20) falls after that date, so the current table was in fact the right pick, but the walk would have been wrong for a 2025-dated question. The other snag is that the row address itself isn't guessable — it's built from three separate legend lookups (origin, value, goods), each phrased in plain language ("a vendor in Austin", "seven hundred million won", "people's time") that has to be translated to a code (O3, W4, K3) before the row address exists; nothing about "700 million won" or "Austin" appears literally in the row filenames, so skipping any one legend would have left me unable to construct the address at all.
