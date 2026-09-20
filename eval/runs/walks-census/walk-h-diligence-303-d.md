1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body

2. Answer

No site visit is required. The file is re-reviewed every 36 months. (Screening score required: 81; financial statements not required — for context, not asked.)

3. Source

/v1/nodes/hard-diligence-legend-revision/body (confirms which version applies for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body (the row with the answer)

4. Notes

- The procurement region lists two near-identical "sec-hard-diligence"-prefixed and unprefixed sets of pages (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), covering three different date ranges of the same subject. The legend-revision page is explicit that reaching for the newest table without checking the date is wrong for any question dated before 2026-01-01 — today (2026-09-20) is safely inside the current table's range, but this is the kind of table where guessing instead of checking the date would silently give a stale answer.
- I first opened `sec-supplier-due-diligence` ("where to start") thinking it was the on-ramp to the O/W/K row table, but it turned out to be a wholly separate four-page subject (sanctions screening, code of conduct, disqualification triggers, ongoing re-checks) with no origin/value/goods indexing at all. It was a dead end for this question — the actual indexed table lives directly under `/v1/regions/procurement` as `sec-hard-diligence`, a sibling entry, not a child of the "where to start" page. Easy to conflate the two since both are titled "Supplier due diligence."
- The row document's closing section ("If the figures are exceeded," about unapproved excess and budget-holder claims) reads like boilerplate carried over from an expense/spend-limit template — it doesn't fit a due-diligence row (site visit / re-review cadence) at all. I ignored it as not applicable to the question, but it's worth flagging as apparently mismatched content sitting in this document.
