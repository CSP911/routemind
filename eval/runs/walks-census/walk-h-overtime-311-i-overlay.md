1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "2am, three hours, at a client's office: overtime multiplier and minute rounding?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place - in force since 2026-01-01, matches late-night hours at a client site" --member /v1/nodes/hard-overtime-legend-revision/body "warning that overtime rate has three versions with different dates - need to confirm which version applies to today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body
./bench/rmcli.py overlay add --id ov_2026-09-21_8943fe --address /v1/nodes/hard-overtime-legend-day/body --why "maps 'two in the morning' to day D4"
./bench/rmcli.py overlay add --id ov_2026-09-21_8943fe --address /v1/nodes/hard-overtime-legend-hours/body --why "maps 'three hours' to hours H2"
./bench/rmcli.py overlay add --id ov_2026-09-21_8943fe --address /v1/nodes/hard-overtime-legend-place/body --why "maps 'out at a client's office' to place P2"
./bench/rmcli.py overlay add --id ov_2026-09-21_8943fe --address /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body --why "the D4/H2/P2 row: multiplier 2.79x, rounding to nearest 10 minutes"
./bench/rmcli.py overlay close --id ov_2026-09-21_8943fe --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

2. Answer

Multiplier: 2.79x
Rounding: to the nearest 10 minutes

3. Source

/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

4. Notes

The revision-warning page was the thing that stopped me from guessing wrong: the overtime rate subject has three superseded versions with different indexing schemes (one qualifier, then two, then three), and the current three-qualifier table only applies from 2026-01-01 onward. Today (2026-09-21) is inside that window, so `sec-hard-overtime` was the right table — but nothing on the table's own listing said so directly; only the legend-revision page states the effective dates, and it explicitly warns that the oldest version says nothing about being superseded, so a naive reader could land there and not know to look further.

The three legends turned out to be non-obvious in a way that mattered: "day D4" isn't actually about the calendar day of the week at all — the day-type legend maps "two in the morning" directly to D4, regardless of what day it is. I almost read "day" as "day of week" and started to reason about whether 2026-09-21 was a weekday, which was the wrong axis entirely; the legend is literally indexed by clock time in one of its rows. Once I saw that, the other two qualifiers were straightforward table lookups: "three hours" → H2 exactly (no rounding/nearest-match needed), "out at a client's office" → P2 exactly. All three matched listed entries exactly, so the "take the nearest entry above it" fallback in each legend was not needed here, though it's worth noting the rule exists for less clean inputs.

One shell hiccup: a loop to prune the now-irrelevant D×H×P rows from the overlay before closing was rejected by the sandbox ("Contains simple_expansion"). I left those extra rows in the overlay rather than fight the shell restriction — the `close --used` list is unambiguous about which five addresses actually answered the question, so the untrimmed overlay membership doesn't affect the answer.
