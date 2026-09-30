1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W1, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "origin/value/goods codes and site-visit + review-frequency sound like vendor risk/procurement diligence thresholds"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_15e40a --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body
```

2. **Answer**
Site visit: no.
Re-review interval: every 36 months.
(Also on the row, for completeness: screening score required 78, financial statements not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body — confirms which of the three diligence table versions is in force for today's date (2026-09-20/21)
- /v1/nodes/sec-hard-diligence — the current diligence table (in force from 2026-01-01), used to locate the exact O4/W1/K1 row
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body — the row itself, contains the answer

4. **Notes**
The domain-area table's one-line description for `/v1/regions/procurement` doesn't mention "due diligence," "premises," or "site visit" at all — it only advertises approval thresholds by category/amount/term. I picked it anyway because origin/value/goods codes and vendor risk screening are procurement-shaped concepts, and it turned out to be right, but a narrower reading of that description could have sent me hunting elsewhere first.

The real hazard was version drift: this subject has three supersized versions of the same table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), each covering a different date range, and the oldest one carries no notice that it was ever replaced. The legend-revision page is explicit that reaching for the newest is wrong for anything dated before 2026-01-01 — since today is 2026-09-20/21, the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct, but I made a point of reading the revision-legend before trusting that rather than assuming "current" was safe by default. Had the question been dated in 2025, the right source would have been `hard-diligence-v2` instead, and grabbing the current table there would have silently given the wrong site-visit/review-interval figures.

Also worth flagging: `overlay close --used` reported the three addresses I named as "reached" rather than "member," since I never formally added them to the overlay with `overlay add` — I only ever added `/v1/regions/procurement` as a member and then drilled down via plain `table`/`read` calls. The close still succeeded and recorded them correctly, but the working set discipline described in the tool's instructions (add/remove members with reasons as you narrow) wasn't fully exercised here since the path to the answer was a single unambiguous drill-down once the right table was open.
