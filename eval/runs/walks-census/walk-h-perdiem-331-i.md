## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/expense
    ./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

## Answer

Lodging cap: 339 USD per night. Receipt required above 60 USD.

(For reference, this row also lists meals at 112 USD/day and incidentals at 23 USD/day, though only the hotel and receipt figures were asked for.)

## Source

- /v1/nodes/hard-perdiem-legend-grade/body — mapped "managing director" to grade G4
- /v1/nodes/hard-perdiem-legend-band/body — mapped "Dhaka" to band B4
- /v1/nodes/hard-perdiem-legend-stay/body — mapped "four nights" to stay S2
- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body — the figures
- /v1/nodes/hard-perdiem-legend-revision/body — confirmed today's date (2026-09-20) falls under the current table (`sec-hard-perdiem`, in force from 2026-01-01), not one of the two superseded versions

## Notes

The expense area table flags up front that overseas per-diem has three versions with different dates in force, and that "reaching for the newest is wrong for anything before 2026-01-01." Today's date (2026-09-20) is safely inside the current table's window, so this wasn't actually ambiguous — but it was worth checking explicitly rather than assuming, since the same walk with an older date would need `hard-perdiem-v2` or `overseas-rates` instead, and both of those older files exist and would answer silently without complaint. The row's "WHY" column text is truncated in the table listing ("...the daily meal allowance and the re…"), so the receipt threshold isn't visible until you actually open the row body — easy to miss if you stop at the table listing instead of reading the file.
