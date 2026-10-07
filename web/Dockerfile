# Knowledge Web — the map and a proxy. No database, no build step, no node.
FROM python:3.12-slim
WORKDIR /app
COPY web/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY web/app.py /app/app.py
# The MCP server ships with the web image: its formatter is what renders "what the agent is handed"
# in the popup, so that the screen and a connected agent cannot disagree about it.
COPY mcp/ /app/mcp/
COPY static/ /app/static/
# See ontology/Dockerfile: COPY carries the build host's modes, and a 0600 static tree serves 500s.
RUN chmod -R a+rX /app
ENV KNOWLEDGE_STATIC=/app/static KNOWLEDGE_API_URL=http://ontology:8100 PORT=8080 PYTHONUNBUFFERED=1
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/api/app-config', timeout=2).status==200 else 1)"
CMD ["python3", "/app/app.py"]
