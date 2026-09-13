# The door

Who may write, and whose name goes on the change. Three modes, and the one thing they have in common
is that the **running service says which one it is in** rather than leaving it to be remembered.

`KNOWLEDGE_AUTH` picks one of three, and the **running service says which one it is in** — in its log
at startup, in `/api/app-config`, and on a chip in the screen's header. Until 2026-09-13 the only
thing that knew was this file, which is the one place a running system cannot be read from.

| | who may write | the name on a change |
|---|---|---|
| `open` *(default)* | anyone who can reach the port | whatever the browser typed — a signature |
| `token` | whoever holds `KNOWLEDGE_TOKEN`, as `Authorization: Bearer …` | still a signature |
| `proxy` | whoever your reverse proxy authenticated | **the proxy's**, and the browser gets no vote |

`open` is what every install has been and is legitimate on a network where it is acceptable. The
change is that it is now a state something states rather than a fact somebody has to remember.

**`proxy` is the only mode that produces an identity**, and it needs two halves: the header
(`KNOWLEDGE_AUTH_HEADER`, default `X-Forwarded-Email`) and the address it is believed from
(`KNOWLEDGE_AUTH_TRUSTED_PROXY`). Believing it from anywhere is *worse* than no authentication —
anybody can send one, and the record then names a person who was not there. So the service **refuses
to start** in that mode without it, and likewise in `token` mode with no secret: an operator who set a
mode decided this was meant to be closed, and coming up open instead turns a decision into a surprise.

The gate is on writes. `KNOWLEDGE_AUTH_READS=1` extends it to reads, which also means giving the
agent the secret — reads are what the MCP does, and it has no session.

Between backbones the door is different and older: **one secret per link, used in both directions**,
compared in constant time. Two things make it workable between organisations — a link refuses to
present its token over plain `http` to a public address, and `also_accept_env` keeps a second secret
good so rotating one is not a flag day. See **[PEERING.md](PEERING.md)**.

The **name** field at the top right is a signature that goes on commits and proposals, kept in that
person's own browser. **It is not a permission.**

---

## Checking it

`./check/auth-check.py` — 32 assertions, run in the web container because it needs fastapi and
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

Between backbones the door is a different and older thing — one secret per link, used in both
directions. **[PEERING.md](PEERING.md)**. Back to [the README](../README.md).
