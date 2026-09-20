# Walk h-threshold-231-d

## Commands
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body
```

## Answer
For category C3, amount V4, term M2: the **division director** signs it off. Yes — three competing
quotes plus a written comparison are required before approval (delegation limit 100045 thousand KRW,
12 working days to expect).

## Source
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions is current for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body (the answer itself)

## Notes
The procurement table warns up front that the threshold subject has been written three times, with the
current version only valid from 2026-01-01 onward, and that "the oldest says nothing at all about having
been replaced." That's the trap: naively reading `hard-threshold-row-category-c3-amount-v4-term-m2` without
checking the legend first could actually still be correct today (2026-09-21 falls after 2026-01-01), but
I would not have known that without reading the revision legend — the row address itself gives no hint it's
one of three competing versions. Checked the legend before trusting the row, which confirmed the current
table (`sec-hard-threshold`) is the right one to use.

The question's codes (C3, V4, M2) were given directly, so no need to consult the category/amount/term
legends to translate plain-language qualifiers into codes — the row address matched exactly once category,
amount, and term legends' codes were assumed to correspond directly to the C3/V4/M2 naming, which the table
listing confirmed.
