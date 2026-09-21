1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W3, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - in force since 2026-01-01, matches today's date 2026-09-21" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which version is in force for today's date" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due diligence pages fit together, may clarify premises visit / review frequency terminology"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f186bc --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

2. Answer:
Yes, a site visit is required. The file is re-reviewed every 12 months.

3. Source:
/v1/nodes/hard-diligence-legend-revision/body (confirms which of three due-diligence table versions applies to today's date)
/v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body (the row itself: Site visit = yes, Re-review interval = every 12 months)

4. Notes:
The procurement table listed three due-diligence documents side by side (sec-hard-diligence, hard-diligence-v2, supplier-due-diligence) with no obvious flag that they were time-limited versions of the same subject — it would have been easy to just grab sec-hard-diligence because it's labeled "current" without checking why the other two exist. Opening hard-diligence-legend-revision confirmed that's the right call for today's date (2026-09-21 falls in the "2026-01-01 onwards" band), but the legend explicitly warns that the same three-value question dated in 2025 would need hard-diligence-v2 instead — an easy trap if the question's date isn't checked against the table's effective range. Also worth noting: the row address for O3/W3/K2 wasn't itself listed as a member of the overlay (only the parent table sec-hard-diligence was), so the close command flagged it as "reached" rather than a named member — harmless here since the parent table was the deliberate anchor, but worth remembering that reading into an unlisted child address is tracked differently.
