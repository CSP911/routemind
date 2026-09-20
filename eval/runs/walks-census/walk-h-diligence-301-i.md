## Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body

## Answer

No, a site visit is not required. The file is re-reviewed every 36 months. (Also for reference: screening score required is 79, and financial statements are not required.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is current for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body (Site visit: no; Re-review interval: every 36 months)

## Notes

- The procurement table surfaces three separate "supplier due diligence" documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious signal at that level about which is current. The oldest one doesn't even say it was superseded. Only the dedicated legend-revision page states the effective date ranges — skipping it and grabbing the first "supplier due diligence" hit, or assuming "current" always means "right for today," would have been the wrong move for a question dated earlier than 2026-01-01. For this question (2026-09-20) the current table was correct, but that had to be checked, not assumed.
- I initially detoured into `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview) looking for the site-visit/re-review answer, since its text mentions "a fourth page covering the ongoing side of the same checks, re-run rather than one-off" without naming it. That page turned out to be about the one-time onboarding gate (sanctions, code of conduct, disqualification) and doesn't itself contain the site-visit or review-cadence figures — those live only in the origin/value/goods matrix under `sec-hard-diligence`. The overview's unnamed "fourth page" was a red herring for this question; worth not chasing it further next time.
- The three-qualifier lookup (origin/value/goods) is clean once you find the three legend pages, but nothing on the `sec-hard-diligence` table itself points you to the legends first — you have to notice the row addresses are coded (`o4-value-w1-goods-k2`) and go find what the codes mean before picking a row. Easy to misfire by guessing a row from the plain-language description alone.
