# Walk h-threshold-033-d

## Commands
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body
```

## Answer
For category C1, amount V4, term M4 (delegation limit 100015 thousand KRW), the sign-off required is
the **CFO**. Yes, other prices are required first: **three competing quotes plus a written comparison**
before approval.

## Source
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
- /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m4/body (the answer itself)

## Notes
The procurement region lists three separate versions of the approval-threshold subject
(`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and a naive search could easily land on
the wrong one — the legend-revision page explicitly warns that "the oldest says nothing at all about
having been replaced," so reaching for whichever table appears first or looks newest without checking
is a real trap. Since today's date (2026-09-20) falls after 2026-01-01, the current table
(`sec-hard-threshold`) is correct. Once inside the current table, the row naming convention
(`hard-threshold-row-category-c1-amount-v4-term-m4`) matched the question's C1/V4/M4 codes directly,
so no legend lookup (amount/category/term definitions) was needed to identify the row — the codes given
in the question were already the table's native indexing scheme.
