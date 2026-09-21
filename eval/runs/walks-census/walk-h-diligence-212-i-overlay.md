1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A vendor in austin, sixty million won, people's time: do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "vendor site visit requirement and periodic re-review cadence are procurement/vendor-management topics"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_e43c10 --address /v1/nodes/hard-diligence-legend-origin/body --why "need to map austin (US city) to an origin code O1-O4"
./bench/rmcli.py overlay add --id ov_2026-09-20_e43c10 --address /v1/nodes/hard-diligence-legend-value/body --why "need to map sixty million won to a value band W1-W4"
./bench/rmcli.py overlay add --id ov_2026-09-20_e43c10 --address /v1/nodes/hard-diligence-legend-goods/body --why "need to map people's time (labor/services) to a goods code K1-K4"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py overlay add --id ov_2026-09-20_e43c10 --address /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body --why "exact match: origin O3 (Austin), value W2 (60M won), goods K3 (people's time)"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e43c10 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body

2. **Answer**: No site visit required. Re-review interval is every 24 months. (Also for reference: screening score required 68, financial statements from last year.) This is from the current supplier due diligence table, in force from 2026-01-01, which covers today's date (2026-09-20/21).

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body

4. **Notes**: Each of the three qualifiers ("austin", "sixty million won", "people's time") turned out to be an exact, literal entry in its respective legend table (O3, W2, K3 respectively) — no fuzzy-matching or "nearest entry" fallback was needed, which was a relief since the legends explicitly warn you to use judgment when a value isn't listed. The main risk here was versioning: the sec-hard-diligence table carries a big "THE CURRENT... in force from 2026-01-01" banner, and there's a legend-revision warning about three versions (a superseded hard-diligence-v2 for 2024-07-01 to 2025-12-31, and an older supplier-due-diligence before that). Since today is 2026-09-20/21, the current table is the right one and I didn't need to open the older versions or the revision-legend at all — I only kept them in the working set out of caution, then didn't cite them since they didn't contribute to the answer. It would have been easy to grab the wrong row by shape (e.g. confusing K2 "something made to our spec" with K3 "people's time" — both sound like they could cover contracted labor) if I hadn't read the goods legend's literal wording carefully.
