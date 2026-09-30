1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O1, value W3, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/site visit and review frequency likely tied to procurement vendor risk classification by origin, value, goods category"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_016b9a --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 12 months. (Screening score required: 39; financial statements: last two years, for context.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is current for today's date)
/v1/nodes/sec-hard-diligence/body (current table, in force from 2026-01-01, located the exact row)
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body (the row itself — site visit and re-review interval)

4. **Notes**:
The question's own wording ("origin O1, value W3, goods K2") already matched the row's qualifiers exactly, so no legend lookup was needed to translate plain-language descriptions into O/W/K codes — that shortcut felt slightly risky (skipping the legend files for origin/value/goods) but the question gave codes directly rather than descriptions, so there was nothing to translate.

The near-miss was on versioning: `sec-hard-diligence` is the third rewrite of this subject (`supplier-due-diligence` → `hard-diligence-v2` → `sec-hard-diligence`), and the legend-revision page is explicit that reaching for the newest one is wrong for any question dated before 2026-01-01. Today is 2026-09-20/21, so the current table is correct here, but this is clearly a place the walk is designed to trip you up on a different date. Checked the revision-legend page before trusting the "CURRENT" label in the table description, rather than taking that label at face value.

The overlay's `close` output flagged the three addresses actually used as "reached ... answered from somewhere the overlay never named" — I had only added the parent `/v1/regions/procurement` table as a working-set member and then drilled down via `table`/`read` without formally `overlay add`-ing each intermediate address. Functionally harmless here since the close still recorded them, but worth noting the working set didn't track the walk precisely.
