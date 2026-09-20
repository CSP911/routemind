## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 6 months.

(Full row for this combination: screening score required 42; financial statements — last three years, audited; site visit — yes; re-review interval — every 6 months. This is the current table, in force since 2026-01-01, and today is 2026-09-20, so it applies.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k1/body (the answer)

## Notes

- The `/v1/regions/procurement` table lists several diligence-adjacent pages (`sec-supplier-due-diligence`, `sec-hard-diligence`, older superseded pages `hard-diligence-v2`, `supplier-due-diligence`, and a legend-revision warning page). It would be easy to open the wrong one — the row data itself lives only under `sec-hard-diligence`, and the "where to start" overview page (`sec-supplier-due-diligence`) has none of the actual figures, just explains the four upstream checks (sanctions, code of conduct, disqualification triggers) that are a separate gate from this per-row table.
- Almost went down the wrong branch: `sec-supplier-due-diligence` looked at first glance like it might hold the answer (it's the top hit under procurement for "due diligence"), but it's explicitly about one-time onboarding checks, not the value/origin/goods-banded table with site-visit and re-review terms. The real answer is in a completely different node (`sec-hard-diligence`) reached only from the procurement table listing, not from within `sec-supplier-due-diligence`.
- The three legends (origin, value, goods) each say "take the nearest entry above it" if the exact figure isn't listed — not needed here since all three inputs (Daejeon, 700M won, office consumables) matched an exact row, but worth noting the fallback rule exists.
- Confirmed the row is current (in force since 2026-01-01, today 2026-09-20) rather than the superseded `hard-diligence-v2` version, which uses the same O/W/K coding but different dates — did not need to open that page since only the current row matters, but its presence in the listing is a trap if you grab the first "diligence" result without checking effective dates.
