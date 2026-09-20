## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
    ./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
    ./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
    ./bench/rmcli.py read /v1/nodes/sanctions-ownership-checks/body
    ./bench/rmcli.py read /v1/nodes/sec-hard-diligence
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Stuttgart → origin O2, three hundred million won → value W3, office consumables → goods K1; row O2/W3/K1 of the current supplier due-diligence table.)

## Source

- /v1/nodes/sec-hard-diligence (current table, in force from 2026-01-01 — confirms this is the applicable version for today, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → K1)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k1/body (Site visit: yes; Re-review interval: every 12 months)

## Notes

- Went down a side path first: /v1/nodes/sec-supplier-due-diligence and its "where to start" page describes four sub-pages (sanctions/ownership, code of conduct, disqualification triggers, and an "ongoing/re-run" page), and /v1/nodes/sanctions-ownership-checks/body does state "re-run the check annually" — but that's the *sanctions screening* cadence, not the site-visit/file re-review cadence the question actually asks about. It would have been an easy, plausible-looking wrong answer (also "annually," so it happens to match, but for the wrong reason and without the site-visit fact at all). The real answer lives one level down, in the origin/value/goods row table, not in the narrative onboarding pages.
- The three legends (origin, value, goods) are exact-phrase lookups ("a firm in Stuttgart," "three hundred million won," "just office consumables") that map 1:1 to the question's wording — almost too neatly, which made me double check I hadn't misread a different row. Confirmed by reading all three legends independently before combining into the row address.
- sec-hard-diligence's one-liner explicitly states it is "in force from 2026-01-01," and today is 2026-09-20, so no need to consult the superseded hard-diligence-v2 or the legend-revision warning page — current table applies cleanly with no boundary-date ambiguity.
