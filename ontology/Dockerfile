# Knowledge ontology API. Build context is the repository root, so that `seed/` is shared with nothing
# else to drift against — one empty ontology, in one place.
#
# The data repository is NOT baked in: it is bind-mounted, and writes commit into it, so the container
# runs as the uid that owns the directory (set `user:` in compose).
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir pyyaml==6.0.2
WORKDIR /app
COPY ontology/service/ /app/service/
COPY ontology/entrypoint.sh /app/entrypoint.sh
COPY seed/ /app/seed/
# The container does not run as root, and COPY carries the host's modes — a checkout made under
# `umask 077` lands here as 0600 and nothing in /app can be read at all. Set them here instead of
# trusting whatever the build host happened to have.
#
# `X` adds `x` only where something already has it, so the ENTRYPOINT needs its own line: a checkout
# on a filesystem that does not carry the bit — Windows, a zip, a share — hands COPY a file that is
# not executable, and the container then fails to start on a script that is plainly there. The README
# has carried a `chmod +x` workaround for exactly this; it belongs in the build, not in a person's
# troubleshooting.
RUN chmod -R a+rX /app && chmod +x /app/entrypoint.sh
ENV ONTOLOGY_DATA=/data/repo ONTOLOGY_PUBLISH=/data/publish PORT=8100 PYTHONUNBUFFERED=1 HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null
EXPOSE 8100
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8100/healthz', timeout=2).status==200 else 1)"
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python3", "/app/service/server.py"]
