1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 700,000,000, staffing/people's time: site visit required for diligence? review frequency for file?" --member /v1/regions/procurement "amount+category approval/diligence thresholds likely here"
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_98b665 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body

2. Answer

Yes, a site visit is required. The file is re-reviewed every 6 months. (This is the row for origin O2 / Stuttgart, value W4 / seven hundred million won, goods K3 / people's time — current supplier due-diligence table, in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. Source

/v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
/v1/nodes/hard-diligence-legend-value/body (seven hundred million won → W4)
/v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)

4. Notes

All three legend lookups were exact matches (Stuttgart, seven hundred million won, and people's time each appear verbatim), so no "nearest entry" judgment call was needed here — unusual good luck, since the legends explicitly warn you may have to approximate.

The main hazard was version confusion: the procurement overlay surfaced three separate diligence tables (`supplier-due-diligence`, `hard-diligence-v2`, and the current `sec-hard-diligence`), plus a `hard-diligence-legend-revision` warning page about exactly this trap. I did not open the superseded versions, but I did check the current table's own header, which states it's "in force from 2026-01-01" — since today is 2026-09-20, that's the correct table and I didn't need to consult the revision-legend page separately. Worth flagging that it would be easy to grab a row from `hard-diligence-v2` by mistake since it has the same row-naming shape.

The `/v1/regions/procurement` overlay member also surfaced a `sec-supplier-due-diligence` "where to start" overview describing "four pages" of due diligence, one being "the ongoing side of the same checks, re-run rather than one-off" — I initially expected this to be the source for the re-review interval, but that overview's entries list didn't clearly correspond to a distinctly-named periodic-review page, and it turned out to be irrelevant: the re-review interval was actually inside the row body of the current origin/value/goods table, not that overview's four sub-pages. I nearly went down that path before checking the row body directly.
