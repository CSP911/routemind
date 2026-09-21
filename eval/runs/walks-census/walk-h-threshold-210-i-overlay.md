1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, roughly 3 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by amount/category and whether competitive quotes are required" --member /v1/regions/expense "business trip cost rules, may cover travel booking or reimbursement"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body
./bench/rmcli.py table /v1/nodes/sec-corporate-travel-agency
./bench/rmcli.py read /v1/nodes/expense-travel-agency-overview/body
./bench/rmcli.py overlay close --id ov_2026-09-21_694f36 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body

2. **Answer**: The team lead signs it off. Yes, two competing quotes are required before approval. (Delegation limit for this row is 5,036 thousand KRW; expect 5 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body

4. **Notes**: The three legend tables map the plain-language description straight onto the row: "flights and hotels" = category C3, "roughly 3 million won" = amount V2, "just the once" = term M1 — all exact matches, no nearest-entry judgment call needed. The current threshold table (`sec-hard-threshold`, in force from 2026-01-01) is the right one for today's date (2026-09-21); I did not need to touch the superseded `hard-threshold-v2` or the legend-revision warning page, since there was no ambiguity about which version applies.

I did detour into the expense region's corporate travel agency section, since flights/hotels are normally booked through that agency and I wanted to check whether an agency-booked fare (which "quotes against the fare and lodging caps" per `expense-travel-agency-overview`) substitutes for the "two competing quotes" requirement in the procurement threshold row. That page describes a different mechanism — a fare/lodging cap check, not a competing-quotes requirement — and nowhere states it overrides or satisfies the procurement threshold table's quote requirement. I treated it as not applicable and stuck with the threshold row's own numbers, but this is the one place the walk could plausibly have gone sideways: someone could mistake "the agency already checked the fare cap" for "no other prices needed," which the sources don't actually support.
