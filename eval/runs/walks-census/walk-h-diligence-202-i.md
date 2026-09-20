1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 36 months.
(This is under the current supplier due-diligence table, in force since 2026-01-01, for a vendor in Austin (origin O3), eight million won (value W1), buying people's time/services (goods K3): screening score required 64, financial statements not required, site visit no, re-review interval every 36 months.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body (site visit: no; re-review interval: every 36 months)

4. **Notes**
The procurement table lists two overlapping approaches to due diligence: a fixed three-check narrative (`supplier-due-diligence`, `sec-supplier-due-diligence` and children) and a 64-row lookup table (`sec-hard-diligence`) indexed by origin/value/goods codes. The narrative pages never mention site visits or a re-review cadence at all — reading only those would have produced "not found" incorrectly. The actual answer lives only in the coded row table, and you can't reach the right row without first decoding all three legends (origin, value, goods) separately — the row addresses themselves give no hint which combination is right without doing that translation first. It would have been easy to misjudge "eight million won" as trivially small and skip straight to a K1 (office consumables) row instead of K3 (people's time) — the goods axis is about what's being bought, not the amount, and the question's "people's time" phrasing maps directly and unambiguously to the K3 legend entry. Also worth flagging: there are three historical versions of this table (`supplier-due-diligence` → `hard-diligence-v2` → current `sec-hard-diligence`); today's date (2026-09-20) falls inside the current version's effective range (from 2026-01-01), so no need to consult the superseded versions, but a careless reading could have grabbed the wrong-vintage table.
