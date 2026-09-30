1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Junior analyst, Tokyo, one night hotel: nightly cap and receipt threshold?" --member /v1/regions/expense "trip allowance and receipt rules live under expense"
./bench/rmcli.py overlay remove --id ov_2026-09-21_d56867 --address <various irrelevant rows under /v1/regions/expense>  (all failed: HTTP 404, address not in overlay)
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d56867 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body

(Read earlier, before the removal attempts, but listed here in the order actually used: /v1/nodes/hard-perdiem-legend-revision/body)

2. **Answer**
Lodging cap: 95 USD per night. Receipt threshold: 18 USD — spend above that amount needs a receipt kept as evidence. (For reference, this row also gives meals at 38 USD/day and incidentals at 7 USD/day, current from 2026-01-01.)

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (established that the 2026-01-01-onward table is the one that applies to today's date, 2026-09-21)
/v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
/v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
/v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body (the figures: 95 USD lodging, 18 USD receipt threshold)

4. **Notes**
The overlay's `remove` calls all failed with HTTP 404 ("address is not in this overlay"), even for addresses printed verbatim from the overlay listing itself (e.g. `/v1/nodes/corp-card`). I didn't chase this down — the working set doesn't need to be pruned for the answer to be found, so I moved on rather than burn turns diagnosing the CLI's overlay-membership tracking.

The real trap here is the three-version warning on `hard-perdiem-legend-revision`: this domain has been written three times (`overseas-rates`, then `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, then `sec-hard-perdiem` for 2026-01-01 onward), and the document says outright that "reaching for the newest is wrong for anything before 2026-01-01" and that the oldest version never says it was replaced. Since today is 2026-09-21, the current table is correct here, but a question dated any time in 2025 would need `hard-perdiem-v2` instead — this is easy to get wrong if you skip the revision-warning doc and just grab whatever table the region listing surfaces first.

The per-diem table itself is a 3-axis lookup (grade × country band × stay length) with no shortcuts — each axis has its own legend document, and none of the axis values are guessable from the question's plain-English wording ("junior analyst," "Tokyo," "one night") without reading the corresponding legend.
