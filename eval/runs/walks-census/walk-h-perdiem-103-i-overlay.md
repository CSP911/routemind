1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Tokyo team manager, 3 weeks: hotel per-night cap and receipt threshold" --member /v1/regions/expense "business trip lodging rates and receipt rules likely here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b0e1f5 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 171 USD per night. A receipt is required above 31 USD.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

4. **Notes**: The overseas per-diem subject has three versions covering different date ranges, and the table itself warns that reaching for the newest is wrong for dates before 2026-01-01 — today (2026-09-21) is past that, so the current table (`sec-hard-perdiem`) is correct, but this is an easy trap for any question not dated in the current window. The table is indexed by three separate legends (grade, band, stay) rather than by plain words, so "team manager," "Tokyo," and "three weeks" each had to be translated (to G2, B1, S4 respectively) before the right row could be addressed — skipping any one of the three legends would have picked the wrong row silently rather than erroring. The overlay `close --used` call reported all five addresses as "reached" rather than "used," because none of them were direct members of the overlay (only the top-level `/v1/regions/expense` table was) — the tool still recorded the close as answered, so this looks like informational bookkeeping rather than a failure, but it's worth flagging since the wording suggested something might be wrong.
