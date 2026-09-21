1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, KRW 60,000,000, custom-to-spec item: is a site visit required, and how often is the vendor file re-reviewed?" --member /v1/regions/procurement "procurement table governs vendor site visits, approval thresholds, and vendor file review cadence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f7439b --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body
```

2. **Answer**
No site visit is required. The vendor's file is re-reviewed every 24 months.
(Full row: screening score required 67, financial statements from last year.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed the current table is the correct version for a 2026 date)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
- /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body (the answer: site visit no, re-review every 24 months)

4. **Notes**
The domain has three superseded versions of this supplier due diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) put this cleanly inside the current table's effective range (2026-01-01 onward), so there was no ambiguity here — but it would have been easy to skip that check entirely and just grab whichever table looked newest, which the revision page specifically flags as the wrong instinct for older dates. All three qualifiers in the question (Austin, sixty million won, "something made to our spec") mapped onto the legends with exact, unambiguous wording matches — no nearest-entry judgment calls were needed. The overlay's close command reported the used addresses as "reached ... from somewhere the overlay never named" since I read them directly rather than adding them as overlay members first; the answer is unaffected but worth flagging as a minor mechanical mismatch between how I worked and how the tool expected the working set to be built.
