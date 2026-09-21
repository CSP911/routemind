1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, KRW 60,000,000, made-to-spec: is a site visit required, and how often is the supplier file reviewed again?" --member /v1/regions/procurement "procurement table covers approval thresholds by amount/category, likely also site visit and review cadence rules"
./bench/rmcli.py overlay remove --id ov_2026-09-20_1af2f1 --address /v1/nodes/contract-custody --why "not about site visits or review cadence"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1af2f1 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body
```

(I also ran `./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body` to check which of the three due-diligence table versions applies to today's date, before the table/read sequence above.)

2. **Answer**

No, a site visit is not required. The supplier's file is re-reviewed every 24 months.

(Underlying figures: screening score required 83, financial statements from last year — given for completeness, not asked.)

3. **Source**

- `/v1/nodes/hard-diligence-legend-revision/body` — confirms the current table (in force from 2026-01-01) is the right one to use for a question dated 2026-09-20/21
- `/v1/nodes/hard-diligence-legend-origin/body` — Da Nang → origin O4
- `/v1/nodes/hard-diligence-legend-value/body` — sixty million won → value W2
- `/v1/nodes/hard-diligence-legend-goods/body` — "something made to our spec" → goods K2
- `/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body` — the row itself: Site visit = no, Re-review interval = every 24 months

4. **Notes**

- There are three separate versions of the supplier due-diligence rules (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page is explicit that reaching for the newest one is only correct for dates on or after 2026-01-01 — for anything in 2025 the answer would have come from `hard-diligence-v2` instead. Since today is 2026-09-20, the current table applied, but it would have been easy to skip that check and just grab whichever table looked newest.
- The procurement table also surfaces a *different*, older-looking "where to start" node (`sec-supplier-due-diligence`) that describes due diligence in prose (sanctions checks, code of conduct, disqualification triggers) with no mention of site visits or numeric re-review intervals. It's a plausible-looking dead end if you stop there instead of continuing to the actual indexed table (`sec-hard-diligence`), which is the only place site-visit/re-review figures actually live.
- The three qualifiers (origin/value/goods) mapped cleanly and unambiguously to O4/W2/K2 — "sixty million won" and "something made to our spec" are exact, verbatim matches in the legends, not nearest-fit judgment calls, so there's no rounding ambiguity to flag there.
- Minor housekeeping snag, not a content issue: an early `overlay remove` call on `/v1/nodes/contract-custody` returned a 404 ("not in this overlay") even though that address was printed as a member of the overlay right after creation. Didn't chase it since it didn't block reaching the answer, but the working set ended up not accurately pruned as a result.
