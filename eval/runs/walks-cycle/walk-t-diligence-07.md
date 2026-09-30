1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence

2. Answer
Supplier due diligence has been written three times (rewritten twice):
- Version 1 (original): in force until 2024-07-01. No start date is stated for it — it is the oldest version and says nothing about being replaced.
- Version 2: in force from 2024-07-01 to 2025-12-31.
- Version 3 (current): in force from 2026-01-01 onwards.

3. Source
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-v2/body
/v1/nodes/supplier-due-diligence/body
/v1/nodes/sec-hard-diligence (table header)

4. Notes
The procurement area table's own description says the current tables have been in force "since 2026-01-01" and calls older pages "superseded," which reads as if there's just one prior version — easy to stop there and undercount. The legend-revision page at /v1/nodes/hard-diligence-legend-revision/body is the one place that states outright there are three versions and warns that the oldest "says nothing at all about having been replaced" (confirmed when reading its body — no revision notice anywhere in it) and that a 2025-dated question needs the middle version, not the newest or oldest. Easy to go wrong two ways here: reading only the current table (sec-hard-diligence) and missing the two older versions entirely, or finding hard-diligence-v2 and assuming that's the *first* rewrite when it's actually the second version, with an even older unlabeled one underneath it. The original version's body has no explicit start date — it's presumably in force from whenever the policy began until 2024-07-01, but the source never gives an actual starting date, only an end date.
