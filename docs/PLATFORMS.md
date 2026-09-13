# Where it runs

The service is three Linux containers, so it is identical on every host Docker runs on. What differs
is the handful of pieces that run on your own machine instead — and on Windows, three of them do.

macOS, Linux and Windows. The service is three Linux containers, so it is identical on every host
Docker runs on; what differs is the handful of pieces that run on your own machine instead.

| | macOS | Linux | Windows |
|---|---|---|---|
| The three containers | yes | yes | yes — Docker Desktop, WSL2 backend |
| The map, in a browser | yes | yes | yes |
| `mcp/knowledge_mcp.py` | yes | yes | yes, natively — no WSL needed |
| `install.sh`, `check/*` | yes | yes | from WSL or Git Bash |

The MCP server is one file, stdlib only, and runs on **any python 3.7 or newer** — checked against
3.7, 3.8, 3.9, 3.11, 3.12 and 3.14. That includes Windows python, with no WSL and nothing to install.

Three things differ, and only the first one bites during normal use.

1. **Write `python`, not `python3`,** in every MCP config below. On Windows `python3` is usually not
   a program at all: it is an alias that opens the Microsoft Store. Give the script an absolute path
   too, unless your client lets you set a working directory.
2. **Run `install.sh` and anything in `check/` from WSL or Git Bash.** They are POSIX shell and there
   is no PowerShell port. Docker Desktop itself is driven normally from either.
3. **Let git give you the repository's own line endings.** `.gitattributes` pins them to LF, so a
   plain `git clone` is right even with `core.autocrlf=true` set globally. Unpacking a zip made on
   Windows, or overriding those attributes, turns `ontology/entrypoint.sh` into CRLF — and the
   container then refuses to start with `no such file or directory` naming a file that is plainly
   there, because the kernel read its shebang as `/bin/sh\r`.

Under WSL, keep the clone inside the WSL filesystem rather than under `/mnt/c`. The ontology container
runs as a fixed uid:gid and commits into `data/repo` through a bind mount, and a Windows-mounted path
does not model POSIX ownership the way that needs.

---

Back to [the README](../README.md).
