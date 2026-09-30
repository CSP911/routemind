1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 700 million won, holds a licence: is an on-site visit required, and what is the periodic review frequency for their file?" --member /v1/regions/procurement "vendor onboarding/site-visit and periodic review requirements are likely procurement policy"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2155a2 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The vendor's file must be re-reviewed every 6 months. (For reference, this row also requires a screening score of 77 and audited financial statements for the last three years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-legend-revision/body (confirms the current table, in force 2026-01-01 onwards, applies to a question dated 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body (the answer: Site visit = yes, Re-review interval = every 6 months)

4. **Notes**
- The "seven hundred million won" figure landed exactly on a legend entry (W4, the top band), so there was no ambiguity or nearest-value judgment call needed there — unlike a figure that fell between bands.
- The near-miss was the revision warning: there are three versions of the supplier due diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the warning explicitly calls out that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-diligence`) was correct, but I deliberately checked the revision legend before reading the row rather than assuming — this is exactly the kind of question where grabbing the first/newest-looking table without checking dates would silently give the right answer today but the wrong habit for other dates.
- "A licence" mapping to goods K4 was a direct, exact match in the legend text, not an inference — worth noting since the phrase could plausibly have been read as "software" or "something made to our spec," but the legend explicitly lists "a licence" verbatim.
