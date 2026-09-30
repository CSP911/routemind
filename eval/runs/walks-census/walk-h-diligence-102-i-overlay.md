## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 8,000,000, services (people's time): is a premises visit required, and what is the re-review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table - by origin, value, goods, likely has premises visit and review frequency by tier"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body
./bench/rmcli.py overlay add --id ov_2026-09-20_351f97 --address /v1/nodes/hard-diligence-legend-origin/body --why "confirms Stuttgart = origin O2"
./bench/rmcli.py overlay add --id ov_2026-09-20_351f97 --address /v1/nodes/hard-diligence-legend-value/body --why "confirms eight million won = value W1"
./bench/rmcli.py overlay add --id ov_2026-09-20_351f97 --address /v1/nodes/hard-diligence-legend-goods/body --why "confirms people's time = goods K3"
./bench/rmcli.py overlay add --id ov_2026-09-20_351f97 --address /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body --why "the matching row: site visit no, re-review every 36 months"
./bench/rmcli.py overlay close --id ov_2026-09-20_351f97 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body
```

## Answer

No, a premises (site) visit is not required. The supplier's file is re-reviewed every 36 months.

This is from the current supplier due diligence table (in force from 2026-01-01), row origin O2 / value W1 / goods K3:
- Screening score required: 48
- Financial statements: not required
- Site visit: no
- Re-review interval: every 36 months

## Source

- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body (the matching row, with the answer)

## Notes

The question's wording ("a firm in Stuttgart", "eight million won", "people's time") is lifted almost verbatim from the three legend tables' "What you have" column, so mapping to O2/W1/K3 was unambiguous once the legends were read — no judgment calls or nearest-entry approximations needed.

The one place to be careful: the procurement area table listed three versions of the due diligence table (a legend-revision warning page, a superseded `hard-diligence-v2`, and the current `sec-hard-diligence`), plus an older `supplier-due-diligence` mentioned in the row's footer. It would be easy to grab a superseded row by accident. I used `sec-hard-diligence`, explicitly labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-0[1-01]", and the row I read confirms "In force from 2026-01-01" — which covers today's date (2026-09-21), so this is the right version. Didn't need to open the legend-revision or v2 pages, but noticed them in time to avoid picking the wrong one.
