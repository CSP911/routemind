# The door

Who may write, and whose name goes on the change. Three modes, and the one thing they have in common
is that the **running service says which one it is in** rather than leaving it to be remembered.

`KNOWLEDGE_AUTH` picks one of three, and the **running service says which one it is in** — in its log
at startup, in `/api/app-config`, and on a chip in the screen's header. Until 2026-09-13 the only
thing that knew was this file, which is the one place a running system cannot be read from.

| | who may write | the name on a change |
|---|---|---|
| `open` *(default)* | anyone who can reach the port | `KNOWLEDGE_ACTOR` (`web`) for the screen; what the client sent in `X-Knowledge-Actor` otherwise — a signature |
| `token` | whoever holds `KNOWLEDGE_TOKEN`, as `Authorization: Bearer …` | the same — still a signature |
| `proxy` | whoever your reverse proxy authenticated | **the proxy's**, and the browser gets no vote |

`open` is what every install has been and is legitimate on a network where it is acceptable. The
change is that it is now a state something states rather than a fact somebody has to remember.

**`proxy` is the only mode that produces an identity**, and it needs two halves: the header
(`KNOWLEDGE_AUTH_HEADER`, default `X-Forwarded-Email`) and the address it is believed from
(`KNOWLEDGE_AUTH_TRUSTED_PROXY`). Believing it from anywhere is *worse* than no authentication —
anybody can send one, and the record then names a person who was not there. So the service **refuses
to start** in that mode without it, and likewise in `token` mode with no secret: an operator who set a
mode decided this was meant to be closed, and coming up open instead turns a decision into a surprise.
The address judged is the connection's own: `X-Forwarded-For` is never read for it, so declare the
address your proxy connects *from*, as the web container sees it (through Docker's published port
that is usually the bridge's gateway, not `127.0.0.1`). Until 2026-11-02 the
server rewrote the address from that header, and any local process could name a declared address in
it and sign as anyone.

The gate is on writes. `KNOWLEDGE_AUTH_READS=1` extends it to reads. The map page itself is a static
shell and always loads; the data behind it is what the gate guards.

**On the screen, in token mode**, the chip at the top right says a secret is needed; clicking it, or
the first refused save, asks for `KNOWLEDGE_TOKEN` and keeps it in that browser. Until 2026-10-10 the
page itself was refused (a bare 401 in JSON) and the screen had no way to send a secret at all.

**The agent** gets the secret from the MCP server, which sends `KNOWLEDGE_TOKEN` as a bearer secret —
from its environment, or from the `.env` of the checkout it runs from. Claude Code started in this
directory therefore needs nothing more; an agent elsewhere sets `KNOWLEDGE_TOKEN` in the server's
environment. Without it an agent reads (unless reads are guarded too) but cannot place, and its walks
are not recorded.

A proxy's identity header may carry a non-ASCII name; it is read as UTF-8, so a commit is signed
"김철수", not mojibake.

Another backbone reading this one through a circuit does not come through this door: it presents
the circuit key (`KNOWLEDGE_CIRCUIT_TOKEN`) at `/v1/peers/token` and `/v1/export/…`, which the
ontology checks in constant time, and a circuit refuses to send a key over plain `http` to a public
address. See **[CIRCUIT.md](CIRCUIT.md)**.

**The name on a change, in `open` and `token` mode**, is not anyone's identity. The screen sends no
name, so everything saved from it is signed `KNOWLEDGE_ACTOR` (`web` unless .env says otherwise) —
the person who proposed a change and the person who accepted it both read `web`. Any other client
may send `X-Knowledge-Actor` (percent-encoded UTF-8, up to 64 characters of letters, digits, space,
`.`, `@`, `-`, `_`), and the MCP server sends its `--actor`; that name goes on the commit as it
was sent, and one that does not fit those rules is replaced by `KNOWLEDGE_ACTOR` without a word.
It is client-supplied: **a signature, not a permission, and not a proof of who wrote it.** Only
`proxy` mode replaces it with an identity, and there an identity longer than 64 characters is
refused rather than cut. An identity that is already an address is the commit's email as it is.

---

## Checking it

`./check/auth-check.py` — it prints how many assertions it ran; run in the web container because it needs fastapi and
uvicorn:

```sh
docker cp check $(docker compose ps -q web):/tmp/check
docker compose exec web python3 /tmp/check/auth-check.py
```

It starts `web/app.py` itself on spare ports with no ontology behind it: the gate answers **before**
anything is proxied, so "401 or not 401" is the whole question and a missing backend cannot confuse
it. Three of its assertions are about the service saying which mode it is in, because until
2026-09-13 the only thing that knew was a file in the repository.

---

Between backbones the door is the circuit key. **[CIRCUIT.md](CIRCUIT.md)**. Back to
[the README](../README.md).
