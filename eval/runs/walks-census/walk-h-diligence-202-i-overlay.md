1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 8 million won, people's time (services): site visit required? review recurrence?" --member /v1/regions/procurement "vendor due diligence, site visits, and periodic review cadence are procurement policy topics"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_6b558d --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body

2. **Answer**
No site visit required. Re-review interval is every 36 months.
(Full row also lists: screening score required = 64, financial statements not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body — Austin → origin O3
- /v1/nodes/hard-diligence-legend-value/body — eight million won → value W1
- /v1/nodes/hard-diligence-legend-goods/body — people's time → goods K3
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body — the answer row (site visit, re-review interval)

4. **Notes**
The procurement table surfaced two due-diligence tracks and it would have been easy to answer from the wrong one: `supplier-due-diligence`/`sec-supplier-due-diligence` cover the one-time sanctions/ownership/code-of-conduct gate (no amounts, no site visits, no recurrence), while the actual amount/origin/goods-banded table with site-visit and re-review data lives at `sec-hard-diligence`. The `hard-diligence-legend-revision` row warned there are three versions of this table (current, `hard-diligence-v2` for 2024-07-01 to 2025-12-31, and `supplier-due-diligence` before that); I didn't need to open that file directly since `sec-hard-diligence` itself states it's "in force from 2026-01-01" and today (2026-09-20/21) falls inside that window, and the answer row repeats the same effective date. Also worth flagging: the question's own framing ("do we have to go and see their premises") maps to a binary "Site visit: no/yes" field rather than a threshold, so there's no approximation involved — Austin/8M won/people's-time landed on an exact row (O3/W1/K3), no nearest-band judgment call needed.
