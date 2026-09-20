1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence (checked, not needed for final answer)
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(Basis: Austin → origin O3, sixty million won → value W2, a licence → goods K4, per the current supplier due diligence table, in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body
- /v1/nodes/hard-diligence-legend-value/body
- /v1/nodes/hard-diligence-legend-goods/body
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body (answer: Site visit = no, Re-review interval = every 24 months)

4. **Notes**
The procurement area lists a "legend-revision" warning that there are THREE versions of the supplier due diligence rules (current since 2026-01-01, a 2024-07-01–2025-12-31 version `hard-diligence-v2`, and an older `supplier-due-diligence`). I didn't need to open the revision-legend document itself because the row I read stated its own "in force from 2026-01-01" date directly, and today (2026-09-20) falls inside that window — but it would have been easy to grab an answer from the superseded `hard-diligence-v2` table by mistake if I'd picked the wrong sibling node from the procurement region listing, since both "current" and "superseded" versions sit at the same level with similar names. Also nearly went down a dead end reading `supplier-due-diligence/body` and the `sec-supplier-due-diligence` overview, which describe the qualitative onboarding checks (sanctions, code of conduct, disqualification) but never mention site visits or numeric re-review cadence — that detail only exists in the specific origin/value/goods row of the current `sec-hard-diligence` table, which is not obvious from the overview pages alone.
