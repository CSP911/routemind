## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/attendance
    ./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-accrual
    ./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
    ./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
    ./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
    ./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body

## Answer

Accrues 1.30 days of leave per month, with a carry-over limit of 14 days — that is the most you can still be holding in January.

## Source

- /v1/nodes/hard-accrual-legend-revision/body (established current table applies for a 2026-09-20 question)
- /v1/nodes/hard-accrual-legend-type/body (three days a week → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (Busan branch → site L2)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body (final figures: 1.30 days/month, 14-day carry-over limit)

## Notes

The attendance area's warning about three accrual versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) was the one place this walk could easily go wrong — a question dated in 2025 would need the superseded `hard-accrual-v2` table instead, and the oldest version doesn't even say it was replaced. Today's date (2026-09-20) put the answer squarely in the current `sec-hard-accrual` table, so no ambiguity there. The three-qualifier lookup (type/tenure/site) required all three legend files before the row address could be assembled, and each legend was explicit that its right-hand column is the only place the mapping exists — worth noting only "three days a week" mapped cleanly to E3, "nine years" mapped exactly to T4, and "Busan branch" mapped exactly to L2, so no nearest-entry judgment calls were needed. The "how much can I still be holding in January" phrasing isn't answered by a separate January-specific figure; it's the row's carry-over limit (14 days), which is the general cap rather than something month-specific — that mapping from the question's wording to the table's field name was the only real interpretive step.
