1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-business-travel-insurance-and-risk
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body

2. Answer
Approval threshold has three versions written down; a claim dated in 2025 falls in the middle version, in force 2024-07-01 to 2025-12-31 (indexed by two qualifiers: category and amount). Its sign-off table by category and amount:

| category \ amount | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| C1 | 1000 thousand KRW | 5001 thousand KRW | 20002 thousand KRW | 100003 thousand KRW |
| C2 | 1004 thousand KRW | 5005 thousand KRW | 20006 thousand KRW | 100007 thousand KRW |
| C3 | 1008 thousand KRW | 5009 thousand KRW | 20010 thousand KRW | 100011 thousand KRW |
| C4 | 1012 thousand KRW | 5013 thousand KRW | 20014 thousand KRW | 100015 thousand KRW |

Everything else (who signs, quote count, turnaround time) beyond this table followed the unchanged approval-thresholds rule until 2026-01-01. This is NOT the current table (that started 2026-01-01, three qualifiers, at /v1/nodes/sec-hard-threshold) and NOT the oldest one either (which had neither category nor term, at /v1/nodes/threshold-table).

3. Source
/v1/nodes/hard-threshold-legend-revision/body (identifies which of the three versions covers 2025 and why the date has to be checked)
/v1/nodes/hard-threshold-v2/body (the actual 2024-07-01–2025-12-31 threshold table with figures)

4. Notes
The word "claim" in the question is a red herring for the tool: RouteMind's expense region has a whole "business travel insurance and risk" sub-area built around literal insurance claims (travel-insurance-claim-deadline, travel-insurance-claim-form, etc.), and I detoured into /v1/regions/expense and /v1/nodes/sec-business-travel-insurance-and-risk to check it before ruling it out — none of those pages mention "approval threshold" or versioned effective dates, so they don't answer this question. The actual match is on "approval threshold," a phrase used verbatim only in /v1/regions/procurement's row description. Once there, the danger was reaching straight for /v1/nodes/sec-hard-threshold because it's labeled "THE CURRENT APPROVAL THRESHOLD TABLE" — but current means in force from 2026-01-01, and the claim is dated in 2025, so the current table is the wrong one. The legend-revision page explicitly calls out that mistake ("reaching for the newest is wrong for anything before 2026-01-01") and names the 2025 case as the one where either extreme (oldest or newest) is wrong — the middle version, hard-threshold-v2, is the one that applies.
