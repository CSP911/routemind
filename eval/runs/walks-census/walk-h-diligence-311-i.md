1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body
```

2. **Answer**

No site visit is required. The supplier's file is re-reviewed every 24 months.
(For completeness: screening score required is 83, financial statements needed are "last year".)

3. **Source**

- /v1/nodes/hard-diligence-legend-revision/body (confirms which of three diligence versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body (the answer)

4. **Notes**

The trickiest part was not the lookup itself — all three qualifiers (Da Nang, 60M won, made-to-spec) had exact, unambiguous matches in their legends, no "nearest entry above it" fallback needed. The real hazard was version selection: `/v1/regions/procurement` lists three separate supplier due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious flag on the oldest one saying it's superseded — the legend-revision page explicitly warns that reaching for the newest by default is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about having been replaced. Since today's date is 2026-09-20, the current table (`sec-hard-diligence`) is correct here, but this is the kind of question where skipping the revision-legend check would silently produce a right-looking answer from the wrong era for a differently-dated question. Worth flagging: nothing in the row itself repeats the qualifiers in plain English (Da Nang/60M won/made-to-spec) — it only speaks in O4/W2/K2 codes, so cross-checking the three legends was mandatory rather than a shortcut.
