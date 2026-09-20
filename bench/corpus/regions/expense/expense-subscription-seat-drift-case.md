---
id: expense-subscription-seat-drift-case
name: "Seat drift left unadjusted"
kind: case
one_liner: "A worked case where a team licence kept billing for seats three people had left months before"
parent: sec-subscription-lifecycle
---
# Seat drift left unadjusted

A twelve-seat team licence was registered when the team was at full headcount. Over five months, three people rotated off the project. Nobody removed their seats from the vendor console, and nobody flagged the change to the registry.

## What was found
- The licence kept billing for 12 seats every month at the full per-seat rate.
- The registry's seat count field still read 12, unchanged since registration — it had never been an auto-tracked figure, only a manual one.
- The quarterly audit that should have caught it had lapsed after the previous budget owner left without a named replacement.

## What ran
The team lead filed a seat adjustment removing the three unused seats and attached a variance note to the monthly budget report, explaining the overspend as a lapsed audit rather than new discretionary spend.

**The vendor does not refund past months for seats that sat unused — the adjustment only stops future billing.** The five months of excess seats were absorbed as sunk cost against the team's budget line.

The lapse traced back to the ownership gap: no replacement had been named when the previous owner left, so the audit cycle had nobody driving it.
