1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Supplier in Da Nang, contract value 8,000,000 KRW, category people's time (services/labor): is an on-site premises visit required, and how often is the supplier's file reassessed?" --member /v1/nodes/sec-hard-diligence "current due diligence table in force since 2026-01-01, likely has origin/value/goods thresholds for site visits" --member /v1/nodes/sec-supplier-due-diligence "overview page explaining how the four due-diligence pages fit together" --member /v1/nodes/hard-diligence-legend-revision "warns of three versions of due diligence rules; need to confirm which applies today 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_cbab5d --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body
```

2. **Answer**

No, a site visit to the supplier's premises is not required. The supplier's file is re-reviewed every 36 months.

(For completeness, this row also requires a screening score of 80 and does not require financial statements.)

3. **Source**

- `/v1/nodes/hard-diligence-legend-origin/body` — maps "a supplier in Da Nang" to origin O4
- `/v1/nodes/hard-diligence-legend-value/body` — maps "eight million won" to value W1
- `/v1/nodes/hard-diligence-legend-goods/body` — maps "people's time" to goods K3
- `/v1/nodes/hard-diligence-legend-revision/body` — confirms the current (three-qualifier) table applies for a 2026-09-20 question
- `/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body` — the row itself: Site visit: no; Re-review interval: every 36 months

4. **Notes**

- The due diligence table isn't one document — it's a matrix keyed by three separate legends (origin, value, goods category) plus one specific row for the combination. Each qualifier had to be translated separately: "Da Nang" → O4, "eight million won" → W1, "people's time" → K3. Getting any one of these wrong (e.g. treating "people's time" as a services/labor guess without checking the legend) would silently point at the wrong row with no error.
- There's a real trap here: three superseded/current versions of the due diligence rules exist (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that "reaching for the newest is wrong for anything before 2026-01-01" — and just as pointedly, the oldest version "says nothing at all about having been replaced." Today's date (2026-09-20/21) is safely inside the current table's validity window (2026-01-01 onward), so this wasn't actually a close call this time, but it's the kind of question where skipping the revision-legend check would go unnoticed until it was wrong.
- When closing the overlay, the addresses I actually read (the three legends and the final row) had never been added as named members of the overlay — only their parent table `sec-hard-diligence` had been. The close command still accepted them but reported them as "reached" rather than a clean "used," noting they were reached from somewhere the overlay never named. Worth flagging: the overlay's working set tracks the top-level table/file members you declare, not every leaf you eventually drill into under them, so "add member" bookkeeping and "actually read" bookkeeping diverge once a table row explodes into many sub-addresses.
