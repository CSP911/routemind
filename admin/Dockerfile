# The operator's screen. No repository, no git, and — deliberately — no docker socket: it prepares a
# backbone and hands back the command, rather than running one itself. See admin/server.py.
FROM python:3.12-slim
WORKDIR /app
COPY admin/server.py /app/server.py
COPY admin/static/ /app/static/
RUN chmod -R a+rX /app
ENV PORT=8090 PYTHONUNBUFFERED=1 HOME=/tmp
EXPOSE 8090
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8090/healthz', timeout=2).status==200 else 1)"
CMD ["python3", "/app/server.py"]
