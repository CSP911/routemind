1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 60,000,000 contract for people's time (services): is a premises visit required, and how often is the file reviewed again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due diligence pages fit together" --member /v1/nodes/hard-diligence-legend-revision "confirms which version is in force for today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1fc56e --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 24 months.
(Row: origin O2 / value W2 / goods K3 — screening score required 52, financial statements from last year, site visit: no, re-review interval: every 24 months.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body

4. **Notes**
The three qualifiers all happened to be exact matches in their legends — Stuttgart = O2, "sixty million won" = W2, "people's time" = K3 — so there was no "nearest entry" judgment call to make, which is the part these legends warn is easy to get wrong.
The one real trap was the version/date check: supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the revision-legend page explicitly warns the oldest version says nothing about being replaced, so grabbing the first hit without checking the legend would silently give a stale answer. Today (2026-09-21) is safely inside the current table's 2026-01-01-onward window, so `sec-hard-diligence` was correct, but this is clearly the row the walk wants you to trip on.
Minor oddity: closing the overlay reported all five addresses as "reached ... from somewhere the overlay never named" rather than as originally-listed members. That's because I only passed the three container/legend-overview addresses as `--member` at creation time and then drilled into leaf rows the tables printed — expected given how the tool works, but worth flagging since the close output phrases it like a discrepancy.
