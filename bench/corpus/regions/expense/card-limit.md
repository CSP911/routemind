---
id: card-limit
name: "Card limits"
kind: table
one_liner: "Per-transaction and monthly caps, and the merchant categories that are blocked outright"
injected_by: operator
parent: corp-card
---
# Card limits

Two caps run at once — one per transaction and one per month — and they are set by grade. The figures
are in the table below.

## How the two interact
The per-transaction cap is a hard decline at the terminal. The monthly cap is not: it is checked at
the statement, and going over it does not stop the payment, it produces a conversation. So the
transaction cap is the one you find out about immediately and the monthly cap is the one you find out
about later.

## When something is over the cap
Do **not** split it. Two payments for one purchase is the thing the rule is actually about, and it is
visible on the statement — same merchant, same day, two charges that sum to the thing you bought.
The right route is a purchase request, which also gets you the quotes the amount band requires.

## Raising a limit
Temporarily, for a specific reason — a conference, a bulk order, a trip with prepaid lodging. Ask the
office & purchasing desk before the spend, not after the decline. A raise is recorded against the
reason and reverts at the end of the month.

## Categories that will decline
Entertainment venues, duty free, gift vouchers, jewellery, online games. Two of these surprise people:
**gift vouchers** are blocked because they are cash equivalents and cannot be evidenced to a purpose,
and **duty free** is blocked even on an approved overseas trip. If you need either, it goes through a
purchase request with the reason written down.

Client spending has a cap of its own on top of these → Entertainment.
