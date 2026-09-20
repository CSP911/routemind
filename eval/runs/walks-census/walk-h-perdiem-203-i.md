## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/expense
    ./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

## Answer

Lodging cap: 235 USD per night.
Receipt threshold: 35 USD — above this, a receipt must be kept (this threshold covers the whole per-diem row, not just lodging).

(For reference, the same row also gives meals at 71 USD/day and incidentals at 14 USD/day, though only the hotel and receipt figures were asked for.)

## Source

- /v1/nodes/hard-perdiem-legend-grade/body — department head → grade G3
- /v1/nodes/hard-perdiem-legend-band/body — Tokyo → band B1
- /v1/nodes/hard-perdiem-legend-stay/body — three weeks → stay S4
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body — the figures (235 USD lodging, 35 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body — confirms this table (in force 2026-01-01 onwards) is the correct version for today's date, 2026-09-20

## Notes

The expense area table flagged up front that the overseas per-diem topic has "the older band-only caps... still here and are superseded," which was the first hint to be careful about versioning. Sure enough, `/v1/nodes/sec-hard-perdiem` turned out to be one of three versions of this same table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend-revision doc was explicit that reaching for the newest is wrong for any question dated before 2026-01-01, and that a 2025-dated question needs the middle version, not either extreme. Today's date (2026-09-20) does fall in the current table's range, so no correction was needed here, but this was clearly a deliberate trap — skipping that revision check would have been an unverified assumption even though it happened to land on the right answer. Worth flagging: the "receipt threshold" figure is a single number attached to the whole per-diem row (lodging+meals+incidentals together), not a hotel-specific figure — the question's phrasing ("above what amount... keep the receipt") maps onto it directly, but it's not itself scoped only to hotel spend, in case that distinction matters downstream.
