# The exchange. No repository, no git, no ontology — so none of what the backbone image carries.
#
# It reuses the backbone's own peer client rather than having one of its own. Reading a peer means
# telling three answers apart — it said no, I could not reach it, I could not read what it sent — and
# a second implementation of that would be a second thing to get wrong, in the one place where being
# wrong takes the absence rule down at every backbone attached.
FROM python:3.12-slim
RUN pip install --no-cache-dir pyyaml==6.0.2
WORKDIR /app
COPY exchange/server.py /app/server.py
COPY ontology/service/peers.py /app/peers.py
RUN chmod -R a+rX /app
ENV EXCHANGE_MEMBERS=/data/members.yaml PORT=8110 PYTHONUNBUFFERED=1 HOME=/tmp
EXPOSE 8110
HEALTHCHECK --interval=15s --timeout=3s --retries=5 CMD python3 -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8110/healthz', timeout=2).status==200 else 1)"
CMD ["python3", "/app/server.py"]
