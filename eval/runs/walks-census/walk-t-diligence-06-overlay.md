1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In August 2025, what screening was required for an origin O2 supplier at contract value W2? Answer under the version of supplier due diligence that was in force on that date." --member /v1/regions/procurement "supplier due diligence / screening thresholds by origin and contract value live under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py overlay close --id ov_2026-09-20_0534c6 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-v2/body

2. **Answer**: 35 (the screening requirement code for origin O2 at contract value W2, under the second version of supplier due diligence — in force 2024-07-01 to 2025-12-31, which covers August 2025).

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established that August 2025 falls under the second/middle version, not the current or oldest one)
- /v1/nodes/hard-diligence-v2/body (the table itself: origin O2 × value W2 = 35)

4. **Notes**: Supplier due diligence has three versions on file, and the legend page is explicit that reaching for the newest (`sec-hard-diligence`, effective 2026-01-01) or oldest (`supplier-due-diligence`, no origin/value split) would both be wrong for an August 2025 date — the middle version (`hard-diligence-v2`, 2024-07-01 to 2025-12-31) is the only correct one. This is exactly the trap the legend page calls out: the oldest version doesn't mention being superseded, so without checking the legend first it would look self-sufficient. I confirmed the date window before reading the table itself to avoid pulling the wrong figure. I briefly opened `sec-supplier-due-diligence` to check whether the numeric codes (30–45) decode into named screening types elsewhere, but that table only indexes the four due-diligence sub-pages (disqualification triggers, sanctions/ownership checks, code of conduct, general overview) with no numeric legend, so I treated the table's own value (35) as the answer.
