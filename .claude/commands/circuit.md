---
description: Read another RouteMind for this session only — nothing is written on either side
argument-hint: <url> <token> [name]
---

Open a circuit to the RouteMind at the address below and show what it shares.

    $ARGUMENTS

Call `knowledge_circuit` with `op: "open"`, taking the first argument as `url`, the second as
`token`, and the third — if there is one — as `name`. Then read `/v1/circuits/<name>/regions` with
`knowledge_table` and show the areas it prints.

Do not invent any address. Follow only what its tables print, exactly as printed, the same discipline
as this backbone's own.

If either the address or the token is missing, say what is needed and stop — do not guess at one, and
do not fall back to reading this backbone instead. A circuit that silently answers from the wrong
ontology is worse than no answer: the rows look the same.

A circuit lasts for this connection, writes nothing on either side, and is yours alone. It reads only
the areas their owner set `export` on — see `docs/CIRCUIT.md`.
