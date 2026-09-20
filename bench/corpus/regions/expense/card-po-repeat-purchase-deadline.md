---
id: card-po-repeat-purchase-deadline
name: "Reporting window once repeat purchases cross the threshold"
kind: deadline
one_liner: "How soon a run of small orders from one supplier has to be flagged once their monthly total crosses the flat quote threshold"
parent: sec-card-or-purchase-order
---
# Reporting a repeat purchase once it crosses the threshold

## What crossing looks like
A string of small orders from the same supplier can add up past the 500,000 KRW quote threshold within a single month even though no single order ever needed a quote on its own. The threshold is checked against the running total, not each purchase in isolation.

## The window
**Once the running total crosses the threshold, the order that tips it over has to be flagged to procurement within 5 working days** — not backdated to when the first order in the run went through. Flag it late and the whole month's run from that supplier is treated as if a quote should have been obtained from the start, which is far harder to unwind after the fact than to catch on the day.

## What flagging does
Procurement checks whether the run needs a retrospective quote or whether it converts cleanly to a PO for anything still outstanding. Either way, the flag is what starts that review — the system totalling the spend on its own doesn't.

## The trap
**Four orders that each clear the card with no quote in sight can still owe one the moment the fourth lands.** Nothing on the card statement marks that crossing for you; it only shows up if someone is watching the supplier total, not just each receipt as it comes in.

Whether that same 500,000 KRW line ever needs revisiting over a longer run than one month is worth checking against the quote threshold table.
