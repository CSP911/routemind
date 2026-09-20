## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k3/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Row: origin O3 = Austin, value W3 = three hundred million won, goods K3 = people's time. Screening score required: 72. Financial statements: last two years.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body
- /v1/nodes/hard-diligence-legend-value/body
- /v1/nodes/hard-diligence-legend-goods/body
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k3/body
- /v1/nodes/hard-diligence-legend-revision/body (confirms current table applies for a 2026-09-20 question)

## Notes

- The `/v1/regions/procurement` table surfaces two "overview" style pages (`sec-supplier-due-diligence` and `supplier-due-diligence`) that read as if they'd answer this directly, but they only describe the onboarding sanctions/code-of-conduct/disqualification screen — a one-time gate, not the site-visit/re-review question. Reading `supplier-due-diligence/body` in full was a detour; it has nothing about site visits or review cadence. The real answer lives in a completely different sub-table (`sec-hard-diligence`), reached from the same procurement listing but easy to skip past because its description ("by origin, value, goods") doesn't obviously scream "site visit."
- `sec-hard-diligence` is a 64-row matrix (4 origins × 4 value bands × 4 goods types) with no way to jump straight to a row — you must resolve all three legends first. Getting any one wrong (e.g. picking the wrong value band) silently lands on a plausible-looking but wrong row, since all 64 row pages have near-identical titles/descriptions.
- The value legend had an exact match ("three hundred million won" = W3 verbatim), which was reassuring — no need to round to a nearest band as the legend's fallback instructions would otherwise require.
- The biggest trap was version drift: there are three historical versions of this due-diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version says nothing about being superseded. Today's date (2026-09-20) falls cleanly under the current table's force period (2026-01-01 onwards), so `sec-hard-diligence` was correct here — but this table makes it easy to grab the wrong version if the question is ever backdated.
