# The MCP server alone, over stdio. Not part of `docker compose up` — that runs the ontology, the
# map and the exchange, and the MCP server is normally launched by the client, on the client's
# machine, as one python file with nothing to install.
#
# This image exists for directories and harnesses that want to start a server and introspect it
# without standing up a backbone first. That works: with nothing at `--api`, `initialize` and
# `tools/list` still answer, and the area list a tool description would have carried is replaced by
# the reason it could not be fetched. An agent is told why rather than handed an empty table.
#
#   docker build -t routemind-mcp -f mcp/Dockerfile .
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
