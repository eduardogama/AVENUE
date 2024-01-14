FROM python:3.11-alpine

MAINTAINER Eduardo S. Gama "eduardogama72@gmail.com"


RUN adduser -D steering
USER steering
WORKDIR /home/steering

ENV PATH="/home/steering/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

COPY --chown=steering:steering *.py /home/steering/


COPY --chown=steering:steering .env /home/steering/
COPY --chown=steering:steering requirements.txt /home/steering/

RUN pip3 install -r requirements.txt


CMD [ "python3", "app.py" ]
