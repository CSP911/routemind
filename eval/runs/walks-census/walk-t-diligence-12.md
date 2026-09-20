## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/hard-diligence-v2
./bench/rmcli.py table /v1/nodes/sec-hard-diligence

## Answer

Two versions are needed, one per claim year:

- **2023 claims → the oldest version** (in force until 2024-07-01, one qualifier, no origin/value split).
  Screening required: three checks —
  1. A sanctions and ownership check against the current restricted-party lists.
  2. A supplier code of conduct acknowledgement, signed by the supplier.
  3. A basic disqualification screen (has this entity or its owners been flagged before).
  A sanctions hit or a refused code of conduct stops registration outright with no delegated override (not team lead, division head, or CEO). A hit found after registration is treated the same as one found before: the vendor is suspended and open POs frozen.

- **2025 claims → the second version** (in force 2024-07-01 to 2025-12-31, two qualifiers: origin × value).
  Screening required is read off a matrix keyed by supplier origin (O1–O4) and contract value band (W1–W4), giving one code per cell (30 through 45, filled in order O1→O4 down, W1→W4 across). The document states the checks required, documents to collect, and re-review interval "beyond the column above" followed the original (pre-2024) rule unchanged — i.e. the same three checks as the 2023 version, just apportioned/intensified per the origin×value cell rather than applied uniformly.

## Source
- /v1/nodes/hard-diligence-legend-revision/body — establishes there are three versions and which date maps to which
- /v1/nodes/sec-supplier-due-diligence (table) — needed to locate the oldest version's address, which the procurement table alone does not list
- /v1/nodes/supplier-due-diligence/body — the 2023 (oldest) version, its three checks
- /v1/nodes/hard-diligence-v2/body — the 2025 (middle) version, the origin×value matrix

## Notes
- The procurement region table lists the legend, the v2 file, and the current (2026) file directly, but **not** the oldest version's address — it has to be reached through `sec-supplier-due-diligence`'s "where to start" table instead. Missing that step, I'd have wrongly concluded only two versions were reachable from procurement and picked the wrong one for 2023.
- The obvious trap here is reaching for `sec-hard-diligence` (marked "THE CURRENT ... TABLE") for the 2025 claims. It isn't current until 2026-01-01; the legend page is explicit that 2025 is the one case where grabbing either extreme (oldest or current) is wrong, and the middle version (`hard-diligence-v2`) is required instead.
- The v2 matrix gives numeric codes (30–45) per origin×value cell but I could not find any legend translating those codes into concrete check descriptions, nor confirmation that the O1–O4/W1–W4 category definitions from the *current* table (`hard-diligence-legend-origin`, `hard-diligence-legend-value`, linked only under `sec-hard-diligence`) apply retroactively to this 2024–2025 version. I did not assume they carry back, since the whole point of the legend-revision page is that nothing should be assumed across versions. Take the "30–45" codes as: a value exists and varies by cell, not as a decoded meaning — that part is not found.
