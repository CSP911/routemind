1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Dinner with a client, about 700,000 won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client dinner sounds like an entertainment expense" --member /v1/nodes/sec-hard-threshold "if this is really a procurement/contract matter, approval threshold depends on amount, category, and term" --member /v1/nodes/purchase-request "quotes requirement lives here if it's a purchase"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_43ec90 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

2. Answer

The department head signs it off. No competing quotes are needed (Competing quotes: none). Delegation limit for this row is 1,050 thousand KRW; working days to expect: 4.

3. Source

/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

4. Notes

The question reads like an expense question ("dinner with a client") glued to a procurement-sounding phrase ("locked in for three years"), and my first instinct was to split it between the expense area (client entertainment) and procurement (contract term). It turned out the three legend tables (category/amount/term) are built exactly to catch this: "dinner with a client" is explicitly listed as category C4 in the category legend, "about 700,000 won" is explicitly V1 in the amount legend, and "locked in for three years" is explicitly M3 in the term legend — all three phrases are lifted almost verbatim from the question, which made it obvious once I found the legends but was not obvious from the region list alone (procurement's "why pick this row" text talks about purchases, vendors, and contracts, not client dinners). The real trap was the threshold table's three-version history: the revision legend warns that reaching for the current table is wrong for anything dated before 2026-01-01, and since today is 2026-09-21 the current three-qualifier table (sec-hard-threshold) is correct — but I made a point of checking the revision legend rather than assuming, since that page exists specifically because the oldest version doesn't announce it's been superseded. I never actually opened the expense-area member I'd put in the overlay (client dinner as an expense claim); the category legend made clear this dinner, because it's a recurring/contracted arrangement rather than a one-off reimbursed meal, is scored as a procurement threshold question, not an expense-report question.
