# The MCP server alone, over stdio.
#
# **This is not how you run RouteMind.** That is `./install.sh`, which brings up the ontology, the
# map and the exchange through `docker compose`; the MCP server is normally launched by the client,
# on the client's machine, as one python file with nothing to install.
#
# It is at the repository root because that is where MCP directories and harnesses look for one —
# they build the image, start it, and introspect it. Glama listed this server and then said "this
# server cannot be deployed", which is what a directory says when it cannot find a way to start the
# thing it is scoring.
#
# This image exists for directories and harnesses that want to start a server and introspect it
# without standing up a backbone first. That works: with nothing at `--api`, `initialize` and
# `tools/list` still answer, and the area list a tool description would have carried is replaced by
# the reason it could not be fetched. An agent is told why rather than handed an empty table.
#
#   docker build -t routemind-mcp .
#   docker run -i --rm routemind-mcp                       # introspection only
#   docker run -i --rm -e KNOWLEDGE_API=http://host.docker.internal:8080/api/knowledge routemind-mcp
#
# stdio, so `-i` and no `-t`: the protocol is JSON-RPC on stdin and stdout, and a tty would put a
# terminal in the middle of it.
FROM python:3.12-slim
WORKDIR /app
# Stdlib only — there is nothing to install, and that is the point of the file being one file.
COPY mcp/knowledge_mcp.py /app/knowledge_mcp.py
# Where the ontology is. The default is the address the shipped compose publishes, reachable from a
# container on the host's network; override it for anything else.
ENV KNOWLEDGE_API=http://host.docker.internal:8080/api/knowledge \
    KNOWLEDGE_ACTOR=mcp \
    PYTHONUNBUFFERED=1
ENTRYPOINT ["python3", "/app/knowledge_mcp.py"]
