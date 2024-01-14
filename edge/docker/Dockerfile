FROM python:3.12-alpine

RUN pip3 install --upgrade pip


WORKDIR /app

ENV PATH="/app/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

ENV CACHE_ADDR="0.0.0.0"
ENV CACHE_PORT="30001"
ENV CACHE_SIZE="1000000000"
ENV CONTENT_TYPE_LATEST="text/plain; version=0.0.4; charset=utf-8"

RUN apk add \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils

COPY --chown=app:app ./src/DiskLRUCache.py /app/
COPY --chown=app:app ./src/lrucache.py /app/
COPY --chown=app:app ./src/app.py /app/
COPY --chown=app:app requirements.txt /app/


RUN pip3 install -r requirements.txt


ENV FLASK_APP=app.py

CMD python app.py
