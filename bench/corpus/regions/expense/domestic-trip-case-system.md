---
id: domestic-trip-case-system
name: "How the claim system applies domestic trip caps"
kind: system
one_liner: "What the trip claim system fills in automatically for lodging and allowance, and where it gets it wrong if a field is left blank"
parent: sec-domestic-trip-cases-1
---
# How the claim system applies domestic trip caps

The claim system reads the city entered against each lodging night and applies the matching cap automatically — 100,000 KRW for Seoul or Busan, 80,000 KRW everywhere else — without the traveller having to look the figure up. The daily allowance of 20,000 KRW is applied once per calendar day of the trip, independent of lodging.

For multi-stop trips it checks each night's city separately, exactly as the caps require, rather than averaging across the trip. For own-car legs it multiplies the logged distance by 300 KRW per km and adds any toll lines entered separately.

**If the city field on a lodging night is left blank, the system defaults to the 80,000 KRW cap rather than rejecting the entry — so a Seoul or Busan night filed without the city set loses 20,000 KRW silently, with no error to flag it.** Always confirm the city field is populated before submitting, particularly on trips typed in quickly after a long day of travel.

Cancelled legs and their refunds are not reconciled automatically; those still have to be reported by hand within the usual window.
